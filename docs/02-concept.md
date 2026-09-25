---
doc_id: DWD-PRC-001
title: DewDrive design precis
project: DewDrive
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# DewDrive design precis

DewDrive is a glazed, insulated box about 1.1 x 1.0 m, tilted 20° toward the sun on a steel stand. Inside, four black trays hold about 4 kg of silica gel impregnated with calcium chloride. At night the vent flaps are opened and a 2 W fan draws air through the box, and the sorbent takes up about 1.2 kg of water. In the morning the flaps are shut; the sun heats the bed to about 85 °C and drives the vapour down onto a finned aluminium floor that forms the condenser, shaded by the box itself. The condensate runs down the slope into a gutter and a 10 L bottle. First-order estimates give about 0.5 L per day at 40 % night RH, about 0.25 L per day at 25 %, and a parts cost of about $475, which is over the $400 budget. One unit supplements drinking water; it does not replace a water supply.

![Hero render](../media/hero.png)

*Figure 1. DewDrive on its stand, with a 1.75 m person for scale. Glazing faces south (for a northern-hemisphere site), the collection bottle sits below the low edge and the 10 W PV panel is on a pole to the north, where it cannot shade the box. Massing model.*

## How it works

1. **Adsorb at night.** In the evening the user opens the south inlet flap and the north outlet flap. The logger switches on the fan, which draws about 40 m³/h of night air through the box, over and under the four sorbent trays, for about 10 h. The CaCl₂ in the silica gel pores binds water first as hydrates and then as a solution held in the pores; the silica gel adds its own uptake and keeps the solution from dripping.
2. **Seal and heat by day.** In the morning the user shuts both flaps. Sunlight passes through the twin-wall polycarbonate and heats the black top faces of the trays. The bed reaches about 80 to 90 °C by midday, and its vapour pressure rises well above that of the condenser.
3. **Condense.** Vapour flows down through the 65 mm gap under the trays to the aluminium floor plate, which is kept near ambient by 21 fins in the shade under the box. The tray undersides are bare aluminium, so little heat radiates from the hot bed onto the condenser.
4. **Collect.** Water films run down the 20° slope to a gutter along the low edge and drain through a silicone tube into a food-grade jerrycan.
5. **Log.** The logger records air temperature and RH, bed and condenser temperatures every 5 min; the user weighs the bottle each day. The data make yields comparable between sites.

![Cutaway](../media/cutaway.png)

*Figure 2. North-south section through the drain, looking west. Blue arrows: night air path with the flaps open. Red arrows: daytime vapour path from the bed (5) to the condenser floor (6). The gutter (7) along the low edge drains to the bottle (8).*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figures 2 and 3.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Stand | Galvanized steel angle, four legs, bolted; tilt 20° | Separable from the box; anchors or ballast pads |
| 2 | Insulated box walls | Plywood skins with 25 mm PIR foam, 1,100 x 1,000 x 140 mm | Open top (glazing) and bottom (condenser) |
| 3 | Glazing lid | 10 mm UV-stabilized twin-wall polycarbonate, hinged on the north edge | Impact-safe; insulates better than single glass |
| 4 | Sorbent trays (4) | Aluminium pans with mesh floors; black top, bare underside | Lift out for recharging the sorbent |
| 5 | Composite sorbent | About 4 kg: 2.7 kg mesoporous silica gel with 1.3 kg CaCl₂ (about 33 wt %) | Bed about 8 to 12 mm deep; all food-grade |
| 6 | Condenser | 2 mm aluminium floor plate with 21 fins, 100 mm deep, underneath | Wetted face food-safe coated |
| 7 | Gutter and drain tube | Gutter along the low edge; food-grade silicone tube | |
| 8 | Collection bottle | 10 L HDPE jerrycan | About 20 days of production before it fills |
| 9 | Vent flap, south inlet | Hinged flap with EPDM seal and latches | Closed by day; seal quality sets the vapour loss |
| 10 | Night fan and outlet flap | 12 V 120 mm fan, about 2 W, on the north wall | Fan switched by the logger |
| 11 | PV panel | 10 W, 12 V, on a pole north of the box | Runs fan and logger |
| 12 | Electronics box | PWM charge controller, 12.8 V 6 Ah LiFePO4 with BMS, ESP32 logger | Only low-voltage DC on the device |
| 13 | Sensors | Air T and RH in a radiation shield; bed and condenser probes | |

Item 14 (hardware and consumables) is in the BOM but not modelled.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are stated in each row and in DWD-REQ-001. The sorbent uptake figures are the least certain input and must be replaced by measured isotherms.

![Water flow](../media/flow.png)

*Figure 4. Water per day at the design point (40 % night RH, 20 °C). All values are estimates.*

Table 2. Water, energy, size and cost.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Vapour carried through the box overnight | about 2.8 kg | 40 m³/h for 10 h at 6.9 g/m³ | |
| Overnight uptake | about 1.2 kg | 4 kg at 0.30 g/g (estimate between published composite values) | |
| Released by day | about 0.6 kg | 50 % of uptake, with the bed near 85 °C and the condenser at 45 to 50 °C | |
| Collected | about 0.49 L per day (range 0.35 to 0.6) | 85 % condensed, 95 % of that reaches the bottle | R1 met, no margin |
| Collected at 25 % night RH | about 0.25 L per day | 0.16 g/g uptake, same fractions | R2 at risk |
| Yield per aperture area | about 0.5 L/m² per day | 1.0 m² aperture | Compare 0.74 to 0.77 L/m² per day in published devices at 60 to 68 % RH |
| Heat to desorb | about 0.5 kWh (1.8 MJ) | 0.6 kg at about 3.0 MJ/kg (latent heat plus binding energy, estimate) | |
| Heat available in the bed | about 2 kWh | 4.5 kWh/m² in the window, 76 % transmitted and absorbed, less about 1.1 kWh glazing loss and 0.2 kWh to warm the bed | R3 met by estimate; the condenser, not the sun, limits yield |
| Solar-to-water efficiency | about 5 % | Latent heat of the collected water (0.33 kWh) over 6.0 kWh of sun | Published devices reach about 9 % (LaPotin et al., 2021) |
| Condenser heat load | about 250 W at peak | Latent heat plus radiation from the low-emissivity tray undersides and convection across the gap | |
| Condenser rise above ambient | about 12 K | Fins and plate about 5 m², h about 5 W/m²K, fin efficiency 0.8 | R5 met by estimate |
| Electrical use | about 24 Wh per day | Fan 2 W for 10 h; logger 0.15 W average | R4 met |
| PV supply | about 35 Wh per day | 10 W, 5 peak sun hours, 0.7 derating | Battery 77 Wh gives about 3 days autonomy |
| Mass | about 45 kg (99 lb) dry; box about 30 kg | Condenser 10.6 kg, stand 12 kg, walls 6 kg, sorbent 4 kg, glazing 4 kg, trays 2.4 kg, rest 6 kg | R9 met by estimate |
| Wind uplift at 20 m/s | about 330 N | 240 Pa dynamic pressure, force coefficient 1.2, 1.1 m² | R10: anchors or about 40 kg ballast |
| Parts cost | about $475 | Indicative prices, `bom/bom.csv` | **R11 not met** (about 19 % over $400) |
| Water per dollar over 5 years | about 1.9 L per dollar (about $0.53 per litre) | 0.49 L per day for 5 years (about 890 L), $475, no maintenance cost | For comparison only |

What the numbers say:

- **The condenser limits yield, not the sun.** The bed has about four times the heat it needs, but the vapour only moves if the condenser stays much cooler than the bed. Keeping the tray undersides low-emissivity and the fins shaded matters more than a larger aperture.
- **Yield is modest.** At about 0.5 L per day, one unit provides about one fifth of one person's survival drinking need. A household would need several units, or should treat DewDrive as a supplement for the driest weeks.
- **The design is sensitive to humidity.** Yield roughly halves between 40 % and 25 % night RH. Site humidity data will decide where DewDrive is worth building.

## Key design choices

All choices below are proposed, awaiting Amish.

1. **Single-stage, flat glazed box** rather than a dual-stage or tubular design. Simplest to build; dual-stage could add about 20 % in later versions (LaPotin et al., 2021).
2. **Silica gel and CaCl₂ composite** rather than MOF, zeolite or LiCl. Low cost and food-grade availability; LiCl absorbs more but is more toxic and costly.
3. **Condenser as the shaded floor of the box**, directly below the bed, rather than a separate condenser. Short vapour path, no pump, one fewer seal.
4. **Low-emissivity tray undersides** to cut radiation from the hot bed onto the condenser.
5. **Fan-assisted night airflow** with a small PV panel and battery, rather than natural airflow. Faster, more even uptake; costs about $75 and adds a lithium battery.
6. **Manual flaps** opened and closed by the user, rather than automatic actuators. Cheaper and repairable; relies on a daily routine.
7. **20° tilt, fixed**, facing the equator. A compromise between sun capture and condensate drainage.
8. **Built-in logging** so that each prototype yields comparable data.

## Safety

> **Safety:** Harvested water must be tested and treated before drinking. Condensed water is close to distilled, but it can pick up bacteria, dust, salt from the sorbent and metal from the condenser. Until a laboratory test shows otherwise, boil or disinfect it and do not use it as the only drinking source. Distilled-like water also lacks minerals.

> **Safety:** The glazing and the inside of the box get hot enough to burn (an estimated 80 to 90 °C in the bed, and higher with an empty bed on a hot day). Open the lid only when cool, wear gloves when handling trays, and label the glazing. The polycarbonate must be rated for the stagnation temperature.

> **Safety:** Calcium chloride irritates eyes and skin and gives off heat when it dissolves. Wear gloves and eye protection when preparing the sorbent. A saturated bed can drip a corrosive salt solution; keep trays level in storage and never let the solution reach the water path.

> **Safety:** The 12.8 V LiFePO4 battery has a built-in BMS and must be fused at the battery. Keep the electronics box shaded, and do not charge a damaged or swollen battery.

> **Safety:** A 1.1 m² tilted panel catches the wind like a sail (about 330 N at 20 m/s). Anchor or ballast the stand before loading the box. Deburr all aluminium fins and sheet edges; fins under the box are at ankle and hand height.

## Open questions

- [ ] What are the measured uptake isotherms of the chosen composite at 20 °C and at 80 to 90 °C? These set every yield number.
- [ ] How much salt carries over into the condensate, and does the aluminium condenser need a coating or a stainless replacement?
- [ ] How well do simple flap seals hold vapour during the day?
- [ ] Is the fan worth its cost and battery, or is natural airflow enough at the target sites?
- [ ] Would two smaller boxes (one per person carrying) beat one large one?
- [ ] Which site and partner provide the humidity and solar data for the design point?
