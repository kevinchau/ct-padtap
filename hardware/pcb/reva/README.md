# PadTap Direct 48 V — Rev A PCB

2-layer, **104.8 × 52.8 mm**, 1.6 mm FR4. Drops into the PETG sled (inner cavity). Black mask, white silk, HASL, 1 oz.

![Top](pcb-top.svg)

## Edge map

| Edge | What |
| --- | --- |
| West | J1 VIN / GND / LIN — 18 AWG into Ø1.3 mm pads, lines up with the cable comb |
| East | J2 5.5 mm barrel, center + |
| South | J3 USB-C, lines up with the 9.6 × 3.8 mm window |
| Lid | Amber + green 0805 under the membranes |

Fuses (MINI 3 A **58 V**) and the **10 Ω NTC** stay on the harness. This board assumes VIN is already fused.

## Order (JLCPCB)

1. Upload [`PadTap-RevA-gerbers.zip`](PadTap-RevA-gerbers.zip)
2. 2-layer, 1.6 mm, 1 oz, black, HASL, 100 × 50 class (board is 104.8 × 52.8)
3. Optional SMT: [`bom-jlc.csv`](bom-jlc.csv) + [`cpl-jlc.csv`](cpl-jlc.csv). Confirm LCSC numbers before paying — they drift.
4. Q1 is **IRLR3110TRPBF DPAK** (100 V logic-level). IRL540N TO-220 will not assemble.

## Rules the layout keeps

- TLIN2029 **TXD pulled high**, no track to the ESP32
- Low-side FET on barrel **sleeve** only — WPC ground is not switched
- OVLO (LM393 + TL431) open-collector on the gate, wins over GPIO5
- USB-C native D+/D− on GPIO19/18; Serial is USB-CDC, LIN is Serial1 on GPIO20

`python3 generate.py` regenerates Gerbers and this drawing.
