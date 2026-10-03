"""DewDrive prototype build plan pictures (DWD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets1|sheets2|layouts|joints|steps1|steps2|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/DWD-DWG-101 to 120        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/plate-holes.png     condenser plate hole layout
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. The box parts are drawn in the box's own frame (lying flat, as on the
bench) unless a picture says otherwise. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import json
import math
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as MD  # noqa: E402
from model import PARAMS as P, stand_geometry, tray_centres, wall_layers  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
SG = stand_geometry(P)
CACHE = Path(tempfile.gettempdir()) / "dewdrive-build-cache"

COL = {"wall": "#C8A165", "skin": "#D6B88A", "batten": "#A16207", "foam": "#FDE68A", "plate": "#9CA3AF",
       "fins": "#6B7280", "gutter": "#0F766E", "fit": "#1F2937", "ledge": "#7C3AED", "deck": "#2563EB",
       "baffle": "#93C5FD", "screens": "#374151", "tray": "#111827", "mesh": "#78716C", "bed": "#E8E2C8",
       "lidf": "#64748B", "pc": "#9CC9D6", "hw": "#111827", "flap": "#B45309", "hood": "#0E7490", "fan": "#1D4ED8",
       "oflap": "#C2410C", "steel": "#57534E", "rail": "#78716C", "leg": "#44403C", "brace": "#A8A29E",
       "xm": "#92400E", "foot": "#334155", "anchor": "#B91C1C", "pole": "#4B5563", "pv": "#1E3A8A",
       "eplate": "#94A3B8", "ebox": "#15803D", "shield": "#F3F4F6", "bottle": "#E5E7EB", "tube": "#DC2626",
       "bolt": "#111827"}


# ----------------------------------------------------------------- components (cached as BREP)
def comps():
    import build123d as b
    src = ROOT / "cad" / "src" / "model.py"
    meta = CACHE / "meta.json"
    if meta.exists() and meta.stat().st_mtime > src.stat().st_mtime:
        m = json.loads(meta.read_text())
        return {k: MD.Comp(v["name"], b.import_brep(str(CACHE / f"{k}.brep")), v["bom"], v["kind"], v["group"], v["material"])
                for k, v in m.items()}
    C = MD.build_components(P)
    CACHE.mkdir(parents=True, exist_ok=True)
    for k, c in C.items():
        b.export_brep(c.shape, str(CACHE / f"{k}.brep"))
    meta.write_text(json.dumps({k: {"name": c.name, "bom": c.bom, "kind": c.kind, "group": c.group, "material": c.material}
                                for k, c in C.items()}))
    return C


C = comps()


def _wloc():
    import build123d as b
    return b.Pos(0, 0, P["z0"]) * b.Rot(P["tilt"], 0, 0)


def flat(shape):
    """World shape back into the box's own frame (box lying flat, glazing up)."""
    return _wloc().inverse() * shape


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*keys, local=False):
    import build123d as b
    sh = C[keys[0]].shape if len(keys) == 1 else b.Compound(children=[C[k].shape for k in keys])   # no boolean fuse: cheap
    return flat(sh) if local else sh


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def nrm(d):
    s, c = math.sin(math.radians(P["tilt"])), math.cos(math.radians(P["tilt"]))
    return (0.0, -s * d, c * d)


def add3(a, b_):
    return tuple(x + y for x, y in zip(a, b_))


# ----------------------------------------------------------------- named parts, in build order (world)
def made():
    return [
        ("walls", part("Wall panels (4)", S("wall_north", "wall_south", "wall_east", "wall_west"), COL["wall"])),
        ("fins", part("Condenser fins (21)", S("fins"), COL["fins"])),
        ("plate", part("Condenser plate", S("plate"), COL["plate"])),
        ("gutter", part("Gutter", S("gutter"), COL["gutter"])),
        ("fit", part("Drain fitting", S("drain_fit"), COL["fit"])),
        ("ledges", part("Wall ledges (2)", S("ledges"), COL["ledge"])),
        ("deck", part("Tray deck frame", S("deck_frame"), COL["deck"])),
        ("baffle", part("Sealing baffle", S("baffle"), COL["baffle"])),
        ("screens", part("Drip screens (4)", S("screens"), COL["screens"])),
        ("trays", part("Sorbent trays (4) with floors", S("trays", "mesh"), COL["tray"])),
        ("bed", part("Composite sorbent", S("bed"), COL["bed"])),
        ("lidf", part("Lid frame", S("lid_frame"), COL["lidf"])),
        ("pc", part("Polycarbonate sheet", S("glazing"), COL["pc"])),
        ("lidhw", part("Lid hinges and latches", S("lid_hinges", "lid_latches"), COL["hw"])),
        ("flap", part("Inlet flap, hinge, latches", S("flap", "flap_hw"), COL["flap"])),
        ("hood", part("Fan hood", S("hood"), COL["hood"])),
        ("fan", part("Night fan", S("fan"), COL["fan"])),
        ("oflap", part("Outlet flap", S("oflap"), COL["oflap"])),
        ("feet", part("Foot plates and cleats (4)", S("feet", "cleats"), COL["foot"])),
        ("legs", part("Legs (4)", S("leg_se", "leg_sw", "leg_ne", "leg_nw"), COL["leg"])),
        ("rails", part("Rails (2)", S("rail_e", "rail_w"), COL["rail"])),
        ("braces", part("Side braces (2)", S("braces"), COL["brace"])),
        ("xm", part("Cross members (2)", S("xm_s", "xm_n"), COL["xm"])),
        ("diag", part("South diagonal brace", S("diag"), COL["xm"])),
        ("anchors", part("Ground anchors (2)", S("anchors"), COL["anchor"])),
        ("pole", part("PV pole and spacers", S("pv_pole"), COL["pole"])),
        ("pv", part("Panel bracket and PV panel", S("pv_bracket", "pv"), COL["pv"])),
        ("eplate", part("Backing plate", S("eplate"), COL["eplate"])),
        ("ebox", part("Electronics box", S("ebox"), COL["ebox"])),
        ("shield", part("Sensor shield", S("shield"), "#D1D5DB")),
        ("bottle", part("Bottle and drain tube", S("bottle", "drain_tube"), COL["bottle"])),
    ]


# ----------------------------------------------------------------- overview
def overview():
    M = dict(made())
    order = [k for k, _ in made()]
    W_, E_ = (-1700, -400, -500), (1500, 300, -200)
    sn, cs = math.sin(math.radians(P["tilt"])), math.cos(math.radians(P["tilt"]))

    def lv(k):   # layers shingle up the slope (north) as they rise, so each one stays partly in view
        return add3(nrm(200 * k), (0, 540 * k * cs, 540 * k * sn))
    off = {"walls": lv(0), "fins": add3(lv(-1.6), (950, 0, -250)), "plate": lv(-1), "gutter": add3(lv(0), (0, -700, -150)),
           "fit": add3(lv(-1), (-400, -900, -250)), "ledges": add3(lv(1), (-700, 0, 0)), "deck": lv(1),
           "baffle": lv(2), "screens": add3(lv(1), (1350, 0, 0)), "trays": lv(3), "bed": lv(4),
           "lidf": lv(5), "pc": lv(6), "lidhw": add3(lv(5), (-1350, 0, 0)), "flap": (-900, -900, 0),
           "hood": add3(lv(1), (1300, 700, 500)), "fan": add3(lv(1), (1300, 1150, 500)), "oflap": add3(lv(1), (1300, 1600, 500)),
           "feet": add3(W_, (300, 0, -800)), "legs": add3(W_, (0, 0, -250)), "rails": add3(W_, (0, 0, 80)),
           "braces": add3(W_, (-350, 0, -250)), "xm": add3(W_, (0, -350, -650)), "diag": add3(W_, (-300, -1000, -500)),
           "anchors": add3(W_, (-650, -700, -250)),
           "pole": add3(E_, (0, 0, -300)), "pv": add3(E_, (0, 0, -100)), "eplate": add3(E_, (1600, 0, 300)),
           "ebox": add3(E_, (1600, 700, 300)), "shield": add3(E_, (1600, 700, 700)), "bottle": (600, -1900, -450)}
    parts = []
    for k in order:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "DewDrive prototype: every component, pulled apart",
                       subtitle="Numbered in build order: box 1 to 18 (middle), stand 19 to 25 (left), power, logging and water 26 to 31 (right). Seen from the south-east and above",
                       elev=20, azim=-55, size=(14, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def _rotz(sh, deg):
    import build123d as b
    return b.Rot(0, 0, deg) * sh


def _upright(sh):
    """Stand a long part on end so its three views fit beside the notes."""
    import build123d as b
    return b.Rot(0, 90, 0) * sh


def _origin(sh):
    import build123d as b
    bb = sh.bounding_box()
    return b.Pos(-bb.center().X, -bb.center().Y, -bb.min.Z) * sh


def sheets(which):
    import build123d as b
    out = []
    base = dict(project="DewDrive", date=DATE)
    W = wall_layers(P)
    loc = _wloc()
    WALLS = [part("Wall panels", S("wall_north", "wall_south", "wall_east", "wall_west"), COL["plate"])]
    gN, gS = SG[1], SG[-1]
    a = P["leg"]

    def sheet(n, key_shape, name, neighbours, title, material, notes, view_shape=None, inset=(24, -58)):
        out.append(bv.component_sheet(Part(name, key_shape, bv.NEW), neighbours, dwg_no=f"DWD-DWG-{n}", title=title,
                                      material=material, notes=notes, view_shape=view_shape, inset_view=inset, **base))

    if which == 1:
        # 101 north and south wall panels
        sk, bat, foam = W["south"]
        south = sk + bat + foam
        sheet(101, loc * south, "South panel", [part("other panels", S("wall_north", "wall_east", "wall_west"), "#ccc"),
                                                part("plate", S("plate"), "#ccc")],
              "DewDrive north and south wall panels (make 1 each): making sketch",
              "6 mm exterior plywood skins, softwood battens, 25 mm PIR foam",
              ["Drawn: the south panel, seen from outside. The north panel is the same",
               "  except for its opening (last lines).",
               "Panel 1,100 long, 133 tall, 40 thick: two 6 mm plywood skins on a",
               "  28 mm core. Core: bottom batten 28 x 44, top batten 28 x 20 (full",
               "  length), end posts 28 x 28 between them, 25 mm PIR in the bays,",
               "  glued to the inner skin. Glue skins to battens with PU adhesive.",
               "South panel: inlet opening 800 x 40, centred, 73 to 113 above the",
               "  bottom edge, framed by a sill batten (28 x 29, on the bottom batten)",
               "  and two 28 x 28 jamb posts. The top batten is the opening's head.",
               "North panel: outlet slot 140 x 44 from the bottom edge, its centre",
               "  330 east of the panel centre: cut it through the bottom batten and",
               "  frame its sides with 28 x 28 posts up to the top batten.",
               "Check: square within 1 mm on the diagonals; skins fully bonded."],
              view_shape=_origin(south), inset=(25, -60))
        # 102 east and west wall panels
        sk, bat, foam = W["east"]
        east = sk + bat + foam
        sheet(102, loc * east, "East panel", [part("other panels", S("wall_north", "wall_south", "wall_west"), "#ccc"),
                                              part("plate", S("plate"), "#ccc")],
              "DewDrive east and west wall panels (make 1 each, mirror): making sketch",
              "6 mm exterior plywood skins, softwood battens, 25 mm PIR foam",
              ["Panel 920 long, 133 tall, 40 thick; it fits between the north and",
               "  south panels. Same core as the long panels: bottom batten 28 x 44,",
               "  top batten 28 x 20, end posts 28 x 28, PIR between.",
               "Threaded inserts: three M6 inserts for wood, 10 mm hole, 20 deep,",
               "  up into the bottom batten on its centre line (20 in from the outer",
               "  face), at 60, 460 and 860 from the south end. The box bolts to the",
               "  stand rails through these.",
               "Ledge screws go into the same bottom batten from inside (DWD-DWG-106).",
               "Corners: three 5 x 65 stainless wood screws through the long panel's",
               "  outer skin and end post into this panel's end post, 22, 67 and 100",
               "  above the bottom edge, 20 in from the outer face; glue as well.",
               "Paint all outer faces; paint the inner skin with heat-resistant paint.",
               "Check: same height as the long panels within 0.5 mm."],
              view_shape=_origin(_rotz(east, 90)), inset=(25, -60))
        # 103 condenser plate
        pl = flat(S("plate"))
        sheet(103, S("plate"), "Condenser plate", [part("walls", S("wall_north", "wall_south", "wall_east", "wall_west"), "#ccc"),
                                                   part("fins", S("fins"), "#ccc")],
              "DewDrive condenser plate: making sketch", "Aluminium sheet 2 mm, 5052 class",
              ["Blank 1,080 x 980 x 2 mm. Top face (the wetted face) up in the views.",
               "Holes along all four edges, 10 mm in from the edge, for the M5",
               "  screws up into the wall bottom battens: 5.5 mm. Positions are in",
               "  the hole layout picture (plate holes) of the build plan.",
               "Three 6.5 mm holes along each east and west edge, 10 mm in, at 90,",
               "  490 and 890 from the south edge: the box to stand bolts.",
               "Drain hole 17 mm, 910 from the west edge and 47 from the south edge.",
               "Deburr all holes. Coat the top face with a food-safe coating after",
               "  the fins are fixed (rivet heads included).",
               "Fit: the walls stand on the top face on EPDM gasket tape; the plate",
               "  edge is 10 mm inside the walls' outer faces all round. The stand",
               "  rails run under the east and west edges.",
               "Check: flat within 2 mm over its length."],
              view_shape=_origin(pl), inset=(-35, -60))
        # 104 fin
        fin = win(flat(S("fins")), -15, 15, -500, 500, -100, 50)
        sheet(104, loc * fin, "Fin", [part("plate", S("plate"), "#ccc")],
              "DewDrive condenser fin (make 21): making sketch", "Aluminium sheet 1 mm",
              ["Blank 920 x 110 x 1 mm. Fold a 10 mm foot along one long edge at 90",
               "  degrees; the fin is then 100 deep below the plate.",
               "Drill 3.3 mm through the foot at 150 pitch, 5 mm from the fold",
               "  (seven holes, the first 20 from each end).",
               "Fit: the foot lies flat on the underside of the plate. Fins at 50",
               "  pitch, the outer ones 40 from the east and west plate edges, 30",
               "  from the north and south edges. Feet point toward the centre line.",
               "Bond each foot with high-temperature epoxy (rated 120 C or more),",
               "  then rivet through the plate with 3.2 mm closed-end aluminium",
               "  rivets, heads on the top (wetted) face.",
               "Check: the fin stands square to the plate within 2 degrees."],
              view_shape=_origin(_rotz(fin, 90)), inset=(-30, -60))
        # 105 gutter
        gu = flat(S("gutter"))
        sheet(105, S("gutter"), "Gutter", [part("plate", S("plate"), "#ccc"), part("south wall", S("wall_south"), "#ccc")],
              "DewDrive gutter: making sketch", "Aluminium sheet 1 mm",
              ["Blank 1,020 x 47 x 1 mm. Fold 16 mm up along one long edge: a 30 mm",
               "  flange and a 16 mm upstand.",
               "Drill 17 mm through the flange for the drain fitting, 370 east of",
               "  the centre (880 from the west end), 17 from the back of the upstand.",
               "Fit: inside the box along the south (low) wall, the flange flat on",
               "  the plate and the upstand against the wall, bedded in food-grade",
               "  silicone; seal both ends to the east and west walls.",
               "Water runs down the plate, over the flange edge into the corner and",
               "  out through the fitting.",
               "Check: no light under the flange when bedded."],
              view_shape=_origin(_upright(gu)), inset=(50, 100))
        # 106 ledge
        led = win(flat(S("ledges")), 400, 600, -500, 500, 0, 200)
        sheet(106, loc * led, "Ledge", [part("east wall", S("wall_east"), "#ccc"), part("deck", S("deck_frame"), "#ccc")],
              "DewDrive wall ledge (make 2): making sketch", "Aluminium equal angle 15 x 15 x 2 mm",
              ["Cut two 910 mm lengths of 15 x 15 x 2 angle; deburr.",
               "Drill four 4.5 mm holes in one leg (the upright leg), 7 from its",
               "  edge, at 50, 320, 590 and 860 from one end; countersink them.",
               "Fit: on the inside of the east and west walls, centred along them,",
               "  the other leg pointing into the box. The top of the ledge is 44",
               "  above the wall bottom, level with the top of the bottom batten.",
               "  Four 4 x 25 countersunk stainless wood screws into the batten.",
               "The tray deck rests on the two ledges (it is not screwed down).",
               "Check: both ledges at the same height within 1 mm."],
              view_shape=_origin(_rotz(led, 90)), inset=(40, 165))
        # 107 deck frame
        df = flat(S("deck_frame"))
        sheet(107, S("deck_frame"), "Deck frame", [part("ledges", S("ledges"), "#ccc"), part("screens", S("screens"), "#ccc")],
              "DewDrive tray deck frame: making sketch", "Aluminium flat bar 20 x 5 mm; angle 20 x 20 x 2 mm",
              ["Flat bar 20 x 5, standing on edge (20 tall). Cut: two sides 916",
               "  (east and west), two ends 1,006 (north and south, fit between the",
               "  sides), one centre bar 906 (north to south, between the ends), two",
               "  cross halves 500.5 (between the centre bar and each side).",
               "Outside size 1,016 x 916. All tops flush.",
               "Join every corner and tee with an angle bracket inside it: 20 x 20 x",
               "  2 angle, 18 long, 16 in all, two 3.2 mm rivets in each leg.",
               "Rivet the baffle sheet on top afterwards (DWD-DWG-108).",
               "Fit: the east and west bars rest on the wall ledges, 2 mm from the",
               "  walls all round; the deck lifts out with the drip screens under it.",
               "Check: flat within 1 mm on a bench; diagonals equal within 2 mm."],
              view_shape=_origin(df), inset=(40, -60))
        # 108 baffle
        bf = flat(S("baffle"))
        sheet(108, S("baffle"), "Baffle", [part("deck", S("deck_frame"), "#ccc")],
              "DewDrive sealing baffle: making sketch", "Aluminium sheet 1 mm",
              ["Blank 1,016 x 916 x 1 mm, the same outside size as the deck frame.",
               "Cut four openings 474 x 414, one under each tray bed: their edges",
               "  15 and 489 east and west of the centre line, 15 and 429 north and",
               "  south of the centre line. Drill 10 mm in the corners, cut between",
               "  with a jigsaw and file straight.",
               "Rivet to the deck frame along the bar centre lines at 150 pitch;",
               "  no rivet falls where a tray lip sits.",
               "Stick EPDM gasket tape round each opening (on top), 8 wide, and an",
               "  EPDM lip seal round the outside edge to close the 2 mm wall gap.",
               "The trays sit on the gasket; the night air can only pass down",
               "  through the beds.",
               "Check: each tray lip covers the gasket all round."],
              view_shape=_origin(bf), inset=(40, -60))
        # 109 drip screen
        xc, yc = tray_centres(P)[3]
        sc = win(flat(S("screens")), xc - 260, xc + 260, 0, 470, 50, 120)
        sheet(109, loc * sc, "Drip screen", [part("deck", S("deck_frame"), "#ccc"), part("baffle", S("baffle"), "#ccc")],
              "DewDrive drip screen (make 4): making sketch",
              "Aluminium flashing 0.5 mm; sheet 1 mm; flat bar 15 x 2 mm",
              ["Drawn: the north-east screen. Upslope is toward the top of the top view.",
               "Channels: 31 per screen, 414 long, bent from 0.5 mm flashing to a",
               "  U 20 wide and 6 deep. Upper layer 16 at 30 pitch; lower layer 15,",
               "  offset half a pitch and 12 lower, so no line of sight.",
               "Frame: two side plates 1 mm, 449.5 x 24; four cross straps 15 x 2",
               "  flat bar, 472 long, 120 each side of the screen centre (upper pair",
               "  on the side plate tops, lower pair 12 lower); ends bent and riveted.",
               "Sump at the low end: 470 x 30 x 12 deep, folded 1 mm, corners sealed,",
               "  with a 422 x 29 tab up its outer wall. End plate at the high end:",
               "  472 x 24 with a 422 x 17 tab. Channels rest on the straps; rivet.",
               "Fit: the two tabs rivet to the faces of the deck bars at each end.",
               "Paint matt black (high-temperature). Check: channel ends overhang",
               "  the sump."],
              view_shape=_origin(sc), inset=(30, -55))
        # 110 tray
        tr = win(flat(S("trays", "mesh")), xc - 246, xc + 246, yc - 216, yc + 216, 100, 140)
        sheet(110, loc * tr, "Tray", [part("baffle", S("baffle"), "#ccc"), part("deck", S("deck_frame"), "#ccc")],
              "DewDrive sorbent tray (make 4): making sketch",
              "Aluminium sheet 1 mm; perforated aluminium 1 mm; stainless woven mesh",
              ["Pan 490 x 430 x 25 deep from 1 mm sheet: blank 540 x 480 with the",
               "  centre cut out to leave an 8 mm rim (inner 474 x 414). Fold the",
               "  four sides up 25 at the 490 x 430 lines; the rim becomes an inward",
               "  bottom lip. Notch and rivet the corners; seal them with silicone.",
               "Floor: 1 mm perforated aluminium (about 50 % open), 488 x 428, laid",
               "  on the lip, with a stainless woven mesh (1 mm aperture) of the same",
               "  size on top. The sorbent holds them down.",
               "Paint the inside and the top edge matt black (high-temperature);",
               "  leave the underside bare.",
               "EPDM gasket tape under the lip, all round.",
               "Fit: the lip sits on the baffle gasket over its opening; 13 to 23 mm",
               "  from the walls, 14 mm between trays.",
               "Check: the floor sags less than 3 mm with 1 kg spread on it."],
              view_shape=_origin(tr), inset=(35, -55))
    else:
        # 111 lid frame
        lf = flat(S("lid_frame"))
        sheet(111, S("lid_frame"), "Lid frame", [part("walls", S("wall_north", "wall_south", "wall_east", "wall_west"), "#ccc")],
              "DewDrive lid frame: making sketch", "Aluminium glazing U-channel 14 x 12 x 2 mm (for 10 mm sheet)",
              ["Four lengths of U-channel, mitred 45 degrees: two 1,100 (north and",
               "  south), two 1,000 (east and west), outside sizes.",
               "Slide them onto the polycarbonate sheet (1,096 x 996, flutes running",
               "  north to south); seal the low (south) flute ends with breather tape",
               "  and the high ends with aluminium tape first.",
               "Join each corner with a 20 x 20 x 2 angle bracket inside the channel",
               "  web, two 3.2 mm rivets each side.",
               "Hinges: three 60 mm stainless butt hinges on the north side, 440 west",
               "  of centre, at centre and 470 east; rivet one leaf to the frame and",
               "  screw the other into the north wall's top batten.",
               "Latches: two over-centre latches on the south side, 475 each side of",
               "  centre; keeper riveted to the frame, body screwed to the wall.",
               "Fit: the frame rests on an EPDM seal on the wall tops.",
               "Check: the lid closes evenly on the seal all round."],
              view_shape=_origin(lf), inset=(40, -60))
        # 112 inlet flap
        fl = flat(S("flap"))
        sheet(112, S("flap"), "Inlet flap", [part("south wall", S("wall_south"), "#ccc"), part("lid", S("lid_frame"), "#ccc")],
              "DewDrive inlet flap: making sketch", "Aluminium sheet 1.5 mm",
              ["Blank 840 x 60 x 1.5 mm; deburr; round the corners to 3 mm.",
               "It covers the 800 x 40 inlet opening with 20 to spare at each end",
               "  and 10 above and below.",
               "Stick EPDM foam seal on its inner face, 10 wide, all round.",
               "Hinge: a piano hinge along the top edge, one leaf riveted to the",
               "  flap, the other screwed into the south wall's top batten.",
               "Latches: two over-centre latches on the bottom edge, 300 each side",
               "  of centre, bodies screwed into the sill batten below the opening.",
               "The wall leans out at the top, so the flap hangs open by its own",
               "  weight when unlatched; latched, it is pulled onto its seal.",
               "Check: closed, a strip of paper is gripped all round."],
              view_shape=_origin(fl), inset=(15, -70))
        # 113 fan hood and outlet flap
        hd = flat(S("hood", "oflap"))
        sheet(113, S("hood"), "Fan hood", [part("walls", S("wall_north", "wall_south", "wall_east", "wall_west"), "#ccc"),
                                           part("plate", S("plate"), "#ccc"), part("flap", S("oflap"), "#ccc")],
              "DewDrive fan hood and outlet flap: making sketch", "Aluminium sheet 1 mm (hood); 1.5 mm (flap)",
              ["Hood 160 wide, 64 deep, 130 tall, folded from one 1 mm blank: front,",
               "  top, bottom and two sides; a 15 mm flange folded out at the back",
               "  edge of each side; corners riveted and sealed.",
               "Cut a 114 mm round hole in the front, centred, for the fan.",
               "The 120 mm fan screws to the inside of the front with four M4",
               "  screws, blowing out (north).",
               "Fit: over the 140 x 44 outlet slot in the north wall, the hood's",
               "  bottom level with the wall bottom; four screws through each flange,",
               "  bedded in silicone.",
               "Outlet flap 140 x 125 x 1.5 mm with EPDM seal, hinged at its top",
               "  edge on the hood front. By day it hangs shut on the fan opening; at",
               "  night a wire stay holds it open.",
               "Check: the fan turns freely with the flap open."],
              view_shape=_origin(hd), inset=(30, 70))
        # 114 rail
        r = S("rail_e")
        rf = flat(r)
        bl = MD.to_local(gN["Yc"], gN["bolt_z"], P)
        sheet(114, r, "Rail", [part("plate", S("plate"), "#ccc"), part("legs", S("leg_ne", "leg_se"), "#ccc"),
                               part("wall", S("wall_east"), "#ccc")],
              "DewDrive stand rail (make 2, a left and a right): making sketch", "Galvanized steel angle 30 x 30 x 3 mm",
              ["Cut two 1,000 mm lengths of 30 x 30 x 3 angle.",
               "Top leg (lies flat under the box): 6.5 mm holes for the box bolts",
               "  15 from the corner at 100, 500 and 900 from the south end; 12 mm",
               "  clearance holes over the plate screw heads, 15 from the corner at",
               "  200, 350, 650 and 800, and 20 from the corner at 20 and 980.",
               f"Hanging leg: one 9 mm hole for each leg bolt, 60 from each end,",
               f"  {P['plate_top'] - P['plate_t'] - bl[1]:.0f} down from the top face.",
               "The hanging leg is on the outside; the east and west rails are",
               "  mirror images. Drill as a pair. Re-galvanize or paint cut ends.",
               "Fit: top leg under the plate's east (or west) edge, its outer edge",
               "  5 mm outside the plate; three M6 bolts up into the wall inserts.",
               "Check: the holes line up with the plate holes when laid under it."],
              view_shape=_origin(_upright(_rotz(rf, 90))), inset=(20, -40))
        # 115 and 116 legs
        for n, key, nm, extra in ((115, "leg_se", "south", ["South legs carry the side brace's high end (395 above the bottom)",
                                                             "  and the diagonal brace: west leg 270, east leg 465 above the",
                                                             "  bottom, in the outward leg, 16 from the corner."]),
                                  (116, "leg_ne", "north", ["North legs carry the side brace's low end, 145 above the bottom.",
                                                             "North-east leg: two 9 mm holes for the PV pole, 559 and 799 above",
                                                             "  the bottom, in the face leg. North-west leg: two 9 mm holes for",
                                                             "  the backing plate, in the outward leg, 15 from the corner."])):
            g = SG[1 if nm == "north" else -1]
            L = g["top"] - P["foot_t"]
            sheet(n, S(key), f"Leg ({nm})", [part("rail", S("rail_e"), "#ccc"), part("feet", S("feet", "cleats"), "#ccc"),
                                             part("braces", S("braces"), "#ccc")],
                  f"DewDrive {nm} legs (make 2, a left and a right): making sketch", "Galvanized steel angle 30 x 30 x 3 mm",
                  [f"Cut two {L:.0f} mm lengths of 30 x 30 x 3 angle; ends square.",
                   "The face leg bolts to the rail and the brace; the outward leg",
                   f"  points {'south' if nm == 'south' else 'north'}, away from the box, and carries the cross member.",
                   f"Face leg, 9 mm holes on its centre line: rail bolt 12 below the",
                   f"  top; foot cleat bolt 17 above the bottom.",
                   "Outward leg: cross member bolt 212 above the bottom, 17 from the",
                   "  corner.",
                   *extra,
                   "Left and right legs are mirror images: drill as a pair.",
                   "Check: the top sits 3 mm below the rail's top face once bolted."],
                  view_shape=_origin(S(key)), inset=(20, -40))
        # 117 side brace
        ps = (SG[-1]["Yc"] + 5, 400.0)
        pn = (SG[1]["Yc"] - 5, 150.0)
        L = math.hypot(pn[0] - ps[0], pn[1] - ps[1])
        ang = math.degrees(math.atan2(pn[1] - ps[1], pn[0] - ps[0]))
        brs = win(S("braces"), 500, 700, -1000, 1000, 0, 1000)
        import build123d as b
        laid = b.Rot(-ang, 0, 0) * b.Pos(0, -(ps[0] + pn[0]) / 2, -(ps[1] + pn[1]) / 2) * brs
        sheet(117, brs, "Side brace", [part("legs", S("leg_se", "leg_ne"), "#ccc"), part("rail", S("rail_e"), "#ccc")],
              "DewDrive side brace (make 2, a left and a right): making sketch", "Galvanized steel angle 30 x 30 x 3 mm",
              [f"Cut two {L + 24:.0f} mm lengths of 30 x 30 x 3 angle; ends square.",
               f"Drill a 9 mm hole 12 from each end on the flat leg's centre line:",
               f"  {L:.0f} between centres.",
               f"It runs from the south leg, 395 above the bottom, down to the north",
               f"  leg, 145 above the bottom, at {abs(ang):.0f} degrees.",
               "Fit: the flat leg lies on the outer face of both legs' face legs,",
               "  the other leg standing out at its lower edge. One M8 bolt at each end.",
               "This brace makes each side frame a rigid triangle.",
               "Check: hole centres within 1 mm of the length above."],
              view_shape=_origin(_rotz(laid, 90)), inset=(15, -20))
        # 118 cross members and diagonal
        xm = S("xm_s")
        sheet(118, xm, "Cross member", [part("legs", S("leg_se", "leg_sw"), "#ccc"), part("diag", S("diag"), "#ccc")],
              "DewDrive cross members (make 2): making sketch", "Galvanized steel angle 30 x 30 x 3 mm",
              ["Cut two 1,150 mm lengths of 30 x 30 x 3 angle; both are the same.",
               "Upright leg: a 9 mm hole 13 from each end, 17 above the lower edge.",
               "Fit: the upright leg lies on the outer face of the two legs' outward",
               "  legs, 200 above the ground, the other leg pointing away from the",
               "  box; one M8 bolt each end. South member at the south legs, north",
               "  member at the north legs.",
               "Check: both holes line up with the leg holes at the same time."],
              view_shape=_origin(xm), inset=(5, -90))
        dg = S("diag")
        pw_, pe_ = (-(545 + a / 2), 275.0), (545 + a / 2, 470.0)
        Ld = math.hypot(pe_[0] - pw_[0], pe_[1] - pw_[1])
        angd = math.degrees(math.atan2(pe_[1] - pw_[1], pe_[0] - pw_[0]))
        dl = b.Rot(0, angd, 0) * b.Pos(0, -SG[-1]["Yc"], -(pw_[1] + pe_[1]) / 2) * dg
        sheet(119, dg, "Diagonal brace", [part("legs", S("leg_se", "leg_sw"), "#ccc"), part("xm", S("xm_s"), "#ccc")],
              "DewDrive south diagonal brace: making sketch", "Galvanized steel angle 30 x 30 x 3 mm",
              [f"Cut one {Ld + 24:,.0f} mm length of 30 x 30 x 3 angle; ends square.",
               f"A 9 mm hole 12 from each end on the flat leg's centre line:",
               f"  {Ld:,.0f} between centres.",
               "Fit: on the outer face of the south legs' outward legs, above the",
               "  south cross member, from the west leg (275 above the ground) up",
               f"  to the east leg (470 above the ground), at {angd:.0f} degrees; the",
               "  other leg stands out at its lower edge. One M8 bolt each end.",
               "It stops the stand racking sideways. The north end needs none: the",
               "  box, bolted to both rails, ties the two side frames together.",
               "Check: the drain tube passes above it with room to spare."],
              view_shape=_origin(_rotz(dl, 0)), inset=(5, -90))
        # 120 foot plate and cleat
        g = SG[-1]
        ft = win(S("feet", "cleats"), 470, 620, g["Yc"] - 70, g["Yc"] + 70, -1, 60)
        sheet(120, ft, "Foot plate and cleat", [part("leg", S("leg_se"), "#ccc")],
              "DewDrive foot plate and cleat (make 4): making sketch", "Steel plate 5 mm; galvanized angle 30 x 30 x 3 mm",
              ["Foot plate 120 x 120 x 5 mm, corners rounded. One 9 mm hole 17 from",
               "  the plate centre toward the box side, countersunk from below so the",
               "  bolt head sits flush and the plate lies flat on the ground.",
               "Cleat: 22 mm length of 30 x 30 x 3 angle. 9 mm holes: upright leg",
               "  17 above its lower face; lying leg 17 from the corner; both centred.",
               "Fit: the cleat's lying leg bolts to the plate with a countersunk",
               "  M8 bolt from below; its upright leg sits inside the leg's face",
               "  leg and bolts to it, 17 above the plate.",
               "Paint or galvanize the plate after drilling.",
               "Check: the leg stands square on the plate."],
              view_shape=_origin(ft), inset=(25, -40))
        # 121 PV pole, 122 backing plate
        pp = S("pv_pole")
        sheet(121, pp, "PV pole", [part("leg", S("leg_ne"), "#ccc"), part("bracket and panel", S("pv_bracket", "pv"), "#ccc"),
                                  part("box", S("wall_east", "wall_north", "lid_frame"), "#ccc")],
              "DewDrive PV pole: making sketch", "Steel square tube 25 x 25 x 2 mm, galvanized; two spacer blocks",
              ["Cut 726 mm of 25 x 25 x 2 square tube; cap the top with the bought",
               "  pole-top tilt bracket's sleeve.",
               "Drill 9 mm right through, on the centre line, 30 and 270 from the",
               "  bottom.",
               "Spacers: two 24 x 24 mm blocks of 8 mm steel, drilled 9 mm.",
               "Fit: on the outer face of the north-east leg's face leg, with a",
               "  spacer at each bolt so the pole stands 6 mm clear of the box",
               "  wall; two M8 x 50 bolts through leg, spacer and pole.",
               "The panel bracket sits on top and tilts the panel 30 degrees,",
               "  facing south.",
               "Check: the pole is plumb within 1 degree."],
              view_shape=_origin(pp), inset=(20, -20))
        bpl = S("eplate")
        sheet(122, bpl, "Backing plate", [part("leg", S("leg_nw"), "#ccc"), part("ebox", S("ebox"), "#ccc"),
                                          part("shield", S("shield"), "#ccc")],
              "DewDrive electronics backing plate: making sketch", "Aluminium sheet 3 mm",
              ["Plate 160 x 430 x 3 mm; corners rounded.",
               "Two 9 mm holes 90 from its west edge, 30 from the top and bottom,",
               "  for the M8 bolts into the north-west leg's outward leg.",
               "Mark and drill the electronics box's four fixing holes through the",
               "  box itself (box centred 20 west of the bolts, 60 above the bottom",
               "  of the plate); M5 screws and nyloc nuts.",
               "Sensor shield arm: 20 x 3 aluminium strip bent to a Z, riveted to",
               "  the plate's top corner; the bought shield screws to its top.",
               "Fit: on the north face of the leg, so the box faces north, shaded by",
               "  the collector, its lid away from the frame.",
               "Check: the box lid opens fully."],
              view_shape=_origin(_rotz(bpl, 0)), inset=(20, 50))
    return out


# ----------------------------------------------------------------- plate hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    pl = flat(S("plate"))
    face = [f for f in pl.faces() if abs(f.center().Z - P["plate_top"]) < 0.01 and f.area > 1e5][0]
    px_, py_ = P["plate_xy"]
    fig = plt.figure(figsize=(12, 9.6), dpi=150)
    ax = fig.add_axes([0.05, 0.06, 0.9, 0.84]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), px_, py_, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((10 + 0, 10), px_ - 20, py_ - 20, fc="none", ec=MUT, lw=0.5, ls=":"))
    lbl = []
    for w in face.inner_wires():
        bb = w.bounding_box()
        x, y, d = bb.center().X + px_ / 2, bb.center().Y + py_ / 2, bb.size.X
        col = "#B91C1C" if d > 15 else (AC if d > 6 else INK)
        ax.add_patch(plt.Circle((x, y), max(d / 2, 4), fc="white", ec=col, lw=1.1))
        lbl.append((x, y, d))
    # dimension lines from the west (left) and south (bottom) edges
    xs = sorted({round(x) for x, y, d in lbl if y < 30})
    for i, x in enumerate(xs):
        ax.text(x, -14 - 14 * (i % 2), f"{x}", ha="center", va="top", fontsize=7.5, color=INK)
        ax.plot([x, x], [0, -10 - 14 * (i % 2)], color=MUT, lw=0.4, ls=":")
    xs = sorted({round(x) for x, y, d in lbl if y > py_ - 30})
    for i, x in enumerate(xs):
        ax.text(x, py_ + 14 + 14 * (i % 2), f"{x}", ha="center", va="bottom", fontsize=7.5, color=INK)
        ax.plot([x, x], [py_, py_ + 10 + 14 * (i % 2)], color=MUT, lw=0.4, ls=":")
    ys = sorted({round(y) for x, y, d in lbl if x < 30})
    for y in ys:
        ax.text(-14, y, f"{y}", ha="right", va="center", fontsize=7.5, color=INK)
    ys = sorted({round(y) for x, y, d in lbl if x > px_ - 30})
    for y in ys:
        ax.text(px_ + 14, y, f"{y}", ha="left", va="center", fontsize=7.5, color=INK)
    dr = [(x, y) for x, y, d in lbl if d > 15][0]
    ax.annotate(f"Drain hole 17 mm\n{dr[0]:.0f} from the west edge,\n{dr[1]:.0f} from the south edge", xy=dr, xytext=(dr[0] - 260, dr[1] + 170),
                fontsize=8, color="#B91C1C", arrowprops=dict(arrowstyle="-", color="#B91C1C", lw=0.6))
    ax.text(px_ / 2, -62, "South edge (the low edge, along the gutter)", ha="center", fontsize=8.5, color=MUT)
    ax.text(px_ / 2, py_ + 52, "North edge (high edge; the fan slot is above the gap in this row)", ha="center", fontsize=8.5, color=MUT)
    ax.text(-75, py_ / 2, "West edge", rotation=90, ha="center", va="center", fontsize=8.5, color=MUT)
    ax.text(px_ + 75, py_ / 2, "East edge", rotation=90, ha="center", va="center", fontsize=8.5, color=MUT)
    ax.text(px_ / 2, py_ / 2 + 60, "Top (wetted) face up. All holes 10 mm in from the edge.", ha="center", fontsize=9, color=INK)
    ax.text(px_ / 2, py_ / 2 + 10, "Black, 5.5 mm: M5 screws up into the wall bottom battens.", ha="center", fontsize=9, color=INK)
    ax.text(px_ / 2, py_ / 2 - 40, "Teal, 6.5 mm: M6 bolts from the stand rails into the wall inserts.", ha="center", fontsize=9, color=AC)
    ax.text(px_ / 2, py_ / 2 - 90, "Figures: mm from the west edge (top and bottom rows) and from the south edge (side rows).",
            ha="center", fontsize=8.5, color=MUT)
    ax.set_xlim(-120, px_ + 120); ax.set_ylim(-80, py_ + 75)
    fig.text(0.03, 0.97, "Condenser plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.935, "Plate 1,080 x 980 x 2 mm seen from above, figures from the model.", fontsize=8.5, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/dewdrive", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "plate-holes.png"


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    WLy = wall_layers(P)

    def layers(side, box_):
        sk, bat, foam = WLy[side]
        return [part(f"{side.capitalize()} wall: plywood skins", win(sk, *box_), COL["skin"]),
                part(f"{side.capitalize()} wall: softwood battens", win(bat, *box_), COL["batten"]),
                part(f"{side.capitalize()} wall: PIR foam", win(foam, *box_), COL["foam"])]

    def L(k, box_):
        return win(S(k, local=True), *box_)

    def J(n, parts, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.joint([p for p in parts if p.shape is not None], OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub,
                            size=kw.pop("size", (8, 6)), **kw))

    # 1 wall corner, from above, cut at mid height
    bx_ = (440, 556, 380, 506, 90, 112.5)
    J(1, layers("north", bx_) + [part("East wall: skins, end post, foam", win(fuse(WLy["east"]), *bx_), "#E7D3B0"),
                                 part("Corner screw, 5 x 65 (cut through)", L("corner_screws", bx_[:5] + (113.5,)), "#DC2626")],
      "wall corner (north-east), seen from above, cut through the middle screw",
      "The east panel fits between the long panels; screws go through the north panel into the east panel's end post",
      elev=70, azim=-120)
    # 2 east edge: wall, plate, rail, bolt, insert, fin
    bx_ = (480, 560, 380, 420, 0, 100)
    J(2, layers("east", bx_) + [part("Condenser plate", L("plate", bx_), COL["plate"]),
                                part("Rail (stand)", L("rail_e", bx_), COL["rail"]),
                                part("M6 bolt into the threaded insert", L("rail_bolts", bx_) + L("inserts", bx_), COL["bolt"]),
                                part("Outer fin", L("fins", bx_), COL["fins"])],
      "box on the stand rail (east edge, cut through a bolt)",
      "Plate screwed up into the bottom batten; the rail lies under the plate edge; an M6 bolt goes up into the insert",
      elev=12, azim=-80, cut="+Y")
    # 3 fin foot
    bx_ = (125, 175, 0, 30, 5, 50)
    J(3, [part("Condenser plate (2 mm)", L("plate", bx_), "#CBD5E1"), part("Fin with its folded 10 mm foot", L("fins", bx_), "#0E7490")],
      "fin on the underside of the condenser plate",
      "Cut across a fin, seen from the south and below. The foot is bonded and riveted (closed-end rivets) to the plate",
      elev=-12, azim=-75)
    # 4 gutter and drain
    bx_ = (330, 410, -500, -400, 15, 80)
    J(4, layers("south", bx_) + [part("Condenser plate", L("plate", bx_), COL["plate"]), part("Gutter", L("gutter", bx_), COL["gutter"]),
                                 part("Drain fitting", L("drain_fit", bx_), COL["fit"]), part("Fins", L("fins", bx_), COL["fins"])],
      "gutter and drain fitting, seen from inside the box",
      "From the north-west. Water runs down the plate, over the gutter flange into the corner and out through the fitting",
      elev=22, azim=150, cut="+X")
    # 5 ledge, deck, baffle, tray at the east wall
    bx_ = (440, 520, 190, 230, 55, 145)
    J(5, layers("east", bx_) + [part("Wall ledge", L("ledges", bx_), COL["ledge"]), part("Deck bar", L("deck_frame", bx_), COL["deck"]),
                                part("Baffle", L("baffle", bx_), COL["baffle"]), part("Tray", L("trays", bx_), COL["tray"]),
                                part("Tray floor", L("mesh", bx_), COL["mesh"]), part("Sorbent", L("bed", bx_), COL["bed"]),
                                part("Drip screen", L("screens", bx_), COL["screens"])],
      "tray deck on the wall ledge, tray on the baffle (east wall)",
      "Seen from the south, cut. The deck rests on the ledge, 2 mm off the wall; the tray lip sits on the baffle gasket",
      elev=10, azim=-90, cut="+Y")
    # 6 drip screens on the centre deck bar
    bxn = (245, 275, 2, 45, 55, 115)
    bxs = (245, 275, -40, -2, 55, 115)
    bx_ = (245, 275, -40, 45, 55, 115)
    J(6, [part("Deck centre cross bar", L("deck_frame", bx_), COL["deck"]), part("Baffle", L("baffle", bx_), COL["baffle"]),
          part("North screen: sump, riveted to the bar's north face", L("screens", bxn), "#374151"),
          part("South screen: end plate, riveted to the bar's south face", L("screens", bxs), "#B45309"),
          part("Trays", L("trays", bx_), COL["tray"])],
      "drip screens hung on a deck bar (centre, cut north to south)",
      "Seen from the west, cut. The north screen's sump and the south screen's end plate are riveted to the two faces of the bar",
      elev=8, azim=180, cut="+X")
    # 7 lid hinge
    bx_ = (-45, 45, 465, 515, 140, 200)
    J(7, layers("north", bx_) + [part("Lid frame", L("lid_frame", bx_), COL["lidf"]), part("Polycarbonate", L("glazing", bx_), COL["pc"]),
                                 part("Hinge", L("lid_hinges", bx_), COL["hw"])],
      "lid on the north wall, at the middle hinge (cut)",
      "The frame rests on an EPDM seal on the wall top; the hinge leaf screws into the top batten",
      elev=12, azim=-10, cut="+X")
    # 8 inlet flap
    bx_ = (-40, 40, -515, -445, 80, 195)
    J(8, layers("south", bx_) + [part("Inlet flap", L("flap", bx_), COL["flap"]), part("Flap hinge", L("flap_hw", bx_), COL["hw"]),
                                 part("Lid frame", L("lid_frame", bx_), COL["lidf"]), part("Deck and baffle", L("deck_frame", bx_) + L("baffle", bx_), COL["deck"])],
      "inlet opening and flap (south wall, cut at the centre)",
      "The opening is above the baffle, so the night air must go down through the beds; the flap hangs from its top hinge",
      elev=10, azim=-170, cut="-X")
    # 9 fan hood
    bx_ = (240, 395, 440, 570, 40, 185)
    J(9, layers("north", bx_) + [part("Fan hood", L("hood", bx_), COL["hood"]), part("Fan", L("fan", bx_), COL["fan"]),
                                 part("Outlet flap", L("oflap", bx_), COL["oflap"]), part("Condenser plate", L("plate", bx_), COL["plate"])],
      "fan hood over the outlet slot (cut through the fan)",
      "Seen from the west, cut. Air from under the deck leaves through the slot, the hood and the fan; by day the flap closes the fan",
      elev=10, azim=172, cut="+X")
    # 10 leg to rail (world)
    g = SG[1]
    bx_ = (500, 600, g["Yc"] - 70, g["Yc"] + 70, g["top"] - 45, g["top"] + 45)
    J(10, [part("Rail", win(S("rail_e"), *bx_), COL["rail"]), part("North-east leg", win(S("leg_ne"), *bx_), COL["leg"]),
           part("M8 bolt", win(S("stand_bolts"), *bx_), COL["bolt"]), part("Condenser plate", win(S("plate"), *bx_), COL["plate"]),
           part("East wall", win(S("wall_east"), *bx_), "#E7D3B0")],
      "leg to rail (north-east leg, seen from the east)",
      "The leg's face leg lies on the rail's hanging leg: one M8 bolt; the leg top is cut square, 3 mm under the rail top",
      elev=10, azim=0)
    # 11 foot
    g = SG[-1]
    bx_ = (470, 620, g["Yc"] - 70, g["Yc"] + 70, -1, 70)
    J(11, [part("Foot plate", win(S("feet"), *bx_), "#94A3B8"), part("Cleat", win(S("cleats"), *bx_), "#0E7490"),
           part("South-east leg", win(S("leg_se"), *bx_), COL["leg"]), part("M8 bolts", win(S("stand_bolts"), *bx_), COL["bolt"])],
      "foot plate, cleat and leg (south-east)",
      "Countersunk bolt up through the plate into the cleat; the leg bolts to the cleat's upright leg",
      elev=20, azim=-140)
    # 12 cross member and diagonal on the south-east leg
    bx_ = (470, 600, g["Yc"] - 60, g["Yc"] + 20, 185, 500)
    J(12, [part("South-east leg", win(S("leg_se"), *bx_), COL["leg"]), part("South cross member", win(S("xm_s"), *bx_), COL["xm"]),
           part("Diagonal brace", win(S("diag"), *bx_), "#D97706"), part("M8 bolts", win(S("stand_bolts"), *bx_), COL["bolt"])],
      "south cross member and diagonal brace on the south-east leg",
      "Both bolt to the leg's outward leg, outside the frame; seen from the south",
      elev=10, azim=-100, size=(8, 7))
    # 13 PV pole
    g = SG[1]
    bx_ = (480, 610, g["Yc"] - 45, g["Yc"] + 45, g["top"] - 100, g["top"] + 60)
    J(13, [part("North-east leg", win(S("leg_ne"), *bx_), COL["leg"]), part("PV pole and spacers", win(S("pv_pole"), *bx_), "#60A5FA"),
           part("M8 bolt", win(S("pv_bolts"), *bx_), COL["bolt"]), part("Rail", win(S("rail_e"), *bx_), COL["rail"]),
           part("East wall", win(S("wall_east"), *bx_), "#E7D3B0")],
      "PV pole on the north-east leg (upper bolt)",
      "Seen from the north-east. 8 mm spacers keep the pole 6 mm clear of the box wall; M8 bolts through leg, spacer and pole",
      elev=20, azim=50, size=(8, 6))
    # 14 side brace on the south leg
    g = SG[-1]
    bx_ = (520, 600, g["Yc"] - 35, g["Yc"] + 70, 360, 440)
    J(14, [part("South-east leg", win(S("leg_se"), *bx_), COL["leg"]), part("Side brace", win(S("braces"), *bx_), COL["brace"]),
           part("M8 bolt", win(S("stand_bolts"), *bx_), COL["bolt"])],
      "side brace on the south-east leg",
      "The brace's flat leg lies on the outer face of the leg; one M8 bolt",
      elev=15, azim=-20)
    return out


# ----------------------------------------------------------------- assembly steps
ONLY_STEPS = None


def steps(group):
    out = []

    def st(n, done, new, title, sub, **kw):
        if ONLY_STEPS and n not in ONLY_STEPS:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def Lp(name, keys, col, e=(0, 0, 0)):
        return part(name, S(*keys, local=True), col, e)

    walls = ["wall_north", "wall_south", "wall_east", "wall_west"]
    box0 = [Lp("Walls", walls + ["corner_screws"], COL["wall"]), Lp("Plate and fins", ["plate", "fins", "plate_screws", "inserts"], COL["plate"])]
    if group == 1:
        st(1, [Lp("North and south panels", ["wall_north", "wall_south"], COL["wall"])],
           [Lp("East panel", ["wall_east"], COL["wall"], (250, 0, 0)), Lp("West panel", ["wall_west"], COL["wall"], (-250, 0, 0))],
           "join the wall panels into a box", "East and west panels between the long panels; glue and three 5 x 65 screws per corner",
           elev=28, azim=-60, label_done=True)
        st(2, [Lp("Condenser plate (seen from below)", ["plate"], COL["plate"])], [Lp("Fins (21)", ["fins"], "#0E7490", (0, 0, -150))],
           "fins onto the condenser plate", "Seen from below. Bond each foot with epoxy, then rivet through the plate; feet toward the centre",
           elev=-30, azim=-60, label_done=True)
        st(3, [Lp("Plate and fins", ["plate", "fins"], COL["plate"])],
           [Lp("Wall box", walls + ["corner_screws", "inserts"], COL["wall"], (0, 0, 250)), Lp("M5 screws", ["plate_screws"], COL["bolt"], (0, 0, -120))],
           "box onto the plate", "Gasket tape on the wall bottoms; M5 screws up through the plate into the bottom battens",
           elev=22, azim=-60, label_done=False)
        st(4, box0, [Lp("Gutter", ["gutter"], COL["gutter"], (0, 0, 220)), Lp("Drain fitting", ["drain_fit"], COL["fit"], (0, 0, 380))],
           "gutter and drain fitting", "Gutter bedded in silicone along the south wall; fitting down through gutter and plate, nut tightened below",
           elev=55, azim=-70, label_done=False)
        box1 = box0 + [Lp("Gutter and fitting", ["gutter", "drain_fit"], COL["gutter"])]
        st(5, box1, [Lp("Wall ledges", ["ledges"], COL["ledge"], (0, 0, 220))],
           "wall ledges onto the east and west walls", "Top of each ledge level with the top of the bottom batten; four screws each",
           elev=55, azim=-70, label_done=False)
        st(6, [Lp("Deck frame", ["deck_frame"], COL["deck"])], [Lp("Baffle sheet", ["baffle"], COL["baffle"], (0, 0, 160))],
           "baffle onto the deck frame", "On the bench. Rivet along the bar centre lines at 150 pitch; then gasket tape and the edge seal",
           elev=40, azim=-60, label_done=True)
        st(7, [Lp("Deck with baffle (seen from below)", ["deck_frame", "baffle"], COL["deck"])],
           [Lp("Drip screens (4)", ["screens"], COL["screens"], (0, 0, -170))],
           "drip screens under the deck", "Seen from below. Each screen's two tabs rivet to the faces of the deck bars; sumps at the low (south) end",
           elev=-40, azim=-60, label_done=True)
        box2 = box1 + [Lp("Ledges", ["ledges"], COL["ledge"])]
        st(8, box2, [Lp("Deck with drip screens", ["deck_frame", "baffle", "screens"], COL["deck"], (0, 0, 300))],
           "deck into the box", "Lower it level onto the two ledges; the lip seal closes the gap to the walls",
           elev=50, azim=-65, label_done=False)
        box3 = box2 + [Lp("Deck", ["deck_frame", "baffle", "screens"], COL["deck"])]
        st(9, box3, [Lp("Trays, filled with sorbent", ["trays", "mesh", "bed"], "#4B5563", (0, 0, 250))],
           "trays onto the deck", "Each tray lip on the gasket round its opening; handle filled trays cool, with gloves",
           elev=50, azim=-65, label_done=False)
        box4 = box3 + [Lp("Trays", ["trays", "mesh", "bed"], COL["tray"])]
        st(10, box4, [Lp("Lid (frame, sheet, hinges, latches)", ["lid_frame", "glazing", "lid_hinges", "lid_latches"], COL["pc"], (0, 0, 280))],
           "the lid", "Seal on the wall tops; hinge leaves into the north top batten; latch bodies on the south wall",
           elev=35, azim=-60, label_done=False)
    else:
        box5 = [Lp("Box", walls + ["plate", "fins", "corner_screws", "plate_screws", "inserts", "gutter", "drain_fit", "ledges",
                                   "deck_frame", "baffle", "screens", "trays", "mesh", "bed", "lid_frame", "glazing",
                                   "lid_hinges", "lid_latches"], COL["wall"])]
        st(11, box5, [Lp("Inlet flap with its hinge and latches", ["flap", "flap_hw"], COL["flap"], (0, -450, 0))],
           "inlet flap on the south wall", "Piano hinge into the top batten; latch bodies into the sill batten below the opening",
           elev=15, azim=-50, label_done=False)
        st(12, box5 + [Lp("Inlet flap", ["flap", "flap_hw"], COL["flap"])],
           [Lp("Fan hood", ["hood"], COL["hood"], (0, 250, 0)), Lp("Fan (inside the hood front)", ["fan"], COL["fan"], (0, 550, 0)),
            Lp("Outlet flap", ["oflap"], COL["oflap"], (0, 850, 0))],
           "fan, hood and outlet flap on the north wall", "Fan screwed inside the hood front; hood over the slot, flanges screwed and sealed",
           elev=15, azim=60, label_done=False)
        feet = part("Foot plates and cleats", S("feet", "cleats"), COL["foot"])
        st(13, [feet], [part("Legs (4)", S("leg_se", "leg_sw", "leg_ne", "leg_nw"), COL["leg"], (0, 0, 200)),
                        part("Rails (2)", S("rail_e", "rail_w"), COL["rail"], (0, 0, 380)),
                        part("Side brace (east)", win(S("braces"), 0, 700, -900, 900, 0, 900), COL["brace"], (300, 0, 0)),
                        part("Side brace (west)", win(S("braces"), -700, 0, -900, 900, 0, 900), COL["brace"], (-300, 0, 0))],
           "the two side frames", "Seen from the east. Each side: two legs, a rail and a brace, M8 bolts; build them flat, then stand them up",
           elev=15, azim=-20, label_done=True)
        sides = [feet, part("Side frames", S("leg_se", "leg_sw", "leg_ne", "leg_nw", "rail_e", "rail_w", "braces"), COL["leg"])]
        st(14, sides, [part("Cross members (2)", S("xm_s", "xm_n"), COL["xm"], (0, -250, 0)),
                       part("South diagonal brace", S("diag"), "#D97706", (0, -400, 0))],
           "cross members and diagonal brace", "Seen from the south. Bolt both cross members, then the diagonal; check the rails are level and square, then tighten",
           elev=12, azim=-78, label_done=False)
        stand = sides + [part("Cross members and diagonal", S("xm_s", "xm_n", "diag", "stand_bolts"), COL["xm"])]
        st(15, stand, [part("Ground anchors (2)", S("anchors"), COL["anchor"], (0, 0, 450))],
           "ground anchors", "Screw each anchor in 190 mm outside a south leg; strap it to the leg with a ratchet strap",
           elev=20, azim=-55, label_done=False)
        stand2 = stand + [part("Anchors", S("anchors"), COL["anchor"])]
        boxw = part("Box (with its flaps and fan)", S("wall_north", "wall_south", "wall_east", "wall_west", "plate", "fins", "gutter",
                                                      "drain_fit", "lid_frame", "glazing", "lid_hinges", "lid_latches", "flap", "flap_hw",
                                                      "hood", "fan", "oflap"), COL["wall"])
        st(16, stand2, [mv(boxw, (0, 0, 450)), part("M6 bolts (6)", S("rail_bolts"), COL["bolt"], (0, 0, -200)),
                        part("Label: empty before lifting", S("label"), "#F2C94C", (0, 0, 450))],
           "box onto the stand", "Two people; trays, sorbent and deck out, label on the east wall. Lower the box onto the rails; six M6 bolts up into the inserts",
           elev=18, azim=-55, label_done=False)
        full = stand2 + [boxw]
        st(17, full, [part("PV pole and spacers", S("pv_pole", "pv_bolts"), COL["pole"], (250, 0, 0)),
                      part("Panel bracket and panel", S("pv_bracket", "pv"), COL["pv"], (0, 0, 300))],
           "PV pole and panel", "Pole on the north-east leg on two spacers and M8 bolts; panel on the bracket, tilted 30 degrees to the south",
           elev=18, azim=40, label_done=False)
        full2 = full + [part("PV pole and panel", S("pv_pole", "pv_bracket", "pv"), COL["pole"])]
        st(18, full2, [part("Backing plate", S("eplate", "ebolts"), COL["eplate"], (0, 250, 0)),
                       part("Electronics box", S("ebox"), COL["ebox"], (0, 450, 0)),
                       part("Sensor shield", S("shield"), "#9CA3AF", (0, 300, 300))],
           "electronics and sensor shield", "Backing plate on the north-west leg; box and shield on the plate; cables along the frame",
           elev=18, azim=130, label_done=False)
        full3 = full2 + [part("Electronics", S("eplate", "ebox", "shield"), COL["ebox"])]
        st(19, full3, [part("Bottle", S("bottle"), "#60A5FA", (0, -300, 0)), part("Drain tube", S("drain_tube"), COL["tube"], (0, -150, 0))],
           "bottle and drain tube", "Tube from the fitting's barb, over the diagonal brace, through the cap grommet",
           elev=18, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "DewDrive prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules in the electronics box, wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/dewdrive", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((22, 14), 66, 46, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(23.5, 58.8, "Inside the IP65 electronics box (on the north-west leg)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(3, 42, 14, 13, "PV panel", "10 W, 12 V,\non its pole", "#1E3A8A")
    blk(26, 42, 17, 13, "Charge controller", "12 V PWM,\nLiFePO4 setting", "#16A34A")
    blk(26, 18, 17, 14, "LiFePO4 battery", "12.8 V 6 Ah,\nbuilt-in BMS;\n10 A fuse at +", "#C2410C")
    blk(50, 42, 15, 13, "Load fuse", "3 A blade fuse\non the load +", "#7C3AED")
    blk(69, 40, 16, 15, "ESP32 logger", "12 V to 5 V buck,\nRTC, microSD", "#0F766E")
    blk(52, 18, 15, 14, "Fan switch", "logic-level\nMOSFET module", "#16A34A")
    blk(97, 46, 19, 10, "Night fan", "12 V, about 2 W,\nin the hood", "#1D4ED8")
    blk(97, 28, 19, 13, "Air T and RH", "SHT4x class, in its\nshield (I2C)", "#4B5563")
    blk(97, 12, 19, 12, "Bed and condenser", "two DS18B20 probes\n(1-wire)", "#4B5563")
    wire([(17, 48.5), (26, 48.5)], RED); lab(21.5, 50.8, "PV +/- 1.0 mm²", RED, "center")
    wire([(34.5, 42), (34.5, 32)], RED); lab(35.2, 37, "battery, 1.5 mm²", RED)
    wire([(43, 48.5), (50, 48.5)], RED); lab(46.5, 50.8, "load, 1.0 mm²", RED, "center")
    wire([(65, 48.5), (69, 48.5)], RED); lab(67, 50.8, "0.5 mm²", RED, "center")
    wire([(57.5, 42), (57.5, 32)], RED); lab(58.2, 37, "fan +, 0.5 mm²", RED)
    wire([(67, 25), (92, 25), (92, 50), (97, 50)], RED); lab(78, 27, "to the fan, 0.5 mm², through a gland", RED, "center")
    wire([(77, 40), (77, 30), (67, 30)], GRY, 1.2); lab(77.6, 35, "gate, 0.25 mm²", GRY)
    wire([(85, 47), (90, 47), (90, 34.5), (97, 34.5)], BLU, 1.2); lab(88, 39, "I2C,\n0.25 mm²", BLU, "right")
    wire([(85, 43), (88, 43), (88, 18), (97, 18)], BLU, 1.2); lab(87.4, 22, "1-wire,\n0.25 mm²", BLU, "right")
    ax.text(23, 9.6, "Safety: battery fuse out until all wiring is checked. Never charge the battery below 0 °C. Keep the box shaded.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(23, 6.2, "Red: power. Blue: signal. Grey: control. All circuits are extra-low voltage: 12.8 V battery, about 22 V panel open circuit.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets1", "sheets2", "layouts", "joints", "steps1", "steps2", "wiring"]
    fns = {"overview": overview, "sheets1": lambda: sheets(1), "sheets2": lambda: sheets(2), "layouts": layouts,
           "joints": joints, "steps1": lambda: steps(1), "steps2": lambda: steps(2), "wiring": wiring}
    for w in what:
        if w.startswith("step:"):
            ONLY_STEPS = [int(w[5:])]
            r = steps(1 if ONLY_STEPS[0] <= 10 else 2)
        elif w.startswith("joint:"):
            r = joints(only=[int(x) for x in w[6:].split(",")])
        else:
            r = fns[w]()
        print(w, "->", r)
