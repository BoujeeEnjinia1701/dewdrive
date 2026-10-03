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

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." DewDrive now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction. The main result is unwelcome: the design as drawn does not meet its water targets.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (DWD-DDR-001 v0.1): the eight TRL 2 review items with a recommendation recorded as decided by Amish, 2026-09-25 (D1 to D8), and the items that stay open (O1, O2).
- `docs/04-calcs/01-sizing.md` (DWD-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: psychrometrics; a CaCl₂ and silica gel isotherm from the Conde (2004) solution correlation, solubility data and the SaltWiki hydrate transitions; night mass transfer as drawn (laminar flow past the trays) and for a through-flow option; a time-stepped night and day cycle with a lumped bed, Stefan diffusion to the condenser, bed-to-condenser radiation and a finned natural-convection condenser, repeated until the bed water at dawn repeats; stagnation and touch temperatures; salt containment against pore volume; electrical energy; mass from the model volumes; wind overturning and sliding; logging storage; cost. The script imports the model's `PARAMS`, `derived()` and part volumes, reads `bom/bom.csv`, prints every quoted number with a tag [A1] to [K1], and writes `docs/04-calcs/results.csv`. It runs in about 2.5 min.
- `cad/src/model.py`: parametric build123d model (stand in true 30 x 30 x 3 mm angle, walls, glazing, four trays and sorbent bed, condenser plate and 21 fins, gutter and drain, flaps, fan hood, bottle, PV pole, electronics box, sensor shield), exporting `cad/step/dewdrive-assembly.step`, `collector-box.step`, `condenser.step`, `sorbent-trays.step`, `stand.step`, `power-and-logging.step` and matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/DWD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:20, with overall, box, top-edge and low-edge dimensions computed from the model and a main-dimensions box. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays DWD-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: all 14 lines priced with a supplier type; total $488 against the new $500 budget (line 1 now includes two ground anchors).
- `cad/src/concept_media.py` now builds the media from `model.py` and takes its key figures and water flow from the calc script; all media in `media/` were regenerated and checked by eye; temporary `media/_views*` folders were deleted.
- DWD-PRB-001, DWD-PRC-001 and DWD-REQ-001 revised to v0.3 (decisions recorded, numbers replaced by DWD-CAL-001, status column from the calc); `README.md` updated to TRL 3 with the new problem line and links; `project.yaml` set to `trl: 3`, `trl_target: 3`, `budget_usd: 500`, the reworded problem line, and the evidence files listed. PDFs are in `docs/pdf/`.

### Requirements (DWD-CAL-001, Table 4)

8 met, 2 not met, 1 at risk, 2 not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| R1 | **Not met** | 0.20 L per day as drawn against 0.5 L; about 0.53 L with the proposed through-flow trays |
| R2 | **Not met** | 0.09 L per day at 25 % RH as drawn against 0.25 L; about 0.35 L with through-flow |
| R7 | At risk | At 33 wt % salt the solution fills the pores above 51 % RH; one 90 % RH night fills 46 % of them as drawn, 111 % with through-flow |
| R6 | Not verifiable at TRL 3 | Water quality needs a laboratory test |
| R10 | Not verifiable at TRL 3 | Wind: 49 kg of ballast or two 120 N anchors are needed at 20 m/s; UV life and cycling need supplier data and test |
| R3, R4, R5, R8, R9, R11, R12, R13 | Met | Bed 104 °C at noon; 23.6 Wh per day against 35 Wh, 2.6 days autonomy; condenser 13.1 K above ambient (thin margin); two actions a day; box 30.9 kg; $488; 0.41 MB of logs; glazing 53 °C and fins 48 °C |

Other key numbers: the night air flowing past the trays captures only about 11 % of the vapour driving force (NTU 0.32 over and 0.06 under the trays), so the bed swings by 0.23 kg a night although it could hold 2.03 kg; doubling the fan flow gives only 0.21 L per day. Of the 3.68 kWh the trays absorb, only 0.17 kWh desorbs water, 1.51 kWh is lost through the glazing and 1.96 kWh radiates from the beads through the mesh floors onto the condenser. Solar-to-water efficiency 2.5 % as drawn and 6.5 % with through-flow. Total mass 51.4 kg (TRL 2: 45 kg). Every TRL 2 number in the docs was checked against the script and corrected where it differed (DWD-CAL-001, Table 5).

### Decisions recorded (DWD-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 `budget_usd` raised to $500 (set in `project.yaml`; R11 redefined); D2 problem line reworded (applied to `project.yaml` and `README.md`; the pitch had no recommended change and is kept); D3 silica gel with about 33 wt % CaCl₂; D4 single-stage flat box with the condenser as its shaded floor; D5 fan-assisted airflow with a 10 W panel and a 12.8 V LiFePO4 battery; D6 manual flaps; D7 fixed 20° tilt and twin-wall polycarbonate; D8 the design point. DewDrive does not use a SwapCell pack, so the SwapCell interface v0.3 items and the shared-pack pricing rule do not affect it.

### Proposed, awaiting Amish

Status update, 2026-09-25: items 2 to 7 below are now **Decided by Amish, 2026-09-25: go with recommendation** (DWD-DDR-002, D9 to D14; see the session "recommendations accepted" below). Item 1 stays Proposed, awaiting Amish.

Still open from TRL 2 (no recommendation was made):

1. First partner and region for co-design, which also supplies the site climate data (O1). Portfolio rule: partners are picked per area later.

New from TRL 3:

2. **Night airflow through the bed (R1, R2).** Options: (a) seal the tray edges and draw the night air down through the mesh-floored trays (about 0.53 and 0.35 L per day; 0.15 Pa of extra pressure drop; a tray gasket and a baffle, a few dollars); (b) keep the flow past the trays and add bed area with more, thinner trays (less effective: even twice the transfer conductance gives 0.29 L per day); (c) accept the as-drawn yield and relax R1 and R2. Recommendation: (a).
3. **Salt loading (R7).** Lower the CaCl₂ to about 25 wt % (1.0 kg in 3.0 kg of gel): the pores then fill only above about 71 % RH, a 90 % RH night fills 82 % of them with through-flow, and the yield stays about 0.51 L per day. Recommendation: adopt together with item 2. This would amend decision D3.
4. **Humid-night protection (R7).** A drip tray under each sorbent tray, and a logger rule that stops the fan above about 70 % RH. Recommendation: adopt both; the fan rule costs nothing.
5. **Bed-to-condenser radiation.** A perforated low-emissivity aluminium screen under the trays would cut most of the 1.96 kWh a day that the beads radiate onto the condenser, lowering its temperature. Recommendation: evaluate on paper before any build; not needed to meet R5 today.
6. **Wind restraint (R10).** Two auger ground anchors are now in BOM line 1; ballast of about 50 kg is the alternative. Recommendation: confirm anchors as the default.
7. **Budget margin.** The BOM is $12 under the $500 budget. Recommendation: keep `budget_usd` at $500; items 2 to 4 add only a few dollars.

### Safety concerns

- Untreated water: possible bacteria, salt carry-over and aluminium from the condenser. The documents require testing and treatment before drinking.
- Hot surfaces: the bed reaches about 104 °C at noon and about 105 °C dry; the glazing supplier rating must exceed that. Outer glazing about 53 °C, fins about 48 °C.
- Calcium chloride: at the decided 33 wt % loading, a humid spell above 51 % RH can fill the pores and weep a corrosive brine (R7 at risk); items 3 and 4 above address it.
- LiFePO4 battery: BMS, fuse at the battery, shaded mounting.
- Wind: without restraint the unit tips at 20 m/s (overturning ratio 0.77); anchors or about 50 kg of ballast are required.

### Citations

The TRL 2 note flagged the CaCl₂ deliquescence point as unsourced. It is now sourced to [SaltWiki](https://www.saltwiki.net/index.php/Calcium_chloride) (about 30 % RH at 20 °C, and the hydrate transitions at 18.5 % and 9 % RH), with solubility from [Wikipedia](https://en.wikipedia.org/wiki/Calcium_chloride). The Conde (2004) correlation parameters for CaCl₂ solutions (*Int. J. Thermal Sciences* 43, 367 to 382) were entered from the published form but could not be checked against the paper in this session (the one web copy tried was behind a verification page); they reproduce the deliquescence point within 0.04 and should be checked against the paper before TRL 4.

### Existing TRL 4 material

None found. `build-log/README.md` is the empty scaffold and was not extended; `electronics/` and `firmware/` are empty.

### Recommended next step

Review this note and decide items 2 to 4, which decide whether DewDrive can meet its water targets at all. Those decisions can be written into the precis, model and calculation as a paper revision at TRL 3. **TRL 4 is on hold by Amish's instruction** and no TRL 4 work was started. For reference only, TRL 4 would need: measured sorption isotherms and uptake rates of the chosen composite (including the salt loading); a lab test article of one tray with through-flow; a test plan and report (TST, `environment: lab`) covering yield, condenser temperature, salt carry-over and brine containment; a laboratory water test; and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (DWD-DDR-002 v0.1). TRL stays 3 (`trl: 3`, `trl_target: 3`).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D9 | Night air drawn down through the sealed, mesh-floored trays | Air past the trays; 0.20 L/day at 40 % RH, 0.09 L at 25 % | Baffle and EPDM tray gasket; inlet flap moved above the trays (800 x 70 to 800 x 40 mm); 0.57 and 0.45 L/day |
| D10 | Salt loading 25 wt % (amends D3) | 1.3 kg CaCl₂ in 2.7 kg gel; pores fill at 51 % RH; bed 8.3 mm | 1.0 kg in 3.0 kg; pores fill at 71 % RH; bed 9.3 mm |
| D11 | Drip tray under each tray and fan stop above 70 % RH | None | New BOM line 15: four black drip screens (two staggered layers of channels, sumps 0.58 L in all); fan rule in DWD-PRC-001. R7 restated to the tray and drip-screen assembly |
| D12 | Evaluate a low-emissivity screen on paper | Not evaluated | Done: 0.82 L/day but 166 °C dry-bed stagnation; not adopted (see O4) |
| D13 | Ground anchors as the default wind restraint | Anchors or ballast | Two anchors of 114 N default; 46 kg ballast the alternative |
| D14 | Keep `budget_usd` at $500 | $500; BOM $488 | $500 unchanged; BOM $515 |

Other changes: `cad/src/model.py` (baffle, drip screens, raised inlet, bed depth), STEP and STL re-exported; drawing DWD-DWG-001 re-run at Rev P2; `docs/04-calcs/sizing.py` and DWD-CAL-001 v0.2 now model the decided design (results.csv regenerated); `bom/bom.csv` and `bom-notes.md`; DWD-PRB-001, DWD-PRC-001 and DWD-REQ-001 to v0.4; DWD-DDR-001 to v0.2 (O2 marked decided); all media regenerated from the model and checked by eye (`_views` folders removed); PDFs re-rendered; README given the concept rationale, burning platform, where-used and inspiration sections, with the concept figures updated.

Other key numbers: bed 112 °C at noon (was 104 °C), stagnation 122 °C (was 105 °C), condenser rise 12.1 K (was 13.1 K), solar-to-water efficiency 7.1 % (was 2.5 %), mass 53.9 kg and box 33.4 kg (were 51.4 and 30.9 kg), water cost $0.49 per litre over 5 years (was $1.34). If grain kinetics cut the night NTU to 1, the yield is still 0.53 L/day (C9).

### Requirement status (DWD-CAL-001 v0.2, Table 4)

10 met, 1 not met, 2 not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| R11 | **Not met** | $515 against $500 |
| R6 | Not verifiable at TRL 3 | Water quality needs a laboratory test |
| R10 | Not verifiable at TRL 3 | Two 114 N anchors or 46 kg ballast at 20 m/s; UV and cycling need supplier data and test |
| R1, R2 | Met | 0.57 L/day against 0.5; 0.45 L/day against 0.25 |
| R7 | Met on paper | Pores 43 % full after one 90 % RH night; 50 % after three with the fan rule (63 % without); sumps 0.58 L |
| R3, R4, R5, R8, R9, R12, R13 | Met | Bed 112 °C; 23.6 Wh/day against 35; 12.1 K; two actions; box 33.4 kg; 0.41 MB; glazing 57 °C, fins 47 °C |

### Still awaiting Amish

1. **O1.** First partner and region for co-design (no recommendation made).
2. **O3, budget (new). Decided by Amish, 2026-09-26: budget top-up to $520 (DWD-DDR-002 v0.2, D15).** BOM $515 against $500. Options: (a) raise `budget_usd` to $520; (b) cut the drip screens to drip gutters under the low edge of each tray (weaker protection); (c) evaluate a lighter condenser on paper, since the black screens cut its peak load from 333 W to 299 W. Recommendation: (c) first, then (a) if it does not close the gap.
3. **O4, low-emissivity screen (new).** 0.82 L/day but a 166 °C dry-bed stagnation. Recommendation: evaluate a stagnation vent or higher-rated glazing on paper at TRL 3.
4. **O5, glazing rating (new).** Dry-bed stagnation is 122 °C, near the usual 120 °C service rating of twin-wall polycarbonate. Recommendation: specify a sheet rated 130 °C or more, or confirm from supplier data that the inner skin stays inside the rating.

### Cross-repo actions

None. DewDrive has its own battery and uses no shared interface, so no decision here needs another repo to change.

### Safety concerns

- The bed now reaches about 112 °C at noon and 122 °C dry (was 104 and 105 °C); the glazing rating must be confirmed (O5). Low-emissivity screens are not to be fitted.
- Brine in the drip-screen sumps is corrosive; emptying them needs gloves and eye protection, and they must be kept apart from the water path.
- Untreated water, the LiFePO4 battery and wind loads are as before; the documents keep all safety sections.

### TRL 4

**TRL 4 remains on hold by Amish's instruction.** No build, test, purchase, PCB or firmware beyond a sketch was started. The fan rule is a design rule only; measured isotherms, a through-flow tray test article, a drip-screen chamber test and a water test remain for TRL 4.

## Session 2026-09-26: sources strengthened

Every link in the README's rationale, burning platform, use tables and inspiration was fetched and checked against its claim.

| Where | Old source | New source |
| --- | --- | --- |
| README, What sparked the idea (Telkes solar still) | Encyclopedia.com with USPTO | USPTO, "A solar life", and US Patent 3,415,719 (Google Patents). The text now says what these support: the still was ordered by the US government but not delivered or used during the war, and later entered military emergency kits; the claim that it supplied torpedoed sailors on life rafts is removed |
| README, Navajo Nation row | Native News Online alone | US Senate Committee on Indian Affairs hearing page (September 27, 2023, Speaker Curley's testimony), with Native News Online kept for the 30 % figure |
| README, Kenya row (was "Northern Kenya and the Horn of Africa", uncited) | none | UNICEF Kenya; row rewritten to what UNICEF states: access is lowest in the arid and semi-arid land counties |
| README, Rajasthan row (uncited) | none | Al Jazeera (2015): Thar Desert villages, water scarce up to 11 months a year, walks of up to 4 km, taanka rainwater storage |
| README, Atacama row (uncited) | none | Carter et al., *Frontiers in Environmental Science* (2025), doi:10.3389/fenvs.2025.1537058: Alto Hospicio, 1.6 % of informal settlements connected to the network, 75.4 % supplied by truck, fog collection assessed |

`INSPIRATIONS.md` line for DewDrive updated to the new sources (same event). `docs/01-problem.md` did not cite the replaced sources.

### Budget top-up

Budget top-up to $520: decided by Amish, 2026-09-26 ("I am ok with the budget top ups"). This closes O3.

- `project.yaml`: `budget_usd` 500 to 520.
- DWD-REQ-001 v0.5: R11 target $520 or less; status Met at $515 (11 of 13 met, R6 and R10 not verifiable at TRL 3).
- DWD-CAL-001 v0.3: `sizing.py` budget updated and re-run; only R11 changed in `results.csv` (now met).
- DWD-DDR-002 v0.2: new row D15; O3 marked decided.
- DWD-PRB-001 v0.5 and DWD-PRC-001 v0.5: budget text updated; `bom/bom-notes.md` and README (budget line, parts cost row) updated; concept blueprint label changed to "budget $520" and media regenerated.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

- `cad/src/product_model.py` (new): a product appearance model for photoreal renders. `product_parts()` returns each part with its shape, colour, material, BOM line, group and explode offset; `TITLE` and `RENDER_VIEWS` (hero, exploded and a back-right detail view) drive the renderer. It imports `PARAMS`, `derived()`, `tray_centres()`, `world()` and `build_parts()` from `cad/src/model.py`, and reuses the stand, drip screens, condenser and sorbent bed unchanged. It adds:
  - painted plywood walls with filleted corners and a shadow-gap parting line, and a teal nameplate on the south wall;
  - an aluminium lid edge frame holding a clear twin-wall polycarbonate pane (ribs down the slope), so the black trays and the sorbent beds show through; three lid hinges on the north edge and a pull handle on the south edge;
  - wire lift bails on the four trays and the sealing baffle and rails as a separate aluminium part;
  - the gutter, a silicone drain tube with a wall grommet, and a 10 L jerrycan with moulded side ribs, a carry handle, a knurled teal cap and a label;
  - the south inlet flap with its EPDM seal, a five-knuckle hinge and two over-centre latches; the louvred fan hood (open underneath) with a fan guard, and the north outlet flap with its hinge;
  - bolts on the stand foot pads, two auger ground anchors with webbing tie straps and ratchets;
  - a framed PV panel with cells, busbars and a junction box, pole clamps on the leg;
  - an IP65 electronics box with a lid, lid screws, a label, cable glands, a lit green status light and a bracket to the leg, a sheathed cable up the leg, and a stacked-plate radiation shield with a domed cap;
  - context: a compact patch of compacted gravel ground, not in the BOM.
- `README.md`: hero image line now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced separately by the render pipeline.
- Self-check previews (matplotlib, clear parts omitted) were used to set the views; they are scratch files and not in the repo.

### Where the appearance model differs from model.py

Every main dimension, the tilt, the heights and all interfaces are as `model.py`. The differences are cosmetic; each is **Proposed, awaiting Amish**:

1. **Ground anchor position and tie-down.** `model.py` does not model the two auger anchors that BOM line 1 includes. The appearance model places them 190 mm outboard of the two south legs, tied to the legs with webbing straps. Recommendation: accept for the renders; the anchor position and tie-down detail belong to the wind-load check at TRL 4 (DWD-CAL-001, H2 to H4).
2. **Electronics box orientation.** The appearance model puts the lid, label and status light on the north face, outward from the stand, so they can be reached without reaching under the box. Recommendation: accept.
3. **Radiation shield.** Drawn as seven stacked plates with a domed cap on a post; its top is about 30 mm higher than the 110 mm cylinder in `model.py`, and the top plate is 96 mm across instead of 90 mm. Recommendation: accept; the shield is a bought part and its size depends on the product chosen.
4. **Jerrycan handle and neck.** The moulded carry handle adds about 48 mm above the can top, beside the cap at the `model.py` position. Recommendation: accept; the drain tube end and cap position are unchanged.
5. **Rounded corners and lid frame.** The box corners are filleted (radius 14 mm) and the glazing sits in a 22 mm aluminium edge frame within the same 1,100 x 1,000 mm outline, as BOM line 3 describes. Recommendation: accept.

### TRL

This is an appearance model only: no tolerances, no fabrication detail, no build or test work. `trl` stays 3, and **TRL 4 remains on hold** by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, constructable design and prototype build plan

Done under the build plan rollout (kit 1.7.0) and Amish's instruction of 2026-09-30 to make the design physically buildable while drawing the build plan. TRL stays 3; nothing was built, bought or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten from a massing model to a constructable one: every made or bought piece is its own component with its material, and `python cad/src/model.py --check` runs 91 constructability checks (contacts, overlaps, clearances); all 91 pass. `build_parts()` keeps the old BOM groups, plus a new group for line 16.
- New decision record `docs/decisions/0003-design-for-construction.md` (DWD-DDR-003, draft, open for Amish's review).
- New build plan `docs/05-build-plan.md` (DWD-BLD-001) with pictures from `cad/src/build_plan_media.py`: an overview, 22 making sketches (`cad/drawings/DWD-DWG-101` to `122`), 14 joint close-ups, 19 assembly steps, a plate hole layout and a wiring diagram, all in `docs/05-build-plan/`.
- New design decisions register `docs/06-design-decisions.md` (DWD-DEC-001).
- `bom/bom.csv`: lines repriced and line 16 (tray deck and wall ledges) added; $620 in all.
- `docs/04-calcs/sizing.py` re-run on the new model (DWD-CAL-001 v0.4): mass by component and material, outlet slot in the fan duty, new leg span in the wind check.
- DWD-REQ-001 v0.6, DWD-PRC-001 v0.6, README (links line, "Building the prototype", key numbers), `project.yaml` (`design_state: constructable`, new evidence) updated.
- STEP and STL re-exported, general arrangement DWD-DWG-001 at Rev P4, concept media regenerated from the new model; PDFs of the changed documents re-rendered.

### Design changes made for construction (DWD-DDR-003)

1. Condenser plate under the walls, closing the box; walls start 5 mm higher and are 133 mm tall so every height and gap in the calculation is kept (the concept plate overlapped the walls by 240 cm³).
2. Walls as battened sandwich panels, screwed at the corners, with framed openings and threaded inserts for the stand.
3. A lift-out tray deck (20 x 5 mm flat bar frame, baffle riveted on top, EPDM edge seal) on two wall ledges, in place of a loose 1 mm baffle on unfixed rails.
4. Drip screens framed and hung from the deck bars by their sump and end plate (they floated 7 mm below the trays); sumps moved under the channel ends.
5. Fins with a 10 mm folded foot, bonded and riveted with closed-end rivets.
6. A folded L gutter in the low corner and a bulkhead drain fitting down through the floor between two fins (the concept gutter could not take water in).
7. One outlet: a slot under the deck into a fan hood, with the outlet flap over the fan. The concept's separate outlet flap would have let the fan draw air past the beds, and a 120 mm fan did not fit under the trays.
8. Inlet opening lowered 20 mm (same 800 x 40 mm, still above the deck) so the wall keeps a solid top edge.
9. Lid sheet in an aluminium U-channel frame with hinges, latches and a seal.
10. Stand redesigned: rails under the box edges bolted into the wall inserts, legs bolted to the rails, side braces, cross members, a south diagonal, foot plates with cleats (the concept stand ran through the box).
11. PV pole as a square tube on spacers on the north-east leg, 6 mm clear of the box (the concept pole passed through the box).
12. Electronics box and sensor shield on a backing plate on the north-west leg.
13. Trays as folded 1 mm pans with a perforated floor under the mesh.

### Key results (DWD-CAL-001 v0.4)

- Water, heat, salt and electrical results unchanged: 0.57 and 0.45 L per day, bed 112 °C at noon, condenser rise 12.1 K, pores fill at 71 % RH.
- **R11 over the value-engineering target:** parts an estimated $620 against a $520 target ($100 over).
- **R9 not met as written:** full box 35.2 kg against 35 kg; 23.4 kg with the trays, sorbent, deck and screens lifted out. Total 60.2 kg.
- Wind: two anchors of 98 N, or 40 kg of ballast. Fan duty about 3.3 Pa.
- Requirement count: 9 met, 1 not met (R9), 1 over its value-engineering target (R11), 2 not verifiable at TRL 3 (R6, R10).

### Proposed, awaiting Amish

All open decisions are in the design decisions register (`docs/06-design-decisions.md`): review of DDR-003; restating R9 for a lift with the trays and deck out; the glazing rating (O5); the low-emissivity screen (O4); the co-design partner (O1); and the appearance model deviations.

### Stale on Amish's Mac

The photoreal renders (`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`), `media/card.png` and `media/social-preview.png`, and the appearance model `cad/src/product_model.py`, still show the concept stand, lid frame, outlet flap and PV pole; they need regenerating after the appearance model is brought into line with `model.py`.

### Safety concerns

- Sorbent preparation (calcium chloride dissolving hot, corrosive brine) now has written steps and stops (build plan S1, S2, S7).
- The glazing rating (122 °C stagnation) must be confirmed before the lid is first closed in sun (S3).
- Mass rose by 6 kg; the build plan lifts the box onto the stand with the trays and deck out, two people, after the anchors are in (S4).

### Recommended next step

Amish to review DDR-003 and decide the R9 item in the register; its Value engineering section has the cost drivers. TRL 4 remains on hold; when released, the build plan is ready to build from.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." trl stays 3; nothing was built or tested.

### Decisions recorded

6 decisions recorded in the design decisions register (DWD-DEC-001, Decisions made, dated 2026-10-02): DWD-DDR-003 accepted as made (1); R9 restated for a lift with the trays and deck taken out, with an empty-before-lifting label (2); glazing rated 130 °C or more (3); a short paper study of a passive stagnation vent, else drop the low-emissivity screens (4); first partner type and region (5), the first candidate to approach and not an agreed partner; appearance deviations accepted and renders to be updated (6).

### Documents changed

- `docs/06-design-decisions.md` (DWD-DEC-001 v0.3): all 6 open items moved to Decisions made; Open decisions now reads "None"; item 2 of "To confirm when parts are bought" updated for the glazing rating.
- `docs/decisions/0003-design-for-construction.md` (DWD-DDR-003 v0.3): status line records acceptance of Tables 1 and 2 and of A2; status stays Draft.
- `docs/decisions/0002-recommendations-accepted.md` (DWD-DDR-002 v0.3): O1, O4 and O5 recorded as decided.
- `docs/decisions/0001-trl2-review-decisions.md` (DWD-DDR-001 v0.3): O1 recorded as decided.
- `docs/01-problem.md` (DWD-PRB-001 v0.7): partner and region named as the first candidate type to approach.
- `docs/03-requirements.md` (DWD-REQ-001 v0.8): R9 restated and met; count of requirements met updated.
- `docs/04-calcs/01-sizing.md` (DWD-CAL-001 v0.6): R9 row and counts for the restated R9; glazing rating decision noted in section D; no computed number changed.
- `docs/02-concept.md` (DWD-PRC-001 v0.8): glazing rating, low-emissivity study, R9, lifting rule and partner from the 2026-10-02 decisions.
- `docs/05-build-plan.md` (DWD-BLD-001 v0.3): glazing rated 130 °C or more (sections 3.9 and 3.19, stop S3); lifting label in step 16 and stop S4.
- `bom/bom-notes.md`: glazing rating and lifting label noted; BOM changes are follow-ups.
- `README.md`: the portability and cost sentence of "Building the prototype".
- PDFs re-rendered with `python .kit/render.py`; superseded versions removed.

No CAD model, BOM quantity or price, or picture was changed. Requirement status: R9 is now met as restated, so 10 met, 1 over its value-engineering target (R11, $620 against $520), 2 not verifiable at TRL 3 (R6, R10).

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (bom): Add an "Empty before lifting" label to the BOM (a line or within line 3 or the box line) and show it in the step 16 picture.
2. Decision 2 (calcs): Re-run `docs/04-calcs/sizing.py` with R9 as restated so `results.csv` and the counts [K1] report R9 met.
3. Decision 3 (bom): Change the BOM line 3 specification to twin-wall polycarbonate rated 130 °C or more (price to be checked; a higher-rated sheet may cost more).
4. Decision 4 (calcs): Write the short paper study of a passive stagnation vent in DWD-CAL-001; if it cannot hold a dry bed near 122 °C at a modest cost, record that the low-emissivity screens are dropped.
5. Decision 6 (pictures): Update the appearance model `cad/src/product_model.py` to the constructable design (stand, lid, no outlet flap) with the five accepted deviations, and regenerate the photoreal renders, `media/card.png` and `media/social-preview.png` on Amish's Mac.

### Points found in the review

- The constructable design is USD 620 against the USD 520 value-engineering target (19 % over), and the savings listed still leave it over.
- Renders still show the concept stand, lid and the outlet flap that P7 removed.

### Safety

The glazing must now be rated 130 °C or more, against a dry-bed stagnation near 122 °C; a 120 °C sheet is allowed only with supplier data and a measured inner-skin temperature. The box must be emptied of its trays and deck before any lift. Low-emissivity screens stay out of the prototype.

### Recommended next step

Carry out the follow-up actions above, starting with the BOM line 3 glazing specification and the stagnation vent study. TRL 4 remains on hold by Amish's instruction.

## Approved follow-ups carried out (2026-10-02)

Amish approved all follow-up actions from the 2026-10-02 sign-off. trl stays 3; no build or test work was done.

### Follow-ups

1. Decision 2 (BOM and picture): done. The "Empty before lifting" label is bill of materials line 14 (about $2, estimate), modelled as a 0.5 mm plate on the east wall in `cad/src/model.py` (two new constructability checks; 93 checks in all, all passing), and drawn yellow in the step 16 picture. The step 16 text in the build plan now says where it goes.
2. Decision 2 (calculations): done. `docs/04-calcs/sizing.py` now tests R9 on the box lifted with the trays and deck out (23.4 kg, met); it was re-run and `results.csv` and the counts [K1] agree: 10 met, 1 not met (R11), 2 not verifiable at TRL 3.
3. Decision 3 (BOM): done. Line 3 now specifies twin-wall polycarbonate rated 130 °C or more, priced at about $48 per square metre (an estimate, about 50 % above a standard sheet, no supplier quote), so line 3 rises from $65 to $82. A quote is still needed.
4. Decision 4 (calculations): done. The study is in DWD-CAL-001 section D (D4, D5): about 117 cm² of stack-effect vent would hold a low-emissivity dry bed at 122 °C, but it would have to stay shut in normal operation (bed 130 to 149 °C), so it needs a thermostat and is not a passive, modest-cost fix. The low-emissivity screens are dropped; the black screens stay (recorded in DWD-DEC-001 v0.4).
5. Decision 6 (appearance model and pictures): done in part. `cad/src/product_model.py` now takes the lid frame and hinges, latches, deck and ledges, gutter and drain, inlet flap hardware, outlet flap, stand, PV pole and bracket, backing plate and bolts from the model, moves the electronics box and shield to the backing plate, and adds the label. Render scenes were exported to `/home/claude/renders/dewdrive` (hero, exploded, detail, and the jobs file). Not done: the photoreal renders, `media/card.png` and `media/social-preview.png`, which are made on Amish's Mac.

### Key results

- Cost: USD 639 against the USD 520 value-engineering target (USD 119 over); USD 620 before these follow-ups (USD 17 for the 130 °C glazing sheet, USD 2 for the label). `budget_usd` is unchanged.
- Mass: 60.2 kg total, box 35.2 kg, 23.4 kg lifted with the trays and deck out; unchanged.
- Requirement status changes: R9 now reads met in `results.csv` (it was not met under the first wording; the written status already read met after the restatement). R11 stays over its target, by USD 119 (was USD 100).

### Documents changed

- `docs/04-calcs/01-sizing.md` (DWD-CAL-001 v0.7), `docs/03-requirements.md` (DWD-REQ-001 v0.9), `docs/02-concept.md` (DWD-PRC-001 v0.9), `docs/05-build-plan.md` (DWD-BLD-001 v0.4), `docs/06-design-decisions.md` (DWD-DEC-001 v0.4), `docs/decisions/0003-design-for-construction.md` (DWD-DDR-003 v0.4), `bom/bom.csv`, `bom/bom-notes.md`, `README.md`.
- `cad/src/model.py` (label), STEP and STL re-exported; `cad/src/sheets.py` and `cad/drawings/DWD-DWG-001` at Rev P5; concept media regenerated; build step 16 picture regenerated; `docs/04-calcs/results.csv` regenerated.
- PDFs re-rendered with `python3 .kit/render.py`.

### Cross-repo actions

None.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
