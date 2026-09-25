---
doc_id: DWD-CAL-001
title: DewDrive sizing calculations
project: DewDrive
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (sorbent isotherm, night adsorption, day desorption and condenser, cyclic yield, stagnation and touch temperatures, salt containment, electrical energy, mass, wind, logging, cost)
---

# DewDrive sizing calculations

On paper, DewDrive as drawn does not make enough water. It meets eight of its thirteen requirements, misses two, has one at risk, and two cannot be verified at TRL 3. The misses are the yield targets: about 0.20 L per day at 40 % night RH (R1 target 0.5 L) and 0.09 L per day at 25 % (R2 target 0.25 L), against 0.49 and 0.25 L per day estimated at TRL 2. The cause is the night airflow, not the sun or the sorbent. Air that skims over and under the trays at about 0.1 m/s passes on only about 11 % of the vapour it could deliver, so the bed takes up about 0.23 kg a night, not 1.2 kg. Drawing the same air down through the mesh-floored bed instead would raise the yield to about 0.53 and 0.35 L per day and meet both targets, but it fills the sorbent pores with solution after one very humid night unless the salt loading is also cut to about 25 wt %. The sun supplies far more heat than the bed uses (the bed reaches about 104 °C at noon), and the condenser stays within 13.1 K of ambient. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B2], is the line of that script's output that carries it.

> **Safety:** These calculations concern hot surfaces (a bed up to about 105 °C), a corrosive calcium chloride solution, a lithium iron phosphate battery and a 1.1 m² panel in wind. They are first-principles estimates for a paper proof of concept, not a substitute for measured isotherms, supplier data, an engineering review or test. Harvested water must be tested and treated before drinking. See DWD-PRC-001, Safety.

## Scope and method

The note checks every requirement in DWD-REQ-001 v0.3 against the design in DWD-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and part volumes, so the areas, gaps and masses used here are those of the STEP files and of drawing DWD-DWG-001. It reads prices from `bom/bom.csv` and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py` (a few minutes; the yield is a time-stepped simulation of repeated night and day cycles until the bed water at dawn repeats).

"As drawn" means the design of record: night air flows through the box past the trays. "Through-flow" is an option raised by this note, in which the fan draws the air down through the mesh-floored trays; it is a proposal awaiting Amish (see `docs/REVIEW.md`), not a change to the design.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Design point | Night 10 h at 20 °C and 40 % RH (low-humidity case 25 %); day air 35 °C; 6.0 kWh/m² per day on the tilted aperture, as a sine from 06:00 to 18:00; flaps shut at 07:00 and opened at 19:00, bed back at air temperature when the fan starts | DWD-REQ-001 |
| Psychrometrics | IAPWS-IF97 saturation pressure; vapour diffusivity 2.5 x 10⁻⁵ m²/s at 20 °C, scaled with T^1.75 | Standard |
| Salt solution | Water activity of aqueous CaCl₂ from the Conde (2004) correlation; solubility 74.5 g/100 g water at 20 °C, 81.1 at 25 °C, 134.5 at 60 °C and 152.4 at 100 °C | Conde, *Int. J. Thermal Sciences* 43, 2004; [Wikipedia](https://en.wikipedia.org/wiki/Calcium_chloride) |
| Salt hydrates | Below deliquescence at night: hexahydrate above 18.5 % RH, tetrahydrate from 9 % to 18.5 %; above 29.9 °C the solid is taken as the dihydrate | [SaltWiki, calcium chloride](https://www.saltwiki.net/index.php/Calcium_chloride) (transitions at 20 °C) |
| Composite | 2.7 kg mesoporous silica gel, 1.0 cm³/g pore volume, skeleton 2,200 kg/m³, packing 0.60; 1.3 kg CaCl₂ (32.5 wt %); the gel walls add 0.08 kg/kg per unit water activity; no pore confinement effect on the salt | Typical wide-pore gel; engineering judgment |
| Heat of sorption | Clausius-Clapeyron on the isotherm at constant bed water, not less than the latent heat | First principles |
| Night mass transfer, as drawn | Air splits between the 45 mm gap over the trays and the 65 mm gap under them in proportion to gap cubed (laminar); one wall active; Nu 4.86 plus a developing-flow term; Lewis analogy; vapour diffusion into the bed with porosity 0.40 and tortuosity 1.5; mesh floor 60 % open | Standard laminar-channel results |
| Night mass transfer, through-flow | Packed-bed Wakao correlation for 3.5 mm beads; diffusion inside the grains not modelled | Standard; grain kinetics must be measured |
| Day, bed | Lumped bed: sorbent, four 0.6 kg aluminium trays and the water; transmittance-absorptance 0.74 on the black tray tops; loss to ambient 3.2 W/(m²·K) through the gap and twin-wall glazing | Twin-wall polycarbonate U value about 3 W/(m²·K) |
| Day, vapour path | Stefan diffusion through still air across the 65 mm gap to the condenser (hot above cold is stably stratified); 60 % of the bed area effective through the mesh | First principles |
| Day, parasitic heat | Radiation from bed to condenser: beads (emissivity 0.9) seen through 60 % open mesh, bare aluminium 0.1 elsewhere, plate 0.9; conduction across the gap; sun through the gaps between trays onto the plate, absorptance 0.5 | Engineering judgment |
| Condenser | 2 mm aluminium plate and 21 fins, 1 x 100 x 920 mm; laminar natural convection on vertical fins; radiation from the fin envelope to shaded ground at ambient; aluminium 205 W/(m·K) | Model; standard correlations |
| Collection | 30 g per day left as drops and films on the plate and gutter | Engineering judgment |
| Electrical | Fan 2 W for 10 h; logger 0.15 W average; 10 W panel, 5 peak sun hours, 0.70 derating; 12.8 V 6 Ah battery, 80 % usable | DWD-PRC-001 |
| Wind | 20 m/s; force coefficient 1.2 on 1.1 m² normal to the lid; centre of pressure a quarter chord upwind of the centre; friction 0.5; factor of safety 1.5 | Engineering judgment |

## A. Air and sorbent

At 20 °C the night air carries 6.92 g/m³ of vapour at 40 % RH and 4.32 g/m³ at 25 % RH [A1]. The Conde correlation puts the deliquescence point of CaCl₂ at 20 °C at a water activity of 0.341, against about 0.30 quoted by SaltWiki [A2]; the difference only matters between 30 and 34 % RH. At 40 % RH the salt is a 40.1 wt % solution holding 1.49 kg of water per kg of salt; at 25 % RH it is the hexahydrate, holding 0.974 kg/kg [A3].

The whole bed would hold 2.03 kg of water at equilibrium at 40 % RH (0.507 g/g) and 1.32 kg at 25 % RH (0.330 g/g) [A4]. Both are well above the 0.30 and 0.16 g/g assumed at TRL 2, so equilibrium does not limit the yield. The 2.7 kg of gel has 2.70 L of pore volume; the bed is 6.55 L of beads, 8.3 mm deep on 0.785 m² of tray floor, which matches the model [A5].

## B. Night adsorption

The fan moves 40 m³/h, so 2.77 kg of vapour passes through the box in a night at 40 % RH, and 1.73 kg at 25 % RH [B4]. The question is how much of it the bed can catch.

**As drawn.** A quarter of the air goes over the trays and three quarters under them, at 0.06 and 0.13 m/s. The flow is laminar (Re 339 and 1,022) and the heat transfer coefficients are only about 1.7 W/(m²·K) [B1]. With diffusion into the bed in series, the number of transfer units is 0.32 over the trays and 0.06 under them, so at most 11 % of the vapour driving force is captured [B2]. In the repeating cycle the bed takes up 0.23 kg a night at 40 % RH (a swing of 0.057 g/g), from 0.44 kg at dusk to 0.67 kg at dawn; the heat of adsorption warms it only to 23.4 °C [B5]. At 25 % RH it takes up 0.12 kg [B6].

**Through-flow option.** Drawing the same air down through the bed gives a superficial velocity of 14.2 mm/s and a gas-side number of transfer units of 17, so the air leaves close to equilibrium with the bed; the bed adds only 0.15 Pa of pressure drop [B3]. The uptake rises to 0.56 kg a night at 40 % RH and 0.38 kg at 25 % RH [B7]. The bed then swings between 0.97 kg at dusk and 1.53 kg at dawn, still below the 2.03 kg equilibrium [C12], so the day desorption, not the night, now sets the limit. Diffusion inside the grains is not modelled; it can only lower these figures, and it must be measured.

## C. Day desorption, condenser and yield

The aperture receives 6.00 kWh/m² per day, of which 4.24 kWh/m² falls between 09:00 and 15:00 (TRL 2 said 4.5); the peak is 785 W/m² [C1].

Table 2 traces the design point as drawn. The bed passes 86 °C by 09:00 and reaches 104 °C at noon [C2]. Vapour only moves once the bed's vapour pressure exceeds that of the condenser, from about 09:00 to 14:00, peaking at about 70 g/h. By mid-afternoon the salt has dried to the dihydrate and desorption stops, although the bed is still at 94 °C.

*Table 2. Day at the design point, as drawn (script output, section C).*

| Hour | Sun (W/m²) | Bed (°C) | Condenser (°C) | Bed water activity | Desorption (g/h) | Bed water (kg) |
| --- | --- | --- | --- | --- | --- | --- |
| 07:00 | 203 | 25.3 | 33.6 | 0.090 | 0 | 0.67 |
| 09:00 | 555 | 86.2 | 43.6 | 0.175 | 9 | 0.67 |
| 11:00 | 759 | 102.1 | 47.5 | 0.183 | 59 | 0.60 |
| 12:00 | 785 | 104.1 | 48.1 | 0.186 | 70 | 0.53 |
| 13:00 | 759 | 103.1 | 47.8 | 0.185 | 65 | 0.47 |
| 15:00 | 555 | 94.1 | 44.8 | 0.094 | 0 | 0.44 |
| 17:00 | 203 | 63.5 | 39.6 | 0.094 | 0 | 0.44 |

*Table 3. Yield and energy.*

| Quantity | As drawn | Through-flow | Tag |
| --- | --- | --- | --- |
| Collected at 40 % night RH | 0.20 L per day (0.23 kg condensed) | 0.53 L per day | C3, C5 |
| Collected at 25 % night RH | 0.09 L per day | 0.35 L per day | C4, C5 |
| Yield per inner aperture area | 0.21 L/m² per day | about 0.56 L/m² per day | C3 |
| Bed peak | 104 °C | 101 °C | C2, C5 |
| Condenser rise above ambient, peak | 13.1 K | 13.3 K | C2, C5 |
| Solar-to-water efficiency | 2.5 % | 6.5 % | C6, C7 |
| Water cost over 5 years, $488 of parts | about $1.34 per litre | about $0.51 per litre | J2 |

The energy balance shows where the sun goes, as drawn at 40 % RH [C6]: 5.54 kWh falls on the inner aperture; the black trays absorb 3.68 kWh; only 0.17 kWh drives desorption; 1.51 kWh is lost back through the glazing; and 1.96 kWh passes from the hot bed straight to the condenser, mostly as radiation from the beads seen through the mesh floor. That parasitic flow sets the condenser load (peak 328 W) and so its temperature. The TRL 2 note assumed low-emissivity tray undersides; with mesh floors the beads themselves face the condenser.

The condenser has 3.86 m² of fins with a natural-convection coefficient of 4.7 W/(m²·K) and a fin efficiency of 0.87, giving 24.6 W/K at a 12 K rise [C8]. It holds the peak rise to 13.1 K, inside R5.

**Sensitivity.** Halving or doubling the night mass transfer gives 0.09 or 0.29 L per day as drawn [C9]. Doubling the fan flow to 80 m³/h gives only 0.21 L per day [C10], because the bed, not the air supply, limits the uptake. Through-flow with the salt cut to 25 wt % gives 0.51 L per day at 40 % RH and 0.37 L at 25 % [C11].

## D. Stagnation and touch temperatures

With a dry bed at noon on a 35 °C day, the bed stagnates near 105 °C [D1]. Twin-wall polycarbonate is usually rated to about 120 °C in service; the supplier rating must be checked. The outer skin of the glazing reaches about 53 °C at stagnation [D2], and the condenser fins, at ankle and hand height, up to 48 °C [D3]. Both are under the 60 °C limit of R13, but the inside of the box is not: the bed and trays are hot enough to burn.

## E. Salt containment

A calcium chloride solution stays in the beads only while its volume is less than the pore volume. At equilibrium at 40 % RH the solution fills 85 % of the 2.70 L of pores; at 90 % RH it would be 8.25 L, three times the pore volume [E1]. The pores fill at 51 % RH at 20 °C, so any long humid spell can make the beads weep brine [E2].

Kinetics save the design as drawn from one bad night: a 10 h night at 90 % RH from the normal dusk state takes the bed only to 46 % of its pore volume. With through-flow the same night overfills the pores (111 %) [E3]. Cutting the salt to 25 wt % raises the pore-filling humidity to 71 % RH (81 % at 20 wt %) [E5], keeps a 90 % RH night to 82 % of the pores with through-flow [E6], and still leaves 1.59 kg of equilibrium uptake at 40 % RH [E4a]. Several humid nights in a row, or a night with rain, can still overfill any loading; a drip tray under each tray, or a hygrostat that stops the fan above about 70 % RH, would contain that case.

## F. Electrical energy

The fan uses 20 Wh a night and the logger 3.6 Wh a day, 23.6 Wh in all, against 35 Wh a day from the 10 W panel, a margin of 1.48 [F1]. The 76.8 Wh battery, 80 % usable, gives 2.6 days with no sun [F2] (TRL 2 said about 3 days). The fan works against only about 0.2 Pa, so a 120 mm fan delivers 40 m³/h at low speed [F3].

## G. Mass

From the model volumes, with component estimates for the parts the massing model draws as solid blocks, the box with trays, sorbent and condenser weighs 30.9 kg, the stand 14.1 kg, and the whole unit 51.4 kg (113 lb) dry [G1]. With the trays and sorbent lifted out first, the box is 24.0 kg [G2]. TRL 2 estimated 45 kg in total; the stand and condenser are heavier than assumed.

## H. Wind

At 20 m/s the dynamic pressure is 240 Pa and the normal force on the lid 317 N: 298 N of uplift and 108 N horizontal, against a dry weight of 505 N [H1]. The overturning moment of 271 N·m exceeds the restoring moment of 209 N·m, so the unit would tip without restraint; about 49 kg of ballast on the stand gives a factor of 1.5 [H2]. Sliding has no margin without ballast (−5 N), and needs 12 kg for a factor of 1.5 [H3]. Two upwind ground anchors, each rated for 120 N or more in uplift, do the same job [H4]. TRL 2 estimated 330 N and about 40 kg.

## I. Logging

Five channels every 5 min for 30 days are 8,640 records, about 0.41 MB as CSV [I1]; any microSD card holds years.

## J. Cost

The BOM has 14 lines and totals $488 against the $500 budget set by Amish on 2026-09-25 [J1]. Over 5 years at the as-drawn yield the parts cost about $1.34 per litre of water, or about $0.51 per litre with through-flow [J2].

## K. Requirements

*Table 4. Requirement status (DWD-REQ-001 v0.3). Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Water at the design point | 0.20 L/day as drawn; 0.53 L/day with through-flow | 0.5 L/day or more | **Not met** |
| R2 | Water in dry nights | 0.09 L/day as drawn; 0.35 L/day with through-flow | 0.25 L/day or more at 25 % RH | **Not met** |
| R3 | Sun-only regeneration | Bed 104 °C at noon | 75 °C or more by midday | Met |
| R4 | Own electrical loads | 23.6 Wh/day against 35 Wh/day of PV; 2.6 days of autonomy | 30 Wh/day or less; 2 days or more | Met |
| R5 | Condenser rise | 13.1 K as drawn; 13.3 K with through-flow | 15 K or less | Met, thin margin |
| R6 | Water quality | Food-grade materials by selection; chloride carry-over needs a water test | Food-grade; chloride below 250 mg/L | Not verifiable at TRL 3 |
| R7 | Salt containment | Pores fill at 51 % RH; 46 % of the pore volume after one 90 % RH night as drawn, 111 % with through-flow | No liquid leaves the trays after a 90 % RH night | At risk |
| R8 | Two actions per day | Open the flaps at dusk, close them at dawn; the fan runs on the logger timer | 2 actions, 5 min or less | Met |
| R9 | Portable | Box 30.9 kg with sorbent, 24.0 kg with trays out; total 51.4 kg | Box 35 kg or less; stand separable | Met |
| R10 | Survive the site | Needs 49 kg of ballast or two anchors at 20 m/s; UV life and 300 cycles need supplier data and test | Stable at 20 m/s; UV-stable; 300 cycles | Not verifiable at TRL 3 |
| R11 | Cost | $488 | $500 or less | Met |
| R12 | Record performance | 8,640 records, 0.41 MB | Every 5 min for 30 days | Met |
| R13 | Protect users | Glazing outer skin about 53 °C at stagnation; fins up to 48 °C; 12.8 V DC | Touched surfaces 60 °C or less; below 60 V DC | Met |

Counts: 8 met, 2 not met (R1, R2), 1 at risk (R7), 2 not verifiable at TRL 3 (R6, R10).

## L. Numbers corrected from TRL 2

*Table 5. TRL 2 figures checked against this note. DWD-PRC-001 and DWD-REQ-001 v0.3 carry the corrected values.*

| Quantity | TRL 2 | TRL 3 | Tag |
| --- | --- | --- | --- |
| Overnight uptake | 1.2 kg (0.30 g/g) | 0.23 kg as drawn; 0.56 kg with through-flow | B5, B7 |
| Water at 40 % night RH | 0.49 L per day | 0.20 L per day as drawn | C3 |
| Water at 25 % night RH | 0.25 L per day | 0.09 L per day as drawn | C4 |
| Sun in the 09:00 to 15:00 window | 4.5 kWh/m² | 4.24 kWh/m² | C1 |
| Bed temperature at midday | 80 to 90 °C | 104 °C | C2 |
| Condenser load, peak | about 250 W | 328 W | C2 |
| Condenser rise | about 12 K | 13.1 K | C2 |
| Solar-to-water efficiency | about 5 % | 2.5 % | C6 |
| Battery autonomy | about 3 days | 2.6 days | F2 |
| Mass | about 45 kg; box about 30 kg | 51.4 kg; box 30.9 kg | G1 |
| Wind force; ballast | about 330 N; about 40 kg | 317 N normal (298 N uplift); 49 kg | H1, H2 |
| Bed depth | 8 to 12 mm | 8.3 mm | A5 |
| Parts cost | about $475 | $488 | J1 |
| Water cost over 5 years | about $0.53 per litre | about $1.34 per litre | J2 |

## M. Limits of this note

- The isotherm is built from bulk salt thermodynamics. Salt confined in silica pores behaves differently, and the Conde parameters are used outside the range of the fit at the high-temperature, high-concentration end. Measured isotherms of the actual composite at 20 °C and at 80 to 105 °C must replace it.
- The day model treats the vapour gap as still air. Any convection in the tilted box would speed up desorption; leaks at the flaps would lose vapour. Both need a test.
- The as-drawn night mass transfer is the most important and least certain number here. Its sensitivity (C9) spans 0.09 to 0.29 L per day; none of that range meets R1.

> **Safety:** A proof of concept on paper does not show that the water is safe to drink. R6 (water quality) needs a laboratory water test before anyone drinks the water, and the documents keep the instruction to test and treat it.
