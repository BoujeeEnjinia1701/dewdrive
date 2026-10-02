---
doc_id: DWD-DDR-003
title: DewDrive design for construction
project: DewDrive
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02, including the recommendation for A2
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2, as made, and the recommendation for A2 in Table 3, which is now decided as recommended and recorded in the design decisions register (DWD-DEC-001).

## Context

On 2026-09-30 Amish asked for the build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The model behind DWD-DDR-002 was a massing model: it showed what DewDrive does, but many of its parts could not be made or fixed as drawn. Checking it with build123d found, among others, that the condenser plate overlapped the walls by 240 cm³, the stand ran through the condenser (12 cm³) and the walls (143 cm³), the PV pole passed through the box (56 cm³), and the drip screens floated 7 mm below the trays with nothing holding them.

Every change below keeps what DewDrive does: the same glazed, insulated 1.1 x 1.0 m box at 20°, the same trays, bed, gaps, drip screens, condenser area and fins, the same night air path down through the beds, the same fan, flaps, panel, battery and logger. The water, heat, salt and electrical results of DWD-CAL-001 are unchanged. The changes are all in `cad/src/model.py`, which now builds every made or bought piece as its own component with its material, and runs 91 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least a stated clearance. All 91 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The 1,080 x 980 mm condenser plate sat inside the walls at the height of their bottom edge, overlapping them by 240 cm³; nothing sealed or fixed it. | The plate now closes the bottom of the box: the walls stand on its top face, on EPDM gasket tape, and 24 M5 screws go up through it into the wall bottom battens. The walls start 5 mm higher (45 mm in the box frame, was 40) and are 133 mm tall (was 140), so the plate's wetted face, the trays, the glazing and every gap keep their heights. | The plate is the floor of a sealed box; screwing it to the walls from below keeps the vapour in and needs no extra frame. Keeping the heights keeps the heat and vapour calculations valid. |
| P2 | The walls were one solid block with no edges to screw into, no way to join the corners and no frame round the openings. | Four panels: 6 mm plywood skins glued to a 28 mm core of softwood battens (28 x 44 mm at the bottom, 28 x 20 mm at the top, 28 x 28 mm end posts) with 25 mm PIR foam in the bays. East and west panels fit between the long panels; three 5 x 65 mm screws per corner. The inlet opening and outlet slot are framed with battens. Six M6 threaded inserts in the east and west bottom battens take the bolts from the stand. | A sandwich panel needs solid timber wherever a screw goes. The battens carry the plate screws, the ledge screws, the lid hinges and latches and the stand bolts. |
| P3 | The sealing baffle was a 1 mm sheet spanning 1 m, carried on two rails along the east and west walls only, and the rails were fixed to nothing. It could not carry four filled trays. | A tray deck: a frame of 20 x 5 mm aluminium flat bar on edge (outside 1,016 x 916 mm, with a centre cross), corners joined by riveted angle brackets, with the 1 mm baffle riveted on top. It rests on two 15 x 15 x 2 mm angle ledges screwed to the east and west walls. An EPDM lip seal closes the 2 mm gap to the walls; EPDM tape round each opening seals the tray lips. New BOM line 16. | By hand calculation the frame sags about 3 mm at its centre under four full trays, which the gasket tape takes up; a heavier bar is an option if a trial shows the tray lips lifting. The deck lifts out, with the drip screens under it, so the sumps can be emptied. The seal keeps the night air going down through the beds, as DWD-DDR-002 (D9) requires. |
| P4 | The drip screens floated 7 mm below the trays with no support, and each brine sump overlapped the ends of the lower channels. | Each screen is a riveted frame: two 1 mm side plates, four 15 x 2 mm cross straps carrying the channels, a sump at the low end and an end plate at the high end. The sump and the end plate each have a tab riveted to a bar of the deck. The sump now sits below the channel ends (it moved 2 mm north) and both channel layers sit 2 mm lower. | Hung from the deck, the screens never touch the condenser or the water path, and come out with the deck. The sump volume (0.58 L), the channel layers and the screen depth used in DWD-CAL-001 are unchanged. |
| P5 | The fins were 1 mm strips standing on their edges against the plate; an edge cannot be riveted or bonded. | Each fin has a 10 mm folded foot, bonded with high-temperature epoxy and fixed with closed-end aluminium rivets at 150 mm pitch. Feet point toward the centre line. | A folded foot gives a face to bond and rivet; closed-end rivets keep the box sealed. The fin depth, length, number and pitch are unchanged. |
| P6 | The gutter was a closed channel standing on the plate, so water running down the plate could not get into it; the drain went out through the south wall 8 mm above the plate. | The gutter is a folded L along the south wall: a 30 mm flange on the plate (water runs over its 1 mm edge) and a 16 mm upstand protecting the plywood. The drain goes down through the gutter and the plate with a food-grade bulkhead fitting, 370 mm east of centre, between two fins. | Water collects in the lowest corner and leaves by gravity; nothing wet touches the plywood. |
| P7 | The concept had a separate 560 x 70 mm outlet flap below the trays beside the fan. With both open at night, the fan would draw outside air in through that flap and out again, past the beds, so almost no air would pass through the sorbent. Also, a 120 mm fan cannot fit in the 65 mm space under the trays. | One outlet: a 140 x 44 mm slot through the north wall below the deck, covered outside by a 160 x 64 x 130 mm hood that holds the fan in its front. The outlet flap (140 x 125 mm) closes the fan opening by day. The fan duty is now about 3.3 Pa (F3). | All the air the fan moves must now enter at the inlet above the deck and pass down through the beds, which is what DWD-CAL-001 assumes. The hood gives the fan room outside the box. |
| P8 | The inlet opening ran from 138 to 178 mm in the box frame, leaving 2 mm of wall above it: no room for a top batten, the lid seal or the flap hinge. | Same 800 x 40 mm opening, now from 118 to 158 mm: still above the deck (110 mm), its head is the wall's top batten. | Keeps the inlet area and the night air path; the wall keeps a solid top edge for the lid seal and the flap hinge. |
| P9 | The lid was a polycarbonate slab resting on the walls, with no frame, hinge, latch or seal. | The sheet sits in a mitred aluminium U-channel frame on an EPDM seal on the wall tops, with three hinges on the north wall and two over-centre latches on the south wall. Its underside stays at 180 mm. | A twin-wall sheet needs its edges held and its flutes closed; the latches press the seal by day. |
| P10 | The stand's rails ran through the condenser and the walls, the legs had no joint to the rails, nothing held the box to the stand, and nothing stopped the stand swaying sideways. | Rails of 30 x 30 x 3 mm angle lie under the plate's east and west edges and bolt up into the wall inserts (six M6 bolts). Each leg's face bolts to its rail's hanging leg (one M8 bolt) and is cut square 3 mm below the rail top. A side brace on each side, cross members at both ends, and a diagonal brace across the south end. Foot plates with bolted cleats. All joints bolted, M8. | Every joint is face to face and bolted. The side frames are rigid triangles; the south diagonal and the box, bolted to both rails, stop the stand racking. The box still lifts off the stand (R9). |
| P11 | The PV pole passed through the north-east corner of the box (56 cm³). | A 25 x 25 x 2 mm square steel tube bolted to the north-east leg with two 8 mm spacers, 6 mm clear of the wall, with a pole-top tilt bracket. | Two bolts and no welding; the panel stays north of the box where it cannot shade it. |
| P12 | The electronics box and sensor shield hung in the air beside the north-west leg. | A 160 x 430 x 3 mm aluminium backing plate bolted to the north face of that leg carries the box and, on a small arm, the sensor shield. | The box sits in the collector's shade with its lid facing out. |
| P13 | The trays were drawn as 8 mm thick blocks with a 1 mm floor; a woven mesh across 474 x 414 mm would sag under 1 kg of sorbent. | Pans folded from 1 mm sheet with an 8 mm inward bottom lip, and a floor of 1 mm perforated aluminium (about 50 % open) under a fine stainless woven mesh. | The tray outside size, the bed area and the bed depth are unchanged. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Box with everything inside 35.2 kg (was 33.4 kg), 23.4 kg with the trays, sorbent, deck and screens lifted out; stand 16.6 kg; total 60.2 kg (was 53.9 kg) [G1, G2]. | Battens, deck, screen frames, lid frame, fin feet and stand bracing; and v0.4 of the note weighs each component with its own material instead of averaged massing densities. |
| Cost | BOM lines 1 to 4, 6, 7, 10 to 12, 14 and 15 repriced and line 16 added: $620 (was $515) against the unchanged $520 value-engineering target (`budget_usd`) [J1]: $100 over. | Parts added for construction; cost drivers and savings are in the Value engineering section of the design decisions register. |
| Wind | Ballast for a factor of 1.5 now 40 kg (was 46 kg); each anchor 98 N (was 114 N) [H2, H4]. | Heavier unit. |
| Fan | About 3.3 Pa (was 0.4 Pa) [F3]; well within a 120 mm fan at low speed. | The outlet slot of P7. |
| Drawings | DWD-DWG-001 Rev P4; making sketches DWD-DWG-101 to 122. | Follow the model. |
| Documents | DWD-CAL-001 v0.5, DWD-REQ-001 v0.7, DWD-PRC-001 v0.7; build plan DWD-BLD-001 and design decisions register DWD-DEC-001 added. | Follow the model. |
| Unchanged | Water (0.57 and 0.45 L per day), bed and stagnation temperatures, condenser rise, salt containment, electrical energy. | No change to the box's heights, areas, bed, screens or condenser. |

*Table 3. Item that changes a requirement: proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A2 | Portability (R9). The full box is 35.2 kg against the 35 kg two-person limit; with the trays, sorbent, deck and screens lifted out (as the build plan does before any lift) it is 23.4 kg. | (a) restate R9 as "box 35 kg or less when lifted with the trays and deck taken out"; (b) take about 0.5 kg out (1.5 mm screen straps and deck brackets, a lighter lid channel) and keep R9 as written. | (a): lifting the box with brine sumps and loose sorbent inside should be avoided anyway; the 0.2 kg excess is inside the accuracy of the estimate. **Accepted 2026-10-02:** R9 restated as a box of 35 kg or less when lifted with the trays and deck taken out, and the box labelled to be emptied before lifting. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan DWD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Cost is reported against the value-engineering target: USD 520 (a hypothetical control target, not a limit) against an estimated USD 620 for the constructable design, USD 100 over; the register lists cost drivers and savings worth trying.
- Requirement status (DWD-CAL-001 v0.5): 9 met, 1 not met (R9 by 0.2 kg as written), 1 over its value-engineering target (R11, by $100), 2 not verifiable at TRL 3 (R6, R10). With A2 accepted, R9 is restated as a box of 35 kg or less when lifted with the trays and deck taken out, and is met at 23.4 kg; the box carries a label to empty it before lifting (DWD-REQ-001).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept stand, lid and outlet flap; they need updating on Amish's Mac, where Blender is.
- Open decisions, and the items to confirm when parts are bought, are kept in the design decisions register (`docs/06-design-decisions.md`, DWD-DEC-001).
