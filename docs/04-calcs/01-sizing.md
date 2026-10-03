---
doc_id: DWD-CAL-001
title: DewDrive sizing calculations
project: DewDrive
doc_type: Calculation
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (sorbent isotherm, night adsorption, day desorption and condenser, cyclic yield, stagnation and touch temperatures, salt containment, electrical energy, mass, wind, logging, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); design of record now through-flow with 25 wt % salt, drip screens and fan cut-out; paper evaluation of a low-emissivity screen
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish (budget $520; R11 met); script re-run
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Re-run on the constructable model (DWD-DDR-003); mass by component and material, outlet slot in the fan duty, new leg span in the wind check, repriced BOM; R9 and R11 not met
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: R9 row and counts follow the restated R9; glazing rating decision noted in section D (DWD-DEC-001, items 2 and 3); no computed number changed
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: Script re-run with R9 as restated (computed counts now agree); paper study of a passive stagnation vent (D4, D5); BOM line 3 repriced for a 130 °C sheet and label added; cost USD 639 against the USD 520 target
---

# DewDrive sizing calculations

This revision checks the design decided by Amish on 2026-09-25 (DWD-DDR-002): night air drawn down through the sealed, mesh-floored trays; 25 wt % CaCl₂ (1.0 kg in 3.0 kg of gel); a black drip screen under each tray; and a fan that stops above 70 % RH. On paper that design, as made constructable in DWD-DDR-003, meets ten of its thirteen requirements. It collects about 0.57 L per day at 40 % night RH (R1 target 0.5 L) and 0.45 L at 25 % (R2 target 0.25 L), against 0.20 and 0.09 L for the v0.1 layout. The salt stays in the pores after three 90 % RH nights in a row. Making the design buildable added the parts that hold it together (wall battens, a tray deck, screen frames, stand bracing and fixings): the estimated parts cost is now $639 against the $520 value-engineering target (R11 over the target by $119) and the full box weighs 35.2 kg against the 35 kg two-person limit, 23.4 kg once the trays and deck are lifted out (R9 was not met as first written; Amish restated it on 2026-10-02 for a lift with the trays and deck out, and it is met). The design decisions register (DWD-DEC-001) lists cost drivers and savings for R11. A low-emissivity screen, evaluated here as decided, would lift the yield to 0.82 L per day but let a dry bed stagnate at about 166 °C, beyond the usual rating of polycarbonate glazing, so it is not adopted; the paper study of a passive vent in section D finds no passive remedy and the screens are dropped. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B2], is the line of that script's output that carries it.

> **Safety:** These calculations concern hot surfaces (a bed up to about 122 °C), a corrosive calcium chloride solution, a lithium iron phosphate battery and a 1.1 m² panel in wind. They are first-principles estimates for a paper proof of concept, not a substitute for measured isotherms, supplier data, an engineering review or test. Harvested water must be tested and treated before drinking. See DWD-PRC-001, Safety.

## Scope and method

The note checks every requirement in DWD-REQ-001 v0.5 against the design in DWD-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and components (`build_components()`, each with its material), so the areas, gaps and masses used here are those of the STEP files and of drawing DWD-DWG-001 Rev P4. It reads prices from `bom/bom.csv` and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 6 min; the yield is a time-stepped simulation of repeated night and day cycles until the bed water at dawn repeats).

"Design" means the design of record after DWD-DDR-002. "v0.1 layout" is the earlier design, in which the night air flowed past the trays at 32.5 wt % salt; its figures are kept for comparison and come from v0.1 of this note unless tagged.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Design point | Night 10 h at 20 °C and 40 % RH (low-humidity case 25 %); day air 35 °C; 6.0 kWh/m² per day on the tilted aperture, as a sine from 06:00 to 18:00; flaps shut at 07:00 and opened at 19:00, bed back at air temperature when the fan starts | DWD-REQ-001 |
| Psychrometrics | IAPWS-IF97 saturation pressure; vapour diffusivity 2.5 x 10⁻⁵ m²/s at 20 °C, scaled with T^1.75 | Standard |
| Salt solution | Water activity of aqueous CaCl₂ from the Conde (2004) correlation; solubility 74.5 g/100 g water at 20 °C, 81.1 at 25 °C, 134.5 at 60 °C and 152.4 at 100 °C | Conde, *Int. J. Thermal Sciences* 43, 2004; [Wikipedia](https://en.wikipedia.org/wiki/Calcium_chloride) |
| Salt hydrates | Below deliquescence at night: hexahydrate above 18.5 % RH, tetrahydrate from 9 % to 18.5 %; above 29.9 °C the solid is taken as the dihydrate | [SaltWiki, calcium chloride](https://www.saltwiki.net/index.php/Calcium_chloride) (transitions at 20 °C) |
| Composite | 3.0 kg mesoporous silica gel, 1.0 cm³/g pore volume, skeleton 2,200 kg/m³, packing 0.60; 1.0 kg CaCl₂ (25 wt %, DWD-DDR-002 D10); the gel walls add 0.08 kg/kg per unit water activity; no pore confinement effect on the salt | Typical wide-pore gel; engineering judgment |
| Heat of sorption | Clausius-Clapeyron on the isotherm at constant bed water, not less than the latent heat | First principles |
| Night mass transfer, design | Air drawn down through the bed: packed-bed Wakao correlation for 3.5 mm beads; diffusion inside the grains not modelled (see C9) | Standard; grain kinetics must be measured |
| Night mass transfer, v0.1 layout | Air splits between the 45 mm gap over the trays and the 65 mm gap under them in proportion to gap cubed (laminar); Nu 4.86 plus a developing-flow term; Lewis analogy; diffusion into the bed with porosity 0.40 and tortuosity 1.5; mesh floor 60 % open | Standard laminar-channel results |
| Fan cut-out | Fan stops above 70 % RH; natural airflow through the open flaps then taken as 4 m³/h, 10 % of the fan flow | Assumption; to check by test |
| Day, bed | Lumped bed: sorbent, four 0.6 kg aluminium trays and the water; transmittance-absorptance 0.74 on the black tray tops; loss to ambient 3.2 W/(m²·K) through the gap and twin-wall glazing | Twin-wall polycarbonate U value about 3 W/(m²·K) |
| Day, vapour path | Stefan diffusion through still air across the 65 mm gap to the condenser (hot above cold is stably stratified); 60 % of the bed area effective through the mesh. The drip screen (two 18 mm deep layers of channels, one third open) adds 18 mm x (1.5 / 0.33 − 1), giving an equivalent path of 128 mm | First principles; geometry from the model |
| Day, parasitic heat | Radiation from bed to condenser: beads (emissivity 0.9) seen through 60 % open mesh, bare aluminium 0.1 elsewhere, plate 0.9; the drip screen blocks every line of sight and acts as a radiation shield with emissivity 0.90 on both faces (black paint), or 0.15 for the low-emissivity option; conduction across the gap; sun through the gaps between trays onto the plate, absorptance 0.5 | Engineering judgment |
| Condenser | 2 mm aluminium plate and 21 fins, 1 x 100 x 920 mm; laminar natural convection on vertical fins; radiation from the fin envelope to shaded ground at ambient; aluminium 205 W/(m·K) | Model; standard correlations |
| Collection | 30 g per day left as drops and films on the plate and gutter | Engineering judgment |
| Electrical | Fan 2 W for 10 h; logger 0.15 W average; 10 W panel, 5 peak sun hours, 0.70 derating; 12.8 V 6 Ah battery, 80 % usable | DWD-PRC-001 |
| Wind | 20 m/s; force coefficient 1.2 on 1.1 m² normal to the lid; centre of pressure a quarter chord upwind of the centre; friction 0.5; factor of safety 1.5 | Engineering judgment |

## A. Air and sorbent

At 20 °C the night air carries 6.92 g/m³ of vapour at 40 % RH and 4.32 g/m³ at 25 % RH [A1]. The Conde correlation puts the deliquescence point of CaCl₂ at 20 °C at a water activity of 0.341, against about 0.30 quoted by SaltWiki [A2]; the difference only matters between 30 and 34 % RH. At 40 % RH the salt is a 40.1 wt % solution holding 1.49 kg of water per kg of salt; at 25 % RH it is the hexahydrate, holding 0.974 kg/kg [A3].

With 1.0 kg of salt the whole bed would hold 1.59 kg of water at equilibrium at 40 % RH (0.397 g/g) and 1.03 kg at 25 % RH (0.258 g/g) [A4], less than the 2.03 and 1.32 kg of the v0.1 loading but still well above what a night delivers. The 3.0 kg of gel has 3.00 L of pore volume; the bed is 7.27 L of beads, 9.3 mm deep on 0.785 m² of tray floor, which matches the model [A5].

## B. Night adsorption

The fan moves 40 m³/h, so 2.77 kg of vapour passes through the box in a night at 40 % RH, and 1.73 kg at 25 % RH [B4].

**Design: air drawn through the bed.** The superficial velocity through the bed is 14.2 mm/s and the gas-side number of transfer units is 19, so the air leaves close to equilibrium with the bed; the bed adds only 0.16 Pa of pressure drop [B3]. In the repeating cycle the bed takes up 0.60 kg a night at 40 % RH (a swing of 0.151 g/g), from 0.63 kg at dusk to 1.23 kg at dawn, still below the 1.59 kg equilibrium; the heat of adsorption warms it to 26.9 °C [B5]. At 25 % RH it takes up 0.48 kg [B6]. The night is no longer the limit: the uptake is set by how dry the day leaves the bed.

**v0.1 layout, for reference.** Air flowing past the trays splits 25 % over and 75 % under them, stays laminar, and reaches NTU 0.31 and 0.06, capturing at most 11 % of the vapour driving force [B1, B2]. That is why v0.1 took up only 0.23 kg a night.

## C. Day desorption, condenser and yield

The aperture receives 6.00 kWh/m² per day, of which 4.24 kWh/m² falls between 09:00 and 15:00; the peak is 785 W/m² [C1].

Table 2 traces the design point. The bed passes 89 °C by 09:00 and reaches 112 °C at noon [C2]. Vapour moves from about 08:30 to 16:00, peaking at about 120 g/h. By late afternoon the salt has dried towards the dihydrate and desorption stops.

*Table 2. Day at the design point (script output, section C).*

| Hour | Sun (W/m²) | Bed (°C) | Condenser (°C) | Bed water activity | Desorption (g/h) | Bed water (kg) |
| --- | --- | --- | --- | --- | --- | --- |
| 07:00 | 203 | 25.0 | 34.2 | 0.312 | 0 | 1.23 |
| 09:00 | 555 | 89.1 | 42.7 | 0.359 | 51 | 1.20 |
| 11:00 | 759 | 108.2 | 46.7 | 0.312 | 121 | 1.02 |
| 12:00 | 785 | 112.4 | 47.1 | 0.269 | 119 | 0.89 |
| 13:00 | 759 | 113.4 | 46.8 | 0.228 | 97 | 0.79 |
| 15:00 | 555 | 102.3 | 43.9 | 0.184 | 37 | 0.65 |
| 17:00 | 203 | 71.2 | 39.2 | 0.168 | 0 | 0.63 |

*Table 3. Yield and energy.*

| Quantity | Design (black screens) | No screens | Low-emissivity screens | v0.1 layout | Tag |
| --- | --- | --- | --- | --- | --- |
| Collected at 40 % night RH | 0.57 L per day | 0.51 L per day | 0.82 L per day | 0.20 L per day | C3, C6, C10 |
| Collected at 25 % night RH | 0.45 L per day | | 0.54 L per day | 0.09 L per day | C4, C10 |
| Bed at noon; peak | 112 °C; 114 °C | peak 101 °C | 130 °C; 149 °C | 104 °C | C2, C6, C10 |
| Condenser rise above ambient, peak | 12.1 K | 13.3 K | 10.5 K | 13.1 K | C2, C6, C10 |
| Condenser load, peak | 299 W | 333 W | 252 W | 328 W | C2, C6, C10 |
| Stagnation, dry bed | 122 °C | 105 °C | 166 °C | 105 °C | D1 |
| Solar-to-water efficiency | 7.1 % | | 10.1 % | 2.5 % | C7 |

The "no screens" column is the through-flow design at 25 wt % without drip screens. The effective emissivity from the bed underside to the condenser is 0.545 with no screen, 0.327 with black screens and 0.071 with low-emissivity screens; the screens double the equivalent vapour path, from 65 to 128 mm [C5].

The energy balance shows where the sun goes in the design at 40 % RH [C7]: 5.54 kWh falls on the inner aperture; the black trays absorb 3.68 kWh; 0.44 kWh drives desorption; 1.69 kWh is lost back through the glazing; and 1.47 kWh passes from the hot bed to the condenser (0.68 kWh with low-emissivity screens).

The condenser has 3.86 m² of fins with a natural-convection coefficient of 4.7 W/(m²·K) and a fin efficiency of 0.87, giving 24.6 W/K at a 12 K rise [C8]. It holds the peak rise to 12.1 K, inside R5.

**Item 5 evaluation (DWD-DDR-002, D12).** A radiation screen under the trays does what the TRL 3 review expected: the less heat the bed sheds to the condenser, the hotter and drier it gets by day, and the cooler the condenser stays. The black drip screens needed for D11 already give part of this effect (0.51 to 0.57 L per day, even though they double the vapour path). A low-emissivity screen gives much more (0.82 L per day, 10.1 % efficiency), but with an empty or dry bed the trays would stagnate near 166 °C, well above the roughly 120 °C service rating usual for twin-wall polycarbonate. Adopting it would need a stagnation vent or a glazing rated for that temperature. That is proposed as a new item (O4), not adopted.

**Sensitivity.** Diffusion inside the grains is not modelled. If it cut the effective night NTU from 19 to 2 or to 1, the design would still collect 0.56 or 0.53 L per day [C9], so R1 holds with little margin in the worst case.

## D. Stagnation and touch temperatures

With a dry bed at noon on a 35 °C day, the bed stagnates near 122 °C with black drip screens, 105 °C with no screens and 166 °C with low-emissivity screens [D1]. The glazing inner skin runs cooler than the bed, but the supplier rating of the polycarbonate must be checked against this. Amish decided on 2026-10-02 (DWD-DEC-001, item 3) to specify a sheet rated 130 °C or more, or a 120 °C sheet only if the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating. The outer skin of the glazing reaches about 57 °C at stagnation [D2], and the condenser fins, at ankle and hand height, up to 47 °C [D3]. Both are under the 60 °C limit of R13, but the inside of the box is not: the bed and trays are hot enough to burn.

*Passive stagnation vent study (decided on 2026-10-02, DWD-DEC-001, item 4).* The low-emissivity screens would raise the dry-bed stagnation temperature to 166 °C. A vent at the high north edge of the box, with its inlet low on the south side 100 mm below, would let hot gap air leave by stack effect. Taking the gap air at the mean of bed and ambient temperature, a discharge coefficient of 0.6 and the same heat balance as D1, holding the dry bed at 122 °C needs about 117 cm² of opening, about a 15 mm tall slot along the 800 mm inlet width; the same vent would bring the black screens to 103 °C [D4]. The vent would have to stay shut in normal operation, because with low-emissivity screens the bed already reaches 130 °C at noon and 149 °C at its peak, above the 122 °C it must hold, and any open vent would let water vapour escape that the condenser should collect [D5]. A passive flap therefore cannot do the job; it would need a thermostat that tells a dry bed from a working one, which is an active part with its own cost (a wax actuator, flap and seal, about $20 as an estimate) on top of a design that is already over its cost target, and the benefit has not been shown beyond the paper gain in yield (0.82 L per day against 0.57 L per day at 40 % RH, C10). The study therefore concludes that the vent cannot hold a dry bed near 122 °C passively at a modest cost, and the low-emissivity screens are dropped, as the 2026-10-02 decision provides. The first prototype keeps the black screens.

## E. Salt containment

A calcium chloride solution stays in the beads only while its volume is less than the pore volume. At equilibrium at 40 % RH the solution fills 58 % of the 3.00 L of pores; at 90 % RH it would be 6.35 L, twice the pore volume [E1]. At 25 wt % the pores fill at 71 % RH at 20 °C, against 51 % RH at the v0.1 loading of 32.5 wt % (81 % RH at 20 wt %) [E2].

Kinetics limit what one humid night can do. A 10 h night at 90 % RH with the fan running, from the normal dusk state, takes the bed to 43 % of its pore volume [E3]. Three such nights in a row with overcast days between them, the worst case for a wet spell, fill 43, 54 and 63 % of the pores with the fan left running [E4], and 37, 44 and 50 % with the fan stopped above 70 % RH [E5]. No brine leaves the beads in either case, and the four drip-screen sumps (0.58 L) remain as a backstop [E6]. R7 is met on paper; a chamber test at TRL 4 must confirm it.

## F. Electrical energy

The fan uses 20 Wh a night and the logger 3.6 Wh a day, 23.6 Wh in all, against 35 Wh a day from the 10 W panel, a margin of 1.48 [F1]. The 76.8 Wh battery, 80 % usable, gives 2.6 days with no sun [F2]. The fan works against only about 3.3 Pa: the 800 x 40 mm inlet above the deck, the 140 x 44 mm outlet slot behind the fan hood (DWD-DDR-003) and 0.16 Pa for the bed, so a 120 mm fan delivers 40 m³/h at low speed [F3]. The humidity cut-out only ever lowers the fan energy.

## G. Mass

v0.4 takes each component of the constructable model (DWD-DDR-003) with its own material: plywood skins at 0.60 g/cm³, softwood battens at 0.45, PIR at 0.035, aluminium at 2.70 and steel at 7.85, the drip-screen channels at the thickness of 0.5 mm flashing, and catalogue masses for the bought items drawn as blocks (bottle, fan, electronics box, PV panel, sensor shield). The box with its deck, trays, sorbent and drip screens weighs 35.2 kg, the stand 16.6 kg and the whole unit 60.2 kg (133 lb) dry; the walls, with their battens, are 7.6 kg [G1]. The trays, sorbent, deck and drip screens (11.8 kg) all lift out through the open lid, and the box without them is 23.4 kg [G2]. v0.3 gave 33.4 kg for the box and 53.9 kg in total, from massing volumes with averaged densities.

## H. Wind

At 20 m/s the dynamic pressure is 240 Pa and the normal force on the lid 317 N: 298 N of uplift and 108 N horizontal, against a dry weight of 591 N [H1]. The overturning moment of 271 N·m exceeds the restoring moment of 244 N·m (ratio 0.90), so the unit would still tip without restraint; about 40 kg of ballast on the stand gives a factor of 1.5 [H2]. Sliding has a margin of 38 N without ballast and needs 3 kg for a factor of 1.5 [H3]. Two upwind ground anchors, each rated for 98 N or more in uplift, do the same job [H4]; they are the default restraint (DWD-DDR-002, D13).

## I. Logging

Five channels every 5 min for 30 days are 8,640 records, about 0.41 MB as CSV [I1]; any microSD card holds years.

## J. Cost

The BOM has 16 lines and totals $639 against the $520 value-engineering target (`budget_usd`, a hypothetical control target, not a limit) [J1], so R11 is over the target by $119. The v0.3 total was $515. The difference is the cost of making the design buildable (DWD-DDR-003): new line 16, the tray deck and wall ledges ($35); wall battens, inserts and paint ($13 more on line 2); the lid's U-channel frame, hinges and latches priced in full ($15 more); trays with a perforated floor under the mesh ($10 more in all); fin feet, rivets and epoxy ($4); a proper drain fitting ($7); stand bracing, foot plates and straps ($3); screen frames ($4 in all); pole, bracket and backing plate ($6); the fan hood ($1); and fixings ($7). The 2026-10-02 decisions added $19: a glazing sheet rated 130 °C or more, estimated at about $48 per square metre against $32 for a standard sheet ($17 more on line 3), and the printed "Empty before lifting" label ($2 on line 14). Cost drivers and savings worth trying are in the Value engineering section of the design decisions register. Over 5 years at the design point the parts cost about $0.59 per litre of water [J2].

## K. Requirements

*Table 4. Requirement status (DWD-REQ-001 v0.9). Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Water at the design point | 0.57 L/day | 0.5 L/day or more | Met |
| R2 | Water in dry nights | 0.45 L/day at 25 % RH | 0.25 L/day or more at 25 % RH | Met |
| R3 | Sun-only regeneration | Bed 112 °C at noon | 75 °C or more by midday | Met |
| R4 | Own electrical loads | 23.6 Wh/day against 35 Wh/day of PV; 2.6 days of autonomy | 30 Wh/day or less; 2 days or more | Met |
| R5 | Condenser rise | 12.1 K | 15 K or less | Met |
| R6 | Water quality | Food-grade materials by selection; chloride carry-over needs a water test | Food-grade; chloride below 250 mg/L | Not verifiable at TRL 3 |
| R7 | Salt containment | Pores fill at 71 % RH; 43 % of the pore volume after one 90 % RH night; 50 % after three with the fan rule; sumps 0.58 L | No brine leaves the tray and drip-screen assembly after a 90 % RH night | Met |
| R8 | Two actions per day | Open the flaps at dusk, close them at dawn; the fan runs on the logger timer with a humidity cut-out | 2 actions, 5 min or less | Met |
| R9 | Portable | Box 35.2 kg with everything inside; 23.4 kg with the trays and deck lifted out; total 60.2 kg | Box 35 kg or less when lifted with the trays and deck taken out (restated 2026-10-02, DWD-DEC-001 item 2); stand separable | Met (was not met by 0.2 kg against the first wording) |
| R10 | Survive the site | Two anchors of 98 N (default) or 40 kg of ballast at 20 m/s; UV life and 300 cycles need supplier data and test | Stable at 20 m/s; UV-stable; 300 cycles | Not verifiable at TRL 3 |
| R11 | Cost | $639 | $520 or less | **Over the value-engineering target by $119** |
| R12 | Record performance | 8,640 records, 0.41 MB | Every 5 min for 30 days | Met |
| R13 | Protect users | Glazing outer skin about 57 °C at stagnation; fins up to 47 °C; 12.8 V DC | Touched surfaces 60 °C or less; below 60 V DC | Met |

Counts: 10 met, 1 over its value-engineering target (R11), 2 not verifiable at TRL 3 (R6, R10), with R9 as restated on 2026-10-02. The computed counts [K1] in `results.csv` now agree (10 met, 1 not met, 2 not verifiable at TRL 3).

## L. Numbers changed from v0.1

*Table 5. v0.1 figures against this revision. DWD-PRC-001 and DWD-REQ-001 v0.4 carry the new values.*

| Quantity | v0.1 (as drawn) | v0.2 (design) | Tag |
| --- | --- | --- | --- |
| Salt loading; bed depth | 32.5 wt %; 8.3 mm | 25 wt %; 9.3 mm | A5 |
| Overnight uptake | 0.23 kg | 0.60 kg | B5 |
| Water at 40 % night RH | 0.20 L per day | 0.57 L per day | C3 |
| Water at 25 % night RH | 0.09 L per day | 0.45 L per day | C4 |
| Bed at noon | 104 °C | 112 °C | C2 |
| Condenser rise; load | 13.1 K; 328 W | 12.1 K; 299 W | C2 |
| Solar-to-water efficiency | 2.5 % | 7.1 % | C7 |
| Stagnation, dry bed | 105 °C | 122 °C | D1 |
| Glazing outer skin; fins | 53 °C; 48 °C | 57 °C; 47 °C | D2, D3 |
| Pore-filling humidity | 51 % RH | 71 % RH | E2 |
| Mass; box | 51.4 kg; 30.9 kg | 53.9 kg; 33.4 kg | G1 |
| Ballast; anchor rating | 49 kg; 120 N | 46 kg; 114 N | H2, H4 |
| Parts cost | $488 | $515 | J1 |
| Water cost over 5 years | $1.34 per litre | $0.49 per litre | J2 |

*Table 6. Numbers changed by the constructable design (DWD-DDR-003). Water, heat, salt and electrical figures are unchanged.*

| Quantity | v0.3 | v0.4 | Tag |
| --- | --- | --- | --- |
| Box; total mass | 33.4 kg; 53.9 kg | 35.2 kg; 60.2 kg | G1 |
| Box with trays (and now the deck) out | 24.0 kg | 23.4 kg | G2 |
| Fan duty | about 0.4 Pa | about 3.3 Pa | F3 |
| Ballast; anchor rating | 46 kg; 114 N | 40 kg; 98 N | H2, H4 |
| Parts cost | $515 | $620 | J1 |
| Water cost over 5 years | $0.49 per litre | $0.59 per litre | J2 |

*Table 7. Numbers changed by the decisions of 2026-10-02 (DWD-DEC-001). Mass, water, heat and wind figures are unchanged.*

| Quantity | v0.6 | v0.7 | Tag |
| --- | --- | --- | --- |
| Parts cost; over the $520 target | $620; $100 | $639; $119 | J1 |
| Water cost over 5 years | $0.59 per litre | $0.61 per litre | J2 |
| Computed count for R9 | not met (first wording) | met (restated) | K1 |

## M. Limits of this note

- The isotherm is built from bulk salt thermodynamics. Salt confined in silica pores behaves differently, and the Conde parameters are used outside the range of the fit at the high-temperature, high-concentration end. Measured isotherms of the actual composite at 20 °C and at 80 to 120 °C must replace it. The Conde parameters should also be checked against the paper.
- The day model treats the vapour gap as still air and the drip screen as a simple added path and radiation shield. Any convection in the tilted box would speed up desorption; leaks at the flaps would lose vapour. Both need a test.
- Diffusion inside the grains is not modelled; C9 shows the yield still meets R1 if it cuts the night NTU to 1, but with only 6 % margin.
- The natural airflow with the fan stopped (4 m³/h) is an assumption; E4 shows that R7 holds even if the fan keeps running.

> **Safety:** A proof of concept on paper does not show that the water is safe to drink. R6 (water quality) needs a laboratory water test before anyone drinks the water, and the documents keep the instruction to test and treat it.
