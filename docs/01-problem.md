---
doc_id: DWD-PRB-001
title: DewDrive problem statement
project: DewDrive
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-01'
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (budget and problem wording decided by Amish in DWD-DDR-001; yield figures from DWD-CAL-001; partner question still open)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); yield and cost figures from DWD-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# DewDrive problem statement

Arid households without surface water or groundwater within reach depend on carried or trucked water; the air above them is an untapped supplementary source. A small, open, solar-powered harvester could turn that moisture into a daily supplement of drinking water, but the physics limits it to well under a litre per square metre per day in dry air (DWD-CAL-001 v0.2 estimates about 0.57 L per day for the design decided on 2026-09-25, with night air drawn through the sorbent trays), so the realistic aim is a supplementary drinking-water source that a household or school can build and repair, not a replacement for a well or a water truck. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Where there is no river, spring or aquifer within reach, water is carried from far away, bought from vendors or trucked in, and it is often of uncertain quality. The World Health Organization puts survival needs for drinking and food at 2.5 to 3 L per person per day, and basic needs including hygiene and cooking at 7.5 to 15 L ([WHO technical note 9](https://cdn.who.int/media/docs/default-source/wash-documents/who-tn-09-how-much-water-is-needed.pdf)).

Even desert air holds water. At 20 °C and 40 % relative humidity (RH), each cubic metre carries about 7 g of vapour. Field trials in Scottsdale, Arizona, recorded night RH of about 40 % falling to 8 % by day ([Fathieh et al., *Science Advances*, 2018](https://www.science.org/doi/10.1126/sciadv.aat3198); [ScienceDaily summary](https://www.sciencedaily.com/releases/2018/06/180608200143.htm)). Cooling air below its dew point, as a fog net or a refrigeration dehumidifier does, fails at this humidity or costs too much energy. A desiccant can instead soak up vapour from cool, relatively humid night air, and the sun can drive it out again by day into a condenser.

Three gaps keep this from reaching the people who need it:

- **Cost and closed designs.** Commercial solar hydropanels produce about 3 to 5 L per day and cost about $2,000 each ([Forbes, 2022](https://www.forbes.com/sites/jeffkart/2022/01/13/solar-powered-source-hydropanels-can-produce-up-to-5-liters-of-drinking-water-per-day/)). They are sealed products that cannot be built or repaired locally.
- **Exotic sorbents.** Much of the research uses metal-organic frameworks (MOFs) or engineered zeolites that are not sold in small quantities at low cost.
- **Unclear real-world yield.** Published yields vary tenfold with humidity, sorbent and device design, so a household cannot tell whether a harvester would be worth building.

## Users and context

Table 1. Intended users (to be confirmed through co-design).

| User | Need | Context |
| --- | --- | --- |
| Rural household in an arid or semi-arid area | A daily supplement of safe drinking water, especially in the dry season | Water carried or bought; sun is plentiful; nights are cooler and more humid than days |
| School or clinic | Drinking water for children or patients when the delivered supply runs short | Some staff time for a twice-daily routine; roof or yard space |
| Local technician or maker | A design they can build from local materials and repair | Basic sheet-metal, woodwork and electronics skills |
| Researcher or NGO | Open, logged yield data across climates | Wants comparable measurements between sites |

Operating environment (proposed design envelope):

- Night air 10 to 30 °C at 25 to 70 % RH; day air 25 to 45 °C at 5 to 30 % RH.
- Clear-sky solar irradiation about 5 to 7 kWh/m² per day on a tilted surface (estimate for desert sites, to be confirmed with site data).
- Dust, wind to 20 m/s (72 km/h), ultraviolet exposure, animals and occasional rain.
- No grid power. The site may be visited only twice a day.

## Constraints

- Garage-buildable research prototype, a value-engineering target of $520 USD in parts (`project.yaml`; a hypothetical control target, not a limit; moved from $400 to $500 by Amish on 2026-09-25, DWD-DDR-001, D1, and to $520 on 2026-09-26, DWD-DDR-002, D15). The TRL 3 estimate was $515, within the target; after the design for construction it is $620, $100 over the target (DWD-DDR-003).
- Regeneration heat from the sun only. Any electricity (fan, logger) comes from the device's own small solar panel.
- Common, low-cost sorbents: silica gel and calcium chloride, both sold as desiccants and food-grade chemicals.
- Everything in contact with the water must be food-grade.
- Two people can carry and set it up without tools beyond a spanner and a screwdriver.
- Open hardware under CERN-OHL-S-2.0; software under MIT.

## Out of scope

- Providing all of a household's water. One unit is sized as a supplement (see DWD-REQ-001).
- Refrigeration or compressor-based dehumidifiers.
- MOF or other specialty sorbents in the first prototype (possible later upgrade).
- Treating the water to a certified potable standard. The design keeps the water clean in the device, but the documents require testing and treatment before drinking until tests show otherwise.

## Prior work

- **MOF harvesters.** Kim and colleagues showed solar-driven harvesting with MOF-801 at 20 % RH ([*Science*, 2017](https://doi.org/10.1126/science.aam8743)). The Arizona field trial produced about 0.2 L per kg of MOF-801 per day, and the aluminium-based MOF-303 was expected to double that at far lower material cost ([Fathieh et al., 2018](https://www.science.org/doi/10.1126/sciadv.aat3198)).
- **Dual-stage zeolite device.** LaPotin and colleagues at MIT reached about 0.77 L/m² per day outdoors with a dual-stage AQSOA Z01 device, at about 9 % thermal efficiency and absorber temperatures up to 94 °C, with overnight air at about 68 % RH ([*Joule*, 2021](https://www.sciencedirect.com/science/article/pii/S254243512030444X)).
- **Salt-in-silica composites.** Calcium chloride confined in mesoporous silica gel (SWS-1L) holds up to 0.6 to 0.7 g of water per gram ([Aristov et al., *Chemical Engineering Science*, 2006](https://www.sciencedirect.com/science/article/abs/pii/S0009250905007050)). A passive harvester with a lithium chloride and silica gel composite produced 355 g per day from 0.48 m² (about 0.74 L/m² per day), with 0.52 g/g uptake at 30 °C and 60 % RH ([Shao et al., *Energy*, 2024](https://www.sciencedirect.com/science/article/abs/pii/S0360544224016906)).
- **Salt in a polymer matrix.** An alginate-derived CaCl₂ composite took up its own weight in water at 10 mbar vapour pressure and released it at 100 to 150 °C ([Kallenberger and Fröba, *Communications Chemistry*, 2018](https://www.nature.com/articles/s42004-018-0028-9)).
- **Commercial hydropanels.** SOURCE hydropanels produce about 3 to 5 L per day per panel at about $2,000 each ([Forbes, 2022](https://www.forbes.com/sites/jeffkart/2022/01/13/solar-powered-source-hydropanels-can-produce-up-to-5-liters-of-drinking-water-per-day/)).

The gap DewDrive targets is an open, documented and locally buildable device using the low-cost composite route, with logging built in so that yield can be compared between sites.

## Open questions

- [ ] Which partner and region for co-design, and what are the real night humidity and solar figures there? (Proposed, awaiting Amish: DWD-DDR-001, O1. Portfolio rule: partners are picked per area later.)
- [ ] Is about 0.5 L per day per unit worth a household's time and money, compared with carrying or buying water? DWD-CAL-001 v0.2 puts the parts cost at about $0.49 per litre over five years.
- [ ] How will households test and treat the water, and who pays for the tests?
- [ ] Would a school or clinic, with staff on site twice a day, be a better first user than a household?

> **Safety:** Harvested water must be tested and treated before drinking. Calcium chloride is an eye and skin irritant, and the box interior runs hot enough to burn. See the safety section of DWD-PRC-001.
