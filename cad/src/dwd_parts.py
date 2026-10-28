"""DewDrive helpers for the kit 1.9 model (repo-specific; the kit's own library is .kit/cad_parts.py).

Fastener sets placed along a world axis, button-head and countersunk screws, rivets and wood screws,
each returned as a list of cad_parts.part() dicts so that every bolt, nut, washer, screw and rivet is
its own part. Coordinates in mm.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cone, Cylinder, Pos, Rot, Sphere, Box  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

# Orientation that turns the kit's +Z fastener frame onto a world axis (+ or - direction)
_ROT = {"+x": Rot(0, 90, 0), "-x": Rot(0, -90, 0), "+y": Rot(-90, 0, 0), "-y": Rot(90, 0, 0),
        "+z": Rot(0, 0, 0), "-z": Rot(180, 0, 0)}


def orient(shape, origin, axis):
    """Place a shape built along +Z so that its +Z points along `axis` ('+x', '-y', ...) at origin."""
    return Pos(*origin) * _ROT[axis] * shape


def bolt_set(d, head_face, axis, grip, material="galvanised", group="fixings", label="", explode=(0, 0, 0), nut=True):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut clamping a joint of thickness `grip`.
    head_face: the point on the joint face under the head; axis: the direction from the joint toward the head
    ('+x' means the head is on the +x side and the nut on the -x side)."""
    out = []
    for nm, sh in cp.hex_bolt_set(d, grip):
        if not nut and "nut" in nm:
            continue
        out.append(part(f"{nm}{', ' + label if label else ''}", orient(sh, head_face, axis), material, kind="fastener",
                        group=group, explode=explode))
    return out


def hex_bolt_only(d, length, head_face, axis, washer=True, material="galvanised", group="fixings", label=""):
    """A bolt into a tapped part or threaded insert (no nut): optional washer under the head."""
    s, k, m, d2, h, p = cp.ISO[d]
    out = []
    off = h if washer else 0.0
    out.append(part(f"M{d}x{length} hex bolt (ISO 4017){', ' + label if label else ''}",
                    orient(Pos(0, 0, off) * cp.hex_bolt(d, length), head_face, axis), material, kind="fastener", group=group))
    if washer:
        out.append(part(f"M{d} washer (ISO 7089){', ' + label if label else ''}", orient(cp.washer(d), head_face, axis),
                        material, kind="fastener", group=group))
    return out


def button_screw(d, length, head_face, axis, material="stainless", group="fixings", label=""):
    """ISO 7380 button-head screw: domed head on the face, shank going into the part (opposite to `axis`)."""
    dk, k = {4: (7.6, 2.2), 5: (9.5, 2.75), 6: (10.5, 3.3)}[d]
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    try:
        head = cp.break_edges(head, k * 0.45)
    except Exception:
        pass
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    return [part(f"M{d}x{length} button-head screw (ISO 7380){', ' + label if label else ''}",
                 orient(head + shank, head_face, axis), material, kind="fastener", group=group)]


def countersunk_screw(d, length, face, axis, material="galvanised", group="fixings", label=""):
    """ISO 10642 countersunk screw: head flush with `face`, head cone inside the part, shank beyond.
    axis points out of the face (away from the part). Returns (parts, cutter for the countersink)."""
    dk = 2.0 * d
    hk = (dk - d) / 2 / math.tan(math.radians(45))
    head = Pos(0, 0, -hk / 2) * Cone(d / 2, dk / 2, hk)
    shank = Pos(0, 0, -(length) / 2) * Cylinder(d / 2, length)
    cut = Pos(0, 0, -hk / 2 + 0.01) * Cone(d / 2 + 0.25, dk / 2 + 0.25, hk + 0.02) + Pos(0, 0, -length / 2) * Cylinder(d / 2 + 0.5, length + 1)
    return ([part(f"M{d}x{length} countersunk screw (ISO 10642){', ' + label if label else ''}",
                  orient(head + shank, face, axis), material, kind="fastener", group=group)],
            orient(cut, face, axis))


def rivet(d, grip, head_face, axis, material="aluminium", group="fixings", label=""):
    """Closed-end blind rivet: dome head on the face, body through the grip plus a set end."""
    dk, k = 2.0 * d, 0.4 * d
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    try:
        head = cp.break_edges(head, k * 0.45)
    except Exception:
        pass
    body = Pos(0, 0, -(grip + d) / 2) * Cylinder(d / 2, grip + d)
    return [part(f"{d} mm closed-end rivet{', ' + label if label else ''}", orient(head + body, head_face, axis),
                 material, kind="fastener", group=group)]


def wood_screw(d, length, head_face, axis, material="stainless", group="fixings", label=""):
    """Countersunk wood screw with its head sitting on the face (pan form, as fitted with a cup washer)."""
    head = Pos(0, 0, 1.5) * Cylinder(d * 0.9, 3.0)
    try:
        head = cp.break_edges(head, 0.8)
    except Exception:
        pass
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    return [part(f"{d} x {length} mm wood screw{', ' + label if label else ''}", orient(head + shank, head_face, axis),
                 material, kind="fastener", group=group)]


def hole(d, origin, axis, depth, both=True):
    """A cylindrical cutter of diameter d along `axis` through `origin` (both ways if both)."""
    c = Pos(0, 0, 0 if both else -depth / 2) * Cylinder(d / 2, depth * (2 if both else 1))
    return orient(c, origin, axis)


def solids(shape):
    """The separate solids of a fused or compound shape, largest first."""
    from build123d import Solid
    try:
        ss = [Solid(q.wrapped) for q in shape.solids()]     # detached copies (no topo_parent), so fillets act on one solid
    except Exception:
        return [shape]
    return sorted(ss, key=lambda s: -s.volume) if ss else [shape]
