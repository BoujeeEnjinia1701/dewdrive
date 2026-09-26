"""DewDrive sizing calculations, DWD-CAL-001 v0.2.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on,
and writes docs/04-calcs/results.csv (the requirement table).

First-principles estimates for a paper proof of concept (TRL 3). Not a substitute for
measured isotherms, a test or an engineering review. The geometry comes from
cad/src/model.py (PARAMS and derived()), prices from bom/bom.csv.

v0.2 checks the design of record after DWD-DDR-002 (recommendations accepted by Amish,
2026-09-25): night air drawn down through the sealed, mesh-floored trays; 25 wt % CaCl2
(1.0 kg in 3.0 kg of gel); a louvred drip screen under each tray; the fan stopped above 70 % RH.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS, derived, volumes_cm3  # noqa: E402

G = derived()
OUT = {}


def say(tag, text, value=None):
    OUT[tag] = value
    print(f"[{tag}] {text}")


# ============================================================================================
# Constants and properties
R_U = 8.314462            # J/(mol K)
M_W = 0.018015            # kg/mol, water
R_V = R_U / M_W           # 461.5 J/(kg K)
P_ATM = 101325.0
SIGMA = 5.670e-8
CP_AIR, RHO_AIR, K_AIR, NU_AIR = 1006.0, 1.18, 0.0262, 1.6e-5
D_V20 = 2.5e-5            # vapour diffusivity in air at 20 C, m2/s (scaled with T^1.75)
H_FG = 2.45e6             # latent heat near 20 to 50 C, J/kg


def psat(T):
    """Saturation pressure of water, Pa, T in C (IAPWS-IF97 region 4)."""
    n = [0.11670521452767e4, -0.72421316703206e6, -0.17073846940092e2, 0.12020824702470e5,
         -0.32325550322333e7, 0.14915108613530e2, -0.48232657361591e4, 0.40511340542057e6,
         -0.23855557567849, 0.65017534844798e3]
    Ts = T + 273.15
    th = Ts + n[8] / (Ts - n[9])
    A = th ** 2 + n[0] * th + n[1]
    B = n[2] * th ** 2 + n[3] * th + n[4]
    C = n[5] * th ** 2 + n[6] * th + n[7]
    return (2 * C / (-B + math.sqrt(B * B - 4 * A * C))) ** 4 * 1e6


def rho_v(T, rh):
    return rh * psat(T) / (R_V * (T + 273.15))


def D_v(T):
    return D_V20 * ((T + 273.15) / 293.15) ** 1.75


# ---------- CaCl2 solution: Conde (2004) water-activity correlation ----------
CONDE = [0.31, 3.698, 0.60, 0.231, 4.584, 0.49, 0.478, -5.20, -0.40, 0.018]


def aw_solution(xi, T):
    """Water activity over aqueous CaCl2 at salt mass fraction xi and T (C)."""
    p = CONDE
    th = (T + 273.15) / 647.096
    pi25 = 1 - (1 + (xi / p[6]) ** p[7]) ** p[8] - p[9] * math.exp(-(xi - 0.1) ** 2 / 0.005)
    f = 2 - (1 + (xi / p[0]) ** p[1]) ** p[2] + ((1 + (xi / p[3]) ** p[4]) ** p[5] - 1) * th
    return pi25 * f


def xi_sat(T):
    """Solubility of CaCl2 as mass fraction; hexahydrate below 29.9 C, then tetra and dihydrate.
    Points: 74.5 g/100 g at 20 C, 81.1 at 25 C, 134.5 at 60 C, 152.4 at 100 C (Wikipedia)."""
    pts = [(0.0, 59.5), (20.0, 74.5), (25.0, 81.1), (29.9, 100.6), (60.0, 134.5), (100.0, 152.4)]
    for (t0, s0), (t1, s1) in zip(pts, pts[1:]):
        if T <= t1:
            s = s0 + (s1 - s0) * (T - t0) / (t1 - t0)
            break
    else:
        s = pts[-1][1]
    return s / (100 + s)


def xi_of_aw(aw, T):
    lo, hi = 0.02, 0.75
    for _ in range(40):
        m = (lo + hi) / 2
        if aw_solution(m, T) > aw:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


# Hydrate plateaus below deliquescence, kg water per kg CaCl2 (M CaCl2 = 110.98 g/mol)
X2, X4, X6 = 2 * 18.015 / 110.98, 4 * 18.015 / 110.98, 6 * 18.015 / 110.98
A64, A42 = 0.185, 0.09      # hexa/tetra and tetra/di transitions at 20 C (SaltWiki), held as RH


def X_salt(aw, T):
    """Equilibrium water per kg salt at water activity aw and T."""
    a_drh = aw_solution(xi_sat(T), T)
    if aw >= a_drh:
        xi = xi_of_aw(aw, T)
        return (1 - xi) / xi
    if T < 29.9:
        if aw >= A64:
            return X6
        if aw >= A42:
            return X4
        return X2
    return X2


# ---------- composite ----------
M_SG, M_SALT = 3.0, 1.0                      # kg (DWD-DDR-002; 25 wt % salt, was 2.7 + 1.3 kg at v0.1)
M_SORB = M_SG + M_SALT
VP_SG = 1.0e-3                               # m3/kg pore volume, mesoporous silica gel (assumed)
RHO_SK = 2200.0                              # silica skeleton density, kg/m3
PACK = 0.60                                  # bead packing fraction
K_SG = 0.08                                  # own uptake of the silica walls, kg/kg per unit aw (assumed, small)


def W_eq(aw, T):
    """Equilibrium water in the whole bed, kg."""
    return M_SALT * X_salt(aw, T) + M_SG * K_SG * aw


def aw_of_W(W, T):
    lo, hi = 1e-4, 0.999
    for _ in range(40):
        m = (lo + hi) / 2
        if W_eq(m, T) < W:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def h_sorption(W, T):
    """Heat of desorption per kg water, J/kg, by Clausius-Clapeyron on the isotherm at constant W.
    On a hydrate plateau the solution branch at the same aw is used, plus 10 % (assumption)."""
    T1, T2 = T - 2.0, T + 2.0
    a1, a2 = aw_of_W(W, T1), aw_of_W(W, T2)
    p1, p2 = a1 * psat(T1), a2 * psat(T2)
    h = R_V * math.log(p2 / p1) / (1 / (T1 + 273.15) - 1 / (T2 + 273.15))
    return max(h, H_FG)


# ============================================================================================
print("DewDrive sizing, DWD-CAL-001 v0.2 (all values are estimates)\n")
print("A. Air, sorbent and bed")
T_N, RH_N, RH_DRY = 20.0, 0.40, 0.25
T_DAY = 35.0
H_NIGHT = 10.0
say("A1", f"Vapour density at 20 C: {1e3 * rho_v(T_N, RH_N):.2f} g/m3 at 40 % RH, "
          f"{1e3 * rho_v(T_N, RH_DRY):.2f} g/m3 at 25 % RH; dew points "
          f"{[round(t, 1) for t in [next(t / 10 for t in range(-300, 300) if psat(t / 10) >= RH_N * psat(T_N)), next(t / 10 for t in range(-300, 300) if psat(t / 10) >= RH_DRY * psat(T_N))]]} C",
    rho_v(T_N, RH_N))
a_drh20 = aw_solution(xi_sat(20.0), 20.0)
say("A2", f"CaCl2 solubility at 20 C {100 * xi_sat(20):.1f} wt %; Conde water activity at saturation "
          f"{a_drh20:.3f} (deliquescence; SaltWiki gives about 0.30). Check: 30 wt % gives aw "
          f"{aw_solution(0.30, 20):.3f}, 40 wt % gives {aw_solution(0.40, 20):.3f}", a_drh20)
x40 = xi_of_aw(RH_N, T_N)
say("A3", f"At 40 % RH and 20 C the salt is a solution of {100 * x40:.1f} wt %: {X_salt(RH_N, T_N):.2f} kg water "
          f"per kg salt; at 25 % RH it is the hexahydrate, {X_salt(RH_DRY, T_N):.3f} kg/kg", X_salt(RH_N, T_N))
W40, W25 = W_eq(RH_N, T_N), W_eq(RH_DRY, T_N)
say("A4", f"Equilibrium bed water: {W40:.2f} kg at 40 % RH ({W40 / M_SORB:.3f} g/g), {W25:.2f} kg at 25 % RH "
          f"({W25 / M_SORB:.3f} g/g); TRL 2 assumed 0.30 and 0.16 g/g", W40)
v_pore = M_SG * VP_SG
v_part = M_SG * (1 / RHO_SK + VP_SG)
v_bulk = v_part / PACK
depth = v_bulk / G["bed_m2"]
say("A5", f"Silica pore volume {1e3 * v_pore:.2f} L; bed bulk volume {1e3 * v_bulk:.2f} L over "
          f"{G['bed_m2']:.3f} m2 of tray floor, so the bed is {1e3 * depth:.1f} mm deep (model: "
          f"{PARAMS['bed_depth']:.1f} mm)", depth)


def sol_volume(W):
    """Volume of the salt solution held in the pores, m3 (density of CaCl2 solution, approx.)."""
    w_salt = max(W - M_SG * K_SG * 0.9, 0)
    xi = M_SALT / (M_SALT + w_salt)
    rho = 998 + 880 * xi       # fits 1,178 at 20 wt % and 1,396 at 45 wt % (approx.)
    return (M_SALT + w_salt) / rho


# ============================================================================================
print("\nB. Night adsorption (10 h, fan 40 m3/h)")
FLOW = 40.0 / 3600         # m3/s
ga, gu = G["gap_over_m"], G["gap_under_m"]
wch = G["inner_x_m"]
f_over = ga ** 3 / (ga ** 3 + gu ** 3)     # laminar split by gap cubed


def channel_h(gap, q):
    """Mean heat transfer coefficient, one wall active, laminar parallel plates, developing flow."""
    Dh = 2 * gap
    v = q / (gap * wch)
    Re = v * Dh / NU_AIR
    Gz = Re * 0.71 * Dh / G["inner_y_m"]
    Nu = 4.86 + 0.0668 * Gz / (1 + 0.04 * Gz ** (2 / 3))
    return Nu * K_AIR / Dh, Re, Nu, v


h_o, Re_o, Nu_o, v_o = channel_h(ga, FLOW * f_over)
h_u, Re_u, Nu_u, v_u = channel_h(gu, FLOW * (1 - f_over))
say("B1", f"v0.1 layout for reference: air splits {100 * f_over:.0f} % over the trays ({1e3 * ga:.0f} mm gap) and {100 * (1 - f_over):.0f} % under "
          f"({1e3 * gu:.0f} mm gap); velocity {v_o:.3f} and {v_u:.3f} m/s; Re {Re_o:.0f} and {Re_u:.0f} (laminar); "
          f"h {h_o:.2f} and {h_u:.2f} W/(m2 K)", (h_o, h_u))
EPS_BED, TAU_BED = 0.40, 1.5
D_eff = D_v(T_N) * EPS_BED / TAU_BED
hm_int = 6 * D_eff / depth                      # vapour diffusion into a layer open on both faces
OPEN_MESH = 0.60
hm_o = 1 / (RHO_AIR * CP_AIR / h_o + 1 / hm_int)
hm_u = 1 / (RHO_AIR * CP_AIR / h_u + 1 / hm_int)
Gm_o, Gm_u = hm_o * G["bed_m2"], hm_u * G["bed_m2"] * OPEN_MESH
ntu_o, ntu_u = Gm_o / (FLOW * f_over), Gm_u / (FLOW * (1 - f_over))
eff_A = f_over * (1 - math.exp(-ntu_o)) + (1 - f_over) * (1 - math.exp(-ntu_u))
say("B2", f"Mass transfer, v0.1 layout for reference (air flows past the bed): gas side {h_o / (RHO_AIR * CP_AIR) * 1e3:.2f} and "
          f"{h_u / (RHO_AIR * CP_AIR) * 1e3:.2f} mm/s, in-bed {hm_int * 1e3:.1f} mm/s; NTU {ntu_o:.2f} over, "
          f"{ntu_u:.2f} under; at most {100 * eff_A:.0f} % of the vapour driving force is captured", eff_A)
# Option B: air drawn down through the mesh-floored bed (packed-bed Wakao correlation)
d_p = 3.5e-3
u_s = FLOW / G["bed_m2"]
Re_p = u_s * d_p / NU_AIR
Sh = 2 + 1.1 * (NU_AIR / D_v(T_N)) ** (1 / 3) * Re_p ** 0.6
a_v = 6 * PACK / d_p
ntu_B = Sh * D_v(T_N) / d_p * a_v * v_bulk / FLOW
eff_B = 1 - math.exp(-ntu_B)
dP_B = 150 * 1.8e-5 * PACK ** 2 * u_s / ((1 - PACK) ** 3 * d_p ** 2) * depth
say("B3", f"Through-flow, design of record (DDR-002; air drawn down through the bed): superficial {1e3 * u_s:.1f} mm/s, gas-side NTU "
          f"{ntu_B:.0f}, capture {100 * eff_B:.0f} % of the driving force (grain-internal kinetics not modelled); "
          f"bed pressure drop {dP_B:.2f} Pa", ntu_B)

U_TOP = 3.2           # W/(m2 K), bed to ambient through gap and twin-wall glazing (assumed)
C_DRY = M_SG * 920 + M_SALT * 670 + 4 * 0.60 * 900   # J/K, sorbent plus four aluminium trays


def night(W0, T_air, rh, hours=H_NIGHT, mode="A", flow=FLOW, dt=60.0, rh_scale=1.0):
    """Time-stepped lumped bed. Returns (W_end, uptake, peak bed temperature)."""
    W, Tb = W0, T_air
    rho_in = rho_v(T_air, rh)
    peak = Tb
    for _ in range(int(hours * 3600 / dt)):
        aw = aw_of_W(W, Tb)
        rho_s = aw * psat(Tb) / (R_V * (Tb + 273.15))
        if mode == "A":
            q_o, q_u = flow * f_over, flow * (1 - f_over)
            mdot = (q_o * (1 - math.exp(-Gm_o * rh_scale / q_o)) + q_u * (1 - math.exp(-Gm_u * rh_scale / q_u))) * (rho_in - rho_s)
            # heat: gas-side only (Lewis), same channels
            ua = (q_o * (1 - math.exp(-h_o * G["bed_m2"] / (RHO_AIR * CP_AIR * q_o)))
                  + q_u * (1 - math.exp(-h_u * G["bed_m2"] * OPEN_MESH / (RHO_AIR * CP_AIR * q_u)))) * RHO_AIR * CP_AIR
        else:
            mdot = flow * (1 - math.exp(-ntu_B * rh_scale)) * (rho_in - rho_s)
            ua = flow * RHO_AIR * CP_AIR * (1 - math.exp(-ntu_B))
        hs = h_sorption(W, Tb)
        C = C_DRY + 4186 * W
        dT = (mdot * hs - ua * (Tb - T_air) - U_TOP * G["tray_m2"] * (Tb - T_air)) / C * dt
        W += mdot * dt
        Tb += dT
        peak = max(peak, Tb)
    return W, W - W0, peak


# ============================================================================================
# Day: sealed box, sun on the black tray tops, vapour diffuses down to the condenser plate
H_TILT = 6.0          # kWh/m2 per day on the tilted aperture
TAU_ALPHA = 0.78 * 0.95
EPS_BED_UNDER = OPEN_MESH * 0.90 + (1 - OPEN_MESH) * 0.10     # beads through the mesh, bare aluminium
EPS_PLATE = 0.90
ALPHA_PLATE = 0.50
# Drip screen (DDR-002): two staggered layers of aluminium channels; no line of sight, so it acts as a
# radiation shield of emissivity EPS_SCR on both faces. Design of record: painted matt black (0.90), so the
# bed can still shed heat to the condenser. Item 5 evaluation: bare, low-emissivity aluminium (0.15, which
# allows for dust and brine films). Vapour detours around the channels: extra diffusion length t (tau / open - 1).
EPS_SCR = 0.90
EPS_SCR_LOWE = 0.15
TAU_SCR = 1.5
FAN_RH_OFF = 0.70     # logger rule: fan stops above 70 % RH (DDR-002)
FLOW_NAT = 0.10 * 40.0 / 3600   # natural airflow through the open flaps with the fan off, assumed 10 % of the fan


def eps_bed_cond(screen=EPS_SCR):
    """Effective emissivity for radiation from the bed underside to the condenser plate.
    screen is the emissivity of the drip-screen faces, or None for no screen."""
    r = 1 / EPS_BED_UNDER + 1 / EPS_PLATE - 1
    if screen:
        r += 2 / screen - 1
    return 1 / r


def vapour_path(screen=EPS_SCR):
    """Equivalent still-air diffusion length from the bed underside to the condenser, m."""
    L = G["gap_under_m"]
    if screen:
        L += G["screen_t_m"] * (TAU_SCR / G["screen_open"] - 1)
    return L
HOLDUP = 0.030        # kg of condensate left as drops and films on the plate and gutter each day


def sun(t):
    """Irradiance on the tilted aperture, W/m2, t in hours after midnight; sine from 06:00 to 18:00."""
    if 6.0 <= t <= 18.0:
        return H_TILT * 1000 * math.pi / 24 * math.sin(math.pi * (t - 6) / 12)
    return 0.0


def condenser_ua(dT):
    """Shaded finned underside to ambient air and shaded ground: W/K for a given rise dT."""
    dT = max(dT, 0.5)
    Lf, hf, tf = G["fin_len_m"], G["fin_h_m"], G["fin_t_m"]
    h_c = 1.42 * (dT / hf) ** 0.25               # laminar vertical plate, air
    m = math.sqrt(2 * h_c / (205.0 * tf))
    eta = math.tanh(m * hf) / (m * hf)
    a_fin = 2 * G["fin_n"] * hf * Lf
    a_base = G["plate_m2"] - G["fin_n"] * tf * Lf
    h_r = 4 * 0.85 * SIGMA * (273.15 + T_DAY + dT / 2) ** 3   # envelope to shaded ground at ambient
    return h_c * (eta * a_fin + 0.5 * a_base) + h_r * G["plate_m2"], eta, h_c


def day(W0, T_amb=T_DAY, dt=60.0, t0=7.0, t1=19.0, trace=False, screen=EPS_SCR):
    """Sealed-box day from the morning flap closure. Returns dict of results."""
    W, Tb = W0, 20.0 + 4.0
    delta = vapour_path(screen)
    eps = eps_bed_cond(screen)
    a_d = G["bed_m2"] * OPEN_MESH
    cond = 0.0
    rec = {"Tb_max": 0.0, "dTc_max": 0.0, "Qc_max": 0.0, "Tb_noon": None, "E_sun": 0.0, "E_win": 0.0,
           "E_des": 0.0, "E_loss": 0.0, "E_bc": 0.0, "rate_max": 0.0, "Tc_max": 0.0}
    Tc = T_amb
    t = t0
    rows = []
    step = 0
    while t < t1:
        G_t = sun(t)
        q_abs = TAU_ALPHA * G_t * G["tray_m2"]
        q_gap = 0.78 * ALPHA_PLATE * G_t * max(G["inner_m2"] - G["tray_m2"], 0)
        aw = aw_of_W(W, Tb)
        pb = aw * psat(Tb)
        # iterate the condenser temperature
        for _ in range(30):
            pc = psat(Tc)
            Tm = (Tb + Tc) / 2
            cmol = P_ATM / (R_U * (Tm + 273.15))
            if pb > pc:
                mdot = M_W * cmol * D_v(Tm) / delta * a_d * math.log((P_ATM - pc) / (P_ATM - pb))
            else:
                mdot = 0.0
            q_rad = eps * SIGMA * G["bed_m2"] * ((Tb + 273.15) ** 4 - (Tc + 273.15) ** 4)
            q_cond = K_AIR / G["gap_under_m"] * G["bed_m2"] * (Tb - Tc)
            q_c = mdot * H_FG + q_rad + q_cond + q_gap
            ua, eta, hc = condenser_ua(Tc - T_amb)
            Tc_new = T_amb + q_c / ua
            if abs(Tc_new - Tc) < 0.01:
                break
            Tc = 0.5 * Tc + 0.5 * Tc_new
        hs = h_sorption(W, Tb)
        q_loss = U_TOP * G["tray_m2"] * (Tb - T_amb)
        C = C_DRY + 4186 * W
        Tb += (q_abs - q_loss - q_rad - q_cond - mdot * hs) / C * dt
        W -= mdot * dt
        cond += mdot * dt
        rec["E_sun"] += G_t * G["inner_m2"] * dt
        rec["E_win"] += q_abs * dt
        rec["E_des"] += mdot * hs * dt
        rec["E_loss"] += q_loss * dt
        rec["E_bc"] += (q_rad + q_cond) * dt
        rec["Tb_max"] = max(rec["Tb_max"], Tb)
        rec["Tc_max"] = max(rec["Tc_max"], Tc)
        rec["dTc_max"] = max(rec["dTc_max"], Tc - T_amb)
        rec["Qc_max"] = max(rec["Qc_max"], q_c)
        rec["rate_max"] = max(rec["rate_max"], mdot * 3600)
        if rec["Tb_noon"] is None and t >= 12.0:
            rec["Tb_noon"] = Tb
        if trace and step % int(3600 / dt) == 0:
            rows.append((t, G_t, Tb, Tc, aw, mdot * 3600 * 1e3, W))
        step += 1
        t = t0 + step * dt / 3600
    rec.update(W_end=W, condensed=cond, collected=max(cond - HOLDUP, 0.0), rows=rows)
    return rec


def cycle(rh, mode="B", flow=FLOW, n=10, rh_scale=1.0, screen=EPS_SCR):
    """Repeat night plus day until the bed water at dawn repeats."""
    W = W_eq(0.2, 60.0)
    for _ in range(n):
        Wn, up, pk = night(W, T_N, rh, mode=mode, flow=flow, rh_scale=rh_scale)
        d = day(Wn, screen=screen)
        W = d["W_end"]
    d["uptake"], d["night_peak"], d["W_dawn"], d["W_dusk"] = up, pk, Wn, W
    return d


print("  (cyclic simulation; this takes a few minutes)")
cD40 = cycle(RH_N)                    # design of record (DDR-002): through-flow, 25 wt % salt, black drip screens
cD25 = cycle(RH_DRY)
cN40 = cycle(RH_N, screen=None)       # same without the drip screens (what the screens cost)
cL40 = cycle(RH_N, screen=EPS_SCR_LOWE)   # item 5 evaluation: low-emissivity screens
cL25 = cycle(RH_DRY, screen=EPS_SCR_LOWE)
supply = FLOW * H_NIGHT * 3600 * rho_v(T_N, RH_N)
say("B4", f"Vapour carried through the box overnight: {supply:.2f} kg at 40 % RH, "
          f"{FLOW * H_NIGHT * 3600 * rho_v(T_N, RH_DRY):.2f} kg at 25 % RH", supply)
say("B5", f"Design, 40 % RH: overnight uptake {cD40['uptake']:.2f} kg ({cD40['uptake'] / M_SORB:.3f} g/g swing), "
          f"bed water {cD40['W_dusk']:.2f} kg at dusk and {cD40['W_dawn']:.2f} kg at dawn (equilibrium {W40:.2f} kg); "
          f"bed warms to {cD40['night_peak']:.1f} C from the heat of adsorption", cD40["uptake"])
say("B6", f"Design, 25 % RH: overnight uptake {cD25['uptake']:.2f} kg", cD25["uptake"])

print("\nC. Day desorption, condenser and yield (sealed box, 35 C air, 6.0 kWh/m2)")
win = sum(sun(6 + i / 60) for i in range(int(12 * 60))) / 60 / 1000
win69 = sum(sun(9 + i / 60) for i in range(int(6 * 60))) / 60 / 1000
say("C1", f"Irradiation on the aperture: {win:.2f} kWh/m2 per day, of which {win69:.2f} kWh/m2 from 09:00 to 15:00; "
          f"peak {sun(12):.0f} W/m2", win69)
say("C2", f"Design, 40 % RH: bed {cD40['Tb_noon']:.0f} C at noon, peak {cD40['Tb_max']:.0f} C; condenser peak "
          f"{cD40['Tc_max']:.1f} C, {cD40['dTc_max']:.1f} K above ambient; condenser load peak {cD40['Qc_max']:.0f} W", cD40["Tb_noon"])
say("C3", f"Design, 40 % RH: condensed {cD40['condensed']:.2f} kg, collected {cD40['collected']:.2f} L per day "
          f"({cD40['collected'] / G['inner_m2']:.2f} L/m2 of inner aperture)", cD40["collected"])
say("C4", f"Design, 25 % RH: collected {cD25['collected']:.2f} L per day", cD25["collected"])
say("C5", f"Effective bed-to-condenser emissivity: {eps_bed_cond(None):.3f} with no screen, {eps_bed_cond(EPS_SCR):.3f} "
          f"with black drip screens, {eps_bed_cond(EPS_SCR_LOWE):.3f} with low-emissivity screens; vapour path "
          f"{1e3 * vapour_path(EPS_SCR):.0f} mm with screens against {1e3 * vapour_path(None):.0f} mm", eps_bed_cond(EPS_SCR))
say("C6", f"Without drip screens: collected {cN40['collected']:.2f} L at 40 % RH; condenser {cN40['dTc_max']:.1f} K "
          f"above ambient, load peak {cN40['Qc_max']:.0f} W; bed peak {cN40['Tb_max']:.0f} C", cN40["collected"])
say("C10", f"Item 5 evaluation, low-emissivity screens: collected {cL40['collected']:.2f} L at 40 % RH and "
           f"{cL25['collected']:.2f} L at 25 % RH; condenser {cL40['dTc_max']:.1f} K above ambient, load peak "
           f"{cL40['Qc_max']:.0f} W; bed {cL40['Tb_noon']:.0f} C at noon, peak {cL40['Tb_max']:.0f} C", cL40["collected"])


def energy(c):
    return {k: c[k] / 3.6e6 for k in ("E_sun", "E_win", "E_des", "E_loss", "E_bc")}


eD, eL = energy(cD40), energy(cL40)
effD = cD40["collected"] * H_FG / 3.6e6 / eD["E_sun"]
effL = cL40["collected"] * H_FG / 3.6e6 / eL["E_sun"]
say("C7", f"Energy, design at 40 % RH: sun on the inner aperture {eD['E_sun']:.2f} kWh; absorbed by the trays "
          f"{eD['E_win']:.2f} kWh; to desorption {eD['E_des']:.2f} kWh; lost through the glazing {eD['E_loss']:.2f} kWh; "
          f"bed to condenser {eD['E_bc']:.2f} kWh (low-emissivity screens {eL['E_bc']:.2f} kWh); solar-to-water efficiency "
          f"{100 * effD:.1f} % ({100 * effL:.1f} % with low-emissivity screens)", effD)
ua12, eta12, hc12 = condenser_ua(12.0)
say("C8", f"Condenser: {G['fin_n']} fins {1e3 * G['fin_t_m']:.0f} x {1e3 * G['fin_h_m']:.0f} x {1e3 * G['fin_len_m']:.0f} mm, "
          f"fin area {2 * G['fin_n'] * G['fin_h_m'] * G['fin_len_m']:.2f} m2, h {hc12:.1f} W/(m2 K), fin efficiency "
          f"{eta12:.2f}; UA {ua12:.1f} W/K at 12 K", ua12)
# Sensitivity: diffusion inside the grains is not modelled; cap the effective night NTU
sens = {n: cycle(RH_N, rh_scale=n / ntu_B)["collected"] for n in (2.0, 1.0)}
say("C9", f"Sensitivity, design at 40 % RH, if grain kinetics cut the night NTU from {ntu_B:.0f} to 2 or 1: "
          f"collected {sens[2.0]:.2f} or {sens[1.0]:.2f} L per day", sens)
dd = day(cD40["W_dawn"], trace=True)
print("      hour   sun W/m2   bed C   cond C   aw     g/h   bed water kg")
for r in dd["rows"]:
    if round(r[0]) in (7, 9, 11, 12, 13, 15, 17, 18):
        print(f"      {r[0]:4.0f}   {r[1]:7.0f}   {r[2]:5.1f}   {r[3]:5.1f}   {r[4]:.3f}  {r[5]:5.0f}   {r[6]:.2f}")


def with_salt(frac, fn):
    """Run fn() with a different salt loading (same 4.0 kg of composite)."""
    global M_SALT, M_SG
    old = M_SALT, M_SG
    M_SALT, M_SG = M_SORB * frac, M_SORB * (1 - frac)
    try:
        return fn()
    finally:
        M_SALT, M_SG = old


def pore_fill_rh(frac):
    def f():
        lo, hi = 0.3, 0.99
        for _ in range(40):
            m = (lo + hi) / 2
            if sol_volume(W_eq(m, T_N)) < M_SG * VP_SG:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2
    return with_salt(frac, f)


print("\nD. Stagnation, glazing and touch temperatures (empty bed, 35 C, noon)")
G_pk = sun(12)


def stagnation(screen=EPS_SCR):
    """Dry bed at noon: absorbed = loss to ambient + loss to the condenser (condenser at ambient + 5 K)."""
    Ts = T_DAY
    eps = eps_bed_cond(screen)
    for _ in range(400):
        q_in = TAU_ALPHA * G_pk * G["tray_m2"]
        q_out = U_TOP * G["tray_m2"] * (Ts - T_DAY) + eps * SIGMA * G["tray_m2"] * ((Ts + 273.15) ** 4 - (T_DAY + 5 + 273.15) ** 4) \
            + K_AIR / G["gap_under_m"] * G["tray_m2"] * (Ts - T_DAY - 5)
        Ts += (q_in - q_out) / 50
    return Ts


Ts, Ts_ns, Ts_le = stagnation(EPS_SCR), stagnation(None), stagnation(EPS_SCR_LOWE)
say("D1", f"Stagnation bed temperature with a dry bed at noon: {Ts:.0f} C with black drip screens ({Ts_ns:.0f} C without "
          f"screens, {Ts_le:.0f} C with low-emissivity screens); twin-wall polycarbonate is usually rated to about 120 C in "
          f"service; check the supplier", Ts)
# Glazing: inner skin sees bed radiation plus gap convection; outer skin to air (h_out 15) plus sky
h_in = 4 * 0.9 * SIGMA * (273.15 + (Ts + T_DAY) / 2) ** 3 + 2.5
R_pc, h_out = 0.14, 15.0
q = (Ts - T_DAY) / (1 / h_in + R_pc + 1 / h_out)
T_out = T_DAY + q / h_out + 0.05 * G_pk / h_out
say("D2", f"Glazing outer skin at stagnation: about {T_out:.0f} C (includes 5 % solar absorption in the skins); "
          f"wall and plywood surfaces stay near ambient plus solar gain on paint", T_out)
T_cond_touch = T_DAY + cD40["dTc_max"]
say("D3", f"Condenser fins (touchable, ankle and hand height): up to {T_cond_touch:.0f} C at the peak of desorption", T_cond_touch)

print("\nE. Salt containment (R7), 25 wt % CaCl2")
v_sol40 = sol_volume(W40)
W90 = W_eq(0.90, T_N)
v_sol90 = sol_volume(W90)


def fill(W):
    return sol_volume(W) / v_pore


rh_fill = pore_fill_rh(M_SALT / M_SORB)
say("E1", f"Solution volume at equilibrium: {1e3 * v_sol40:.2f} L at 40 % RH ({100 * v_sol40 / v_pore:.0f} % of the "
          f"{1e3 * v_pore:.2f} L pore volume); {1e3 * v_sol90:.2f} L at 90 % RH ({100 * v_sol90 / v_pore:.0f} %)", v_sol90 / v_pore)
say("E2", f"The pores fill at {100 * rh_fill:.0f} % RH (20 C) with 25 wt % salt; {100 * pore_fill_rh(0.325):.0f} % RH at the "
          f"v0.1 loading of 32.5 wt %; {100 * pore_fill_rh(0.20):.0f} % RH at 20 wt %", rh_fill)
Wn90 = night(cD40["W_dusk"], T_N, 0.90)[0]
say("E3", f"One 10 h night at 90 % RH with the fan running, from the normal dusk state: bed water {Wn90:.2f} kg, "
          f"{100 * fill(Wn90):.0f} % of the pores", fill(Wn90))


def humid_spell(flow, nights=3):
    """Consecutive 90 % RH nights with overcast days in between (flaps shut by day, no desorption)."""
    W, out = cD40["W_dusk"], []
    for _ in range(nights):
        W = night(W, T_N, 0.90, flow=flow)[0]
        out.append(W)
    return out


spell_fan = humid_spell(FLOW)
spell_rule = humid_spell(FLOW_NAT)
say("E4", "Three 90 % RH nights in a row, fan left running (rule failed): pores "
          + ", ".join(f"{100 * fill(w):.0f} %" for w in spell_fan) + " full after nights 1 to 3", fill(spell_fan[-1]))
say("E5", f"Same spell with the fan stopped above {100 * FAN_RH_OFF:.0f} % RH (natural airflow assumed "
          f"{FLOW_NAT * 3600:.0f} m3/h): pores " + ", ".join(f"{100 * fill(w):.0f} %" for w in spell_rule)
          + " full", fill(spell_rule[-1]))
excess = {k: max(sol_volume(v[-1]) - v_pore, 0.0) for k, v in (("fan", spell_fan), ("rule", spell_rule))}
say("E6", f"Brine that could leave the beads after the spell: {1e3 * excess['rule']:.2f} L with the fan rule, "
          f"{1e3 * excess['fan']:.2f} L with the fan left running; the four drip-screen sumps hold {G['sump_l']:.2f} L",
    excess)

print("\nF. Electrical energy (R4)")
P_FAN, P_LOG = 2.0, 0.15
E_day = P_FAN * H_NIGHT + P_LOG * 24
PV_W, PSH, DERATE = 10.0, 5.0, 0.70
E_pv = PV_W * PSH * DERATE
BATT = 12.8 * 6.0
auto = BATT * 0.80 / E_day
say("F1", f"Loads {E_day:.1f} Wh per day (fan {P_FAN * H_NIGHT:.0f} Wh, logger {P_LOG * 24:.1f} Wh); PV {E_pv:.0f} Wh per day "
          f"(10 W x 5 h x 0.70); margin {E_pv / E_day:.2f}", E_day)
say("F2", f"Battery {BATT:.1f} Wh, 80 % usable: {auto:.1f} days of autonomy with no sun", auto)
a_in = PARAMS["flap_in"][0] * PARAMS["flap_in"][1] / 1e6
dP_box = 0.5 * RHO_AIR * (FLOW / a_in) ** 2 * 3 + dP_B
say("F3", f"Fan duty: {FLOW * 3600:.0f} m3/h against about {dP_box:.1f} Pa (flap openings and the hood, 3 velocity "
          f"heads at the {1e3 * a_in / 1e3:.3f} m2 inlet, plus {dP_B:.2f} Pa for the bed); a 120 mm fan delivers this at low speed", dP_box)

print("\nG. Mass (R9), from the model volumes")
vol = volumes_cm3()
dens = {  # g/cm3 effective, for the solid volumes in the massing model
    "walls": 0.36,        # 12 mm plywood (0.6) in 40 mm, rest PIR (0.035): (12 x 0.6 + 28 x 0.035) / 40
    "glazing": 0.17,      # 10 mm twin-wall PC, 1.7 kg/m2, plus frame (added below)
    "trays": 2.70, "condenser": 2.70, "gutter": 2.70, "flap": 2.70, "fan": 1.2,
    "screens": 2.70 * 0.5,   # massing channels are 1 mm thick; the BOM calls for 0.5 mm flashing
    "stand": 7.85, "bottle": 0.0, "pv": 0.9, "ebox": 1.3, "shield": 0.3,
}
mass = {k: vol[k] * dens.get(k, 0) / 1e3 for k in vol if k != "bed"}
mass["glazing"] += 1.2          # aluminium edge frame and hinges
mass["trays"] = min(mass["trays"], 4 * 0.60 + 0.5 + G["baffle_m2"] * PARAMS["baffle_t"] * 2.7)  # 0.6 kg each, rails, baffle
mass["bed"] = M_SORB
mass["bottle"] = 0.45
# parts drawn as solid blocks in the massing model: use component estimates instead
mass.update(flap=0.4, fan=0.8, ebox=1.8, pv=2.5, shield=0.2)
mass["hardware"] = 1.5
box = sum(mass[k] for k in ("walls", "glazing", "trays", "bed", "screens", "condenser", "gutter", "flap", "fan"))
total = sum(mass.values())
for k in sorted(mass, key=lambda k: -mass[k]):
    print(f"      {k:10s} {mass[k]:6.2f} kg")
say("G1", f"Box with trays, sorbent and condenser {box:.1f} kg; stand {mass['stand']:.1f} kg; total dry {total:.1f} kg "
          f"({total * 2.2046:.0f} lb)", box)
box_no_trays = box - mass["trays"] - mass["bed"] - mass["screens"]
say("G2", f"Box lifted with trays, sorbent and drip screens removed: {box_no_trays:.1f} kg (screens {mass['screens']:.1f} kg)", box_no_trays)

print("\nH. Wind (R10), 20 m/s")
V = 20.0
q_w = 0.5 * 1.2 * V ** 2
CF = 1.2
A_p = G["aperture_m2"]
F_n = q_w * CF * A_p
tilt = math.radians(PARAMS["tilt"])
F_up, F_h = F_n * math.cos(tilt), F_n * math.sin(tilt)
Wt = total * 9.81
h_cp = G["box_centre_z_m"]
a = G["leg_span_y_m"] / 2
e = 0.25 * PARAMS["box_y"] / 1e3      # centre of pressure a quarter chord upwind of the centre (assumed)
M_ot = F_up * (a + e) + F_h * h_cp
M_rs = Wt * a
SF = 1.5
ballast = max(SF * M_ot - M_rs, 0) / (9.81 * a)
mu = 0.5
slide_margin = mu * (Wt - F_up) - F_h
ballast_slide = max(SF * F_h / mu + F_up - Wt, 0) / 9.81
say("H1", f"Dynamic pressure {q_w:.0f} Pa; normal force {F_n:.0f} N (Cf {CF}, {A_p:.2f} m2): uplift {F_up:.0f} N, "
          f"horizontal {F_h:.0f} N; dry weight {Wt:.0f} N", F_n)
say("H2", f"Overturning moment {M_ot:.0f} N m against a restoring {M_rs:.0f} N m (ratio {M_rs / M_ot:.2f}); "
          f"ballast for a factor of 1.5: {ballast:.0f} kg on the stand, or anchors", ballast)
say("H3", f"Sliding (friction 0.5): margin {slide_margin:.0f} N without ballast; ballast for 1.5 against sliding "
          f"{ballast_slide:.0f} kg", ballast_slide)
anchor = max(SF * M_ot - M_rs, 0) / (2 * 2 * a)
say("H4", f"Alternative: two upwind ground anchors, each rated for {anchor:.0f} N or more in uplift", anchor)

print("\nI. Logging (R12)")
rec_bytes, chans = 48, 5
n_rec = 30 * 24 * 12
say("I1", f"{chans} channels every 5 min for 30 days: {n_rec} records, about {n_rec * rec_bytes / 1e6:.2f} MB as CSV; "
          f"any microSD card holds years", n_rec)

print("\nJ. Cost (R11)")
bom = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
say("J1", f"BOM: {len(bom)} lines, total ${cost:.2f}; budget $520 (top-up approved by Amish, 2026-09-26)", cost)
life_l = cD40["collected"] * 365 * 5
say("J2", f"Water cost over 5 years at the design point: {life_l:.0f} L, ${cost / life_l:.2f} per litre", cost / life_l)

# ============================================================================================
print("\nK. Requirements (DWD-REQ-001 v0.4)")
R = []


def req(rid, name, value, target, status):
    R.append((rid, name, value, target, status))


req("R1", "Water at the design point", f"{cD40['collected']:.2f} L/day (C3)",
    ">= 0.5 L/day", "not met" if cD40["collected"] < 0.5 else "met")
req("R2", "Water in dry nights", f"{cD25['collected']:.2f} L/day at 25 % RH (C4)",
    ">= 0.25 L/day at 25 % RH", "not met" if cD25["collected"] < 0.25 else "met")
req("R3", "Sun-only regeneration", f"bed {cD40['Tb_noon']:.0f} C at noon (C2)", ">= 75 C by midday",
    "met" if cD40["Tb_noon"] >= 75 else "not met")
req("R4", "Own electrical loads", f"{E_day:.1f} Wh/day against {E_pv:.0f} Wh/day PV; {auto:.1f} days autonomy (F1, F2)",
    "<= 30 Wh/day; >= 2 days", "met" if E_day <= 30 and auto >= 2 else "not met")
req("R5", "Condenser rise", f"{cD40['dTc_max']:.1f} K (C2)",
    "<= 15 K", "met" if cD40["dTc_max"] <= 15 else "not met")
req("R6", "Water quality", "materials food-grade by selection; chloride carry-over needs a water test", "food-grade; Cl < 250 mg/L",
    "not verifiable at TRL 3")
r7_ok = fill(Wn90) < 1.0 and excess["rule"] <= G["sump_l"] / 1e3
req("R7", "Salt containment", f"pores fill at {100 * rh_fill:.0f} % RH; {100 * fill(Wn90):.0f} % of pore volume after one 90 % RH night; "
    f"{100 * fill(spell_rule[-1]):.0f} % after three with the fan rule; sumps {G['sump_l']:.2f} L (E2 to E6)",
    "no brine leaves the tray and drip-screen assembly after a 90 % RH night", "met" if r7_ok else "at risk")
req("R8", "Two actions per day", "open flaps at dusk, close at dawn; fan on a timer with a humidity cut-out", "2 actions, <= 5 min", "met")
req("R9", "Portable", f"box {box:.1f} kg with sorbent; {box_no_trays:.1f} kg with trays out; total {total:.1f} kg (G1, G2)",
    "box <= 35 kg; stand separable", "met" if box <= 35 else "not met")
req("R10", "Survive the site", f"two anchors of {anchor:.0f} N (default) or {ballast:.0f} kg ballast for 20 m/s (H2 to H4); UV and 300 cycles need supplier data and test",
    "stable at 20 m/s; UV; 300 cycles", "not verifiable at TRL 3")
req("R11", "Cost", f"${cost:.0f} (J1)", "<= $520 (top-up, 2026-09-26)", "met" if cost <= 520 else "not met")
req("R12", "Record performance", f"{n_rec} records, {n_rec * rec_bytes / 1e6:.2f} MB (I1)", "5 min for 30 days", "met")
req("R13", "Protect users", f"glazing outer about {T_out:.0f} C at stagnation; fins up to {T_cond_touch:.0f} C; 12.8 V DC (D1 to D3)",
    "touched surfaces <= 60 C; < 60 V DC", "met" if T_out <= 60 and T_cond_touch <= 60 else "not met")
with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "value", "target", "status"])
    w.writerows(R)
for r in R:
    print(f"  {r[0]:4s} {r[4]:24s} {r[2]}")
from collections import Counter
cnt = Counter(r[4] for r in R)
say("K1", "Counts: " + ", ".join(f"{v} {k}" for k, v in sorted(cnt.items())), dict(cnt))
