"""DewDrive parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP files to cad/step and STL files to cad/stl.

Main dimensions and interfaces only; not for fabrication.

Coordinates in mm. X runs east to west across the collector, Y runs south to north, Z is up.
The glazed box is built flat in a local frame (glazing on top, condenser floor below) and is
then tilted by PARAMS["tilt"] about X so the glazing faces south (toward -Y) and the high edge
is to the north. Every part carries its BOM line number from bom/bom.csv.

docs/04-calcs/sizing.py (DWD-CAL-001) imports PARAMS and derived() so that the calculation
uses the same dimensions as the STEP files and drawing DWD-DWG-001.
"""
import math
from pathlib import Path

# ---------------------------------------------------------------------------------------------
# Top-level parameters (mm unless noted). Edit these, not the geometry below.
PARAMS = {
    "tilt": 20.0,            # collector tilt from horizontal, degrees (DDR-001, D5)
    "box_x": 1100.0,         # outer box size east-west
    "box_y": 1000.0,         # outer box size along the slope (south-north)
    "wall_t": 40.0,          # insulated wall: 6 mm plywood + 25 mm PIR + 6 mm plywood + paint, rounded
    "wall_z0": 40.0,         # local height of the wall bottom edge
    "wall_h": 140.0,         # wall height
    "glaz_t": 10.0,          # twin-wall polycarbonate thickness
    "plate_t": 2.0,          # condenser floor plate thickness
    "plate_top": 45.0,       # local height of the condenser plate top (wetted face)
    "fin_n": 21,             # number of condenser fins
    "fin_t": 1.0,            # fin thickness
    "fin_h": 100.0,          # fin depth below the plate
    "fin_pitch": 50.0,       # fin spacing east-west
    "tray_x": 490.0,         # tray outer size east-west
    "tray_y": 430.0,         # tray outer size along the slope
    "tray_h": 25.0,          # tray depth
    "tray_z0": 110.0,        # local height of the tray mesh floor
    "tray_rim": 8.0,         # tray side flange width (sets the bed area)
    "bed_depth": 8.3,        # sorbent bed depth; checked against the sorbent volume in DWD-CAL-001
    "gutter_w": 30.0,        # gutter width along the low edge
    "flap_in": (800.0, 70.0),   # south inlet flap, width x height
    "flap_out": (560.0, 70.0),  # north outlet flap beside the fan hood
    "fan_hood": (160.0, 64.0, 140.0),
    "z0": 680.0,             # height of the local box origin above the ground at the box centre
    "leg": 30.0,             # stand angle leg size (30 x 30 x 3 mm)
    "leg_t": 3.0,
    "foot": 120.0,           # square foot pad
    "pv_size": (340.0, 250.0, 25.0),  # 10 W panel
    "pv_z": 1330.0,          # PV panel centre height
    "ebox": (160.0, 110.0, 220.0),    # electronics box
    "bottle": (180.0, 260.0, 320.0),  # 10 L jerrycan
    "bottle_xy": (360.0, -760.0),
}

BOM_NAMES = {
    1: "Stand, galvanized steel angle",
    2: "Insulated box walls",
    3: "Glazing lid, twin-wall polycarbonate",
    4: "Sorbent trays (4), black aluminium mesh",
    5: "Composite sorbent, silica gel and CaCl2",
    6: "Condenser plate with fins",
    7: "Condensate gutter and drain tube",
    8: "Collection bottle, 10 L",
    9: "Vent flap, south inlet",
    10: "Night fan and outlet flap, 12 V",
    11: "PV panel, 10 W, on pole",
    12: "Electronics box (charger, LiFePO4, logger)",
    13: "Air temperature and RH sensor shield",
}


def _trig(P=PARAMS):
    t = math.radians(P["tilt"])
    return math.sin(t), math.cos(t)


def world(x, y, z, P=PARAMS):
    """Local box point to world coordinates."""
    s, c = _trig(P)
    return (x, y * c - z * s, P["z0"] + y * s + z * c)


def tray_centres(P=PARAMS):
    ox = P["box_x"] / 2 - P["wall_t"] - P["tray_x"] / 2 - 13.0
    oy = P["box_y"] / 2 - P["wall_t"] - P["tray_y"] / 2 - 23.0
    return [(sx * ox, sy * oy) for sx in (-1, 1) for sy in (-1, 1)]


def derived(P=PARAMS):
    """Areas, gaps and heights the calculation note uses (SI units: m, m2)."""
    ix, iy = P["box_x"] - 2 * P["wall_t"], P["box_y"] - 2 * P["wall_t"]
    bed_x, bed_y = P["tray_x"] - 2 * P["tray_rim"], P["tray_y"] - 2 * P["tray_rim"]
    glaz_bot = P["wall_z0"] + P["wall_h"]
    s, c = _trig(P)
    top_edge = world(0, P["box_y"] / 2, glaz_bot + P["glaz_t"], P)[2]
    low_edge = world(0, -P["box_y"] / 2, glaz_bot + P["glaz_t"], P)[2]
    fin_bottom = min(world(0, y, P["plate_top"] - P["plate_t"] - P["fin_h"], P)[2]
                     for y in (-P["box_y"] / 2, P["box_y"] / 2))
    return {
        "aperture_m2": P["box_x"] * P["box_y"] / 1e6,           # glazed lid, outer
        "inner_m2": ix * iy / 1e6,                               # inside the walls
        "inner_x_m": ix / 1e3, "inner_y_m": iy / 1e3,
        "tray_m2": 4 * P["tray_x"] * P["tray_y"] / 1e6,          # tray footprint (black tops)
        "bed_m2": 4 * bed_x * bed_y / 1e6,                       # sorbent surface
        "gap_under_m": (P["tray_z0"] - P["plate_top"]) / 1e3,    # bed underside to condenser
        "gap_over_m": (glaz_bot - P["tray_z0"] - P["tray_h"]) / 1e3,  # tray rim to glazing
        "bed_depth_m": P["bed_depth"] / 1e3,
        "plate_m2": (P["box_x"] - 20) * (P["box_y"] - 20) / 1e6,
        "fin_len_m": (P["box_y"] - 80) / 1e3,
        "fin_h_m": P["fin_h"] / 1e3, "fin_t_m": P["fin_t"] / 1e3, "fin_n": P["fin_n"],
        "fin_pitch_m": P["fin_pitch"] / 1e3,
        "top_edge_m": top_edge / 1e3, "low_edge_m": low_edge / 1e3,
        "fin_bottom_m": fin_bottom / 1e3,
        "box_centre_z_m": P["z0"] / 1e3,
        "leg_span_y_m": 2 * (P["box_y"] / 2 - 60) * c / 1e3,     # horizontal distance between leg lines
        "leg_span_x_m": (P["box_x"] - 40) / 1e3,
        "box_air_m3": ix * iy * P["wall_h"] / 1e9,
        "wall_area_m2": 2 * (P["box_x"] + P["box_y"]) * P["wall_h"] / 1e6,
    }


# ---------------------------------------------------------------------------------------------
def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom)] in world coordinates."""
    from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector

    s, c = _trig(P)
    W = Pos(0, 0, P["z0"]) * Rot(P["tilt"], 0, 0)
    LX, LY, WT = P["box_x"], P["box_y"], P["wall_t"]
    ix, iy = LX - 2 * WT, LY - 2 * WT
    zw0, zw1 = P["wall_z0"], P["wall_z0"] + P["wall_h"]

    def bar(a, b, w):
        a, b = Vector(*a), Vector(*b)
        d = b - a
        return Solid.make_cylinder(w / 2, d.length, Plane(origin=a, z_dir=d.normalized()))

    def angle(a, b, size=P["leg"], t=P["leg_t"]):
        """Equal-leg steel angle between two world points (massing: L section, true size)."""
        a, b = Vector(*a), Vector(*b)
        d = b - a
        L = d.length
        prof = Pos(size / 2, t / 2, L / 2) * Box(size, t, L) + Pos(t / 2, size / 2, L / 2) * Box(t, size, L)
        return Plane(origin=a, z_dir=d.normalized()).location * prof

    # 2 Insulated walls, open top and bottom
    walls = Pos(0, 0, (zw0 + zw1) / 2) * (Box(LX, LY, P["wall_h"]) - Box(ix, iy, P["wall_h"] + 10))
    # 3 Glazing lid
    glazing = Pos(0, 0, zw1 + P["glaz_t"] / 2) * Box(LX, LY, P["glaz_t"])
    # 4 Trays and 5 sorbent bed
    trays = bed = None
    rim = P["tray_rim"]
    for (x, y) in tray_centres(P):
        pan = Pos(x, y, P["tray_z0"] + P["tray_h"] / 2) * (
            Box(P["tray_x"], P["tray_y"], P["tray_h"])
            - Pos(0, 0, 1.0) * Box(P["tray_x"] - 2 * rim, P["tray_y"] - 2 * rim, P["tray_h"]))
        cake = Pos(x, y, P["tray_z0"] + 1.0 + P["bed_depth"] / 2) * Box(
            P["tray_x"] - 2 * rim - 0.5, P["tray_y"] - 2 * rim - 0.5, P["bed_depth"])
        trays = pan if trays is None else trays + pan
        bed = cake if bed is None else bed + cake
    rail_z = P["tray_z0"] - 5
    trays = trays + Pos(-(ix / 2 - 8), 0, rail_z) * Box(16, iy, 10) + Pos(ix / 2 - 8, 0, rail_z) * Box(16, iy, 10)
    # 6 Condenser plate and fins
    pt = P["plate_top"]
    condenser = Pos(0, 0, pt - P["plate_t"] / 2) * Box(LX - 20, LY - 20, P["plate_t"])
    x0 = -(P["fin_n"] - 1) / 2 * P["fin_pitch"]
    for i in range(P["fin_n"]):
        condenser = condenser + Pos(x0 + i * P["fin_pitch"], 0, pt - P["plate_t"] - P["fin_h"] / 2) * Box(
            P["fin_t"], LY - 80, P["fin_h"])
    # 7 Gutter and drain
    gy = -LY / 2 + WT + P["gutter_w"] / 2
    gutter = Pos(0, gy, pt + 8) * (Box(ix, P["gutter_w"], 16) - Pos(0, 0, 3) * Box(ix - 6, P["gutter_w"] - 6, 16))
    bx, by = P["bottle_xy"]
    g_out = world(bx, -LY / 2 - 20, pt + 8, P)
    drain = bar(world(bx, -LY / 2 + WT, pt + 8, P), g_out, 16) + bar(g_out, (bx, by + 40, P["bottle"][2] + 60), 16)
    # 9 South inlet flap; 10 fan hood and north outlet flap
    fw, fh = P["flap_in"]
    flap = Pos(-100, -LY / 2 - 5, zw0 + fh / 2) * Box(fw, 10, fh)
    ow, oh = P["flap_out"]
    hx, hy, hz = P["fan_hood"]
    fan = Pos(-230, LY / 2 + 5, zw0 + oh / 2) * Box(ow, 10, oh) + Pos(330, LY / 2 + hy / 2, zw0 + hz / 2) * Box(hx, hy, hz)

    # 1 Stand (world frame): four legs, side rails under the walls, braces, feet
    zr = zw0 - 3                                   # rail seat just under the wall bottom
    pts = {(xs, ys): world(xs * (LX / 2 - 20), ys * (LY / 2 - 60), zr, P) for xs in (-1, 1) for ys in (-1, 1)}
    stand = None
    for (xs, ys), (x, y, z) in pts.items():
        piece = angle((x, y, 6), (x, y, z)) + Pos(x, y, 3) * Box(P["foot"], P["foot"], 6)
        stand = piece if stand is None else stand + piece
    for xs in (-1, 1):
        a, b = pts[(xs, -1)], pts[(xs, 1)]
        stand = stand + angle(a, b) + angle((a[0], a[1], 120), (b[0], b[1], b[2] * 0.55))
    for ys in (-1, 1):
        a, b = pts[(-1, ys)], pts[(1, ys)]
        stand = stand + angle((a[0], a[1], 200), (b[0], b[1], 200))

    # 8 Bottle on the ground below the low edge
    bw, bd, bh = P["bottle"]
    bottle = Pos(bx, by, bh / 2) * Box(bw, bd, bh) + Pos(bx, by + 40, bh + 20) * Cylinder(28, 40)
    # 11 PV panel on a pole above the north-east leg (north of the box: no shade on the aperture)
    px, py, pz = pts[(1, 1)]
    pvx, pvy, pvz = P["pv_size"]
    pv = Pos(px - 200, py + 40, P["pv_z"]) * Rot(P["tilt"] + 10, 0, 0) * Box(pvx, pvy, pvz)
    pv = pv + bar((px, py + 30, pz), (px, py + 30, P["pv_z"] - 20), 30) \
        + bar((px, py + 30, P["pv_z"] - 30), (px - 200, py + 40, P["pv_z"] - 30), 20)
    # 12 Electronics box and 13 sensor shield on the north-west leg
    ex, ey, _ = pts[(-1, 1)]
    ebx, eby, ebz = P["ebox"]
    ebox = Pos(ex - 110, ey, 310 + ebz / 2) * Box(ebx, eby, ebz)
    shield = Pos(ex - 110, ey, 700) * Cylinder(45, 110) + bar((ex - 110, ey, 645), (ex - 20, ey, 645), 12)

    return [
        ("stand", BOM_NAMES[1], stand, 1),
        ("walls", BOM_NAMES[2], W * walls, 2),
        ("glazing", BOM_NAMES[3], W * glazing, 3),
        ("trays", BOM_NAMES[4], W * trays, 4),
        ("bed", BOM_NAMES[5], W * bed, 5),
        ("condenser", BOM_NAMES[6], W * condenser, 6),
        ("gutter", BOM_NAMES[7], W * gutter + drain, 7),
        ("bottle", BOM_NAMES[8], bottle, 8),
        ("flap", BOM_NAMES[9], W * flap, 9),
        ("fan", BOM_NAMES[10], W * fan, 10),
        ("pv", BOM_NAMES[11], pv, 11),
        ("ebox", BOM_NAMES[12], ebox, 12),
        ("shield", BOM_NAMES[13], shield, 13),
    ]


def volumes_cm3(P=PARAMS):
    """Solid volume of each part in cm3, for the mass estimate in DWD-CAL-001."""
    return {k: shape.volume / 1e3 for k, _, shape, _ in build_parts(P)}


def build(P=PARAMS):
    """Whole assembly as one compound (used by the drawing sheet)."""
    from build123d import Compound
    return Compound(children=[shape for _, _, shape, _ in build_parts(P)])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    parts = {k: shape for k, _, shape, _ in build_parts()}
    groups = {
        "dewdrive-assembly": list(parts),
        "collector-box": ["walls", "glazing", "trays", "bed", "condenser", "gutter", "flap", "fan"],
        "condenser": ["condenser"],
        "sorbent-trays": ["trays", "bed"],
        "stand": ["stand"],
        "power-and-logging": ["pv", "ebox", "shield"],
    }
    for name, keys in groups.items():
        comp = Compound(children=[parts[k] for k in keys])
        export_step(comp, str(root / "step" / f"{name}.step"))
        export_stl(comp, str(root / "stl" / f"{name}.stl"))
        print(f"exported {name}: {len(keys)} parts")
    d = derived()
    print("aperture {aperture_m2:.3f} m2, bed {bed_m2:.3f} m2, top edge {top_edge_m:.3f} m".format(**d))
