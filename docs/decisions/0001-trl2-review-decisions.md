---
doc_id: DWD-DDR-001
title: DewDrive TRL 2 review decisions
project: DewDrive
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D8; the O2 proposals were decided in DWD-DDR-002; item O1 remains proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation or a single proposed choice is therefore decided in favor of it. The one item without a recommendation stays open. TRL 4 work is on hold by the same instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (TRL 2 session) and in DWD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Budget | Raise `budget_usd` from $400 to $500 for a research prototype with fan and logging, rather than a fanless $400 version or cost cuts that cost yield. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Problem wording | Reword the `project.yaml` problem line to: "Arid households without surface water or groundwater within reach depend on carried or trucked water; the air above them is an untapped supplementary source." Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Sorbent | Silica gel with about 33 wt % CaCl₂, rather than LiCl composites, zeolite or MOF. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Collector layout | Single-stage flat glazed box with the condenser as its shaded floor, rather than dual-stage or a separate condenser. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Night airflow and power | Fan-assisted night airflow with a 10 W PV panel and a 12.8 V LiFePO4 battery, rather than natural airflow. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Flaps | Manual flaps, rather than automatic actuators. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Tilt and glazing | Fixed 20° tilt facing the equator; twin-wall polycarbonate glazing rather than glass. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Design point | 20 °C and 40 % RH at night, 6.0 kWh/m² of sun per day on the aperture; low-humidity case 25 % RH. Decided by Amish, 2026-09-25: go with recommendation. |

Notes on the decided items:

- **D1.** `budget_usd` in `project.yaml` is now 500. R11 in DWD-REQ-001 v0.3 is redefined to $500. The TRL 3 BOM totals $488 (DWD-CAL-001, J1).
- **D2.** The problem line is applied to `project.yaml` and `README.md`. The review recommended no change to the `pitch`, which still describes the device accurately, so it is kept.
- **D3.** The salt loading is decided at about 33 wt %. DWD-CAL-001 (section E) found that this loading lets the solution fill the pores above 51 % RH, and proposes about 25 wt % instead; that was a new item, decided by Amish on 2026-09-25 (DWD-DDR-002, D10: 25 wt %), which amends D3.
- **D4 and D5.** DWD-CAL-001 (section B) found that air flowing past the trays captures only about 11 % of the vapour it carries, so R1 and R2 are not met as drawn. Drawing the air through the bed was decided by Amish on 2026-09-25 (DWD-DDR-002, D9); it keeps D4 and D5.
- **D8.** DWD-CAL-001 (C1) shows that the 6.0 kWh/m² day puts 4.24 kWh/m², not 4.5, in the 09:00 to 15:00 window; DWD-REQ-001 v0.3 carries the corrected figure.
- **SwapCell.** DewDrive uses its own 76.8 Wh battery and does not use a SwapCell pack. The portfolio decisions of 2026-09-25 on the SwapCell interface (v0.3 items: wake without CAN, charge-while-discharging mode, latch vibration rating) and on pricing shared packs once therefore do not change the DewDrive design or BOM.

*Table 2. Items left open by this record. O1 is still Proposed, awaiting Amish; O2 has since been decided.*

| # | Item | Why it stays open |
| --- | --- | --- |
| O1 | First partner and region for co-design, which will also supply the site climate data | No recommendation was made; the portfolio decision is to pick co-design partners per area later |
| O2 | New TRL 3 proposals: through-flow trays, salt loading, radiation between bed and condenser, humid-night protection | Decided by Amish, 2026-09-25: go with recommendation. Recorded in DWD-DDR-002 (D9 to D14) |

## Consequences

- DWD-PRB-001, DWD-PRC-001 and DWD-REQ-001 are revised to v0.3 to show the decisions: the key design choices of the precis are no longer "proposed", R11 carries the new budget, and the design point is decided.
- `project.yaml` carries `budget_usd: 500` and the reworded problem line.
- The partner question (O1) stays open in DWD-PRB-001.
