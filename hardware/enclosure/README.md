# Under-panel sled

A two-piece PETG box, **108 × 56 × 18 mm**, meant to VHB to the underside of a Cybertruck center-console panel. Cables enter one short end and the Starlink barrel leaves the other, so the slab slides in parallel to the panel.

Print `padtap_case.scad` if you have OpenSCAD (fillets, round barrel, LED membranes). `generate_stl.py` emits compact ASCII STLs with the same openings — slicer-legal if you just need to print tonight.

| File | |
| --- | --- |
| `padtap_case.scad` | Source. `PART="base"` / `"lid"` / `"preview"` |
| `padtap_base.stl` | Body, openings, bosses |
| `padtap_lid.stl` | Mount face (print this side on the bed) |

## Openings

| Face | Feature | Size |
| --- | --- | --- |
| West | Cable comb, 3 U-slots | 4.4 mm wide, saddle 4.2 mm — 48 V+, GND, LIN. Drop in from above; lid clamps. |
| East | Barrel jack | Ø 8.2 mm, center 6.5 mm above floor. 5.5 mm panel jack. |
| South | USB-C window | 9.6 × 3.8 mm for ESP32-C3 SuperMini. Tape after flash. |
| North + south | Vents | 10 × 2.2 mm × 3 per long side (buck heat). |
| Lid | LED membranes | Ø 3.2 mm, 0.4 mm floor — amber + green show through. |
| Lid, bed face | VHB pockets | 12 × 12 × 0.35 mm, four corners. |

## Why this height

Internal 14.6 mm. That fits a **low-profile 60 V 3 A buck ≤ 12 mm tall** (Starlink peaks at 1.7 A — you do not need a 5 A tower heatsink). ESP32 SuperMini, 5 V buck, LIN module, and FET sit beside it.

If your 36 V module is taller than 12 mm, raise `base_h` in the SCAD.

## Print

- PETG (console can see 50–60 °C in sun). Not PLA.
- 0.2 mm layers, 4 perimeters, 30 % gyroid, 250 / 80 °C.
- Base: floor down. No supports — U-slots open from the top.
- Lid: **VHB face on the bed** (glossy stick surface), lip up.
- 4× M2.5 × 8 mm into heat-set inserts (base bosses).

## Mount

1. Flash firmware, confirm LEDs.
2. Stick 3M VHB 5952 squares in the four lid pockets.
3. Offer the sled under the console panel with the comb facing the WPC connector and the barrel facing the rear of the console (or wherever the Mini cable wants to go).
4. Press 10 seconds. Route 16 AWG so seat travel cannot snag it.
5. Keep the box off HVAC condensate and carpet.

Assembled height below the panel is **18 mm**. Confirm clearance on your truck before you glue.
