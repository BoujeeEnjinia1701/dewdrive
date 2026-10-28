---
doc_id: DWD-RSK-001
title: DewDrive risk register and hazard analysis
project: DewDrive
doc_type: Risk register
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 pipeline, stage P3)
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'H4, H6, F5, F11 after Amish''s decisions of 2026-10-25 (fan cut-out 65 % RH; 25 m/s design gust)'
---

# DewDrive risk register and hazard analysis

The top project risk is that the design gives too little water: on paper it already misses its 0.5 L per day target (0.44 L), and the real composite may give less than the bulk-salt model. The top hazards are drinking untreated water, burns from the hot interior and CaCl₂ in the eyes. The highest design FMEA items are seal leakage at the flaps and lid and damage to the PTFE coating on the brine-wetted parts. Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high); for detection, 5 means hard to detect.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Yield below 0.5 L per day | Already 0.44 L on paper; isotherm and kinetics of the real composite, absorber absorptance, mesh open share and the temperature drop through the bed could take it lower (0.37 L in C13) | PR-001 not met; weaker case for users | 5 | 4 | Design lead | Decision requested (DWD-DEC-001, open item 2); measure isotherms and absorptance before building (TRL 4 plan); study the low-emissivity screens with a thermostatic vent (C10) |
| P2 | Cost stays over the value-engineering target | Coatings, glazing grade and the parts that made it buildable | $695 against $520 | 5 | 2 | Design lead | Savings in DWD-DEC-001 Value engineering; quotes for the estimated lines |
| P3 | No partner site agreed | The field station candidate is a type, not an agreement | No site data, no TRL 4 test | 3 | 4 | Amish | Approach two or three stations in parallel (DWD-PLN-001) |
| P4 | Coating or mesh not available locally | PTFE coating shops and PTFE glass-fibre mesh are not everywhere | Brine-wetted parts revert to bare metal and corrode | 3 | 3 | Builder | Confirm items 9 and 10 of DWD-DEC-001 before building; fallback is 316 stainless with a shorter life, as a documented decision |
| P5 | Concept choice reopened | A and B within 10 % on the weighted score (DWD-OPT-001) | Rework if Amish chooses B or C | 2 | 4 | Amish | Decision requested in DWD-DDR-004 |
| P6 | Water quality claims misread | Users treat the water as safe without treatment | Illness | 2 | 5 | Partner NGO | Every document says test and treat; labelling on the jerrycan |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Untreated or contaminated water | Dust, microbes or salt in the condensate; jerrycan left for days | Gastrointestinal illness | 4 | 3 | Food-grade wetted parts; drip screens and sumps keep brine out; instruction to boil or disinfect; laboratory test at TRL 4 | Medium until tested |
| H2 | Hot surfaces inside the box | Bed about 105 °C at noon, 133 °C dry on a peak day (DWD-CAL-001 C2, D6) | Burns to hands | 3 | 3 | Open the lid only when cool; gloves; glazing labelled hot; outer surfaces 55 °C or less (PR-013) | Low |
| H3 | CaCl₂ contact | Preparing the sorbent; emptying sumps; a split tray | Skin and serious eye irritation (H315, H319) | 3 | 3 | Gloves and eye protection (build plan safety stops); pores fill only above 71 % RH; sumps | Low |
| H4 | Brine in the drinking water | Pores overfill in a wet spell; tray tipped; coating failure | Salty water; chloride above 250 mg/L | 3 | 2 | Fan cut-out above 65 % RH, restart below 60 % (DWD-DEC-001 item 3); drip screens with no line of sight; level trays; flaps shut in rain | Low |
| H5 | Battery fire or short | Damaged LiFePO4 cell; short in the wiring | Fire, burns | 4 | 1 | Built-in BMS, fuse at the battery, shaded IP65 box, LiFePO4 chemistry | Low |
| H6 | Unit tips over in wind | 495 N on the lid in the 25 m/s design gust; anchors not fitted | Crush injury, damage | 4 | 2 | Two ground anchors rated 250 N or more (or 96 kg of ballast) before the box goes on; check at set-up | Low |
| H7 | Lifting injury | Box 36.1 kg with everything inside | Back injury | 3 | 2 | Empty before lifting (label): 23.4 kg, two people | Low |
| H8 | Cuts | Sheet-aluminium edges, fins at ankle and hand height | Cuts | 2 | 3 | Deburr all edges; edge breaks in the model; paint on the fins | Low |
| H9 | Glazing failure | Polycarbonate inner skin near 106 °C on a peak day, or UV ageing | Sheet sags or cracks, hot interior exposed | 3 | 2 | Sheet rated 130 °C or more (decided 2026-10-02); UV-stabilized | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Inlet flap, lid and outlet flap seals | Keep vapour in by day, force air through the beds at night | Leak | Day vapour lost; night air bypasses the beds; yield falls | EPDM ageing, warped flap, latch not closed | 4 | 4 | 3 | 48 | Smoke check in the first checks; inspect seals monthly; latches with positive over-centre |
| F2 | PTFE coating on trays, floor bars, absorbers and screens | Keep brine off the aluminium | Coating scratched or pin-holed | Pitting, brine leak, aluminium in the water path | Handling, beads abrading the coating | 4 | 3 | 4 | 48 | Coating thickness from the coater; handle trays with gloves; inspect at each recharge |
| F3 | Absorber plates | Absorb the sun over the beds | Dust or salt crust on the plate; plate lifted off the bed | Lower absorptance or poor contact; yield falls | Dust through the inlet; brine creep | 3 | 3 | 3 | 27 | Wipe at recharge; finger holes to lift and reseat; measure absorptance at TRL 4 |
| F4 | Composite sorbent | Store water overnight | Capacity loss; gel cracking | Yield falls over the season | Ordinary gel cracking in solution; salt migration | 4 | 3 | 3 | 36 | Water-resistant gel grade (DWD-DEC-001 item 1); cycling test at TRL 4 |
| F5 | Fan and humidity cut-out | Move night air; stop above 65 % RH | Fan stops, or runs in a humid night | No uptake, or pores fill faster | Fan failure; RH sensor fault | 3 | 2 | 2 | 12 | Logger flags fan current and RH; fail-safe is fan off; sumps as backstop |
| F6 | Battery and charge controller | Power fan and logger | Battery flat | Fan does not run; no log | Cloudy spell longer than 2.6 days; BMS cut-off | 2 | 2 | 2 | 8 | Logger records battery voltage; 1.48 PV margin |
| F7 | Condenser plate, fins and underside paint | Reject 292 W at an 11.9 K rise | Paint chalks or dust coats the fins; coating on wetted face wears | Condenser hotter; yield falls; aluminium in the water | Sun and dust under the box; abrasion | 3 | 3 | 3 | 27 | Repaint as needed; log the condenser rise at TRL 4 (PR-005 at risk); food-safe coating check at TRL 4 water test |
| F8 | Gutter and drain | Carry water to the jerrycan | Blocked or leaking | Water lost | Dust, insects, kinked tube | 2 | 3 | 2 | 12 | Screened drain; tube clip; daily weighing shows a drop |
| F9 | Drip screens and sumps | Catch any brine | Sump overflows | Brine reaches the plate | Wet spell with the fan rule failed | 4 | 1 | 4 | 16 | Sumps 0.58 L; empty after wet spells |
| F10 | Glazing | Let the sun in, hold the heat | Sags or crazes | Heat loss, leak | Sheet below rating, UV | 3 | 2 | 2 | 12 | 130 °C grade; UV-stabilized face up |
| F11 | Stand and anchors | Hold the unit in wind | Anchor pulls out | Tip-over | Soft or sandy soil; gust above the 25 m/s design gust | 4 | 2 | 3 | 24 | Anchors rated 250 N or more in the site soil (D20; to confirm, item 6); ballast alternative (96 kg); design wind a 25 m/s gust until the site value is known (item 4, decided 2026-10-25) |
| F12 | Tray deck | Carry the trays level on the gasket | Sags past the gasket | Air bypasses at the tray lips | Load at 105 °C | 3 | 2 | 3 | 18 | Check sag at build (item 8); deeper bar if needed |
