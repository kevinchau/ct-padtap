#!/usr/bin/env python3
"""PadTap Direct 48 V Rev A.1 — compact 58 × 34 mm 2-layer board.

Sits on the sled floor against the south wall:
  USB-C through the south window, barrel through the east hole,
  40 mm pigtail from J1 to the west comb.

48 V island is west (entry + TVS + Schottky + bulk). Switch-node is short.
Analog OVLO sits north of the buck, away from SW. FET + thermal vias hug the barrel.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

OUT = Path(__file__).parent
GERBER = OUT / "gerber"
DOCS = Path(__file__).resolve().parents[3] / "docs" / "diagrams"

BOARD_W, BOARD_H = 58.0, 34.0
EDGE = 0.25
HOLES = [(3.0, 3.0), (55.0, 3.0), (3.0, 31.0), (55.0, 31.0)]


class Pad:
    def __init__(self, ref, pin, x, y, w, h, net, plated=True, drill=0.0, shape="rect"):
        self.ref, self.pin, self.net = ref, pin, net
        self.x, self.y, self.w, self.h = x, y, w, h
        self.plated, self.drill, self.shape = plated, drill, shape


class Trace:
    def __init__(self, x1, y1, x2, y2, w, net, layer="F"):
        self.x1, self.y1, self.x2, self.y2, self.w, self.net, self.layer = x1, y1, x2, y2, w, net, layer


class Via:
    def __init__(self, x, y, net, drill=0.3, od=0.65):
        self.x, self.y, self.net, self.drill, self.od = x, y, net, drill, od


pads, traces, vias, silk, bodies = [], [], [], [], []


def P(*a, **k):
    pads.append(Pad(*a, **k))


def body(x, y, w, h, label, fill):
    bodies.append((x, y, w, h, label, fill))
    silk.append(("t", x, y - h / 2 - 1.1, label, 0.7))


def man(net, pts, w, layer="F"):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if abs(x1 - x2) < 0.02:
            traces.append(Trace(x1, y1, x1, y2, w, net, layer))
        elif abs(y1 - y2) < 0.02:
            traces.append(Trace(x1, y1, x2, y1, w, net, layer))
        else:
            traces.append(Trace(x1, y1, x2, y1, w, net, layer))
            traces.append(Trace(x2, y1, x2, y2, w, net, layer))


def r0805(ref, x, y, rot, n1, n2):
    dx, dy = (0.95, 0) if rot == 0 else (0, 0.95)
    P(ref, "1", x - dx, y - dy, 1.0, 1.25 if rot == 0 else 1.0, n1)
    P(ref, "2", x + dx, y + dy, 1.0, 1.25 if rot == 0 else 1.0, n2)
    body(x, y, 2.0, 1.3, ref, "#2A2D32")


def c0805(ref, x, y, rot, n1, n2):
    r0805(ref, x, y, rot, n1, n2)


def c1210(ref, x, y, n1, n2):
    P(ref, "1", x - 1.6, y, 1.5, 2.4, n1)
    P(ref, "2", x + 1.6, y, 1.5, 2.4, n2)
    body(x, y, 3.4, 2.6, ref, "#1C1E22")


def sod123(ref, x, y, anode, cathode):
    P(ref, "A", x - 1.65, y, 1.15, 1.05, anode)
    P(ref, "K", x + 1.65, y, 1.15, 1.05, cathode)
    body(x, y, 3.8, 1.7, ref, "#C5C8CE")


def sma(ref, x, y, a, k):
    P(ref, "A", x - 2.25, y, 1.6, 2.1, a)
    P(ref, "K", x + 2.25, y, 1.6, 2.1, k)
    body(x, y, 5.2, 2.7, ref, "#C5C8CE")


def smb(ref, x, y, n1, n2):
    P(ref, "1", x - 2.35, y, 1.9, 2.2, n1)
    P(ref, "2", x + 2.35, y, 1.9, 2.2, n2)
    body(x, y, 5.5, 3.5, ref, "#C5C8CE")


def soic8(ref, x, y, nets):
    for i in range(4):
        py = y + 1.905 - i * 1.27
        P(ref, str(i + 1), x - 2.65, py, 1.45, 0.55, nets[i])
        P(ref, str(8 - i), x + 2.65, py, 1.45, 0.55, nets[7 - i])
    body(x, y, 6.0, 5.0, ref, "#1A1C20")
    silk.append(("d", x - 2.0, y + 2.15))


def sot23(ref, x, y, n1, n2, n3):
    P(ref, "1", x - 0.95, y - 0.95, 0.75, 0.65, n1)
    P(ref, "2", x - 0.95, y + 0.95, 0.75, 0.65, n2)
    P(ref, "3", x + 0.95, y, 0.75, 0.85, n3)
    body(x, y, 2.9, 2.5, ref, "#1A1C20")


def sot223(ref, x, y):
    P(ref, "TAB", x + 1.5, y, 3.6, 3.1, "3V3")
    P(ref, "1", x - 2.7, y - 2.3, 1.1, 0.95, "GND")
    P(ref, "2", x - 2.7, y, 1.1, 0.95, "3V3")
    P(ref, "3", x - 2.7, y + 2.3, 1.1, 0.95, "5V")
    body(x, y, 7.0, 6.5, ref, "#1A1C20")


def dpak(ref, x, y):
    P(ref, "TAB", x + 2.2, y, 6.4, 6.4, "VOUT-")
    P(ref, "G", x - 4.1, y + 2.3, 1.5, 1.2, "GATE")
    P(ref, "D", x - 4.1, y, 1.5, 1.2, "VOUT-")
    P(ref, "S", x - 4.1, y - 2.3, 1.5, 1.2, "GND")
    body(x, y, 10.0, 6.7, ref, "#8B9098")
    for i in range(-1, 2):
        for j in range(-1, 2):
            vias.append(Via(x + 2.2 + i * 1.4, y + j * 1.4, "VOUT-", 0.3, 0.6))


def inductor(ref, x, y):
    P(ref, "1", x - 2.3, y, 1.9, 3.1, "SW")
    P(ref, "2", x + 2.3, y, 1.9, 3.1, "5V")
    body(x, y, 6.8, 6.5, ref, "#4A3B2A")


def tp(ref, x, y, net):
    P(ref, "1", x, y, 1.6, 1.6, net, plated=True, drill=0.7, shape="circ")
    silk.append(("t", x, y + 1.5, ref, 0.6))


def place():
    # --- J1 west, 5.08 mm, 18 AWG ---
    for name, net, y in (("VIN", "VIN_IN", 10.0), ("GND", "GND", 16.0), ("LIN", "LIN_J", 22.0)):
        P("J1", name, 3.8, y, 3.0, 2.4, net, plated=True, drill=1.3, shape="circ")
        silk.append(("t", 7.6, y + 0.25, name, 0.85))
    body(4.2, 16.0, 7.2, 16.5, "J1", "#1C1E22")

    # --- 48 V island ---
    sma("D1", 13.5, 10.0, "VIN_IN", "VIN_48")       # SS510
    smb("D2", 13.5, 16.5, "VIN_48", "GND")          # SMBJ58A at the connector
    c1210("C1", 13.5, 23.5, "VIN_48", "GND")        # 10u/100V
    c0805("Cin", 19.5, 10.0, 0, "VIN_48", "GND")    # 100n 100V

    # --- XL7015: 1 VIN, 2 SW, 3 GND, 4 FB, 5 COMP, 6 EN, 7 NC, 8 VIN ---
    soic8("U2", 27.0, 10.5, ["VIN_48", "SW", "GND", "FB", "COMP", "EN5", "NC", "VIN_48"])
    inductor("L1", 27.0, 19.5)
    sod123("D3", 20.5, 19.5, "GND", "SW")
    r0805("RfbH", 33.5, 14.5, 90, "5V", "FB")
    r0805("RfbL", 36.0, 14.5, 90, "FB", "GND")
    c0805("Ccomp", 33.5, 10.5, 0, "COMP", "GND")
    c0805("C5v", 33.5, 19.5, 0, "5V", "GND")
    c0805("C5v2", 36.0, 19.5, 0, "5V", "GND")
    r0805("Ren5", 22.0, 6.5, 0, "EN5", "VIN_48")     # EN to VIN through 100k… use 100k
    # EN5 tied to VIN_48 via Ren5 — actually 100k. Silk note.

    # --- 3V3 ---
    sot223("U3", 27.0, 28.5)
    c0805("C3v", 34.0, 28.5, 0, "3V3", "GND")
    c0805("C3v2", 36.5, 28.5, 0, "3V3", "GND")

    # --- TLIN2029 8-SOIC: 1 RXD, 2 EN, 3 NC, 4 TXD, 5 GND, 6 LIN, 7 VSUP, 8 NC ---
    soic8("U4", 44.0, 28.5, ["LIN_RX", "5V", "NC", "TXD_PU", "GND", "LIN_BUS", "5V", "NC"])
    r0805("Rtx", 50.5, 28.5, 0, "TXD_PU", "5V")       # MUST — internal PD would dominate LIN
    r0805("Rrx", 50.5, 31.5, 0, "LIN_RX", "3V3")      # RXD is open-drain
    c0805("Clin", 50.5, 25.5, 0, "LIN_BUS", "GND")    # 220 pF
    r0805("Rlin", 39.0, 22.0, 0, "LIN_J", "LIN_BUS")  # 1 k series
    # J1 LIN goes to LIN_J then Rlin to LIN_BUS — robustness
    sod123("Elin", 39.0, 25.5, "GND", "LIN_BUS")      # PESD1LIN (bidirectional treated as SOD)

    # --- OVLO, north of analog, away from SW ---
    # LM393: 1 OUT1, 2 IN1-, 3 IN1+, 4 GND, 5 IN2+, 6 IN2-, 7 OUT2, 8 VCC
    soic8("U5", 13.5, 30.0, ["nGATE", "1IN-", "VREF", "GND", "NC5", "NC6", "NC7", "5V"])
    sot23("U6", 21.0, 30.0, "GND", "VREF", "VREF")    # TL431 anode / ref=cathode
    r0805("R215", 8.5, 28.0, 90, "VIN_48", "1IN-")
    r0805("R10ov", 8.5, 24.5, 90, "1IN-", "GND")
    r0805("Rbias", 21.0, 26.5, 0, "5V", "VREF")
    r0805("Rsns", 8.5, 21.0, 90, "VIN_48", "VSENSE")  # 215 k — 100 k clips at Dz
    r0805("R10k", 8.5, 17.5, 90, "VSENSE", "GND")
    c0805("Csense", 5.5, 19.2, 0, "VSENSE", "GND")    # 1 nF
    sod123("Dz", 5.5, 26.5, "GND", "VSENSE")

    # --- Gate: OVLO OC + GPIO 1k, 10k pd, 47k+1uF ramp, 1N4148 dump ---
    r0805("R1k", 40.0, 22.0, 0, "GPIO5", "nGATE")
    r0805("R10g", 40.0, 19.0, 0, "nGATE", "GND")
    r0805("R47k", 44.5, 22.0, 0, "nGATE", "GATE")
    c0805("Cgate", 44.5, 19.0, 0, "GATE", "GND")
    sod123("Dg", 48.5, 22.0, "GATE", "nGATE")         # discharge when nGATE falls

    # --- ESP32-C3-MINI-1, antenna north, USB south ---
    u1x, u1y = 44.0, 12.2
    left = [
        (u1y + 6.0, "3V3", "3V3"),
        (u1y + 4.73, "EN", "EN"),
        (u1y + 3.46, "IO4", "VSENSE"),
        (u1y + 2.19, "IO5", "GPIO5"),
        (u1y + 0.92, "IO6", "GPIO6"),
        (u1y - 0.35, "IO7", "GPIO7"),
        (u1y - 1.62, "IO9", "BOOT"),
        (u1y - 2.89, "GNDL", "GND"),
    ]
    right = [
        (u1y + 6.0, "IO20", "LIN_RX"),
        (u1y + 4.73, "IO19", "USB_D+"),
        (u1y + 3.46, "IO18", "USB_D-"),
        (u1y + 2.19, "IO21", "IO21"),
        (u1y + 0.92, "GNDR", "GND"),
        (u1y - 0.35, "3V3B", "3V3"),
        (u1y - 1.62, "IO3", "IO3"),
        (u1y - 2.89, "GNDR2", "GND"),
    ]
    for py, name, net in left:
        P("U1", name, u1x - 5.55, py, 1.55, 0.65, net)
    for py, name, net in right:
        P("U1", name, u1x + 5.55, py, 1.55, 0.65, net)
    body(u1x, u1y, 13.2, 16.6, "U1 ESP32-C3", "#1A1C20")
    silk.append(("t", u1x, u1y + 9.4, "ANTENNA", 0.6))
    c0805("Cesp", u1x - 8.4, u1y + 6.0, 0, "3V3", "GND")
    r0805("Ren", 36.5, 5.4, 0, "EN", "3V3")
    r0805("Rboot", 51.5, 5.4, 0, "BOOT", "3V3")
    c0805("Cen", 36.5, 3.4, 0, "EN", "GND")

    # --- USB-C south, center 30 mm from west → place board so this hits the window ---
    cx = 30.0
    P("J3", "SH1", cx - 4.3, 3.2, 1.3, 2.0, "GND", plated=True, drill=0.9, shape="circ")
    P("J3", "SH2", cx + 4.3, 3.2, 1.3, 2.0, "GND", plated=True, drill=0.9, shape="circ")
    for dx, net in ((-3.2, "GND"), (-2.4, "VBUS"), (-1.6, "CC1"), (-0.8, "USB_D+"),
                    (0.0, "USB_D-"), (0.8, "USB_D-"), (1.6, "USB_D+"), (2.4, "CC2"),
                    (3.2, "VBUS")):
        P("J3", net + str(dx), cx + dx, 0.9, 0.28, 1.05, net)
    body(cx, 2.2, 9.0, 7.0, "J3 USB-C", "#C5C8CE")
    r0805("Rcc1", 24.5, 5.4, 0, "CC1", "GND")
    r0805("Rcc2", 35.5, 5.4, 0, "CC2", "GND")
    sod123("Dusb", 20.5, 5.4, "VBUS", "5V")

    # --- LEDs under lid membranes (north of ESP) ---
    P("Drail", "A", 50.5, 16.8, 0.85, 1.15, "LED_A")
    P("Drail", "K", 52.2, 16.8, 0.85, 1.15, "GND")
    body(51.35, 16.8, 2.2, 1.3, "Drail", "#E8A317")
    P("Darm", "A", 50.5, 14.4, 0.85, 1.15, "LED_B")
    P("Darm", "K", 52.2, 14.4, 0.85, 1.15, "GND")
    body(51.35, 14.4, 2.2, 1.3, "Darm", "#7DAE74")
    r0805("Rr", 54.5, 16.8, 90, "GPIO6", "LED_A")
    r0805("Ra", 54.5, 14.4, 90, "GPIO7", "LED_B")

    # --- Q1 + barrel east ---
    dpak("Q1", 50.5, 22.5)
    P("J2", "TIP", 55.4, 22.5, 3.0, 3.0, "VOUT+", plated=True, drill=1.2, shape="circ")
    P("J2", "SL1", 55.4, 27.2, 2.2, 2.2, "VOUT-", plated=True, drill=1.0, shape="circ")
    P("J2", "SL2", 55.4, 17.8, 2.2, 2.2, "VOUT-", plated=True, drill=1.0, shape="circ")
    body(54.5, 22.5, 6.5, 12.0, "J2", "#2A2D32")
    silk.append(("t", 54.5, 11.5, "J2 +", 0.8))

    for i, (hx, hy) in enumerate(HOLES, 1):
        P(f"H{i}", "1", hx, hy, 5.2, 5.2, "GND", plated=True, drill=2.7, shape="circ")

    for ref, x, y, net in (
        ("TP1", 18.5, 32.4, "VIN_48"),
        ("TP2", 32.0, 32.4, "5V"),
        ("TP3", 35.5, 32.4, "3V3"),
        ("TP4", 47.5, 32.4, "LIN_BUS"),
        ("TP5", 22.5, 32.4, "GND"),
    ):
        tp(ref, x, y, net)

    # GND stitching every ~7 mm, skip 48 V island internals
    for x in range(6, 56, 7):
        for y in range(6, 32, 7):
            if 10 < x < 18 and 8 < y < 26:
                continue
            vias.append(Via(x, y, "GND"))
    vias.append(Via(44.0, 18.5, "LIN_RX"))
    vias.append(Via(41.5, 22.0, "nGATE"))
    vias.append(Via(47.0, 22.5, "GATE"))
    vias.append(Via(53.5, 22.5, "VOUT+"))


def pad(ref, pin):
    for p in pads:
        if p.ref == ref and p.pin == pin:
            return (p.x, p.y)
    raise KeyError(ref, pin)


def route():
    WP, W, WS = 1.6, 0.4, 0.25

    man("VIN_IN", [pad("J1", "VIN"), pad("D1", "A")], WP)
    man("VIN_48", [pad("D1", "K"), pad("D2", "1")], WP)
    man("VIN_48", [pad("D1", "K"), (18.5, 10.0), (18.5, 10.5), pad("U2", "1")], WP)
    man("VIN_48", [pad("D2", "1"), pad("C1", "1")], WP)
    # 48 V to barrel tip along the north rail, 1.6 mm, away from SW
    man("VOUT+", [pad("D1", "K"), (18.5, 7.2), (53.5, 7.2), (53.5, 22.5), pad("J2", "TIP")], WP)

    man("SW", [pad("U2", "2"), (24.35, 10.5), (24.35, 19.5), pad("L1", "1")], W)
    man("5V", [pad("L1", "2"), pad("C5v", "1")], W)
    man("5V", [pad("C5v", "1"), (33.5, 28.5), pad("U3", "3")], W)
    man("5V", [(41.35, 28.5), pad("U4", "7")], W)
    man("3V3", [pad("U3", "TAB"), (38.45, 28.5), (38.45, 18.2), pad("U1", "3V3")], W)

    man("LIN_J", [pad("J1", "LIN"), (7.5, 22.0), pad("Rlin", "1")], WS)
    man("LIN_BUS", [pad("Rlin", "2"), (41.35, 22.0), (41.35, 28.5), pad("U4", "6")], WS)
    man("LIN_RX", [pad("U4", "1"), (41.35, 30.4), (49.55, 30.4), (49.55, 18.2), pad("U1", "IO20")], WS)

    man("GPIO5", [pad("U1", "IO5"), (38.45, 14.39), (38.45, 22.0), pad("R1k", "1")], WS)
    man("nGATE", [pad("R1k", "2"), pad("R47k", "1")], WS)
    man("nGATE", [pad("U5", "1"), (16.15, 30.0), (16.15, 22.0), pad("R1k", "2")], WS)
    man("GATE", [pad("R47k", "2"), (46.4, 22.5), pad("Q1", "G")], WS)
    man("VOUT-", [pad("Q1", "TAB"), pad("J2", "SL1")], WP)

    man("VSENSE", [pad("Rsns", "2"), (8.5, 15.66), (38.45, 15.66), pad("U1", "IO4")], WS)
    man("VREF", [pad("U6", "3"), pad("U5", "3")], WS)
    man("1IN-", [pad("R215", "2"), pad("U5", "2")], WS)

    man("USB_D+", [pad("U1", "IO19"), (49.55, 16.93), (49.55, 4.0), (29.2, 4.0)], WS)
    man("USB_D-", [pad("U1", "IO18"), (49.55, 15.66), (52.0, 15.66), (52.0, 3.5), (30.0, 3.5)], WS)
    man("VBUS", [(32.4, 0.9), (32.4, 5.4), pad("Dusb", "A")], W)
    man("EN", [pad("U1", "EN"), pad("Ren", "1")], WS)
    man("BOOT", [pad("U1", "IO9"), pad("Rboot", "1")], WS)
    man("GPIO6", [pad("U1", "IO6"), (38.45, 13.12), pad("Rr", "1")], WS)
    man("LED_A", [pad("Rr", "2"), pad("Drail", "A")], WS)
    man("GPIO7", [pad("U1", "IO7"), (38.45, 11.85), pad("Ra", "1")], WS)
    man("LED_B", [pad("Ra", "2"), pad("Darm", "A")], WS)
    man("GND", [pad("J1", "GND"), (6.0, 16.0)], WP)
    man("EN5", [pad("U2", "6"), pad("Ren5", "1")], WS)
    man("TXD_PU", [pad("U4", "4"), pad("Rtx", "1")], WS)
    man("FB", [pad("U2", "4"), pad("RfbL", "1")], WS)


# ----- Gerber / BOM / SVG (same machinery, new size) -----
def gxy(x, y):
    return f"X{int(round(x * 1_000_000))}Y{int(round(y * 1_000_000))}"


class Gbr:
    def __init__(self):
        self.ap, self.n, self.body = {}, 10, []

    def sel(self, key):
        if key not in self.ap:
            self.ap[key] = self.n
            self.n += 1
        self.body.append(f"D{self.ap[key]}*")

    def dumps(self, name):
        lines = ["%FSLAX36Y36*%", "%MOMM*%", f"G04 {name}*", "%LPD*%"]
        for key, d in sorted(self.ap.items(), key=lambda kv: kv[1]):
            if key[0] == "C":
                lines.append(f"%ADD{d}C,{key[1:]}*%")
            else:
                w, h = key[1:].split("x")
                lines.append(f"%ADD{d}R,{w}X{h}*%")
        lines += self.body + ["M02*"]
        return "\n".join(lines) + "\n"


def flash(g, p, grow=0.0):
    if p.shape == "circ" or p.drill:
        g.sel(f"C{p.w + grow:.3f}")
    else:
        g.sel(f"R{p.w + grow:.3f}x{p.h + grow:.3f}")
    g.body.append(gxy(p.x, p.y) + "D03*")


def emit_gerbers():
    GERBER.mkdir(parents=True, exist_ok=True)
    L = {k: Gbr() for k in ("GTL", "GBL", "GTS", "GBS", "GTO", "GBO", "GKO", "GTP")}
    ko = L["GKO"]
    ko.sel("C0.120")
    ko.body += ["G01*", gxy(0, 0) + "D02*", gxy(BOARD_W, 0) + "D01*",
                gxy(BOARD_W, BOARD_H) + "D01*", gxy(0, BOARD_H) + "D01*", gxy(0, 0) + "D01*"]
    gbl = L["GBL"]
    gbl.body += ["G36*", gxy(EDGE, EDGE) + "D02*", gxy(BOARD_W - EDGE, EDGE) + "D01*",
                 gxy(BOARD_W - EDGE, BOARD_H - EDGE) + "D01*", gxy(EDGE, BOARD_H - EDGE) + "D01*",
                 gxy(EDGE, EDGE) + "D01*", "G37*"]
    for p in pads:
        flash(L["GTL"], p)
        flash(L["GTS"], p, 0.1)
        if p.drill == 0:
            flash(L["GTP"], p, -0.05)
        if p.drill:
            flash(L["GBL"], p)
            flash(L["GBS"], p, 0.1)
    for t in traces:
        g = L["GTL"] if t.layer == "F" else L["GBL"]
        g.sel(f"C{t.w:.3f}")
        g.body += ["G01*", gxy(t.x1, t.y1) + "D02*", gxy(t.x2, t.y2) + "D01*"]
    for v in vias:
        for layer, grow in (("GTL", 0), ("GBL", 0), ("GTS", 0.08), ("GBS", 0.08)):
            L[layer].sel(f"C{v.od + grow:.3f}")
            L[layer].body.append(gxy(v.x, v.y) + "D03*")
    L["GTO"].sel("C0.200")
    for s in silk:
        if s[0] == "t":
            L["GTO"].body.append(gxy(s[1], s[2]) + "D03*")
        elif s[0] == "d":
            L["GTO"].sel("C0.400")
            L["GTO"].body.append(gxy(s[1], s[2]) + "D03*")
            L["GTO"].sel("C0.200")
    names = {k: f"PadTap-RevA.{k}" for k in L}
    for k, g in L.items():
        (GERBER / names[k]).write_text(g.dumps(k), encoding="utf-8")

    def drill(rows, path, plated):
        tools, lines = {}, ["M48", f";{'PTH' if plated else 'NPTH'}", "METRIC,TZ"]
        for d, x, y in rows:
            key = f"{d:.3f}"
            if key not in tools:
                tools[key] = f"T{len(tools)+1:02d}"
                lines.append(f"{tools[key]}C{d:.3f}")
        lines.append("%")
        cur = None
        for d, x, y in rows:
            t = tools[f"{d:.3f}"]
            if t != cur:
                lines.append(t)
                cur = t
            lines.append(f"X{x:.3f}Y{y:.3f}")
        lines.append("M30")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    pth, npth = [], []
    for p in pads:
        if p.drill:
            (npth if p.ref.startswith("H") else pth).append((p.drill, p.x, p.y))
    for v in vias:
        pth.append((v.drill, v.x, v.y))
    drill(pth, GERBER / "PadTap-RevA-PTH.DRL", True)
    drill(npth, GERBER / "PadTap-RevA-NPTH.DRL", False)
    z = OUT / "PadTap-RevA-gerbers.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zh:
        for f in sorted(GERBER.iterdir()):
            zh.write(f, f.name)
    return z


BOM = [
    ("U1", "ESP32-C3-MINI-1-N4", "C2919203", "1", "MCU, antenna north"),
    ("U2", "XL7015E1 SOP-8", "C142613", "1", "5–80 V → 5 V. Pins 1 VIN, 2 SW, 3 GND, 4 FB, 5 COMP, 6 EN, 8 VIN"),
    ("U3", "AMS1117-3.3 SOT-223", "C6186", "1", "5 V → 3.3 V"),
    ("U4", "TLIN2029DRQ1 SOIC-8", "C582774", "1", "1 RXD, 2 EN, 4 TXD, 5 GND, 6 LIN, 7 VSUP"),
    ("U5", "LM393DR SOIC-8", "C7950", "1", "OVLO, OC on nGATE"),
    ("U6", "TL431 SOT-23", "C511218", "1", "2.495 V"),
    ("Q1", "IRLR3110TRPBF DPAK", "C152302", "1", "100 V logic-level, 9 thermal vias on tab"),
    ("D1", "SS510 SMA", "C8678", "1", "Reverse, 100 V"),
    ("D2", "SMBJ58A SMB", "C13589", "1", "TVS at J1, not at the barrel"),
    ("D3", "SS14 SOD-123", "C227409", "1", "Buck catch, short SW node"),
    ("Dz", "MMSZ5226B", "C212815", "1", "ADC 3.3 V clamp"),
    ("Dg", "1N4148W", "C212147", "1", "Fast gate dump"),
    ("Dusb", "1N5819WS", "C212814", "1", "USB OR into 5 V"),
    ("Elin", "PESD1LIN", "C841366", "1", "LIN ESD"),
    ("Drail", "0805 amber", "C72043", "1", "Rail"),
    ("Darm", "0805 green", "C72041", "1", "Armed"),
    ("L1", "220 µH 6×6 ≥1 A", "C167254", "1", "Next to U2 SW"),
    ("C1", "10 µF 100 V 1210", "C59419", "1", "VIN bulk at TVS"),
    ("Cin", "100 nF 100 V 0805", "C1463", "1", "VIN HF"),
    ("C5v", "10 µF 16 V 0805", "C45783", "2", "5 V"),
    ("C3v", "10 µF 10 V 0805", "C45783", "2", "3V3 + ESP"),
    ("Clin", "220 pF 50 V", "C14663", "1", "ISO 17987"),
    ("Cgate", "1 µF 25 V", "C14663", "1", "80 ms-class ramp with 47 k"),
    ("Ccomp", "10 nF 50 V", "C14663", "1", "XL7015 COMP"),
    ("Csense", "1 nF 50 V", "C14663", "1", "ADC filter"),
    ("Cen", "1 µF 16 V", "C14663", "1", "EN RC"),
    ("Cesp", "100 nF 16 V", "C14663", "1", "ESP 3V3"),
    ("R215", "215 k 1 %", "C17521", "1", "OVLO top"),
    ("R10ov", "10 k 1 %", "C17414", "1", "OVLO bot → 56.14 V"),
    ("Rsns", "215 k 1 %", "C17521", "1", "ADC sense — 56 V → 2.49 V (100 k clips at Dz)"),
    ("R10k", "10 k 1 %", "C17414", "1", "ADC"),
    ("RfbH", "7.50 k 1 %", "C17664", "1", "5.02 V with 2.49 k"),
    ("RfbL", "2.49 k 1 %", "C17636", "1", "FB"),
    ("R1k", "1 k", "C17513", "1", "GPIO5 series"),
    ("R10g", "10 k", "C17414", "1", "nGATE pd"),
    ("R47k", "47 k", "C17710", "1", "Gate ramp"),
    ("Rtx", "10 k", "C17414", "1", "TXD high — do not omit"),
    ("Rrx", "4.7 k", "C17604", "1", "RXD pull-up (open-drain)"),
    ("Rlin", "1 k", "C17513", "1", "LIN series"),
    ("Ren", "10 k", "C17414", "1", "EN"),
    ("Rboot", "10 k", "C17414", "1", "BOOT"),
    ("Ren5", "100 k", "C17407", "1", "XL7015 EN to VIN"),
    ("Rbias", "10 k", "C17414", "1", "TL431"),
    ("Rcc1", "5.1 k", "C17610", "2", "USB CC"),
    ("Rr", "1 k", "C17513", "1", "Amber"),
    ("Ra", "1 k", "C17513", "1", "Green"),
    ("J1", "3× Ø1.3 mm", "—", "1", "VIN GND LIN, 18 AWG, pigtail to comb"),
    ("J2", "PJ-002A 5.5×2.1", "C381065", "1", "East, center +"),
    ("J3", "USB-C 16P mid-mount", "C165948", "1", "South window"),
]


def emit_bom():
    (OUT / "bom-jlc.csv").write_text(
        "Designator,Comment,LCSC,Qty,Note\n" + "\n".join(",".join(r) for r in BOM) + "\n",
        encoding="utf-8",
    )
    lines = ["Designator,Mid X,Mid Y,Layer,Rotation"]
    for x, y, w, h, label, _ in bodies:
        lines.append(f"{label.split()[0]},{x:.3f},{y:.3f},T,0")
    (OUT / "cpl-jlc.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def svg_board():
    sc, m = 12, 36
    W, H = BOARD_W * sc + 2 * m, BOARD_H * sc + 2 * m + 40

    def S(x, y):
        return (m + x * sc, m + 24 + (BOARD_H - y) * sc)

    out = [
        f'<rect width="{W}" height="{H}" fill="#0B0C0E"/>',
        f'<text x="{m}" y="22" fill="#E8A317" font-size="14" font-family="ui-monospace,monospace">PADTAP REV A.1  ·  58 × 34 mm  ·  2-LAYER  ·  48 V ISLAND WEST, SWITCH EAST</text>',
    ]
    x0, y0 = S(0, BOARD_H)
    out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{BOARD_W*sc:.1f}" height="{BOARD_H*sc:.1f}" rx="8" fill="#121318" stroke="#3A3D42" stroke-width="1.6"/>')
    # zone tints
    def zone(x, y, w, h, fill, label):
        a = S(x, y + h)
        out.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{w*sc:.1f}" height="{h*sc:.1f}" fill="{fill}" opacity="0.22" rx="4"/>')
        out.append(f'<text x="{a[0]+6:.1f}" y="{a[1]+14:.1f}" fill="#E8EAED" font-size="9" font-family="ui-monospace,monospace" opacity="0.7">{label}</text>')

    zone(0.8, 6.5, 19, 20, "#C45C4A", "48 V")
    zone(20.5, 6.5, 16, 16, "#E8A317", "BUCK")
    zone(6.5, 24.5, 18, 8.5, "#7DAE74", "OVLO")
    zone(37.5, 24, 16, 9, "#6AA6C9", "LIN")
    zone(37, 4, 16, 18, "#8B9098", "MCU")
    zone(46, 17, 11.5, 14, "#C45C4A", "SW")

    col = {
        "VIN_IN": "#C45C4A", "VIN_48": "#C45C4A", "VOUT+": "#C45C4A",
        "SW": "#E8A317", "5V": "#E8A317", "3V3": "#7DAE74",
        "LIN_BUS": "#6AA6C9", "LIN_RX": "#6AA6C9", "LIN_J": "#6AA6C9",
        "nGATE": "#E8A317", "GATE": "#E8A317", "GPIO5": "#E8A317",
        "USB_D+": "#6AA6C9", "USB_D-": "#6AA6C9", "VBUS": "#7DAE74",
    }
    for t in traces:
        a, b = S(t.x1, t.y1), S(t.x2, t.y2)
        out.append(
            f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            f'stroke="{col.get(t.net, "#5C6068")}" stroke-width="{max(1.4, t.w*sc):.1f}" '
            f'stroke-linecap="round" opacity="0.9"/>'
        )
    for x, y, w, h, label, fill in bodies:
        px, py = S(x, y)
        out.append(
            f'<rect x="{px-w*sc/2:.1f}" y="{py-h*sc/2:.1f}" width="{w*sc:.1f}" height="{h*sc:.1f}" '
            f'rx="2" fill="{fill}" stroke="#E8EAED" stroke-width="0.7"/>'
        )
        if w * sc > 36:
            out.append(
                f'<text x="{px:.1f}" y="{py+3:.1f}" fill="#E8EAED" font-size="8" '
                f'font-family="ui-monospace,monospace" text-anchor="middle">{label[:18]}</text>'
            )
    for p in pads:
        px, py = S(p.x, p.y)
        if p.shape == "circ" or p.drill:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{max(p.w,p.h)*sc/2:.1f}" fill="#D4AF37"/>')
            if p.drill:
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{p.drill*sc/2:.1f}" fill="#0B0C0E"/>')
        else:
            out.append(
                f'<rect x="{px-p.w*sc/2:.1f}" y="{py-p.h*sc/2:.1f}" width="{p.w*sc:.1f}" '
                f'height="{p.h*sc:.1f}" rx="0.5" fill="#D4AF37"/>'
            )
    for v in vias:
        px, py = S(v.x, v.y)
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="#7A7E86"/>')
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.0" fill="#0B0C0E"/>')

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="PadTap Rev A.1 PCB">
{chr(10).join(out)}
</svg>
'''
    (OUT / "pcb-top.svg").write_text(svg, encoding="utf-8")
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "pcb-top.svg").write_text(svg, encoding="utf-8")


def emit_readme():
    (OUT / "README.md").write_text(
        f"""# PadTap Direct 48 V — Rev A.1

**{BOARD_W:.0f} × {BOARD_H:.0f} mm**, 2-layer, 1.6 mm FR4. ~45 % of the sled cavity. Sits on the floor against the south wall.

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
""",
        encoding="utf-8",
    )


def main():
    place()
    route()
    z = emit_gerbers()
    emit_bom()
    svg_board()
    emit_readme()
    print(f"{BOARD_W} x {BOARD_H} mm  pads={len(pads)} traces={len(traces)} vias={len(vias)}")
    print(z)


if __name__ == "__main__":
    main()
