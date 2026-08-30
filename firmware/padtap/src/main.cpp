#include <Arduino.h>
#include "lin_map.h"

// PadTap — Cybertruck WPC tap → Starlink Mini
// LIN is listen-only. Do not wire TLIN2029 TXD.
//
// Direct 48 V (default, -DPADTAP_DIRECT=1): switched raw Tesla rail.
//   Hardware LM393 + firmware latch kill the FET at 56.0 V.
// Buck 36 V (-DPADTAP_DIRECT=0): 36 V module is the Mini's supply;
//   OVLO still trips so a mis-set pot cannot pass 58 V.
//
// Tesla 48 V uses digital / solid-state fuses. They trip on capacitor
// inrush, not RMS. Do not slam a buck or the Mini's input caps onto
// the rail. VIN NTC (harness) + 80 ms FET ramp.

#ifndef PADTAP_DIRECT
#define PADTAP_DIRECT 1
#endif

static const int PIN_LIN_RX = 20;
static const int PIN_FET = 5;
static const int PIN_VIN_ADC = 4;
static const int PIN_LED_RAIL = 6;
static const int PIN_LED_ARM = 7;
static const int FET_PWM_CH = 1;

static const float VIN_DIV_TOP = 100000.0f;
static const float VIN_DIV_BOT = 10000.0f;
static const float VIN_RAIL_V = 30.0f;
static const float VIN_OVLO_V = 56.0f;
static const float VIN_OVLO_CLEAR_V = 54.0f;
static const uint32_t LIN_BAUD = 19200;
static const uint32_t RAMP_MS = 80;  // Mini Cin · dV/dt stays well under an e-fuse

enum Mode { MODE_AUTO, MODE_A, MODE_B, MODE_C };
static Mode mode = MODE_AUTO;

static bool sawVinDropOnToggle = false;
static bool sawLinToggle = false;
static bool lastLinEn = false;
static bool haveLin = false;
static bool arm = false;
static bool ovlatched = false;
static bool rampOn = false;
static uint32_t rampStartMs = 0;

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

void driveFet(bool want) {
  static bool lastWant = false;
  if (!want) {
    ledcWrite(FET_PWM_CH, 0);
    rampOn = false;
    lastWant = false;
    return;
  }
  if (!lastWant) {
    rampOn = true;
    rampStartMs = millis();
    Serial.println("FET ramp");
  }
  lastWant = true;
  if (rampOn) {
    uint32_t dt = millis() - rampStartMs;
    uint32_t duty = dt >= RAMP_MS ? 255 : (dt * 255UL) / RAMP_MS;
    ledcWrite(FET_PWM_CH, duty);
    if (duty >= 255) rampOn = false;
  } else {
    ledcWrite(FET_PWM_CH, 255);
  }
}

void setup() {
  ledcSetup(FET_PWM_CH, 20000, 8);
  ledcAttachPin(PIN_FET, FET_PWM_CH);
  ledcWrite(FET_PWM_CH, 0);
  pinMode(PIN_LED_RAIL, OUTPUT);
  pinMode(PIN_LED_ARM, OUTPUT);
  analogReadResolution(12);
  Serial.begin(115200);
  Serial1.begin(LIN_BAUD, SERIAL_8E1, PIN_LIN_RX, -1);
  delay(300);
  Serial.printf("PadTap boot  build=%s  mode=AUTO  LIN RX only  OVLO=%.0f V  ramp=%u ms\n",
                PADTAP_DIRECT ? "DIRECT48" : "BUCK36", VIN_OVLO_V, (unsigned)RAMP_MS);
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
  driveFet(arm);
  digitalWrite(PIN_LED_RAIL, rail ? HIGH : LOW);
  digitalWrite(PIN_LED_ARM, arm ? HIGH : LOW);

  static uint32_t t = 0;
  if (millis() - t > 1000) {
    t = millis();
    Serial.printf("vin=%.1f rail=%d arm=%d ramp=%d mode=%d lin=%d drop=%d ov=%d\n",
                  vin, rail, arm, rampOn, (int)mode, lastLinEn, sawVinDropOnToggle, ovlatched);
  }
}
