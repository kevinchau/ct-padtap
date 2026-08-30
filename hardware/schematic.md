# PadTap controller

Two builds, one Y-harness, one sled.

| | **Direct 48 V** (default) | **Buck 36 V** (conservative) |
| --- | --- | --- |
| Doc | [schematic-direct.md](schematic-direct.md) | this page |
| Mini sees | Raw Tesla rail, typically 44–50 V | Regulated 36.00 V |
| Extra conversion | None | 60 V → 36 V buck ≤ 12 mm |
| Overvoltage | LM393 + firmware kill FET at **56.0 V** | Buck absorbs Tesla’s 58 V peak |
| Use when | You want the efficiency; Mini hardware takes ~56 V | You want to stay inside the printed 12–48 V rating |

Shared front end: 48 V in (Tesla 28–58 V) → fused → **NTC 10 Ω ICL** → reverse Schottky → TVS.

Tesla 48 V digital fuses trip on buck input-cap inrush. The NTC is not optional on the 36 V build — that is the exact failure of a raw converter on the frunk tap. Direct still needs it for the 5 V MCU buck, plus an 80 ms FET ramp for Mini’s own caps.

- **5 V buck** (7–60 V in): ESP32-C3 + TLIN2029A-Q1 VSUP
- **LIN RX only** — TX pin not wired

## Buck 36 V

48 V in → fused → reverse Schottky → TVS → two bucks.

- **36 V buck** (8–60 V in, 3 A, ≤12 mm tall): Starlink Mini sweet spot. Must fit the 14.6 mm sled cavity.
- **FQP30N06L** low-side switch on Starlink return (36 V, 60 V FET is enough here)

## Nets (buck)

| Net | From | To |
| --- | --- | --- |
| VIN_48 | Y-harness 48 V+ via 3 A fuse | NTC 10 Ω → Schottky → SMBJ58A → both bucks |
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

## Protection (buck)

- ATC 3 A on VIN_48
- ATC 3 A on V36
- SMBJ58A on VIN_48
- SMBJ40A on V36
- Series Schottky (100 V, 5 A) reverse protection
- 3.3 V zener on ADC node (divider would otherwise exceed 3.3 V at 58 V)

Firmware still runs the 56 V OVLO so a mis-set 36 V pot cannot pass Tesla’s peak.

## Forbidden parts

| Don’t use | Why |
| --- | --- |
| LM2596 | 40 V max input |
| MP1584 | 28 V max input |
| 12 V car-USB adapters | Wrong rail, wrong range |
| Driving LIN TX | We are not a second commander |

## Rev B

`pcb/` is reserved for an LM76003-Q1 + TLIN2029A-Q1 + ESP32-C3 board after the probe log names the LIN PID and the Tesla housing. Direct 48 V Rev B would drop the 36 V buck and keep the OVLO comparator.
