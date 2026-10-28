---
doc_id: DWD-DDR-004
title: DewDrive concept selection
project: DewDrive
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between options A, B and C of DWD-OPT-001; proposed, awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed, awaiting Amish. Options B (120) and A (117) are within 10 % on the weighted total, so both go to Amish without a pick (STANDARDS section 21). Option A stays the design of record until he decides.

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21). DewDrive was designed before kit 1.8, so its current design is option A and is not redesigned without Amish's go. Two more options were defined with different working principles and modelled at detail level D3 (DWD-OPT-001; `cad/src/dwd_options.py`): B, a radiative dew condenser (no sorbent), and C, a liquid-desiccant glazed still (liquid absorption on cloth, condensation on the glazing).

## Options considered

| Option | Working principle | Water at 40 % / 25 % night RH | Estimated parts cost | Weighted score (of 170) |
| --- | --- | --- | --- | --- |
| A, solar desiccant box | Fan-driven night adsorption through CaCl₂-silica gel beds; sealed glazed box regenerates by day; shaded finned floor condenses | 0.44 / 0.31 L per day (DWD-CAL-001 C3, C4) | $695 (BOM) | 117 |
| B, radiative dew condenser | Sky-cooled insulated panel with a high-emissivity coating; dew below the dew point | 0 / 0 (DWD-STM-001 B2) | about $230 (estimate) | 120 |
| C, liquid-desiccant glazed still | CaCl₂ brine on black cloth absorbs at night through open gable doors; closed glazed still regenerates by day | about 0.2 to 0.5 / about 0 (DWD-STM-001 C1 to C3) | about $445 (estimate) | 90 |

## Decision

Proposed, awaiting Amish. The choices are:

1. **Keep option A** as the design of record. Option B leads on the total only because of its simplicity and safety; it makes no water at the design point, which is the need the product exists for (UR-001). Treated as a gate, UR-001 removes option B, and option A then leads option C by 30 %. Option A misses its own 0.5 L per day target (0.44 L), which is open item 2 of DWD-DEC-001.
2. **Move to option B.** Cheaper, passive and safe, but it would supply water only on humid nights (about 55 to 60 % RH and above), not in the dry season.
3. **Move to option C.** Passive, but it makes 0.2 to 0.5 L per day at the design point depending on how hot the cloth gets, and keeps free brine next to the water path.

The scores are within 10 %, so no pick is made here. For information: none of the three meets the 0.5 L per day target on the lumped model's central estimate; option A comes closest with the least uncertainty (0.44 L per day), option C spans 0.2 to 0.5 L per day and option B makes nothing.

## Consequences

- Whatever Amish decides, the drawing, priced BOM and build plan describe option A until a different choice is made. `project.yaml` lists `concept_options: [A, B, C]` and leaves `concept_chosen` as "A (proposed)".
- Option B's best idea, a high-emissivity coating, is already on option A's condenser underside as a STEM check fix (DWD-DEC-001, D18).
- If Amish chose option B or C, the repo would go back to stage P1 for that option's calculation note, drawing, BOM and build plan.
