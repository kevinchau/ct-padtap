# PadTap

Cybertruck center-console **wireless-charger tap** → regulated **36 V** barrel for **Starlink Mini**.

The Y-harness sits between Tesla PN **1877045** and the vehicle plug so the pad and the **key-card NFC reader stay alive**. A small board listens to the on-screen pad enable (almost certainly LIN, not a 48 V cut), bucks Tesla’s 28–58 V rail down to 36 V, and switches a 5.5 mm barrel.

This is **not** a Tesla-approved accessory point. Tesla’s approved 48 V taps are the roof and frunk feeds (400 W). Read [SAFETY.md](SAFETY.md) before you open the console.

## Why this exists

You wanted 48 V out of the wireless-pad connector, switched from the screen (Controls → Outlets & Mods → Wireless Phone Charging Pads).

Three facts get in the way:

1. **Unplugging the pad kills NFC.** Same module. The tap must be a pass-through Y.
2. **The screen toggle is almost certainly LIN**, not a power cut. Tesla would not drop 48 V to this module just to disable Qi — that would kill the key card. Predecessor Model Y pads already talk LIN (NXP TJA1021). Firmware still auto-detects if Tesla *does* cut 48 V (Mode A).
3. **Raw Cybertruck 48 V can be 58 V.** Starlink Mini is rated 12–48 V, 60 W. Nominal 44–50 V has worked for people on the roof feed; 58 V is out of spec. PadTap bucks to **36 V**.

## What’s in this repo

| Path | |
| --- | --- |
| [docs/research.md](docs/research.md) | Sources: Tesla DIY 48 V, WPC R&R, owner manual, Starlink spec, CTOC |
| [hardware/harness.md](hardware/harness.md) | Y-harness, connector hunt, hypothesized 4-pin map |
| [hardware/schematic.md](hardware/schematic.md) | Board nets, protection, forbidden parts |
| [hardware/bom.csv](hardware/bom.csv) | Order list |
| [firmware/padtap](firmware/padtap) | ESP32-C3 PlatformIO, LIN listen-only, AUTO / A / B / C |

## Architecture

```
Cybertruck console harness
        │  48V+  GND  LIN  P4
        ▼
     Y-harness ── 1:1 ──► WPC 1877045 (Qi + NFC)
        │
        ├ 48V+ / GND / LIN (listen)
        ▼
     PadTap board
        │  fuse → Schottky → TVS
        ├ 5 V buck  → ESP32-C3 + TLIN2029 (RX only)
        ├ 36 V buck → FET → 3 A fuse → 5.5×2.1 barrel, center +
        ▼
     Starlink Mini   25–40 W avg, 60 W peak
```

### Modes

| Mode | When | Behavior |
| --- | --- | --- |
| **AUTO** | First boot | Latches A if 48 V drops on toggle; B if LIN bit flips |
| **A** Power-follow | 48 V is cut with the pads | MOSFET follows VIN |
| **B** LIN-follow | Expected | MOSFET follows the learned LIN enable bit |
| **C** Awake-follow | Manual | On whenever the rail is up |

## Probe first

Tesla’s connector pinout lives in **Service Mode Plus → Low Voltage → Wiring / Connector diagram** (the Cybertruck wiring guide). Search `wireless charger`, `WPC`, `1877045`, `NFC`. Screenshot ID, pins, colors, fuse.

Until that page is in-hand:

- Pin 1 ≈ 48 V+ (blue tape, blue housing)
- Pin 2 ≈ GND
- Pin 3 ≈ LIN (~12 V idle, 19.2 kbps)
- Pin 4 ≈ unknown — pass through

Owner reports say **four pins**. Do not crimp a GT150 (or anything else) until a photo of *your* plug matches.

Measure idle WPC current. If Tesla’s fuse cannot take pad + 60 W, **stop** and use the 400 W roof/frunk feed.

## Board (Rev A)

- ESP32-C3 SuperMini
- TLIN2029A-Q1 or equivalent, **TX disconnected**
- 8–60 V → 36 V 5 A buck (not LM2596, not MP1584)
- 7–60 V → 5 V 2 A buck
- FQP30N06L low-side on the Mini return
- ATC 3 A in and out, SMBJ58A / SMBJ40A

Flash:

```
cd firmware/padtap
pio run -t upload
pio device monitor -b 115200
```

Serial: `mode a` / `mode b` / `mode c` / `mode auto`. First capture fills `firmware/padtap/src/lin_map.h`.

## Install (short)

Tesla torque: T20, **5 N·m**. Official access: LH center floor rail → center-console front panel. Bench-test 36.00 V and barrel polarity on the official Starlink PSU **before** the Mini sees the truck. First wake without Starlink: confirm key card and Qi. Then plug the Mini.

## Starlink barrel

5.5 mm OD. Spec sheet draws **2.5 mm** center pin; 2.1 mm plugs are widely used. Center **positive** — meter the wall wart.

## License

MIT. You are modifying a 48 V vehicle. That is on you.
