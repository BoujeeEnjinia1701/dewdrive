# BOM notes

Prices are indicative concept estimates (TRL 2) in USD and will be confirmed with named suppliers at TRL 3. Line numbers match the callouts in `media/exploded.png` and `media/cutaway.png`. Line 14 has no callout.

| Group | Items | Indicative cost |
| --- | --- | --- |
| Collector: stand, box, glazing, trays, sorbent, condenser, water path | 1 to 9, 14 | about $347 |
| Night fan, power and logging | 10 to 13 | about $128 |
| **Total parts cost** | 1 to 14 | **about $475** |

The total of about $475 is about 19 % over the $400 `budget_usd` in `project.yaml`. A fanless version that relies on natural airflow at night and logs from a USB power bank would drop most of items 10 to 12 and come to about $400, at the cost of slower overnight uptake. The options are set out in `docs/REVIEW.md`; the budget is unchanged until Amish decides.

Every part that touches the water (items 5 to 8 and the sealant in item 14) must be food-grade or food-contact rated. The sorbent is the part most likely to change: the calcium chloride loading and the silica gel grade are both proposals awaiting Amish.
