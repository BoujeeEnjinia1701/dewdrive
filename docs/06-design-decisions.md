---
doc_id: DWD-DEC-001
title: DewDrive design decisions register
project: DewDrive
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, DWD-DDR-001 to DWD-DDR-003 and the build plan work
---

# DewDrive design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

All are **Proposed, awaiting Amish**.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review of the design-for-construction changes P1 to P13 (condenser plate under the walls, battened wall panels, tray deck, hung drip screens, fin feet, gutter and floor drain, one outlet through the fan hood, lowered inlet, framed lid, bolted and braced stand, PV pole and backing plate, folded trays) | (a) accept as made; (b) change any item | (a) | The whole build plan follows them | DWD-DDR-003, Table 1 |
| 2 | Budget (R11): the buildable design costs $620 against the $520 `budget_usd` | (a) raise `budget_usd` to $625; (b) cut about $20 (single strap size, offcut sheet, cheaper bracket and plate), still over budget; (c) also drop the logger for a timer-only fan switch (about $15 more), losing R12 | (a) | Buying every part on the BOM | DWD-DDR-003, A1; DWD-CAL-001, J1 |
| 3 | Portability (R9): the full box is 35.2 kg against 35 kg; 23.4 kg with the trays and deck lifted out first, as the build plan does | (a) restate R9 as "box 35 kg or less when lifted with the trays and deck taken out"; (b) take about 0.5 kg out (thinner screen straps and deck brackets, lighter lid channel) and keep R9 as written | (a) | Step 16 (box onto the stand) | DWD-DDR-003, A2; DWD-CAL-001, G1, G2 |
| 4 | Glazing temperature rating: a dry bed stagnates at about 122 °C, near the usual 120 °C service rating of twin-wall polycarbonate | (a) specify a sheet rated 130 °C or more; (b) confirm from supplier data that the inner skin, which runs cooler than the bed, stays inside the rating | (a), or (b) if no such sheet is sold locally | Lid sheet (section 3.9); safety stop S3 | DWD-DDR-002, O5 |
| 5 | Low-emissivity drip screens: 0.82 L per day instead of 0.57, but a 166 °C dry-bed stagnation | (a) evaluate a stagnation vent or a higher-rated glazing on paper at TRL 3; (b) drop the idea | (a) | None for the first prototype (black screens) | DWD-DDR-002, O4 |
| 6 | First partner and region for co-design, which also supplies the site climate data | Partner and region to be named | None yet (portfolio rule: partners are picked per area later) | Site, anchors and the design point check | DWD-DDR-001, O1 |
| 7 | Appearance model deviations (anchor position and straps, electronics box orientation, radiation shield, jerrycan handle, rounded corners and lid frame), now also behind the constructable design | (a) accept the five deviations and update the appearance model and renders to the constructable design on Amish's Mac; (b) leave the renders as concept images | (a) | None in the build; renders and storefront images | `docs/REVIEW.md`, session 2026-09-26 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The silica gel is a grade that does not crack in liquid water (sold as water-resistant or for impregnation), with about 1.0 cm³/g pore volume | Ordinary silica gel can shatter when the salt solution is poured on it; the pore volume sets the salt containment | Build plan, section 3.8; DWD-CAL-001, E1 |
| 2 | The polycarbonate sheet's temperature rating and that the U-channel fits its 10 mm edge | Open decision 4; the frame holds the sheet | Build plan, section 3.9 |
| 3 | High-temperature epoxy rated 120 °C or more, and a food-safe coating for aluminium | The fins' bond and the wetted face see condenser temperatures and the water | Build plan, section 3.2 |
| 4 | The bulkhead fitting suits a 17 mm hole and its nut clears the fins (31 mm or less across) | It sits between two fins 50 apart | Build plan, section 3.3 |
| 5 | The 120 mm fan fits the hood front's 114 mm hole and its four corner screws | Sets the hood hole | Build plan, section 3.11 |
| 6 | The ground anchors hold 100 N or more of uplift in the site's soil | DWD-CAL-001, H4 asks for 98 N each | Build plan, section 3.19 |
| 7 | The electronics box is about 160 x 110 x 220 and holds the controller, battery and logger | Sets the backing plate and hole pattern | Build plan, section 3.18 |
| 8 | The tray deck sags no more than the gasket can take (about 3 mm at the centre by hand calculation) | If the tray lips lift, use a deeper bar | DWD-DDR-003, P3 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: budget raised to $500; problem wording; silica gel and CaCl₂ composite; single-stage flat box with the condenser as its floor; fan-assisted night airflow with a 10 W panel and LiFePO4 battery; manual flaps; fixed 20° tilt and twin-wall polycarbonate; design point | Amish: go with recommendation | DWD-DDR-001 |
| 2026-09-25 | TRL 3 items D9 to D14: night air drawn down through sealed trays; 25 wt % salt; drip screens and a fan cut-out above 70 % RH; low-emissivity screen evaluated on paper; ground anchors as default restraint; budget kept at $500 | Amish: "i accept all your recommendations, go with them across all repos." | DWD-DDR-002 |
| 2026-09-25 | TRL 4 on hold; `trl_target` stays 3 | Amish | `project.yaml` |
| 2026-09-26 | Budget top-up to $520 (D15) | Amish: "I am ok with the budget top ups" | DWD-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | DWD-DDR-003 (changes made under this instruction; open decision 1) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | `.kit/STANDARDS.md`, section 18 |
