---
doc_id: DWD-PRC-001
title: DewDrive design precis
project: DewDrive
doc_type: Design precis
version: "0.8"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (how it works, components, first-order numbers, design choices, safety, open questions, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (design choices decided by Amish in DWD-DDR-001; numbers replaced by DWD-CAL-001; parametric model and drawing DWD-DWG-001; yield shortfall and proposed fixes)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); through-flow trays, 25 wt % salt, drip screens, fan humidity cut-out, anchors as default; numbers from DWD-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Design made constructable (DWD-DDR-003): tray deck, one outlet through the fan hood, bolted stand; mass and cost from DWD-CAL-001 v0.4"
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02 carried in (DWD-DEC-001 items 2 to 5): glazing rated 130 °C or more, stagnation vent study, R9 restated with lifting rule, first partner type'
---

# DewDrive design precis

DewDrive is a glazed, insulated box 1.1 x 1.0 m, tilted 20° toward the sun on a steel stand. Inside, four black trays hold 4 kg of silica gel impregnated with 25 wt % calcium chloride. At night the vent flaps are opened and a 2 W fan draws air in above the trays and down through their mesh floors, and the sorbent takes up water. In the morning the flaps are shut; the sun heats the bed to about 112 °C by noon and drives the vapour down past a black drip screen onto a finned aluminium floor that forms the condenser, shaded by the box itself. The condensate runs down the slope into a gutter and a 10 L bottle. The TRL 3 calculation (DWD-CAL-001 v0.2) gives about 0.57 L per day at 40 % night RH and 0.45 L at 25 %, meeting the 0.5 and 0.25 L targets. The design follows Amish's decisions of 2026-09-25 (DWD-DDR-002), which replaced the v0.1 layout that made only 0.20 L per day. Made buildable in DWD-DDR-003, the estimated parts cost is $620 against the $520 value-engineering target (moved to $520 by Amish on 2026-09-26), $100 over the target. One unit supplements drinking water; it does not replace a water supply.

![Hero render](../media/hero.png)

*Figure 1. DewDrive on its stand, with a 1.75 m person for scale. Glazing faces south (for a northern-hemisphere site), the collection bottle sits below the low edge and the 10 W PV panel is on a pole to the north, where it cannot shade the box. Generated from the parametric model `cad/src/model.py`.*

## How it works

1. **Adsorb at night.** In the evening the user opens the south inlet flap, which sits above the tray deck, and the outlet flap over the fan on the north wall. The logger switches on the fan, which draws 40 m³/h of night air in over the trays, down through the 9.3 mm sorbent beds and their mesh floors, and out under the deck through a slot into the fan hood, for 10 h. The trays sit on an EPDM gasket on the sealing baffle of a lift-out deck, so the air cannot bypass the beds. The CaCl₂ in the silica gel pores binds water first as hydrates and then as a solution held in the pores; the silica gel adds a little uptake of its own and keeps the solution in place. If the air goes above 70 % RH the logger stops the fan.
2. **Seal and heat by day.** In the morning the user shuts both flaps. Sunlight passes through the twin-wall polycarbonate and heats the black top faces of the trays. The bed passes 89 °C by 09:00 and reaches about 112 °C at noon, and its vapour pressure rises above that of the condenser.
3. **Condense.** Vapour diffuses down through the 65 mm gap under the trays, around the drip-screen channels, to the aluminium floor plate, which stays within about 12 K of ambient thanks to 21 fins in the shade under the box.
4. **Collect.** Water films run down the 20° slope to a gutter along the low edge and drain through a silicone tube into a food-grade jerrycan.
5. **Log.** The logger records air temperature and RH, bed and condenser temperatures every 5 min, and applies the fan humidity cut-out; the user weighs the bottle each day. The data make yields comparable between sites.

![Cutaway](../media/cutaway.png)

*Figure 2. North-south section through the drain, looking west. Blue arrows: night air path with the flaps open, in above the trays and down through the beds. Red arrows: daytime vapour path from the bed (5) past the drip screen (15) to the condenser floor (6). The gutter (7) along the low edge drains to the bottle (8).*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv`, drawing DWD-DWG-001 and Figures 2 and 3.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Stand | Galvanized steel angle 30 x 30 x 3 mm, rails, legs, braces and cross members, bolted; tilt 20° | Separable from the box; two ground anchors by default, about 40 kg of ballast as the alternative (DWD-DDR-002, D13; DWD-CAL-001, H2 to H4) |
| 2 | Insulated box walls | Plywood skins with 25 mm PIR foam, 1,100 x 1,000 x 140 mm, 40 mm thick | Open top (glazing) and bottom (condenser) |
| 3 | Glazing lid | 10 mm UV-stabilized twin-wall polycarbonate, hinged on the north edge | Rated 130 °C or more; a 120 °C sheet only if supplier data and the inner skin measured at the TRL 4 stagnation test both show it stays inside its rating (DWD-DEC-001, item 3) |
| 4 | Sorbent trays (4) | Aluminium pans 490 x 430 x 25 mm with stainless mesh floors; black top, bare underside; EPDM edge gasket on a 1 mm aluminium sealing baffle | Lift out for recharging; the baffle forces the night air through the beds (D9) |
| 5 | Composite sorbent | 4 kg: 3.0 kg mesoporous silica gel with 1.0 kg CaCl₂ (25 wt %, D10) | Bed 9.3 mm deep on 0.785 m²; all food-grade |
| 15 | Drip screens (4) | Two staggered layers of 20 x 6 mm aluminium channels at 30 mm pitch under each tray, running down the slope to a closed brine sump; painted matt black | Catch any brine that leaves the beds (sumps 0.58 L in all) with no line of sight from bed to condenser (D11) |
| 6 | Condenser | 2 mm aluminium floor plate with 21 fins, 1 x 100 x 920 mm at 50 mm pitch | Wetted face food-safe coated |
| 7 | Gutter and drain tube | Gutter along the low edge; food-grade silicone tube | |
| 8 | Collection bottle | 10 L HDPE jerrycan | About 17 days of production at the design point |
| 9 | Vent flap, south inlet | Hinged flap 800 x 40 mm above the trays, with EPDM seal and latches | Closed by day; seal quality sets the vapour loss |
| 10 | Night fan, hood and outlet flap | 12 V 120 mm fan, about 2 W, in a hood over a slot in the north wall below the deck; the outlet flap closes the fan opening by day | Fan switched by the logger; stops above 70 % RH |
| 11 | PV panel | 10 W, 12 V, on a pole north of the box | Runs fan and logger |
| 12 | Electronics box | PWM charge controller, 12.8 V 6 Ah LiFePO4 with BMS, ESP32 logger | Only low-voltage DC on the device |
| 13 | Sensors | Air T and RH in a radiation shield; bed and condenser probes | The air RH reading drives the fan cut-out |

Item 14 (hardware and consumables) is in the BOM but not modelled. Item 16 is the lift-out tray deck with its sealing baffle and the wall ledges. The general arrangement is drawing DWD-DWG-001 Rev P4 (`cad/drawings/`); the STEP files are in `cad/step/`; how to build it is the build plan DWD-BLD-001 (`docs/05-build-plan.md`).

**Fan rule (DWD-DDR-002, D11).** The logger runs the fan from the evening flap opening for 10 h, and stops it whenever the air RH is above 70 % (restarting below about 65 %, to avoid cycling). This is a design rule for the firmware sketch; firmware beyond a sketch is TRL 4 work and on hold.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

## Numbers from DWD-CAL-001

All values are first-principles estimates from `docs/04-calcs/sizing.py` (DWD-CAL-001 v0.5); the tag after each value is the line of the script output that carries it. The sorbent isotherm is built from bulk salt data and must be replaced by measured isotherms of the actual composite.

![Water flow](../media/flow.png)

*Figure 4. Water per day at the design point (40 % night RH, 20 °C). All values are estimates.*

Table 2. Water, energy, size and cost.

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Vapour carried through the box overnight | 2.77 kg (B4) | 40 m³/h for 10 h at 6.92 g/m³ | |
| Share of the vapour driving force captured | Nearly all (gas-side NTU 19, B3) | Air drawn down through the bed; 0.16 Pa pressure drop | v0.1 layout: 11 % (B2) |
| Overnight uptake | 0.60 kg (B5) | Cyclic simulation; equilibrium would allow 1.59 kg (A4) | |
| Collected at 40 % night RH | 0.57 L per day (C3) | 0.60 kg condensed less 30 g of films | R1 met |
| Collected at 25 % night RH | 0.45 L per day (C4) | Same model | R2 met |
| Bed temperature at noon | 112 °C (C2) | 785 W/m² peak; 4.24 kWh/m² from 09:00 to 15:00 (C1) | R3 met |
| Condenser rise above ambient, peak | 12.1 K (C2) | Load 299 W peak; UA 24.6 W/K (C8) | R5 met |
| Where the sun goes | 3.68 kWh absorbed; 0.44 kWh desorbs water; 1.69 kWh lost through the glazing; 1.47 kWh to the condenser (C7) | The black drip screens cut the effective bed-to-condenser emissivity from 0.545 to 0.327 (C5) | |
| Solar-to-water efficiency | 7.1 % (C7) | Published devices reach about 9 % (LaPotin et al., 2021) | |
| Stagnation temperature, dry bed | 122 °C (D1) | Noon, 35 °C air | Glazing rated 130 °C or more (DWD-DEC-001, item 3) |
| Electrical use and supply | 23.6 Wh per day against 35 Wh (F1); 2.6 days of autonomy (F2) | Fan 2 W for 10 h; logger 0.15 W | R4 met |
| Salt containment | Pores fill above 71 % RH (E2); 43 % full after one 90 % RH night (E3) | Sumps 0.58 L (E6) | R7 met on paper |
| Mass | 60.2 kg (133 lb) dry; box 35.2 kg, 23.4 kg with the trays and deck lifted out (G1, G2) | Model components | R9 met as restated on 2026-10-02 (lift with the trays and deck out) |
| Wind at 20 m/s | 317 N normal to the lid; tips without two anchors or 40 kg of ballast (H1 to H4) | Force coefficient 1.2 on 1.1 m² | R10 not verifiable at TRL 3 |
| Parts cost | $620 (J1) | `bom/bom.csv` | R11 over the value-engineering target by $100 (target $520) |
| Water per dollar over 5 years | about $0.49 per litre (J2) | Parts only | For comparison |

What the numbers say:

- **Drawing the air through the bed fixes the yield.** The v0.1 layout, with air skimming past the trays, captured only 11 % of the vapour driving force and made 0.20 L per day. Through the bed, the air leaves close to equilibrium with the sorbent, and the day desorption now sets the limit. Even if slow diffusion inside the grains cut the night NTU to 1, the yield would still be 0.53 L per day (C9).
- **The drip screens help the yield.** Black channels under the trays catch brine and also cut the radiation from the hot beads to the condenser by about 40 %: 0.57 L per day with them against 0.51 L without (C6).
- **A low-emissivity screen would do more, but overheats the box.** Bare aluminium channels would give 0.82 L per day, but a dry bed would stagnate at about 166 °C, beyond the rating of polycarbonate glazing (C10, D1). That option is not adopted. Amish decided on 2026-10-02 (DWD-DEC-001, item 4) on one short paper study of a passive stagnation vent; if it cannot hold a dry bed near 122 °C at a modest cost, the low-emissivity screens are dropped.
- **The lower salt loading contains the brine.** At 25 wt % the solution fills the pores only above 71 % RH, against 51 % RH at the v0.1 loading (E2).
- **Cost is over the value-engineering target once the design is buildable.** The gasket, baffle and drip screens added $27 (total $515, D15); the parts that make the design buildable (DWD-DDR-003) bring the estimated cost to $620 against the $520 target ($100 over).
- **Yield is still modest.** About 0.57 L per day is about one fifth of one person's survival drinking need.

## Key design choices

Choices 1 to 7 were decided by Amish on 2026-09-25 (DWD-DDR-001, going with the recommendation), and choices 8 to 11 on the same day (DWD-DDR-002). Choice 12 was part of the design from the start.

1. **Single-stage, flat glazed box** rather than a dual-stage or tubular design (D4). Dual-stage could add about 20 % in later versions (LaPotin et al., 2021).
2. **Silica gel and CaCl₂ composite**, rather than MOF, zeolite or LiCl (D3), at 25 wt % salt (D10, amending the 33 wt % of D3).
3. **Condenser as the shaded floor of the box**, directly below the bed (D4). Short vapour path, no pump, one fewer seal.
4. **Fan-assisted night airflow** with a 10 W PV panel and a 12.8 V LiFePO4 battery, rather than natural airflow (D5).
5. **Manual flaps** opened and closed by the user, rather than automatic actuators (D6).
6. **20° tilt, fixed**, facing the equator, with twin-wall polycarbonate glazing rather than glass (D7).
7. **Design point** of 20 °C and 40 % RH at night and 6.0 kWh/m² of sun, with a 25 % RH low-humidity case (D8).
8. **Night air drawn down through the sealed trays** (D9), with the inlet flap above the trays and the fan below them.
9. **Drip screens and a fan humidity cut-out** for wet spells (D11). The screens are black, not low-emissivity, after the paper evaluation of D12.
10. **Two ground anchors by default**, ballast as the alternative (D13).
11. **Value-engineering target kept at $500** (D14), then moved to $520 by Amish on 2026-09-26 (D15) once the BOM reached $515.
12. **Built-in logging** so that each prototype yields comparable data.

## Safety

> **Safety:** Harvested water must be tested and treated before drinking. Condensed water is close to distilled, but it can pick up bacteria, dust, salt from the sorbent and metal from the condenser. Until a laboratory test shows otherwise, boil or disinfect it and do not use it as the only drinking source. Distilled-like water also lacks minerals.

> **Safety:** The inside of the box gets hot enough to burn: an estimated 112 °C in the bed at noon and about 122 °C with a dry bed (DWD-CAL-001 v0.2, C2 and D1). The glazing outer skin reaches about 57 °C and the condenser fins about 47 °C. Open the lid only when cool, wear gloves when handling trays and drip screens, and label the glazing. The polycarbonate must be rated 130 °C or more (DWD-DEC-001, item 3); a 120 °C sheet is acceptable only if the supplier's data and the inner-skin temperature measured at the TRL 4 stagnation test both show it stays inside its rating. Do not fit bare, low-emissivity screens: they would raise the dry bed to about 166 °C.

> **Safety:** Calcium chloride irritates eyes and skin and gives off heat when it dissolves. Wear gloves and eye protection when preparing the sorbent and when emptying the drip-screen sumps. At 25 wt % the solution fills the pores only above about 71 % RH (DWD-CAL-001, E2); the fan stops above 70 % RH and the drip screens catch any brine. Keep trays level, close the flaps in rain, and never let the solution reach the water path.

> **Safety:** The 12.8 V LiFePO4 battery has a built-in BMS and must be fused at the battery. Keep the electronics box shaded, and do not charge a damaged or swollen battery.

> **Safety:** The tilted lid catches the wind like a sail (317 N at 20 m/s). Without restraint the unit tips over (DWD-CAL-001, H2). Fit the two ground anchors, or about 40 kg of ballast, before the box goes on the stand. Empty the box of its trays and deck before lifting it; it carries a label saying so (R9 as restated, DWD-DEC-001, item 2). Deburr all aluminium fins, channels and sheet edges; fins under the box are at ankle and hand height.

## Open questions

- [ ] What are the measured uptake isotherms and rates of the 25 wt % composite at 20 °C and at 80 to 120 °C? These set every yield number.
- [x] How can the parts cost come back to $500, or should the value-engineering target move? Decided by Amish, 2026-09-26: target moved to $520 (DWD-DDR-002, D15).
- [ ] Can a passive stagnation vent hold a dry bed near 122 °C at a modest cost? Decided by Amish, 2026-10-02 (DWD-DEC-001, item 4): one short paper study; if it cannot, the low-emissivity screens are dropped.
- [x] Glazing rating with a 122 °C dry bed. Decided by Amish, 2026-10-02 (DWD-DEC-001, item 3): rated 130 °C or more, or a 120 °C sheet only with supplier data and a measured inner-skin temperature at the TRL 4 stagnation test.
- [ ] How much salt carries over into the condensate, and does the aluminium condenser need a coating or a stainless replacement?
- [ ] How well do simple flap and tray seals hold, by night against bypass air and by day against vapour loss?
- [ ] Which site provides the humidity and solar data for the design point? Partner type decided by Amish, 2026-10-02 (DWD-DEC-001, item 5): the first candidate to approach, not yet agreed, is a university dryland field station in a hot semi-arid region with night humidity of about 25 to 40 % and an existing weather record, with a water and sanitation NGO for the later community trial.
