# Y-harness

Sits between the Cybertruck center-console wireless charger (Tesla PN **1877045**, connector **C X0648**) and the vehicle plug.

Sources:
- [Electrical Reference sheet 46](https://service.tesla.com/docs/Cybertruck/ElectricalReference/prog-242/interactive/pdf/console_phone_and_usb_charging_print.pdf)
- [X0648 connector page](https://service.tesla.com/docs/Cybertruck/ElectricalReference/prog-242/connector/x0648/) — Tesla PN **1042593-03-A**

```
VEHICLE 5718 ──► [our 6210 male]─┬─ 1:1 ─► [our 5718 female] ──► CHARGER 6210
                                 │
                                 ├─ pin 1  RD/BU  18 AWG  ─► PadTap VIN  (3 A + NTC)
                                 ├─ pin 9  BN/BU  18 AWG  ─► PadTap GND
                                 └─ pin 4  GN     22 AWG  ─► TLIN2029 RX only
```

## Plastics

This is **wire-to-board**, not a sealed 4-pin GT150.

| Side | Sumitomo | Tesla | What it is |
| --- | --- | --- | --- |
| Vehicle harness (unplugs from the charger) | **6098-5718** grey 12-way **female** | 1042593-03-A / X0648 | TS/DL 1.5 mm (060), unsealed |
| Charger module | **6098-6210** 12-way **male** | on 1877045 | DL series PCB header, grey, TH, horizontal mate |

5718 plugs onto 6210. Confirmed: [Nexelec](https://nexelec.com/products/sumitomo-60985718) lists 6210 as the mate; Sumitomo’s PCB catalogue lists 6210 as a 12-way DL header.

**Y-harness buy list**

1. **6098-5718** female — plugs into the charger. Crimp terminals below.
2. **6098-6210** male PCB header — the vehicle 5718 plugs onto this. 6210 is a through-hole header, not a wire housing. Solder a pigtail to the pins (or a 25 mm breakout) and strain-relief / pot it. Do not expect a free-hanging male 6210.

Do not substitute 6098-5704 / 6098-5713 (TS natural pair). Different color/keying; Tesla’s plug is grey 5718 onto 6210.

## Terminals (into 5718 only)

Tesla cavity table, X0648:

| Cavity | Terminal | Size | Color | mm² | Dest | Tap? |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | 8240-0213 | 1.5×0.64 F | **RD/BU** | 1.00 | X0644-20 (Console VBATT) | **Yes** |
| 2 | unused | | | | | empty |
| **3** | 8240-0213 | 1.5×0.64 F | WH/BU | 1.00 | X0644-1 | Pass-through (USB GND) |
| **4** | 8240-0215 | 1.5×0.64 F | **GN** | 0.35 | X0944M-5 (LIN in) | **Listen only** |
| 5–8 | unused | | | | | empty |
| **9** | 8240-0213 | 1.5×0.64 F | BN/BU | 1.00 | X0944M-6 (WPC GND) | **Yes** |
| **10** | 8240-0215 | 1.5×0.64 F | GY | 0.35 | X0644-16 (LIN out / HVAC) | **Never break** |
| **11** | 8240-0215 | 1.5×0.64 F | PK/WH | 0.35 | X0944M-11 CANH | No tap |
| **12** | 8240-0215 | 1.5×0.64 F | BU/WH | 0.35 | X0944M-12 CANL | No tap |

**8240-0213** — female, tin, TS 1.5 mm, **0.75–1.25 mm²** (16–18 AWG), insulation 1.4–2.3 mm. Use on cavities 1, 3, 9. Tesla’s 1.00 mm² sits in the middle. **Do not crimp 16 AWG GXL** (1.31 mm², fat insulation) — it is out of spec. Tap pigtails: **18 AWG GXL** or 1.00 mm² FLRY.

**8240-0215** — female, tin, TS 1.5 mm, **0.3–0.5 mm²**, insulation 1.1–1.7 mm. Use on 4, 10, 11, 12. LIN tap: **22 AWG**.

Male tabs are part of the 6210 header. No crimp males unless you change architecture.

Crimp: open-barrel Sumitomo TS 1.5 mm die (Rennsteig lists 8240-0213). A random SN-28B will smash these.

## Why a Y, not an unplug

Unplugging X0648 kills NFC (CAN 11/12), HVAC switchpack LIN (pin 10), and USB pass-through (1/3).

Tesla R&R: disconnect, harness clip, T20 ×4 at **5 N·m**.

## Power

Pin 1 is Right Controller high-side **X0034-91** `WIRELESS_PHONE_CHARGER_AND_VCUSB`, shared with USB. Pad toggle is LIN (`LIN_INDUCTIVE_CHARGER` on pin 10). Mode B expected. NTC + 80 ms ramp on the tap.

## Rules

- 1:1 on cavities 1, 3, 4, 9, 10, 11, 12. Leave 2, 5–8 empty.
- Tap only **1, 9, 4**. Pin 4 parallel, no extra pull-up, no TX.
- Never open 10 or 11/12. Do not use pin 3 as PadTap ground.
- Adhesive shrink, cloth tape, strain-relief so seat travel cannot yank 5718 off 6210.
