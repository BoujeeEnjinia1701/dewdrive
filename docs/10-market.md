---
doc_id: DWD-MKT-001
title: DewDrive market and viability
project: DewDrive
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First market and viability note (kit 1.8 pipeline); prices checked 2026-10-25
---

# DewDrive market and viability

DewDrive is for arid households, schools and clinics that carry or buy their drinking water, and for the researchers and NGOs who want comparable yield data; it competes with sealed solar hydropanels at about $2,000 a panel and with grid-powered atmospheric water generators. An open design matters because the people who need it cannot buy or repair a sealed product, and because published yields vary so much that only logged, comparable units can show where it is worth building. Prices and benchmarks were checked on 2026-10-25 unless another date is given. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Arid households | Households carrying or buying water in hot semi-arid regions with night humidity of 25 to 40 % (DWD-PRB-001) | SOURCE solar hydropanel: about $2,000 per panel for about 3 to 5 L per day (Forbes, 2022); sealed, not locally repairable | 695 in parts (DWD-CAL-001 J1), plus local labour | About a third of a hydropanel's price, built and repaired locally; about $0.87 per litre over 5 years in parts at 0.44 L per day, against a hydropanel's higher output |
| Schools and clinics | Sites with staff on hand twice a day and a delivered supply that runs short | Watergen GENNY home atmospheric water generator: up to 20 L per day, 550 W nominal and about 400 Wh per litre at 26.7 °C and 60 % RH; price not listed (Watergen); needs grid power and humid air | 695 | No grid, works at 25 to 40 % RH where refrigeration-type generators give little |
| Researchers and NGOs | University field stations and WASH programmes comparing sorbents and sites | No open, logged reference device found; the field station partner type was decided on 2026-10-02 | 695 | Open model, calculation and logger; the sorbent can be swapped for MOF or other composites later |

The parts are ordinary: white silica gel beads sell at retail for about €313 per 25 kg drum, VAT included, about €12.50 per kilogram (silica-gel.it), against the $8 per kilogram estimate in the BOM, so the sorbent line may rise by about $15 at small-quantity retail prices; food-grade CaCl₂ is a common food additive (E 509). The cost per litre of carried or trucked water in the partner's region is to assess with the partner.

## Open route

Local sheet-metal and joinery workshops build the box, trays and stand from the build plan; a coating shop applies the PTFE coatings; electronics distributors supply the panel, battery and logger parts. University field stations run the first units and publish logged yields; water and sanitation NGOs carry the design to schools and households where the data show it is worth the money. CERN-OHL-S-2.0 keeps changes to the hardware open and MIT keeps the scripts open, and the parametric model lets a site change the box size, tilt or sorbent and rerun the numbers.

## Sources

- Kart, J. "SOURCE Solar-Powered Hydropanels Can Produce Up to 5 Liters of Drinking Water per Day." *Forbes*, January 13, 2022. https://www.forbes.com/sites/jeffkart/2022/01/13/solar-powered-source-hydropanels-can-produce-up-to-5-liters-of-drinking-water-per-day/ (cited in DWD-PRB-001).
- Watergen. "GENNY Home" product page. https://watergen.com/product-page-genny-home/ (checked 2026-10-25).
- Silica Gel Italia. "25 kg Bulk Silica Gel, White Spherical, Drum." https://www.silica-gel.it/en/spherical-white-silica-gel/153-beaded-white-silica-gel-bulk-drum-20-kg.html (checked 2026-10-25).
