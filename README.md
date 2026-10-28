# DewDrive

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Stage P3](https://img.shields.io/badge/stage-P3%20design%20outputs-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1386351481.svg)](https://zenodo.org/badge/latestdoi/1386351481) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/dewdrive/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/dewdrive/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/dewdrive/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/dewdrive)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Stage:** P3 · **Value-engineering target:** USD 520; parts USD 695 · **Difficulty:** 4 of 5

Solar-regenerated desiccant harvester that adsorbs moisture from air overnight and releases it into a passive condenser during the day.

![DewDrive: solar-regenerated desiccant water harvester, product render](media/render-hero.png)

[Exploded render](media/render-exploded.png) · [Detail render](media/render-detail.png) · [Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement DWD-DWG-001 (PDF)](cad/drawings/DWD-DWG-001.pdf) · [STEM check](docs/01b-stem-check.md) · [Concept options](docs/02a-concept-options.md) · [Requirements](docs/03-requirements.md) · [Traceability](docs/03b-traceability.md) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Prototype build plan](docs/05-build-plan.md) · [Design decisions](docs/06-design-decisions.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Cool desert nights are more humid than the days, and a salt-loaded desiccant can store that night-time moisture until the sun is strong enough to drive it out. DewDrive uses that daily rhythm directly: one glazed box that adsorbs at night and becomes a small solar still by day, with its own shaded floor as the condenser. It needs no compressor, no refrigerant and no grid, only a 2 W fan and the sun, and it keeps working at humidities where fog nets and dew condensers give nothing.

The design is open and garage-buildable on purpose. Silica gel and calcium chloride are sold as ordinary desiccants and food additives; the box is plywood, foam, polycarbonate and sheet aluminium; and the numbers behind every claim are in a script anyone can rerun. Commercial hydropanels are sealed products at about $2,000 each. An open design that a local workshop can build, repair and log lets communities and researchers compare real yields site by site.

## Burning platform

In 2022, 2.2 billion people still lacked safely managed drinking water, and 115 million collected untreated surface water from lakes, ponds, rivers and streams ([WHO, drinking-water fact sheet](https://www.who.int/news-room/fact-sheets/detail/drinking-water)). Over 2 billion people live in water-stressed countries, a pressure the WHO expects climate change and population growth to worsen in some regions (same source).

The cost falls hardest on the people who carry the water. UNICEF estimates that women and girls spend 200 million hours every day collecting it ([UNICEF, 2016](https://www.unicef.org/press-releases/unicef-collecting-water-often-colossal-waste-time-women-and-girls)). Even a supplementary half litre a day, made at the point of use, is water that nobody had to walk for.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Humanitarian and WASH programs | Supplementary drinking water at schools, clinics and camps in arid areas, with logged yields to guide deployment |
| Agriculture and pastoralism | Drinking water at remote grazing posts and farm huts far from wells |
| Education and research | An open, instrumented test bed for sorbent and collector research across climates |
| Off-grid tourism and remote stations | Water for ranger posts, weather stations and eco-lodges supplied by truck |
| Emergency preparedness | A buildable backup source where wells or delivered supplies fail in drought |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Navajo Nation, United States | About 30 % of homes lack running water, according to Navajo Nation Council Speaker Crystalyne Curley's testimony to the US Senate Committee on Indian Affairs on September 27, 2023 ([Senate Committee on Indian Affairs](https://www.indian.senate.gov/hearings/oversight-hearing-on-water-as-a-trust-resource-examining-access-in-native-communities/); [Native News Online](https://nativenewsonline.net/currents/senate-committee-on-indian-affairs-hears-30-of-navajo-nation-homes-lack-running-water)); a high-income country with households that haul water |
| Jordan | One of the most water-scarce countries in the world, with about 61 m³ of renewable water per person per year against a 500 m³ minimum ([UNICEF Jordan](https://www.unicef.org/jordan/water-sanitation-and-hygiene)) |
| Arid and semi-arid counties, Kenya | Access to safe water and basic sanitation is lowest in the arid and semi-arid land (ASAL) counties, where UNICEF focuses its water work with the government ([UNICEF Kenya](https://www.unicef.org/kenya/water-sanitation-and-hygiene)) |
| Rajasthan, India | In Thar Desert villages of northwest Rajasthan, water is scarce for up to 11 months of the year; women walk up to 4 km to fetch it, and villages store rainwater in underground taankas ([Al Jazeera, 2015](https://www.aljazeera.com/gallery/2015/11/19/women-lead-the-way-out-of-poverty-in-an-indian-desert)) |
| Atacama, Chile | In Alto Hospicio, only 1.6 % of informal settlements are connected to the water network and 75.4 % receive water by truck; researchers are assessing fog collection there as a complementary source ([Carter et al., *Frontiers in Environmental Science*, 2025](https://doi.org/10.3389/fenvs.2025.1537058)) |

## What sparked the idea

The starting point was a wartime device: the inflatable solar still that Mária Telkes developed at MIT during the Second World War for aircrews downed at sea. Seawater evaporated inside a balloon-like plastic envelope that folded into a package the size of a paper cup, and condensed again as drinkable water. The US government ordered 100,000 of them; by the summer of 1945 none had been delivered and the still was not used in the war, but solar stills later became part of military emergency kits ([USPTO, "A solar life"](https://www.uspto.gov/learning-and-resources/journeys-innovation/historical-stories/solar-life)). Telkes later patented a collapsible still, erected by inflation, as emergency equipment for the occupants of life rafts ([US Patent 3,415,719](https://patents.google.com/patent/US3415719A/en)). It showed that sunlight, a transparent envelope and a cool condensing surface can make drinkable water with no fuel at all. Telkes's still needed seawater. DewDrive asks what the same daytime still could do far from any sea, if a desiccant bed filled itself overnight from the desert air.

## Problem

Arid households without surface water or groundwater within reach depend on carried or trucked water; the air above them is an untapped supplementary source. Even desert air holds about 7 g of water per cubic metre on a 40 % RH night. Commercial solar hydropanels cost about $2,000 each and cannot be built or repaired locally. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

Problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A glazed, insulated box 1.1 x 1.0 m, tilted 20° toward the sun, holds 4 kg of silica gel impregnated with 25 wt % calcium chloride in four sealed trays, each bed covered by a black perforated absorber plate. At night the vent flaps are opened and a small solar-powered fan draws air in above the trays and down through the sorbent beds; the fan stops if the air goes above 70 % RH. By day the flaps are shut, the sun heats the absorber plates and the sorbent to about 105 °C, and the vapour passes a black drip screen, condenses on the shaded, finned floor of the box and drains into a bottle. TRL 3 calculations ([DWD-CAL-001](docs/04-calcs/01-sizing.md) v0.8) for the design decided on 2026-09-25 ([DWD-DDR-002](docs/decisions/0002-recommendations-accepted.md)), made buildable in [DWD-DDR-003](docs/decisions/0003-design-for-construction.md) and corrected by the STEM check ([DWD-DDR-005](docs/decisions/0005-stem-check-fixes.md)), give:

| Quantity | Estimate |
| --- | --- |
| Water at 40 % night RH | about 0.44 L per day, short of the 0.5 L target (decision awaiting Amish) |
| Water at 25 % night RH | about 0.31 L per day (target 0.25 L) |
| Mass | about 61 kg dry; box about 36 kg, 23 kg with the trays and deck lifted out |
| Parts cost | Estimated USD 695, USD 175 over the USD 520 value-engineering target (a hypothetical control target, not a limit) |

One unit is a supplement: about one sixth of one person's survival drinking need.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## STEM check

Twenty-seven claims on the design are checked against known physics, chemistry and biology ([DWD-STM-001](docs/01b-stem-check.md)): seventeen are within known science and ten are plausible, of which seven need a test, a log or a supplier's rating at TRL 4, so the check stays open. Five details failed and were fixed under Amish's standing instruction of 2026-10-23: the sun fell on white sorbent beads rather than a black surface, so the design would have made almost no water (now black perforated absorber plates on the beds); the tray floor passed only about a quarter of the bed area to the vapour (now a coarser mesh on thin bars); bare aluminium and a stainless mesh sat in hot calcium chloride brine (now black PTFE coatings and a PTFE-coated glass-fibre mesh); bare aluminium fins were counted as a good radiator (now painted); and the ground anchors had a 6 % margin (now 250 N). A second Claude session, given only the STEM check, the calculation note, the requirements and the sizing script, tried to refute the results and found the floor and anchor problems; what it found is in the STEM check and the review note. With the fixes the design makes about 0.44 L per day, short of its 0.5 L target, and how to recover that is a decision for Amish.

## Concept options

![Three ways to harvest water from desert air, side by side at one scale](media/options.png)

Three working principles were modelled at the same level of detail ([DWD-OPT-001](docs/02a-concept-options.md)): A, the current solar desiccant box (score 117 of 170); B, a radiative dew condenser (120); and C, a liquid-desiccant glazed still (90). A and B are within 10 %, so both go to Amish without a pick ([DWD-DDR-004](docs/decisions/0004-concept-selection.md)). Option B makes no water at 40 % night RH, because a sky-cooled panel cannot reach the 6 °C dew point; option A stays the design of record until Amish decides.

## Key components

- Silica gel and calcium chloride composite sorbent in four black, sealed trays, with air drawn through the beds at night and a black perforated absorber plate on each bed and an open floor of mesh on thin bars
- Drip screens with brine sumps under the trays
- Glazed, insulated solar box on a tilted steel stand
- Finned aluminium condenser forming the shaded floor of the box
- Night fan with a 10 W PV panel and a small LiFePO4 battery
- Humidity and temperature logging

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is [cad/src/model.py](cad/src/model.py): every option at detail level D3 (option A has 427 parts, every screw, bolt, nut, washer and rivet among them), checked by `python .kit/cad_check.py --export`, with a STEP file per part of the chosen design in `cad/step/A/` and an assembly STEP per option.

## Building the prototype

The prototype build plan ([docs/05-build-plan.md](docs/05-build-plan.md)) shows how to make each of the 31 components and put them together, with a making sketch for every made part, close-ups of the joints and a picture for every assembly step. Making the concept buildable added the parts that hold it together: battened wall panels, a lift-out tray deck that carries the drip screens, a fan hood that is now the only outlet, and a bolted, braced stand ([DWD-DDR-003](docs/decisions/0003-design-for-construction.md)). The STEM check of 2026-10-25 then added the absorber plates, the open tray floor, the PTFE coatings, the painted condenser underside and stronger anchors ([DWD-DDR-005](docs/decisions/0005-stem-check-fixes.md)). The parts now cost about USD 695, over the USD 520 value-engineering target, and the full box weighs 36.1 kg; Amish restated the portability requirement on 2026-10-02 for a lift with the trays and deck taken out (23.4 kg). Both are recorded in the [design decisions register](docs/06-design-decisions.md). It is a plan only: building and testing to it is TRL 4 work.

![DewDrive prototype: every component pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

> **Safety:** Harvested water must be tested and treated before drinking. The box interior and glazing get hot enough to burn, calcium chloride irritates eyes and skin, the small lithium iron phosphate battery must be fused, and the tilted panel must be held down with two ground anchors rated 250 N or more (or about 96 kg of ballast) against a 25 m/s gust, the design wind decided by Amish on 2026-10-25. See the safety section of the [design precis](docs/02-concept.md).

## Repository layout

```
docs/                 controlled documents (PRB, STM, OPT, PRC, URS, PRS, RTM, CAL, BLD, DEC, REG, FEA, RSK, MKT, PLN, DDR) and REVIEW.md
docs/04-calcs/        sizing.py (DWD-CAL-001) and stem_check.py (DWD-STM-001)
cad/src/model.py      parametric model of options A, B and C (kit 1.9, detail level D3); dwd_options.py and dwd_parts.py
cad/src/              sheets.py, build_plan_media.py, concept_media.py, product_model.py
cad/step/, cad/stl/   STEP per part of the chosen design and per assembly for every option; STL of the chosen design
cad/drawings/         DWD-DWG-001 general arrangement and DWD-DWG-101 to 122 making sketches
bom/bom.csv           priced bill of materials
electronics/, firmware/, build-log/   empty until TRL 4
media/                concept media and renders
.kit/                 shared documentation kit 1.9.1 (do not edit here)
```

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (DWD-PRC-001 for the precis), a version and a revision history. Run `python .kit/render.py --check` to validate them, `python docs/04-calcs/sizing.py` and then `python docs/04-calcs/stem_check.py` for the calculations, `python .kit/trace.py` for the traceability matrix and `python .kit/cad_check.py --export` for the CAD fidelity check. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `DWD-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
