---
doc_id: DWD-REQ-001
title: DewDrive requirements
project: DewDrive
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# DewDrive requirements

These requirements were checked by calculation at TRL 3 in DWD-CAL-001. The design as drawn meets eight of thirteen: R1 and R2 (water yield) are **not met**, R7 (salt containment) is at risk, and R6 and R10 can only be verified by test. Targets are still proposals for review, not user-validated needs, and will be revised after co-design sessions.

## Design point

Decided by Amish on 2026-09-25 (DWD-DDR-001, D8). Unless a requirement says otherwise, it applies at this design point:

- Night: 10 h adsorption at 20 °C air and 40 % RH (6.92 g/m³ of vapour).
- Day: 6.0 kWh/m² of sun on the tilted aperture, of which 4.24 kWh/m² falls in the 09:00 to 15:00 window (DWD-CAL-001, C1; TRL 2 said 4.5); air at 35 °C.
- Low-humidity case: night air at 20 °C and 25 % RH, same sun.

## Requirements

Table 1. Requirements and TRL 3 status. Values and tags are from DWD-CAL-001, Table 4.

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Produce water at the design point | 0.5 L per day or more collected, per unit | Cyclic mass and heat balance (DWD-CAL-001); later field test | **Not met:** 0.20 L per day as drawn (C3). About 0.53 L per day if night air is drawn through the bed (C5, proposed) |
| R2 | Produce water in dry nights | 0.25 L per day or more at 25 % night RH | Same | **Not met:** 0.09 L per day as drawn (C4). About 0.35 L per day with through-flow (C5, proposed) |
| R3 | Use only the sun for regeneration | No fuel or grid power; bed reaches 75 °C or more by midday on a clear day at 35 °C ambient | Collector heat balance | Met: bed about 104 °C at noon (C2) |
| R4 | Run its own electrical loads | Fan and logger need 30 Wh per day or less, supplied by the on-board PV panel, with 2 days or more of battery autonomy | Energy budget | Met: 23.6 Wh per day against 35 Wh per day; 2.6 days of autonomy (F1, F2) |
| R5 | Keep the condenser cool | Condenser 15 K or less above ambient at the peak of desorption | Condenser heat balance | Met, thin margin: 13.1 K (C2) |
| R6 | Keep the water clean | All wetted parts food-grade; no salt carry-over (chloride in the collected water below 250 mg/L) | Materials review; later laboratory water test | **Not verifiable at TRL 3.** Materials chosen to meet it |
| R7 | Contain the salt | No liquid CaCl₂ solution leaves the trays, even after a night at 90 % RH | Pore volume against solution volume; later chamber test | **At risk:** the pores fill at 51 % RH at equilibrium (E2); one 90 % RH night fills 46 % of them as drawn, 111 % with through-flow (E3) |
| R8 | Be simple to operate | Two user actions per day (open flaps in the evening, close them in the morning), 5 min per day or less | Task analysis; co-design sessions | Met by design |
| R9 | Be portable and quick to set up | Box 35 kg or less (two-person lift); stand separable; set up by two people in 30 min or less | Mass from model volumes; later trial | Met: box 30.9 kg, 24.0 kg with trays out; total 51.4 kg (G1, G2). Set-up time needs a trial |
| R10 | Survive the site | Stable in 20 m/s (72 km/h) wind with anchors or ballast; UV-stable glazing; sorbent 300 cycles or more with 20 % or less loss of capacity | Wind load calculation; supplier data; later cycling test | **Not verifiable at TRL 3.** Wind: 49 kg of ballast or two anchors of 120 N each are needed (H2 to H4) |
| R11 | Cost | Parts $500 or less (`project.yaml` budget, raised from $400 by Amish on 2026-09-25, DWD-DDR-001 D1) | Priced BOM | Met: $488 (J1) |
| R12 | Record performance | Log air temperature and RH, bed and condenser temperature every 5 min for 30 days or more; daily water mass recorded by weighing | Storage estimate; design review | Met: 8,640 records, 0.41 MB (I1) |
| R13 | Protect users | External surfaces a person would touch in normal use stay at 60 °C or less; the glazing is labelled hot; no exposed conductor above 60 V DC | Surface temperature estimate; design review | Met: glazing outer skin about 53 °C at stagnation, fins up to 48 °C (D2, D3); 12.8 V DC |

## Assumptions

- The composite (about 33 wt % CaCl₂ in mesoporous silica gel) is modelled from bulk salt thermodynamics: at equilibrium it holds 0.507 g/g at 40 % RH and 0.330 g/g at 25 % RH (DWD-CAL-001, A4). The yield is set by how fast the bed takes up and gives off water, not by these capacities. Measured isotherms and uptake rates of the actual composite must replace the model.
- The day ends with the salt dried to about the dihydrate; the night starts with the bed at air temperature.
- One unit is a supplement: even about 0.5 L per day is about one fifth of one person's survival drinking need of 2.5 to 3 L per day (WHO technical note 9).

> **Safety:** Requirements R6, R7, R10 and R13 exist because of hazards: untreated water, a corrosive salt solution, wind loads on a 1.1 m² panel, and hot surfaces. They cannot be waived without a documented decision by Amish.
