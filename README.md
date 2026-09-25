# DewDrive

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $500 USD · **Difficulty:** 4 of 5

Solar-regenerated desiccant harvester that adsorbs moisture from air overnight and releases it into a passive condenser during the day.

![DewDrive concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement DWD-DWG-001 (PDF)](cad/drawings/DWD-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Arid households without surface water or groundwater within reach depend on carried or trucked water; the air above them is an untapped supplementary source. Even desert air holds about 7 g of water per cubic metre on a 40 % RH night. Commercial solar hydropanels cost about $2,000 each and cannot be built or repaired locally. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

Problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A glazed, insulated box 1.1 x 1.0 m, tilted 20° toward the sun, holds 4 kg of silica gel impregnated with calcium chloride. At night the vent flaps are opened and a small solar-powered fan draws air through the box; by day the flaps are shut, the sun heats the sorbent to about 104 °C, and the vapour condenses on the shaded, finned floor of the box and drains into a bottle. TRL 3 calculations ([DWD-CAL-001](docs/04-calcs/01-sizing.md)) show that the design as drawn falls well short of its water targets, because night air flowing past the trays leaves most of its vapour behind; drawing it through the trays is proposed as the fix:

| Quantity | Estimate |
| --- | --- |
| Water at 40 % night RH | about 0.20 L per day as drawn; about 0.53 L with through-flow (proposed) |
| Water at 25 % night RH | about 0.09 L per day as drawn; about 0.35 L with through-flow (proposed) |
| Mass | about 51 kg dry; box about 31 kg |
| Parts cost | $488 (budget $500) |

One unit is a supplement: even with the fix, about one fifth of one person's survival drinking need.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Silica gel and calcium chloride composite sorbent in four black trays
- Glazed, insulated solar box on a tilted steel stand
- Finned aluminium condenser forming the shaded floor of the box
- Night fan with a 10 W PV panel and a small LiFePO4 battery
- Humidity and temperature logging

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is [cad/src/model.py](cad/src/model.py), with STEP files in `cad/step/`.

## Safety

> **Safety:** Harvested water must be tested and treated before drinking. The box interior and glazing get hot enough to burn, calcium chloride irritates eyes and skin, the small lithium iron phosphate battery must be fused, and the tilted panel must be anchored or ballasted (about 50 kg) against wind. See the safety section of the [design precis](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (DWD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `DWD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
