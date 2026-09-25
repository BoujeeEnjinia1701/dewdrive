# Review note: DewDrive

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (DWD-PRB-001 v0.2): problem, users, operating environment, constraints, out of scope, prior work with inline sources (MOF, zeolite and salt-composite harvesters, commercial hydropanels, WHO water needs), open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (DWD-REQ-001 v0.2): a stated design point and 13 measurable requirements (R1 to R13), each with a concept status.
- `docs/02-concept.md` (DWD-PRC-001 v0.2): how it works, 13 numbered components, first-order water, heat, electrical, mass, wind and cost numbers with assumptions, eight design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the tilted glazed box (walls, glazing, four trays, sorbent bed, finned condenser floor, gutter and drain, flaps, fan), stand, bottle, PV pole, electronics box and sensor shield, each with its BOM number. It places the 1.75 m person by hand so the figure never overlaps the collector, and draws its own north-south cutaway with computed callouts and air and vapour arrows.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 13), `cutaway.png`, `flow.png` (daily water mass balance, all values labelled as estimates). Temporary `media/_views*` folders are deleted by the script.
- `bom/bom.csv`: 14 lines with indicative USD prices, numbered to match the exploded view; `bom/bom-notes.md` gives the group totals and the budget gap.
- `README.md`: hero image and links line before "## Problem"; problem, concept, key components and safety updated to match the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Water at 40 % night RH, 20 °C | about 0.49 L per day (range 0.35 to 0.6) | R1 met, no margin |
| Water at 25 % night RH | about 0.25 L per day | R2 at risk |
| Yield per aperture area | about 0.5 L/m² per day | Published devices: 0.74 to 0.77 at 60 to 68 % RH |
| Bed temperature by midday | 80 to 90 °C | R3 met by estimate |
| Heat available versus needed | about 2 kWh versus 0.5 kWh | Condenser limits yield |
| Condenser rise above ambient | about 12 K | R5 met by estimate |
| Solar-to-water efficiency | about 5 % | |
| Electrical use versus PV supply | about 24 versus 35 Wh per day | R4 met, thin margin |
| Mass | about 45 kg dry; box about 30 kg | R9 met by estimate |
| Wind uplift at 20 m/s | about 330 N | R10 needs anchors or ballast |
| Parts cost | about $475 | **R11 not met**, about 19 % over $400 |

Requirements not met or at risk:

- **R11 (cost) not met:** about $475 against $400.
- **R2 (dry-night yield) at risk:** about 0.25 L per day meets the target only at the nominal estimate; the CaCl₂ uptake below about 30 % RH is uncertain.
- **R1 has no margin:** every yield number rests on estimated sorbent isotherms that must be measured.
- **R6 (water quality) and R7 (salt containment) cannot be verified at TRL 2;** R10 (wind, UV, cycle life) is unverified.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to $500 for a research prototype with fan and logging; (b) a fanless version with natural night airflow and USB power-bank logging, about $400, lower and slower uptake; (c) cut cost elsewhere (plain plywood without foam, cheaper glazing), which costs yield. Recommendation: (a), because the logged data are the main output of the first prototype. `project.yaml` is unchanged.
2. **Problem and pitch wording.** The `project.yaml` problem ("no water source at all") implies DewDrive could be a sole supply, but one unit gives about one fifth of one person's survival drinking need. Options: keep it; or reword it to, for example, "Arid households without surface water or groundwater within reach depend on carried or trucked water; the air above them is an untapped supplementary source." Recommendation: reword, keeping the meaning. Both fields are unchanged in `project.yaml`; the README keeps the original sentence and adds context.
3. Sorbent: silica gel with about 33 wt % CaCl₂, rather than LiCl composites, zeolite or MOF.
4. Single-stage flat glazed box with the condenser as the shaded floor, rather than dual-stage or a separate condenser.
5. Fan-assisted night airflow with a 10 W PV panel and a 12.8 V LiFePO4 battery, rather than natural airflow.
6. Manual flaps, rather than automatic actuators.
7. Fixed 20° tilt facing the equator; twin-wall polycarbonate glazing rather than glass.
8. Design point: 20 °C and 40 % RH at night, 6.0 kWh/m² of sun; low-humidity case 25 % RH.
9. First partner and region for co-design, which will also supply the site climate data.

### Safety concerns

- Untreated water: possible bacteria, salt carry-over and aluminium from the condenser. The documents require testing and treatment before drinking.
- Hot surfaces: bed about 80 to 90 °C, higher at stagnation with an empty bed; the polycarbonate rating must cover it.
- Calcium chloride: eye and skin irritant, exothermic on dissolving, and a corrosive solution if the bed over-saturates.
- LiFePO4 battery: BMS, fuse at the battery, shaded mounting.
- Wind: about 330 N on the tilted panel at 20 m/s; anchors or ballast are required. Sharp fin edges at ankle and hand height.

### Problems and notes

- The kit cutaway only cuts east-west, which hid the gutter, flaps and fan, so `concept_media.py` builds a north-south cutaway with the kit's own renderer and adds callouts with the same projection.
- The CaCl₂ deliquescence point (about 30 % RH) is quoted without a source; the session's web search budget ran out. Add a source at TRL 3.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to replace the estimated isotherms with published or measured data, check the heat and mass balances and the condenser temperature by calculation, and produce the parametric model and drawing sheet.
