# BOM notes

Prices are TRL 3 estimates in USD, built up from typical small-quantity prices for each supplier type named in `bom.csv`. They are not quotes. Line numbers match the callouts in `media/exploded.png` and `media/cutaway.png`. Line 14 has no callout.

| Group | Items | Cost |
| --- | --- | --- |
| Collector: stand, box, glazing, trays, sorbent, condenser, water path, flap, drip screens, tray deck, hardware | 1 to 9, 14 to 16 | $504 |
| Night fan, power and logging | 10 to 13 | $135 |
| **Total parts cost** | 1 to 16 | **$639** |

The total of $639 is $119 over the $520 value-engineering target (`budget_usd`, a hypothetical control target, not a limit; set to $500 by Amish on 2026-09-25, DWD-DDR-001 D1, and $520 on 2026-09-26, DWD-DDR-002 D15). R11 is over its target. DWD-CAL-001 (J1) reads this file and checks the total. The total was $515 before the design for construction (DWD-DDR-003, which added line 16 and repriced others, to $620) and rose by $19 with the decisions of 2026-10-02, below.

Changes for DWD-DDR-002 (from $488): line 4 rose from $10.00 to $11.50 per tray for the EPDM edge gasket and a share of the sealing baffle that makes the night air pass through the beds (D9); line 5 rose from $28 to $29 for the new mix of 3.0 kg gel and 1.0 kg CaCl₂ (D10); new line 15 adds four black drip screens with brine sumps at $5 each (D11). The anchors in line 1 are now the default wind restraint (D13).

Changes at TRL 3 from TRL 2 ($475): line 1 rose by $10 to include two auger ground anchors; line 6 rose by $3 after a material build-up.

Every part that touches the water (items 5 to 8 and the sealant in item 14) must be food-grade or food-contact rated. The drip screens (item 15) hold brine and must be kept apart from the water path.

Decided by Amish on 2026-10-02 (DWD-DEC-001) and carried into this file the same day:

- Line 3 (glazing lid): the sheet is twin-wall polycarbonate rated 130 °C or more (item 3), or a 120 °C sheet only if the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating. Price basis: a 130 °C grade at about $48 per square metre (an estimate of about 50 % above the $32 per square metre of a standard sheet; no supplier quote yet) over 1.09 m², which raises the sheet from about $35 to about $52, so line 3 rises from $65 to $82. Re-price from a quote when one is available.
- Line 14 (hardware and consumables): one printed outdoor vinyl label, 150 x 50 mm, "Empty before lifting: remove trays, sorbent and deck", on the east wall (item 2), about $2 (estimate), so line 14 rises from $32 to $34. The label is modelled as a 0.5 mm plate in `cad/src/model.py` and drawn in the picture for build step 16; its mass (about 5 g) is counted in the hardware group.
- The drip screens stay black (item 4); the paper study of a passive vent (DWD-CAL-001, section D) finds no modest-cost passive remedy, so the low-emissivity screens are dropped.
