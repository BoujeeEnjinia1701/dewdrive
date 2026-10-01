"""DewDrive parametric model (build123d), constructable design (DWD-DDR-003, from the DWD-DDR-002 concept).

Run from the repo root:
    python cad/src/model.py            export STEP and STL, print key sizes and the constructability checks
    python cad/src/model.py --check    print the constructability checks only

Every made or bought piece is its own component (build_components), with the faces it shares with
its neighbours, its fixings and its material, so the drawings, the build plan pictures and the mass
estimate all come from the same geometry. build_parts() groups the components by the BOM lines the
calculation note and the concept media use.

Coordinates in mm. X runs east to west across the collector, Y runs south to north, Z is up.
The glazed box is built in a local frame (glazing on top, condenser floor below) and then tilted by
PARAMS["tilt"] about X so the glazing faces south (toward -Y) and the high edge is to the north.
The stand, the PV pole, the electronics and the bottle are built in world coordinates.

docs/04-calcs/sizing.py (DWD-CAL-001) imports PARAMS, derived() and build_components() so that the
calculation uses the same dimensions and volumes as the STEP files and drawing DWD-DWG-001.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------------------------
# Top-level parameters (mm unless noted). Edit these, not the geometry below.
PARAMS = {
    "tilt": 20.0,            # collector tilt from horizontal, degrees (DDR-001, D7)
    "box_x": 1100.0,         # outer box size east-west
    "box_y": 1000.0,         # outer box size along the slope (south-north)
    "wall_t": 40.0,          # wall: 6 mm plywood + 28 mm core (softwood battens, 25 mm PIR) + 6 mm plywood
    "skin_t": 6.0,           # plywood skin
    "wall_z0": 45.0,         # local height of the wall bottom edge (= condenser plate top, DDR-003 P1)
    "wall_h": 133.0,         # wall height; the lid frame sits on the wall top (DDR-003 P1)
    "batten_bot": 44.0,      # bottom core batten height (28 thick): carries the plate screws and the ledges
    "batten_top": 20.0,      # top core batten height: carries the lid hinges and latches
    "post_w": 28.0,          # corner and jamb posts in the core
    "glaz_z0": 180.0,        # local height of the polycarbonate underside
    "glaz_t": 10.0,          # twin-wall polycarbonate thickness
    "lid_frame": (12.0, 2.0),  # lid edge channel: depth x wall thickness (aluminium glazing U-channel)
    "plate_t": 2.0,          # condenser floor plate thickness
    "plate_top": 45.0,       # local height of the condenser plate top (wetted face)
    "plate_xy": (1080.0, 980.0),  # condenser plate size; it closes the bottom of the walls
    "fin_n": 21,             # number of condenser fins
    "fin_t": 1.0,            # fin thickness
    "fin_h": 100.0,          # fin depth below the plate
    "fin_foot": 10.0,        # folded foot that is bonded and riveted to the plate (DDR-003 P5)
    "fin_pitch": 50.0,       # fin spacing east-west
    "tray_x": 490.0,         # tray outer size east-west
    "tray_y": 430.0,         # tray outer size along the slope
    "tray_h": 25.0,          # tray depth
    "tray_z0": 110.0,        # local height of the tray floor (the underside of its bottom lip)
    "tray_rim": 8.0,         # tray bottom lip width (sets the bed area)
    "tray_sheet": 1.0,       # tray sheet thickness
    "mesh_t": 0.8,           # stainless mesh on expanded-metal floor
    "bed_depth": 9.3,        # sorbent bed depth, 3.0 kg gel + 1.0 kg CaCl2 (DDR-002); checked in DWD-CAL-001 A5
    "baffle_t": 1.0,         # sealing baffle sheet on top of the tray deck, top at the tray floor (DDR-002)
    "deck_bar": (20.0, 5.0),  # tray deck bars on edge: height x thickness (DDR-003 P3)
    "deck_gap": 2.0,         # deck to wall clearance, closed by an EPDM lip seal
    "ledge": (15.0, 2.0),    # wall ledges under the deck, aluminium angle leg x thickness (east and west walls)
    "scr_w": 20.0,           # drip screen channel width (DDR-002): two staggered layers of U-channels
    "scr_lip": 6.0,          # channel lip height
    "scr_t": 1.0,            # channel sheet thickness (massing; 0.5 mm flashing in the BOM)
    "scr_pitch": 30.0,       # channel pitch in each layer; layers offset by half a pitch, no line of sight
    "scr_z_hi": 90.0,        # local height of the upper channel layer bottom
    "scr_z_lo": 78.0,        # local height of the lower channel layer bottom
    "scr_frame_z0": 64.0,    # bottom of the screen side plates and sumps
    "sump": (30.0, 12.0),    # brine sump at the low end of each drip screen, width along slope x depth
    "gutter_w": 30.0,        # gutter flange width along the low edge
    "gutter_h": 16.0,        # gutter upstand height against the south wall
    "drain_x": 370.0,        # drain outlet position east-west (between fins)
    "flap_in": (800.0, 40.0),   # south inlet opening, width x height; above the deck (through-flow, DDR-002)
    "flap_in_z": 138.0,         # local height of the inlet opening centre (deck at 110, glazing at 180)
    "flap_out": (140.0, 125.0),  # outlet flap over the fan, on the hood front (DDR-003 P7)
    "slot_out": (140.0, 44.0),   # outlet slot through the north wall, below the deck, behind the hood
    "fan_x": 330.0,          # fan hood centre east-west
    "fan_hood": (160.0, 64.0, 130.0),
    "z0": 680.0,             # height of the local box origin above the ground at the box centre
    "leg": 30.0,             # stand angle leg size (30 x 30 x 3 mm)
    "leg_t": 3.0,
    "leg_y": 440.0,          # leg positions along the slope, local y, each side of centre
    "foot": 120.0,           # square foot plate
    "foot_t": 5.0,
    "xm_z": 200.0,           # height of the end cross members
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
    4: "Sorbent trays (4)",
    5: "Composite sorbent, silica gel and CaCl2",
    6: "Condenser plate with fins",
    7: "Condensate gutter and drain",
    8: "Collection bottle, 10 L",
    9: "Inlet flap, south wall",
    10: "Night fan, hood and outlet flap",
    11: "PV panel, 10 W, on pole",
    12: "Electronics box (charger, LiFePO4, logger)",
    13: "Air temperature and RH sensor shield",
    15: "Drip screens (4) with brine sumps",
    16: "Tray deck and wall ledges",
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought" or "fixing"
    group: str | None  # legacy part key (build_parts, concept media, calculation)
    material: str      # key into the density table of DWD-CAL-001


def _trig(P=PARAMS):
    t = math.radians(P["tilt"])
    return math.sin(t), math.cos(t)


def world(x, y, z, P=PARAMS):
    """Local box point to world coordinates."""
    s, c = _trig(P)
    return (x, y * c - z * s, P["z0"] + y * s + z * c)


def to_local(Y, Z, P=PARAMS):
    """World (Y, Z) to local (y, z)."""
    s, c = _trig(P)
    dz = Z - P["z0"]
    return (Y * c + dz * s, -Y * s + dz * c)


def tray_centres(P=PARAMS):
    ox = P["box_x"] / 2 - P["wall_t"] - P["tray_x"] / 2 - 13.0
    oy = P["box_y"] / 2 - P["wall_t"] - P["tray_y"] / 2 - 23.0
    return [(sx * ox, sy * oy) for sx in (-1, 1) for sy in (-1, 1)]


def stand_geometry(P=PARAMS):
    """Leg positions and bolt heights (world), from where each leg meets its rail."""
    s, c = _trig(P)
    xr = P["box_x"] / 2 - 5.0                 # outer face of the rail's hanging leg (545)
    a, t = P["leg"], P["leg_t"]
    zr_top = P["plate_top"] - P["plate_t"]    # rail top (local) = plate underside, 43
    zr_bot = zr_top - a                       # bottom of the rail's hanging leg, 13
    out = {}
    for ys in (-1, 1):
        yl = ys * P["leg_y"]
        Yc = yl * c - (zr_top - a / 2) * s    # leg centre (world Y) where the rail band is
        # top of the leg: square cut 3 mm below the rail top edge at the leg's low (south) side.
        # A rail edge at local height zl crosses the vertical line at world Y at this height:
        def edge_z(Y, zl):
            y = (Y + zl * s) / c
            return P["z0"] + y * s + zl * c
        top = edge_z(Yc - a / 2, zr_top) - 3.0
        bolt_z = (edge_z(Yc, zr_top) + edge_z(Yc, zr_bot)) / 2 - 2.0
        bolt_z = min(bolt_z, top - 12.0)
        out[ys] = {"Yc": Yc, "top": top, "bolt_z": bolt_z, "xr": xr, "band": (edge_z(Yc, zr_bot), edge_z(Yc, zr_top))}
    return out


def derived(P=PARAMS):
    """Areas, gaps and heights the calculation note uses (SI units: m, m2)."""
    ix, iy = P["box_x"] - 2 * P["wall_t"], P["box_y"] - 2 * P["wall_t"]
    bed_x, bed_y = P["tray_x"] - 2 * P["tray_rim"], P["tray_y"] - 2 * P["tray_rim"]
    glaz_bot = P["glaz_z0"]
    top_edge = world(0, P["box_y"] / 2, glaz_bot + P["glaz_t"] + P["lid_frame"][1], P)[2]
    low_edge = world(0, -P["box_y"] / 2, glaz_bot + P["glaz_t"] + P["lid_frame"][1], P)[2]
    fin_bottom = min(world(0, y, P["plate_top"] - P["plate_t"] - P["fin_h"], P)[2]
                     for y in (-P["box_y"] / 2, P["box_y"] / 2))
    SG = stand_geometry(P)
    return {
        "aperture_m2": P["box_x"] * P["box_y"] / 1e6,           # glazed lid, outer
        "inner_m2": ix * iy / 1e6,                               # inside the walls
        "inner_x_m": ix / 1e3, "inner_y_m": iy / 1e3,
        "tray_m2": 4 * P["tray_x"] * P["tray_y"] / 1e6,          # tray footprint (black tops)
        "bed_m2": 4 * bed_x * bed_y / 1e6,                       # sorbent surface
        "gap_under_m": (P["tray_z0"] - P["plate_top"]) / 1e3,    # bed underside to condenser
        "gap_over_m": (glaz_bot - P["tray_z0"] - P["tray_h"]) / 1e3,  # tray rim to glazing
        "bed_depth_m": P["bed_depth"] / 1e3,
        "plate_m2": P["plate_xy"][0] * P["plate_xy"][1] / 1e6,
        "fin_len_m": (P["box_y"] - 80) / 1e3,
        "fin_h_m": P["fin_h"] / 1e3, "fin_t_m": P["fin_t"] / 1e3, "fin_n": P["fin_n"],
        "fin_pitch_m": P["fin_pitch"] / 1e3,
        "top_edge_m": top_edge / 1e3, "low_edge_m": low_edge / 1e3,
        "fin_bottom_m": fin_bottom / 1e3,
        "box_centre_z_m": P["z0"] / 1e3,
        "leg_span_y_m": (SG[1]["Yc"] - SG[-1]["Yc"]) / 1e3,     # horizontal distance between leg lines
        "leg_span_x_m": (P["box_x"] - 40) / 1e3,
        "box_air_m3": ix * iy * P["wall_h"] / 1e9,
        "wall_area_m2": 2 * (P["box_x"] + P["box_y"]) * P["wall_h"] / 1e6,
        "baffle_m2": ((ix - 2 * P["deck_gap"]) * (iy - 2 * P["deck_gap"]) - 4 * bed_x * bed_y) / 1e6,
        "screen_open": (P["scr_pitch"] - P["scr_w"]) / P["scr_pitch"],   # open share of each channel layer
        "screen_t_m": (P["scr_z_hi"] + P["scr_lip"] - P["scr_z_lo"]) / 1e3,  # depth of the two layers
        "sump_l": 4 * (P["tray_x"] - 20) * (P["sump"][0] - 2) * (P["sump"][1] - 1) / 1e6,  # brine sump volume, L
        "inlet_m2": P["flap_in"][0] * P["flap_in"][1] / 1e6,
        "slot_m2": P["slot_out"][0] * P["slot_out"][1] / 1e6,
    }


# ---------------------------------------------------------------------------------------------
def _b():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, r, h):
    b = _b()
    return b.Pos(x, y, z0 + h / 2) * b.Cylinder(r, h)


def xcyl(x0, y, z, r, h):
    b = _b()
    return b.Pos(x0 + h / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def ycyl(x, y0, z, r, h):
    b = _b()
    return b.Pos(x, y0 + h / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def hexz(x, y, z0, af, h):
    b = _b()
    return b.Pos(x, y, z0 + h / 2) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)


def hexx(x0, y, z, af, h):
    b = _b()
    return b.Pos(x0 + h / 2, y, z) * b.Rot(0, 90, 0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)


def hexy(x, y0, z, af, h):
    b = _b()
    return b.Pos(x, y0 + h / 2, z) * b.Rot(90, 0, 0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def tube(a, c, r):
    """Round bar or tube of radius r between two points."""
    b = _b()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def angle_yz(xa, xb, p0, p1, size, t, flange_side, ext=0.0):
    """Steel angle lying in the plane x = xa..xb (its flat leg), between world points p0 and p1 given
    as (Y, Z), extended ext beyond each point. Its second leg stands out from the flat leg's outer
    face (the one at xb) across the bar, on the edge given by flange_side (+1 upper, -1 lower)."""
    b = _b()
    (y0, z0), (y1, z1) = p0, p1
    L = math.hypot(y1 - y0, z1 - z0)
    ang = math.degrees(math.atan2(z1 - z0, y1 - y0))
    sgn = 1 if xb > xa else -1
    xm = (xa + xb) / 2
    flat = b.Pos(xm, 0, 0) * b.Box(abs(xb - xa), L + 2 * ext, size)
    out_leg = b.Pos(xb + sgn * (size - t) / 2 - sgn * 0, 0, flange_side * (size - t) / 2) * b.Box(size - t, L + 2 * ext, t)
    loc = b.Pos(0, (y0 + y1) / 2, (z0 + z1) / 2) * b.Rot(ang, 0, 0)
    return loc * (flat + out_leg)


# ---------------------------------------------------------------------------------------------
def wall_layers(P=PARAMS):
    """The four wall panels in the local frame, each as (skins, battens, foam). North and south
    panels run the full 1,100 mm; east and west panels fit between them."""
    LX, LY, WT, sk = P["box_x"], P["box_y"], P["wall_t"], P["skin_t"]
    z0, z1 = P["wall_z0"], P["wall_z0"] + P["wall_h"]
    hb, ht, pw = P["batten_bot"], P["batten_top"], P["post_w"]
    zb, zt = z0 + hb, z1 - ht
    fw, fh = P["flap_in"]
    fzc = P["flap_in_z"]
    sw, sh = P["slot_out"]
    fx = P["fan_x"]
    out = {}
    for side in ("south", "north", "east", "west"):
        if side in ("south", "north"):
            sg = -1 if side == "south" else 1
            yo, yi = sg * LY / 2, sg * (LY / 2 - WT)
            ylo, yhi = min(yo, yi), max(yo, yi)
            skin_o = bx(-LX / 2, LX / 2, *sorted((yo, yo - sg * sk)), z0, z1)
            skin_i = bx(-LX / 2, LX / 2, *sorted((yi, yi + sg * sk)), z0, z1)
            cy0, cy1 = ylo + sk, yhi - sk
            core = bx(-LX / 2, LX / 2, cy0, cy1, z0, z1)
            bat = (bx(-LX / 2, LX / 2, cy0, cy1, z0, zb) + bx(-LX / 2, LX / 2, cy0, cy1, zt, z1)
                   + bx(-LX / 2, -LX / 2 + pw, cy0, cy1, zb, zt) + bx(LX / 2 - pw, LX / 2, cy0, cy1, zb, zt))
            hole = None
            if side == "south":       # inlet opening, framed by a sill and two jamb posts
                fz0, fz1 = fzc - fh / 2, fzc + fh / 2
                bat = bat + bx(-fw / 2 - pw, fw / 2 + pw, cy0, cy1, zb, fz0) \
                    + bx(-fw / 2 - pw, -fw / 2, cy0, cy1, fz0, zt) + bx(fw / 2, fw / 2 + pw, cy0, cy1, fz0, zt)
                hole = bx(-fw / 2, fw / 2, ylo - 1, yhi + 1, fz0, fz1)
            else:                     # outlet slot behind the fan hood, cut through the bottom batten
                bat = bat + bx(fx - sw / 2 - pw, fx - sw / 2, cy0, cy1, zb, zt) + bx(fx + sw / 2, fx + sw / 2 + pw, cy0, cy1, zb, zt)
                hole = bx(fx - sw / 2, fx + sw / 2, ylo - 1, yhi + 1, z0, z0 + sh)
        else:
            sg = 1 if side == "east" else -1
            xo, xi = sg * LX / 2, sg * (LX / 2 - WT)
            xlo, xhi = min(xo, xi), max(xo, xi)
            ylim = LY / 2 - WT
            skin_o = bx(*sorted((xo, xo - sg * sk)), -ylim, ylim, z0, z1)
            skin_i = bx(*sorted((xi, xi + sg * sk)), -ylim, ylim, z0, z1)
            cx0, cx1 = xlo + sk, xhi - sk
            core = bx(cx0, cx1, -ylim, ylim, z0, z1)
            bat = (bx(cx0, cx1, -ylim, ylim, z0, zb) + bx(cx0, cx1, -ylim, ylim, zt, z1)
                   + bx(cx0, cx1, -ylim, -ylim + pw, zb, zt) + bx(cx0, cx1, ylim - pw, ylim, zb, zt))
            hole = None
        foam = core - bat
        if side in ("east", "west"):          # M6 threaded inserts from below for the box to rail bolts
            for y in (-400.0, 0.0, 400.0):
                bat = bat - zcyl(sg * (LX / 2 - WT / 2), y, z0 - 1, 5.0, 21)
        skins = skin_o + skin_i
        if hole is not None:
            skins, bat, foam = skins - hole, bat - hole, foam - hole
        out[side] = (skins, bat, foam)
    return out


def build_components(P=PARAMS):
    """Every component in world coordinates, as {key: Comp}."""
    b = _b()
    s, c = _trig(P)
    W = b.Pos(0, 0, P["z0"]) * b.Rot(P["tilt"], 0, 0)
    LX, LY, WT = P["box_x"], P["box_y"], P["wall_t"]
    ix, iy = LX - 2 * WT, LY - 2 * WT
    zw0, zw1 = P["wall_z0"], P["wall_z0"] + P["wall_h"]
    C = {}

    def add(key, name, shape, bom, kind, group, material, local=False):
        C[key] = Comp(name, W * shape if local else shape, bom, kind, group, material)

    # ---------------------------------------------------------------- 2 walls
    WL = wall_layers(P)
    pilot = fuse([b.Pos(sx * (LX / 2 - WT / 2), sy * (LY / 2 - 32.5), z) * b.Rot(90, 0, 0) * b.Cylinder(2.5, 65)
                  for sx in (-1, 1) for sy in (-1, 1) for z in (zw0 + 22, zw0 + 67, zw0 + 100)])
    for side, (sk, bat, foam) in WL.items():
        add(f"wall_{side}", f"{side.capitalize()} wall panel", (sk + bat + foam) - pilot, 2, "made", "walls", f"wall_{side}", local=True)

    # ---------------------------------------------------------------- 6 condenser plate and fins
    px_, py_ = P["plate_xy"]
    pt, ptk = P["plate_top"], P["plate_t"]
    xs_w = LX / 2 - WT / 2                     # screw line under the east and west walls (530)
    ys_w = LY / 2 - WT / 2                     # screw line under the north and south walls (480)
    fx = P["fan_x"]
    sw_ = P["slot_out"][0]
    ns_x = [-525, -375, -225, -75, 75, 225, 375, 525]
    nn_x = [-525, -375, -225, -75, 75, fx - sw_ / 2 - 14, fx + sw_ / 2 + 14, 525]   # north: screws into the jamb posts
    ew_y = [-300, -150, 150, 300]
    bolt_y = [-400.0, 0.0, 400.0]              # box to rail bolts
    screws = [(x, -ys_w) for x in ns_x] + [(x, ys_w) for x in nn_x] + [(sx * xs_w, y) for sx in (-1, 1) for y in ew_y]
    bolts = [(sx * xs_w, y) for sx in (-1, 1) for y in bolt_y]
    dx_, dy_ = P["drain_x"], -LY / 2 + WT + 17.0
    plate = bx(-px_ / 2, px_ / 2, -py_ / 2, py_ / 2, pt - ptk, pt)
    for (x, y) in screws:
        plate = plate - zcyl(x, y, pt - ptk - 1, 2.75, ptk + 2)
    for (x, y) in bolts:
        plate = plate - zcyl(x, y, pt - ptk - 1, 3.25, ptk + 2)
    plate = plate - zcyl(dx_, dy_, pt - ptk - 1, 8.5, ptk + 2)
    add("plate", "Condenser plate", plate, 6, "made", "condenser", "al", local=True)
    fins = []
    x0 = -(P["fin_n"] - 1) / 2 * P["fin_pitch"]
    ft, fh, ff = P["fin_t"], P["fin_h"], P["fin_foot"]
    fl = LY - 80
    for i in range(P["fin_n"]):
        x = x0 + i * P["fin_pitch"]
        web = bx(x - ft / 2, x + ft / 2, -fl / 2, fl / 2, pt - ptk - fh, pt - ptk)
        d = -1 if x > 0 else 1                 # feet point toward the centre line
        foot = bx(*sorted((x + d * ft / 2, x + d * (ft / 2 + ff))), -fl / 2, fl / 2, pt - ptk - ft, pt - ptk)
        fins.append(web + foot)
    add("fins", "Condenser fins (21)", fuse(fins), 6, "made", "condenser", "al", local=True)
    heads = [zcyl(x, y, pt - ptk - 2.8, 4.75, 2.8) for (x, y) in screws]
    add("plate_screws", "Plate screws, M5 button head, into the bottom battens", fuse(heads), None, "fixing", None, "steel", local=True)
    ins = [zcyl(x, y, pt, 5.0, 20) - zcyl(x, y, pt - 1, 3.0, 22) for (x, y) in bolts]
    add("inserts", "Threaded inserts, M6, in the bottom battens", fuse(ins), None, "fixing", None, "steel", local=True)
    cs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (zw0 + 22, zw0 + 67, zw0 + 100):
                cs.append(b.Pos(sx * (LX / 2 - WT / 2), sy * (LY / 2 - 32.5), z) * b.Rot(90, 0, 0) * b.Cylinder(2.5, 65)
                          + b.Pos(sx * (LX / 2 - WT / 2), sy * (LY / 2 + 1.5), z) * b.Rot(90, 0, 0) * b.Cylinder(4.5, 3))
    add("corner_screws", "Corner screws, 5 x 65 mm stainless wood screws", fuse(cs), None, "fixing", None, "steel", local=True)

    # ---------------------------------------------------------------- 7 gutter and drain
    gw, gh = P["gutter_w"], P["gutter_h"]
    gy0 = -LY / 2 + WT
    gutter = bx(-ix / 2, ix / 2, gy0, gy0 + gw, pt, pt + 1) + bx(-ix / 2, ix / 2, gy0, gy0 + 1, pt + 1, pt + gh)
    gutter = gutter - zcyl(dx_, dy_, pt - 1, 8.5, 3)
    add("gutter", "Gutter", gutter, 7, "made", "gutter", "al", local=True)
    fit = (zcyl(dx_, dy_, pt + 1, 15, 3) + zcyl(dx_, dy_, pt - ptk - 5, 8.25, ptk + 9)
           + hexz(dx_, dy_, pt - ptk - 5, 27, 5) + zcyl(dx_, dy_, pt - ptk - 25, 6, 20))
    add("drain_fit", "Drain fitting (bulkhead, hose barb)", fit, 7, "bought", "gutter", "plastic", local=True)
    bxx, byy = P["bottle_xy"]
    bw, bd, bh = P["bottle"]
    tip = world(dx_, dy_, pt - ptk - 25, P)
    tip2 = world(dx_, dy_, pt - ptk - 40, P)          # first 15 mm along the fitting's axis
    bend = (tip2[0], tip2[1], tip2[2] - 30)
    cap = (bxx, byy + 40, bh + 40)
    above = (cap[0], cap[1], cap[2] + 20)
    tube_ = (tube(tip, tip2, 8) + b.Pos(*tip2) * b.Sphere(8) + tube(tip2, bend, 8) + b.Pos(*bend) * b.Sphere(8) + tube(bend, above, 8) + b.Pos(*above) * b.Sphere(8)
             + tube(above, cap, 8))
    add("drain_tube", "Drain tube, silicone 12 mm bore", tube_, 7, "bought", "gutter", "silicone")
    bottle = bx(bxx - bw / 2, bxx + bw / 2, byy - bd / 2, byy + bd / 2, 0, bh) + zcyl(bxx, byy + 40, bh, 28, 40)
    add("bottle", "Collection bottle, 10 L", bottle, 8, "bought", "bottle", "bottle")

    # ---------------------------------------------------------------- 16 ledges and tray deck
    lg, lt = P["ledge"]
    dh, dt = P["deck_bar"]
    dz1 = P["tray_z0"] - P["baffle_t"]          # deck bar tops (109)
    dz0 = dz1 - dh                              # deck bar bottoms (89)
    gap = P["deck_gap"]
    hx, hy = ix / 2 - gap, iy / 2 - gap         # deck outer half sizes (508, 458)
    ledges = []
    for sx in (-1, 1):
        xo = sx * ix / 2
        ledges.append(bx(*sorted((xo, xo - sx * lg)), -iy / 2 + 5, iy / 2 - 5, dz0 - lt, dz0)
                      + bx(*sorted((xo, xo - sx * lt)), -iy / 2 + 5, iy / 2 - 5, dz0 - lg, dz0 - lt))
    add("ledges", "Wall ledges (2)", fuse(ledges), 16, "made", "deck", "al", local=True)
    bars = [bx(hx - dt, hx, -hy, hy, dz0, dz1), bx(-hx, -hx + dt, -hy, hy, dz0, dz1),
            bx(-hx + dt, hx - dt, hy - dt, hy, dz0, dz1), bx(-hx + dt, hx - dt, -hy, -hy + dt, dz0, dz1),
            bx(-dt / 2, dt / 2, -hy + dt, hy - dt, dz0, dz1),
            bx(dt / 2, hx - dt, -dt / 2, dt / 2, dz0, dz1), bx(-hx + dt, -dt / 2, -dt / 2, dt / 2, dz0, dz1)]
    # small angle brackets in the inside corners, riveted to both bars (18 tall, legs 20 x 2)
    br = []
    bl, bt = 20.0, 2.0
    corners = [(hx - dt, hy - dt, -1, -1), (-hx + dt, hy - dt, 1, -1), (hx - dt, -hy + dt, -1, 1), (-hx + dt, -hy + dt, 1, 1),
               (dt / 2, hy - dt, 1, -1), (-dt / 2, hy - dt, -1, -1), (dt / 2, -hy + dt, 1, 1), (-dt / 2, -hy + dt, -1, 1),
               (hx - dt, dt / 2, -1, 1), (-hx + dt, dt / 2, 1, 1), (hx - dt, -dt / 2, -1, -1), (-hx + dt, -dt / 2, 1, -1),
               (dt / 2, dt / 2, 1, 1), (-dt / 2, dt / 2, -1, 1), (dt / 2, -dt / 2, 1, -1), (-dt / 2, -dt / 2, -1, -1)]
    for (x, y, sx, sy) in corners:
        za, zb_ = dz0 + 1, dz1 - 1
        br.append(bx(*sorted((x, x + sx * bl)), *sorted((y, y + sy * bt)), za, zb_)
                  + bx(*sorted((x, x + sx * bt)), *sorted((y + sy * bt, y + sy * bl)), za, zb_))
    add("deck_frame", "Tray deck frame", fuse(bars + br), 16, "made", "deck", "al", local=True)
    bed_x, bed_y = P["tray_x"] - 2 * P["tray_rim"], P["tray_y"] - 2 * P["tray_rim"]
    baffle = bx(-hx, hx, -hy, hy, dz1, P["tray_z0"])
    for (x, y) in tray_centres(P):
        baffle = baffle - bx(x - bed_x / 2, x + bed_x / 2, y - bed_y / 2, y + bed_y / 2, dz1 - 1, P["tray_z0"] + 1)
    add("baffle", "Sealing baffle sheet", baffle, 16, "made", "deck", "al", local=True)

    # ---------------------------------------------------------------- 15 drip screens, hung from the deck
    sw, lip, st, sp = P["scr_w"], P["scr_lip"], P["scr_t"], P["scr_pitch"]
    rim = P["tray_rim"]
    sl = P["tray_y"] - 2 * rim
    swp, sdp = P["sump"]
    zf0 = P["scr_frame_z0"]
    chan = bx(-sw / 2, sw / 2, -sl / 2, sl / 2, 0, lip) - bx(-sw / 2 + st, sw / 2 - st, -sl / 2 - 1, sl / 2 + 1, st, lip + 1)
    scr = []
    for (xc, yc) in tray_centres(P):
        north = yc > 0
        xa, xb = xc - (P["tray_x"] / 2 - 9), xc + (P["tray_x"] / 2 - 9)       # side plate outer faces (x 15 and 489)
        y_sump0 = dt / 2 if north else -hy + dt                               # sump south face on a deck bar
        y_end = hy - dt if north else -dt / 2                                 # end plate north face on a deck bar
        n = int((bed_x - sw) // sp) + 1
        x0c = xc - (n - 1) * sp / 2
        items = []
        for i in range(n):
            items.append(b.Pos(x0c + i * sp, yc, P["scr_z_hi"]) * chan)
            if i < n - 1:
                items.append(b.Pos(x0c + (i + 0.5) * sp, yc, P["scr_z_lo"]) * chan)
        # side plates, end plate (with a riveting tab up the deck bar face), sump with its tab
        items.append(bx(xa, xa + 1, y_sump0, y_end - 1, zf0, P["scr_z_hi"] - 2))
        items.append(bx(xb - 1, xb, y_sump0, y_end - 1, zf0, P["scr_z_hi"] - 2))
        items.append(bx(xa, xb, y_end - 1, y_end, zf0, P["scr_z_hi"] - 2) + bx(xa + 25, xb - 25, y_end - 1, y_end, P["scr_z_hi"] - 2, dz1 - 4))
        sump = bx(xa + 1, xb - 1, y_sump0, y_sump0 + swp, zf0, zf0 + sdp) - bx(xa + 2, xb - 2, y_sump0 + 1, y_sump0 + swp - 1, zf0 + 1, zf0 + sdp + 1)
        sump = sump + bx(xa + 25, xb - 25, y_sump0, y_sump0 + 1, zf0 + sdp, dz1 - 4)
        items.append(sump)
        # cross straps, 15 x 2 flat bar: upper pair on the side plate tops, lower pair between the plates
        for yy in (yc - 120, yc + 120):
            items.append(bx(xa, xb, yy - 7.5, yy + 7.5, P["scr_z_hi"] - 2, P["scr_z_hi"]))
            items.append(bx(xa + 1, xb - 1, yy - 7.5, yy + 7.5, P["scr_z_lo"] - 2, P["scr_z_lo"]))
        scr.append(fuse(items))
    add("screens", "Drip screens (4)", b.Compound(children=scr), 15, "made", "screens", "screens", local=True)

    # ---------------------------------------------------------------- 4 trays and 5 sorbent
    trays, mesh, bed = [], [], []
    tz0, th, tsh = P["tray_z0"], P["tray_h"], P["tray_sheet"]
    for (x, y) in tray_centres(P):
        ox0, ox1, oy0, oy1 = x - P["tray_x"] / 2, x + P["tray_x"] / 2, y - P["tray_y"] / 2, y + P["tray_y"] / 2
        walls_ = bx(ox0, ox1, oy0, oy1, tz0, tz0 + th) - bx(ox0 + tsh, ox1 - tsh, oy0 + tsh, oy1 - tsh, tz0 - 1, tz0 + th + 1)
        lip_ = bx(ox0 + tsh, ox1 - tsh, oy0 + tsh, oy1 - tsh, tz0, tz0 + tsh) - bx(x - bed_x / 2, x + bed_x / 2, y - bed_y / 2, y + bed_y / 2, tz0 - 1, tz0 + 2)
        trays.append(walls_ + lip_)
        mesh.append(bx(ox0 + tsh, ox1 - tsh, oy0 + tsh, oy1 - tsh, tz0 + tsh, tz0 + tsh + P["mesh_t"]))
        zb0 = tz0 + tsh + P["mesh_t"]
        bed.append(bx(x - bed_x / 2, x + bed_x / 2, y - bed_y / 2, y + bed_y / 2, zb0, zb0 + P["bed_depth"]))
    add("trays", "Sorbent trays (4)", fuse(trays), 4, "made", "trays", "al", local=True)
    add("mesh", "Tray floors, stainless mesh on expanded metal (4)", fuse(mesh), 4, "bought", "trays", "mesh", local=True)
    add("bed", "Composite sorbent", fuse(bed), 5, "made", "bed", "sorbent", local=True)

    # ---------------------------------------------------------------- 3 glazing lid
    fd, fwt = P["lid_frame"]
    gz0, gt = P["glaz_z0"], P["glaz_t"]
    fz0, fz1 = gz0 - fwt, gz0 + gt + fwt       # frame 178 to 192
    frame = bx(-LX / 2, LX / 2, -LY / 2, LY / 2, fz0, fz1) - bx(-LX / 2 + fd, LX / 2 - fd, -LY / 2 + fd, LY / 2 - fd, fz0 - 1, fz1 + 1) \
        - bx(-LX / 2 + fwt, LX / 2 - fwt, -LY / 2 + fwt, LY / 2 - fwt, gz0, gz0 + gt)
    add("lid_frame", "Lid frame, aluminium U-channel", frame, 3, "made", "glazing", "al", local=True)
    pc = bx(-LX / 2 + fwt, LX / 2 - fwt, -LY / 2 + fwt, LY / 2 - fwt, gz0, gz0 + gt)
    add("glazing", "Twin-wall polycarbonate sheet", pc, 3, "bought", "glazing", "pc", local=True)
    hinges = []
    for x in (-440.0, 0.0, 470.0):
        hinges.append(bx(x - 30, x + 30, LY / 2, LY / 2 + 2, zw1 - 18, zw1) + bx(x - 30, x + 30, LY / 2, LY / 2 + 2, fz0, fz1 - 2)
                      + xcyl(x - 30, LY / 2 + 3, zw1, 3, 60))
    add("lid_hinges", "Lid hinges (3)", fuse(hinges), 3, "bought", "glazing", "steel", local=True)
    latches = []
    for x in (-475.0, 475.0):
        latches.append(bx(x - 20, x + 20, -LY / 2 - 12, -LY / 2, zw1 - 28, zw1 - 4) + bx(x - 15, x + 15, -LY / 2 - 2, -LY / 2, fz0 + 2, fz1 - 2)
                       + bx(x - 4, x + 4, -LY / 2 - 6, -LY / 2 - 2, zw1 - 6, fz0 + 8))
    add("lid_latches", "Lid latches (2)", fuse(latches), 3, "bought", "glazing", "steel", local=True)

    # ---------------------------------------------------------------- 9 inlet flap
    fwi, fhi = P["flap_in"]
    fzc = P["flap_in_z"]
    flap = bx(-fwi / 2 - 20, fwi / 2 + 20, -LY / 2 - 1.5, -LY / 2, fzc - fhi / 2 - 10, fzc + fhi / 2 + 10)
    add("flap", "Inlet flap", flap, 9, "made", "flap", "al", local=True)
    kz = fzc + fhi / 2 + 10 + 2.5
    fhw = xcyl(-fwi / 2 - 20, -LY / 2 - 2.5, kz, 2.5, fwi + 40)
    flatch = []
    for x in (-300.0, 300.0):
        zt_ = fzc - fhi / 2 - 10
        flatch.append(bx(x - 15, x + 15, -LY / 2 - 10, -LY / 2, zt_ - 22, zt_ - 4) + bx(x - 3, x + 3, -LY / 2 - 6, -LY / 2 - 1.5, zt_ - 4, zt_ + 6))
    add("flap_hw", "Flap hinge and latches (2)", fhw + fuse(flatch), 9, "bought", "flap", "steel", local=True)

    # ---------------------------------------------------------------- 10 fan hood, fan and outlet flap
    hwid, hdep, hht = P["fan_hood"]
    hx0, hx1 = fx - hwid / 2, fx + hwid / 2
    hz0, hz1 = zw0, zw0 + hht
    y0h = LY / 2
    hood = bx(hx0, hx1, y0h, y0h + hdep, hz0, hz1) - bx(hx0 + 1, hx1 - 1, y0h - 1, y0h + hdep - 1, hz0 + 1, hz1 - 1)
    hood = hood + bx(hx0 - 15, hx0, y0h, y0h + 1, hz0, hz1) + bx(hx1, hx1 + 15, y0h, y0h + 1, hz0, hz1)
    fzc_ = (hz0 + hz1) / 2
    hood = hood - ycyl(fx, y0h + hdep - 2, fzc_, 57, 4)
    add("hood", "Fan hood", hood, 10, "made", "fan", "al", local=True)
    fan = bx(fx - 60, fx + 60, y0h + hdep - 1 - 25, y0h + hdep - 1, fzc_ - 60, fzc_ + 60) - ycyl(fx, y0h + hdep - 30, fzc_, 56, 30)
    fan = fan + ycyl(fx, y0h + hdep - 26, fzc_, 20, 24)
    add("fan", "Night fan, 12 V 120 mm", fan, 10, "bought", "fan", "fan", local=True)
    ow, oh = P["flap_out"]
    oflap = bx(fx - ow / 2, fx + ow / 2, y0h + hdep, y0h + hdep + 1.5, fzc_ - oh / 2 - 1, fzc_ + oh / 2 - 1)
    oflap = oflap + xcyl(fx - ow / 2, y0h + hdep + 2.5, fzc_ + oh / 2 + 1.5 - 1, 2.5, ow)
    add("oflap", "Outlet flap with hinge", oflap, 10, "made", "fan", "al", local=True)

    # ---------------------------------------------------------------- 1 stand (world)
    SG = stand_geometry(P)
    a, t = P["leg"], P["leg_t"]
    xr = SG[1]["xr"]                                 # 545
    rails = []
    zr1 = pt - ptk
    for sx in (-1, 1):
        r = bx(*sorted((sx * (xr - a), sx * xr)), -LY / 2, LY / 2, zr1 - t, zr1) \
            + bx(*sorted((sx * xr, sx * (xr - t))), -LY / 2, LY / 2, zr1 - a, zr1 - t)
        for (x, y) in screws:
            if xr - a - 6 < x * sx < xr + 6:
                r = r - zcyl(x, y, zr1 - t - 1, 6.0, t + 2)
        for (x, y) in bolts:
            if x * sx > 0:
                r = r - zcyl(x, y, zr1 - t - 1, 3.25, t + 2)
        rails.append(r)
    leg_parts, feet, cleats, sbolts = [], [], [], []
    hole8 = 4.5
    for ys in (-1, 1):
        g = SG[ys]
        Yc, top = g["Yc"], g["top"]
        for sx in (-1, 1):
            xa_, xb_ = sx * xr, sx * (xr + t)               # face flange (on the rail)
            yf = Yc + ys * a / 2                            # outward flange on the outer end (south legs: south)
            face = bx(*sorted((xa_, xb_)), Yc - a / 2, Yc + a / 2, P["foot_t"], top)
            outw = bx(*sorted((sx * xr, sx * (xr + a))), *sorted((yf, yf - ys * t)), P["foot_t"], top)
            leg = face + outw
            leg_parts.append(((ys, sx), leg))
            # foot plate and cleat
            fxc = sx * (xr + a / 2 - 15)
            feet.append(bx(fxc - P["foot"] / 2, fxc + P["foot"] / 2, Yc - P["foot"] / 2, Yc + P["foot"] / 2, 0, P["foot_t"]))
            cl = bx(*sorted((sx * xr, sx * (xr - t))), Yc - a / 2 + 4, Yc + a / 2 - 4, P["foot_t"], P["foot_t"] + a) \
                + bx(*sorted((sx * xr, sx * (xr - a))), Yc - a / 2 + 4, Yc + a / 2 - 4, P["foot_t"], P["foot_t"] + t)
            cleats.append(cl)
    legs = dict(leg_parts)
    # side braces on the outer faces of the legs' face flanges: south leg high to north leg low
    braces, bpts = [], {}
    for sx in (-1, 1):
        ps = (SG[-1]["Yc"] + 5, 400.0)
        pn = (SG[1]["Yc"] - 5, 150.0)
        xa_, xb_ = sx * (xr + t), sx * (xr + 2 * t)
        braces.append(angle_yz(xa_, xb_, ps, pn, a, t, -1, ext=12.0))
        bpts[sx] = (ps, pn)
    # end cross members on the outward flanges, outside the frame
    xms = []
    for ys in (-1, 1):
        Yo = SG[ys]["Yc"] + ys * a / 2                     # outer face of the outward flanges
        z0x = P["xm_z"]
        xms.append(bx(-(xr + a), xr + a, *sorted((Yo, Yo + ys * t)), z0x, z0x + a)
                   + bx(-(xr + a), xr + a, *sorted((Yo, Yo + ys * a)), z0x, z0x + t))
    # south end diagonal, on the outer face of the south cross member plane, above it
    Yo = SG[-1]["Yc"] - a / 2
    pw_ = (-(xr + a / 2), 275.0)
    pe_ = (xr + a / 2, 470.0)
    L = math.hypot(pe_[0] - pw_[0], pe_[1] - pw_[1])
    ang = math.degrees(math.atan2(pe_[1] - pw_[1], pe_[0] - pw_[0]))
    dia = b.Pos(0, Yo - t / 2, (pw_[1] + pe_[1]) / 2) * b.Rot(0, -ang, 0) * (
        b.Box(L + 24, t, a) + b.Pos(0, -(a - t) / 2 - t / 2, -(a - t) / 2) * b.Box(L + 24, a - t, t))
    # anchors (bought), outboard of the south legs
    anchors = []
    for sx in (-1, 1):
        ax_ = sx * (xr + a + 190)
        ay_ = SG[-1]["Yc"]
        anchors.append(zcyl(ax_, ay_, -400, 5, 430) + b.Pos(ax_, ay_, 45) * b.Rot(90, 0, 0) * b.Torus(12, 3)
                       + b.Pos(ax_, ay_, -330) * b.Cylinder(40, 4))
    # bolts: leg to rail (along x), braces, cross members, diagonal, cleats
    for ys in (-1, 1):
        g = SG[ys]
        for sx in (-1, 1):
            sbolts.append((("x", sx), (g["Yc"], g["bolt_z"]), sx * (xr - t), sx * (xr + t)))
            sbolts.append((("x", sx), (g["Yc"], P["foot_t"] + a / 2 + 2), sx * (xr - t), sx * (xr + t)))  # cleat to leg
    for sx in (-1, 1):
        ps, pn = bpts[sx]
        sbolts.append((("x", sx), ps, sx * xr, sx * (xr + 2 * t)))
        sbolts.append((("x", sx), pn, sx * xr, sx * (xr + 2 * t)))
    bolt_shapes, cutters = [], []
    for (ax_, sx), (Y, Z), xa_, xb_ in sbolts:
        x0b, x1b = min(xa_, xb_), max(xa_, xb_)
        bolt_shapes.append(xcyl(x0b - 0.0, Y, Z, 4, x1b - x0b) + hexx(x1b, Y, Z, 13, 5.5) + hexx(x0b - 6.5, Y, Z, 13, 6.5))
        cutters.append(xcyl(x0b - 1, Y, Z, hole8, x1b - x0b + 2))
    for ys in (-1, 1):
        Yo = SG[ys]["Yc"] + ys * a / 2
        for sx in (-1, 1):
            X, Z = sx * (xr + a / 2 + 2), P["xm_z"] + a / 2 + 2
            y0b, y1b = sorted((Yo - ys * t, Yo + ys * t))
            bolt_shapes.append(ycyl(X, y0b, Z, 4, y1b - y0b) + hexy(X, y1b, Z, 13, 5.5) + hexy(X, y0b - 6.5, Z, 13, 6.5))
            cutters.append(ycyl(X, y0b - 1, Z, hole8, y1b - y0b + 2))
    for (X, Z) in (pw_, pe_):
        Yo = SG[-1]["Yc"] - a / 2
        y0b, y1b = Yo - t, Yo + t
        bolt_shapes.append(ycyl(X, y0b, Z, 4, 2 * t) + hexy(X, y1b, Z, 13, 5.5) + hexy(X, y0b - 6.5, Z, 13, 6.5))
        cutters.append(ycyl(X, y0b - 1, Z, hole8, 2 * t + 2))
    for ys in (-1, 1):                              # cleat to foot: countersunk bolt up through the plate
        for sx in (-1, 1):
            X = sx * (xr - a / 2 - 2)
            Y = SG[ys]["Yc"]
            bolt_shapes.append(zcyl(X, Y, 0, 4, P["foot_t"] + t) + hexz(X, Y, P["foot_t"] + t, 13, 6.5))
            cutters.append(zcyl(X, Y, -1, hole8, P["foot_t"] + t + 2))
    cut = fuse(cutters)

    def drill(sh):
        return sh - cut

    for i, sx in enumerate((-1, 1)):
        add(f"rail_{'w' if sx < 0 else 'e'}", f"{'West' if sx < 0 else 'East'} rail", drill(W * rails[i]), 1, "made", "stand", "steel")
    for (ys, sx), leg in legs.items():
        nm = f"{'north' if ys > 0 else 'south'}-{'west' if sx < 0 else 'east'}"
        add(f"leg_{'n' if ys > 0 else 's'}{'w' if sx < 0 else 'e'}", f"Leg, {nm}", drill(leg), 1, "made", "stand", "steel")
    add("braces", "Side braces (2)", drill(fuse(braces)), 1, "made", "stand", "steel")
    add("xm_s", "South cross member", drill(xms[0]), 1, "made", "stand", "steel")
    add("xm_n", "North cross member", drill(xms[1]), 1, "made", "stand", "steel")
    add("diag", "South diagonal brace", drill(dia), 1, "made", "stand", "steel")
    add("feet", "Foot plates (4)", drill(fuse(feet)), 1, "made", "stand", "steel")
    add("cleats", "Foot cleats (4)", drill(fuse(cleats)), 1, "made", "stand", "steel")
    add("anchors", "Ground anchors (2)", fuse(anchors), 1, "bought", "stand", "steel")
    add("stand_bolts", "Stand bolts, M8", fuse(bolt_shapes), None, "fixing", None, "steel")
    rb = []
    for (x, y) in bolts:
        rb.append(hexz(x, y, zr1 - t - 5, 10, 5) + zcyl(x, y, zr1 - t, 3, t + ptk + 18))
    add("rail_bolts", "Box to rail bolts, M6, into threaded inserts", fuse(rb), None, "fixing", None, "steel", local=True)

    # ---------------------------------------------------------------- 11 PV pole and panel (north-east leg)
    gN = SG[1]
    Yc = gN["Yc"]
    sp_ = 8.0                                         # spacer between leg and pole
    pq = 25.0                                         # square tube 25 x 25 x 2
    px0 = xr + t + sp_
    pole_z0, pole_z1 = gN["top"] - 330, P["pv_z"] - 70
    Yp = Yc - 2.0                                     # clear of the leg's outer flange on its north edge
    pzb = (pole_z0 + 30, gN["top"] - 60)
    pole = bx(px0, px0 + pq, Yp - pq / 2, Yp + pq / 2, pole_z0, pole_z1) - bx(px0 + 2, px0 + pq - 2, Yp - pq / 2 + 2, Yp + pq / 2 - 2, pole_z0 - 1, pole_z1 + 1)
    spacers = fuse([bx(xr + t, px0, Yp - 12, Yp + 12, z - 12, z + 12) for z in pzb])
    pbolts = fuse([xcyl(xr, Yp, z, 4, t + sp_ + pq) + hexx(xr - 5.5, Yp, z, 13, 5.5) + hexx(px0 + pq, Yp, z, 13, 6.5)
                   for z in pzb])
    pcut = fuse([xcyl(xr - 2, Yp, z, hole8, t + sp_ + pq + 4) for z in pzb])
    C["leg_ne"].shape = C["leg_ne"].shape - pcut
    pvx, pvy, pvz = P["pv_size"]
    pcx = px0 + pq / 2
    tilt_pv = P["tilt"] + 10
    # pole-top bracket: a sleeve with a top plate, a lug and a tilt pin; the panel plate pivots on the pin
    rp = 6.0
    tz = pole_z1 + 6 + 30                              # pin axis height
    tr = math.radians(tilt_pv)
    nrm = (0.0, -math.sin(tr), math.cos(tr))
    head = b.Pos(pcx, Yp + rp * nrm[1], tz + rp * nrm[2]) * b.Rot(tilt_pv, 0, 0)   # plate underside tangent to the pin
    sleeve = (bx(pcx - pq / 2 - 3, pcx + pq / 2 + 3, Yp - pq / 2 - 3, Yp + pq / 2 + 3, pole_z1 - 40, pole_z1 + 6)
              - bx(pcx - pq / 2, pcx + pq / 2, Yp - pq / 2, Yp + pq / 2, pole_z1 - 41, pole_z1))
    lug = bx(pcx - 30, pcx + 30, Yp - 6, Yp + 6, pole_z1 + 6, tz) + xcyl(pcx - 30, Yp, tz, rp, 60)
    bracket = sleeve + lug + head * (b.Pos(0, 0, 3) * b.Box(330, 120, 6))
    panel = head * (b.Pos(0, 0, 6 + pvz / 2) * (b.Box(pvx, pvy, pvz) - b.Pos(0, 0, -3) * b.Box(pvx - 30, pvy - 30, pvz - 5)))
    add("pv_pole", "PV pole, square tube, with spacers", pole - pcut + spacers - pcut, 11, "made", "pv", "steel")
    add("pv_bracket", "Panel tilt bracket", bracket, 11, "bought", "pv", "steel")
    add("pv", "PV panel, 10 W", panel, 11, "bought", "pv", "pv")
    add("pv_bolts", "Pole bolts, M8", pbolts, None, "fixing", None, "steel")

    # ---------------------------------------------------------------- 12 electronics and 13 sensor shield (north-west leg)
    ebx, eby, ebz = P["ebox"]
    # backing plate on the north face of the north-west leg's outer flange (the north frame has no diagonal)
    Yb0 = Yc + a / 2                                   # north face of the outer flange
    Yb1 = Yb0 + 3
    bxc = -(xr + a / 2)                                # 560 west
    bp_z0, bp_z1 = gN["top"] - 560, gN["top"] - 130
    bplate = bx(bxc - 90, bxc + 70, Yb0, Yb1, bp_z0, bp_z1)
    ecut = fuse([ycyl(bxc, Yb0 - t - 1, z, hole8, t + 5) for z in (bp_z0 + 30, bp_z1 - 30)])
    ebolts = fuse([ycyl(bxc, Yb0 - t, z, 4, t + 3) + hexy(bxc, Yb1, z, 13, 5.5) + hexy(bxc, Yb0 - t - 6.5, z, 13, 6.5)
                   for z in (bp_z0 + 30, bp_z1 - 30)])
    C["leg_nw"].shape = C["leg_nw"].shape - ecut
    add("eplate", "Electronics backing plate", bplate - ecut, 12, "made", "ebox", "al")
    ez0 = bp_z0 + 60
    ebox = bx(bxc - 20 - ebx / 2, bxc - 20 + ebx / 2, Yb1, Yb1 + eby, ez0, ez0 + ebz)
    add("ebox", "Electronics box", ebox, 12, "bought", "ebox", "ebox")
    add("ebolts", "Backing plate bolts, M8", ebolts, None, "fixing", None, "steel")
    sz0 = bp_z1 + 10
    arm = (bx(bxc - 70, bxc - 50, Yb1, Yb1 + 3, bp_z1 - 60, bp_z1) + bx(bxc - 70, bxc - 50, Yb1 + 3, Yb1 + 70, bp_z1 - 3, bp_z1)
           + bx(bxc - 70, bxc - 50, Yb1 + 50, Yb1 + 70, bp_z1, sz0))
    shield = zcyl(bxc - 60, Yb1 + 60, sz0, 45, 110) + arm
    add("shield", "Sensor radiation shield on its arm", shield, 13, "bought", "shield", "shield")
    return C


GROUPS = ["stand", "walls", "glazing", "deck", "trays", "bed", "screens", "condenser", "gutter", "bottle", "flap", "fan",
          "pv", "ebox", "shield"]


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom)] grouped by BOM line (fixings left out), for the concept media
    and the appearance model."""
    from build123d import Compound
    C = build_components(P)
    out = []
    for g in GROUPS:
        shapes = [c.shape for c in C.values() if c.group == g]
        bom = next(c.bom for c in C.values() if c.group == g)
        out.append((g, BOM_NAMES[bom], Compound(children=shapes), bom))
    return out


def volumes_cm3(P=PARAMS):
    """Solid volume of each component in cm3, for the mass estimate in DWD-CAL-001."""
    return {k: c.shape.volume / 1e3 for k, c in build_components(P).items()}


def build(P=PARAMS):
    """Whole assembly as one compound (used by the drawing sheet)."""
    from build123d import Compound
    return Compound(children=[c.shape for c in build_components(P).values()])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(P=PARAMS, C=None):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = C or build_components(P)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    walls = ["wall_south", "wall_north", "wall_east", "wall_west"]
    for w in walls:
        chk(f"{C[w].name} on the condenser plate", S(w), S("plate"), "touch")
        chk(f"{C[w].name} under the lid frame", S(w), S("lid_frame"), "touch")
    chk("East wall panel between the north and south panels", S("wall_east"), S("wall_north") + S("wall_south"), "touch")
    chk("West wall panel between the north and south panels", S("wall_west"), S("wall_north") + S("wall_south"), "touch")
    chk("Fins under the plate", S("fins"), S("plate"), "touch")
    chk("Fins clear of the rails", S("fins"), S("rail_e") + S("rail_w"), 5.0)
    chk("Fins clear of the drain fitting", S("fins"), S("drain_fit"), 2.0)
    chk("Gutter on the plate and against the south wall", S("gutter"), S("plate") + S("wall_south"), "touch")
    chk("Drain fitting through the gutter and plate", S("drain_fit"), S("gutter") + S("plate"), "touch")
    chk("Drain tube on the fitting", S("drain_tube"), S("drain_fit"), "touch")
    chk("Drain tube into the bottle", S("drain_tube"), S("bottle"), "touch")
    chk("Drain tube clear of the stand", S("drain_tube"), S("xm_s") + S("diag") + S("leg_se"), 10.0)
    chk("Plate screws under the plate", S("plate_screws"), S("plate"), "touch")
    chk("Plate screws clear of the rails (in the rail clearance holes)", S("plate_screws"), S("rail_e") + S("rail_w"), 0.5)
    for k in ("rail_e", "rail_w"):
        chk(f"{C[k].name} under the plate", S(k), S("plate"), "touch")
        chk(f"{C[k].name} clear of the walls", S(k), fuse([S(w) for w in walls]), 1.0)
    chk("Box to rail bolts in the rails and plate", S("rail_bolts"), S("rail_e") + S("rail_w"), "touch")
    chk("Box to rail bolts in the threaded inserts", S("rail_bolts"), S("inserts"), "touch")
    chk("Threaded inserts in the east and west bottom battens", S("inserts"), S("wall_east") + S("wall_west"), "touch")
    chk("Corner screws in the wall panels", S("corner_screws"), fuse([S(w) for w in walls]), "touch")
    chk("Ledges on the east and west walls", S("ledges"), S("wall_east") + S("wall_west"), "touch")
    chk("Deck frame on the ledges", S("deck_frame"), S("ledges"), "touch")
    chk("Deck frame clear of the walls", S("deck_frame"), fuse([S(w) for w in walls]), 1.5)
    chk("Baffle on the deck frame", S("baffle"), S("deck_frame"), "touch")
    chk("Baffle clear of the walls (EPDM lip seal closes the gap)", S("baffle"), fuse([S(w) for w in walls]), 1.5)
    chk("Drip screens hung on the deck bars", S("screens"), S("deck_frame"), "touch")
    chk("Drip screens clear of the ledges", S("screens"), S("ledges"), 1.0)
    chk("Drip screens clear of the condenser plate and gutter", S("screens"), S("plate") + S("gutter"), 5.0)
    chk("Drip screens clear of the walls", S("screens"), fuse([S(w) for w in walls]), 5.0)
    chk("Drip screens clear of the baffle", S("screens"), S("baffle"), 1.0)
    chk("Trays on the baffle", S("trays"), S("baffle"), "touch")
    chk("Trays clear of the walls", S("trays"), fuse([S(w) for w in walls]), 5.0)
    chk("Trays clear of the deck frame", S("trays"), S("deck_frame"), 0.5)
    chk("Tray floors on the tray lips", S("mesh"), S("trays"), "touch")
    chk("Sorbent on the tray floors", S("bed"), S("mesh"), "touch")
    chk("Trays clear of the glazing", S("trays"), S("glazing"), 30.0)
    chk("Glazing in the lid frame", S("glazing"), S("lid_frame"), "touch")
    chk("Lid hinges on the north wall and lid frame", S("lid_hinges"), S("wall_north") + S("lid_frame"), "touch")
    chk("Lid latches on the south wall and lid frame", S("lid_latches"), S("wall_south") + S("lid_frame"), "touch")
    chk("Lid latches clear of the inlet flap", S("lid_latches"), S("flap") + S("flap_hw"), 5.0)
    chk("Inlet flap on the south wall", S("flap"), S("wall_south"), "touch")
    chk("Flap hinge and latches on the flap and wall", S("flap_hw"), S("flap") + S("wall_south"), "touch")
    chk("Fan hood on the north wall", S("hood"), S("wall_north"), "touch")
    chk("Fan hood clear of the lid hinges", S("hood"), S("lid_hinges"), 5.0)
    chk("Fan in the hood", S("fan"), S("hood"), "touch")
    chk("Outlet flap on the hood", S("oflap"), S("hood"), "touch")
    legs = ["leg_se", "leg_sw", "leg_ne", "leg_nw"]
    for k in legs:
        rail = S("rail_e") if k.endswith("e") else S("rail_w")
        chk(f"{C[k].name} against its rail", S(k), rail, "touch")
        chk(f"{C[k].name} clear of the box", S(k), fuse([S(w) for w in walls]) + S("plate"), 2.0)
        chk(f"{C[k].name} on its foot plate", S(k), S("feet"), "touch")
        chk(f"{C[k].name} against its cleat", S(k), S("cleats"), "touch")
    chk("Cleats on the foot plates", S("cleats"), S("feet"), "touch")
    chk("Side braces on the legs", S("braces"), fuse([S(k) for k in legs]), "touch")
    chk("Side braces clear of the rails and box", S("braces"), S("rail_e") + S("rail_w") + S("plate"), 5.0)
    chk("South cross member on the south legs", S("xm_s"), S("leg_se") + S("leg_sw"), "touch")
    chk("North cross member on the north legs", S("xm_n"), S("leg_ne") + S("leg_nw"), "touch")
    chk("South diagonal on the south cross member plane, on the legs", S("diag"), S("leg_se") + S("leg_sw"), "touch")
    chk("South diagonal clear of the south cross member", S("diag"), S("xm_s"), 5.0)
    chk("Bottle clear of the stand", S("bottle"), S("xm_s") + S("diag") + S("feet"), 20.0)
    chk("PV pole spacers on the north-east leg", S("pv_pole"), S("leg_ne"), "touch")
    chk("PV pole clear of the box", S("pv_pole"), S("wall_east") + S("wall_north") + S("lid_frame") + S("plate") + S("rail_e"), 5.0)
    chk("PV pole clear of the side brace", S("pv_pole"), S("braces"), 5.0)
    chk("Panel bracket on the pole", S("pv_bracket"), S("pv_pole"), "touch")
    chk("Panel on its bracket", S("pv"), S("pv_bracket"), "touch")
    chk("Panel clear of the box", S("pv"), S("lid_frame") + S("glazing") + S("wall_north"), 100.0)
    chk("Backing plate on the north-west leg", S("eplate"), S("leg_nw"), "touch")
    chk("Backing plate clear of the side brace", S("eplate"), S("braces"), 5.0)
    chk("Backing plate clear of the box", S("eplate"), S("wall_west") + S("plate") + S("rail_w"), 5.0)
    chk("Electronics box on its backing plate", S("ebox"), S("eplate"), "touch")
    chk("Sensor shield arm on the backing plate", S("shield"), S("eplate"), "touch")
    chk("Sensor shield clear of the box", S("shield"), S("wall_west") + S("lid_frame"), 30.0)
    chk("Anchors clear of the feet", S("anchors"), S("feet"), 50.0)
    return rows


def print_checks(P=PARAMS, C=None):
    rows = checks(P, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:66s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    by_group = lambda gs: [c.shape for c in C.values() if c.group in gs]  # noqa: E731
    groups = {
        "dewdrive-assembly": [c.shape for c in C.values()],
        "collector-box": by_group(["walls", "glazing", "deck", "trays", "bed", "screens", "condenser", "gutter", "flap", "fan"]),
        "condenser": by_group(["condenser"]),
        "sorbent-trays": by_group(["deck", "trays", "bed", "screens"]),
        "stand": by_group(["stand"]),
        "power-and-logging": by_group(["pv", "ebox", "shield"]),
    }
    for name, shapes in groups.items():
        comp = Compound(children=shapes)
        export_step(comp, str(root / "step" / f"{name}.step"))
        export_stl(comp, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        print(f"exported {name}: {len(shapes)} components")
    d = derived()
    print("aperture {aperture_m2:.3f} m2, bed {bed_m2:.3f} m2, top edge {top_edge_m:.3f} m, low edge {low_edge_m:.3f} m".format(**d))
    SG = stand_geometry()
    for ys, g in SG.items():
        print(f"{'north' if ys > 0 else 'south'} legs: Y {g['Yc']:.1f}, top {g['top']:.1f}, rail bolt at {g['bolt_z']:.1f} (band {g['band'][0]:.1f} to {g['band'][1]:.1f})")
    print_checks(C=C)
