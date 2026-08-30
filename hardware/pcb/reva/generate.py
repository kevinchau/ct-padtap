#!/usr/bin/env python3
"""PadTap Direct 48 V Rev A — 2-layer board that fits the 108×56 sled.

Emits Gerbers (JLCPCB names), Excellon drill, BOM, CPL, and README SVGs.
Board is 104.8 × 52.8 mm (inner cavity). Fuses + NTC stay on the harness.
"""
from __future__ import annotations

import math
import zipfile
from pathlib import Path

OUT = Path(__file__).parent
GERBER = OUT / "gerber"
DOCS = Path(__file__).resolve().parents[3] / "docs" / "diagrams"

BOARD_W, BOARD_H = 104.8, 52.8
EDGE = 0.15  # copper-to-edge

# Case: wall 1.6, bosses at 5.5 from outer → 3.9 on this board
HOLES = [(3.9, 3.9), (100.9, 3.9), (3.9, 48.9), (100.9, 48.9)]


def r2(x, y=None):
    if y is None:
        return round(x, 4)
    return (round(x, 4), round(y, 4))


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------
class Pad:
    def __init__(self, ref, pin, x, y, w, h, net, plated=True, drill=0.0, rot=0, shape="rect"):
        self.ref, self.pin, self.net = ref, pin, net
        self.x, self.y, self.w, self.h = x, y, w, h
        self.plated, self.drill, self.rot, self.shape = plated, drill, rot, shape

    def corners(self):
        ca, sa = math.cos(math.radians(self.rot)), math.sin(math.radians(self.rot))
        hw, hh = self.w / 2, self.h / 2
        pts = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        out = []
        for px, py in pts:
            out.append((self.x + px * ca - py * sa, self.y + px * sa + py * ca))
        return out


class Trace:
    def __init__(self, x1, y1, x2, y2, w, net, layer="F"):
        self.x1, self.y1, self.x2, self.y2, self.w, self.net, self.layer = x1, y1, x2, y2, w, net, layer


class Via:
    def __init__(self, x, y, net, drill=0.3, od=0.6):
        self.x, self.y, self.net, self.drill, self.od = x, y, net, drill, od


class Silk:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.kw = kw


pads: list[Pad] = []
traces: list[Trace] = []
vias: list[Via] = []
silk: list[Silk] = []
courtyards: list[tuple] = []  # x,y,w,h,rot,label,fill


def add_pad(*a, **k):
    pads.append(Pad(*a, **k))


def manhattan(net, pts, w, layer="F"):
    """pts is a list of (x,y). Route orthogonal, prefer X then Y."""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if abs(x1 - x2) < 0.01:
            traces.append(Trace(x1, y1, x1, y2, w, net, layer))
        elif abs(y1 - y2) < 0.01:
            traces.append(Trace(x1, y1, x2, y1, w, net, layer))
        else:
            traces.append(Trace(x1, y1, x2, y1, w, net, layer))
            traces.append(Trace(x2, y1, x2, y2, w, net, layer))


def r0805(ref, x, y, rot, n1, n2):
    dx = 0.95 if rot == 0 else 0
    dy = 0.95 if rot == 90 else 0
    add_pad(ref, "1", x - dx, y - dy, 1.0, 1.3 if rot == 0 else 1.0, n1, rot=rot)
    add_pad(ref, "2", x + dx, y + dy, 1.0, 1.3 if rot == 0 else 1.0, n2, rot=rot)
    courtyards.append((x, y, 2.2, 1.4, rot, ref, "#2A2D32"))
    silk.append(Silk("text", x=x, y=y - 1.6, s=ref, size=0.8))


def c0805(ref, x, y, rot, n1, n2):
    r0805(ref, x, y, rot, n1, n2)


def c1210(ref, x, y, rot, n1, n2):
    dx = 1.6 if rot == 0 else 0
    dy = 1.6 if rot == 90 else 0
    add_pad(ref, "1", x - dx, y - dy, 1.6, 2.4 if rot == 0 else 1.6, n1)
    add_pad(ref, "2", x + dx, y + dy, 1.6, 2.4 if rot == 0 else 1.6, n2)
    courtyards.append((x, y, 3.6, 2.6, rot, ref, "#1C1E22"))
    silk.append(Silk("text", x=x, y=y - 2.0, s=ref, size=0.8))


def sod123(ref, x, y, rot, anode, cathode):
    # anode pad 1, cathode pad 2 (stripe)
    dx = 1.7 if rot == 0 else 0
    add_pad(ref, "A", x - dx, y, 1.2, 1.1, anode)
    add_pad(ref, "K", x + dx, y, 1.2, 1.1, cathode)
    courtyards.append((x, y, 3.9, 1.8, rot, ref, "#C5C8CE"))
    silk.append(Silk("text", x=x, y=y - 1.6, s=ref, size=0.8))


def sma(ref, x, y, anode, cathode):
    add_pad(ref, "A", x - 2.3, y, 1.7, 2.2, anode)
    add_pad(ref, "K", x + 2.3, y, 1.7, 2.2, cathode)
    courtyards.append((x, y, 5.4, 2.8, 0, ref, "#C5C8CE"))
    silk.append(Silk("text", x=x, y=y - 2.2, s=ref, size=0.8))


def smb(ref, x, y, n1, n2):
    add_pad(ref, "1", x - 2.4, y, 2.0, 2.3, n1)
    add_pad(ref, "2", x + 2.4, y, 2.0, 2.3, n2)
    courtyards.append((x, y, 5.6, 3.6, 0, ref, "#C5C8CE"))
    silk.append(Silk("text", x=x, y=y - 2.6, s=ref, size=0.8))


def soic8(ref, x, y, nets: list[str]):
    # pin 1 SW, CCW. Body 5×4.  nets[0] is pin1
    for i in range(4):
        py = y + 1.905 - i * 1.27
        add_pad(ref, str(i + 1), x - 2.7, py, 1.5, 0.6, nets[i])
        add_pad(ref, str(8 - i), x + 2.7, py, 1.5, 0.6, nets[7 - i])
    courtyards.append((x, y, 6.2, 5.0, 0, ref, "#1A1C20"))
    silk.append(Silk("text", x=x, y=y - 3.4, s=ref, size=0.8))
    silk.append(Silk("dot", x=x - 2.0, y=y + 2.2))


def sot23(ref, x, y, n1, n2, n3):
    # 1=left bot, 2=left top, 3=right (standard SOT-23)
    add_pad(ref, "1", x - 1.0, y - 0.95, 0.8, 0.7, n1)
    add_pad(ref, "2", x - 1.0, y + 0.95, 0.8, 0.7, n2)
    add_pad(ref, "3", x + 1.0, y, 0.8, 0.9, n3)
    courtyards.append((x, y, 3.0, 2.6, 0, ref, "#1A1C20"))
    silk.append(Silk("text", x=x, y=y - 2.0, s=ref, size=0.8))


def sot223(ref, x, y, tab, n1, n2, n3):
    # AMS1117: pin1 GND, pin2 VOUT=tab, pin3 VIN
    add_pad(ref, "TAB", x + 1.6, y, 3.8, 3.2, tab)
    add_pad(ref, "1", x - 2.8, y - 2.3, 1.2, 1.0, n1)
    add_pad(ref, "2", x - 2.8, y, 1.2, 1.0, n2)
    add_pad(ref, "3", x - 2.8, y + 2.3, 1.2, 1.0, n3)
    courtyards.append((x, y, 7.2, 6.6, 0, ref, "#1A1C20"))
    silk.append(Silk("text", x=x, y=y - 4.0, s=ref, size=0.8))


def dpak(ref, x, y):
    # IRLR3110: pin1 gate, pin2 drain=tab, pin3 source. Tab to the east (barrel).
    add_pad(ref, "TAB", x + 2.4, y, 6.5, 6.5, "VOUT-")
    add_pad(ref, "1", x - 4.2, y + 2.3, 1.6, 1.3, "nGATE")  # gate
    add_pad(ref, "2", x - 4.2, y, 1.6, 1.3, "VOUT-")  # drain
    add_pad(ref, "3", x - 4.2, y - 2.3, 1.6, 1.3, "GND")  # source
    courtyards.append((x, y, 10.2, 6.8, 0, ref, "#8B9098"))
    silk.append(Silk("text", x=x, y=y - 4.4, s=ref + " IRLR3110", size=0.8))


def inductor(ref, x, y, n1, n2):
    add_pad(ref, "1", x - 2.4, y, 2.0, 3.2, n1)
    add_pad(ref, "2", x + 2.4, y, 2.0, 3.2, n2)
    courtyards.append((x, y, 7.0, 6.6, 0, ref, "#4A3B2A"))
    silk.append(Silk("text", x=x, y=y - 4.0, s=ref, size=0.8))


def usb_c(ref, cx):
    # Mid-mount 16P on south edge. Opening faces -Y. Center at (cx, 0.6)
    y = 1.2
    # shell TH pads
    for sx in (-4.3, 4.3):
        add_pad(ref, "SH", cx + sx, y + 2.2, 1.4, 2.2, "GND", plated=True, drill=0.9, shape="circ")
    # SMT signal row (simplified 12 contacts we care about)
    # A1/B12 GND, A4/A9 VBUS, A6/B6 D+, A7/B7 D-, A5 CC1, B5 CC2
    sig = [
        (-3.25, "GND"),
        (-2.50, "VBUS"),
        (-1.75, "CC1"),
        (-1.00, "USB_D+"),
        (-0.25, "USB_D-"),
        (0.50, "SBU"),
        (1.25, "USB_D-"),
        (2.00, "USB_D+"),
        (2.75, "CC2"),
        (3.50, "VBUS"),
    ]
    for dx, net in sig:
        add_pad(ref, net, cx + dx, y + 0.35, 0.3, 1.1, net if net != "SBU" else "NC")
    courtyards.append((cx, 2.0, 9.2, 7.4, 0, "J3 USB-C", "#C5C8CE"))
    silk.append(Silk("text", x=cx, y=6.2, s="J3 USB-C", size=0.9))


def barrel(ref, x, y):
    # PJ-002A style 5.5 mm: sleeve / center / switch. Center = VOUT+, sleeve = VOUT-
    add_pad(ref, "TIP", x - 1.5, y, 3.2, 3.2, "VOUT+", plated=True, drill=1.2, shape="circ")
    add_pad(ref, "SLEEVE", x - 6.5, y + 4.5, 2.4, 2.4, "VOUT-", plated=True, drill=1.0, shape="circ")
    add_pad(ref, "SW", x - 6.5, y - 4.5, 2.4, 2.4, "VOUT-", plated=True, drill=1.0, shape="circ")
    courtyards.append((x - 3.5, y, 11.0, 10.5, 0, "J2 BARREL", "#2A2D32"))
    silk.append(Silk("text", x=x - 3.5, y=y - 6.6, s="J2 5.5 mm +", size=0.9))


def terminal(ref):
    # 3× 18 AWG solder pads on west, aligned with comb slots (outer y 11.6, 19.6, 27.6)
    names = [("VIN", "VIN_IN", 10.0), ("GND", "GND", 18.0), ("LIN", "LIN_BUS", 26.0)]
    for name, net, y in names:
        add_pad(ref, name, 4.8, y, 3.2, 2.6, net, plated=True, drill=1.3, shape="circ")
        silk.append(Silk("text", x=8.8, y=y + 0.3, s=name, size=1.0))
    courtyards.append((5.0, 18.0, 8.0, 20.0, 0, "J1", "#1C1E22"))
    silk.append(Silk("text", x=5.0, y=31.5, s="J1 HARNESS", size=0.9))


def esp32(ref, x, y):
    """ESP32-C3-MINI-1, 13.2 × 16.6, antenna to +Y (north). Pins we use."""
    # Two side rows, 1.27 pitch. Simplified: left IO, right power/USB.
    left = [
        (y + 6.0, "3V3"),
        (y + 4.73, "EN"),
        (y + 3.46, "IO4"),
        (y + 2.19, "IO5"),
        (y + 0.92, "IO6"),
        (y - 0.35, "IO7"),
        (y - 1.62, "IO8"),
        (y - 2.89, "IO9"),
        (y - 4.16, "IO10"),
        (y - 5.43, "GND"),
    ]
    right = [
        (y + 6.0, "IO21"),
        (y + 4.73, "IO20"),
        (y + 3.46, "IO18"),
        (y + 2.19, "IO19"),
        (y + 0.92, "IO3"),
        (y - 0.35, "IO2"),
        (y - 1.62, "IO1"),
        (y - 2.89, "IO0"),
        (y - 4.16, "GND"),
        (y - 5.43, "VIN3"),
    ]
    net_of = {
        "3V3": "3V3",
        "EN": "EN",
        "IO4": "VSENSE",
        "IO5": "GPIO5",
        "IO6": "LED_RAIL",
        "IO7": "LED_ARM",
        "IO8": "IO8",
        "IO9": "BOOT",
        "IO10": "IO10",
        "GND": "GND",
        "IO21": "IO21",
        "IO20": "LIN_RX",
        "IO18": "USB_D-",
        "IO19": "USB_D+",
        "IO3": "IO3",
        "IO2": "IO2",
        "IO1": "IO1",
        "IO0": "IO0",
        "VIN3": "3V3",
    }
    for py, name in left:
        add_pad(ref, name, x - 5.6, py, 1.6, 0.7, net_of[name])
    for py, name in right:
        add_pad(ref, name, x + 5.6, py, 1.6, 0.7, net_of[name])
    courtyards.append((x, y, 13.4, 16.8, 0, "U1 ESP32-C3-MINI-1", "#1A1C20"))
    silk.append(Silk("text", x=x, y=y + 9.6, s="U1 ESP32-C3-MINI-1", size=0.9))
    silk.append(Silk("text", x=x, y=y + 8.4, s="ANTENNA KEEP-OUT", size=0.7))


def led(ref, x, y, net):
    add_pad(ref, "A", x - 0.85, y, 0.9, 1.2, net)
    add_pad(ref, "K", x + 0.85, y, 0.9, 1.2, "GND")
    courtyards.append((x, y, 2.2, 1.4, 0, ref, "#E8A317" if "RAIL" in ref else "#7DAE74"))
    silk.append(Silk("text", x=x, y=y - 1.6, s=ref, size=0.7))


# ---------------------------------------------------------------------------
# Place
# ---------------------------------------------------------------------------
def place():
    terminal("J1")
    usb_c("J3", 75.2)
    barrel("J2", 100.5, 26.4)

    # Input protection west-center
    sma("D1", 18.0, 12.0, "VIN_IN", "VIN_48")  # SS510, stripe to VIN_48
    smb("D2", 18.0, 20.5, "VIN_48", "GND")  # SMBJ58A
    c1210("C1", 18.0, 29.0, 0, "VIN_48", "GND")  # 10u 100V

    # 5 V buck
    soic8("U2", 34.0, 14.0, [
        "VIN_48",  # 1 VIN
        "VIN_48",  # 2 VIN
        "SW",      # 3 SW
        "GND",     # 4 GND
        "FB",      # 5 FB
        "EN5",     # 6 EN
        "GND",     # 7 GND
        "VIN_48",  # 8 VIN (XL7015-ish SOP8 — silk says XL7015)
    ])
    inductor("L1", 34.0, 26.5, "SW", "5V")
    r0805("Rfb1", 40.5, 20.0, 90, "5V", "FB")
    r0805("Rfb2", 43.5, 20.0, 90, "FB", "GND")
    c0805("C5v", 40.5, 26.5, 0, "5V", "GND")
    sod123("D3", 27.5, 26.5, 0, "GND", "SW")  # catch diode

    # 3V3
    sot223("U3", 34.0, 40.0, "3V3", "GND", "3V3", "5V")
    c0805("C3v", 42.5, 40.0, 0, "3V3", "GND")

    # LIN
    soic8("U4", 52.5, 40.0, [
        "LIN_RX",   # 1 RXD
        "nFAULT",   # 2
        "5V",       # 3 VSUP
        "LIN_BUS",  # 4 LIN
        "TXD_PU",   # 5 TXD — pulled high, NOT to MCU
        "GND",      # 6 GND
        "5V",       # 7 EN
        "5V",       # 8 nWAKE
    ])
    r0805("Rtx", 60.0, 40.0, 0, "TXD_PU", "5V")
    c0805("Clin", 60.0, 44.5, 0, "LIN_BUS", "GND")

    # OVLO
    soic8("U5", 52.5, 24.0, [
        "1IN-", "1IN+", "1OUT", "GND",
        "2OUT", "2IN-", "2IN+", "5V",
    ])
    sot23("U6", 63.5, 18.5, "GND", "VREF", "5V")  # TL431: 1 anode, 2 cathode=ref, 3 ref (TO-92 mapping varies)
    # SOT-23 TL431: 1 ref, 2 anode, 3 cathode commonly (pinout-A)
    # We'll treat n1=anode GND, n3=cathode VREF, n2=ref tied to cathode for 2.495
    r0805("R215", 63.5, 24.0, 90, "VIN_48", "1IN-")
    r0805("R10ov", 66.5, 24.0, 90, "1IN-", "GND")
    r0805("Rref", 63.5, 13.5, 0, "5V", "VREF")
    # LM393 pin2 1IN+ = VREF, pin1 1IN- = divider, pin3 1OUT = nGATE (OC)

    # Sense
    r0805("R100k", 63.5, 30.5, 90, "VIN_48", "VSENSE")
    r0805("R10k", 66.5, 30.5, 90, "VSENSE", "GND")
    sod123("Dz", 70.5, 30.5, 0, "GND", "VSENSE")  # 3.3 V zener

    # Gate
    r0805("R1k", 78.0, 36.0, 0, "GPIO5", "nGATE")
    r0805("R10g", 78.0, 40.0, 0, "nGATE", "GND")
    r0805("R47k", 84.0, 36.0, 0, "nGATE", "nGATE")  # placeholder — RC on gate
    c0805("Cgate", 84.0, 40.0, 0, "nGATE", "GND")

    # MCU + USB
    esp32("U1", 75.0, 16.5)
    led("Drail", 72.4, 38.4, "LED_RAIL")
    led("Darm", 80.4, 38.4, "LED_ARM")
    r0805("Rr", 72.4, 42.2, 0, "LED_RAIL", "GPIO6")
    r0805("Ra", 80.4, 42.2, 0, "LED_ARM", "GPIO7")
    r0805("Ren", 68.0, 8.5, 0, "EN", "3V3")
    r0805("Rboot", 82.0, 8.5, 0, "BOOT", "3V3")
    c0805("Cen", 68.0, 5.8, 0, "EN", "GND")
    r0805("Rcc1", 70.0, 3.2, 0, "CC1", "GND")
    r0805("Rcc2", 80.0, 3.2, 0, "CC2", "GND")
    sod123("Dusb", 62.0, 8.5, 0, "VBUS", "5V")

    # FET
    dpak("Q1", 90.5, 26.4)

    # Mounting (NPTH)
    for i, (hx, hy) in enumerate(HOLES, 1):
        add_pad(f"H{i}", "1", hx, hy, 5.5, 5.5, "GND", plated=True, drill=3.2, shape="circ")

    # Vias to GND pour
    gnd_vias = [
        (12, 18), (12, 36), (25, 36), (25, 8),
        (45, 8), (45, 48), (70, 48), (95, 8),
        (95, 44), (88, 18), (88, 34), (55, 12),
        (40, 48), (20, 48), (75, 28), (96, 26.4),
    ]
    for x, y in gnd_vias:
        vias.append(Via(x, y, "GND"))
    vias.append(Via(52.5, 18.0, "VREF", drill=0.3, od=0.6))
    vias.append(Via(78.0, 32.0, "nGATE"))
    vias.append(Via(75.0, 28.5, "LIN_RX"))
    vias.append(Via(90.5, 32.5, "VOUT-"))
    vias.append(Via(96.0, 20.0, "VOUT+"))


def route():
    W, WS, WP = 0.35, 0.25, 1.2  # signal, small, power

    def pad(ref, pin):
        for p in pads:
            if p.ref == ref and p.pin == pin:
                return (p.x, p.y)
        raise KeyError(ref, pin)

    # VIN_IN J1 → D1 anode → D1 K = VIN_48
    manhattan("VIN_IN", [pad("J1", "VIN"), pad("D1", "A")], WP)
    manhattan("VIN_48", [pad("D1", "K"), (18, 16), pad("D2", "1")], WP)
    manhattan("VIN_48", [pad("D1", "K"), (24, 12), (24, 14), pad("U2", "1")], WP)
    manhattan("VIN_48", [(24, 14), (24, 29), pad("C1", "1")], WP)

    # VIN_48 → barrel tip (VOUT+)
    manhattan("VOUT+", [pad("D1", "K"), (24, 12), (96, 12), pad("J2", "TIP")], WP)
    manhattan("VOUT+", [pad("J2", "TIP"), (96, 20)], WP)

    # Q1 drain tab → barrel sleeve
    manhattan("VOUT-", [pad("Q1", "TAB"), (96.5, 26.4), pad("J2", "SLEEVE")], WP)

    # 5V
    manhattan("5V", [pad("L1", "2"), pad("C5v", "1")], W)
    manhattan("5V", [pad("C5v", "1"), (40.5, 40), pad("U3", "3")], W)
    manhattan("5V", [(46, 40), (46, 40), pad("U4", "3")], W)

    # SW
    manhattan("SW", [pad("U2", "3"), (31.3, 14), (31.3, 26.5), pad("L1", "1")], W)

    # 3V3 to ESP
    manhattan("3V3", [pad("U3", "TAB"), (48, 40), (48, 22.5), pad("U1", "3V3")], W)

    # LIN
    manhattan("LIN_BUS", [pad("J1", "LIN"), (12, 26), (12, 40), (49.8, 40), pad("U4", "4")], WS)
    manhattan("LIN_RX", [pad("U4", "1"), (49.8, 44.8), (80.6, 44.8), (80.6, 21.23), pad("U1", "IO20")], WS)

    # Gate
    manhattan("GPIO5", [pad("U1", "IO5"), (69.4, 18.69), (69.4, 36), pad("R1k", "1")], WS)
    manhattan("nGATE", [pad("R1k", "2"), (90.5, 36), pad("Q1", "1")], WS)
    manhattan("nGATE", [pad("U5", "3"), (52.5, 21.0), (78, 21), (78, 36), pad("R1k", "2")], WS)

    # ADC
    manhattan("VSENSE", [pad("R100k", "2"), pad("U1", "IO4")], WS)

    # USB
    manhattan("USB_D+", [pad("U1", "IO19"), (80.6, 18.69), (80.6, 4.0), (77.0, 4.0)], WS)
    manhattan("USB_D-", [pad("U1", "IO18"), (80.6, 19.96), (86, 19.96), (86, 4.5), (74.0, 4.5)], WS)
    manhattan("VBUS", [(78.7, 1.55), (78.7, 8.5), pad("Dusb", "A")], W)

    # LEDs
    manhattan("GPIO6", [pad("U1", "IO6"), (69.4, 17.42), (69.4, 42.2), pad("Rr", "2")], WS)
    manhattan("GPIO7", [pad("U1", "IO7"), (69.4, 16.15), (88, 16.15), (88, 42.2), pad("Ra", "2")], WS)

    # EN / boot
    manhattan("EN", [pad("U1", "EN"), pad("Ren", "1")], WS)
    manhattan("BOOT", [pad("U1", "IO9"), pad("Rboot", "1")], WS)

    # Tie 1IN+ to VREF
    manhattan("VREF", [pad("U6", "3"), (63.5, 21.1), pad("U5", "2")], WS)
    manhattan("1IN-", [pad("R215", "2"), pad("U5", "1")], WS)

    # GND stitches from pads that sit on top — short to nearby via
    manhattan("GND", [pad("J1", "GND"), (12, 18)], WP)


# ---------------------------------------------------------------------------
# Gerber
# ---------------------------------------------------------------------------
def gxy(x, y):
    return f"X{int(round(x * 1_000_000))}Y{int(round(y * 1_000_000))}"


class Gbr:
    def __init__(self):
        self.ap = {}  # key -> d-code
        self.n = 10
        self.body = []

    def aper(self, key, defn):
        if key not in self.ap:
            self.ap[key] = self.n
            self.n += 1
        return self.ap[key]

    def sel(self, key, defn):
        d = self.aper(key, defn)
        self.body.append(f"D{d}*")
        return d

    def dumps(self, name):
        lines = [
            "%FSLAX36Y36*%",
            "%MOMM*%",
            f"G04 {name}*",
            "%LPD*%",
        ]
        for key, d in sorted(self.ap.items(), key=lambda kv: kv[1]):
            if key[0] == "C":
                lines.append(f"%ADD{d}C,{key[1:]}*%")
            elif key[0] == "R":
                w, h = key[1:].split("x")
                lines.append(f"%ADD{d}R,{w}X{h}*%")
        lines.extend(self.body)
        lines.append("M02*")
        return "\n".join(lines) + "\n"


def emit_gerbers():
    GERBER.mkdir(parents=True, exist_ok=True)
    layers = {
        "GTL": Gbr(),
        "GBL": Gbr(),
        "GTS": Gbr(),
        "GBS": Gbr(),
        "GTO": Gbr(),
        "GBO": Gbr(),
        "GKO": Gbr(),
        "GTP": Gbr(),
    }

    # Outline
    ko = layers["GKO"]
    ko.sel("C0.100", "C")
    pts = [(0, 0), (BOARD_W, 0), (BOARD_W, BOARD_H), (0, BOARD_H), (0, 0)]
    ko.body.append("G01*")
    ko.body.append(gxy(*pts[0]) + "D02*")
    for p in pts[1:]:
        ko.body.append(gxy(*p) + "D01*")

    def flash_pad(g, p, mask=False, paste=False):
        if p.shape == "circ" or p.drill:
            d = p.w if not mask else p.w + 0.1
            if mask:
                d = p.w + 0.1
            key = f"C{d:.3f}"
            g.sel(key, "C")
            g.body.append(gxy(p.x, p.y) + "D03*")
        else:
            w, h = p.w, p.h
            if mask:
                w, h = w + 0.1, h + 0.1
            if paste:
                w, h = max(0.2, w - 0.05), max(0.2, h - 0.05)
            key = f"R{w:.3f}x{h:.3f}"
            g.sel(key, "R")
            g.body.append(gxy(p.x, p.y) + "D03*")

    # Bottom GND pour as a stroked outline fill (region)
    gbl = layers["GBL"]
    gbl.body.append("G36*")
    gbl.body.append(gxy(EDGE, EDGE) + "D02*")
    gbl.body.append(gxy(BOARD_W - EDGE, EDGE) + "D01*")
    gbl.body.append(gxy(BOARD_W - EDGE, BOARD_H - EDGE) + "D01*")
    gbl.body.append(gxy(EDGE, BOARD_H - EDGE) + "D01*")
    gbl.body.append(gxy(EDGE, EDGE) + "D01*")
    gbl.body.append("G37*")

    for p in pads:
        flash_pad(layers["GTL"], p)
        flash_pad(layers["GTS"], p, mask=True)
        if p.drill == 0:
            flash_pad(layers["GTP"], p, paste=True)
        # TH also on bottom
        if p.drill:
            flash_pad(layers["GBL"], p)
            flash_pad(layers["GBS"], p, mask=True)

    for t in traces:
        g = layers["GTL"] if t.layer == "F" else layers["GBL"]
        g.sel(f"C{t.w:.3f}", "C")
        g.body.append("G01*")
        g.body.append(gxy(t.x1, t.y1) + "D02*")
        g.body.append(gxy(t.x2, t.y2) + "D01*")

    for v in vias:
        layers["GTL"].sel(f"C{v.od:.3f}", "C")
        layers["GTL"].body.append(gxy(v.x, v.y) + "D03*")
        layers["GBL"].sel(f"C{v.od:.3f}", "C")
        layers["GBL"].body.append(gxy(v.x, v.y) + "D03*")
        layers["GTS"].sel(f"C{v.od + 0.1:.3f}", "C")
        layers["GTS"].body.append(gxy(v.x, v.y) + "D03*")
        layers["GBS"].sel(f"C{v.od + 0.1:.3f}", "C")
        layers["GBS"].body.append(gxy(v.x, v.y) + "D03*")

    # Silk
    gto = layers["GTO"]
    gto.sel("C0.150", "C")
    for s in silk:
        if s.kind == "text":
            # draw a tiny tick so the layer is non-empty; SVG carries readable silk
            gto.body.append(gxy(s.kw["x"], s.kw["y"]) + "D03*")
        elif s.kind == "dot":
            gto.sel("C0.400", "C")
            gto.body.append(gxy(s.kw["x"], s.kw["y"]) + "D03*")
            gto.sel("C0.150", "C")

    names = {
        "GTL": "PadTap-RevA.GTL",
        "GBL": "PadTap-RevA.GBL",
        "GTS": "PadTap-RevA.GTS",
        "GBS": "PadTap-RevA.GBS",
        "GTO": "PadTap-RevA.GTO",
        "GBO": "PadTap-RevA.GBO",
        "GKO": "PadTap-RevA.GKO",
        "GTP": "PadTap-RevA.GTP",
    }
    for k, g in layers.items():
        (GERBER / names[k]).write_text(g.dumps(k), encoding="utf-8")

    # Excellon
    pth, npth = [], []
    tools = {}

    def tool(d):
        key = f"{d:.3f}"
        if key not in tools:
            tools[key] = f"T{len(tools) + 1:02d}"
        return tools[key]

    for p in pads:
        if p.drill:
            t = tool(p.drill)
            (npth if not p.plated else pth).append((t, p.x, p.y, p.drill, not p.plated))
    for v in vias:
        t = tool(v.drill)
        pth.append((t, v.x, v.y, v.drill, False))

    def drill_file(rows, path, plated=True):
        lines = ["M48", f";{'PTH' if plated else 'NPTH'}", "METRIC,TZ"]
        seen = {}
        for t, x, y, d, _ in rows:
            if t not in seen:
                lines.append(f"{t}C{d:.3f}")
                seen[t] = d
        lines.append("%")
        cur = None
        for t, x, y, d, _ in rows:
            if t != cur:
                lines.append(t)
                cur = t
            lines.append(f"X{x:.3f}Y{y:.3f}")
        lines.append("M30")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Split NPTH holes (mount) from PTH
    pth_rows = [(t, x, y, d, n) for t, x, y, d, n in pth + [] if True]
    # Rebuild from pads/vias
    pth_rows, npth_rows = [], []
    for p in pads:
        if not p.drill:
            continue
        t = tool(p.drill)
        if p.ref.startswith("H"):
            npth_rows.append((t, p.x, p.y, p.drill, True))
        else:
            pth_rows.append((t, p.x, p.y, p.drill, False))
    for v in vias:
        t = tool(v.drill)
        pth_rows.append((t, v.x, v.y, v.drill, False))
    drill_file(pth_rows, GERBER / "PadTap-RevA-PTH.DRL", True)
    drill_file(npth_rows, GERBER / "PadTap-RevA-NPTH.DRL", False)

    zpath = OUT / "PadTap-RevA-gerbers.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(GERBER.iterdir()):
            z.write(f, f.name)
    return zpath


# ---------------------------------------------------------------------------
# BOM / CPL
# ---------------------------------------------------------------------------
BOM = [
    ("U1", "ESP32-C3-MINI-1-N4", "C2919203", "1", "Espressif module, 4 MB"),
    ("U2", "XL7015E1 SOP-8", "C142613", "1", "5–80 V → 5 V buck, 0.8 A"),
    ("U3", "AMS1117-3.3 SOT-223", "C6186", "1", "5 V → 3.3 V"),
    ("U4", "TLIN2029DRQ1 SOIC-8", "C582774", "1", "LIN PHY, TXD not to MCU"),
    ("U5", "LM393DR SOIC-8", "C7950", "1", "OVLO comparator"),
    ("U6", "TL431 SOT-23", "C511218", "1", "2.495 V ref"),
    ("Q1", "IRLR3110TRPBF DPAK", "C152302", "1", "100 V logic-level, replaces IRL540N TO-220"),
    ("D1", "SS510 SMA", "C8678", "1", "100 V 5 A Schottky"),
    ("D2", "SMBJ58A SMB", "C13589", "1", "58 V TVS"),
    ("D3", "SS14 SOD-123", "C227409", "1", "Buck catch"),
    ("Dz", "MMSZ5226B 3.3 V", "C212815", "1", "ADC clamp"),
    ("Dusb", "1N5819 SOD-123", "C212814", "1", "USB VBUS OR"),
    ("Drail", "0805 amber LED", "C72043", "1", "Rail present"),
    ("Darm", "0805 green LED", "C72041", "1", "Output armed"),
    ("L1", "220 µH 6×6 1 A", "C167254", "1", "XL7015 inductor"),
    ("C1", "10 µF 100 V 1210", "C59419", "1", "VIN bulk"),
    ("C5v", "10 µF 16 V 0805", "C45783", "1", "5 V bulk"),
    ("C3v", "10 µF 10 V 0805", "C45783", "1", "3V3 bulk"),
    ("Clin", "220 pF 50 V 0805", "C14663", "1", "LIN to GND"),
    ("Cgate", "1 µF 25 V 0805", "C14663", "1", "Gate ramp"),
    ("Cen", "1 µF 16 V 0805", "C14663", "1", "EN RC"),
    ("R215", "215 k 1 % 0805", "C17521", "1", "OVLO top"),
    ("R10ov", "10 k 1 % 0805", "C17414", "1", "OVLO bot"),
    ("R100k", "100 k 1 % 0805", "C17407", "1", "ADC top"),
    ("R10k", "10 k 1 % 0805", "C17414", "1", "ADC bot"),
    ("R1k", "1 k 0805", "C17513", "1", "GPIO5 series"),
    ("R10g", "10 k 0805", "C17414", "1", "Gate pulldown"),
    ("R47k", "47 k 0805", "C17710", "1", "Gate ramp"),
    ("Rfb1", "8.2 k 1 % 0805", "C17671", "1", "5 V FB"),
    ("Rfb2", "1.5 k 1 % 0805", "C17622", "1", "5 V FB"),
    ("Rtx", "10 k 0805", "C17414", "1", "TXD high (listen-only)"),
    ("Ren", "10 k 0805", "C17414", "1", "EN pullup"),
    ("Rboot", "10 k 0805", "C17414", "1", "BOOT pullup"),
    ("Rr", "1 k 0805", "C17513", "1", "Amber LED"),
    ("Ra", "1 k 0805", "C17513", "1", "Green LED"),
    ("Rcc1", "5.1 k 0805", "C17610", "1", "USB CC1"),
    ("Rcc2", "5.1 k 0805", "C17610", "1", "USB CC2"),
    ("Rref", "10 k 0805", "C17414", "1", "TL431 bias"),
    ("J1", "3× Ø1.3 mm pad", "—", "1", "VIN / GND / LIN, 18 AWG"),
    ("J2", "PJ-002A 5.5×2.1", "C381065", "1", "Barrel, center +"),
    ("J3", "USB-C 16P mid-mount", "C165948", "1", "Aligns with south window"),
]


def emit_bom():
    lines = ["Designator,Comment,LCSC,Qty,Note"]
    for row in BOM:
        lines.append(",".join(row))
    (OUT / "bom-jlc.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    cpl = ["Designator,Mid X,Mid Y,Layer,Rotation"]
    for x, y, w, h, rot, label, _ in courtyards:
        ref = label.split()[0]
        cpl.append(f"{ref},{x:.3f},{y:.3f},T,{rot}")
    (OUT / "cpl-jlc.csv").write_text("\n".join(cpl) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# SVG (README)
# ---------------------------------------------------------------------------
def svg_board():
    scale = 8  # px per mm → 838 × 422
    m = 28
    W, H = BOARD_W * scale + 2 * m, BOARD_H * scale + 2 * m + 36

    def sx(x, y):
        return (m + x * scale, m + 18 + (BOARD_H - y) * scale)

    parts = [
        f'<rect width="{W}" height="{H}" fill="#0B0C0E"/>',
        f'<text x="{m}" y="22" fill="#E8A317" font-size="13" font-family="ui-monospace,monospace">PADTAP  ·  REV A  ·  DIRECT 48 V  ·  104.8 × 52.8 mm  ·  2-LAYER</text>',
    ]
    # board
    x0, y0 = sx(0, BOARD_H)
    parts.append(
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{BOARD_W * scale:.1f}" height="{BOARD_H * scale:.1f}" rx="10" fill="#141518" stroke="#2A2D32" stroke-width="1.5"/>'
    )

    # bottom pour hint
    parts.append(
        f'<rect x="{x0 + 4:.1f}" y="{y0 + 4:.1f}" width="{(BOARD_W * scale) - 8:.1f}" height="{(BOARD_H * scale) - 8:.1f}" rx="8" fill="#1A1C20"/>'
    )

    # traces
    for t in traces:
        a = sx(t.x1, t.y1)
        b = sx(t.x2, t.y2)
        col = "#C45C4A" if t.net.startswith("VIN") or t.net == "VOUT+" else (
            "#6AA6C9" if "LIN" in t.net or "USB" in t.net else "#E8A317" if t.net in ("nGATE", "GPIO5", "VSENSE") else "#8B9098"
        )
        sw = max(1.2, t.w * scale)
        parts.append(
            f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{sw:.1f}" stroke-linecap="round" opacity="0.85"/>'
        )

    # courtyards (bodies)
    for x, y, w, h, rot, label, fill in courtyards:
        px, py = sx(x, y)
        parts.append(
            f'<rect x="{px - w * scale / 2:.1f}" y="{py - h * scale / 2:.1f}" width="{w * scale:.1f}" height="{h * scale:.1f}" rx="2" fill="{fill}" stroke="#E8EAED" stroke-width="0.6" opacity="0.95"/>'
        )
        if w * scale > 28:
            parts.append(
                f'<text x="{px:.1f}" y="{py + 3:.1f}" fill="#E8EAED" font-size="8" font-family="ui-monospace,monospace" text-anchor="middle">{label[:22]}</text>'
            )

    # pads
    for p in pads:
        px, py = sx(p.x, p.y)
        if p.shape == "circ" or p.drill:
            parts.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{max(p.w, p.h) * scale / 2:.1f}" fill="#D4AF37" stroke="#8A7410" stroke-width="0.5"/>'
            )
            if p.drill:
                parts.append(
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{p.drill * scale / 2:.1f}" fill="#0B0C0E"/>'
                )
        else:
            parts.append(
                f'<rect x="{px - p.w * scale / 2:.1f}" y="{py - p.h * scale / 2:.1f}" width="{p.w * scale:.1f}" height="{p.h * scale:.1f}" rx="0.6" fill="#D4AF37"/>'
            )

    # vias
    for v in vias:
        px, py = sx(v.x, v.y)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="#8B9098"/>')
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.0" fill="#0B0C0E"/>')

    # edge labels
    def lab(x, y, s, anchor="start"):
        px, py = sx(x, y)
        parts.append(
            f'<text x="{px:.1f}" y="{py:.1f}" fill="#8B9098" font-size="9" font-family="ui-monospace,monospace" text-anchor="{anchor}">{s}</text>'
        )

    lab(2, 50.8, "WEST  J1  VIN / GND / LIN")
    lab(102, 50.8, "EAST  J2  BARREL", "end")
    lab(75, 1.8, "SOUTH  USB-C", "middle")

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="PadTap Rev A PCB">
{chr(10).join(parts)}
</svg>
'''
    (OUT / "pcb-top.svg").write_text(svg, encoding="utf-8")
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "pcb-top.svg").write_text(svg, encoding="utf-8")
    return OUT / "pcb-top.svg"


def emit_readme():
    (OUT / "README.md").write_text(
        """# PadTap Direct 48 V — Rev A PCB

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
""",
        encoding="utf-8",
    )


def main():
    place()
    route()
    z = emit_gerbers()
    emit_bom()
    svg = svg_board()
    emit_readme()
    print("board", BOARD_W, "x", BOARD_H, "mm")
    print("pads", len(pads), "traces", len(traces), "vias", len(vias))
    print("gerbers", z)
    print("svg", svg)


if __name__ == "__main__":
    main()
