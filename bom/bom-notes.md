# BOM notes

Prices are TRL 3 estimates in USD, built up from typical small-quantity prices for each supplier type named in `bom.csv`. They are not quotes. Line numbers match the callouts in `media/exploded.png` and `media/cutaway.png`. Line 14 has no callout.

| Group | Items | Cost |
| --- | --- | --- |
| Collector: stand, box, glazing, trays, sorbent, condenser, water path, drip screens | 1 to 9, 14, 15 | $387 |
| Night fan, power and logging | 10 to 13 | $128 |
| **Total parts cost** | 1 to 15 | **$515** |

The total of $515 is within the $520 `budget_usd`: the budget of $500 set by Amish on 2026-09-25 (DWD-DDR-001, D1) was topped up to $520 by Amish on 2026-09-26 (DWD-DDR-002, D15), closing O3. R11 is met, with $5 to spare. DWD-CAL-001 (J1) reads this file and checks the total.

Changes for DWD-DDR-002 (from $488): line 4 rose from $10.00 to $11.50 per tray for the EPDM edge gasket and a share of the sealing baffle that makes the night air pass through the beds (D9); line 5 rose from $28 to $29 for the new mix of 3.0 kg gel and 1.0 kg CaCl₂ (D10); new line 15 adds four black drip screens with brine sumps at $5 each (D11). The anchors in line 1 are now the default wind restraint (D13).

Changes at TRL 3 from TRL 2 ($475): line 1 rose by $10 to include two auger ground anchors; line 6 rose by $3 after a material build-up.

Every part that touches the water (items 5 to 8 and the sealant in item 14) must be food-grade or food-contact rated. The drip screens (item 15) hold brine and must be kept apart from the water path.

Decided by Amish on 2026-10-02 (DWD-DEC-001): the glazing in line 3 is twin-wall polycarbonate rated 130 °C or more, or a 120 °C sheet only if the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating (item 3); the box carries an "Empty before lifting" label (item 2). The line 3 specification text and the label are follow-ups and are not yet in `bom.csv`; the drip screens stay black (item 4).
