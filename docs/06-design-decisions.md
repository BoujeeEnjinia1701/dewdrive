---
doc_id: DWD-DEC-001
title: DewDrive design decisions register
project: DewDrive
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, DWD-DDR-001 to DWD-DDR-003 and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations of open items 1 to 6 on 2026-10-02; all moved to decisions made; glazing rating line updated
---

# DewDrive design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The silica gel is a grade that does not crack in liquid water (sold as water-resistant or for impregnation), with about 1.0 cm³/g pore volume | Ordinary silica gel can shatter when the salt solution is poured on it; the pore volume sets the salt containment | Build plan, section 3.8; DWD-CAL-001, E1 |
| 2 | The polycarbonate sheet is rated 130 °C or more (decided 2026-10-02), or, for a 120 °C sheet, that the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating; and that the U-channel fits its 10 mm edge | A dry bed stagnates near 122 °C; the frame holds the sheet | Build plan, section 3.9; decision of 2026-10-02 (open item 3) |
| 3 | High-temperature epoxy rated 120 °C or more, and a food-safe coating for aluminium | The fins' bond and the wetted face see condenser temperatures and the water | Build plan, section 3.2 |
| 4 | The bulkhead fitting suits a 17 mm hole and its nut clears the fins (31 mm or less across) | It sits between two fins 50 apart | Build plan, section 3.3 |
| 5 | The 120 mm fan fits the hood front's 114 mm hole and its four corner screws | Sets the hood hole | Build plan, section 3.11 |
| 6 | The ground anchors hold 100 N or more of uplift in the site's soil | DWD-CAL-001, H4 asks for 98 N each | Build plan, section 3.19 |
| 7 | The electronics box is about 160 x 110 x 220 and holds the controller, battery and logger | Sets the backing plate and hole pattern | Build plan, section 3.18 |
| 8 | The tray deck sags no more than the gasket can take (about 3 mm at the centre by hand calculation) | If the tray lips lift, use a deeper bar | DWD-DDR-003, P3 |

## Value engineering

Value-engineering target: USD 520 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 620 (USD 100 over the target). The estimate was USD 515 before the design for construction.

Main cost drivers (the parts added to make the design buildable): the tray deck and wall ledges (USD 35), the lid's U-channel frame, hinges and latches priced in full (USD 15 more), wall battens, inserts and paint (USD 13 more), trays with a perforated floor under the mesh (USD 10 more), a proper drain fitting (USD 7), fixings (USD 7), pole, bracket and backing plate (USD 6), fin feet, rivets and epoxy (USD 4), screen frames (USD 4), stand bracing, foot plates and straps (USD 3) and the fan hood (USD 1). Over 5 years at the design point the parts cost about USD 0.59 per litre of water.

Savings worth trying: a single 1.5 mm strap size and offcut sheet for the deck and screens (about USD 15), a cheaper panel bracket and backing plate (about USD 5), and a timer-only fan switch in place of the logger (about USD 15, but it loses R12). Together these still leave the design over the target.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: value-engineering target raised to $500; problem wording; silica gel and CaCl₂ composite; single-stage flat box with the condenser as its floor; fan-assisted night airflow with a 10 W panel and LiFePO4 battery; manual flaps; fixed 20° tilt and twin-wall polycarbonate; design point | Amish: go with recommendation | DWD-DDR-001 |
| 2026-09-25 | TRL 3 items D9 to D14: night air drawn down through sealed trays; 25 wt % salt; drip screens and a fan cut-out above 70 % RH; low-emissivity screen evaluated on paper; ground anchors as default restraint; value-engineering target kept at $500 | Amish: "i accept all your recommendations, go with them across all repos." | DWD-DDR-002 |
| 2026-09-25 | TRL 4 on hold; `trl_target` stays 3 | Amish | `project.yaml` |
| 2026-09-26 | Value-engineering target moved to $520 (D15) | Amish: "I am ok with the budget top ups" | DWD-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | DWD-DDR-003 (changes made under this instruction; accepted on 2026-10-02, below) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | `.kit/STANDARDS.md`, section 18 |
| 2026-10-02 | Open item 1: design for construction accepted: the changes P1 to P13 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | DWD-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Open item 2: R9 restated as a box of 35 kg or less when lifted with the trays and deck taken out (23.4 kg, met); the box is labelled to be emptied before lifting | Amish: "i approve your recommendations for all 555 open decisions." | DWD-DDR-003, A2; DWD-CAL-001, G1, G2 |
| 2026-10-02 | Open item 3: glazing is twin-wall polycarbonate rated 130 °C or more; a 120 °C sheet is accepted only if the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating | Amish: "i approve your recommendations for all 555 open decisions." | DWD-DDR-002, O5 |
| 2026-10-02 | Open item 4: one short paper study of a passive stagnation vent; if it cannot hold a dry bed near 122 °C at a modest cost, the low-emissivity screens are dropped. The first prototype keeps black screens | Amish: "i approve your recommendations for all 555 open decisions." | DWD-DDR-002, O4 |
| 2026-10-02 | Open item 5: first partner, the first candidate type to approach (not yet agreed), is a university dryland field station in a hot semi-arid region with night humidity of about 25 to 40 % and an existing weather record, with a water and sanitation NGO for the later community trial | Amish: "i approve your recommendations for all 555 open decisions." | DWD-DDR-001, O1 |
| 2026-10-02 | Open item 6: the five appearance model deviations are accepted, and the appearance model and renders are to be updated to the constructable design on Amish's Mac | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, session 2026-09-26 |
