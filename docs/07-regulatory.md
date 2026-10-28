---
doc_id: DWD-REG-001
title: DewDrive regulatory and standards register
project: DewDrive
doc_type: Regulatory register
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First register (kit 1.8 pipeline); sources checked 2026-10-25
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'G12: design gust 25 m/s (item 4, 2026-10-25)'
---

# DewDrive regulatory and standards register

DewDrive makes water that people may drink, handles a corrosive salt and carries a small lithium battery, so three sets of rules matter: drinking-water quality, materials in contact with the water, and the bought electrical parts. The open design itself is not placed on any market; rules on selling products apply to whoever builds and sells a unit. This register is not legal advice; anything marked "to assess" needs a qualified reviewer before any claim about the water or the product. Method: STANDARDS section 23. Sources checked 2026-10-25 where a link is given; standards named without a link were not opened in this session and are "to assess".

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | WHO *Guidelines for Drinking-Water Quality* and the WHO chloride fact sheet | International | Health-based guideline values; chloride has no health-based value, taste becomes detectable above about 250 mg/L | Reference for the collected water (PR-006); the device is not a treatment step and the documents require treatment before drinking | Partner NGO (water testing) | Applies as guidance; water test at TRL 4 |
| G2 | Directive (EU) 2020/2184 on water intended for human consumption, Annex I Part C | European Union | Indicator values: chloride 250 mg/L, aluminium 200 µg/L | Reference limits for chloride carry-over and aluminium from the condenser (PR-006); the national rule of the partner's country applies in practice | Partner NGO; local water authority | Applies as reference limit; national rule to assess |
| G3 | Regulation (EC) No 1935/2004 (food-contact materials) and Regulation (EU) No 10/2011 (plastics) | European Union | Materials in contact with food and drinking water | Wetted parts: food-safe coating on the condenser top, gutter sealant, silicone drain tube, HDPE jerrycan (PR-006) | Design lead; supplier declarations | To assess: obtain supplier declarations of compliance |
| G4 | NSF/ANSI/CAN 61, drinking water system components | United States and Canada | Health effects of materials in contact with drinking water | Same wetted parts as G3, for a North American build | Design lead | To assess |
| G5 | GHS classification of calcium chloride (supplier safety data sheet) | International | Skin irritation category 2 (H315) and eye irritation category 2A (H319) | Preparing the sorbent and emptying the brine sumps: gloves and eye protection (build plan, safety stops) | Builder; user | Applies; met by the safety notes and PPE |
| G6 | Food-additive grade calcium chloride (E 509 in the EU) | European Union (other countries have equivalents) | Purity of CaCl₂ sold for food use | The sorbent salt is bought food grade (BOM line 5), so trace impurities that could volatilise are limited | Builder | Applies by specification |
| G7 | UN Manual of Tests and Criteria, section 38.3 (lithium battery transport) | International | Test summary required to ship lithium cells and batteries | The bought 12.8 V 6 Ah LiFePO4 battery (BOM line 12) | Supplier; builder | To assess: obtain the supplier's UN 38.3 test summary |
| G8 | IEC 62133-2, safety of portable secondary lithium cells and batteries | International | Battery safety tests | The bought battery with its BMS | Supplier | To assess: supplier certificate |
| G9 | Low Voltage Directive 2014/35/EU | European Union | Electrical equipment rated 50 to 1,000 V AC or 75 to 1,500 V DC | The device runs at 12.8 V DC | None | Does not apply |
| G10 | Radio Equipment Directive 2014/53/EU (and FCC rules in the United States) | European Union; United States | Radio equipment placed on the market | The ESP32 logger has Wi-Fi and Bluetooth radio; a pre-certified module is specified | Builder who places a unit on the market | Does not apply to the open design; certification needed later for any sale |
| G11 | IEC 61215 and IEC 61730 (PV module design and safety qualification) | International | PV module performance and safety | The bought 10 W panel (BOM line 11) | Supplier | To assess: supplier certificate |
| G12 | EN 1991-1-4, wind actions on structures | Europe (national annexes) | Design wind speeds and force coefficients | The 25 m/s design gust (decided by Amish 2026-10-25, until the site value is known) and force coefficient in DWD-CAL-001 section H are first-order; the site wind speed comes from the national annex or local code | Design lead | To assess for the partner site |
| G13 | EN ISO 13732-1, contact with hot surfaces | International | Burn thresholds by surface material and contact time | The 60 °C touch limit of PR-013 and the hot interior of the box | Design lead | To assess: confirm the threshold values against the standard |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- World Health Organization. *Chloride in Drinking-Water: Background Document for Development of WHO Guidelines for Drinking-Water Quality.* https://cdn.who.int/media/docs/default-source/wash-documents/wash-chemicals/chloride-fs-new.pdf (checked 2026-10-25).
- European Union. Directive (EU) 2020/2184 of the European Parliament and of the Council of 16 December 2020 on the quality of water intended for human consumption, Annex I. https://gesetze.legal/eu/rl_2020_2184_eu/anhang_i (checked 2026-10-25).
- Wikipedia. "Low Voltage Directive." https://en.wikipedia.org/wiki/Low_Voltage_Directive (checked 2026-10-25).
- Sigma-Aldrich. *Safety Data Sheet: Calcium Chloride Dihydrate*, version 4.5, 2014. https://isolab.ess.washington.edu//laboratory/safety/sds/calcium_chloride.pdf (checked 2026-10-25).
- Regulation (EC) No 1935/2004, Regulation (EU) No 10/2011, NSF/ANSI/CAN 61, UN Manual of Tests and Criteria section 38.3, IEC 62133-2, Directive 2014/53/EU, IEC 61215, IEC 61730, EN 1991-1-4 and EN ISO 13732-1: named by title; not opened in this session (to assess).
