---
doc_id: DWD-PLN-001
title: DewDrive project plan
project: DewDrive
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First plan (kit 1.8 pipeline), with the reference list of every source cited in the repo
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Open items 3 and 4 decided by Amish (2026-10-25)'
---

# DewDrive project plan

DewDrive is at stage P3 (design outputs) and TRL 3: the constructable design, its calculation note, drawings, priced BOM, build plan, STEM check, concept options, requirements and pipeline documents all exist. The next gate, P4 (verification, TRL 4), is on hold while the portfolio cap is TRL 3. The decisions requested now are the concept selection of DWD-DDR-004 (options A and B within 10 % on the weighted score) and how to recover PR-001 (0.44 L per day against 0.5; DWD-DEC-001, open item 2). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and STEM check | Design lead | DWD-STM-001, DWD-OPT-001, DWD-DDR-004, DWD-DDR-005 | Done at P3; STEM check open on 7 rows that need tests, logs or supplier ratings |
| Requirements | Design lead | DWD-URS-001, DWD-PRS-001, DWD-RTM-001 | Done at P3; targets to confirm with the partner |
| Calculation and CAD | Design lead | DWD-CAL-001 v0.8; `cad/src/model.py` at D3 for options A to C; drawings; STEP | Done at P3 |
| Build plan and BOM | Design lead | DWD-BLD-001; `bom/bom.csv` | Done at P3; quotes for the estimated lines |
| Regulatory, risk and market | Design lead | DWD-REG-001, DWD-RSK-001, DWD-MKT-001, DWD-FEA-001 | First pass done; "to assess" items open |
| Partner and site | Amish | Agreement with a dryland field station; site humidity and sun record | Not started (partner type decided 2026-10-02) |
| Verification (P4) | Partner and design lead | Isotherm and absorptance measurements, prototype build, chamber and field tests, water test | On hold (TRL cap 3) |

## Resources needed

Table 2. Resources (P4 resources are planned work, on hold).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts | One unit to DWD-BLD-001 | | 695 (BOM, estimate) |
| Sheet-metal and joinery workshop | Box, trays, deck, screens, stand | About 5 days | To assess with the workshop |
| Coating shop | PTFE coatings of trays, floors, absorbers, screens | One batch | Included in the BOM estimate; to quote |
| Laboratory (partner or university) | Isotherms of the composite at 20 °C and 80 to 120 °C; absorptance of the absorber over the beads | About 2 weeks | To assess |
| Water-testing laboratory | Chloride, aluminium and microbiological tests of the condensate | One set per site | To assess |
| Field station | Site, weather record, 30 days of logged operation | 1 month or more | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Reached (documents added 2026-10-25) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Reached |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed, feasibility closed | Reached, except: concept selection awaiting Amish (DWD-DDR-004); STEM check open on 7 rows that only tests, logs or supplier ratings can close; PR-001 not met on paper |
| P3 Design outputs | Model, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability complete | Reached (TRL 3) |
| P4 Verification | Test plans and lab reports, verification report, RSK updated | On hold (TRL cap 3) |
| P5 Validation | Field trials with a partner, human factors, certification status | On hold |
| P6 Commercialization | Launch plan with a named deployment partner | On hold |

## Next steps and decision requested

1. **Decisions requested (Amish):** concept selection, DWD-DDR-004 (B 120 and A 117 of 170; option B makes no water at the design point); recovery of PR-001 (DWD-DEC-001, open item 2); fan cut-out and design wind speed (open items 3 and 4) were decided by Amish on 2026-10-25: 65 % RH with restart below 60 %, and a 25 m/s gust until the site value is known.
2. When the TRL cap lifts: measure the composite's isotherms, the absorber's absorptance and the mesh's open share first, because PR-001 is already short on paper.
3. Approach two or three dryland field stations for the first site (risk P3).
4. Get quotes for the estimated BOM lines (coatings, mesh, absorber sheet, glazing grade).

## References

- Alduchov, O. A., and R. E. Eskridge. "Improved Magnus Form Approximation of Saturation Vapor Pressure." *Journal of Applied Meteorology* 35 (1996): 601 to 609.
- Al Jazeera. "Women Lead the Way out of Poverty in an Indian Desert." November 19, 2015. https://www.aljazeera.com/gallery/2015/11/19/women-lead-the-way-out-of-poverty-in-an-indian-desert.
- Aristov, Y. I., et al. Calcium chloride confined in mesoporous silica gel (SWS-1L). *Chemical Engineering Science*, 2006. https://www.sciencedirect.com/science/article/abs/pii/S0009250905007050.
- Atashi, N., et al. "Delineation of Dew Formation Zones in Iran Using Long-Term Model Simulations and Cluster Analysis." *Hydrology and Earth System Sciences* 25 (2021): 4719 to 4740. https://hess.copernicus.org/articles/25/4719/2021/hess-25-4719-2021.html (checked 2026-10-25).
- Carter, V., et al. *Frontiers in Environmental Science*, 2025. https://doi.org/10.3389/fenvs.2025.1537058.
- Conde, M. R. "Properties of Aqueous Solutions of Lithium and Calcium Chlorides: Formulations for Use in Air Conditioning Equipment Design." *International Journal of Thermal Sciences* 43 (2004).
- European Union. Directive (EU) 2020/2184, Annex I. https://gesetze.legal/eu/rl_2020_2184_eu/anhang_i (checked 2026-10-25).
- Fathieh, F., et al. "Practical Water Production from Desert Air." *Science Advances*, 2018. https://www.science.org/doi/10.1126/sciadv.aat3198.
- Kabeel, A. E. "Water Production from Air Using Multi-Shelves Solar Glass Pyramid System." *Renewable Energy* 32, no. 1 (2007): 157 to 172. https://ideas.repec.org/a/eee/renene/v32y2007i1p157-172.html (checked 2026-10-25).
- Kallenberger, P. A., and M. Fröba. Alginate-derived CaCl₂ composite for water harvesting. *Communications Chemistry*, 2018. https://www.nature.com/articles/s42004-018-0028-9.
- Kart, J. "SOURCE Solar-Powered Hydropanels Can Produce Up to 5 Liters of Drinking Water per Day." *Forbes*, January 13, 2022. https://www.forbes.com/sites/jeffkart/2022/01/13/solar-powered-source-hydropanels-can-produce-up-to-5-liters-of-drinking-water-per-day/.
- Kim, H., et al. "Water Harvesting from Air with Metal-Organic Frameworks Powered by Natural Sunlight." *Science*, 2017. https://doi.org/10.1126/science.aam8743.
- Kim, H., S. R. Rao, E. A. Kapustin, L. Zhao, S. Yang, O. M. Yaghi and E. N. Wang. "Adsorption-Based Atmospheric Water Harvesting Device for Arid Climates." *Nature Communications* 9 (2018): 1191. https://doi.org/10.1038/s41467-018-03162-7 (checked 2026-10-25).
- LaPotin, A., et al. "Dual-Stage Atmospheric Water Harvesting Device for Scalable Solar-Driven Water Production." *Joule*, 2021. https://www.sciencedirect.com/science/article/pii/S254243512030444X.
- Native News Online and US Senate Committee on Indian Affairs, oversight hearing of September 27, 2023. https://www.indian.senate.gov/hearings/oversight-hearing-on-water-as-a-trust-resource-examining-access-in-native-communities/.
- SaltWiki. "Calcium Chloride." https://www.saltwiki.net/index.php/Calcium_chloride.
- Shao, Z., et al. Passive LiCl and silica gel harvester. *Energy*, 2024. https://www.sciencedirect.com/science/article/abs/pii/S0360544224016906.
- Sigma-Aldrich. *Safety Data Sheet: Calcium Chloride Dihydrate*, version 4.5, 2014. https://isolab.ess.washington.edu//laboratory/safety/sds/calcium_chloride.pdf (checked 2026-10-25).
- Silica Gel Italia. 25 kg drum of white spherical silica gel. https://www.silica-gel.it/en/spherical-white-silica-gel/153-beaded-white-silica-gel-bulk-drum-20-kg.html (checked 2026-10-25).
- Specialty Steel Industry of North America (SSINA). "Chloride Stress Corrosion Cracking." https://www.ssina.com/education/corrosion/chloride-stress-corrosion-cracking/ (checked 2026-10-25).
- UNICEF. "Collecting Water Is Often a Colossal Waste of Time for Women and Girls." 2016. https://www.unicef.org/press-releases/unicef-collecting-water-often-colossal-waste-time-women-and-girls.
- UNICEF Jordan and UNICEF Kenya, water, sanitation and hygiene pages. https://www.unicef.org/jordan/water-sanitation-and-hygiene; https://www.unicef.org/kenya/water-sanitation-and-hygiene.
- USPTO. "A Solar Life." https://www.uspto.gov/learning-and-resources/journeys-innovation/historical-stories/solar-life; Telkes, M. US Patent 3,415,719. https://patents.google.com/patent/US3415719A/en.
- Watergen. "GENNY Home." https://watergen.com/product-page-genny-home/ (checked 2026-10-25).
- Wikipedia. "Low Voltage Directive." https://en.wikipedia.org/wiki/Low_Voltage_Directive (checked 2026-10-25).
- World Health Organization. *Chloride in Drinking-Water.* https://cdn.who.int/media/docs/default-source/wash-documents/wash-chemicals/chloride-fs-new.pdf (checked 2026-10-25); "Drinking-Water" fact sheet, https://www.who.int/news-room/fact-sheets/detail/drinking-water; *How Much Water Is Needed in Emergencies*, technical note 9, https://cdn.who.int/media/docs/default-source/wash-documents/who-tn-09-how-much-water-is-needed.pdf.
