"""DewDrive concept media (TRL 3, DWD-DDR-002 revision), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Massing-plus model: main dimensions and interfaces; not for fabrication.

Coordinates in mm. X runs east to west across the collector, Y runs south to north, Z is up.
Every part carries its BOM line number from bom/bom.csv. Numbers on the media come from
docs/04-calcs/sizing.py (DWD-CAL-001) and are estimates.
"""
import contextlib
import io
import math
import sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[2] / ".kit"), str(HERE.parent), str(HERE.parents[2] / "docs" / "04-calcs")]
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all, human_figure, _render  # noqa: E402
from model import PARAMS, build_parts, world, derived  # noqa: E402

TILT = PARAMS["tilt"]
L_X, L_Y, WALL = PARAMS["box_x"], PARAMS["box_y"], PARAMS["wall_t"]
BOTTLE = PARAMS["bottle_xy"]
s, c = math.sin(math.radians(TILT)), math.cos(math.radians(TILT))
N = (0.0, -s, c)                                  # glazing normal in world


def along_n(d, extra=(0.0, 0.0, 0.0)):
    """Explode offset d mm along the glazing normal, plus an extra world offset."""
    return (N[0] * d + extra[0], N[1] * d + extra[1], N[2] * d + extra[2])


COLORS = {"stand": "#6B7280", "walls": "#C8A165", "glazing": "#9CC9D6", "trays": "#1F2937", "bed": "#E8E2C8",
          "condenser": "#9CA3AF", "gutter": "#0F766E", "bottle": "#E5E7EB", "flap": "#B45309", "fan": "#2563EB",
          "pv": "#1E3A8A", "ebox": "#15803D", "shield": "#F3F4F6", "screens": "#4B5563"}
EXPLODE = {"stand": (0, 0, -450), "walls": along_n(120), "glazing": along_n(1850, (1300, 0, 0)),
           "trays": along_n(350, (1350, 0, 0)), "bed": along_n(1100, (500, 0, 0)), "condenser": along_n(-260),
           "screens": along_n(700, (2300, 700, 900)),
           "gutter": (0, -420, -120), "bottle": (250, -520, -80), "flap": (-150, -700, 150),
           "fan": (1300, 900, -700), "pv": (1400, 900, -900), "ebox": (2300, -700, -150), "shield": (2300, -700, 0)}
parts = [Part(name, shape, COLORS[k], bom, EXPLODE[k]) for k, name, shape, bom in build_parts()]
_stand_pts = {(xs, ys): world(xs * (L_X / 2 - 20), ys * (L_Y / 2 - 60), PARAMS["wall_z0"] - 3)
              for xs in (-1, 1) for ys in (-1, 1)}
pts = _stand_pts

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as C  # noqa: E402

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
        (3, world(X, 250, 190), (60, -90)),
        (5, world(X, 100, 116), (-90, -170)),
        (4, world(X, -300, 111), (-40, 130)),
        (15, world(X, 200, 86), (-70, 170)),
        (2, world(X, L_Y / 2 - 20, 150), (70, -40)),
        (10, world(X, L_Y / 2 + 50, 100), (70, 20)),
        (6, world(X, 150, 0), (60, 110)),
        (9, world(X, -L_Y / 2 - 8, PARAMS["flap_in_z"]), (-10, -75)),
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
    # night: in above the trays at the south, down through the beds, out below them at the north fan
    arrow(world(X, -L_Y / 2 - 70, PARAMS["flap_in_z"]), world(X, -330, 160), "#2563EB")
    for yy in (-250, 50):
        arrow(world(X, yy, 168), world(X, yy, 72), "#2563EB")
    arrow(world(X, 250, 62), world(X, L_Y / 2 + 150, 75), "#2563EB")
    for yy in (-150, 150, 380):
        arrow(world(X, yy, 108), world(X, yy, 52), "#C2410C")
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=names[b].color, mec="#111827", ms=7,
                          label=f"{b}  {names[b].name}") for b in sorted(b for b, _, _ in callouts)]
    handles += [plt.Line2D([], [], color="#2563EB", lw=1.6, label="Night: air drawn down through the beds"),
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
    A = C.cD40
    render_all(
        parts, project="DewDrive", title="Solar desiccant water harvester concept", dwg_no="DWD-DWG-010",
        key_figures=[f"{derived()['aperture_m2']:.1f} m2 glazed lid, tilted {TILT:.0f} deg to the sun",
                     "4 kg composite sorbent (silica gel with 25 % CaCl2)",
                     f"About {A['collected']:.2f} L/day at 40 % night RH, air drawn through the beds (estimate)",
                     f"Bed about {A['Tb_noon']:.0f} C at noon by sun only; fan {C.P_FAN * C.H_NIGHT:.0f} Wh/night",
                     f"Collector 1.1 x 1.0 m, top edge {derived()['top_edge_m']:.2f} m high",
                     f"About {sum(C.mass.values()):.0f} kg dry; box about {C.box:.0f} kg (estimate)",
                     f"Parts ${C.cost:.0f} (budget $520)"],
        cut=False, scale_figure=False, context=[person],
        flow={"title": "water per day at the design point, g (estimates; 40 % night RH, 20 C)",
              "unit": "g",
              "stages": [("Vapour in night air", round(1e3 * C.supply)), ("Adsorbed overnight", round(1e3 * A["uptake"])),
                         ("Condensed by day", round(1e3 * A["condensed"])), ("In the bottle", round(1e3 * A["collected"]))],
              "losses": [(0, "Leaves in the outlet air", round(1e3 * (C.supply - A["uptake"]))),
                         (2, "Films and drops", round(1e3 * (A["condensed"] - A["collected"])))]},
    )
    cutaway()
    import shutil
    for d in Path("media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
