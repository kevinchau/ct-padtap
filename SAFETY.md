# Safety

Cybertruck low voltage is **48 V** and Tesla says to assume every LV wire and connector is **always energized**, even when the truck is “off.”

- Eye protection. No jewelry. Insulated probes.
- 48 V arcs. A short across a blue connector can weld a probe tip and pop a body-controller fuse. Some of those fuses feed more than a phone pad.
- Do **not** unplug the wireless charger as a “test.” It is the key-card NFC reader.
- Do **not** inject power into Tesla (no backfeed from a bench supply into VIN_48).
- Do **not** drive LIN TX until you have captured the bus and know you are not colliding with the commander.
- Fuse the tap at **3 A**. If Tesla’s upstream fuse is smaller than Starlink + pad, stop and use the 400 W roof/frunk feed instead.
- Tesla max is **58 V**. Mini printed max is **48 V**; Mini hardware is ~**56 V**. Direct 48 V **must** include the 56.0 V OVLO (LM393 + firmware). Never defeat it. Never clamp the Tesla rail with a 54 V TVS.
- Buck 36 V is the conservative path if you want the Mini inside its printed rating at Tesla’s 58 V peak.
- First power-up of the Mini happens **after** NFC and Qi are confirmed still working.
- This is not a Tesla-approved accessory point. Warranty, fire, and brick risk are yours.

Tesla-approved alternative: [Connecting Accessories to the 48V Power Feeds](https://service.tesla.com/docs/Public/diy/cybertruck/en_us/GUID-EC88B024-50C5-4B34-B716-FDED8CF3FBE0.html) — roof and frunk, 400 W each.
