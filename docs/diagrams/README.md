# Drawings

Dark-sheet SVGs for the GitHub README, plus concept renders.

```
python3 generate.py
```

| File | |
| --- | --- |
| `system-direct.svg` / `system-buck.svg` | Block architecture — 5718 / 6210 Y |
| `schematic-direct.svg` / `schematic-buck.svg` | Controller (NTC, 58 V MINI, IRL540N, 80 ms ramp) |
| `ovlo.svg` | LM393 56.14 V trip |
| `harness.svg` | Vehicle 5718 → our 6210 → our 5718 → charger 6210 |
| `mating.svg` | 6098-5718 female onto 6098-6210 DL header |
| `pin-map.svg` | X0648 cavity map, latch up, 1–6 over 7–12 |
| `connector-face.jpg` | Concept 5718 mating face |
| `mating-render.jpg` | Concept 5718 onto 6210 header |
| `harness-render.jpg` | Concept Y-harness |
| `enclosure-iso.svg` | Exploded 108 × 56 × 18 mm sled |
| `enclosure-pack-direct.svg` / `enclosure-pack-buck.svg` | Interior packing |
| `enclosure-section.svg` | Under-panel cutaway |
| `enclosure-hero.jpg` | Concept product shot |
| `enclosure-exploded.jpg` | Concept exploded render |
| `enclosure-installed.jpg` | Concept install under a console panel |
| `voltage.svg` / `modes.svg` / `gpio.svg` | Voltage overlap, firmware modes, GPIO |

Renders are visualization, not photos of a built unit. Tesla’s cavity drawing is not republished — `pin-map.svg` is a redraw. Print the STLs in `hardware/enclosure/`.
