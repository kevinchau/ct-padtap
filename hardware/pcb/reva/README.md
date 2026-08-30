# PadTap Direct 48 V — Rev A.1

**58 × 34 mm**, 2-layer, 1.6 mm FR4. ~45 % of the sled cavity. Sits on the floor against the south wall.

![Top](pcb-top.svg)

| | |
| --- | --- |
| West | J1 VIN / GND / LIN — 18 AWG, ~40 mm pigtail to the comb |
| East | J2 barrel through the sled hole, center + |
| South | USB-C through the window |
| 48 V | West island: TVS + Schottky + 10 µF/100 V. 1.6 mm rail to the barrel along the **south**, not under the MCU |
| SW | XL7015 pin 2 to L1, catch diode on that node only |
| OVLO | North, away from SW. LM393 OC on nGATE |
| Q1 | IRLR3110 DPAK, 9 thermal vias on the tab, source to GND pour |
| LIN | 1 k series + 220 pF + PESD. TXD **10 k to 5 V** (internal pulldown would dominate the bus). RXD 4.7 k to 3V3 |

Fuses and the NTC stay on the harness.

## Order

[`PadTap-RevA-gerbers.zip`](PadTap-RevA-gerbers.zip) → JLCPCB, 2-layer, 1.6 mm, black, HASL. SMT optional: `bom-jlc.csv` + `cpl-jlc.csv`. Confirm LCSC C-numbers.

Place the board so USB-C (30 mm from the west edge) lines up with the 9.6 mm window (outer x = 72).
