# PadTap controller

48 V in (Tesla 28–58 V) → fused → reverse Schottky → TVS → two bucks.

- **5 V buck** (7–60 V in): ESP32-C3 + TLIN2029A-Q1 VSUP
- **36 V buck** (8–60 V in, 5 A): Starlink Mini sweet spot
- **FQP30N06L** low-side switch on Starlink return
- **LIN RX only** — TX pin not wired

Do **not** feed Starlink Mini raw Cybertruck 48 V. Tesla max is **58 V**. Mini max is **48 V**.

## Nets

| Net | From | To |
| --- | --- | --- |
| VIN_48 | Y-harness 48 V+ via 3 A fuse | Schottky → SMBJ58A → both bucks |
| GND | Y-harness GND | Board GND, FET source, barrel sleeve |
| LIN_BUS | Y-harness LIN (parallel) | TLIN2029 LIN pin |
| LIN_RX | TLIN2029 RXD | ESP32 GPIO20 |
| V5 | 5 V buck | ESP32 5V, TLIN VSUP |
| V36 | 36 V buck | Barrel center via FET + 3 A fuse |
| VSENSE | 100 k / 10 k on VIN_48 | ESP32 ADC, 3.3 V zener clamp |
| nGATE | ESP32 GPIO5 + 100 Ω | FET gate, 10 k pulldown |

## GPIO

| Pin | Function |
| --- | --- |
| GPIO20 | UART RX (LIN) |
| GPIO5 | FET gate |
| GPIO4 | ADC VIN_48 |
| GPIO6 | Amber LED, rail present |
| GPIO7 | Green LED, output armed |

## Protection

- ATC 3 A on VIN_48
- ATC 3 A on V36
- SMBJ58A on VIN_48
- SMBJ40A on V36
- Series Schottky (100 V, 5 A) reverse protection
- 3.3 V zener on ADC node (divider would otherwise exceed 3.3 V at 58 V)

## Forbidden parts

| Don’t use | Why |
| --- | --- |
| LM2596 | 40 V max input |
| MP1584 | 28 V max input |
| 12 V car-USB adapters | Wrong rail, wrong range |
| Driving LIN TX | We are not a second commander |

## Rev B

`pcb/` is reserved for an LM76003-Q1 + TLIN2029A-Q1 + ESP32-C3 board after the probe log names the LIN PID and the Tesla housing.
