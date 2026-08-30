#pragma once
#include <stdint.h>

// Fill these from the first probe capture (toggle Wireless Phone Charging Pads
// while the serial log is running). Until then, AUTO can still latch Mode A
// (48 V drops) or you can force Mode C from the serial console.

static const uint8_t LIN_ENABLE_PID = 0x00;   // 0 = unknown
static const uint8_t LIN_ENABLE_BYTE = 0;
static const uint8_t LIN_ENABLE_MASK = 0x01;
static const bool LIN_ENABLE_INVERT = false;  // true if bit is 1 when pads are OFF
