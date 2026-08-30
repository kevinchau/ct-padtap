#include <Arduino.h>
#include "lin_map.h"

// PadTap — Cybertruck WPC tap → Starlink Mini
// LIN is listen-only. Do not wire TLIN2029 TXD.
//
// Direct 48 V (default, -DPADTAP_DIRECT=1): switched raw Tesla rail.
//   Hardware LM393 + firmware latch kill the FET at 56.0 V.
// Buck 36 V (-DPADTAP_DIRECT=0): 36 V module is the Mini's supply;
//   OVLO still trips so a mis-set pot cannot pass 58 V.

#ifndef PADTAP_DIRECT
#define PADTAP_DIRECT 1
#endif

static const int PIN_LIN_RX = 20;
static const int PIN_FET = 5;
static const int PIN_VIN_ADC = 4;
static const int PIN_LED_RAIL = 6;
static const int PIN_LED_ARM = 7;

static const float VIN_DIV_TOP = 100000.0f;
static const float VIN_DIV_BOT = 10000.0f;
static const float VIN_RAIL_V = 30.0f;
static const float VIN_OVLO_V = 56.0f;        // Mini hardware ceiling
static const float VIN_OVLO_CLEAR_V = 54.0f;  // hysteresis
static const uint32_t LIN_BAUD = 19200;

enum Mode { MODE_AUTO, MODE_A, MODE_B, MODE_C };
static Mode mode = MODE_AUTO;

static bool sawVinDropOnToggle = false;
static bool sawLinToggle = false;
static bool lastLinEn = false;
static bool haveLin = false;
static bool arm = false;
static bool ovlatched = false;

static uint8_t linBuf[10];
static uint8_t linLen = 0;
static uint32_t linLastMs = 0;

float readVin() {
  const int raw = analogRead(PIN_VIN_ADC);
  const float vAdc = (raw / 4095.0f) * 3.3f;
  return vAdc * ((VIN_DIV_TOP + VIN_DIV_BOT) / VIN_DIV_BOT);
}

bool linEnableBit(const uint8_t *data, uint8_t n) {
  if (LIN_ENABLE_PID == 0 || n <= LIN_ENABLE_BYTE) return lastLinEn;
  bool bit = (data[LIN_ENABLE_BYTE] & LIN_ENABLE_MASK) != 0;
  if (LIN_ENABLE_INVERT) bit = !bit;
  return bit;
}

void parseLinByte(uint8_t b) {
  uint32_t now = millis();
  if (now - linLastMs > 8) linLen = 0;
  linLastMs = now;
  if (linLen < sizeof(linBuf)) linBuf[linLen++] = b;

  // Very small LIN-ish frame: 0x55 sync then PID then data.
  if (linLen >= 3 && linBuf[0] == 0x55) {
    uint8_t pid = linBuf[1] & 0x3F;
    if (LIN_ENABLE_PID != 0 && pid == LIN_ENABLE_PID) {
      bool en = linEnableBit(&linBuf[2], linLen - 2);
      if (haveLin && en != lastLinEn) sawLinToggle = true;
      lastLinEn = en;
      haveLin = true;
    }
    Serial.printf("LIN pid=0x%02X n=%u\n", pid, linLen);
  }
}

void applyMode(bool rail) {
  if (ovlatched) {
    arm = false;
    return;
  }
  if (mode == MODE_AUTO) {
    if (!rail) {
      arm = false;
      return;
    }
    if (sawVinDropOnToggle) mode = MODE_A;
    else if (sawLinToggle) mode = MODE_B;
  }
  if (mode == MODE_A) arm = rail;
  else if (mode == MODE_B) arm = rail && lastLinEn;
  else if (mode == MODE_C) arm = rail;
  else arm = rail && (haveLin ? lastLinEn : true);
}

void setup() {
  pinMode(PIN_FET, OUTPUT);
  digitalWrite(PIN_FET, LOW);
  pinMode(PIN_LED_RAIL, OUTPUT);
  pinMode(PIN_LED_ARM, OUTPUT);
  analogReadResolution(12);
  Serial.begin(115200);
  Serial1.begin(LIN_BAUD, SERIAL_8E1, PIN_LIN_RX, -1);
  delay(300);
  Serial.printf("PadTap boot  build=%s  mode=AUTO  LIN RX only  OVLO=%.0f V\n",
                PADTAP_DIRECT ? "DIRECT48" : "BUCK36", VIN_OVLO_V);
}

void loop() {
  while (Serial1.available()) parseLinByte((uint8_t)Serial1.read());

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toLowerCase();
    if (cmd == "mode a") mode = MODE_A;
    if (cmd == "mode b") mode = MODE_B;
    if (cmd == "mode c") mode = MODE_C;
    if (cmd == "mode auto") mode = MODE_AUTO;
    if (cmd == "ov reset") ovlatched = false;
    Serial.printf("mode=%d ov=%d\n", (int)mode, ovlatched);
  }

  static bool lastRail = true;
  float vin = readVin();
  bool rail = vin > VIN_RAIL_V;
  if (lastRail && !rail) sawVinDropOnToggle = true;
  lastRail = rail;

  if (vin >= VIN_OVLO_V) {
    if (!ovlatched) Serial.printf("OVLO trip vin=%.1f\n", vin);
    ovlatched = true;
  } else if (ovlatched && vin <= VIN_OVLO_CLEAR_V) {
    ovlatched = false;
    Serial.printf("OVLO clear vin=%.1f\n", vin);
  }

  applyMode(rail);
  if (ovlatched) arm = false;
  digitalWrite(PIN_FET, arm ? HIGH : LOW);
  digitalWrite(PIN_LED_RAIL, rail ? HIGH : LOW);
  digitalWrite(PIN_LED_ARM, arm ? HIGH : LOW);

  static uint32_t t = 0;
  if (millis() - t > 1000) {
    t = millis();
    Serial.printf("vin=%.1f rail=%d arm=%d mode=%d lin=%d drop=%d ov=%d\n",
                  vin, rail, arm, (int)mode, lastLinEn, sawVinDropOnToggle, ovlatched);
  }
}
