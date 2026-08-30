# Research notes

Compiled 2026-08-29 for kevinchau/ct-padtap.

## Cybertruck 48 V

Tesla public DIY: [Connecting Accessories to the 48V Power Feeds](https://service.tesla.com/docs/Public/diy/cybertruck/en_us/GUID-EC88B024-50C5-4B34-B716-FDED8CF3FBE0.html)

- Only approved taps: roof 400 W, powered frunk 400 W
- Voltage: **28 V min, 44–50 V nominal, 58 V max**
- Three wires: red/blue = 48 V+, green = LIN, black/blue (roof) or brown/blue (frunk) = GND
- 48 V connectors are **blue**; 48 V wires have **blue tape** ([owner manual](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-2233D4D1-D4E5-4897-9A41-DE8593381CAA.html))
- LV is assumed **always energized**
- Enable from Controls → Outlets & Mods. Keep Outlets On for after-exit power.

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

CTOC: people have run Mini on the **roof/frunk 48 V feeds** successfully. That is still out of spec at Tesla’s 58 V peak. PadTap bucks to **36 V**.

## Wiring guide

Interactive connector/pinout/wire-color diagrams: **Service Mode Plus → Low Voltage → Wiring Service Diagram** (2025+). service.tesla.com Electrical Reference is the same data, login-walled.

## Not this project

HV “Inductive Charger” headers on the traction battery are for vehicle wireless charging (cancelled for CT). Unrelated to the phone pad.
