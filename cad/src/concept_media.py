"""DewDrive concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X runs east to west across the collector, Y runs south to north, Z is up.
The glazed box is built flat in a local frame (glazing on top, condenser floor below) and then
tilted 20 degrees so the glazing faces south (toward -Y) and the high edge is to the north.
Every part carries its BOM line number from bom/bom.csv.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure, _render

TILT = 20.0                      # collector tilt, degrees (proposed; about site latitude)
L_X, L_Y = 1100.0, 1000.0        # outer size of the box, mm
WALL = 40.0                      # insulated wall thickness
Z0 = 680.0                       # height of the local origin above the ground

W = Pos(0, 0, Z0) * Rot(TILT, 0, 0)            # local box frame to world
s, c = math.sin(math.radians(TILT)), math.cos(math.radians(TILT))
N = (0.0, -s, c)                                  # glazing normal in world


def world(x, y, z):
    """Local box point to world coordinates."""
    return (x, y * c - z * s, Z0 + y * s + z * c)


def along_n(d, extra=(0.0, 0.0, 0.0)):
    """Explode offset d mm along the glazing normal, plus an extra world offset."""
    return (N[0] * d + extra[0], N[1] * d + extra[1], N[2] * d + extra[2])


def bar(a, b, w):
    """Square-ish bar (drawn as a round tube for massing) between two world points."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(w / 2, d.length, Plane(origin=a, z_dir=d.normalized()))


# ---------------- local layers (z in the box frame) ----------------
# Floor: condenser plate top at z = 45; fins below to z = -60.
# Sorbent trays: z = 110 to 135. Glazing: z = 180 to 192.

# 2 Insulated box walls (plywood skins with foam core), open top and bottom
walls = Pos(0, 0, 110) * (Box(L_X, L_Y, 140) - Box(L_X - 2 * WALL, L_Y - 2 * WALL, 150))

# 3 Glazing lid: twin-wall polycarbonate in a light frame, hinged on the north edge
glazing = Pos(0, 0, 186) * Box(L_X, L_Y, 12)

# 4 Sorbent trays: four black aluminium mesh-bottom pans, 2 x 2
# 5 Composite sorbent bed inside the trays
TX, TY = 490.0, 430.0
trays = None
bed = None
for x in (-252.0, 252.0):
    for y in (-222.0, 222.0):
        pan = Pos(x, y, 122.5) * (Box(TX, TY, 25) - Pos(0, 0, 4) * Box(TX - 16, TY - 16, 25))
        cake = Pos(x, y, 118) * Box(TX - 18, TY - 18, 12)
        trays = pan if trays is None else trays + pan
        bed = cake if bed is None else bed + cake
# tray rails along the east and west walls
trays = trays + Pos(-492, 0, 105) * Box(16, L_Y - 2 * WALL, 10) + Pos(492, 0, 105) * Box(16, L_Y - 2 * WALL, 10)

# 6 Condenser: aluminium floor plate with fins below, running down the slope, shaded by the box
condenser = Pos(0, 0, 42.5) * Box(L_X - 20, L_Y - 20, 5)
for i in range(21):
    x = -500.0 + 50.0 * i
    condenser = condenser + Pos(x, 0, -10) * Box(3, L_Y - 80, 100)

# 7 Condensate gutter along the low (south) edge inside the box, and drain tube to the bottle
gutter = Pos(0, -L_Y / 2 + WALL + 15, 52) * (Box(L_X - 2 * WALL, 30, 16) - Pos(0, 0, 4) * Box(L_X - 2 * WALL - 8, 22, 16))
g_out = world(360, -L_Y / 2 - 20, 52)
BOTTLE = (360.0, -760.0)
drain = (bar(world(360, -L_Y / 2 + WALL, 52), g_out, 16)
         + bar(g_out, (BOTTLE[0], BOTTLE[1] + 40, 380), 16))

# 9 Vent flaps: south inlet flap at the vapour-gap level (closed by day); the north outlet flap is part of item 10
flaps = Pos(-100, -L_Y / 2 - 5, 80) * Box(800, 10, 70)
outlet_flap = Pos(-230, L_Y / 2 + 5, 80) * Box(560, 10, 70)

# 10 Night fan: 120 mm, 12 V, in a hooded housing on the north wall
fan = Pos(330, L_Y / 2 + 32, 100) * Box(160, 64, 140) + outlet_flap

# ---------------- world-frame parts ----------------
# 1 Stand: galvanized steel angle, four legs, side rails under the box, cross braces
pts = {}
for xs in (-1, 1):
    for ys in (-1, 1):
        pts[(xs, ys)] = world(xs * (L_X / 2 - 20), ys * (L_Y / 2 - 60), -60)
stand = None
for (xs, ys), (x, y, z) in pts.items():
    leg = bar((x, y, 0), (x, y, z), 40)
    foot = Pos(x, y, 3) * Box(120, 120, 6)
    stand = leg + foot if stand is None else stand + leg + foot
for xs in (-1, 1):
    stand = stand + bar(pts[(xs, -1)], pts[(xs, 1)], 40)                 # side rail under the box
    a, b = pts[(xs, -1)], pts[(xs, 1)]
    stand = stand + bar((a[0], a[1], 120), (b[0], b[1], b[2] * 0.55), 25)  # diagonal brace
for ys in (-1, 1):
    a, b = pts[(-1, ys)], pts[(1, ys)]
    stand = stand + bar((a[0], a[1], 200), (b[0], b[1], 200), 25)         # low cross brace

# 8 Collection bottle: 10 L food-grade HDPE jerrycan on the ground below the low edge
bottle = Pos(BOTTLE[0], BOTTLE[1], 160) * Box(180, 260, 320) \
    + Pos(BOTTLE[0], BOTTLE[1] + 40, 340) * Cylinder(28, 40)

# 11 Small PV panel, 10 W, on a pole above the north-east leg (north of the box, so it casts no shade on it)
px, py, pz = pts[(1, 1)]
PV_Z = 1330.0
pv = Pos(px - 200, py + 40, PV_Z) * Rot(TILT + 10, 0, 0) * Box(340, 250, 25)
pv = pv + bar((px, py + 30, pz), (px, py + 30, PV_Z - 20), 30) \
    + bar((px, py + 30, PV_Z - 30), (px - 200, py + 40, PV_Z - 30), 20)

# 12 Electronics box: charge controller, 12 V LiFePO4 battery, logger, on the north-west leg
ex, ey, ez = pts[(-1, 1)]
ebox = Pos(ex - 110, ey, 420) * Box(160, 110, 220)

# 13 Sensors: ambient T and RH shield on the north-west leg, bed and condenser probes inside
# (the bed and condenser probes are listed in the BOM but too small to model)
shield = Pos(ex - 110, ey, 700) * Cylinder(45, 110) + bar((ex - 110, ey, 645), (ex - 20, ey, 645), 12)

parts = [
    Part("Stand, galvanized steel angle", stand, "#6B7280", 1, (0, 0, -450)),
    Part("Insulated box walls", W * walls, "#C8A165", 2, along_n(120)),
    Part("Glazing lid, twin-wall polycarbonate", W * glazing, "#9CC9D6", 3, along_n(1850, (1300, 0, 0))),
    Part("Sorbent trays (4), black aluminium mesh", W * trays, "#1F2937", 4, along_n(350, (1350, 0, 0))),
    Part("Composite sorbent, silica gel and CaCl2", W * bed, "#E8E2C8", 5, along_n(1100, (500, 0, 0))),
    Part("Condenser plate with fins", W * condenser, "#9CA3AF", 6, along_n(-260)),
    Part("Condensate gutter and drain tube", W * gutter + drain, "#0F766E", 7, (0, -420, -120)),
    Part("Collection bottle, 10 L", bottle, "#E5E7EB", 8, (250, -520, -80)),
    Part("Vent flap, south inlet", W * flaps, "#B45309", 9, (-150, -700, 150)),
    Part("Night fan and outlet flap, 12 V", W * fan, "#2563EB", 10, (1300, 900, -700)),
    Part("PV panel, 10 W, on pole", pv, "#1E3A8A", 11, (1400, 900, -900)),
    Part("Electronics box (charger, LiFePO4, logger)", ebox, "#15803D", 12, (2300, -700, -150)),
    Part("Air temperature and RH sensor shield", shield, "#F3F4F6", 13, (2300, -700, 0)),
]

# Scale reference: a 1.75 m person standing clear of the stand (placed by hand so that it does not
# overlap the collector in the hero or the blueprint isometric view)
person = human_figure(1750.0, x=2100.0, y=-300.0, z=0.0)
person.name = "1.75 m person"


def _projector(shown, elev, azim, W=1280, H=960, pad=0.06):
    """Same orthographic projection as concept._zbuffer, so callouts land on the rendered pixels."""
    import numpy as np
    e, a = np.radians(elev), np.radians(azim)
    d = -np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    right = np.cross(d, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, d)
    P = np.stack([right, up])
    pts = []
    for p in shown:
        verts, _ = p.shape.tessellate(1.0)
        pts.append(np.array([[v.X, v.Y, v.Z] for v in verts]))
    q = np.vstack(pts) @ P.T
    lo, hi = q.min(0), q.max(0)
    span = (hi - lo).max() * (1 + 2 * pad)
    ctr = (lo + hi) / 2
    k = min(W, H) / span
    return lambda pt: ((np.array(pt) @ P.T)[0] - ctr[0]) * k + W / 2, \
        lambda pt: H / 2 - ((np.array(pt) @ P.T)[1] - ctr[1]) * k


def cutaway(out="media/cutaway.png"):
    """Section on a north-south plane at x = 360 mm (through the drain), looking west, with BOM callouts."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    big = 6000.0
    X = 360.0
    cutter = Pos(X - big / 2, 0, 0) * Box(big, big, big)
    keep = []
    for p in parts:
        if p.bom in (11, 12, 13):          # PV, electronics and sensor sit outside the section
            continue
        if p.bom == 8:                     # bottle kept whole
            keep.append(Part(p.name, p.shape, p.color, p.bom))
            continue
        s = p.shape & cutter
        if s.volume > 1e-6:
            keep.append(Part(p.name, s, p.color, p.bom))
    elev, azim = 4, 0
    _render(keep, out, elev=elev, azim=azim)   # plain render; title and callouts are added below
    px, py = _projector(keep, elev, azim)
    img = plt.imread(out)
    fig = plt.figure(figsize=(8, 6), dpi=160)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(img); ax.set_axis_off()
    ax.set_xlim(0, 1280); ax.set_ylim(960, 0)
    lx = pts[(-1, -1)]
    callouts = [  # (bom, point in world, label offset in px)
        (3, world(X, 250, 192), (60, -90)),
        (5, world(X, 100, 124), (-90, -170)),
        (4, world(X, -300, 111), (-40, 130)),
        (2, world(X, L_Y / 2 - 20, 150), (70, -40)),
        (10, world(X, L_Y / 2 + 50, 100), (70, 20)),
        (6, world(X, 150, 0), (60, 110)),
        (9, world(X, -L_Y / 2 - 8, 80), (-70, -40)),
        (7, world(X, -L_Y / 2 + WALL + 15, 55), (-90, 30)),
        (8, (BOTTLE[0], BOTTLE[1], 250), (-80, 0)),
        (1, (lx[0], lx[1], 300), (70, 60)),
    ]
    names = {p.bom: p for p in parts}
    for b, pt, (dx, dy) in callouts:
        x, y = px(pt), py(pt)
        ax.plot([x, x + dx], [y, y + dy], color="#111827", lw=0.8)
        ax.plot([x], [y], "o", color="#111827", ms=2.5)
        ax.text(x + dx, y + dy, str(b), fontsize=8, fontweight="bold", color="white", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.3", fc="#0F766E", ec="white", lw=0.8))
    # night air path (blue) and daytime vapour path (red), drawn in the section plane
    def arrow(p0, p1, col):
        ax.add_patch(FancyArrowPatch((px(p0), py(p0)), (px(p1), py(p1)), arrowstyle="-|>", mutation_scale=12,
                                     lw=1.6, color=col, alpha=0.85))
    arrow(world(X, -L_Y / 2 - 150, 80), world(X, -150, 80), "#2563EB")
    arrow(world(X, 150, 80), world(X, L_Y / 2 + 150, 100), "#2563EB")
    arrow(world(X, -350, 155), world(X, 350, 155), "#2563EB")
    for yy in (-300, 0, 300):
        arrow(world(X, yy + 40, 112), world(X, yy + 40, 52), "#C2410C")
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=names[b].color, mec="#111827", ms=7,
                          label=f"{b}  {names[b].name}") for b in sorted(b for b, _, _ in callouts)]
    handles += [plt.Line2D([], [], color="#2563EB", lw=1.6, label="Night: air drawn through the box"),
                plt.Line2D([], [], color="#C2410C", lw=1.6, label="Day: vapour from bed to condenser")]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=7.5, bbox_to_anchor=(0.0, 0.9))
    fig.text(0.02, 0.97, "DewDrive: cutaway (north-south section through the drain, looking west)", fontsize=9,
             fontweight="bold", color="#111827", va="top")
    fig.text(0.02, 0.93, "CONCEPT, NOT FOR FABRICATION", fontsize=6.5, color="#B45309", va="top")
    fig.text(0.02, 0.03, "South (low edge) at left. Flaps open at night; closed by day while the sun heats the bed.",
             fontsize=7.5, color="#4B5563", va="bottom")
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    render_all(
        parts, project="DewDrive", title="Solar desiccant water harvester concept", dwg_no="DWD-DWG-010",
        key_figures=["1.0 m2 glazed aperture, tilted 20 deg to the sun",
                     "4 kg composite sorbent (silica gel with about 33 % CaCl2)",
                     "About 0.5 L/day at 40 % night RH (estimate)",
                     "Regeneration 75 to 90 C by sun only; fan about 20 Wh/night",
                     "Collector 1.1 x 1.0 m, top edge about 1.1 m high",
                     "About 45 kg dry; box alone about 30 kg (estimate)",
                     "Parts about $475, over the $400 budget (indicative)"],
        cut=False, scale_figure=False, context=[person],
        flow={"title": "water per day at the design point, g (all values are estimates; 40 % night RH, 20 C)",
              "unit": "g",
              "stages": [("Vapour in night air", 2770), ("Adsorbed overnight", 1200),
                         ("Released by day", 600), ("Condensed", 510), ("In the bottle", 485)],
              "losses": [(0, "Passes the bed", 1570), (1, "Left in the bed", 600),
                         (2, "Re-adsorbed or vented", 90), (3, "Films and drips", 25)]},
    )
    cutaway()
    import shutil
    for d in Path("media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
