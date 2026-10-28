---
doc_id: DWD-URS-001
title: DewDrive user requirements
project: DewDrive
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First issue (kit 1.8 pipeline), drawn from the users and stakeholders in DWD-PRB-001 v0.8
---

# DewDrive user requirements

These are the needs of the people DewDrive is for, written from their side. They come from the users and stakeholders in the problem statement (DWD-PRB-001, Tables 1 and 2) and are proposals until co-design sessions with the first partner confirm them. The product requirements that answer them are in DWD-PRS-001 (`03-requirements.md`), and the links are in the generated traceability matrix DWD-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Daily water in the dry season | I get a useful daily supplement of drinking water from the air on a typical dry-season night (about 40 % RH) | High | Rural household; school or clinic (PRB Table 1) |
| UR-002 | Performance | Water on the driest nights | I still get some water on the driest nights (about 25 % RH) | Medium | Rural household (PRB Table 1) |
| UR-003 | Usability | Little daily effort | Running it takes two short actions a day that anyone in the household or school can do | High | Rural household; school or clinic |
| UR-004 | Safety | Water I can make safe | The water it makes contains nothing that simple boiling or disinfection cannot make safe to drink | High | Rural household; water and sanitation NGO (PRB Table 2) |
| UR-005 | Safety | No harm to people | Nobody, including children, can be burned, hurt by chemicals or get an electric shock in normal use | High | School or clinic; rural household |
| UR-006 | Environment and durability | Survives an unattended site | It survives sun, dust, wind, rain and animals at a site visited only twice a day | High | Rural household; field station (PRB Table 2) |
| UR-007 | Deployment and assembly | Two people can move and set it up | Two people can carry it in parts and set it up with a spanner and a screwdriver | Medium | Local technician; rural household |
| UR-008 | Logistics | No fuel, no grid | It runs on sunlight alone, with no fuel and no grid connection | High | Rural household (PRB constraints) |
| UR-009 | Maintenance | Built and repaired locally | A local workshop can build and repair it from parts sold by general suppliers, with common tools | High | Local technician or maker; local workshops (PRB Table 2) |
| UR-010 | Cost | Worth the money | The parts cost is low enough that the water is worth it compared with carrying or buying water | High | Rural household; NGO |
| UR-011 | Performance | Comparable yield records | Each unit records its own yield and weather so that sites can be compared | Medium | Researcher or NGO; field station |
| UR-012 | Safety | Salt stays out of the water | The drying salt never gets into the drinking water or spills onto people | High | Rural household; water and sanitation NGO |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.

> **Safety:** UR-004, UR-005 and UR-012 exist because of hazards: untreated water, hot surfaces inside the box, a corrosive salt solution and a small lithium battery. They cannot be waived without a documented decision by Amish.
