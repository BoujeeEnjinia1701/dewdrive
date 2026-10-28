"""DewDrive product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the battened plywood walls, the twin-wall
glazing in its U-channel frame with hinges and latches, the four trays with their black absorber plates on the
sorbent, the tray deck, baffle and drip screens, the painted finned condenser with every rivet, the gutter, drain
and jerrycan, both flaps, the fan in its hood, the bolted galvanized stand with foot plates, cleats and auger
anchors, the PV panel on its pole, the electronics enclosure with its battery, controller and logger board, the
radiation shield, and every screw, bolt, nut, washer and insert. Only the site is added, as context parts: a
mud-brick yard wall behind the unit and a 1.75 m mannequin standing on the ground for scale. Ground level is
model z = 0; the site wall and the anchors reach below it. The hero is rendered by .kit/photoreal.py as an
outdoor scene on sand under a high sun (RENDER_VIEWS "args").
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the unit as built), "context" (site wall and mannequin). Exploded views use the per-part
"explode" offsets set here by sub-assembly.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "DewDrive: solar-regenerated desiccant water harvester"

_SITE = ["--scene=outdoor", "--ground=sand", "--ground-z=0", "--sun=55,-65", "--lens=45"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 16, "az": -40, "args": _SITE,
     "note": "Site render in a desert yard from the front right and a little above (about 16 deg elevation): the glazed box "
             "tilted 20 deg toward the sun on its galvanized stand, black absorber plates on the four sorbent beds behind the "
             "clear lid, PV panel on its pole behind, the jerrycan under the low edge, a mud-brick yard wall behind and a "
             "1.75 m person standing on the sand at the left for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 26, "az": -45,
     "note": "Studio render from the front right and above (about 26 deg elevation): glazing in its U-channel frame, black "
             "absorber plates over the beds, inlet flap with its latches, painted fins under the box, bolted stand"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view from the front right and above (about 26 deg elevation): lid lifted along the glazing normal, "
             "trays with absorber plates and sorbent above the deck with its drip screens, walls, condenser below, stand "
             "dropped, PV, electronics and sensor shield pulled clear"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 22, "az": 55,
     "note": "Detail from the back right, slightly above (about 22 deg elevation): fan hood and outlet flap on the north wall, "
             "electronics enclosure on its backing plate, radiation shield and PV pole"},
]

_T = math.radians(M.PARAMS["tilt"])
_N = (0.0, -math.sin(_T), math.cos(_T))          # glazing normal


def _n(d, extra=(0.0, 0.0, 0.0)):
    return (_N[0] * d + extra[0], _N[1] * d + extra[1], _N[2] * d + extra[2])


EXPLODE = {"lid": _n(900, (0, 0, 0)), "trays": _n(560), "screens": _n(300), "deck": _n(300), "walls": _n(60),
           "box": _n(0), "condenser": _n(-260), "water": (300, -600, -80), "flap": (0, -420, 120), "fan": (0, 420, 0),
           "stand": (0, 0, -420), "pv": (500, 600, 200), "ebox": (-700, 400, 0), "shield": (-700, 400, 250)}


def site():
    """Site context: a mud-brick yard wall north of the unit and a mannequin for scale. Ground level is z = 0;
    the wall reaches 200 mm below ground."""
    out = []
    wall = Pos(0, 2600, 650) * Box(5200, 300, 1700)
    out.append(part("Mud-brick yard wall (site)", break_edges(wall, 20.0), "mud", kind="context", group="context", color="#9C7A55"))
    try:
        import context_parts
        man = Pos(-1700, -500, 0) * Rot(0, 0, -25) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["group"] = "shell"
        q["explode"] = EXPLODE.get(p["group"], (0, 0, 0))
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "context" for p in ps), "context")
