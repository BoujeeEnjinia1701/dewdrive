---
doc_id: DWD-REQ-001
title: DewDrive requirements
project: DewDrive
doc_type: Requirements
version: "0.8"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with a design point and concept status
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (design point and budget decided by Amish in DWD-DDR-001; R11 redefined to $500; status column from DWD-CAL-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R7 restated for the drip screens; R8 and R10 wording; status from DWD-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish (R11 target $520; status from DWD-CAL-001 v0.3)
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from DWD-CAL-001 v0.4 for the constructable design (DWD-DDR-003); R9 and R11 not met, open for Amish
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: R9 restated by Amish on 2026-10-02 for a lift with the trays and deck taken out, with an empty-before-lifting label (DWD-DEC-001, item 2); R9 met
---

# DewDrive requirements

These requirements were checked by calculation at TRL 3 in DWD-CAL-001 v0.5, for the design decided by Amish on 2026-09-25 (DWD-DDR-002) as made buildable in DWD-DDR-003: night air drawn down through the sealed trays, 25 wt % CaCl₂, a drip screen under each tray and a fan cut-out above 70 % RH. The design meets ten of thirteen. Making it buildable added parts: R11 (cost) is over its value-engineering target, at an estimated $620 against $520, and R9 (portability) was not met as first written, the full box being 35.2 kg against 35 kg. Amish restated R9 on 2026-10-02 for a lift with the trays and deck taken out (DWD-DEC-001, item 2), and it is met at 23.4 kg. The design decisions register (DWD-DEC-001) lists R11's cost drivers and savings. R6 and R10 can only be verified by test. The yield targets R1 and R2, missed by the v0.1 design, are now met. Targets are still proposals for review, not user-validated needs, and will be revised after co-design sessions.

## Design point

Decided by Amish on 2026-09-25 (DWD-DDR-001, D8). Unless a requirement says otherwise, it applies at this design point:

- Night: 10 h adsorption at 20 °C air and 40 % RH (6.92 g/m³ of vapour).
- Day: 6.0 kWh/m² of sun on the tilted aperture, of which 4.24 kWh/m² falls in the 09:00 to 15:00 window (DWD-CAL-001, C1); air at 35 °C.
- Low-humidity case: night air at 20 °C and 25 % RH, same sun.

## Requirements

Table 1. Requirements and TRL 3 status. Values and tags are from DWD-CAL-001 v0.5, Table 4.

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Produce water at the design point | 0.5 L per day or more collected, per unit | Cyclic mass and heat balance (DWD-CAL-001); later field test | Met: 0.57 L per day (C3); v0.1 design 0.20 L |
| R2 | Produce water in dry nights | 0.25 L per day or more at 25 % night RH | Same | Met: 0.45 L per day (C4); v0.1 design 0.09 L |
| R3 | Use only the sun for regeneration | No fuel or grid power; bed reaches 75 °C or more by midday on a clear day at 35 °C ambient | Collector heat balance | Met: bed about 112 °C at noon (C2) |
| R4 | Run its own electrical loads | Fan and logger need 30 Wh per day or less, supplied by the on-board PV panel, with 2 days or more of battery autonomy | Energy budget | Met: 23.6 Wh per day against 35 Wh per day; 2.6 days of autonomy (F1, F2) |
| R5 | Keep the condenser cool | Condenser 15 K or less above ambient at the peak of desorption | Condenser heat balance | Met: 12.1 K (C2) |
| R6 | Keep the water clean | All wetted parts food-grade; no salt carry-over (chloride in the collected water below 250 mg/L) | Materials review; later laboratory water test | **Not verifiable at TRL 3.** Materials chosen to meet it |
| R7 | Contain the salt | No liquid CaCl₂ solution leaves the tray and drip-screen assembly or reaches the condenser, even after a night at 90 % RH (restated by DWD-DDR-002, D11; was "leaves the trays") | Pore volume against solution volume; sump volume; later chamber test | Met on paper: the pores fill only above 71 % RH (E2); one 90 % RH night fills 43 % of them (E3), three in a row 50 % with the fan rule and 63 % without it (E4, E5); the sumps hold 0.58 L as a backstop (E6) |
| R8 | Be simple to operate | Two user actions per day (open flaps in the evening, close them in the morning), 5 min per day or less | Task analysis; co-design sessions | Met by design; the fan timer and humidity cut-out need no user action |
| R9 | Be portable and quick to set up | Box 35 kg or less when lifted with the trays and deck taken out (two-person lift), and labelled to be emptied before lifting; stand separable; set up by two people in 30 min or less. Restated by Amish on 2026-10-02 (DWD-DEC-001, item 2; DWD-DDR-003, A2); was "box 35 kg or less" | Mass from model components; later trial | Met: 23.4 kg with the trays, sorbent, deck and screens lifted out; 35.2 kg with everything inside; total 60.2 kg (G1, G2). Set-up time needs a trial |
| R10 | Survive the site | Stable in 20 m/s (72 km/h) wind with two ground anchors (default, DWD-DDR-002, D13) or ballast; UV-stable glazing; sorbent 300 cycles or more with 20 % or less loss of capacity | Wind load calculation; supplier data; later cycling test | **Not verifiable at TRL 3.** Wind: two anchors of 98 N each, or 40 kg of ballast (H2 to H4) |
| R11 | Cost | Parts $520 or less (`project.yaml` value-engineering target, moved from $400 to $500 by Amish on 2026-09-25, DWD-DDR-001 D1, and to $520 on 2026-09-26, DWD-DDR-002 D15) | Priced BOM | **Over the value-engineering target by $100:** $620 (J1) against $520; the buildable design added parts (DWD-DDR-003) |
| R12 | Record performance | Log air temperature and RH, bed and condenser temperature every 5 min for 30 days or more; daily water mass recorded by weighing | Storage estimate; design review | Met: 8,640 records, 0.41 MB (I1) |
| R13 | Protect users | External surfaces a person would touch in normal use stay at 60 °C or less; the glazing is labelled hot; no exposed conductor above 60 V DC | Surface temperature estimate; design review | Met: glazing outer skin about 57 °C at stagnation, fins up to 47 °C (D2, D3); 12.8 V DC |

## Assumptions

- The composite (25 wt % CaCl₂: 1.0 kg in 3.0 kg of mesoporous silica gel) is modelled from bulk salt thermodynamics: at equilibrium it holds 0.397 g/g at 40 % RH and 0.258 g/g at 25 % RH (DWD-CAL-001, A4). The yield is set by how fast the bed takes up and gives off water, not by these capacities. Measured isotherms and uptake rates of the actual composite must replace the model.
- The day ends with the salt dried to about the dihydrate; the night starts with the bed at air temperature.
- With the fan stopped above 70 % RH, natural airflow through the open flaps is taken as 4 m³/h (10 % of the fan flow); this is an assumption to check by test.
- One unit is a supplement: about 0.57 L per day is about one fifth of one person's survival drinking need of 2.5 to 3 L per day (WHO technical note 9).

> **Safety:** Requirements R6, R7, R10 and R13 exist because of hazards: untreated water, a corrosive salt solution, wind loads on a 1.1 m² panel, and hot surfaces. They cannot be waived without a documented decision by Amish.
