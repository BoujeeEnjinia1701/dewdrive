---
doc_id: DWD-DEC-001
title: DewDrive design decisions register
project: DewDrive
doc_type: Design decisions register
version: '0.6'
status: Draft
date: '2026-10-25'
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
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Follow-ups carried out; vent study result recorded (low-emissivity screens dropped); cost USD 639 against the USD 520 target
- version: "0.5"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: concept selection opened (DWD-DDR-004, proposed, awaiting Amish); STEM check fixes D16 to D20 decided under Amish's standing instruction of 2026-10-23 (DWD-DDR-005), D19 and D20 after the independent review; open items 2 to 4 (PR-001 recovery, fan cut-out, design wind speed); items to confirm 9 to 12; value engineering at USD 695"
- version: '0.6'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish decided open items 3 (fan cut-out 65 % RH) and 4 (25 m/s design gust) as recommended on 2026-10-25; items 1 and 2 stay open'
---

# DewDrive design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Concept selection between the three options of DWD-OPT-001 | A, solar desiccant box (current design); B, radiative dew condenser; C, liquid-desiccant glazed still | None: B scores 120 and A 117 of 170, within 10 %, so both go to Amish without a pick (STANDARDS section 21). For information, B makes no water at the design point, and with UR-001 as a gate A leads C by 30 %. Proposed, awaiting Amish | Everything, if B or C were chosen; nothing if A is kept | DWD-DDR-004; DWD-OPT-001 |
| 2 | How to recover PR-001: the design collects 0.44 L per day against 0.5 (0.37 to 0.41 under the sensitivities, DWD-CAL-001 C9, C12, C13) | (a) restate PR-001 at about 0.4 L per day for one unit; (b) a larger box (about 1.3 x 1.0 m) for the same target, with more cost and mass; (c) reopen the low-emissivity drip screens (0.82 L per day in C10) with a thermostatic stagnation vent and a glazing grade for the higher bed temperature, reversing the 2026-10-02 decision; (d) keep the target and decide after the isotherms and absorptance are measured at TRL 4 | (d) now, with (c) studied on paper as the route with the largest gain. Proposed, awaiting Amish | (b) and (c) change the box, screens, glazing and cost | DWD-CAL-001 v0.8, C3, C10, C13; DWD-STM-001 S26 |

Open items 3 (fan cut-out) and 4 (design wind speed) were decided by Amish on 2026-10-25 as recommended and are under Decisions made; items 1 (concept, no pick) and 2 (recovering PR-001, recommendation "decide after measurement") stay open.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The silica gel is a grade that does not crack in liquid water (sold as water-resistant or for impregnation), with about 1.0 cm³/g pore volume | Ordinary silica gel can shatter when the salt solution is poured on it; the pore volume sets the salt containment | Build plan, section 3.8; DWD-CAL-001, E1 |
| 2 | The polycarbonate sheet is rated 130 °C or more (decided 2026-10-02), or, for a 120 °C sheet, that the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating; and that the U-channel fits its 10 mm edge | A dry bed stagnates near 122 °C; the frame holds the sheet | Build plan, section 3.9; decision of 2026-10-02 (open item 3) |
| 3 | High-temperature epoxy rated 120 °C or more, and a food-safe coating for aluminium | The fins' bond and the wetted face see condenser temperatures and the water | Build plan, section 3.2 |
| 4 | The bulkhead fitting suits a 17 mm hole and its nut clears the fins (31 mm or less across) | It sits between two fins 50 apart | Build plan, section 3.3 |
| 5 | The 120 mm fan fits the hood front's 114 mm hole and its four corner screws | Sets the hood hole | Build plan, section 3.11 |
| 6 | The ground anchors hold 250 N or more of uplift in the site's soil (DWD-DEC-001 D20) | DWD-CAL-001 H4 asks for 234 N each at the 25 m/s design gust (96 N at the earlier 20 m/s, H5) | Build plan, section 3.19 |
| 7 | The electronics box is about 160 x 110 x 220 and holds the controller, battery and logger | Sets the backing plate and hole pattern | Build plan, section 3.18 |
| 8 | The tray deck sags no more than the gasket can take (about 3 mm at the centre by hand calculation; DWD-STM-001 S19 puts the bar stress at about 20 MPa) | If the tray lips lift, use a deeper bar | DWD-DDR-003, P3 |
| 9 | A coating shop can apply black PTFE (fluoropolymer) to one face of the trays and floors and all faces of the absorbers and drip screens, and quote it | Lines 4 and 15 carry estimates only | DWD-DDR-005, D16 and D17 |
| 10 | PTFE-coated glass-fibre open mesh with about 1.8 mm aperture and about 60 % open area is available locally (baking or conveyor mesh) and holds 2 to 5 mm beads | Replaces the stainless woven mesh; its open share sets the vapour path (DWD-CAL-001, D19) | DWD-DDR-005, D17 and D19 |
| 11 | Perforated aluminium sheet 1 mm, 3 mm holes at 6 mm staggered pitch (R3 T6) is stocked | Sets the absorber's open share (22.7 %) and so its absorptance | DWD-DDR-005, D16 |
| 12 | The plywood, PIR foam, EPDM seals, silicone and coatings are rated for gap air of about 85 °C and surfaces near a 133 °C bed on a peak day | Peak-day stagnation (DWD-CAL-001 D6) | DWD-STM-001 S27 |

## Value engineering

Value-engineering target: USD 520 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 695 (USD 175 over the target). The estimate was USD 515 before the design for construction and USD 639 before the STEM check fixes of 2026-10-25.

Main cost drivers (the parts added to make the design buildable): the tray deck and wall ledges (USD 35), the lid's U-channel frame, hinges and latches priced in full (USD 15 more), wall battens, inserts and paint (USD 13 more), trays with a perforated floor under the mesh (USD 10 more), a proper drain fitting (USD 7), fixings (USD 7), pole, bracket and backing plate (USD 6), fin feet, rivets and epoxy (USD 4), screen frames (USD 4), stand bracing, foot plates and straps (USD 3) and the fan hood (USD 1). The decisions of 2026-10-02 added a glazing sheet rated 130 °C or more (USD 17 more, an estimate without a supplier quote) and the "Empty before lifting" label (USD 2). The STEM check fixes of 2026-10-25 added USD 56: absorber plates (USD 24, D16), black PTFE coatings and a PTFE-coated glass-fibre mesh (USD 32, D17), paint on the condenser underside (USD 8, D18) and floor bars in place of the perforated floor sheets (USD 8 less, D19), all estimates to quote. Over 5 years at the design point the parts cost about USD 0.87 per litre of water.

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
| 2026-10-02 | Result of the vent study of open item 4: a passive vent cannot hold a dry bed near 122 °C at a modest cost (it needs about 117 cm² and must stay shut in normal operation), so the low-emissivity screens are dropped and the black screens stay | Applies Amish's 2026-10-02 decision of open item 4 to the study result | DWD-CAL-001 v0.7, section D (D4, D5) |
| 2026-10-25 | D16: black perforated aluminium absorber plates (1 mm, R3 T6, 22.7 % open, black PTFE) rest on the four beds, because the white beads do not absorb the sun as DWD-CAL-001 assumed (DWD-STM-001 S5; 0.03 L per day without them) | Decided under Amish's standing instruction of 2026-10-23 on STEM check fixes; Amish can reverse it | DWD-DDR-005 |
| 2026-10-25 | D17: brine-wetted faces in black PTFE-coated aluminium and a PTFE-coated glass-fibre floor mesh, because bare aluminium pits and stainless steel risks chloride stress corrosion cracking in hot CaCl₂ brine (DWD-STM-001 S20) | Decided under Amish's standing instruction of 2026-10-23 on STEM check fixes; Amish can reverse it | DWD-DDR-005 |
| 2026-10-25 | D18: fins and condenser plate underside painted with a matt, high-emissivity paint, so they radiate as DWD-CAL-001 C8 assumes (DWD-STM-001 S12) | Decided under Amish's standing instruction of 2026-10-23 on STEM check fixes; Amish can reverse it | DWD-DDR-005 |
| 2026-10-25 | D19: tray floor of a PTFE-coated glass-fibre mesh (about 1.8 mm aperture) on seven 6 x 1.5 mm aluminium bars on edge, in place of a 50 % perforated sheet under a fine mesh, because the floor passed only about 25 % of the bed area to the vapour where DWD-CAL-001 had taken 60 % (independent review; yield 0.36 L per day as it was, 0.44 L with the open floor) | Decided under Amish's standing instruction of 2026-10-23 on STEM check fixes; Amish can reverse it | DWD-DDR-005 |
| 2026-10-25 | D20: ground anchors specified at 250 N or more of uplift each in the site soil, for a 25 m/s gust (234 N), in place of 100 N (a 6 % margin at 20 m/s; independent review) | Decided under Amish's standing instruction of 2026-10-23 on STEM check fixes; Amish can reverse it | DWD-DDR-005 |
| 2026-10-25 | Open item 3: fan humidity cut-out lowered from 70 % to 65 % RH, with restart below 60 %, so it sits 6 points below the 71 % RH at which the pores fill, outside a low-cost sensor's tolerance (supersedes the 70 % of DWD-DDR-002, D11) | Amish: "i concur with your recommendations" | `docs/04-calcs/sizing.py` FAN_RH_OFF, FAN_RH_ON; DWD-STM-001 S16; DWD-BLD-001 first checks; DWD-PRC-001 fan rule |
| 2026-10-25 | Open item 4: design wind speed for PR-010 a 25 m/s gust until the site value is known from the national wind annex (DWD-REG-001 G12); the 250 N anchors of D20 cover it (234 N each); the ballast alternative rises from 39 to 96 kg | Amish: "i concur with your recommendations" | DWD-CAL-001 v0.9 H1 to H5; DWD-PRS-001 PR-010; DWD-BLD-001 S4; DWD-RSK-001 H6, F11 |
