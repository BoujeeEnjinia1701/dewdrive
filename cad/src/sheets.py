"""DewDrive general arrangement sheet DWD-DWG-001, Rev P2 (TRL 3, DWD-DDR-002 revision).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/DWD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are computed from the model and PARAMS,
so they follow any parameter change. The concept sheet in media/ is DWD-DWG-010.
"""
import math
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build, derived, world  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived()
    work = ROOT / "cad" / "drawings" / "_views"
    asm = build()
    views = project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="DewDrive", title="General arrangement", dwg_no="DWD-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Plywood and PIR box, twin-wall PC lid, Al trays and finned condenser, galv. steel stand; see bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Through-flow trays, baffle, raised inlet, drip screens (DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    out = []
    LX, LY = P["box_x"], P["box_y"]
    # ---- top view (looking down, north up): overall and box plan sizes
    x, y, w, h = c["top"]
    out += dim_h(x, x + w, y - 3.5, f"{bb.size.X:.0f} overall")
    out += dim_v(x - 4, y, y + h, f"{bb.size.Y:.0f} overall")
    bx0 = x + (-LX / 2 - bb.min.X) * k
    bx1 = x + (LX / 2 - bb.min.X) * k
    out += [ext(bx0, y + 2, bx0, y - 10), ext(bx1, y + 2, bx1, y - 10)]
    out += dim_h(bx0, bx1, y - 9, f"{LX:.0f} box")
    # ---- front view (from the south, -Y): overall height, top and low edge heights
    x, y, w, h = c["front"]
    zb = y + h
    out += dim_v(x - 4, y, zb, f"{bb.size.Z:.0f} to PV")
    zt = zb - D["top_edge_m"] * 1e3 * k
    out += [ext(x - 11, zt, bx0, zt)]
    out += dim_v(x - 10, zt, zb, f"{D['top_edge_m'] * 1e3:.0f} top edge")
    # ---- right view (from +X, south at left): box slope length, tilt, low edge height
    x, y, w, h = c["right"]
    zb = y + h
    ylo = x + (world(0, -LY / 2, P["wall_z0"] + P["wall_h"] + P["glaz_t"])[1] - bb.min.Y) * k
    zlo = zb - D["low_edge_m"] * 1e3 * k
    out += [ext(ylo, zlo, x - 6, zlo)]
    out += dim_v(x - 5, zlo, zb, f"{D['low_edge_m'] * 1e3:.0f} low edge")
    out.append(_t(x + w / 2, y - 3, f"Glazing tilted {P['tilt']:.0f} deg, facing the equator", 2.3, 400, INK, "middle"))
    s._layers += out
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale")
    gap_u, gap_o = D["gap_under_m"] * 1e3, D["gap_over_m"] * 1e3
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Box {LX:.0f} x {LY:.0f} x {P['wall_h']:.0f}; walls {P['wall_t']:.0f} (ply, 25 PIR, ply)",
        f"Lid {P['glaz_t']:.0f} twin-wall PC, hinged north edge; inner {D['inner_x_m'] * 1e3:.0f} x {D['inner_y_m'] * 1e3:.0f}",
        f"Trays 4 x {P['tray_x']:.0f} x {P['tray_y']:.0f} x {P['tray_h']:.0f}, sealed on a baffle; bed {P['bed_depth']:.1f} deep, {D['bed_m2']:.3f} m2",
        f"Drip screens: 2 layers of {P['scr_w']:.0f} x {P['scr_lip']:.0f} channels at {P['scr_pitch']:.0f} pitch; sumps {D['sump_l']:.2f} L",
        f"Gaps: {gap_o:.0f} tray rim to lid, {gap_u:.0f} tray floor to condenser",
        f"Condenser {P['plate_t']:.0f} Al plate, {P['fin_n']} fins {P['fin_t']:.0f} x {P['fin_h']:.0f} at {P['fin_pitch']:.0f} pitch",
        f"Inlet {P['flap_in'][0]:.0f} x {P['flap_in'][1]:.0f} (S, above trays); outlet {P['flap_out'][0]:.0f} x {P['flap_out'][1]:.0f} and fan (N, below)",
        f"Stand 4 legs, L{P['leg']:.0f} x {P['leg_t']:.0f} galv.; feet {P['foot']:.0f} sq; 2 ground anchors",
        "Mass about 54 kg dry; box about 33 kg (DWD-CAL-001 v0.2, G1)",
        "Third-angle; front view from south (-Y), right from +X",
    ], x=276, y=158, width=140)
    path = s.save(ROOT / "cad" / "drawings" / "DWD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {path} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
