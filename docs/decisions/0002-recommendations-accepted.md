---
doc_id: DWD-DDR-002
title: DewDrive TRL 3 recommendations accepted
project: DewDrive
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish (O3 decided)
---

# 0002: TRL 3 recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D9 to D14 and, on 2026-09-26, the budget top-up (D15, closing O3); items O1, O4 and O5 remain proposed

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) listed six new items with a recommendation, raised by DWD-CAL-001 v0.1 after DWD-DDR-001 was written. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of it. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so nothing here is built, bought or tested.

## Decision

*Table 1. Decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item (REVIEW.md, TRL 3) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D9 | Night airflow through the bed (item 2) | Option (a): seal the tray edges and draw the night air down through the mesh-floored trays | `model.py`: 1 mm sealing baffle between trays and walls, trays on an EPDM edge gasket; south inlet flap moved above the trays (800 x 40 mm, was 800 x 70 mm below them); outlet and fan stay below the trays. DWD-CAL-001 v0.2 now models through-flow as the design of record. BOM line 4 $10.00 to $11.50 each |
| D10 | Salt loading (item 3; amends D3) | Lower the CaCl₂ to 25 wt %: 1.0 kg in 3.0 kg of gel (was 1.3 kg in 2.7 kg, 32.5 wt %) | Bed depth 8.3 to 9.3 mm in `model.py`; BOM line 5 $28 to $29; pores now fill at 71 % RH, not 51 % |
| D11 | Humid-night protection (item 4) | Adopt both: a drip tray under each sorbent tray, and a logger rule that stops the fan above 70 % RH | New BOM line 15 (four drip screens, $20): two staggered layers of 20 x 6 mm aluminium channels running down the slope, painted black, with a closed brine sump at the low end (0.58 L in all). They catch drips without blocking the air and vapour path. The fan rule is stated in DWD-PRC-001; firmware beyond a sketch is TRL 4 and on hold |
| D12 | Bed-to-condenser radiation screen (item 5) | Evaluate on paper before any build | Done in DWD-CAL-001 v0.2 (C5, C10, D1): low-emissivity screens would raise the yield to 0.82 L per day but push the dry bed to 166 °C at stagnation, beyond the usual polycarbonate rating. Not adopted; the drip screens are painted black instead. A follow-up is proposed below (O4) |
| D13 | Wind restraint (item 6) | Two auger ground anchors are the default; about 50 kg of ballast is the alternative | Wording in DWD-PRC-001, DWD-REQ-001 (R10) and the drawing notes; anchors were already in BOM line 1 |
| D14 | Budget margin (item 7) | Keep `budget_usd` at $500 | `project.yaml` unchanged at 500. The premise that items 2 to 4 add "only a few dollars" did not hold: the BOM is now $515 (see O3, closed by D15) |
| D15 | Budget top-up (O3) | Budget top-up to $520: decided by Amish, 2026-09-26 ("I am ok with the budget top ups") | `project.yaml` `budget_usd` 500 to 520; R11 in DWD-REQ-001 v0.5 now $520 or less and met at $515; DWD-CAL-001 v0.3 re-run |

Results of the decided design (DWD-CAL-001 v0.2), before and after:

| Quantity | Before (CAL-001 v0.1, as drawn) | After (v0.2, design of record) |
| --- | --- | --- |
| Water at 40 % night RH (R1, 0.5 L) | 0.20 L per day | 0.57 L per day |
| Water at 25 % night RH (R2, 0.25 L) | 0.09 L per day | 0.45 L per day |
| Pore-filling humidity (R7) | 51 % RH | 71 % RH |
| Pores filled by one 90 % RH night | 46 % | 43 %; 50 % after three such nights with the fan rule |
| Bed at noon; stagnation | 104 °C; 105 °C | 112 °C; 122 °C |
| Condenser rise (R5, 15 K) | 13.1 K | 12.1 K |
| Solar-to-water efficiency | 2.5 % | 7.1 % |
| Mass; box | 51.4 kg; 30.9 kg | 53.9 kg; 33.4 kg |
| Parts cost (R11, $500) | $488 | $515 |

## Items still open

*Table 2. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design, which also supplies the site climate data | No recommendation was made; stays open (DWD-DDR-001) |
| O3 | Budget: the BOM is $515 against $500 (R11 not met) | **Decided by Amish, 2026-09-26: budget top-up to $520 (option a); see D15.** Original options: Options: (a) raise `budget_usd` to $520; (b) cut the drip screens to a drip gutter under the low edge of each tray (about $8 in all, weaker protection); (c) evaluate a lighter condenser on paper, since the black screens cut its peak load from 333 W to 299 W. Recommendation: (c) first, then (a) if it does not close the gap |
| O4 | Low-emissivity screen with overheat protection | New. The low-e screen gives 0.82 L per day but a 166 °C stagnation bed; it would need a stagnation vent or a glazing rated well above that. Recommendation: evaluate on paper at TRL 3 |
| O5 | Glazing temperature rating | New. With black drip screens the dry bed stagnates at about 122 °C, near the usual 120 °C service rating of twin-wall polycarbonate. Recommendation: specify a sheet rated 130 °C or more, or confirm from supplier data that the inner skin, which runs cooler than the bed, stays inside the rating |

## Consequences

- DWD-PRB-001 v0.4, DWD-PRC-001 v0.4, DWD-REQ-001 v0.4 and DWD-CAL-001 v0.2 carry the decided design. R7 is restated to cover the tray and drip-screen assembly.
- Drawing DWD-DWG-001 moves to Rev P2; STEP, STL and all media are regenerated from `model.py`.
- Requirement status: 10 met, 1 not met (R11, cost), 2 not verifiable at TRL 3 (R6, R10). After the budget top-up to $520 (D15, 2026-09-26), R11 is met: 11 met, 2 not verifiable at TRL 3.
- `trl: 3` and `trl_target: 3` are unchanged. The drip-screen sump test, measured isotherms and the fan rule firmware are TRL 4 work and on hold.
