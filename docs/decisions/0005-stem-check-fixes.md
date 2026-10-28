---
doc_id: DWD-DDR-005
title: DewDrive STEM check fixes
project: DewDrive
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Five detail fixes from the first STEM check and its independent review (DWD-STM-001 S5, S9, S12, S18, S20), made under Amish's standing instruction of 2026-10-23
---

# 0005: STEM check fixes

- **Date:** 2026-10-25
- **Status:** decided under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction"). Amish can reverse any of them. None changes the working principle, the pitch or the scope.

## Context

The first STEM check of DewDrive (DWD-STM-001, kit 1.8) found three details where the design as drawn did not do what DWD-CAL-001 assumed (D16 to D18), and its independent review found two more (D19, D20). Each is fixed in the model, the calculation, the BOM and the build plan, and the STEM check row closes on the fix. The fixes do not restore PR-001: the design collects 0.44 L per day against 0.5, and how to recover it is for Amish (DWD-DEC-001, open item 2).

## Options considered and decisions

### D16: the sun must fall on a black surface (STEM S5)

DWD-CAL-001 up to v0.7 took 95 % absorptance "on the black tray tops", but the trays are open pans and 93 % of their footprint is the sorbent bed, whose silica gel and calcium chloride beads are white (absorptance about 0.3, an estimate). Rerun with that value, the v0.7 design makes 0.03 L per day, not 0.57 (DWD-CAL-001 v0.8, C11).

| Option | For | Against |
| --- | --- | --- |
| Black perforated absorber plate resting on each bed (chosen) | Stock material; night air still passes through the holes; lifts out with the tray; keeps the beads in place | Adds 1.7 kg and about $24 (its coating is counted under D17); heat must conduct down through the bed (about 16 K drop at noon, C12) |
| Black pigment (food-grade carbon) mixed into the beads | No new part | Unknown effect on the isotherm and salt confinement; dust; a new material in the bed |
| Solid black lid on each tray with side air entry | Highest absorptance | Changes the night air path that DWD-DDR-002 decided |

**Decision:** a 1 mm aluminium absorber plate, perforated with 3 mm holes at 6 mm staggered pitch (stock R3 T6, 22.7 % open), black PTFE-coated, 484 by 424 mm with two finger holes, resting on each bed. A 35 % open plate was tried first and gave less water; the closer pattern gives an effective transmittance-absorptance of 0.70 (C11).

### D17: brine-wetted parts must survive hot calcium chloride (STEM S20)

The trays, perforated floors and drip screens were bare or painted aluminium, and the floor mesh was a stainless woven mesh. Aluminium pits in chloride brine, and austenitic stainless steel risks chloride stress corrosion cracking above about 60 °C (SSINA); the beds run to about 110 °C.

| Option | For | Against |
| --- | --- | --- |
| Black PTFE coating on the brine-wetted faces, PTFE-coated glass-fibre mesh (chosen) | PTFE is inert to CaCl₂ and rated to 260 °C; keeps the light aluminium parts; undersides stay bare so the radiation figures hold | A coating shop is needed; damaged coating exposes the metal (carried in the design FMEA) |
| Trays and screens in 316 stainless steel | Robust in pitting | Still at risk of stress corrosion cracking above 60 °C; heavier and dearer |
| Polymer trays (PPS, PEEK) | No corrosion | Expensive; few local suppliers |

**Decision:** black PTFE (fluoropolymer) coating on the tray insides, the floor top faces, the absorber plates and the drip screens; PTFE-coated glass-fibre open mesh on the floors. Estimated $32 more (BOM lines 4 and 15, estimates to quote).

### D18: the condenser underside must radiate as the calculation assumes (STEM S12)

DWD-CAL-001 (C8) gives the finned underside an emissivity of 0.85 for radiation to the shaded ground, but the fins and plate underside were bare aluminium (about 0.1).

**Decision:** paint the fins and plate underside with a matt, high-emissivity exterior paint (about 0.9), about $8 (BOM line 6). This is option B's best idea (DWD-OPT-001) grafted onto option A. The alternatives, more fins or deeper fins, add aluminium and mass for the same effect.

### D19: the tray floor must let the vapour through (STEM S9, independent review)

DWD-CAL-001 up to v0.7 took 60 % of the bed area as open to the vapour through the tray floor, but the floor was a 50 % perforated sheet under a fine mesh, which passes about 25 %. Corrected, the design collects 0.36 L per day.

| Option | For | Against |
| --- | --- | --- |
| PTFE-coated glass-fibre mesh, about 1.8 mm aperture (about 60 % open), on seven 6 x 1.5 mm aluminium bars on edge (chosen) | 59 % open; bars are stock flat bar resting on the tray lip; cheaper than the perforated sheet | Bed 6 mm higher in the tray; more emissive mesh seen from the condenser; mesh open share is an estimate |
| 70 % open expanded aluminium under a 1.5 mm mesh | Stiff, one sheet | 0.41 L per day; still a blocking sheet |
| Keep the floor and correct the calculation only | No change | 0.36 L per day |

**Decision:** the mesh on bars, 0.44 L per day (C3). The 6 mm bars raise the bed in the tray; the bed top with its absorber plate stays 7 mm below the tray rim.

### D20: the ground anchors must hold a gust (STEM S18, independent review)

At 20 m/s each anchor must hold 96 N against a 100 N rating, a margin of about 6 %; at 25 m/s it must hold 234 N. **Decision:** specify two auger anchors each rated 250 N or more of uplift in the site soil (BOM line 1; DWD-DEC-001, to confirm item 6). The design wind speed itself is open item 4 of DWD-DEC-001.

## Consequences

- Estimated cost rises from $639 to $695 (DWD-CAL-001 J1), $175 over the $520 value-engineering target. The box with everything inside is 36.1 kg; lifted with the trays and deck out it is unchanged at 23.4 kg.
- Water at the design point is 0.44 L per day, so **PR-001 is not met** (0.37 to 0.41 L under the sensitivities); 0.31 L per day at 25 % RH meets PR-002. The bed reaches 105 °C at noon; on a peak day a dry bed reaches about 133 °C and the glazing inner skin about 106 °C, inside the 130 °C rating.
- The build plan gains the absorber plates (section 3.7, step 9), the floor bars and coarser mesh (section 3.7), the coatings (sections 3.2, 3.6, 3.7), the underside paint (section 3.2) and the 250 N anchors (section 3.19).
