# Supply and tool list

US vendors. Prices as of 2026-08-29, they move. Direct 48 V build.

Do **not** buy 32 V mini fuses. Tesla LV is 48 V, allowed to 58 V.

## Connectors

| Item | PN | Qty | Buy | ~$ |
| --- | --- | --- | --- | --- |
| 12-way female, grey | 6098-5718 | 1 (buy 2) | [Nexelec](https://nexelec.com/products/sumitomo-60985718) · [eBay 4-pack](https://www.ebay.com/itm/374601171115) · [AliExpress 10](https://www.aliexpress.com/item/1005008563988761.html) | 4–12 |
| 12-way male PCB header | 6098-6210 | 2 | [Octopart](https://octopart.com/search?q=6098-6210) · [Eleocean](http://www.eleocean.com/productshow.php?cid=25&id=13164) | 3–8 |
| Female terminal 0.75–1.25 mm² | 8240-0213 | 10 | [Connector ID (singles)](https://www.connectorid.com/products/sumitomo-8240-0213) · [Nexelec MOQ 200](https://nexelec.com/products/sumitomo-82400213) · [Auto-Click](https://www.auto-click.co.uk/8240-0213) | 0.62 ea |
| Female terminal 0.3–0.5 mm² | 8240-0215 | 10 | [Nexelec](https://nexelec.com/products/sumitomo-82400215) | 0.49 ea |

5718 plugs into the charger. 6210 is a through-hole header — solder a pigtail, pot it, vehicle 5718 plugs onto that. Confirm TPA in the 5718 bag.

## Wire and insulation

| Item | PN | Qty | Buy | ~$ |
| --- | --- | --- | --- | --- |
| 18 AWG GXL red | WL18-2 | 10 ft | [Waytek](https://www.waytekwire.com/search?query=WL18-2) | 0.25/ft |
| 18 AWG GXL black | WL18-0 | 10 ft | [Waytek](https://www.waytekwire.com/search?query=WL18-0) | 0.25/ft |
| 22 AWG GXL green | GXL-22 | 5 ft | [Waytek GXL catalog](https://www.waytekwire.com/catalog/wire-and-cable/automotive-cross-link-wire) | 0.20/ft |
| Adhesive-lined 3:1 shrink kit | 3:1 dual-wall | 1 | [Amazon](https://www.amazon.com/s?k=adhesive+lined+heat+shrink+3%3A1+kit) | 15 |
| PET cloth harness tape | tesa 51036 19 mm | 1 | [Amazon](https://www.amazon.com/dp/B0DF8NPC66) | 12 |

Do not crimp 16 AWG into 8240-0213 (max 1.25 mm²).

## Fuses — 58 V

| Item | PN | Qty | Buy | ~$ |
| --- | --- | --- | --- | --- |
| MINI 3 A 58 V | 0997003.WXN | 5 | [Digi-Key](https://www.digikey.com/en/products/detail/littelfuse-inc/0997003-WXN/701055) | 1 ea |
| MINI in-line holder 16 ga | LPM-04B class | 2 | [Waytek](https://www.waytekwire.com/product/optifuse-lpm-04b-1-16r-mini-in-line-fuse-holder) | 4 ea |

A 32 V mini (the violet 3 A at AutoZone) is the wrong part.

## Board

| Item | PN | Qty | Buy | ~$ |
| --- | --- | --- | --- | --- |
| ESP32-C3 SuperMini 3-pack | ESP32-C3-FH4 | 1 pack | [Amazon](https://www.amazon.com/dp/B0F12JS872) | 13 |
| LIN transceiver | TLIN2029DRQ1 | 2 | [Digi-Key](https://www.digikey.com/en/products/detail/texas-instruments/TLIN2029DRQ1/8322880) · [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/TLIN2029DRQ1) | 2 |
| 5–80 V → 5 V buck | XL7015 | 2 | [Amazon](https://www.amazon.com/dp/B0FCXYMQ1S) | 8 |
| NTC 10 Ω 3.7 A | B57237S0100M000 | 2 | [Digi-Key](https://www.digikey.com/en/products/detail/tdk-epcos/B57237S0100M000/652130) | 1.44 |
| TVS 58 V | SMBJ58A | 5 | [Digi-Key](https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ58A/276411) | 0.50 |
| Schottky 100 V 5 A | SS510 / SS5P10 | 5 | [Digi-Key search](https://www.digikey.com/en/products/filter/diodes-rectifiers-single?keywords=SS510) | 0.60 |
| Starlink Mini DC cable 5.5×2.1 | DC5521 | 1 | [Amazon](https://www.amazon.com/dp/B0DLL79FJY) | 14 |
| 1N4148 (gate diode) | 1N4148TR | 10 | [Digi-Key](https://www.digikey.com/en/products/detail/onsemi/1N4148TR/458966) | 0.10 |
| 3.3 V zener | MMSZ5226BT1G | 5 | [Digi-Key](https://www.digikey.com/en/products/detail/on-semiconductor/MMSZ5226BT1G/919344) | 0.20 |
| N-FET 100 V logic TO-220 | IRL540NPBF | 2 | [Digi-Key](https://www.digikey.com/en/products/detail/infineon-technologies/IRL540NPBF/812000) | 2.47 |
| Dual comparator | LM393P | 2 | [Digi-Key](https://www.digikey.com/en/products/detail/texas-instruments/LM393P/277092) | 0.50 |
| 2.495 V ref | TL431CP | 2 | [Digi-Key](https://www.digikey.com/en/products/detail/texas-instruments/TL431CP/276496) | 0.50 |
| 215 k 1% 0805 | — | 10 | [Digi-Key](https://www.digikey.com/en/products/filter/chip-resistor-surface-mount?keywords=215k%200805%201%25) | 1 |

FQP13N10L is obsolete. IRL540NPBF is the 100 V logic-level stand-in. Lay the TO-220 flat.

## Case

| Item | PN | Qty | Buy | ~$ |
| --- | --- | --- | --- | --- |
| PETG black 1.75 mm | — | 1 kg (~20 g used) | [Amazon](https://www.amazon.com/s?k=PETG+filament+black+1.75mm) | 20 |
| M2.5 heat-set + 8 mm screws | M2.5 | 1 kit | [Amazon](https://www.amazon.com/s?k=M2.5+heat+set+inserts+kit) | 10 |
| 3M VHB 5952 1/2 in | 5952 | 1 roll | [Amazon](https://www.amazon.com/s?k=3M+VHB+5952+1%2F2+inch) | 18 |

## Tools

| Item | PN | Buy | ~$ |
| --- | --- | --- | --- |
| Open-barrel crimper 14–24 AWG | IWISS IWC-1424A | [Amazon](https://www.amazon.com/dp/B096JS87R8) | 35 |
| T20 Torx | Klein 19543 | [Amazon](https://www.amazon.com/dp/B00093DYRO) | 12 |
| Torque driver 1–6 N·m | 1/4 in | [Amazon](https://www.amazon.com/s?k=1%2F4+inch+torque+screwdriver+6+Nm) | 40 |
| Nylon trim pry set | — | [Amazon](https://www.amazon.com/s?k=automotive+trim+removal+tool+set+nylon) | 12 |
| DMM 60 V CAT III | Klein MM400 | [Amazon](https://www.amazon.com/s?k=Klein+MM400) | 50 |
| Soldering iron | TS101 | [Amazon](https://www.amazon.com/s?k=TS101+soldering+iron) | 40 |
| Heat gun | — | [Amazon](https://www.amazon.com/s?k=heat+gun+adhesive+shrink) | 25 |
| Terminal pick | — | [Amazon](https://www.amazon.com/s?k=automotive+terminal+release+tool+pick) | 10 |
| OEM TS 1.5 mm die (optional) | Rennsteig 624 1686 3 012 RT | [Rennsteig](https://www.rennsteig.us/products/crimping-tools/general-stamped-and-formed-contacts/1628-crimp-die-set-for-sumitomo-ts-series-1-5-mm-060-terminals) · [EFI](https://www.eficonnection.com/home/product/rennsteig-crimp-die-set-624-1686-3-012rt) | 300 + frame |
| Logic analyzer (optional) | 8-ch 24 MHz | [Amazon](https://www.amazon.com/s?k=8+channel+logic+analyzer+24MHz+USB) | 15 |
| Hot-glue / DP100 | pot 6210 | [Amazon](https://www.amazon.com/s?k=hot+glue+gun+kit) | 10 |

Do not use an SN-28B on 8240-0213. IWC-1424A or the Rennsteig die. Pull-test every crimp.

## Order in three carts

1. **Nexelec / Connector ID / Octopart** — 5718, 6210, terminals.
2. **Digi-Key** — NTC, TLIN2029, SMBJ58A, IRL540N, LM393, TL431, 58 V fuses, passives.
3. **Amazon + Waytek** — ESP32, XL7015, Starlink cable, crimper, T20, tape, GXL, VHB, PETG.

One-off parts ~$90–120. Tools ~$150 if you don't already have a DMM and iron. Skip the $300 Rennsteig unless you are making more than one Y.
