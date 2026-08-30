#!/usr/bin/env python3
"""Axis-aligned STLs for the under-panel sled.

Print-quality source (fillets, round barrel, LED membranes) is padtap_case.scad.
This mesh is slicer-legal: comb, barrel, USB, vents, bosses, VHB, screw holes.
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parents[1] / "public" / "enclosure"

L, W = 64.0, 40.0
BASE_H, LID_T, LIP_H, WALL, FLOOR = 13.6, 1.6, 1.2, 1.5, 1.5
COMB_W, COMB_GAP, COMB_SADDLE, COMB_N, COMB_Y0 = 4.0, 6.0, 3.6, 3, 11.0
BARREL_D, BARREL_Z, BARREL_Y = 8.2, 6.0, 25.5
USB_W, USB_H, USB_X, USB_Z = 9.6, 3.6, 27.2, 2.2
VENT_W, VENT_H, VENT_Z, VENT_XS = 8.0, 2.0, 5.2, (14.0, 38.0)
BOSS_XY = ((5.0, 6.0), (57.0, 6.0), (5.0, 34.0), (57.0, 34.0))
BOSS, INSERT, INSERT_H = 5.5, 3.4, 3.8
LED_POS = ((53.4, 19.8), (53.4, 17.4))
LED_D, MEMBRANE = 2.8, 0.4
VHB, VHB_T = 10.0, 0.35
SCREW = 2.7


class Mesh:
    def __init__(self, name: str) -> None:
        self.name = name
        self.faces: list[tuple] = []

    def add(self, a, b, c) -> None:
        self.faces.append((a, b, c))

    def box(self, x, y, z, w, d, h) -> None:
        if w <= 1e-6 or d <= 1e-6 or h <= 1e-6:
            return
        x2, y2, z2 = x + w, y + d, z + h
        v = [
            (x, y, z),
            (x2, y, z),
            (x2, y2, z),
            (x, y2, z),
            (x, y, z2),
            (x2, y, z2),
            (x2, y2, z2),
            (x, y2, z2),
        ]
        for a, b, c, d_ in (
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ):
            self.add(v[a], v[b], v[c])
            self.add(v[a], v[c], v[d_])

    def plate(self, x, y, z, w, d, h, holes: list[tuple[float, float, float, float]] | None = None) -> None:
        """Solid plate minus axis-aligned rectangular through-holes in XY."""
        if not holes:
            self.box(x, y, z, w, d, h)
            return
        xs = {x, x + w}
        for hx, _hy, hw, _hd in holes:
            xs.add(max(x, min(x + w, hx)))
            xs.add(max(x, min(x + w, hx + hw)))
        xs_sorted = sorted(xs)
        for i in range(len(xs_sorted) - 1):
            x0, x1 = xs_sorted[i], xs_sorted[i + 1]
            if x1 - x0 < 1e-6:
                continue
            xm = (x0 + x1) / 2
            blocked: list[tuple[float, float]] = []
            for hx, hy, hw, hd in holes:
                if hx < xm < hx + hw:
                    blocked.append((max(y, hy), min(y + d, hy + hd)))
            blocked.sort()
            merged: list[tuple[float, float]] = []
            for b0, b1 in blocked:
                if b1 <= b0:
                    continue
                if merged and b0 <= merged[-1][1] + 1e-9:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], b1))
                else:
                    merged.append((b0, b1))
            cursor = y
            for b0, b1 in merged:
                if b0 > cursor:
                    self.box(x0, cursor, z, x1 - x0, b0 - cursor, h)
                cursor = max(cursor, b1)
            if cursor < y + d:
                self.box(x0, cursor, z, x1 - x0, y + d - cursor, h)

    def write(self, path: Path) -> None:
        lines = [f"solid {self.name}"]
        for a, b, c in self.faces:
            ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
            vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
            nx = uy * vz - uz * vy
            ny = uz * vx - ux * vz
            nz = ux * vy - uy * vx
            lines.append(f"  facet normal {nx:.4e} {ny:.4e} {nz:.4e}")
            lines.append("    outer loop")
            for p in (a, b, c):
                lines.append(f"      vertex {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}")
            lines.append("    endloop")
            lines.append("  endfacet")
        lines.append(f"endsolid {self.name}")
        path.write_text("\n".join(lines) + "\n")


def comb_slots() -> list[tuple[float, float]]:
    return [(COMB_Y0 + i * COMB_GAP, COMB_W) for i in range(COMB_N)]


def base() -> Mesh:
    m = Mesh("padtap_base")
    m.box(0, 0, 0, L, W, FLOOR)
    wall_h = BASE_H - FLOOR

    # West wall + U-comb. Saddle is solid; slots open above it.
    slots = comb_slots()
    m.box(0, 0, FLOOR, WALL, W, COMB_SADDLE)
    cursor = 0.0
    for sy, sw in slots:
        m.box(0, cursor, FLOOR + COMB_SADDLE, WALL, max(sy - cursor, 0), wall_h - COMB_SADDLE)
        cursor = sy + sw
    m.box(0, cursor, FLOOR + COMB_SADDLE, WALL, W - cursor, wall_h - COMB_SADDLE)

    # East wall + barrel (square of the circle diameter — jack still fits).
    br = BARREL_D
    by = BARREL_Y - br / 2
    bz = FLOOR + BARREL_Z - br / 2
    m.box(L - WALL, 0, FLOOR, WALL, by, wall_h)
    m.box(L - WALL, by + br, FLOOR, WALL, W - (by + br), wall_h)
    m.box(L - WALL, by, FLOOR, WALL, br, bz - FLOOR)
    m.box(L - WALL, by, bz + br, WALL, br, BASE_H - (bz + br))

    # South wall: USB window + vents.
    cuts = [(USB_X, USB_W, FLOOR + USB_Z, USB_H)] + [(vx, VENT_W, FLOOR + VENT_Z, VENT_H) for vx in VENT_XS]
    cuts.sort()
    cursor = 0.0
    for cx, cw, cz, ch in cuts:
        m.box(cursor, 0, FLOOR, max(cx - cursor, 0), WALL, wall_h)
        m.box(cx, 0, FLOOR, cw, WALL, cz - FLOOR)
        m.box(cx, 0, cz + ch, cw, WALL, BASE_H - (cz + ch))
        cursor = cx + cw
    m.box(cursor, 0, FLOOR, L - cursor, WALL, wall_h)

    # North wall + vents.
    cursor = 0.0
    for vx in VENT_XS:
        m.box(cursor, W - WALL, FLOOR, max(vx - cursor, 0), WALL, wall_h)
        m.box(vx, W - WALL, FLOOR, VENT_W, WALL, VENT_Z)
        m.box(vx, W - WALL, FLOOR + VENT_Z + VENT_H, VENT_W, WALL, wall_h - (VENT_Z + VENT_H))
        cursor = vx + VENT_W
    m.box(cursor, W - WALL, FLOOR, L - cursor, WALL, wall_h)

    # Corner bosses with square insert wells (heat-set from inside). SCAD uses round.
    for x, y in BOSS_XY:
            bx, by_ = x - BOSS / 2, y - BOSS / 2
            bh = wall_h - 0.6
            well = bh - INSERT_H
            m.box(bx, by_, FLOOR, BOSS, BOSS, well)
            m.plate(
                bx,
                by_,
                FLOOR + well,
                BOSS,
                BOSS,
                INSERT_H,
                [(x - INSERT / 2, y - INSERT / 2, INSERT, INSERT)],
            )

    return m


def lid() -> Mesh:
    m = Mesh("padtap_lid")
    vhb_holes = []
    for x in (8.0, L - 8.0 - VHB):
        for y in (6.0, W - 6.0 - VHB):
            vhb_holes.append((x, y, VHB, VHB))
    m.plate(0, 0, 0, L, W, MEMBRANE, vhb_holes)

    screw_holes = []
    for x, y in BOSS_XY:
        screw_holes.append((x - SCREW / 2, y - SCREW / 2, SCREW, SCREW))
    led_holes = [(x - LED_D / 2, y - LED_D / 2, LED_D, LED_D) for x, y in LED_POS]
    m.plate(0, 0, MEMBRANE, L, W, LID_T - MEMBRANE, screw_holes + led_holes)

    lip_x = WALL / 2 + 0.2
    lip_y = WALL / 2 + 0.2
    lip_w = L - WALL - 0.4
    lip_d = W - WALL - 0.4
    comb_relief = [(0.0, sy + 0.3, WALL + 2, COMB_W - 0.6) for sy, _sw in comb_slots()]
    m.plate(lip_x, lip_y, LID_T, lip_w, lip_d, LIP_H - 0.15, screw_holes + comb_relief)
    return m


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    b = base()
    l = lid()
    b.write(HERE / "padtap_base.stl")
    l.write(HERE / "padtap_lid.stl")
    (PUBLIC / "padtap_base.stl").write_text((HERE / "padtap_base.stl").read_text())
    (PUBLIC / "padtap_lid.stl").write_text((HERE / "padtap_lid.stl").read_text())
    print(f"base {len(b.faces)} tris {(HERE / 'padtap_base.stl').stat().st_size}B")
    print(f"lid  {len(l.faces)} tris {(HERE / 'padtap_lid.stl').stat().st_size}B")


if __name__ == "__main__":
    main()
