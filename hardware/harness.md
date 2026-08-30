# Y-harness

Sits between the Cybertruck center-console wireless charger (Tesla PN **1877045-00-C**, connector **C X0648**) and the vehicle plug.

Source: [Electrical Reference — Console Phone and USB Charging](https://service.tesla.com/docs/Cybertruck/ElectricalReference/prog-242/interactive/pdf/console_phone_and_usb_charging_print.pdf), sheet 46, prog-242 rev 1.11.

```
VEHICLE ──► [Y female]─┬─ all X0648 pins 1:1 ─► [Y male] ──► WPC 1877045
                       │
                       ├─ pin 1  YE/BU  16 AWG  ─► PadTap VIN  (3 A + NTC)
                       ├─ pin 9  BN/BU  16 AWG  ─► PadTap GND
                       └─ pin 4  GY     22 AWG  ─► TLIN2029 RX only
```

## Why a Y, not an unplug

Unplugging X0648 kills **NFC / key card** (CAN auth to Left Controller X0010-84/85), throws a Service Mode error, and **breaks LIN to the HVAC switchpack / touchpad** (pin 10 daisy-chain). USB pass-through on pins 1 and 3 also rides through this connector.

Tesla R&R: [Wireless Charger - Center Console](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8B81665F-D4DC-4DED-B787-45A957056FF9.html) — disconnect the electrical connector, release the harness clip, T20 ×4 at **5 N·m**.

## C X0648 pinout

12-way. Seven pins used. Owner 4-pin reports were wrong.

| Pin | Net | Color / gauge | From / to | Tap? |
| --- | --- | --- | --- | --- |
| **1** | 48 V+ HSD `WIRELESS_PHONE_CHARGER_AND_VCUSB` | YE/BU 1.00 mm² · 446(C) / 1924(V) | Right Controller **X0034-91** high-side drive. Internally pass-through to Console VBATT (USB03-A RD/BU 401) / rear USB | **Yes** (pass-through + tap) |
| **3** | USB GND pass-through | WH/BU 1.00 mm² · 401(C) | Rear USB ground | Pass-through only |
| **4** | LIN in `LIN_1_WIRELESS_PHONE_CHARGER_AND_VCUSB` | GY 0.35 mm² · 649(C) / 1924(V) | Right Controller **X0034-75** | **Listen only**, parallel. Do not break |
| **9** | WPC GND return `WIRELESS_PHONE_CHARGER_AND_VCUSB_GND_RETURN` | BN/BU 1.00 mm² · 649(C) / 1924(V) | Right Controller **X0034-17** | **Yes** |
| **10** | LIN out `LIN_INDUCTIVE_CHARGER` | GY 0.35 mm² · 401(C) | Console Controller **X0644-16** → HVAC switchpack / touchpad | Pass-through. **Never break** |
| **11** | CANH `CAN_AUTHENTICATION_CONSOLE_P` | PK/WH 0.35 mm² · 682(C) / 2543(V) | Left Controller **X0010-84** | Pass-through. No tap |
| **12** | CANL `CAN_AUTHENTICATION_CONSOLE_N` | BU/WH 0.35 mm² · 682(C) / 2543(V) | Left Controller **X0010-85** | Pass-through. No tap |

1.00 mm² ≈ 17 AWG. Tap with 16 AWG. LIN/CAN stay 22 AWG.

## Power: switched, but shared with USB

Pin 1 is a **high-side drive** from the Right Controller, not an unfused always-hot. The net name includes **VCUSB**. Tesla is not going to drop that rail to turn Qi off — the USB hub would die. The pad toggle is the LIN net `LIN_INDUCTIVE_CHARGER`. Firmware still watches for a power cut (Mode A).

This HSD already feeds WPC + USB. Console USB-C is 65 W per port. Measure idle current on pin 1 before you add 60 W of Starlink. Digital fuse: NTC on VIN + 80 ms FET ramp.

## Connector plastic

Highest pin number is 12 — this is a **12-way**, not GT150 4-way. Harvest pigtails from a donor **1877045-00-C**. Photograph the latch and cavity map on *your* truck before ordering terminals.

X0944 (in-line, between Right Controller and X0648) carries the same 48 V / GND / LIN / CAN trio (pins 1, 6, 5, 11, 12 on that connector). Do not tap there unless you like working behind the Right Controller.

## Rules

- 1:1 pass-through on **every** pin, including unused cavities.
- Tap only **1, 9, 4**. Pin 4 is high-Z listen. No extra pull-up. No TX.
- Never open pin 10 (HVAC LIN) or 11/12 (key-card CAN).
- Do not use pin 3 as PadTap ground.
- Adhesive-lined heat-shrink, then cloth tape.
- Strain-relief so seat travel cannot yank X0648.
