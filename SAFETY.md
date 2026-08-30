# Safety

Cybertruck low voltage is **48 V** and Tesla says to assume every LV wire and connector is **always energized**, even when the truck is “off.”

- Eye protection. No jewelry. Insulated probes.
- 48 V arcs. A short across a blue connector can weld a probe tip and pop a body-controller fuse. Some of those fuses feed more than a phone pad.
- Do **not** unplug the wireless charger as a “test.” It is the key-card NFC reader.
- Do **not** inject power into Tesla (no backfeed from a bench supply into VIN_48).
- Do **not** drive LIN TX until you have captured the bus and know you are not colliding with the commander.
- Fuse the tap at **3 A**. If Tesla’s upstream fuse is smaller than Starlink + pad, stop and use the 400 W roof/frunk feed instead.
- Starlink Mini max input is **48 V**. Tesla max is **58 V**. Always buck (PadTap = 36 V).
- First power-up of the Mini happens **after** NFC and Qi are confirmed still working.
- This is not a Tesla-approved accessory point. Warranty, fire, and brick risk are yours.

Tesla-approved alternative: [Connecting Accessories to the 48V Power Feeds](https://service.tesla.com/docs/Public/diy/cybertruck/en_us/GUID-EC88B024-50C5-4B34-B716-FDED8CF3FBE0.html) — roof and frunk, 400 W each.
