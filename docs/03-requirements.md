---
doc_id: DWD-REQ-001
title: DewDrive requirements
project: DewDrive
doc_type: Requirements
version: "0.2"
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
---

# DewDrive requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after co-design sessions. Two requirements are not met by the current concept (R11 cost, and R2 at risk), and several can only be verified by test.

## Design point

Unless a requirement says otherwise, it applies at this design point (proposed):

- Night: 10 h adsorption at 20 °C air and 40 % RH (about 6.9 g/m³ of vapour).
- Day: about 6.0 kWh/m² of sun on the tilted aperture, with about 4.5 kWh/m² in the 6 h desorption window; air at 35 °C.
- Low-humidity case: night air at 20 °C and 25 % RH, same sun.

## Requirements

Table 1. Requirements and concept status. "Estimate" means a first-order figure from DWD-PRC-001, to be checked at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Produce water at the design point | 0.5 L per day or more collected, per unit | Mass balance calculation from sorbent isotherms; later field test | Estimate about 0.49 L per day (range 0.35 to 0.6). Met at the nominal estimate, no margin |
| R2 | Produce water in dry nights | 0.25 L per day or more at 25 % night RH | Same | Estimate about 0.25 L per day. **At risk**: depends on the CaCl₂ hydrate behaviour below its deliquescence point |
| R3 | Use only the sun for regeneration | No fuel or grid power; bed reaches 75 °C or more by midday on a clear day at 35 °C ambient | Collector heat balance | Estimate 80 to 90 °C; similar glazed absorbers reached 94 °C (LaPotin et al., 2021). Met by estimate |
| R4 | Run its own electrical loads | Fan and logger need 30 Wh per day or less, supplied by the on-board PV panel, with 2 days or more of battery autonomy | Energy budget | Estimate about 24 Wh per day against about 35 Wh per day from a 10 W panel; about 3 days autonomy. Met, thin margin |
| R5 | Keep the condenser cool | Condenser 15 K or less above ambient at the peak of desorption | Condenser heat balance | Estimate about 12 K with a low-emissivity tray underside. Met by estimate, unverified |
| R6 | Keep the water clean | All wetted parts food-grade; no salt carry-over (chloride in the collected water below 250 mg/L) | Materials review; later laboratory water test | **Not verifiable at TRL 2.** Materials chosen to meet it |
| R7 | Contain the salt | No liquid CaCl₂ solution leaves the trays, even after a night at 90 % RH | Salt loading calculation against uptake at 90 % RH; later chamber test | Unverified. Salt loading capped at about 33 wt % for this reason |
| R8 | Be simple to operate | Two user actions per day (open flaps in the evening, close them in the morning), 5 min per day or less | Task analysis; co-design sessions | Met by design |
| R9 | Be portable and quick to set up | Box 35 kg or less (two-person lift); stand separable; set up by two people in 30 min or less | Mass estimate; later trial | Estimate box about 30 kg, total about 45 kg. Met by estimate |
| R10 | Survive the site | Stable in 20 m/s (72 km/h) wind with anchors or ballast; UV-stable glazing; sorbent 300 cycles or more with 20 % or less loss of capacity | Wind load calculation; supplier data; later cycling test | Unverified. Wind uplift estimate about 330 N, so anchors or about 40 kg of ballast are needed |
| R11 | Cost | Parts $400 or less (`project.yaml` budget) | Priced BOM | **Not met:** about $475 (indicative), about 19 % over |
| R12 | Record performance | Log air temperature and RH, bed and condenser temperature every 5 min for 30 days or more; daily water mass recorded by weighing | Design review | Met by design (logger and sensors, items 12 and 13) |
| R13 | Protect users | External surfaces a person would touch in normal use stay at 60 °C or less; the glazing is labelled hot; no exposed conductor above 60 V DC | Surface temperature estimate; design review | Met by design at 12.8 V; glazing surface temperature unverified |

## Assumptions

- The composite (about 33 wt % CaCl₂ in mesoporous silica gel) takes up about 0.30 g/g at 40 % RH and 20 °C and about 0.16 g/g at 25 % RH. These are estimates between published values for similar composites (0.52 g/g at 60 % RH for a LiCl and silica gel composite, Shao et al., 2024; up to 0.6 to 0.7 g/g for SWS-1L, Aristov et al., 2006). They must be replaced by measured isotherms at TRL 3.
- Half of the overnight uptake is released by day. That needs the bed near 85 °C with the condenser at 45 to 50 °C.
- One unit is a supplement: about 0.5 L per day is about one fifth of one person's survival drinking need of 2.5 to 3 L per day (WHO technical note 9).

> **Safety:** Requirements R6, R7, R10 and R13 exist because of hazards: untreated water, a corrosive salt solution, wind loads on a 1.1 m² panel, and hot surfaces. They cannot be waived without a documented decision by Amish.
