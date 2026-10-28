"""DewDrive concept options B and C (DWD-OPT-001), modelled at detail level D3 (STANDARDS section 24).

Both options use the same 1.1 m x 1.0 m footprint as option A so the three can be compared at one scale.
Coordinates in mm: X east, Y north, Z up, ground at z = 0. Every part is a cad_parts.part() dict.

    B  Radiative dew condenser: an insulated aluminium panel with a high-emissivity white coating, tilted 30 deg
       on a welded and bolted galvanized stand, with a gutter, drain and jerrycan. No sorbent, no power.
    C  Liquid-desiccant glazed still: three tiers of black cloth soaked in CaCl2 brine on an aluminium rack in a
       black HDPE brine tray, under a fixed glazed gable roof on cut-and-folded aluminium gable plates; vent
       doors in the gables are opened at night; condensate runs down the glazing into eave channels.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot, Torus, Compound  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
import dwd_parts as dp  # noqa: E402

B_PARAMS = dict(tilt=30.0, panel_x=1100.0, panel_y=1000.0, frame=(30.0, 3.0), foam_t=27.0, sheet_t=1.0, back_t=1.0,
                zc=950.0, leg=(40.0, 4.0), foot=(150.0, 6.0), attach_y=400.0)
C_PARAMS = dict(frame_x=1100.0, frame_y=1000.0, zb=450.0, steel=(40.0, 4.0), tray_t=6.0, tray_in=(526.0, 476.0),
                pitch=35.0, eave_z=25.0, gable_t=2.0, flange=27.0, panel_t=12.0, pc_t=4.0, foot=(120.0, 6.0))


def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, r, h):
    return Pos(x, y, z0 + h / 2) * Cylinder(r, h)


def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def fuse(items):
    out = None
    for s in items:
        out = s if out is None else out + s
    return out


def _bottle(x, y):
    """10 L jerrycan with cap and moulded handle."""
    body = bx(x - 90, x + 90, y - 130, y + 130, 0, 320)
    body = break_edges(body, 12.0)
    cap = zcyl(x, y + 40, 320, 28, 40)
    handle = bx(x - 12, x + 12, y - 110, y - 20, 320, 345) - bx(x - 13, x + 13, y - 95, y - 35, 319, 335)
    return body + cap + handle


def _anchor(x, y):
    return zcyl(x, y, -400, 5, 430) + Pos(x, y, 45) * Rot(90, 0, 0) * Torus(12, 3) + Pos(x, y, -330) * Cylinder(40, 4)


def _weld(length, leg, at_xyz, rot):
    return Pos(*at_xyz) * rot * cp.weld_fillet(length, leg)


# =============================================================================================================
# Option B: radiative dew condenser
# =============================================================================================================
def option_b(P=B_PARAMS):
    t = math.radians(P["tilt"])
    s, c = math.sin(t), math.cos(t)
    W = Pos(0, 0, P["zc"]) * Rot(P["tilt"], 0, 0)
    HX, HY = P["panel_x"] / 2, P["panel_y"] / 2
    a, ft = P["frame"]
    out = []

    def add(name, shape, mat, kind="made", group="panel", color=None):
        out.append(part(name, shape, mat, kind=kind, group=group, color=color))

    def world(x, y, z):
        return (x, y * c - z * s, P["zc"] + y * s + z * c)

    zf1 = 31.0                                   # frame height (local z), panel stack inside it
    xi, yi = HX - ft, HY - ft                    # frame inner faces (547, 497)
    # rivet and bolt cutters (local), shared by sheet, frame and foam
    riv = []
    for y in (-400, -200, 0, 200, 400):
        for sx in (-1, 1):
            if abs(y) != 400:
                riv.append((sx * (HX + 1), y, 21.0, "+x" if sx > 0 else "-x"))
    for x in (-400, -200, 0, 200, 400):
        riv.append((x, HY + 1, 21.0, "+y"))
    rcut = fuse([dp.hole(4.1, (x, y, z), ax, 14) for (x, y, z, ax) in riv])
    bolts_l = [(sx * HX, sy * P["attach_y"], 15.5) for sx in (-1, 1) for sy in (-1, 1)]
    bcut = fuse([dp.hole(10.5, (sx * (HX + 1), y, z), "+x", 12) for (sx_, y, z) in bolts_l for sx in [1 if sx_ > 0 else -1]])
    pockets = fuse([dp.orient(Pos(0, 0, -11) * Cylinder(11, 22), (sx_ * xi, y, z), "+x" if sx_ > 0 else "-x")
                    for (sx_, y, z) in [(1 if q[0] > 0 else -1, q[1], q[2]) for q in bolts_l]])
    # frame: welded aluminium angle 30 x 30 x 3, vertical leg outside, horizontal leg at the bottom
    ew = []
    for sx in (-1, 1):
        m = bx(*sorted((sx * HX, sx * xi)), -HY, HY, 0, zf1) + bx(*sorted((sx * xi, sx * (HX - a))), -yi, yi, 0, ft)
        ew.append(m)
        add(f"Panel frame, {'east' if sx > 0 else 'west'} side, 30 x 30 x 3 aluminium angle", W * (m - rcut - bcut), "aluminium")
    for sy in (-1, 1):
        m = bx(-xi, xi, *sorted((sy * HY, sy * yi)), 0, zf1) + bx(-(HX - a), HX - a, *sorted((sy * yi, sy * (HY - a))), 0, ft)
        add(f"Panel frame, {'north' if sy > 0 else 'south'} side, 30 x 30 x 3 aluminium angle", W * (m - rcut), "aluminium")
    for k, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        bead = Pos(sx * xi, sy * yi, ft) * Rot(0, 0, 90 * k) * Rot(0, 0, 90) * Rot(0, -90, 0) * cp.weld_fillet(zf1 - ft, 4.0)
        add(f"Weld, frame corner {k + 1} (TIG fillet)", W * bead, "aluminium", kind="weld")
    notch = fuse([bx(sx * (xi - 9), sx * xi + sx, sy * (yi - 9), sy * yi + sy, -1, zf1 + 1) for sx in (-1, 1) for sy in (-1, 1)])
    back = bx(-xi, xi, -yi, yi, ft, ft + P["back_t"]) - notch
    add("Back sheet, 1 mm aluminium", W * back, "aluminium")
    foam = bx(-xi + 1, xi - 1, -yi + 1, yi - 1, ft + P["back_t"], zf1) - notch - rcut - pockets
    add("Insulation board, 27 mm closed-cell polyethylene foam", W * foam, "insulated_white", color="#D9D9D2")
    # condenser sheet: 1 mm aluminium, white high-emissivity coating on top; flanges folded down on the east,
    # west and north sides; drip lip folded down at the low (south) edge into the gutter
    st = P["sheet_t"]
    sheet = bx(-HX - st, HX + st, -HY - 15, HY + st, zf1, zf1 + st)
    sheet = sheet + bx(HX, HX + st, -HY, HY + st, 6, zf1) + bx(-HX - st, -HX, -HY, HY + st, 6, zf1) \
        + bx(-HX - st, HX + st, HY, HY + st, 6, zf1) + bx(-HX - st, HX + st, -HY - 15, -HY - 14, 5, zf1)
    add("Condenser sheet, 1 mm aluminium, white radiative coating", W * (sheet - rcut - bcut), "insulated_white", color="#F4F4F0")
    for (x, y, z, ax) in riv:
        face = (x + (st if ax == "+x" else -st if ax == "-x" else 0) - (1 if ax == "+x" else -1 if ax == "-x" else 0),
                y + (st - 1 if ax == "+y" else 0), z)
        for q in dp.rivet(4, st + ft, face, ax, label="sheet to frame"):
            q["shape"] = W * q["shape"]; q["group"] = "panel"; out.append(q)
    # stand: four galvanized angle legs 40 x 40 x 4 welded to foot plates, one M10 bolt each into the panel frame
    la, lt = P["leg"]
    fa, fth = P["foot"]
    legs = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            X0 = sx * (HX + st)
            _, Yc, Zc = world(sx * HX, sy * P["attach_y"], 15.5)
            top = Zc + 40
            fl_a = bx(*sorted((X0, X0 + sx * lt)), Yc - la / 2, Yc + la / 2, fth, top)
            yb = Yc + sy * la / 2
            fl_b = bx(*sorted((X0, X0 + sx * la)), *sorted((yb, yb - sy * lt)), fth, top)
            nm = f"{'north' if sy > 0 else 'south'}-{'east' if sx > 0 else 'west'}"
            legs[(sx, sy)] = (X0, Yc, top, yb)
            hole_ = dp.hole(10.5, (X0, Yc, Zc), "+x", 12)
            add(f"Leg, {nm}, 40 x 40 x 4 galvanized angle", fl_a + fl_b - hole_, "galvanised", group="stand")
            fx = X0 + sx * la / 2
            add(f"Foot plate, {nm}, 150 x 150 x 6 galvanized", break_edges(bx(fx - fa / 2, fx + fa / 2, Yc - fa / 2, Yc + fa / 2, 0, fth), 1.0),
                "galvanised", group="stand")
            # fillet weld along the outer face of flange A, clear of flange B
            y0, y1 = (Yc - la / 2, yb - sy * lt) if sy > 0 else (yb - sy * lt, Yc + la / 2)
            xo = X0 + sx * lt
            rot = Rot(0, 0, -90) if sx > 0 else Rot(0, 0, 90)
            start = (xo, y1 if sx > 0 else y0, fth)
            add(f"Weld, leg {nm} to foot plate", _weld(abs(y1 - y0), 5.0, start, rot), "galvanised", kind="weld", group="stand")
            out += dp.bolt_set(10, (X0 + sx * lt, Yc, Zc), "+x" if sx > 0 else "-x", lt + st + ft, label=f"leg {nm} to panel", group="stand")
    # side braces (30 x 30 x 3 angle) on the outer faces of flange A: south leg low to north leg high
    for sx in (-1, 1):
        X0s, Ys, _, _ = legs[(sx, -1)]
        X0n, Yn, _, _ = legs[(sx, 1)]
        xa_, xb_ = X0s + sx * lt, X0s + sx * (lt + 3)
        p0, p1 = (Ys + 5, 300.0), (Yn - 5, 950.0)
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        xm = (xa_ + xb_) / 2
        br = Pos(0, (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2) * Rot(ang, 0, 0) * (
            Pos(xm, 0, 0) * Box(3, L + 24, 30) + Pos(xb_ + sx * 13.5, 0, -13.5) * Box(27, L + 24, 3))
        cut = fuse([dp.hole(9, (xa_, y, z), "+x", 12) for (y, z) in (p0, p1)])
        add(f"Side brace, {'east' if sx > 0 else 'west'}, 30 x 30 x 3 galvanized angle", br - cut, "galvanised", group="stand")
        for (y, z) in (p0, p1):
            out += dp.bolt_set(8, (xb_, y, z), "+x" if sx > 0 else "-x", lt + 3, label="side brace", group="stand")
    # the brace holes in the legs
    for i, q in enumerate(out):
        if q["name"].startswith("Leg,"):
            sx = 1 if "east" in q["name"] else -1
            X0s, Ys, _, _ = legs[(sx, -1)]
            X0n, Yn, _, _ = legs[(sx, 1)]
            pts = [(Ys + 5, 300.0)] if "south" in q["name"] else [(Yn - 5, 950.0)]
            q["shape"] = q["shape"] - fuse([dp.hole(9, (X0s, y, z), "+x", 12) for (y, z) in pts])
    # end cross members on flange B, front and back, 30 x 30 x 3 angle
    for sy in (-1, 1):
        Yo = legs[(1, sy)][3]
        z0 = 160.0
        xm_ = bx(-(HX + st + la), HX + st + la, *sorted((Yo, Yo + sy * 3)), z0, z0 + 30) + \
            bx(-(HX + st + la), HX + st + la, *sorted((Yo, Yo + sy * 30)), z0, z0 + 3)
        xs = [sx * (HX + st + la / 2 + 2) for sx in (-1, 1)]
        cut = fuse([dp.hole(9, (x, Yo, z0 + 17), "+y", 12) for x in xs])
        add(f"{'North' if sy > 0 else 'South'} cross member, 30 x 30 x 3 galvanized angle", xm_ - cut, "galvanised", group="stand")
        for x in xs:
            out += dp.bolt_set(8, (x, Yo + sy * 3, z0 + 17), "+y" if sy > 0 else "-y", 3 + lt, label="cross member", group="stand")
        for q in out:
            if q["name"].startswith("Leg,") and (("north" in q["name"]) == (sy > 0)):
                q["shape"] = q["shape"] - fuse([dp.hole(9, (x, Yo, z0 + 17), "+y", 12) for x in xs])
    # gutter on two brackets from the south legs, drain to a jerrycan
    gz0, gz1, gy0, gy1 = 675.0, 705.0, -482.0, -436.0
    gx = HX + 20
    gutter = bx(-gx, gx, gy0, gy1, gz0, gz1) - bx(-gx + 1, gx - 1, gy0 + 1, gy1 - 1, gz0 + 1, gz1 + 1)
    gutter = gutter - zcyl(gx - 25, (gy0 + gy1) / 2, gz0 - 1, 8.5, 3)
    add("Gutter, 1 mm aluminium, folded, with end caps", gutter, "aluminium", group="water")
    for sx in (-1, 1):
        X0, Yc, _, yb = legs[(sx, -1)]
        x0b, x1b = sorted((X0 + sx * 6, X0 + sx * 34))
        brk = bx(x0b, x1b, yb - 3, yb, 640, gz0) + bx(x0b, x1b, gy0 - 3, yb, gz0 - 3, gz0)
        cut = dp.hole(9, ((x0b + x1b) / 2, yb, 655), "+y", 12)
        add(f"Gutter bracket, {'east' if sx > 0 else 'west'}, 25 x 3 galvanized flat bar", brk - cut, "galvanised", group="water")
        out += dp.bolt_set(8, ((x0b + x1b) / 2, yb - 3, 655), "-y", 3 + lt, label="gutter bracket", group="water")
        for q in out:
            if q["name"] == f"Leg, south-{'east' if sx > 0 else 'west'}, 40 x 40 x 4 galvanized angle":
                q["shape"] = q["shape"] - cut
    dx, dy = gx - 25, (gy0 + gy1) / 2
    fit = zcyl(dx, dy, gz0 + 1, 15, 3) + zcyl(dx, dy, gz0 - 25, 8.25, 26) + Pos(dx, dy, gz0 - 8) * cp._hex(27, 5)
    fit = fit - zcyl(dx, dy, gz0 - 30, 5.5, 40)
    add("Drain bulkhead fitting with 12 mm hose barb, food grade", fit, "hdpe_natural", kind="bought", group="water")
    bxx, byy = gx + 120, -760.0
    p0, p1, p2 = (dx, dy, gz0 - 25), (dx, dy, gz0 - 80), (bxx, byy + 40, 380)
    tb = tube(p0, p1, 8) + Pos(*p1) * __import__("build123d").Sphere(8) + tube(p1, p2, 8)
    tb = tb - zcyl(dx, dy, gz0 - 30, 6, 6)
    add("Drain tube, food-grade silicone, 12 mm bore", tb, "hdpe_natural", kind="bought", group="water", color="#E8E6DF")
    add("Collection jerrycan, 10 L food-grade HDPE", _bottle(bxx, byy), "hdpe_natural", kind="bought", group="water", color="#E9ECEE")
    for sx in (-1, 1):
        X0, Yc, _, _ = legs[(sx, -1)]
        add(f"Auger ground anchor with eye ({'east' if sx > 0 else 'west'})", _anchor(X0 + sx * 230, Yc), "galvanised", kind="bought", group="stand")
    return out


# =============================================================================================================
# Option C: liquid-desiccant glazed still
# =============================================================================================================
def option_c(P=C_PARAMS):
    HX, HY = P["frame_x"] / 2, P["frame_y"] / 2
    Zb = P["zb"]
    sa, st = P["steel"]
    tx, ty = P["tray_in"]
    pa = math.radians(P["pitch"])
    tn = math.tan(pa)
    Ze = Zb + P["eave_z"]
    apex = Ze + HY * tn
    out = []

    def add(name, shape, mat, kind="made", group="still", color=None):
        out.append(part(name, shape, mat, kind=kind, group=group, color=color))

    # ---- steel base frame: four galvanized angles 40 x 40 x 4, welded corners, vertical leg outside
    xi, yi = HX - st, HY - st
    for sx in (-1, 1):
        m = bx(*sorted((sx * HX, sx * xi)), -HY, HY, Zb - sa, Zb) + bx(*sorted((sx * xi, sx * (HX - sa))), -yi, yi, Zb - sa, Zb - sa + st)
        m = m - fuse([dp.hole(9, (sx * HX, y, Zb - 20), "+x", 12) for y in (-350.0, 0.0, 350.0)]) \
            - fuse([dp.hole(9, (sx * HX, y, Zb - 28), "+x", 12) for y in (-478.0, 478.0)])
        add(f"Base frame, {'east' if sx > 0 else 'west'} side, 40 x 40 x 4 galvanized angle", m, "galvanised", group="base")
    for sy in (-1, 1):
        m = bx(-xi, xi, *sorted((sy * HY, sy * yi)), Zb - sa, Zb) + bx(-(HX - sa), HX - sa, *sorted((sy * yi, sy * (HY - sa))), Zb - sa, Zb - sa + st)
        m = m - fuse([dp.hole(9, (x, sy * HY, Zb - 12), "+y", 12) for x in (-532.0, 532.0)])
        add(f"Base frame, {'north' if sy > 0 else 'south'} side, 40 x 40 x 4 galvanized angle", m, "galvanised", group="base")
    for k, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        bead = Pos(sx * xi, sy * yi, Zb - sa + st) * Rot(0, 0, 90 * k) * Rot(0, 0, 90) * Rot(0, -90, 0) * cp.weld_fillet(sa - st, 4.0)
        add(f"Weld, base frame corner {k + 1}", bead, "galvanised", kind="weld", group="base")
    # ---- legs: angle 40 x 40 x 4 outside each corner, bolted to the frame; welded foot plates
    fa, fth = P["foot"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            nm = f"{'north' if sy > 0 else 'south'}-{'east' if sx > 0 else 'west'}"
            fl_a = bx(*sorted((sx * HX, sx * (HX + st))), *sorted((sy * (HY - 44), sy * (HY + st))), fth, Zb)
            fl_b = bx(*sorted((sx * (HX - 40), sx * (HX + st))), *sorted((sy * HY, sy * (HY + st))), fth, Zb)
            leg = fl_a + fl_b - dp.hole(9, (sx * HX, sy * 478.0, Zb - 28), "+x", 12) - dp.hole(9, (sx * 532.0, sy * HY, Zb - 12), "+y", 12)
            add(f"Leg, {nm}, 40 x 40 x 4 galvanized angle", leg, "galvanised", group="base")
            fx, fy = sx * (HX - 18), sy * (HY - 18)
            add(f"Foot plate, {nm}, 120 x 120 x 6 galvanized", break_edges(bx(fx - fa / 2, fx + fa / 2, fy - fa / 2, fy + fa / 2, 0, fth), 1.0),
                "galvanised", group="base")
            xo = sx * (HX + st)
            y0, y1 = sorted((sy * (HY - 44), sy * HY))
            rot = Rot(0, 0, -90) if sx > 0 else Rot(0, 0, 90)
            add(f"Weld, leg {nm} to foot plate", _weld(y1 - y0, 4.0, (xo, y1 if sx > 0 else y0, fth), rot), "galvanised", kind="weld", group="base")
            out += dp.bolt_set(8, (sx * (HX + st), sy * 478.0, Zb - 28), "+x" if sx > 0 else "-x", 2 * st, label=f"leg {nm}", group="base")
            out += dp.bolt_set(8, (sx * 532.0, sy * (HY + st), Zb - 12), "+y" if sy > 0 else "-y", 2 * st, label=f"leg {nm}", group="base")
    # ---- black HDPE brine tray, welded from 6 mm sheet, on the frame's bottom legs; drain plug
    tt = P["tray_t"]
    tray = bx(-tx, tx, -ty, ty, Zb - sa + st, Zb) - bx(-tx + tt, tx - tt, -ty + tt, ty - tt, Zb - sa + st + tt, Zb + 1)
    try:
        from build123d import Axis, fillet
        tray = fillet(tray.edges().filter_by(Axis.Z).group_by(Axis.X)[0] + tray.edges().filter_by(Axis.Z).group_by(Axis.X)[-1], 4.0)
    except Exception:
        pass
    plug_xy = (tx - 40, -ty + 40)
    tray = tray - zcyl(*plug_xy, Zb - sa + st - 1, 10, tt + 2)
    add("Brine tray, black HDPE 6 mm, welded", tray, "hdpe_black", group="tray")
    plug = zcyl(*plug_xy, Zb - sa + st - 14, 10, 14 + tt) + Pos(plug_xy[0], plug_xy[1], Zb - sa + st - 14) * cp._hex(30, 8)
    add("Brine drain plug, HDPE, 3/4 in BSP", plug, "hdpe_black", kind="bought", group="tray")
    # ---- cloth rack: four aluminium posts 20 x 20 x 2 and three shelf tiers of 20 x 20 x 2 angle with black cloth
    zt = Zb - sa + st + tt                           # tray floor
    posts = [(sx * 475.0, sy * 95.0) for sx in (-1, 1) for sy in (-1, 1)]
    tiers = [(Zb + 40.0, 400.0), (Zb + 150.0, 240.0), (Zb + 240.0, 125.0)]
    post_top = tiers[-1][0] + 20.0
    for i, (x, y) in enumerate(posts):
        pst = Pos(x, y, zt) * cp.shs(20, 2, post_top - zt)
        cut = fuse([dp.hole(8.5, (x, y, z0 + 10), "+y", 30) for z0, _ in tiers])
        add(f"Rack post {i + 1}, 20 x 20 x 2 aluminium tube", pst - cut, "aluminium", group="rack")
    for k, (z0, hy) in enumerate(tiers):
        z1 = z0 + 20
        hxr = 520.0
        vi = hy <= 125      # the top tier's long members are bolted to the posts: vertical leg on the inner side
        mem = [bx(-hxr, hxr, hy - 20, hy, z1 - 2, z1) + (bx(-hxr, hxr, hy - 20, hy - 18, z0, z1) if vi else bx(-hxr, hxr, hy - 2, hy, z0, z1)),
               bx(-hxr, hxr, -hy, -hy + 20, z1 - 2, z1) + (bx(-hxr, hxr, -hy + 18, -hy + 20, z0, z1) if vi else bx(-hxr, hxr, -hy, -hy + 2, z0, z1)),
               bx(hxr - 20, hxr, -hy + 20, hy - 20, z1 - 2, z1) + bx(hxr - 2, hxr, -hy + 20, hy - 20, z0, z1),
               bx(-hxr, -hxr + 20, -hy + 20, hy - 20, z1 - 2, z1) + bx(-hxr, -hxr + 2, -hy + 20, hy - 20, z0, z1)]
        if hy > 125:
            for sy in (-1, 1):
                mem.append(bx(-hxr + 20, hxr - 20, *sorted((sy * 105, sy * 125)), z1 - 2, z1) + bx(-hxr + 20, hxr - 20, *sorted((sy * 105, sy * 107)), z0, z1))
        fr = fuse(mem)
        cut = fuse([dp.hole(8.5, (x, y, z0 + 10), "+y", 30) for (x, y) in posts])
        add(f"Shelf frame, tier {k + 1}, 20 x 20 x 2 aluminium angle, welded", fr - cut, "aluminium", group="rack")
        cloth = bx(-hxr, hxr, -hy, hy, z1, z1 + 2) - fuse([bx(x - 11, x + 11, y - 11, y + 11, z1 - 1, z1 + 3) for (x, y) in posts])
        add(f"Black cotton cloth, tier {k + 1}, soaked in 30 wt % CaCl2 brine", cloth, "canvas", group="rack", color="#1E1E1E")
        for (x, y) in posts:
            sy = 1 if y > 0 else -1
            out += dp.bolt_set(8, (x, sy * 107, z0 + 10), "+y" if sy > 0 else "-y", 22, label=f"tier {k + 1} to post", group="rack")
    # ---- gable plates: 2 mm aluminium, cut and folded, the top edges folded in as glazing flanges; vent doors
    gt = P["gable_t"]
    fl = P["flange"]

    def slope_z(y):
        return Ze + (HY - abs(y)) * tn

    from build123d import Polygon, Plane, extrude
    for sx in (-1, 1):
        xo, xin = sx * (HX + gt), sx * HX
        pts = [(-440, Zb - sa + 4), (440, Zb - sa + 4), (440, Zb), (HY, Zb), (HY, Ze), (0, apex), (-HY, Ze), (-HY, Zb), (-440, Zb)]
        face = Plane.YZ.offset(min(xo, xin)) * Polygon(*pts, align=None)
        plate = extrude(face, amount=gt)
        bbx = plate.bounding_box()
        if bbx.min.X < min(xo, xin) - 0.5:
            plate = extrude(face, amount=-gt)
        flanges = []
        for side in (-1, 1):
            L = HY / math.cos(pa)
            # strip under the glazing plane, from eave (y = side*HY) to apex
            strip = Pos(0, 0, -gt / 2) * Box(fl, L, gt)
            xs = sx * (HX + gt - fl / 2)
            ang = -side * P["pitch"]
            ym, zm = side * HY / 2, (Ze + apex) / 2
            flanges.append(Pos(xs, ym, zm) * Rot(ang, 0, 0) * strip)
        g = fuse([plate] + flanges)
        g = g - bx(min(xo, xin) - 1, max(xo, xin) + 1, -210, 210, Zb + 40, Zb + 160)
        g = g - fuse([dp.hole(9, (xo, y, Zb - 20), "+x", 12) for y in (-350.0, 0.0, 350.0)])
        add(f"Gable plate, {'east' if sx > 0 else 'west'}, 2 mm aluminium, folded glazing flanges", g, "aluminium", group="roof")
        for y in (-350.0, 0.0, 350.0):
            out += dp.bolt_set(8, (xo, y, Zb - 20), "+x" if sx > 0 else "-x", gt + st, label="gable plate", group="roof")
        # vent door, outside the plate, piano hinge on its top edge, two latches
        d0 = xo
        door = bx(*sorted((d0, d0 + sx * 1.5)), -230, 230, Zb + 25, Zb + 170)
        add(f"Vent door, {'east' if sx > 0 else 'west'} gable, 1.5 mm aluminium with EPDM seal", break_edges(door, 0.4), "aluminium", group="roof")
        hinge = Pos(d0 + sx * 4.5, 0, Zb + 173) * Rot(90, 0, 0) * Cylinder(3, 460)
        add(f"Vent door piano hinge, {'east' if sx > 0 else 'west'}, stainless", hinge + bx(*sorted((d0 + sx * 1.5, d0 + sx * 3)), -230, 230, Zb + 160, Zb + 171),
            "stainless", kind="bought", group="roof")
        for y in (-150.0, 150.0):
            lat = bx(*sorted((d0, d0 + sx * 10)), y - 15, y + 15, Zb + 3, Zb + 20) + bx(*sorted((d0 + sx * 1.5, d0 + sx * 6)), y - 4, y + 4, Zb + 20, Zb + 32)
            add(f"Vent door latch, {'east' if sx > 0 else 'west'} ({'north' if y > 0 else 'south'})", lat, "stainless", kind="bought", group="roof")
    # ---- glazed slopes: 4 mm polycarbonate in an aluminium U-channel frame, resting on the gable flanges
    Lp = (HY - 15) / math.cos(pa)
    pt_, pc_ = P["panel_t"], P["pc_t"]
    PX = HX + gt + 4
    riv_uv = [(sx * (HX + gt - 12), v) for sx in (-1, 1) for v in (120.0, Lp - 120)]
    for side, nm in ((-1, "south"), (1, "north")):
        loc = Pos(0, side * HY, Ze) * (Rot(0, 0, 0) if side < 0 else Rot(0, 0, 180)) * Rot(P["pitch"], 0, 0)
        ring = bx(-PX, PX, 0, Lp, 0, pt_) - bx(-PX + 15, PX - 15, 15, Lp - 15, -1, pt_ + 1)
        slot = bx(-PX + 5, PX - 5, 5, Lp - 5, (pt_ - pc_) / 2, (pt_ + pc_) / 2)
        rc = fuse([zcyl(u * (1 if side < 0 else -1), v, -fl, 2.05, pt_ + fl + 2) for (u, v) in riv_uv])
        add(f"Glazing frame, {nm} slope, 12 mm aluminium U-channel", loc * (ring - slot - rc), "aluminium", group="roof")
        add(f"Glazing, {nm} slope, 4 mm UV-stabilized polycarbonate", loc * (slot - rc), "polycarbonate", kind="bought", group="roof")
        for (u, v) in riv_uv:
            uu = u * (1 if side < 0 else -1)
            for q in dp.rivet(4, pt_ + gt, (uu, v, pt_), "+z", label=f"{nm} glazing to gable flange"):
                q["shape"] = loc * q["shape"]; q["group"] = "roof"; out.append(q)
    for q in out:     # rivet holes through the gable flanges
        if q["name"].startswith("Gable plate"):
            for side in (-1, 1):
                loc = Pos(0, side * HY, Ze) * (Rot(0, 0, 0) if side < 0 else Rot(0, 0, 180)) * Rot(P["pitch"], 0, 0)
                q["shape"] = q["shape"] - loc * fuse([zcyl(u * (1 if side < 0 else -1), v, -fl, 2.05, pt_ + fl + 2) for (u, v) in riv_uv])
    # ridge cap: folded 1 mm aluminium over the gap between the slopes, riveted to the south glazing frame
    cw = 45.0
    caps = []
    for side in (-1, 1):
        loc = Pos(0, side * HY, Ze) * (Rot(0, 0, 0) if side < 0 else Rot(0, 0, 180)) * Rot(P["pitch"], 0, 0)
        caps.append(loc * bx(-PX, PX, Lp - cw + 20, Lp + 20, pt_, pt_ + 1))
    add("Ridge cap, 1 mm aluminium, folded", fuse(caps), "aluminium", group="roof")
    # ---- eave condensate channels inside, on the tray rim and frame edge; drains through the east gable
    for sy in (-1, 1):
        ch = bx(-HX + 2, HX - 2, *sorted((sy * 465, sy * HY)), Zb, Zb + 22) - bx(-HX + 3, HX - 3, *sorted((sy * 466, sy * (HY - 1))), Zb + 1, Zb + 23)
        ch = ch - Pos(HX - 2.5, sy * 482, Zb + 12) * Rot(0, 90, 0) * Cylinder(8.5, 3)
        add(f"Eave condensate channel, {'north' if sy > 0 else 'south'}, 1 mm aluminium", ch, "aluminium", group="water")
        fit = Pos(HX + 4.75, sy * 482, Zb + 12) * Rot(0, 90, 0) * (Cylinder(8.0, 14.5) - Cylinder(5.5, 16)) \
            + Pos(HX + 3.5, sy * 482, Zb + 12) * Rot(0, 90, 0) * (Cylinder(12, 3) - Cylinder(8.0, 4))
        add(f"Drain fitting, {'north' if sy > 0 else 'south'} channel, food grade", fit, "hdpe_natural", kind="bought", group="water")
        for q in out:
            if q["name"].startswith("Gable plate, east"):
                q["shape"] = q["shape"] - Pos(HX + 1, sy * 482, Zb + 12) * Rot(0, 90, 0) * Cylinder(8.1, 6)
        bxx, byy = HX + 160, sy * 640.0
        p0, p1, p2 = (HX + 9, sy * 482, Zb + 12), (HX + 70, sy * 482, Zb + 12), (bxx, byy + 40, 380)
        from build123d import Sphere
        tb = tube(p0, p1, 8) + Pos(*p1) * Sphere(8) + tube(p1, p2, 8)
        tb = tb - Pos(HX + 4.75, sy * 482, Zb + 12) * Rot(0, 90, 0) * Cylinder(8.05, 14.5)
        add(f"Drain tube, {'north' if sy > 0 else 'south'}, food-grade silicone", tb, "hdpe_natural", kind="bought", group="water", color="#E8E6DF")
        add(f"Collection jerrycan, {'north' if sy > 0 else 'south'}, 10 L food-grade HDPE", _bottle(bxx, byy), "hdpe_natural", kind="bought", group="water", color="#E9ECEE")
    for sx in (-1, 1):
        add(f"Auger ground anchor with eye ({'east' if sx > 0 else 'west'})", _anchor(sx * (HX + 200), -HY + 18), "galvanised", kind="bought", group="base")
    return out
