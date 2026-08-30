# Research notes

Compiled 2026-08-29 for kevinchau/ct-padtap. Direct-48 V path added 2026-08-29.

## Cybertruck 48 V

Tesla public DIY: [Connecting Accessories to the 48V Power Feeds](https://service.tesla.com/docs/Public/diy/cybertruck/en_us/GUID-EC88B024-50C5-4B34-B716-FDED8CF3FBE0.html)

- Only approved taps: roof 400 W, powered frunk 400 W
- Voltage: **28 V min, 44–50 V nominal, 58 V max**
- Three wires: red/blue = 48 V+, green = LIN, black/blue (roof) or brown/blue (frunk) = GND
- 48 V connectors are **blue**; 48 V wires have **blue tape** ([owner manual](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-2233D4D1-D4E5-4897-9A41-DE8593381CAA.html))
- LV is assumed **always energized**
- Enable from Controls → Outlets & Mods. Keep Outlets On for after-exit power.

Real-world bus sits in the nominal band. 58 V is the design maximum of the HV→LV converter, not the everyday voltage. Direct 48 V still treats 58 V as a disconnect, not an operating point.

Tesla: the 400 W feeds “stop providing power when current that exceeds the listed specifications is detected” and reset from Controls → Outlets & Mods → Reset. Those are **solid-state / digital fuses**, not slow blade fuses. The wireless-pad circuit is a smaller body-controller channel with the same kind of protection.

### Inrush / NTC

A buck converter’s input capacitors look like a short for microseconds. On Cybertruck 48 V that spike trips the digital fuse even when steady-state watts are fine — this is the known failure of a raw 48 V → 12 V module on the frunk tap. The fix that works in the truck is an **NTC inrush current limiter** in series with VIN (10 Ω cold, ≥3 A, e.g. EPCOS B57237S0100M000 / MF72-10D13). After it warms it drops to a few tenths of an ohm.

PadTap:

- **NTC on VIN**, after F1, on the harness next to the fuse holders (the disc does not fit the 12.1 mm sled). Covers the 5 V MCU buck and the optional 36 V buck.
- **80 ms FET ramp** (firmware PWM + 47 k / 1 µF on the gate) so Starlink Mini’s own input caps don’t dump the same spike when the pad toggle arms the output. An NTC on VIN is already warm by then (ESP32 is up) so it cannot save the Mini turn-on — the ramp has to.

Do not substitute a signal thermistor (10 k NTC). It has to be a power ICL.

## Wireless charger

Tesla Electrical Reference, **Console – Phone and USB Charging**, sheet 46, prog-242 rev 1.11:

https://service.tesla.com/docs/Cybertruck/ElectricalReference/prog-242/interactive/pdf/console_phone_and_usb_charging_print.pdf

Module: **Wireless Phone Charger + NFC Reader**, connector **C X0648**. Tesla housing PN **1042593-03-A**.

Plastics (confirmed against the X0648 connector page and the user’s identification):

- Vehicle plug: Sumitomo **6098-5718** grey 12-way female, TS/DL 1.5 mm unsealed
- Charger: Sumitomo **6098-6210** 12-way male DL PCB header (wire-to-board)
- Female terminals: **8240-0213** (0.75–1.25 mm²) on 1/3/9, **8240-0215** (0.3–0.5 mm²) on 4/10/11/12
- Cavity table: 1 RD/BU 1.00, 3 WH/BU 1.00, 4 GN 0.35, 9 BN/BU 1.00, 10 GY 0.35, 11 PK/WH 0.35, 12 BU/WH 0.35. Unused: 2, 5, 6, 7, 8

48 V is a **Right Controller high-side drive** X0034-91, net `WIRELESS_PHONE_CHARGER_AND_VCUSB` (RD/BU 1.00 mm² into pin 1). Shared with the USB hub — the pad toggle is not going to drop this rail. LIN in on pin 4 (GN), LIN out on pin 10 (GY, `LIN_INDUCTIVE_CHARGER`) to the HVAC switchpack / touchpad. CAN auth on 11/12 to the Left Controller.

Do not put Tesla’s PDF in a public fork. Transcribe pin facts; do not republish the sheet.

Tesla R&R: [Wireless Charger - Center Console](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8B81665F-D4DC-4DED-B787-45A957056FF9.html) — one electrical connector, harness clip, T20 ×4 at 5 N·m.

- Tesla PN **1877045-00-A / 00-C** Gen 5.0, dual 15 W Qi, center console
- R&R: [GUID-8B81665F-D4DC-4DED-B787-45A957056FF9](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8B81665F-D4DC-4DED-B787-45A957056FF9.html) — connector + clip, T20 ×4, 5 N·m
- Same location as **key-card NFC**. Unplug → Service Mode error, NFC dead, sometimes ambient light dead ([CTOC](https://www.cybertruckownersclub.com/forum/threads/disable-wireless-charging-pad.15032/page-2), Facebook: “the plug has 4 pins”)
- Pads feel warm even empty (always drawing)
- Software disable (Holiday 2025): Controls → Outlets & Mods → Wireless Phone Charging Pads ([owner manual](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-7B00E438-94C4-4B66-BBEB-0C39C70777DC.html))

## LIN

Model Y WPC teardown uses **NXP TJA1021** LIN PHY ([ChargerLAB](https://www.chargerlab.com/teardown-of-tesla-model-y-15w-wireless-charging-module-2)). Cybertruck 48 V accessories (factory lightbar) are 48 V + LIN; community intercepts use ESP32 + LIN transceiver with TX careful / listen. LIN recessive is ~12 V even on a 48 V vehicle.

Working assumption: screen toggle is a **LIN command**, not a 48 V cut — otherwise NFC dies. Firmware auto-detects the other case.

## Starlink Mini

[Spec sheet](https://starlink.com/public-files/specification_sheet_mini.pdf): **12–48 V DC, 60 W**, 25–40 W average. USB-C PD path is 100 W / 20 V / 5 A with Starlink’s cable.

Barrel: 5.5 mm OD. Spec drawing shows 2.5 mm pin; field reports 2.1 mm plugs working. **Confirm polarity on the official PSU** (center + expected).

### Hardware above 48 V

Printed rating is 48 V. Teardown of the Mini input ([DIY Solar #86410](https://diysolarforum.com/threads/starlink-mini-dc-power-consumption.86410/), PCB photo [Oleg Kutkov](https://x.com/olegkutkov/status/1817940568304971945)):

- Input DC-DC FETs: Infineon **BSZ146N10LS5**, 100 V
- TVS across the barrel: **60 V** class, clamps ~66–73 V
- Reverse-protect back-to-back MOSFETs on the input
- Controller IC unpublished; 48 V-class parts imply ~60 V abs max

That is why Direct 48 V is viable on a Cybertruck: nominal 44–50 V is inside both the printed spec and the silicon. The only conflict is Tesla’s **58 V** design max vs Mini’s **~56 V** comfortable hardware ceiling. PadTap Direct **opens the FET at 56.0 V** (LM393 + firmware latch, clears at 54.0 V). We do not ride the Mini’s TVS.

CTOC: people have run Mini on the **roof/frunk 48 V feeds** successfully at nominal voltage. Direct on the pad tap is the same rail, plus a disconnect for the 58 V tail.

The 36 V buck path is **deprecated** and does not fit the 15 mm sled.

## Wiring guide

Interactive connector/pinout/wire-color diagrams: **Service Mode Plus → Low Voltage → Wiring Service Diagram** (2025+). service.tesla.com Electrical Reference is the same data, login-walled.

## Not this project

HV “Inductive Charger” headers on the traction battery are for vehicle wireless charging (cancelled for CT). Unrelated to the phone pad.
