# BOM notes

Prices are TRL 3 estimates in USD, built up from typical small-quantity prices for each supplier type named in `bom.csv`. They are not quotes. Line numbers match the callouts in `media/exploded.png` and `media/cutaway.png`. Line 14 has no callout.

| Group | Items | Cost |
| --- | --- | --- |
| Collector: stand, box, glazing, trays, sorbent, condenser, water path | 1 to 9, 14 | $360 |
| Night fan, power and logging | 10 to 13 | $128 |
| **Total parts cost** | 1 to 14 | **$488** |

The total of $488 is inside the $500 `budget_usd` that Amish set on 2026-09-25 (DWD-DDR-001, D1), with a margin of $12 (2.4 %). The margin is thin: the condenser (line 6) and the glazing (line 3) are the lines most likely to move. DWD-CAL-001 (J1) reads this file and checks the total.

Changes from TRL 2 ($475): line 1 rose by $10 to include two auger ground anchors, because DWD-CAL-001 (H2 to H4) shows the stand tips at 20 m/s without about 50 kg of ballast or anchors; line 6 rose by $3 after a material build-up. The other lines keep their price and now name a supplier type.

Every part that touches the water (items 5 to 8 and the sealant in item 14) must be food-grade or food-contact rated. The sorbent is the part most likely to change: DWD-CAL-001 (E4 to E6) proposes cutting the salt loading to about 25 wt % to keep the solution inside the pores. That change would not change the cost noticeably. The through-flow tray option proposed in `docs/REVIEW.md` is not in this BOM; it is awaiting Amish.
