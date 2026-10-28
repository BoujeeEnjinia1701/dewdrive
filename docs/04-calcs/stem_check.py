"""DewDrive STEM check, DWD-STM-001 (STANDARDS section 20).

Run from the repo root after the sizing script:
    python docs/04-calcs/sizing.py        (writes docs/04-calcs/sizing_out.json, about 8 min)
    python docs/04-calcs/stem_check.py    (writes docs/04-calcs/stem_results.csv)

Each claim the design (option A) and the two other concept options (B, C; DWD-OPT-001) make is checked here
against a limit, a balance, an independent first-order estimate or a cited source. Values tagged [C3] and so
on come from the calculation note DWD-CAL-001 through sizing_out.json; the independent estimates are computed
below from first principles, so a change in the design that breaks a claim shows up when this is rerun.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from stem_check import Check, WITHIN, PLAUSIBLE, SIGMA  # noqa: E402

J = json.loads((Path(__file__).parent / "sizing_out.json").read_text())
V = J["values"]
P_ATM, R_U, M_W = 101325.0, 8.314462, 0.018015


def psat(T):
    """Saturation pressure of water, Pa (Magnus form, Alduchov and Eskridge 1996), independent of sizing.py."""
    return 610.94 * math.exp(17.625 * T / (T + 243.04))


def rho_v(T, rh):
    return rh * psat(T) * M_W / (R_U * (T + 273.15))


def dew_point(T, rh):
    g = math.log(rh) + 17.625 * T / (T + 243.04)
    return 243.04 * g / (17.625 - g)


# Conde (2004) water activity of aqueous CaCl2, same correlation as DWD-CAL-001 (Int. J. Thermal Sciences 43)
CONDE = [0.31, 3.698, 0.60, 0.231, 4.584, 0.49, 0.478, -5.20, -0.40, 0.018]


def aw_cacl2(xi, T):
    p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = CONDE
    th = (T + 273.15) / 647.1
    A = 2 - (1 + (xi / p0) ** p1) ** p2
    B = (1 + (xi / p3) ** p4) ** p5 - 1
    f = A + B * th
    pi25 = 1 - (1 + (xi / p6) ** p7) ** p8 - p9 * math.exp(-((xi - 0.1) ** 2) / 0.005)
    return pi25 * f


def xi_of_aw(aw, T):
    lo, hi = 0.0001, 0.6
    for _ in range(60):
        m = (lo + hi) / 2
        if aw_cacl2(m, T) > aw:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


c = Check(out=Path(__file__).parent / "stem_results.csv")
T_N, RH_N, RH_D, T_DAY = 20.0, 0.40, 0.25, 35.0

# ------------------------------------------------------------------------------------------- option A
c.order_of_magnitude("S1", "Night air at 20 C and 40 % RH carries about 6.92 g/m3 of water vapour [A1]", "Physics", "Thermodynamics",
                     claimed=6.92, estimate=1e3 * rho_v(T_N, RH_N), unit="g/m3", factor=1.05,
                     law="Ideal gas law on the saturation pressure (Magnus form); independent of the CAL's IAPWS fit",
                     closed_by="DWD-CAL-001 A1")
xi40 = xi_of_aw(RH_N, T_N)
c.claim("S2", "Overnight uptake of the 4 kg bed (0.54 kg [B5]) stays below its equilibrium capacity at 40 % RH (1.0 kg CaCl2 as a "
        f"{100 * xi40:.1f} wt % solution plus 0.08 kg/kg per unit activity on 3.0 kg of gel)", "Chemistry", "Physical chemistry (equilibria)",
        law="CaCl2 solution water activity (Conde 2004); salt in the pores held as solution above deliquescence",
        value=V["uptake40"], limit=1.0 * (1 - xi40) / xi40 + 3.0 * 0.08 * RH_N, unit="kg", rule="below", closed_by="DWD-CAL-001 A4, B5")
c.balance("S3", "The fan's night air supplies more vapour than the bed takes up (2.77 kg carried [B4] against 0.54 kg adsorbed [B5])",
          "Physics", "Fluid mechanics", inputs={"vapour in 40 m3/h for 10 h": 40 * 10 * rho_v(T_N, RH_N)},
          outputs={"uptake": V["uptake40"]}, unit="kg", law="Mass balance on the air stream", closed_by="DWD-CAL-001 B4, B5")
# Ergun pressure drop of the bed, independent estimate
u, dp_, eps, L, mu = 40 / 3600 / 0.785, 3.5e-3, 0.40, 9.3e-3, 1.8e-5
ergun = (150 * mu * (1 - eps) ** 2 * u / (eps ** 3 * dp_ ** 2) + 1.75 * 1.2 * (1 - eps) * u ** 2 / (eps ** 3 * dp_)) * L
c.order_of_magnitude("S4", "Drawing 40 m3/h down through the 9.3 mm beds costs about 0.16 Pa [B3], well within a 2 W, 120 mm fan "
                     "(about 3.3 Pa for the whole box [F3])", "Physics", "Fluid mechanics", claimed=V["dP_bed"], estimate=ergun, unit="Pa",
                     law="Ergun equation, 3.5 mm beads, bed voidage 0.40", closed_by="DWD-CAL-001 B3, F3")
tau_pc, a_paint = 0.78, 0.95
c.claim("S5", "The sun is absorbed on a black surface over the beds with transmittance-absorptance about 0.70 [C11]. Was 0.74 on the bare "
        "beads, which are white (absorptance about 0.3): the v0.7 design would have made 0.03 L per day [C11]; fixed with black "
        "perforated absorber plates on the beds", "Physics", "Optics and radiation",
        law="Transmittance of 10 mm twin-wall polycarbonate (about 0.78) times absorptance; a 22.7 % open black plate with light "
            "through the holes scattered back onto its underside; cannot exceed the plain black plate (0.78 x 0.95)",
        value=V["tau_alpha"], limit=tau_pc * a_paint, unit="", rule="below", closed_by="DWD-DEC-001 D16; DWD-CAL-001 C11")
c.balance("S6", "Day energy balance closes: absorbed 3.46 kWh [C7] covers desorption, loss through the glazing and heat to the condenser",
          "Physics", "Heat transfer", inputs={"absorbed": V["E_win"]},
          outputs={"desorption": V["E_des"], "glazing loss": V["E_loss"], "to condenser": V["E_bc"]}, unit="kWh",
          law="First law over the day; the remainder is sensible heat left in the bed at dusk", closed_by="DWD-CAL-001 C7")
hdes = V["E_des"] * 3.6e6 / V["uptake40"] / 1e6
c.claim("S7", f"Desorbing the night's water takes {hdes:.2f} MJ/kg, at least the latent heat of water", "Chemistry",
        "Physical chemistry (thermochemistry)", law="Heat of desorption of a salt solution is at least the latent heat (2.26 MJ/kg at 100 C)",
        value=hdes, limit=2.26, unit="MJ/kg", rule="above", closed_by="DWD-CAL-001 C7")
c.cited("S8", f"Solar-to-water efficiency of {100 * V['eff']:.1f} % [C7] for a single-stage sorption collector", "Physics", "Thermodynamics",
        law="Published outdoor results: about 9 % for a dual-stage zeolite device (LaPotin et al., Joule, 2021); a single stage recovers "
            "no latent heat, so it should sit below that; the independent review recalls single-stage devices at a few per cent (unverified)",
        detail=f"{100 * V['eff']:.1f} % below about 9 %, but high for a single stage; rests on the estimated absorber figures",
        verdict=PLAUSIBLE)
# Stefan diffusion across the gap at noon, independent estimate from the CAL's noon state
Tb, Tc = V["Tb_noon"], V["Tc_max"]
aw_noon = 0.314                                   # bed water activity at noon, CAL Table 2 (v0.8)
pb, pc = aw_noon * psat(Tb), psat(Tc)
Tm = (Tb + Tc) / 2 + 273.15
D = 2.5e-5 * (Tm / 293.15) ** 1.75
flux = M_W * P_ATM / (R_U * Tm) * D / 0.128 * math.log((P_ATM - pc) / (P_ATM - pb))
rate = flux * 0.785 * V["open_vap"] * 3600
c.order_of_magnitude("S9", f"Vapour crosses the gap and the drip screen to the condenser at about {V['rate_max_kg_h'] * 1e3:.0f} g/h at its peak "
                     f"(C2); the tray floor lets {100 * V['open_vap']:.0f} % of the bed area through. Was 60 % for a 50 % perforated sheet under a "
                     "fine mesh, about 25 % in fact (independent review); fixed with an open floor of bars and a coarser mesh", "Physics", "Heat transfer",
                     claimed=V["rate_max_kg_h"] * 1e3, estimate=1e3 * rate, unit="g/h", factor=2.0,
                     law="Stefan diffusion through still air over the open share of the tray floor; hot over cold and moist (light) over dry is "
                         "stably stratified; estimate taken at the noon state of the v0.8 day table", closed_by="DWD-DEC-001 D19; DWD-CAL-001 C2")
c.claim("S10", "Condensation happens: at noon saturation at the condenser plate (value) is below the bed's vapour pressure (limit)", "Physics", "Thermodynamics",
        law="Vapour pressure of the bed (water activity x saturation at bed temperature) against saturation at the plate",
        value=pc / 1e3, limit=pb / 1e3, unit="kPa", rule="below", closed_by="DWD-CAL-001 C2")
# condenser: vertical-plate natural convection and radiation from a painted fin envelope
dT = 12.0
Ra = 9.81 * (1 / 308.0) * dT * 0.1 ** 3 / (1.6e-5 * 2.25e-5)
h_vp = 0.59 * Ra ** 0.25 * 0.0265 / 0.1
c.cited("S11", f"Fins shed heat by natural convection at about {V['hc12']:.1f} W/(m2 K) [C8], holding the condenser within 15 K of the air",
        "Physics", "Heat transfer", law=f"Laminar isolated vertical plate, Nu = 0.59 Ra^0.25, gives {h_vp:.1f} W/(m2 K); but the fins hang "
        "under a hot, tilted, downward-facing floor that traps warm air (independent review): 30 % less convection gives about 14 K, "
        "and also half the radiation about 16 K", detail="PR-005 at risk; condenser temperature to be logged at TRL 4", verdict=PLAUSIBLE)
h_r = 4 * 0.85 * SIGMA * (273.15 + 41) ** 3
c.claim("S12", "The finned underside also radiates to the shaded ground as an envelope of emissivity 0.85 (C8). Bare aluminium fins "
        "(emissivity about 0.1) would not; fixed by painting the fins and plate underside with a matt high-emissivity paint",
        "Physics", "Optics and radiation", law="Radiation from a grey envelope, h_r = 4 eps sigma T^3; painted metal about 0.9",
        value=0.85, limit=0.90, unit="emissivity", rule="below", closed_by="DWD-DEC-001 D18")
c.claim("S13", f"On a peak day (1000 W/m2, 40 C air) a dry bed stagnates near {V['Ts_peak']:.0f} C and the glazing inner skin near "
        f"{V['T_glaz_in_peak']:.0f} C [D6], below the 130 C rating of the specified glazing (was checked as the bed at 785 W/m2; "
        "independent review)", "Chemistry", "Materials and polymer chemistry",
        law="Polycarbonate service rating applies to the sheet; inner skin from the film model of DWD-CAL-001 D2; DWD-DEC-001 decision of 2026-10-02",
        value=V["T_glaz_in_peak"], limit=130.0, unit="C", rule="below", closed_by="DWD-CAL-001 D6")
c.claim("S14", f"Surfaces touched in normal use stay at or below 60 C: glazing outer skin {V['T_glaz_out']:.0f} C, fins {V['T_fin']:.0f} C [D2, D3]",
        "Biology", "Human physiology and biomechanics",
        law="PR-013 touch limit of 60 C; contact burn thresholds depend on material and contact time (EN ISO 13732-1, values to confirm)",
        value=max(V["T_glaz_out"], V["T_fin"]), limit=60.0, unit="C", rule="below", closed_by="DWD-CAL-001 D2, D3")
c.claim("S15", f"After one 90 % RH night the salt solution fills {100 * V['fill_90']:.0f} % of the gel's pores [E3], so no brine drains out",
        "Chemistry", "Physical chemistry (equilibria)", law="Solution volume (Conde activity, solution density) against 3.0 L of pore volume",
        value=V["fill_90"], limit=1.0, unit="of pore volume", rule="below", closed_by="DWD-CAL-001 E3")
c.claim("S16", f"The fan's {100 * V['rh_off']:.0f} % RH cut-out (restart below {100 * V['rh_on']:.0f} %) sits below the {100 * V['rh_fill']:.0f} % RH at which the pores fill at equilibrium [E2]", "Engineering and technology",
        "Control", law="Logger rule against the pore-filling humidity; lowered from 70 % RH, 1 point below pore filling and inside a low-cost sensor's tolerance, by Amish on 2026-10-25 (DWD-DEC-001 item 3)",
        value=V["rh_off"], limit=V["rh_fill"], unit="RH", rule="below", margin=0.05, closed_by="DWD-CAL-001 E3 to E5; DWD-DEC-001 item 3")
c.balance("S17", "The 10 W panel covers the fan and logger: 23.6 Wh per day of load [F1]", "Engineering and technology", "Power and link budgets",
          inputs={"PV 10 W x 5 h x 0.70": 10 * 5 * 0.70}, outputs={"fan 2 W x 10 h": 20.0, "logger 0.15 W x 24 h": 3.6}, unit="Wh",
          law="Daily energy budget", closed_by="DWD-CAL-001 F1, F2")
q_w = 0.5 * 1.2 * 20 ** 2
c.claim("S18", f"Two ground anchors each rated 250 N in uplift hold the unit in a 25 m/s gust; each must carry {V['anchor25_N']:.0f} N "
        f"[H4] ({V['anchor_N']:.0f} N at the earlier 20 m/s [H5]). Was 100 N, a 6 % margin at 20 m/s (independent review)",
        "Physics", "Mechanics and statics", law="Dynamic pressure, force coefficient 1.2 on 1.1 m2, overturning about the downwind legs "
        "with a factor of 1.5; anchor rating in the site soil to confirm when bought; design wind speed a 25 m/s gust until the site value is known (decided by Amish 2026-10-25, DWD-DEC-001 item 4)",
        value=V["anchor25_N"], limit=250.0, unit="N", rule="below", margin=0.10)
I_bar = 5 * 20 ** 3 / 12
w_line = 52.0 / 1016
M_bar = w_line * 1016 ** 2 / 8
c.claim("S19", "The 20 x 5 mm deck bars carry the trays, sorbent, water, absorbers and screens (about 52 N on the centre bar over 1,016 mm)",
        "Physics", "Strength of materials", law="Simply supported bar, sigma = M / (I / c); 6063-T5 aluminium yield about 110 MPa with a factor of 2",
        value=M_bar / (I_bar / 10), limit=110 / 2, unit="MPa", rule="below", closed_by="DWD-DEC-001, to confirm item 8")
c.cited("S20", "Brine-wetted parts survive hot CaCl2 solution: tray insides, floors, absorbers and drip screens in black PTFE-coated aluminium, "
        "the floor mesh PTFE-coated glass fibre. Was bare aluminium and a stainless woven mesh, which pit in chloride brine and, above "
        "about 60 C, risk chloride stress corrosion cracking", "Chemistry", "Electrochemistry and batteries",
        law="Chloride pitting of aluminium; chloride stress corrosion cracking of 304 and 316 is rare below 60 C (SSINA), the beds run to "
            "about 110 C; PTFE is inert to CaCl2 and rated to 260 C",
        detail="Bare metal fails the 300-cycle life; coated parts within known science, coating damage carried in the design FMEA",
        verdict=WITHIN, closed_by="DWD-DEC-001 D17")
c.cited("S21", "The composite keeps 80 % or more of its capacity over 300 cycles", "Chemistry", "Materials and polymer chemistry",
        law="CaCl2 does not decompose below about 175 C; ordinary silica gel can crack when wetted with solution, so a water-resistant grade "
            "is specified (DWD-DEC-001, to confirm item 1)", detail="Cycling test needed (TRL 4)", verdict=PLAUSIBLE)
c.cited("S22", f"The lumped bed model holds although heat enters at the plate on top: about {V['dT_grad']:.0f} K drop through the 9.3 mm bed "
        f"at noon; desorbing at the mid-depth temperature the yield is {V['collected_grad']:.2f} L per day [C12]", "Mathematics",
        "Numerical method", law="Conduction through a packed bed, k about 0.2 W/(m K)",
        detail=f"Yield falls from {V['collected40']:.2f} to {V['collected_grad']:.2f} L per day; PR-001 at risk under this sensitivity",
        verdict=PLAUSIBLE, closed_by="DWD-CAL-001 C12")
c.cited("S23", "Condensate chloride stays below 250 mg/L: brine cannot reach the plate (pores never fill, sumps, no line of sight)",
        "Chemistry", "Analytical chemistry", law="EU Directive 2020/2184 indicator value 250 mg/L; WHO taste threshold about 250 mg/L",
        detail="Water test needed (TRL 4)", verdict=PLAUSIBLE)
c.cited("S24", "Collected water is free of harmful microbes once treated; the device itself is not a treatment step", "Biology", "Microbiology",
        law="Condensate is near distilled but picks up dust and microbes from surfaces and the bottle; boiling or disinfection before drinking",
        detail="Documents require treatment before drinking; laboratory test needed (TRL 4)", verdict=PLAUSIBLE)
c.cited("S26", f"Pessimistic combination of the calculation's uncertainties (bed temperature drop and half the light through the absorber "
        f"holes absorbed): {V['collected_pess']:.2f} L per day [C13] against {V['collected40']:.2f} on the lumped model", "Mathematics",
        "Statistics and uncertainty", law="Independent review: the sensitivities were never combined",
        detail="PR-001 not met on paper; range to be narrowed by measuring absorptance and isotherms (TRL 4)", verdict=PLAUSIBLE,
        closed_by="DWD-CAL-001 C13")
c.cited("S27", "Parts near the hot interior stay inside their ratings on a peak day (bed about 133 C): plywood and PIR walls, EPDM seals, "
        "silicone, PTFE coatings", "Chemistry", "Materials and polymer chemistry",
        law="Gap air at about the mean of bed and air (about 85 C); fan, battery and electronics are outside the box; PTFE 260 C, "
            "silicone and EPDM typically above 130 C, PIR and plywood ratings to confirm with suppliers",
        detail="Supplier ratings to confirm (DWD-DEC-001, to confirm item 12)", verdict=PLAUSIBLE)
closure = V["E_win"] - V["E_des"] - V["E_loss"] - V["E_bc"]
c.claim("S25", f"The yield simulation conserves energy: unaccounted heat at dusk {closure:.2f} kWh is sensible heat left in the bed",
        "Mathematics", "Units and dimensional analysis", law="Sensible heat of the bed, trays and absorbers (about 7 kJ/K) over its rise at dusk",
        value=closure, limit=7.5e3 * (71.0 - 25.0) / 3.6e6 * 1.5, unit="kWh", rule="below", closed_by="DWD-CAL-001 C7")
# ------------------------------------------------------------------------------------------- option B
eps_sky = 0.711 + 0.56 * (dew_point(T_N, RH_N) / 100) + 0.73 * (dew_point(T_N, RH_N) / 100) ** 2
Ta = T_N + 273.15
Ts = Ta
for _ in range(200):     # panel energy balance: net radiation to sky = convective gain (h 5 W/(m2 K))
    q_rad = 0.95 * SIGMA * (Ts ** 4 - eps_sky * Ta ** 4)
    Ts += (5.0 * (Ta - Ts) - q_rad) / 40
depress = Ta - Ts
c.order_of_magnitude("B1", f"Option B: a high-emissivity panel under a clear night sky runs about 10 K below the air", "Physics", "Optics and radiation",
                     claimed=10.0, estimate=depress, unit="K", law=f"Net radiation to a sky of emissivity {eps_sky:.2f} (Berdahl and Martin) "
                     "against convection at 5 W/(m2 K)", closed_by="DWD-OPT-001")
c.claim("B2", f"Option B makes no water at the design point: the panel ({T_N - depress:.1f} C) stays above the dew point "
        f"({dew_point(T_N, RH_N):.1f} C at 40 % RH; {dew_point(T_N, RH_D):.1f} C at 25 %)", "Physics", "Thermodynamics",
        law="Dew forms only on a surface below the dew point; field data show no condensation below about 71 % RH (Atashi et al., 2021)",
        value=dew_point(T_N, RH_N), limit=T_N - depress, unit="C", rule="below", closed_by="DWD-OPT-001")
# ------------------------------------------------------------------------------------------- option C
xi_n = xi_of_aw(RH_N, T_N)
salt, area, hm = 2.7, 3.2, 2.1e-3                    # kg CaCl2 in 9 kg of 30 % brine; wetted cloth both faces, m2; m/s


def option_c_night(T_cloth, T_glaz=50.0):
    """Brine regenerated against glazing at T_glaz with cloth at T_cloth, then a 10 h night at 40 % RH."""
    xi_d = max(xi_of_aw(psat(T_glaz) / psat(T_cloth), T_cloth), xi_n)
    W = salt * (1 - xi_d) / xi_d
    up = 0.0
    for _ in range(600):                             # 10 h night in 60 s steps
        xi = salt / (salt + W)
        mdot = hm * area * max(rho_v(T_N, RH_N) - aw_cacl2(xi, T_N) * psat(T_N) * M_W / (R_U * (T_N + 273.15)), 0.0)
        W += mdot * 60
        up += mdot * 60
    return xi_d, up


xi80, up80 = option_c_night(80.0)
xi70, up70 = option_c_night(70.0)
c.order_of_magnitude("C1", "Option C: with the cloth at 80 C and the glazing at 50 C the brine dries to about 52 wt %, and takes up about "
                     "0.7 kg overnight at 40 % RH by natural convection", "Chemistry", "Physical chemistry (equilibria)", claimed=0.7, estimate=up80,
                     unit="kg", law=f"Regeneration ends where aw x psat(cloth) = psat(glazing): {100 * xi80:.0f} wt %; night equilibrium {100 * xi_n:.1f} wt %; "
                         "mass transfer 2.1 mm/s on 3.2 m2 of cloth (estimate)", closed_by="DWD-OPT-001")
c.order_of_magnitude("C2", f"Option C's yield hinges on the cloth temperature: with the cloth at 70 C the brine dries only to about 44 wt % "
                     "and takes up about 0.27 kg overnight", "Physics", "Thermodynamics", claimed=0.27, estimate=up70, unit="kg",
                     law=f"Same balance with psat(50 C) / psat(70 C): {100 * xi70:.1f} wt % against {100 * xi_n:.1f} wt % at night",
                     closed_by="DWD-OPT-001")
c.order_of_magnitude("C3", "Option C collects about 0.2 L per day (cloth at 70 C) to 0.5 L per day (cloth at 80 C) at the design point, "
                     "far below the 2.5 L per m2 per day reported for unstated test conditions (Kabeel, 2007)", "Physics",
                     "Thermodynamics", claimed=0.5, estimate=0.7 * up80, unit="L/day",
                     law=f"Solar still collection efficiency about 0.7 (estimate): {0.7 * up70:.2f} to {0.7 * up80:.2f} L per day",
                     closed_by="DWD-OPT-001")
state = c.write()
print(f"option C: regenerated {100 * xi80:.1f} wt % (80 C) or {100 * xi70:.1f} wt % (70 C), night equilibrium {100 * xi_n:.1f} wt %, uptake {up80:.2f} or {up70:.2f} kg; "
      f"option B: depression {depress:.1f} K, sky emissivity {eps_sky:.3f}")
