#!/usr/bin/env python3
"""Generate PadTap README diagrams (dark Cybertruck sheet)."""
from pathlib import Path
import html

OUT = Path(__file__).parent
BG, PANEL, PANEL2 = "#0B0C0E", "#141518", "#1C1E22"
LINE, AMBER, TEXT = "#2A2D32", "#E8A317", "#E8EAED"
MUTED, STEEL, OK = "#8B9098", "#C5C8CE", "#7DAE74"
DANGER, BLUE = "#C45C4A", "#6AA6C9"
FONT = "ui-sans-serif, system-ui, -apple-system, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


def svg(w, h, body, title=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<rect width="{w}" height="{h}" fill="{BG}"/>
{body}
</svg>
'''


def t(x, y, s, *, fill=TEXT, size=13, anchor="start", family=FONT, weight="500"):
    s = html.escape(s)
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-family="{family}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def r(x, y, w, h, *, fill=PANEL, stroke=LINE, rx=8, sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, *, stroke=AMBER, sw=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, *, stroke=AMBER, fill="none", sw=2):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def circ(x, y, rad, *, fill=PANEL, stroke=AMBER, sw=1.5):
    return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def cap(x, y, s, fill=MUTED):
    return t(x, y, s, fill=fill, size=11, family=MONO)


# ---------------------------------------------------------------------------
def system(direct=True):
    w, h = 920, 430
    board = "DIRECT 48 V" if direct else "BUCK 36 V"
    mid = "OVLO kills FET at 56 V" if direct else "58 V → 36 V buck"
    fet = "100 V FET + 3 A fuse" if direct else "MOSFET + 3 A fuse"
    mini = "44–50 V  ·  5.5 mm" if direct else "36 V  ·  5.5 mm"
    parts = [
        r(8, 70, 170, 220),
        t(93, 108, "Cybertruck", anchor="middle", fill=STEEL),
        t(93, 128, "console harness", anchor="middle", fill=MUTED, size=12),
        t(93, 168, "48V+  GND", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(93, 188, "LIN   P4", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(93, 240, "28–58 V", anchor="middle", fill=MUTED, size=11),
        t(93, 258, "NFC + Qi module", anchor="middle", fill=MUTED, size=11),
        line(178, 180, 250, 180),
        r(250, 90, 150, 180, fill=PANEL2, stroke=AMBER),
        t(325, 128, "Y-HARNESS", anchor="middle", fill=AMBER, size=14, family=MONO),
        t(325, 152, "all 4 pins", anchor="middle", size=12),
        t(325, 170, "1:1 pass-through", anchor="middle", size=12),
        t(325, 210, "tap 48V / GND / LIN", anchor="middle", fill=MUTED, size=11),
        line(400, 150, 470, 150, stroke=STEEL),
        path("M325 270 V320 H470"),
        r(470, 70, 170, 140),
        t(555, 112, "WPC 1877045", anchor="middle", fill=STEEL),
        t(555, 136, "dual 15 W Qi", anchor="middle", fill=MUTED, size=12),
        t(555, 156, "key-card NFC", anchor="middle", fill=MUTED, size=12),
        r(470, 250, 170, 140, stroke=AMBER),
        t(555, 292, board, anchor="middle", fill=AMBER, size=14, family=MONO),
        t(555, 316, "LIN sniffer", anchor="middle", size=12),
        t(555, 334, mid, anchor="middle", size=12),
        t(555, 352, fet, anchor="middle", size=12),
        line(640, 320, 710, 320),
        r(710, 250, 190, 140),
        t(805, 300, "Starlink Mini", anchor="middle", fill=STEEL),
        t(805, 324, mini, anchor="middle", fill=AMBER, size=12, family=MONO),
        t(805, 344, "25–40 W avg · 60 W pk", anchor="middle", fill=MUTED, size=12),
        t(20, 28, "PADTAP  ·  SYSTEM" + ("  ·  DIRECT 48 V" if direct else "  ·  BUCK 36 V"),
          fill=AMBER, size=12, family=MONO),
    ]
    name = "system-direct.svg" if direct else "system-buck.svg"
    (OUT / name).write_text(svg(w, h, "\n".join(parts), f"PadTap system {board}"), encoding="utf-8")


def pin_map():
    rows = [
        ("1", "48 V+ HSD", "YE/BU 1.00  ·  X0034-91  ·  TAP + pass-through"),
        ("3", "USB GND thru", "WH/BU 1.00  ·  rear USB  ·  pass-through only"),
        ("4", "LIN in", "GY 0.35  ·  X0034-75  ·  listen, do not break"),
        ("9", "WPC GND", "BN/BU 1.00  ·  X0034-17  ·  TAP"),
        ("10", "LIN out", "GY 0.35  ·  X0644-16 HVAC  ·  never break"),
        ("11", "CANH", "PK/WH 0.35  ·  X0010-84 auth  ·  no tap"),
        ("12", "CANL", "BU/WH 0.35  ·  X0010-85 auth  ·  no tap"),
    ]
    parts = [
        t(360, 28, "C X0648  ·  WIRELESS PHONE CHARGER + NFC READER  ·  12-WAY", fill=AMBER, size=12, family=MONO, anchor="middle"),
        r(20, 48, 680, 330, fill=PANEL),
    ]
    y = 78
    parts += [
        t(40, y, "PIN", fill=MUTED, size=11, family=MONO),
        t(90, y, "NET", fill=MUTED, size=11, family=MONO),
        t(250, y, "COLOR / SOURCE", fill=MUTED, size=11, family=MONO),
    ]
    y = 100
    for n, name, how in rows:
        parts += [
            t(40, y, n, fill=AMBER, size=14, family=MONO),
            t(90, y, name, fill=TEXT, size=13),
            t(250, y, how, fill=MUTED, size=12, family=MONO),
        ]
        y += 38
    parts.append(t(40, 360, "Sheet 46, prog-242 rev 1.11. Harvest the 12-way from a donor 1877045. Do not buy GT150 4-way.", fill=MUTED, size=12))
    (OUT / "pin-map.svg").write_text(svg(720, 390, "\n".join(parts), "X0648 pin map"), encoding="utf-8")


def harness():
    parts = [
        t(20, 28, "Y-HARNESS  ·  C X0648 12-WAY  ·  TAP PINS 1 / 9 / 4", fill=AMBER, size=12, family=MONO),
        r(20, 60, 200, 160),
        t(120, 100, "VEHICLE", anchor="middle", fill=STEEL),
        t(120, 122, "HARNESS", anchor="middle", fill=STEEL),
        t(120, 150, "pin 1  YE/BU", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(120, 170, "pin 9  BN/BU", anchor="middle", fill=AMBER, size=12, family=MONO),
        line(220, 140, 280, 140),
        r(280, 70, 170, 140, fill=PANEL2, stroke=AMBER),
        t(365, 108, "Y FEMALE", anchor="middle", fill=AMBER, size=13, family=MONO),
        t(365, 132, "to vehicle plug", anchor="middle", fill=MUTED, size=12),
        t(365, 168, "all 12 pins 1:1", anchor="middle", size=12),
        line(450, 110, 510, 110, stroke=STEEL),
        path("M365 210 V250 H510"),
        r(510, 50, 190, 120),
        t(605, 90, "Y MALE", anchor="middle", fill=STEEL, size=13, family=MONO),
        t(605, 112, "→ WPC 1877045", anchor="middle", size=12),
        t(605, 134, "Qi + NFC + CAN", anchor="middle", fill=MUTED, size=12),
        r(510, 210, 190, 130, stroke=AMBER),
        t(605, 248, "PADTAP TAP", anchor="middle", fill=AMBER, size=13, family=MONO),
        t(605, 272, "1  YE/BU  48 V HSD", anchor="middle", size=12),
        t(605, 292, "9  BN/BU  GND", anchor="middle", size=12),
        t(605, 312, "4  GY  LIN listen", anchor="middle", fill=MUTED, size=12),
        t(20, 250, "Never break pin 10 (LIN to HVAC switchpack) or 11/12 (key-card CAN).", fill=DANGER, size=13),
        t(20, 272, "Pin 3 is USB GND pass-through — not PadTap return.", fill=MUTED, size=13),
        t(20, 294, "HSD X0034-91 is shared with USB. NTC + 80 ms ramp. Strain-relief.", fill=MUTED, size=13),
    ]
    (OUT / "harness.svg").write_text(svg(720, 360, "\n".join(parts), "Y-harness"), encoding="utf-8")


def voltage():
    # 0–70 V mapped onto 12%–82% of width (pad 80 px)
    def x(v):
        return 40 + (v / 70.0) * 640

    parts = [
        t(20, 28, "VOLTAGE OVERLAP  ·  TESLA 48 V vs STARLINK MINI", fill=AMBER, size=12, family=MONO),
        r(20, 50, 680, 200, fill=PANEL),
        line(40, 110, 680, 110, stroke=LINE, sw=4),
        # Mini printed 12–48
        f'<rect x="{x(12):.1f}" y="98" width="{x(48)-x(12):.1f}" height="12" rx="2" fill="{OK}" opacity="0.45"/>',
        # Mini hardware 48–56
        f'<rect x="{x(48):.1f}" y="98" width="{x(56)-x(48):.1f}" height="12" rx="2" fill="{AMBER}" opacity="0.55"/>',
        # Tesla 28–50 nominal overlap
        f'<rect x="{x(28):.1f}" y="118" width="{x(50)-x(28):.1f}" height="8" rx="2" fill="{AMBER}" opacity="0.85"/>',
        # Tesla 56–58 danger
        f'<rect x="{x(56):.1f}" y="98" width="{x(58)-x(56):.1f}" height="12" rx="2" fill="{DANGER}"/>',
    ]
    for v, label, col in [(12, "12", MUTED), (28, "28", MUTED), (48, "48", TEXT), (56, "56 OVLO", AMBER), (58, "58", DANGER)]:
        parts += [
            line(x(v), 88, x(v), 132, stroke=col, sw=1),
            t(x(v), 84, label, fill=col, size=11, family=MONO, anchor="middle"),
        ]
    parts += [
        t(40, 168, "Mini printed 12–48 V", fill=OK, size=13),
        t(40, 190, "Mini hardware ~56 V  ·  Direct FET opens here", fill=AMBER, size=13),
        t(40, 212, "Tesla accessory max 58 V  ·  Direct disconnects, Buck absorbs", fill=DANGER, size=13),
        t(40, 234, "Nominal Cybertruck rail 44–50 V — both builds pass this", fill=MUTED, size=13),
    ]
    (OUT / "voltage.svg").write_text(svg(720, 270, "\n".join(parts), "Voltage overlap"), encoding="utf-8")


def schematic_direct():
    """Low-side N-FET switched pass-through + LM393 OVLO."""
    w, h = 1280, 720
    parts = [
        t(24, 32, "SCHEMATIC  ·  PADTAP DIRECT 48 V  ·  LOW-SIDE SWITCH  ·  OVLO 56.0 V", fill=AMBER, size=13, family=MONO),
        # Tesla source
        r(24, 80, 130, 70, fill=PANEL2, stroke=AMBER),
        t(89, 108, "TESLA 48 V", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(89, 128, "28–58 V", anchor="middle", fill=MUTED, size=11),
        line(154, 115, 190, 115),
        r(190, 98, 58, 34, fill=PANEL2, stroke=STEEL, rx=4),
        t(219, 120, "F1 3A", anchor="middle", fill=TEXT, size=11, family=MONO),
        line(248, 115, 262, 115),
        r(262, 98, 70, 34, fill=PANEL2, stroke=AMBER, rx=4),
        t(297, 120, "NTC 10Ω", anchor="middle", fill=AMBER, size=11, family=MONO),
        line(332, 115, 346, 115),
        r(346, 98, 72, 34, fill=PANEL2, stroke=STEEL, rx=4),
        t(382, 120, "D1 SS510", anchor="middle", fill=TEXT, size=11, family=MONO),
        line(418, 115, 455, 115),
        circ(455, 115, 4, fill=AMBER, stroke=AMBER),
        t(455, 90, "VIN_48", fill=AMBER, size=11, family=MONO, anchor="middle"),
        # TVS down
        line(455, 115, 455, 170, stroke=STEEL),
        r(410, 170, 90, 36, fill=PANEL2, stroke=STEEL, rx=4),
        t(455, 193, "D2 SMBJ58A", anchor="middle", fill=TEXT, size=11, family=MONO),
        line(455, 206, 455, 250, stroke=STEEL),
        t(470, 248, "GND", fill=MUTED, size=11, family=MONO),
        # 5V buck
        line(455, 115, 560, 115),
        r(560, 70, 160, 90, fill=PANEL2, stroke=AMBER),
        t(640, 100, "U2  5 V BUCK", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(640, 120, "7–60 V in", anchor="middle", fill=MUTED, size=11),
        t(640, 140, "not MP1584", anchor="middle", fill=MUTED, size=11),
        line(720, 115, 760, 115, stroke=OK),
        r(760, 70, 200, 150, fill=PANEL2, stroke=AMBER),
        t(860, 100, "U3 ESP32-C3", anchor="middle", fill=AMBER, size=13, family=MONO),
        t(860, 122, "GPIO20 LIN RX", anchor="middle", fill=MUTED, size=11, family=MONO),
        t(860, 140, "GPIO5  FET gate", anchor="middle", fill=MUTED, size=11, family=MONO),
        t(860, 158, "GPIO4  VIN ADC", anchor="middle", fill=MUTED, size=11, family=MONO),
        t(860, 176, "GPIO6/7 LEDs", anchor="middle", fill=MUTED, size=11, family=MONO),
        t(860, 198, "USB-C program", anchor="middle", fill=MUTED, size=11, family=MONO),
        # TLIN
        r(760, 240, 200, 90, fill=PANEL2),
        t(860, 270, "U4 TLIN2029A-Q1", anchor="middle", fill=STEEL, size=12, family=MONO),
        t(860, 292, "RXD → GPIO20", anchor="middle", fill=MUTED, size=11, family=MONO),
        t(860, 310, "TXD not wired", anchor="middle", fill=DANGER, size=11, family=MONO),
        # LIN from left
        r(24, 240, 130, 70),
        t(89, 268, "LIN TAP", anchor="middle", fill=OK, size=12, family=MONO),
        t(89, 288, "22 AWG listen", anchor="middle", fill=MUTED, size=11),
        line(154, 275, 760, 275, stroke=OK),
        # Barrel + always hot
        line(455, 115, 455, 340, stroke=AMBER),
        line(455, 340, 200, 340),
        r(80, 322, 120, 36, fill=PANEL2, stroke=STEEL, rx=4),
        t(140, 345, "F2 3 A", anchor="middle", fill=TEXT, size=12, family=MONO),
        line(80, 340, 40, 340),
        r(24, 370, 150, 90, stroke=AMBER),
        t(99, 404, "BARREL 5.5 mm", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(99, 424, "center +  = VIN", anchor="middle", fill=MUTED, size=11),
        t(99, 442, "sleeve     = switched", anchor="middle", fill=MUTED, size=11),
        # FET low side
        line(99, 460, 99, 520, stroke=STEEL),
        r(40, 520, 160, 80, fill=PANEL2, stroke=AMBER),
        t(120, 548, "Q1 FQP13N10L", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(120, 568, "N-FET 100 V  low-side", anchor="middle", fill=MUTED, size=11),
        t(120, 586, "D ← sleeve   S → GND", anchor="middle", fill=MUTED, size=11, family=MONO),
        line(120, 600, 120, 640, stroke=STEEL),
        t(130, 636, "GND", fill=MUTED, size=11, family=MONO),
        # Gate from ESP32
        path("M760 158 H700 V560 H200", stroke=BLUE, sw=1.5),
        t(430, 548, "nGATE  80 ms ramp + LM393 OC", fill=BLUE, size=11, family=MONO, anchor="middle"),
        # OVLO block
        r(280, 390, 280, 210, fill=PANEL2, stroke=AMBER),
        t(420, 418, "OVLO  ·  U1 LM393", anchor="middle", fill=AMBER, size=13, family=MONO),
        t(420, 442, "IN+  TL431  2.495 V", anchor="middle", fill=TEXT, size=12, family=MONO),
        t(420, 462, "IN−  VIN × 10k / 225k", anchor="middle", fill=TEXT, size=12, family=MONO),
        t(420, 486, "trip  2.495 × 22.5 = 56.14 V", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(420, 510, "OC → Q1 gate  (wins over GPIO)", anchor="middle", fill=MUTED, size=12),
        t(420, 532, "firmware latch 56.0 / clear 54.0", anchor="middle", fill=MUTED, size=12),
        t(420, 556, "serial  ov reset", anchor="middle", fill=MUTED, size=12, family=MONO),
        t(420, 580, "Do not clamp Tesla rail with 54 V TVS", anchor="middle", fill=DANGER, size=11),
        # ADC divider note
        t(560, 200, "R1/R2 100k/10k → GPIO4 + 3.3 V zener", fill=MUTED, size=11, family=MONO),
        t(24, 690, "NTC on VIN (harness) stops buck inrush into Tesla digital fuses. 80 ms FET ramp stops Mini input-cap dump. Do not skip either.", fill=AMBER, size=12),
        t(24, 710, "Low-side switch: barrel sleeve is opened. Do not low-side the WPC ground. LIN TX stays off.", fill=MUTED, size=12),
    ]
    (OUT / "schematic-direct.svg").write_text(svg(w, h, "\n".join(parts), "Direct 48 V schematic"), encoding="utf-8")


def schematic_buck():
    w, h = 1280, 640
    parts = [
        t(24, 32, "SCHEMATIC  ·  PADTAP BUCK 36 V  ·  CONSERVATIVE  ·  STAYS IN 12–48 V PRINT", fill=AMBER, size=13, family=MONO),
        r(24, 80, 130, 70, fill=PANEL2, stroke=AMBER),
        t(89, 108, "TESLA 48 V", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(89, 128, "28–58 V", anchor="middle", fill=MUTED, size=11),
        line(154, 115, 190, 115),
        r(190, 98, 58, 34, fill=PANEL2, stroke=STEEL, rx=4),
        t(219, 120, "F1 3A", anchor="middle", fill=TEXT, size=11, family=MONO),
        line(248, 115, 262, 115),
        r(262, 98, 70, 34, fill=PANEL2, stroke=AMBER, rx=4),
        t(297, 120, "NTC 10Ω", anchor="middle", fill=AMBER, size=11, family=MONO),
        line(332, 115, 346, 115),
        r(346, 98, 72, 34, fill=PANEL2, stroke=STEEL, rx=4),
        t(382, 120, "D1 SS510", anchor="middle", fill=TEXT, size=11, family=MONO),
        line(418, 115, 455, 115),
        circ(455, 115, 4, fill=AMBER, stroke=AMBER),
        t(455, 90, "VIN_48", fill=AMBER, size=11, family=MONO, anchor="middle"),
        line(455, 115, 455, 170, stroke=STEEL),
        r(410, 170, 90, 36, fill=PANEL2, stroke=STEEL, rx=4),
        t(455, 193, "D2 SMBJ58A", anchor="middle", fill=TEXT, size=11, family=MONO),
        # two bucks
        line(455, 115, 560, 80),
        r(560, 50, 200, 80, fill=PANEL2, stroke=AMBER),
        t(660, 80, "U5  36 V BUCK  3 A", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(660, 100, "≤12 mm tall  ·  60 V in", anchor="middle", fill=MUTED, size=11),
        t(660, 118, "set 36.00 V  ·  Loctite pot", anchor="middle", fill=MUTED, size=11),
        line(455, 115, 560, 175),
        r(560, 150, 200, 70, fill=PANEL2),
        t(660, 178, "U2  5 V BUCK", anchor="middle", fill=STEEL, size=12, family=MONO),
        t(660, 198, "ESP32 + TLIN VSUP", anchor="middle", fill=MUTED, size=11),
        line(760, 90, 820, 90),
        r(820, 50, 160, 70, fill=PANEL2, stroke=STEEL, rx=4),
        t(900, 78, "D3 SMBJ40A", anchor="middle", fill=TEXT, size=12, family=MONO),
        t(900, 98, "across 36 V", anchor="middle", fill=MUTED, size=11),
        line(900, 120, 900, 200, stroke=STEEL),
        r(820, 200, 160, 80, fill=PANEL2, stroke=AMBER),
        t(900, 232, "Q1 FQP30N06L", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(900, 252, "low-side on 36 V return", anchor="middle", fill=MUTED, size=11),
        t(900, 270, "60 V OK here", anchor="middle", fill=MUTED, size=11),
        line(900, 280, 900, 340, stroke=STEEL),
        r(820, 340, 200, 80, stroke=AMBER),
        t(920, 372, "BARREL 5.5 mm", anchor="middle", fill=AMBER, size=12, family=MONO),
        t(920, 394, "center +  = 36.00 V", anchor="middle", fill=MUTED, size=11),
        t(920, 412, "F2 3 A on 36 V out", anchor="middle", fill=MUTED, size=11),
        r(560, 250, 200, 170, fill=PANEL2, stroke=AMBER),
        t(660, 284, "U3 ESP32-C3", anchor="middle", fill=AMBER, size=13, family=MONO),
        t(660, 308, "same GPIO map", anchor="middle", fill=MUTED, size=12),
        t(660, 328, "U4 TLIN2029  RX only", anchor="middle", fill=MUTED, size=12),
        t(660, 352, "OVLO still in firmware", anchor="middle", fill=AMBER, size=12),
        t(660, 374, "mis-set pot cannot pass 58 V", anchor="middle", fill=MUTED, size=11),
        t(660, 396, "pio run -e buck", anchor="middle", fill=STEEL, size=12, family=MONO),
        t(24, 500, "NTC on VIN is not optional. Tesla digital fuses trip on the 36 V module’s input caps — same failure as a raw buck on the frunk tap.", fill=AMBER, size=13),
        t(24, 524, "Same Y-harness, same sled, same 80 ms FET ramp. Extra parts: 36 V module, FQP30N06L, SMBJ40A.", fill=MUTED, size=13),
        t(24, 560, "Forbidden: LM2596 (40 V), MP1584 (28 V), driving LIN TX, low-siding the WPC ground.", fill=DANGER, size=13),
    ]
    (OUT / "schematic-buck.svg").write_text(svg(w, h, "\n".join(parts), "Buck 36 V schematic"), encoding="utf-8")


def gpio():
    rows = [
        ("GPIO20", "UART RX", "TLIN2029 RXD", "LIN 19.2 kbps 8E1. TX pin not wired."),
        ("GPIO5", "FET gate", "Q1 via 1 k", "Active high. LM393 OC can pull it down."),
        ("GPIO4", "ADC", "VIN_48 divider", "100 k / 10 k + 3.3 V zener. 12-bit."),
        ("GPIO6", "LED amber", "Rail present", "VIN > 30 V. Lid membrane."),
        ("GPIO7", "LED green", "Output armed", "FET on. Lid membrane."),
        ("USB-C", "CDC", "ESP32-C3 SuperMini", "Flash + serial. Tape the window after."),
    ]
    parts = [t(24, 32, "GPIO MAP  ·  ESP32-C3 SUPERMINI  ·  SAME FOR DIRECT AND BUCK", fill=AMBER, size=12, family=MONO)]
    y = 56
    parts.append(r(20, 48, 760, 46, fill=PANEL2, stroke="none", rx=4))
    for i, h in enumerate(["PIN", "FN", "NET", "NOTES"]):
        xs = [40, 140, 280, 430][i]
        parts.append(t(xs, 76, h, fill=MUTED, size=11, family=MONO))
    y = 100
    for pin, fn, net, notes in rows:
        parts.append(r(20, y, 760, 44, fill=PANEL if y % 88 == 100 else PANEL2, stroke="none", rx=4))
        parts += [
            t(40, y + 28, pin, fill=AMBER, size=13, family=MONO),
            t(140, y + 28, fn, fill=TEXT, size=13),
            t(280, y + 28, net, fill=STEEL, size=13, family=MONO),
            t(430, y + 28, notes, fill=MUTED, size=13),
        ]
        y += 48
    (OUT / "gpio.svg").write_text(svg(800, y + 20, "\n".join(parts), "GPIO map"), encoding="utf-8")


def enclosure_iso():
    parts = [
        t(360, 28, "ENCLOSURE  ·  EXPLODED  ·  108 × 56 × 18 mm  ·  LID STICKS TO PANEL", fill=AMBER, size=12, family=MONO, anchor="middle"),
        # lid
        path("M250 86 L470 86 L510 62 L290 62 Z", fill=PANEL2, stroke=AMBER, sw=1.5),
        path("M470 86 L510 62 L510 74 L470 98 Z", fill=PANEL, stroke=LINE),
        path("M250 86 L470 86 L470 98 L250 98 Z", fill=PANEL, stroke=LINE),
        f'<rect x="268" y="70" width="22" height="14" fill="{AMBER}" opacity="0.35"/>',
        f'<rect x="420" y="70" width="22" height="14" fill="{AMBER}" opacity="0.35"/>',
        circ(410, 76, 4, fill=AMBER, stroke=AMBER),
        circ(428, 76, 4, fill=OK, stroke=OK),
        t(380, 52, "LID  ·  VHB FACE UP", fill=AMBER, size=11, family=MONO, anchor="middle"),
        line(270, 110, 270, 168, stroke=LINE, sw=1),
        line(490, 110, 490, 168, stroke=LINE, sw=1),
        f'<line x1="270" y1="110" x2="270" y2="168" stroke="{LINE}" stroke-dasharray="4 4"/>',
        f'<line x1="490" y1="110" x2="490" y2="168" stroke="{LINE}" stroke-dasharray="4 4"/>',
        # base
        path("M220 238 L480 238 L520 214 L260 214 Z", fill=PANEL2, stroke=STEEL, sw=1.5),
        path("M220 238 L480 238 L480 286 L220 286 Z", fill=PANEL, stroke=LINE),
        path("M480 238 L520 214 L520 262 L480 286 Z", fill=PANEL2, stroke=LINE),
        r(220, 250, 8, 8, fill=BG, stroke=AMBER, rx=1),
        r(220, 262, 8, 8, fill=BG, stroke=AMBER, rx=1),
        r(220, 274, 8, 8, fill=BG, stroke=AMBER, rx=1),
        t(208, 268, "COMB", fill=AMBER, size=10, family=MONO, anchor="end"),
        circ(480, 262, 7, fill=BG, stroke=AMBER),
        t(498, 248, "Ø8.2 BARREL", fill=AMBER, size=10, family=MONO),
        r(380, 278, 28, 6, fill=BG, stroke=AMBER, rx=1),
        t(394, 304, "USB-C", fill=AMBER, size=10, family=MONO, anchor="middle"),
        t(370, 204, "BASE  ·  16.2 mm", fill=STEEL, size=11, family=MONO, anchor="middle"),
        t(80, 380, "108 mm", fill=MUTED, size=12, family=MONO),
        t(600, 250, "56 mm", fill=MUTED, size=12, family=MONO),
        t(600, 190, "18 mm drop", fill=MUTED, size=12, family=MONO),
        line(220, 360, 520, 360, stroke=LINE),
    ]
    (OUT / "enclosure-iso.svg").write_text(svg(720, 400, "\n".join(parts), "Enclosure exploded"), encoding="utf-8")


def enclosure_pack(direct=True):
    label = "OVLO 56 V" if direct else "36 V BUCK ≤12 mm"
    sub = "LM393 + TL431 + 215 k" if direct else "50 × 25 · 60 V in"
    fet = "100 V" if direct else "flat"
    parts = [
        t(360, 22, f"TOP  ·  LID OFF  ·  {'DIRECT 48 V' if direct else 'BUCK 36 V'}  ·  104.8 × 52.8 × 14.6 mm",
          fill=AMBER, size=12, family=MONO, anchor="middle"),
        r(48, 48, 624, 248, fill=PANEL, stroke=STEEL, rx=10),
    ]
    for i in range(3):
        parts.append(r(48, 88 + i * 36, 14, 22, fill=BG, stroke=AMBER, rx=1))
    parts += [
        t(36, 178, "COMB", fill=AMBER, size=11, family=MONO, anchor="end"),
        r(86, 64, 250, 88, fill=PANEL2, stroke=AMBER, rx=4),
        t(211, 102, label, fill=AMBER, size=13, family=MONO, anchor="middle"),
        t(211, 122, sub, fill=MUTED, size=11, anchor="middle"),
        r(86, 168, 168, 80, fill=PANEL2, rx=4),
        t(170, 204, "LIN PHY", fill=STEEL, size=12, family=MONO, anchor="middle"),
        t(170, 222, "TX off", fill=MUTED, size=11, anchor="middle"),
        r(266, 168, 110, 80, fill=PANEL2, rx=4),
        t(321, 204, "5 V", fill=STEEL, size=12, family=MONO, anchor="middle"),
        t(321, 222, "22 × 17", fill=MUTED, size=11, anchor="middle"),
        r(390, 168, 140, 80, fill=PANEL2, stroke=AMBER, rx=4),
        t(460, 204, "ESP32-C3", fill=AMBER, size=12, family=MONO, anchor="middle"),
        t(460, 222, "USB → south", fill=MUTED, size=11, anchor="middle"),
        r(546, 64, 70, 184, fill=PANEL2, rx=4),
        t(581, 150, "FET", fill=STEEL, size=11, family=MONO, anchor="middle"),
        t(581, 168, fet, fill=MUTED, size=10, anchor="middle"),
        circ(672, 172, 16, fill=BG, stroke=AMBER, sw=1.5),
        t(704, 168, "Ø8.2", fill=AMBER, size=11, family=MONO),
        r(422, 288, 76, 8, fill=BG, stroke=AMBER, rx=1),
        t(460, 322, "USB-C", fill=AMBER, size=11, family=MONO, anchor="middle"),
    ]
    name = "enclosure-pack-direct.svg" if direct else "enclosure-pack-buck.svg"
    (OUT / name).write_text(svg(720, 340, "\n".join(parts), f"Interior packing {label}"), encoding="utf-8")


def enclosure_section():
    parts = [
        t(360, 22, "SECTION  ·  STUCK UNDER THE PANEL  ·  18 mm DROP", fill=AMBER, size=12, family=MONO, anchor="middle"),
        r(80, 44, 560, 28, fill=PANEL2, stroke=STEEL, rx=2),
        t(360, 63, "Console panel underside", fill=STEEL, size=12, anchor="middle"),
    ]
    for x in (140, 250, 430, 540):
        parts.append(f'<rect x="{x}" y="72" width="36" height="8" fill="{AMBER}" opacity="0.7"/>')
    parts += [
        t(88, 80, "VHB", fill=AMBER, size=10, family=MONO),
        r(100, 80, 520, 14, fill=PANEL, stroke=AMBER, rx=1),
        t(360, 91, "LID  ·  BED FACE UP", fill=AMBER, size=11, family=MONO, anchor="middle"),
        r(100, 94, 520, 110, fill=BG, stroke=LINE, rx=1),
        r(130, 110, 220, 54, fill=PANEL2, stroke=AMBER, rx=3),
        t(240, 142, "OVLO + 100 V FET", fill=AMBER, size=12, family=MONO, anchor="middle"),
        r(370, 118, 90, 38, fill=PANEL2, rx=3),
        t(415, 142, "ESP32", fill=STEEL, size=11, family=MONO, anchor="middle"),
        r(480, 118, 70, 38, fill=PANEL2, rx=3),
        t(515, 142, "LIN", fill=STEEL, size=11, family=MONO, anchor="middle"),
        t(360, 188, "14.6 mm internal — TO-220 laid flat", fill=MUTED, size=11, anchor="middle"),
        r(100, 204, 520, 14, fill=PANEL, stroke=STEEL, rx=1),
        t(360, 215, "BASE FLOOR", fill=STEEL, size=11, family=MONO, anchor="middle"),
        line(640, 80, 640, 218),
        t(652, 156, "18 mm", fill=AMBER, size=11, family=MONO),
        t(120, 250, "← comb (drop-in)", fill=AMBER, size=11, family=MONO),
        t(600, 250, "barrel →", fill=AMBER, size=11, family=MONO, anchor="end"),
    ]
    (OUT / "enclosure-section.svg").write_text(svg(720, 280, "\n".join(parts), "Enclosure section"), encoding="utf-8")


def ovlo():
    parts = [
        t(24, 28, "OVLO DETAIL  ·  HARDWARE WINS OVER A WEDGED MCU", fill=AMBER, size=12, family=MONO),
        r(20, 48, 760, 300, fill=PANEL),
        t(48, 84, "VIN_48", fill=AMBER, size=13, family=MONO),
        path("M110 78 H200", stroke=AMBER),
        t(210, 70, "215 k 1%", fill=STEEL, size=12, family=MONO),
        line(200, 78, 360, 78, stroke=AMBER),
        circ(360, 78, 3, fill=AMBER, stroke=AMBER),
        t(372, 70, "IN−", fill=BLUE, size=12, family=MONO),
        line(360, 78, 360, 140, stroke=STEEL),
        t(210, 160, "10 k 1%", fill=STEEL, size=12, family=MONO),
        line(360, 140, 360, 200, stroke=STEEL),
        t(372, 200, "GND", fill=MUTED, size=12, family=MONO),
        r(500, 56, 240, 120, fill=PANEL2, stroke=AMBER),
        t(620, 88, "U1 LM393", fill=AMBER, size=14, family=MONO, anchor="middle"),
        t(620, 110, "IN+ = TL431 2.495 V", fill=TEXT, size=12, family=MONO, anchor="middle"),
        t(620, 130, "VCC = 5 V from U2", fill=MUTED, size=12, family=MONO, anchor="middle"),
        t(620, 150, "OC to Q1 gate", fill=TEXT, size=12, family=MONO, anchor="middle"),
        t(48, 230, "Trip  2.495 × (215k+10k)/10k  =  56.14 V", fill=AMBER, size=14, family=MONO),
        t(48, 256, "Do not substitute 200 k — that trips at 52 V, inside Tesla nominal.", fill=DANGER, size=13),
        t(48, 282, "Firmware latches at 56.0 V, clears at 54.0 V. Serial: ov reset.", fill=MUTED, size=13),
        t(48, 308, "1 k between GPIO5 and gate so a comparator fight is 3.3 mA, not 33 mA.", fill=MUTED, size=13),
        t(48, 332, "A 54 V TVS across the barrel would dump a legal 50 V Tesla rail. Disconnect, don’t clamp.", fill=MUTED, size=13),
    ]
    (OUT / "ovlo.svg").write_text(svg(800, 370, "\n".join(parts), "OVLO detail"), encoding="utf-8")


def modes():
    cards = [
        ("AUTO", "First boot", ["Latches A if 48 V drops", "on toggle; B if LIN flips."]),
        ("A", "Power-follow", ["48 V is cut with the pads.", "MOSFET follows VIN."]),
        ("B", "LIN-follow", ["Expected. MOSFET follows", "the learned enable bit.", "NFC stays up."]),
        ("C", "Awake-follow", ["On whenever the rail is up.", "Keep Outlets On / Camp."]),
    ]
    parts = [t(24, 28, "MODES  ·  OVLO AT 56.0 V OVERRIDES EVERY ONE", fill=AMBER, size=12, family=MONO)]
    x = 20
    for mid, name, lines in cards:
        parts.append(r(x, 50, 185, 150, fill=PANEL, stroke=AMBER if mid == "B" else LINE))
        parts.append(t(x + 16, 78, f"MODE {mid}", fill=AMBER, size=12, family=MONO))
        parts.append(t(x + 16, 104, name, fill=TEXT, size=15))
        yy = 132
        for ln in lines:
            parts.append(t(x + 16, yy, ln, fill=MUTED, size=12))
            yy += 18
        x += 195
    (OUT / "modes.svg").write_text(svg(800, 220, "\n".join(parts), "Firmware modes"), encoding="utf-8")


if __name__ == "__main__":
    system(True)
    system(False)
    pin_map()
    harness()
    voltage()
    schematic_direct()
    schematic_buck()
    gpio()
    enclosure_iso()
    enclosure_pack(True)
    enclosure_pack(False)
    enclosure_section()
    ovlo()
    modes()
    print("wrote", len(list(OUT.glob("*.svg"))), "svgs in", OUT)
