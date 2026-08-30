# Y-harness

Sits between the Cybertruck center-console wireless charger (Tesla PN **1877045-00-C**) and the vehicle plug.

```
VEHICLE HARNESS ──► [Y female]─┬─ all 4 pins ─► [Y male] ──► WPC 1877045
                               │
                               ├─ 48V+  16 AWG  ─► PadTap VIN  (3 A fuse)
                               ├─ GND   16 AWG  ─► PadTap GND
                               └─ LIN   22 AWG  ─► TLIN2029 RX only
```

## Why a Y, not an unplug

Unplugging the module kills **NFC / key card**, throws a Service Mode error, and can kill the forward ambient light. The pad and the key-card reader are the same part.

Tesla R&R: [Wireless Charger - Center Console](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8B81665F-D4DC-4DED-B787-45A957056FF9.html) — disconnect the electrical connector, release the harness clip, T20 ×4 at **5 N·m**.

## Connector

Tesla Electrical Reference (connector ID, pinout, colors, fuse) is in **Service Mode Plus → Low Voltage → Wiring / Connector diagram**. Search `wireless charger`, `WPC`, `1877045`, `NFC`.

Until that screenshot exists, treat this as a **hypothesis**:

| Pin | Function | How to prove | Tap? |
| --- | --- | --- | --- |
| 1 | 48 V+ | Highest DC vs chassis, blue tape, blue housing | Yes |
| 2 | GND | Continuity to chassis | Yes |
| 3 | LIN | ~12 V idle, 19.2 kbps awake | Listen only |
| 4 | Wake / NFC / NC | Log during pad toggle and key-card tap | Pass-through |

Owner reports: **4 pins**. Tesla 48 V accessory convention (roof/frunk feeds): red/blue = 48 V+, green = LIN, black or brown/blue = GND. 48 V connectors are **blue**.

### How to get the plastic

1. **Preferred:** harvest pigtails from a donor **1877045-00-C**.
2. Match the photo to Aptiv GT150 4-way (`15326820` / `15326821`), TE NanoMQS, or Molex Mini50. Do not crimp until the latch and seal match.
3. Prototype only: backprobe a mated OEM plug (Mode C, no LIN).

## Rules

- 1:1 pass-through on every pin.
- LIN is high-Z listen. No extra pull-up. No TX until the PID map is known.
- Adhesive-lined heat-shrink, then cloth tape (Tesla DIY accessory spec).
- Strain-relief so seat travel cannot yank the header.
