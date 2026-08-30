# Under-panel sled

Two-piece PETG, **64 × 40 × 15 mm**, sized to the Rev A.1 board (58 × 34 mm). VHB the lid to the underside of a console panel.

Print `padtap_case.scad` if you have OpenSCAD. `generate_stl.py` emits compact ASCII STLs with the same openings.

| File | |
| --- | --- |
| `padtap_case.scad` | Source. `PART="base"` / `"lid"` / `"preview"` |
| `padtap_base.stl` | Body, openings, bosses |
| `padtap_lid.stl` | Mount face (print this side on the bed) |

## Openings

| Face | Feature | Size |
| --- | --- | --- |
| West | Cable comb, 3 U-slots | 4.0 mm, lines up with J1 VIN / GND / LIN |
| East | Barrel | Ø 8.2 mm at board y = 22.5, center 6 mm above floor |
| South | USB-C | 9.6 × 3.6 mm, centred on board x = 30 |
| Lid | LED membranes | 2× Ø 2.8 mm over the 0805s |
| Lid, bed face | VHB pockets | 4× 10 mm square |

Bosses match the PCB holes at (3, 3), (55, 3), (3, 31), (55, 31).

## Height

Assembled drop **15 mm**. Internal 12.1 mm — enough for the DPAK FET, ESP32-C3-MINI-1, and XL7015. Direct 48 V only.

Fuses and the 10 Ω NTC stay on the harness.

## Print

- PETG. Not PLA.
- 0.2 mm layers, 4 perimeters, 30 % gyroid, 250 / 80 °C.
- Base: floor down. No supports.
- Lid: **VHB face on the bed**, lip up.
- 4× M2.5 × 6 mm into heat-set inserts.

Confirm 15 mm of clearance under the panel before you glue.
