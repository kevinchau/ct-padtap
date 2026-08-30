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

## Wireless charger

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

Buck 36 V remains the conservative build if you want the Mini to stay inside the printed 12–48 V rating even during a 58 V excursion.

## Wiring guide

Interactive connector/pinout/wire-color diagrams: **Service Mode Plus → Low Voltage → Wiring Service Diagram** (2025+). service.tesla.com Electrical Reference is the same data, login-walled.

## Not this project

HV “Inductive Charger” headers on the traction battery are for vehicle wireless charging (cancelled for CT). Unrelated to the phone pad.
