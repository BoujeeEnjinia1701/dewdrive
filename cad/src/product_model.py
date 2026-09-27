"""DewDrive product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the painted insulated box with filleted corners and a
shadow-gap parting line, an aluminium lid frame with a clear twin-wall polycarbonate pane (the
black trays and the sorbent beds show through it), lid hinges and a pull handle, lift bails on the
trays, the finned condenser under the box, the gutter and silicone drain tube, the hinged south
inlet flap with its seal and two over-centre latches, the louvred fan hood and outlet flap on the
north wall, the galvanized stand with bolted foot pads, two auger ground anchors with webbing tie
straps, a 10 L jerrycan with a moulded handle and teal cap, the framed 10 W PV panel on its pole,
the electronics box with a lit green status light and a stacked-plate radiation shield. Context is
a compact patch of compacted ground.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived(), tray_centres(), world() and
build_parts() in model.py (the stand, the drip screens, the condenser and the sorbent bed are
reused unchanged). Axes as model.py: X east to west, Y south to north (front is -Y, the glazing
faces south), Z up, ground at Z = 0. The anchor and strap positions are an appearance choice; see
docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,  # noqa: E402
                       extrude, fillet)
from model import PARAMS, build_parts, derived, tray_centres, world  # noqa: E402

TITLE = "DewDrive: solar-regenerated desiccant water harvester"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); the glazed box faces "
             "south toward the viewer with the black sorbent trays behind the clear lid, the PV panel behind "
             "it and the collection jerrycan in front"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): glazed lid, sorbent beds, "
             "trays, sealing baffle, drip screens, insulated box, condenser, gutter and jerrycan, inlet flap, "
             "fan hood, PV panel, electronics box and sensor shield, stand"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": 55,
     "note": "Detail from the back right, slightly above (about 22 deg elevation), without the ground: louvred "
             "fan hood and outlet flap on the north wall, electronics box with its green status light, "
             "radiation shield and PV pole"},
]

# Colours (restrained product palette; kit accent)
C_WALL = "#E3DFD7"       # painted plywood skin
C_ALU = "#C4C9CF"        # aluminium frame, flap, gutter
C_ALU_DARK = "#9EA5AD"
C_GALV = "#A9AFB5"       # galvanized steel stand
C_STEEL = "#8C9299"      # bolts, fittings
C_BLACK = "#23262B"      # matt black trays and screens
C_RUBBER = "#1C1F23"
C_BED = "#E6E0CC"        # silica gel and CaCl2 beads
C_CLEAR = "#DCEBF5"
C_ACCENT = "#0F766E"
C_LABEL = "#F4F4F2"
C_HOOD = "#3A3F46"
C_BOTTLE = "#E9ECEE"
C_TUBE = "#E8E6DF"
C_CELL = "#1B2436"
C_EBOX = "#E9EAEC"
C_EBOX2 = "#C9CDD3"
C_LED = "#22C55E"
C_SHIELD = "#F2F2EF"
C_STRAP = "#3A4048"
C_GROUND = "#CDC4B2"
C_STONE = "#B4AB99"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round rod or tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _band(a, b, w, t):
    """Flat strap of width w and thickness t from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    pl = Plane(origin=a, z_dir=d.normalized())
    return pl.location * (Pos(0, 0, d.length / 2) * Box(w, t, d.length))


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _vert(s):
    return s.edges().filter_by(Axis.Z)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _union(items):
    out = None
    for s in items:
        out = s if out is None else out + s
    return out


def product_parts(P=PARAMS):
    D = derived(P)  # noqa: F841  (kept so the appearance model tracks the same derived set as the calc)
    s_, c_ = math.sin(math.radians(P["tilt"])), math.cos(math.radians(P["tilt"]))
    W = Pos(0, 0, P["z0"]) * Rot(P["tilt"], 0, 0)          # local box frame to world, as model.py
    N = (0.0, -s_, c_)                                      # glazing normal in world

    def along_n(d, extra=(0.0, 0.0, 0.0)):
        return (N[0] * d + extra[0], N[1] * d + extra[1], N[2] * d + extra[2])

    LX, LY, WT = P["box_x"], P["box_y"], P["wall_t"]
    ix, iy = LX - 2 * WT, LY - 2 * WT
    zw0, zw1 = P["wall_z0"], P["wall_z0"] + P["wall_h"]
    gt = P["glaz_t"]
    base = {k: shape for k, _, shape, _ in build_parts(P)}
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ insulated box walls (BOM 2)
    E_WALL = (0, 0, 0)
    wo = _box(0, 0, (zw0 + zw1) / 2, LX, LY, P["wall_h"])
    wo = _fillet_try(wo, _vert(wo), [14.0, 10.0, 6.0])
    wo = _fillet_try(wo, _bottom(wo), [3.0, 2.0])
    wall = wo - _box(0, 0, (zw0 + zw1) / 2, ix, iy, P["wall_h"] + 10)
    # shadow-gap parting line round the outside, where the two plywood skins meet the foam band
    keep = _box(0, 0, 0, LX - 3, LY - 3, 20)
    keep = _fillet_try(keep, _vert(keep), [12.5, 8.5, 4.5])
    gap = _box(0, 0, 0, LX + 20, LY + 20, 3) - keep
    wall -= Pos(0, 0, zw0 + 32) * gap
    add("Insulated box walls (painted plywood)", W * wall, C_WALL, "painted", 2, "shell", E_WALL)

    # nameplate on the south wall, right of the inlet flap
    fy = -LY / 2
    plate = _box(430, fy - 0.3, 95, 190, 0.6, 40)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [4.0, 2.0])
    add("Nameplate", W * plate, C_ACCENT, "painted", 2, "shell", E_WALL)
    ink = (_box(385, fy - 0.8, 101, 80, 0.4, 11) + _box(470, fy - 0.8, 104, 50, 0.4, 4)
           + _box(470, fy - 0.8, 96, 50, 0.4, 3) + _box(430, fy - 0.8, 84, 160, 0.4, 3))
    add("Nameplate print", W * ink, C_LABEL, "paper", 2, "shell", E_WALL)

    # ------------------------------------------------------------ glazing lid (BOM 3)
    E_LID = along_n(1250)
    fw_ = 22.0
    fo = _box(0, 0, zw1 + gt / 2 + 1, LX, LY, gt + 2)
    fo = _fillet_try(fo, _vert(fo), [14.0, 10.0, 6.0])
    fo = _fillet_try(fo, _top(fo), [2.0, 1.0])
    fin = _box(0, 0, zw1 + gt / 2 + 1, LX - 2 * fw_, LY - 2 * fw_, gt + 10)
    fin = _fillet_try(fin, _vert(fin), [4.0, 2.0])
    frame = fo - fin
    add("Lid edge frame (aluminium)", W * frame, C_ALU, "metal", 3, "shell", E_LID)
    # twin-wall pane: two skins and ribs running down the slope
    px_, py_ = LX - 2 * fw_ + 8, LY - 2 * fw_ + 8
    pane = _box(0, 0, zw1 + 0.6, px_, py_, 1.2) + _box(0, 0, zw1 + gt - 0.6, px_, py_, 1.2)
    n_rib = int(px_ // 25)
    x0 = -(n_rib - 1) * 25 / 2
    for i in range(n_rib):
        pane += _box(x0 + i * 25, 0, zw1 + gt / 2, 0.8, py_, gt - 2.0)
    add("Twin-wall polycarbonate glazing", W * pane, C_CLEAR, "clear", 3, "shell", E_LID)
    # hinges on the north edge
    hinges = None
    for x in (-380, 0, 380):
        h = _xcyl(x, LY / 2 + 5, zw1 + 4, 5.0, 70) + _box(x, LY / 2 + 1.0, zw1 - 18, 70, 2.0, 40)
        h += _box(x, LY / 2 - 20, zw1 + gt + 2.6, 70, 40, 1.2)
        hinges = h if hinges is None else hinges + h
    add("Lid hinges", W * hinges, C_STEEL, "metal", 3, "shell", E_LID)
    handle = _pipe([(-80, fy, zw1 + 6), (-80, fy - 26, zw1 + 6), (80, fy - 26, zw1 + 6), (80, fy, zw1 + 6)], 5.0)
    add("Lid pull handle", W * handle, C_ALU_DARK, "metal", 3, "shell", E_LID)

    # ------------------------------------------------------------ sorbent trays (BOM 4) and bed (BOM 5)
    rim, tz0, th = P["tray_rim"], P["tray_z0"], P["tray_h"]
    tx, ty = P["tray_x"], P["tray_y"]
    pans, bails = [], []
    for (x, y) in tray_centres(P):
        po = _box(x, y, tz0 + th / 2, tx, ty, th)
        po = _fillet_try(po, _vert(po), [6.0, 4.0])
        pi = _box(x, y, tz0 + th / 2 + 1.0, tx - 2 * rim, ty - 2 * rim, th)
        pi = _fillet_try(pi, _vert(pi), [2.0, 1.0])
        pans.append(po - pi)
        for sy in (-1, 1):
            yy = y + sy * (ty / 2 - rim / 2)
            bails.append(_pipe([(x - 60, yy, tz0 + th), (x - 60, yy, tz0 + th + 7),
                                (x + 60, yy, tz0 + th + 7), (x + 60, yy, tz0 + th)], 2.0))
    add("Sorbent trays (black tops)", W * _union(pans), C_BLACK, "painted", 4, "internal", along_n(520))
    add("Tray lift bails", W * _union(bails), C_STEEL, "metal", 4, "internal", along_n(520))
    add("Composite sorbent beds", base["bed"], C_BED, "clay", 5, "internal", along_n(760))
    rail_z = tz0 - 5
    baffle = _box(0, 0, tz0 - P["baffle_t"] / 2, ix, iy, P["baffle_t"])
    for (x, y) in tray_centres(P):
        baffle -= _box(x, y, tz0, tx - 2 * rim, ty - 2 * rim, 10)
    baffle += _box(-(ix / 2 - 8), 0, rail_z, 16, iy, 10) + _box(ix / 2 - 8, 0, rail_z, 16, iy, 10)
    add("Sealing baffle and tray rails", W * baffle, C_ALU, "metal", 4, "internal", along_n(330))

    # drip screens (BOM 15), condenser (BOM 6), as model.py
    add("Drip screens and brine sumps", base["screens"], C_BLACK, "painted", 15, "internal", along_n(180))
    add("Finned condenser plate", base["condenser"], C_ALU, "metal", 6, "internal", along_n(-330))

    # ------------------------------------------------------------ gutter, drain, bottle (BOM 7, 8)
    E_WATER = (0, -380, -60)
    pt = P["plate_top"]
    gy = -LY / 2 + WT + P["gutter_w"] / 2
    gutter = _box(0, gy, pt + 8, ix, P["gutter_w"], 16) - _box(0, gy, pt + 11, ix - 6, P["gutter_w"] - 6, 16)
    add("Condensate gutter", W * gutter, C_ALU, "metal", 7, "internal", E_WATER)
    bx, by = P["bottle_xy"]
    bw, bd, bh = P["bottle"]
    g_in = world(bx, -LY / 2 + WT, pt + 8, P)
    g_out = world(bx, -LY / 2 - 20, pt + 8, P)
    drain = _pipe([g_in, g_out, (bx, by + 40, bh + 60)], 8.0)
    add("Silicone drain tube", drain, C_TUBE, "plastic", 7, "shell", E_WATER)
    gro =Plane(origin=Vector(*g_out), z_dir=(Vector(*g_out) - Vector(*g_in)).normalized()).location * \
        (Pos(0, 0, -2) * Cylinder(12.0, 6.0))
    add("Drain grommet", gro, C_RUBBER, "rubber", 14, "shell", E_WATER)

    jb = _box(bx, by, bh / 2, bw, bd, bh)
    jb = _fillet_try(jb, _vert(jb), [22.0, 16.0, 10.0])
    jb = _fillet_try(jb, _top(jb), [14.0, 10.0, 6.0])
    jb = _fillet_try(jb, _bottom(jb), [6.0, 4.0])
    for k in range(4):                                    # moulded side ribs (texture)
        z = 70 + k * 45
        for sx in (-1, 1):
            jb -= _box(bx + sx * bw / 2, by - 20, z, 3.0, bd - 90, 6)
    # moulded carry handle at the back of the top
    hy_ = by - 70
    jb += _box(bx, hy_ - 45, bh + 18, 26, 14, 36) + _box(bx, hy_ + 45, bh + 18, 26, 14, 36)
    grip = _box(bx, hy_, bh + 40, 26, 104, 16)
    grip = _fillet_try(grip, grip.edges().filter_by(Axis.Y), [6.0, 4.0])
    jb += grip
    jb += _zcyl(bx, by + 40, bh + 6, 22.0, 14.0)          # neck
    add("Collection jerrycan, 10 L", jb, C_BOTTLE, "plastic", 8, "shell", E_WATER)
    cap = _zcyl(bx, by + 40, bh + 20, 28.0, 40.0)
    cap = _fillet_try(cap, _top(cap), [4.0, 2.0])
    for k in range(18):                                   # knurled grip ribs
        a = 2 * math.pi * k / 18
        cap -= _zcyl(bx + 28.5 * math.cos(a), by + 40 + 28.5 * math.sin(a), bh + 16, 2.0, 30.0)
    add("Jerrycan cap", cap, C_ACCENT, "plastic", 8, "shell", E_WATER)
    lab = _box(bx, by - bd / 2 - 0.3, 150, 120, 0.6, 110)
    lab = _fillet_try(lab, lab.edges().filter_by(Axis.Y), [6.0, 3.0])
    add("Jerrycan label", lab, C_LABEL, "paper", 8, "shell", E_WATER)
    lprint = _box(bx, by - bd / 2 - 0.7, 185, 90, 0.4, 14) + _box(bx, by - bd / 2 - 0.7, 160, 90, 0.4, 4) \
        + _box(bx, by - bd / 2 - 0.7, 150, 90, 0.4, 4) + _box(bx, by - bd / 2 - 0.7, 115, 60, 0.4, 10)
    add("Jerrycan label print", lprint, C_ACCENT, "paper", 8, "shell", E_WATER)

    # ------------------------------------------------------------ south inlet flap (BOM 9)
    E_FLAP = (0, -300, 40)
    fwid, fht = P["flap_in"]
    fz = P["flap_in_z"]
    fl = _box(-100, fy - 5, fz, fwid, 10, fht)
    fl = _fillet_try(fl, fl.edges().filter_by(Axis.Y), [4.0, 2.0])
    fl = _fillet_try(fl, fl.faces().sort_by(Axis.Y)[0].edges(), [1.5, 1.0])
    add("South inlet flap", W * fl, C_ALU, "metal", 9, "shell", E_FLAP)
    seal = _box(-100, fy - 0.5, fz, fwid + 12, 1.0, fht + 12) - _box(-100, fy - 0.5, fz, fwid, 3, fht)
    add("Inlet flap seal", W * seal, C_RUBBER, "rubber", 9, "shell", E_FLAP)
    knuckles = None
    for k in range(5):
        kx = -100 - fwid / 2 + 40 + k * (fwid - 80) / 4
        kn = _xcyl(kx, fy - 6, fz + fht / 2 + 1, 4.0, 60)
        knuckles = kn if knuckles is None else knuckles + kn
    knuckles += _xcyl(-100, fy - 6, fz + fht / 2 + 1, 1.5, fwid - 20)
    add("Inlet flap hinge", W * knuckles, C_STEEL, "metal", 9, "shell", E_FLAP)
    latches = None
    for x in (-100 - 280, -100 + 280):
        body = _box(x, fy - 7, fz - fht / 2 - 16, 30, 14, 24)
        body = _fillet_try(body, body.edges().filter_by(Axis.Y), [3.0, 2.0])
        lever = _box(x, fy - 16, fz - fht / 2 - 6, 18, 5, 30)
        lever = _fillet_try(lever, lever.edges().filter_by(Axis.Y), [2.0, 1.0])
        hook = _box(x, fy - 12, fz - fht / 2 + 6, 12, 4, 10)
        la = body + lever + hook
        latches = la if latches is None else latches + la
    add("Over-centre latches", W * latches, C_STEEL, "metal", 9, "shell", E_FLAP)

    # ------------------------------------------------------------ fan hood and outlet flap (BOM 10)
    E_FAN = (0, 320, 60)
    hx, hy, hz = P["fan_hood"]
    ny = LY / 2
    hood = _box(330, ny + hy / 2, zw0 + hz / 2, hx, hy, hz)
    hood = _fillet_try(hood, hood.edges().filter_by(Axis.Y), [10.0, 6.0, 4.0])
    hood = _fillet_try(hood, hood.faces().sort_by(Axis.Y)[-1].edges(), [4.0, 2.0])
    hood -= _box(330, ny + hy / 2 - 3, zw0 + hz / 2 - 4, hx - 8, hy - 2, hz)   # open underneath
    for k in range(6):                                                        # louvre grooves
        hood -= _box(330, ny + hy, zw0 + 36 + k * 16, hx - 40, 4.0, 5.0)
    add("Fan hood (12 V fan inside)", W * hood, C_HOOD, "plastic", 10, "shell", E_FAN)
    guard = _ycyl(330, ny + 3, zw0 + hz / 2, 58.0, 4.0) - _ycyl(330, ny + 3, zw0 + hz / 2, 54.0, 6.0)
    for a in (0, 60, 120):
        guard += Pos(330, ny + 3, zw0 + hz / 2) * Rot(0, a, 0) * Box(2.0, 4.0, 112)
    add("Fan guard", W * guard, C_RUBBER, "metal", 10, "internal", E_FAN)
    ow, oh = P["flap_out"]
    of = _box(-230, ny + 5, zw0 + oh / 2, ow, 10, oh)
    of = _fillet_try(of, of.edges().filter_by(Axis.Y), [4.0, 2.0])
    of += _xcyl(-230, ny + 11, zw0 + oh + 1, 4.0, ow - 20)
    add("North outlet flap", W * of, C_ALU, "metal", 10, "shell", E_FAN)

    # ------------------------------------------------------------ stand (BOM 1)
    E_STAND = (0, 0, -420)
    add("Stand, galvanized steel angle", base["stand"], C_GALV, "metal", 1, "shell", E_STAND)
    pts = {(xs, ys): world(xs * (LX / 2 - 20), ys * (LY / 2 - 60), zw0 - 3, P) for xs in (-1, 1) for ys in (-1, 1)}
    bolts = []
    for (x, y, _z) in pts.values():
        for dx in (-42, 42):
            for dy in (-42, 42):
                b = _hex_z(x + dx, y + dy, 8.0, 13.0, 4.0) + _zcyl(x + dx, y + dy, 11.0, 3.0, 4.0)
                bolts.append(b)
    add("Foot pad bolts", _union(bolts), C_STEEL, "metal", 14, "shell", E_STAND)

    # two auger ground anchors outboard of the south legs, tied to the legs with webbing straps
    anchors, straps, buckles = [], [], []
    for xs in (-1, 1):
        lx, ly, _ = pts[(xs, -1)]
        ax_, ay_ = lx + xs * 190, ly
        eye = Pos(ax_, ay_, 34) * Rot(90, 0, 0) * (Cylinder(22, 7) - Cylinder(15, 9))
        anchors.append(eye + _zcyl(ax_, ay_, 7, 5.0, 16) + _zcyl(ax_, ay_, 1.5, 16.0, 3.0))
        a = (ax_ - xs * 18, ay_, 38)
        b = (lx + xs * 2, ly + 15, 230)
        straps.append(_band(a, b, 25.0, 2.0))
        m = [(a[i] + b[i]) / 2 for i in range(3)]
        dvec = Vector(b[0] - a[0], b[1] - a[1], b[2] - a[2]).normalized()
        buckles.append(Plane(origin=Vector(*m), z_dir=dvec).location * Box(32, 8, 40))
    add("Auger ground anchors", _union(anchors), C_GALV, "metal", 1, "shell", E_STAND)
    add("Anchor tie straps", _union(straps), C_STRAP, "fabric", 1, "shell", E_STAND)
    add("Strap ratchets", _union(buckles), C_STEEL, "metal", 1, "shell", E_STAND)

    # ------------------------------------------------------------ PV panel on its pole (BOM 11)
    E_PV = (320, 320, 220)
    px, py, pz = pts[(1, 1)]
    pvx, pvy, pvz = P["pv_size"]
    PVL = Pos(px - 200, py + 40, P["pv_z"]) * Rot(P["tilt"] + 10, 0, 0)
    pfr = Box(pvx, pvy, pvz)
    pfr = _fillet_try(pfr, _vert(pfr), [3.0, 1.5])
    pfr -= Pos(0, 0, 4) * Box(pvx - 16, pvy - 16, pvz)
    add("PV panel frame", PVL * pfr, C_ALU, "metal", 11, "shell", E_PV)
    cells = Pos(0, 0, pvz / 2 - 3.5) * Box(pvx - 16, pvy - 16, 3.0)
    add("PV cells and glass", PVL * cells, C_CELL, "screen", 11, "shell", E_PV)
    grid = None
    for i in range(1, 6):
        g = Pos(-(pvx - 16) / 2 + i * (pvx - 16) / 6, 0, pvz / 2 - 1.9) * Box(1.2, pvy - 16, 0.3)
        grid = g if grid is None else grid + g
    for j in range(1, 4):
        grid += Pos(0, -(pvy - 16) / 2 + j * (pvy - 16) / 4, pvz / 2 - 1.9) * Box(pvx - 16, 1.2, 0.3)
    add("PV cell busbars", PVL * grid, "#AEB6C2", "metal", 11, "shell", E_PV)
    jbox = Pos(0, 30, -pvz / 2 - 8) * Box(60, 50, 16)
    add("PV junction box", PVL * jbox, C_RUBBER, "plastic", 11, "shell", E_PV)
    pole = _pipe([(px, py + 30, pz), (px, py + 30, P["pv_z"] - 20)], 15.0)
    pole += _pipe([(px, py + 30, P["pv_z"] - 30), (px - 200, py + 40, P["pv_z"] - 30)], 10.0)
    pole += _zcyl(px, py + 30, P["pv_z"] - 18, 16.0, 4.0)
    add("PV pole and arm", pole, C_GALV, "metal", 11, "shell", E_PV)
    clamps = _zcyl(px, py + 30, pz + 40, 19.0, 18.0) + _zcyl(px, py + 30, pz + 110, 19.0, 18.0)
    clamps -= _zcyl(px, py + 30, pz + 75, 15.5, 120.0)
    add("Pole clamps", clamps, C_STEEL, "metal", 14, "shell", E_PV)

    # ------------------------------------------------------------ electronics box (BOM 12) and sensors (BOM 13)
    E_EL = (-480, -260, -120)
    ex, ey, _ = pts[(-1, 1)]
    ebx, eby, ebz = P["ebox"]
    ecx, ecz = ex - 110, 310 + ebz / 2
    eb = _box(ecx, ey - 6, ecz, ebx, eby - 12, ebz)
    eb = _fillet_try(eb, eb.edges().filter_by(Axis.Y), [8.0, 5.0, 3.0])
    eb = _fillet_try(eb, eb.faces().sort_by(Axis.Y)[0].edges(), [2.0, 1.0])
    add("Electronics box (IP65)", eb, C_EBOX, "plastic", 12, "shell", E_EL)
    lid = _box(ecx, ey + eby / 2 - 6, ecz, ebx, 12, ebz)
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Y), [8.0, 5.0, 3.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Y)[-1].edges(), [2.5, 1.5])
    add("Electronics box lid", lid, C_EBOX2, "plastic", 12, "shell", E_EL)
    fy2 = ey + eby / 2      # lid faces north, outward from the stand
    lscr = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            s = _ycyl(ecx + sx * (ebx / 2 - 10), fy2 + 0.6, ecz + sz * (ebz / 2 - 10), 3.4, 1.2)
            lscr.append(s - _box(ecx + sx * (ebx / 2 - 10), fy2 + 1.2, ecz + sz * (ebz / 2 - 10), 4.0, 1.0, 0.8))
    add("Lid screws", _union(lscr), C_STEEL, "metal", 14, "shell", E_EL)
    ntag = _box(ecx, fy2 + 0.3, ecz + 70, 100, 0.6, 22)
    add("Electronics box label", ntag, C_ACCENT, "painted", 12, "shell", E_EL)
    tprint = _box(ecx - 12, fy2 + 0.7, ecz + 72, 60, 0.4, 7) + _box(ecx + 30, fy2 + 0.7, ecz + 66, 24, 0.4, 3)
    add("Electronics box label print", tprint, C_LABEL, "paper", 12, "shell", E_EL)
    ring = _ycyl(ecx, fy2 + 2, ecz + 20, 7.0, 4.0) - _ycyl(ecx, fy2 + 2, ecz + 20, 4.5, 6.0)
    add("Status light bezel", ring, C_RUBBER, "plastic", 12, "shell", E_EL)
    led = _ycyl(ecx, fy2 + 2.5, ecz + 20, 4.4, 3.0) + Pos(ecx, fy2 + 4.0, ecz + 20) * Sphere(3.6)
    led &= _box(ecx, fy2 + 3, ecz + 20, 10, 6, 10)
    add("Status light, green (lit)", led, C_LED, "emissive", 12, "shell", E_EL)
    gl = []
    for gx in (ecx - 40, ecx + 40):
        g = _hex_z(gx, ey, 310 - 2.5, 20.0, 5.0) + _zcyl(gx, ey, 310 - 9, 8.0, 8.0)
        gl.append(_fillet_try(g, _bottom(g), [2.0, 1.0]))
    add("Cable glands", _union(gl), C_RUBBER, "plastic", 14, "shell", E_EL)
    brk = _box(ex - 16, ey + 6, ecz, 32, 50, 150)
    add("Electronics box bracket", brk, C_GALV, "metal", 12, "shell", E_EL)
    # cable from the gland, up the leg to the rail (then to the fan and the PV panel)
    cable = _pipe([(ecx + 40, ey, 297), (ecx + 40, ey, 262), (ex + 14, ey + 14, 262),
                   (ex + 14, ey + 14, pts[(-1, 1)][2] - 40)], 4.0)
    add("Fan and PV cable (sheathed)", cable, C_RUBBER, "rubber", 12, "shell", E_EL)

    # radiation shield: stacked dishes on a post, arm to the leg
    shx, shz = ex - 110, 700
    dishes = []
    for k in range(7):
        z = shz - 50 + k * 15
        d = _zcyl(shx, ey, z, 45.0 if k < 6 else 48.0, 3.0)
        dishes.append(_fillet_try(d, d.edges(), [1.2, 0.6]))
    dishes.append(Pos(shx, ey, shz + 44) * Sphere(46.0) & _box(shx, ey, shz + 64, 100, 100, 40))
    add("Radiation shield plates", _union(dishes), C_SHIELD, "plastic", 13, "shell", E_EL)
    post = _zcyl(shx, ey, shz - 5, 6.0, 110) + _pipe([(shx, ey, 645), (ex - 20, ey, 645), (ex + 5, ey, 645)], 6.0)
    add("Shield post and arm", post, C_GALV, "metal", 13, "shell", E_EL)

    # ------------------------------------------------------------ context (not in the BOM)
    gx0, gx1, gy0, gy1 = -900.0, 840.0, -1040.0, 660.0
    ground = _box((gx0 + gx1) / 2, (gy0 + gy1) / 2, -30, gx1 - gx0, gy1 - gy0, 60)
    ground = _fillet_try(ground, _vert(ground), [160.0, 100.0])
    ground = _fillet_try(ground, _top(ground), [18.0, 10.0, 5.0])
    add("Ground patch (compacted gravel)", ground, C_GROUND, "clay", None, "context", (0, 0, 0))
    rnd = random.Random(7)
    stones = []
    avoid = [(x, y) for (x, y, _z) in pts.values()] + [(bx, by)]
    while len(stones) < 26:
        x = rnd.uniform(gx0 + 120, gx1 - 120)
        y = rnd.uniform(gy0 + 120, gy1 - 120)
        if any(abs(x - a) < 190 and abs(y - b) < 210 for a, b in avoid):
            continue
        r = rnd.uniform(9, 22)
        st = Pos(x, y, 0) * Rot(0, 0, rnd.uniform(0, 180)) * (Sphere(r) & Box(4 * r, 4 * r, 0.9 * r))
        stones.append(st)
    add("Gravel stones", _union(stones), C_STONE, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
