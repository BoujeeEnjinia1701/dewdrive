---
doc_id: DWD-FEA-001
title: DewDrive feasibility assessment
project: DewDrive
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First assessment (kit 1.8 pipeline), after the STEM check and DWD-CAL-001 v0.8
---

# DewDrive feasibility assessment

DewDrive is feasible to build and test as a research prototype, but on paper it does not meet its 0.5 L per day target: the physics holds after the five STEM check fixes and every part can be made in a small workshop or bought, yet the design collects about 0.44 L per day (0.37 to 0.41 L under the sensitivities), on an isotherm built from bulk salt data and an estimated absorber absorptance. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design (physics) | Solar-regenerated sorption with a shaded condenser is within known science; 27 claims checked on option A, five detail failures fixed (absorber, tray floor, brine-wetted materials, condenser emissivity, anchors) | Medium | Yield 0.44 L per day against 0.5, PR-001 not met; 0.37 to 0.41 under the sensitivities (C9, C12, C13); recovery open for Amish | DWD-STM-001; DWD-CAL-001 v0.8 |
| Materials | Plywood and PIR walls, aluminium sheet, PTFE coatings, twin-wall polycarbonate rated 130 °C, food-grade silica gel and CaCl₂ | Medium | Coating quality and quote; water-resistant silica gel grade; polycarbonate grade against a 106 °C inner skin on a peak day; hot-material ratings (item 12) | DWD-DDR-005; DWD-DEC-001 items 1, 2, 9, 10 |
| Manufacturing and assembly | Cut, fold, drill, rivet and bolt; 31 components and 19 assembly steps in the build plan; coatings bought in | High | Seal quality at the flaps, deck gasket and lid decides night bypass and day vapour loss | DWD-BLD-001; `cad/fidelity.json` (D3, 0 interferences) |
| Power and controls | 10 W panel, 76.8 Wh LiFePO4 battery and an ESP32 logger with a fan timer and humidity cut-out; 23.6 Wh per day against 35 Wh | High | Firmware is a sketch until TRL 4; the cut-out needs a working RH sensor (fail-safe: fan off) | DWD-CAL-001 F1 to F3 |
| Supply of parts | General suppliers for everything; the absorber sheet (R3 T6) and PTFE-coated glass-fibre mesh to confirm locally | Medium | Coating shop and mesh availability in the partner's region | BOM; DWD-DEC-001 items 9 to 12 |
| Cost | $695 against a $520 value-engineering target | Medium | Over target by $175; water about $0.87 per litre over 5 years, parts only | DWD-CAL-001 J1, J2; DWD-MKT-001 |
