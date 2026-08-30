# PadTap Direct 48 V

Switched pass-through. No 36 V buck. Starlink Mini sees the Cybertruck rail (typically 44–50 V).

Tesla’s published accessory range is **28 V min / 44–50 V nominal / 58 V max**. Mini is printed **12–48 V**, but the input stage is a 48 V-class converter: Infineon **BSZ146N10LS5** 100 V FETs and a **60 V TVS** across the barrel (clamps ~66–73 V). That hardware will take **~56 V**. Tesla’s 58 V peak is the gap — we disconnect at **56.0 V** instead of converting.

Double-converting (our buck, then Mini’s buck) wastes 4–8 W at cruise. Direct FET loss at 40 W / 48 V is ~0.2 W.

```
VIN_48 ── ATC 3 A ── Schottky SS510 ──┬── SMBJ58A ── GND
                                      │
                                      ├── 5 V buck (7–60 V) ── ESP32-C3 + TLIN2029 VSUP
                                      │
                                      ├── 100 k / 10 k ── ADC GPIO4 + 3.3 V zener
                                      │         │
                                      │         └── 215 k / 10 k ── LM393 IN−
                                      │                              IN+ = 2.495 V (TL431)
                                      │                              OC output ── FET gate
                                      │
                                      └── FQP13N10L drain
                                              source ── ATC 3 A ── barrel center +
                                              gate ← ESP32 GPIO5 via 1 k, 10 k pulldown
```

Low-side switch on the Mini return, same as the 36 V build. Do **not** low-side the WPC ground.

## Why 56.0 V, not 58 V

| Limit | V | Source |
| --- | --- | --- |
| Mini printed max | 48 | Spec sheet next to the barrel |
| Mini hardware ceiling | ~56–60 | 100 V input FETs, 60 V TVS |
| Direct OVLO trip | **56.0** | LM393 + firmware latch |
| Direct OVLO clear | 54.0 | Hysteresis |
| Tesla accessory max | 58 | DIY 48 V power-feed document |

If the LV bus ever sits at 58 V, Direct turns Starlink off. That is rare (nominal 44–50 V). If you need the Mini up during a 58 V excursion, build [schematic.md](schematic.md) (buck 36 V) instead.

Do **not** put a 54 V TVS across the barrel. Tesla is allowed to run at 50 V; a 54 V clamp would dump the truck’s rail into the diode. Disconnect, don’t clamp.

## OVLO (hardware)

LM393, 5 V VCC, open-collector to the FET gate.

- IN+ = TL431 2.495 V
- IN− = VIN × 10 k / (215 k + 10 k)
- Trip: 2.495 × 225 / 10 = **56.14 V** (215 k 1 %)
- When VIN > 56 V, OC conducts, gate = 0, FET off — even if the ESP32 is wedged
- 1 k between GPIO5 and gate so a fight is 3.3 mA, not 33 mA

Firmware is the second gate: latches `ov` at 56.0 V, clears at 54.0 V, serial `ov reset` to force.

## Nets

| Net | From | To |
| --- | --- | --- |
| VIN_48 | Y-harness 48 V+ via 3 A fuse | Schottky → SMBJ58A → 5 V buck + FET drain |
| GND | Y-harness GND | Board GND, FET source via output fuse to barrel sleeve |
| LIN_BUS | Y-harness LIN (parallel) | TLIN2029 LIN pin |
| LIN_RX | TLIN2029 RXD | ESP32 GPIO20 |
| V5 | 5 V buck | ESP32 5V, TLIN VSUP, LM393 VCC, TL431 bias |
| VOUT | FET source via 3 A fuse | Barrel center + |
| VSENSE | 100 k / 10 k on VIN_48 | ESP32 ADC, 3.3 V zener |
| nGATE | ESP32 GPIO5 + 1 k, LM393 OC | FQP13N10L gate, 10 k pulldown |

## GPIO

Same map as the 36 V build.

| Pin | Function |
| --- | --- |
| GPIO20 | UART RX (LIN) |
| GPIO5 | FET gate (1 k) |
| GPIO4 | ADC VIN_48 |
| GPIO6 | Amber LED, rail present |
| GPIO7 | Green LED, output armed |

## Protection

- ATC 3 A on VIN_48
- ATC 3 A on barrel (Starlink 60 W / 48 V ≈ 1.25 A; 60 W / 28 V ≈ 2.1 A)
- SMBJ58A on VIN_48 only
- Series Schottky 100 V 5 A reverse protection
- 3.3 V zener on ADC node
- LM393 OVLO + firmware latch at 56.0 V
- 100 V logic-level FET (FQP13N10L) — 60 V FQP30N06L is too close to Tesla max

## Current

| Mini load | @ 36 V (buck) | @ 48 V (direct) |
| --- | --- | --- |
| 25 W cruise | 0.69 A | 0.52 A |
| 40 W typical | 1.11 A | 0.83 A |
| 60 W peak | 1.67 A | 1.25 A |

3 A fuse still the right ceiling. 16 AWG still conservative.

## Forbidden

| Don’t | Why |
| --- | --- |
| 36 V buck in this build | That’s the other schematic |
| FQP30N06L (60 V) | Tesla max 58 V + Mini input inductance |
| SMBJ40A / 54 V TVS on VOUT | Clamps a legal Tesla rail |
| LM2596 / MP1584 | 5 V buck must be 60 V-in |
| Driving LIN TX | Sniffer only |
| Feeding Mini above 56 V “because the TVS is 60 V” | TVS is a clamp, not an operating point |

Flash the `direct` PlatformIO env.
