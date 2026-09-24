"""Blender side of the project video (storyboard revision 3.1, tools/viz/project_video/storyboard.md).

Explanatory illustration, not evidence. Everything is procedural (no downloaded assets). Six
scenes, each built in its own collection at its own place in world space, each with its own
camera; make_project_video.py renders them one by one (with 6 frames of overlap on each side for
the 12-frame cross-dissolve) and adds captions, the legend, the end card and the voice.

Data drawn (all read from files, nothing typed in):
  * scene_data.json (tools/viz/export_bank_scene_data.py): the 65 types in flyvis layout order and
    their three layout bands, the 604 real (source, target) cells with sign and total mean
    synapses, and the Mi9 -> T4d offset kernel (scenes 2 and 4; the exam plate in scene 4 is the
    65 x 65 existence table of the same 604 cells);
  * project_data.json (tools/viz/project_video/export_project_video_data.py): the two 30-type banks
    (flyvis restricted, FlyWire), one degree-preserving shuffle of each (harness shuffled_bank,
    seed 0), and per rank 1..4 the real P3 existence margin and the 99 shuffle margins from
    results/genome/c6/checks/flywire_bf_p3/{arm}/per_shuffle_rank{r}.csv (scene 5).
    Pillar and tick heights are margin x one constant, identical for both stacks, zero at the
    baseline; nothing is printed.

Illustrative, not data (as the storyboard asks; listed so nobody reads them as measurements):
  * scene 2: the hypothetical wiring drawn by the wire icosphere; the three "individual column"
    kernels before averaging (the averaged kernel itself is the real Mi9 -> T4d kernel);
  * scene 3: sphere heights, the crossing lines and the ghost copies (no axis, no values);
  * the connection curves' routing around a stack (which disc they join is data; the angle is a
    drawing choice), the tree's shape, and the stacks' disc radius.
  * FlyWire's signs are a placeholder (+1) in its bank, so neither 30-type stack shows signs.

Run (normally via make_project_video.py):
    blender --background --python tools/viz/project_video/build_project_video.py -- \
        --build <dir> [--scenes 1,2,...] [--stills "1:3.5,2:10.0"] [--samples 64] [--percent 100]
"""

import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT.parent / "connectome-seed-data" / "renderings"
BANK_JSON = DATA / "bank_scene" / "scene_data.json"
PROJ_JSON = DATA / "project_video" / "project_data.json"
FONT_FILE = "C:/Windows/Fonts/segoeuisl.ttf"      # Segoe UI Semilight: never bold
FPS = 24
RES = (1920, 1080)
VIEW = "Standard"
BLOOM = (0.65, 0.8, 1.25)       # threshold, size, strength
PAD = 6                                           # frames rendered past each scene edge (dissolve)
SPACING = 400.0                                   # world-x distance between scene sets

# ------------------------------------------------------------------ cues
# Seconds from the start of each scene's voice clip, read off the clips' pause structure (the
# phrase boundaries of the measured rev3 clips; make_project_video.py checks the clip hashes).
CUE = {
    1: dict(goal=0.0, elephant=3.05, lineage=5.28, five=7.96, grammar=9.09, body=11.13,
            operators=13.01, youth=14.74, fitness=17.08, artefact=18.5, tree=19.55),
    2: dict(seed=0.0, rule=1.58, types=3.66, pairs=4.91, where=6.12, sign=6.74, regen=7.78,
            bank=10.18, template=11.05, averaged=13.8),
    3: dict(before=0.0, condition=1.45, cheap=2.87, youth=4.83, expensive=5.9, runs=7.89,
            notmet=9.36, refuted=10.44, under=11.48, paused=13.35, cancelled=14.66),
    4: dict(main=0.0, three=1.97, none=3.46, r21=4.48, which=7.16, lowest=9.83, exam=12.91,
            whatnot=16.33, family=17.37, chosen=19.71),
    5: dict(second=0.0, female=1.35, term=3.43, every=9.09, flyvis=10.78, thirty=11.98,
            neartie=13.57, reading=15.48, flag=17.13),
    6: dict(grammar=0.0, nopass=0.91, youth=2.52, paused=3.13, body=4.02, operators=5.16,
            designed=6.62, notrun=7.48, nothing=8.17, nexxt=11.33, share=12.2, registered=14.22),
}


# ------------------------------------------------------------------ small maths
def clamp01(x):
    return max(0.0, min(1.0, x))


def smooth(x):
    x = clamp01(x)
    return x * x * x * (x * (6 * x - 15) + 10)


def ramp(t, t0, dur=0.6):
    return smooth((t - t0) / dur) if dur > 0 else float(t >= t0)


def window(t, t_in, t_out, fin=0.5, fout=0.5):
    return min(ramp(t, t_in, fin), 1.0 - ramp(t, t_out - fout, fout))


def bump(t, t0, up=0.35, hold=0.6, down=0.8):
    """0 -> 1 -> 0: a single brightening when something is named (not a repeating pulse)."""
    return min(ramp(t, t0, up), 1.0 - ramp(t, t0 + up + hold, down))


def lerp(a, b, u):
    return a + (b - a) * u


def vlerp(a, b, u):
    return Vector(a).lerp(Vector(b), u)


def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


PAL = {k: srgb(v) for k, v in dict(
    bg0="#05070D", bg1="#0B1020", real="#7FA3C8", exc="#FFB36B", inh="#6BB8FF",
    fail="#E5484D", amber="#F5A524", wire="#FFFFFF", text="#E8ECF4", solid="#DCE7F5",
    dim="#6F7887", grey="#8E97A6").items()}


# ------------------------------------------------------------------ materials
class Mat:
    """Emission-only or glassy (Principled + emission) material with alpha, strength, colour
    controls. Every animated value goes through set(), which also feeds the frame hash."""
    all = []

    def __init__(self, name, rgb, strength=1.0, alpha=1.0, solid=False, blended=False):
        m = bpy.data.materials.new(name)
        if blended:
            m.surface_render_method = "BLENDED"
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        mix = nt.nodes.new("ShaderNodeMixShader")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        if solid:
            sh = nt.nodes.new("ShaderNodeBsdfPrincipled")
            sh.inputs["Roughness"].default_value = 0.35
            self.col_in = [sh.inputs["Base Color"], sh.inputs["Emission Color"]]
            self.str_in = sh.inputs["Emission Strength"]
        else:
            sh = nt.nodes.new("ShaderNodeEmission")
            self.col_in = [sh.inputs["Color"]]
            self.str_in = sh.inputs["Strength"]
        nt.links.new(tr.outputs[0], mix.inputs[1])
        nt.links.new(sh.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs["Surface"])
        self.solid, self.m, self.mix = solid, m, mix
        self.rgb0, self.s0, self.a0 = rgb, strength, alpha
        self.vals = None
        self.set(alpha, strength, rgb)
        Mat.all.append(self)

    def set(self, alpha=None, strength=None, rgb=None):
        a = self.a0 if alpha is None else alpha
        s = self.s0 if strength is None else strength
        c = self.rgb0 if rgb is None else rgb
        v = (round(a, 4), round(s, 4), tuple(round(x, 4) for x in c))
        if v == self.vals:
            return
        self.vals = v
        self.mix.inputs[0].default_value = a
        self.str_in.default_value = s
        for i, inp in enumerate(self.col_in):
            k = 0.18 if (self.solid and i == 0) else 1.0
            inp.default_value = (c[0] * k, c[1] * k, c[2] * k, 1.0)

    def reset(self):
        self.set(self.a0, self.s0, self.rgb0)


# ------------------------------------------------------------------ geometry helpers
FONT = None


def link(ob, coll):
    coll.objects.link(ob)
    return ob


def mesh_obj(name, coll, bm, mat, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat.m)
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    return link(ob, coll)


def hex_prism_bm(r, h, bm=None, center=(0, 0, 0), z0=0.0):
    bm = bm or bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r, radius2=r, depth=h,
                          matrix=Matrix.Translation((center[0], center[1], z0 + h / 2)))
    return bm


def box_bm(sx, sy, sz, center=(0, 0, 0), bm=None):
    bm = bm or bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(center) @
                          Matrix.Diagonal((sx, sy, sz, 1.0)))
    return bm


def hex_ring_bm(r, z=0.0, bm=None, center=(0, 0)):
    bm = bm or bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=6, radius=r,
                            matrix=Matrix.Translation((center[0], center[1], z)))
    return bm


def wire(ob, thick):
    md = ob.modifiers.new("wire", "WIREFRAME")
    md.thickness = thick
    md.use_replace = True
    md.use_even_offset = True
    return ob


def curve_obj(name, coll, splines, bevel, mats, mat_idx=None, radii=None, res=2):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = bevel
    cu.bevel_resolution = res
    cu.use_fill_caps = True
    cu.bevel_factor_mapping_start = "SPLINE"
    cu.bevel_factor_mapping_end = "SPLINE"
    for m in mats:
        cu.materials.append(m.m)
    for i, pts in enumerate(splines):
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for j, p in enumerate(pts):
            sp.points[j].co = (p[0], p[1], p[2], 1.0)
            if radii is not None:
                sp.points[j].radius = radii[i]
        if mat_idx is not None:
            sp.material_index = mat_idx[i]
    ob = bpy.data.objects.new(name, cu)
    return link(ob, coll)


def set_curve_points(ob, splines):
    for sp, pts in zip(ob.data.splines, splines):
        for j, p in enumerate(pts):
            sp.points[j].co = (p[0], p[1], p[2], 1.0)


def qbez(p0, p1, c, n=18):
    p0, p1, c = np.asarray(p0, float), np.asarray(p1, float), np.asarray(c, float)
    s = np.linspace(0, 1, n)[:, None]
    return (1 - s) ** 2 * p0 + 2 * s * (1 - s) * c + s ** 2 * p1


def circle_pts(r, n=72, z=0.0, a0=0.0, frac=1.0):
    return [(r * math.cos(a0 + 2 * math.pi * frac * i / n), r * math.sin(a0 + 2 * math.pi * frac * i / n), z)
            for i in range(n + 1)]


def dashes(p0, p1, n, fill=0.5):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    out = []
    for i in range(n):
        a = i / n
        b = a + fill / n
        out.append([tuple(p0 + (p1 - p0) * a), tuple(p0 + (p1 - p0) * b)])
    return out


def text(name, coll, body, size, mat, loc, cam, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    if FONT:
        cu.font = FONT
    cu.materials.append(mat.m)
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    c = ob.constraints.new("COPY_ROTATION")
    c.target = cam
    return link(ob, coll)


def empty(name, coll, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    ob.location = loc
    return link(ob, coll)


def parent(ch, par):
    ch.parent = par
    ch.matrix_parent_inverse = Matrix.Identity(4)


def pause_glyph(name, coll, mat, loc, size, cam):
    """Two thin emissive bars facing the camera."""
    root = empty(name, coll, loc)
    c = root.constraints.new("COPY_ROTATION")
    c.target = cam
    bm = bmesh.new()
    for dx in (-0.22, 0.22):
        box_bm(0.16 * size, 0.7 * size, 0.02 * size, center=(dx * size, 0, 0), bm=bm)
    ob = mesh_obj(name + "_bars", coll, bm, mat)
    parent(ob, root)
    return root


def seal_ring(name, coll, mat, radius, bevel, loc=(0, 0, 0), n=96, a0=-math.pi / 2):
    """The seal: a ring that closes (bevel_factor_end 0 -> 1) plus a small clasp diamond at the
    closing point. Meaning, for the whole film: written before the run."""
    ring = curve_obj(name, coll, [circle_pts(radius, n, 0.0, a0)], bevel, [mat])
    ring.location = loc
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=bevel * 4.5, radius2=0.0,
                          depth=bevel * 5, matrix=Matrix.Translation((0, 0, bevel * 2.5)))
    bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0.0, radius2=bevel * 4.5,
                          depth=bevel * 5, matrix=Matrix.Translation((0, 0, -bevel * 2.5)))
    clasp = mesh_obj(name + "_clasp", coll, bm, mat)
    clasp.location = (loc[0] + radius * math.cos(a0), loc[1] + radius * math.sin(a0), loc[2])
    return ring, clasp


def look_at(cam, target):
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def hex_lattice(extent):
    pts = []
    for q in range(-extent, extent + 1):
        for r in range(-extent, extent + 1):
            if abs(q + r) <= extent:
                pts.append((q, r, max(abs(q), abs(r), abs(q + r))))
    return pts


def hex_xy(q, r, s):
    return (s * 1.5 * q, s * math.sqrt(3) * (r + q / 2))


def flyvis_xy(du, dv, s):
    # flyvis/utils/hex_utils.py:70-71 (mode "default"), as in export_bank_scene_data.py
    return (s * 1.5 * dv, -s * math.sqrt(3) * (du + dv / 2))


def show(ob, v):
    ob.hide_render = not v


# ------------------------------------------------------------------ shared builders
S2_END_AZ = 0.0          # scene 2: a quarter orbit, from -90 to 0 degrees
SLAB_Y, GATE_Y, TREE_Y, TREE_H = 4.0, 11.0, 13.8, 2.3
SLAB_NAMES = ["grammar", "body + brain", "operators", "youth", "fitness"]
SLAB_STATE = {"grammar": "solid", "body + brain": "wire", "operators": "wire", "youth": "dim",
              "fitness": "wire"}
WIRE_ALPHA = 0.32          # "about 15 %" in the storyboard; raised so wire reads at 1080p
WIRE_STRENGTH = 1.6


class Slabs:
    """The five points as five upright slabs in their three states (solid / dim + pause / wire)."""

    def __init__(self, coll, cam, origin, y=5.0, gap=2.25, w=1.45, h=2.4, labels=True):
        self.obs, self.mats, self.glyph, self.labels, self.base = {}, {}, None, {}, {}
        self.h = h
        for i, n in enumerate(SLAB_NAMES):
            x = (i - 2) * gap
            st = SLAB_STATE[n]
            loc = Vector(origin) + Vector((x, y, 0))
            self.base[n] = loc.copy()
            if st == "solid":
                m = Mat(f"slab_{n}", PAL["solid"], 2.2, solid=True)
            elif st == "dim":
                m = Mat(f"slab_{n}", PAL["dim"], 0.2, solid=True)
            else:
                m = Mat(f"slab_{n}", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
            ob = mesh_obj(f"slab_{n}", coll, box_bm(w, 0.12, h, center=(0, 0, h / 2)), m, loc)
            if st == "wire":
                wire(ob, 0.022)
            self.obs[n], self.mats[n] = ob, m
            if labels:
                lm = Mat(f"slablab_{n}", PAL["text"], 0.75)
                self.labels[n] = (text(f"lab_{n}", coll, n, 0.44, lm, loc + Vector((0, 0, h + 0.5)),
                                       cam), lm)
            if st == "dim":
                gm = Mat("pause_glyph", PAL["text"], 0.9)
                self.glyph = (pause_glyph("pause", coll, gm, loc + Vector((0, -0.25, h * 0.5)),
                                          0.9, cam), gm)

    def centre(self, n):
        return self.base[n] + Vector((0, 0, self.h / 2))

    def set(self, n, rise=1.0, hi=0.0, alpha=1.0, label=None):
        """rise: 0..1 growth from the ground; hi: 0..1 brightening when named; alpha: fade."""
        ob, m = self.obs[n], self.mats[n]
        st = SLAB_STATE[n]
        ob.scale = (1.0, 1.0, max(rise, 1e-3))
        show(ob, rise > 0.002 and alpha > 0.003)
        if st == "solid":
            m.set(alpha, 2.2 + 2.5 * hi)
        elif st == "dim":
            m.set(alpha, 0.2 + 1.2 * hi)
        else:
            m.set(alpha * (WIRE_ALPHA + (1 - WIRE_ALPHA) * hi), WIRE_STRENGTH + 1.5 * hi)
        if n in self.labels:
            lo, lm = self.labels[n]
            la = alpha * (rise if label is None else label)
            lm.set(la, 0.75 + 0.9 * hi)
            show(lo, la > 0.003)
        if st == "dim" and self.glyph:
            g, gm = self.glyph
            ga = alpha * clamp01((rise - 0.8) / 0.2)
            gm.set(ga)
            for c in g.children:
                show(c, ga > 0.003)


class Tree:
    """The evolutionary tree: a procedural L-system (trunk + 4 binary levels), wire only."""

    def __init__(self, coll, origin, height=1.9, levels=4):
        segs = [[] for _ in range(levels + 1)]

        def grow(p, d, L, lev):
            q = p + d * L
            segs[lev].append([tuple(p + d * L * k / 6) for k in range(7)])
            if lev == levels:
                return
            for sgn in (-1, 1):
                ang = math.radians(27 + 4 * lev) * sgn
                tw = math.radians(18) * (1 if (lev % 2) else -1) * sgn
                rot = Matrix.Rotation(ang, 3, "Y") @ Matrix.Rotation(tw, 3, "X")
                grow(q, (rot @ Vector(d)).normalized(), L * 0.74, lev + 1)

        grow(Vector(origin), Vector((0, 0, 1)), height, 0)
        self.m = Mat("tree", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
        self.levels = [curve_obj(f"tree_l{i}", coll, s, 0.028 * (0.8 ** i) + 0.008, [self.m])
                       for i, s in enumerate(segs)]
        self.root = Vector(origin)

    def set(self, draw, alpha=1.0):
        """draw: 0..1 over all levels, each level drawn along its length in turn."""
        n = len(self.levels)
        for i, ob in enumerate(self.levels):
            u = clamp01(draw * n - i)
            ob.data.bevel_factor_end = max(u, 1e-4)
            show(ob, u > 0.002 and alpha > 0.003)
        self.m.set(alpha * WIRE_ALPHA * 1.1)


def stack_layout(types, spacing, band_gap, order_groups=("retina", "intermediate", "output")):
    """z of each type's disc, top to bottom: retina, intermediate, output; flyvis order inside."""
    z, zs, prev = 0.0, {}, None
    ordered = [t for g in order_groups for t in sorted((t for t in types if t["group"] == g),
                                                       key=lambda t: t["flyvis_order"])]
    for t in ordered:
        if prev is not None and t["group"] != prev:
            z -= band_gap
        zs[t["name"]] = z
        z -= spacing
        prev = t["group"]
    return ordered, zs


def pair_angle(src, tar):
    h = hashlib.md5(f"{src}->{tar}".encode()).digest()
    return (h[0] * 256 + h[1]) / 65536 * 2 * math.pi


def arc_between(center, z0, z1, a, R, n=16):
    """A connection curve on the outside of a disc stack, from the rim at height z0 to the rim at
    height z1 at azimuth a, bulging outward with the height difference (drawing choice)."""
    cx, cy = center[0], center[1]
    d = np.array([math.cos(a), math.sin(a), 0.0])
    p0 = np.array([cx, cy, z0]) + d * R
    p1 = np.array([cx, cy, z1]) + d * R
    if abs(z1 - z0) < 1e-6:          # self-connection: a small loop outward
        side = np.array([-d[1], d[0], 0.0])
        s = np.linspace(0, 1, n)[:, None]
        ang = 2 * math.pi * s
        return p0 + d * 0.35 * (1 - np.cos(ang)) + side * 0.12 * np.sin(ang)
    c = (p0 + p1) / 2 + d * (0.25 + 0.32 * abs(z1 - z0))
    return qbez(p0, p1, c, n)


# ------------------------------------------------------------------ scene base
class SceneBase:
    k = 0
    lead = 0.3
    fstop = 2.0

    def __init__(self, D, P):
        self.D, self.P = D, P
        self.O = Vector((SPACING * (self.k - 1), 0, 0))
        self.coll = bpy.data.collections.new(f"S{self.k}")
        bpy.context.scene.collection.children.link(self.coll)
        cd = bpy.data.cameras.new(f"cam{self.k}")
        cd.lens = 35
        cd.clip_start, cd.clip_end = 0.1, 300
        cd.dof.use_dof = True
        cd.dof.aperture_fstop = self.fstop
        cd.dof.aperture_blades = 6
        self.cam = link(bpy.data.objects.new(f"cam{self.k}", cd), self.coll)
        L = bpy.data.lights.new(f"rim{self.k}", "AREA")
        L.energy = 20
        L.size = 8
        L.color = (0.75, 0.85, 1.0)
        L.use_shadow = False
        lo = link(bpy.data.objects.new(f"rim{self.k}", L), self.coll)
        lo.location = self.O + Vector((0, 2, 12))
        self.extra = []
        self.build()

    def c(self, name):
        return self.lead + CUE[self.k][name]

    def w(self, *p):
        return self.O + Vector(p)

    def camera(self, loc, target, focus=None, lens=None):
        self.cam.location = loc
        look_at(self.cam, target)
        f = Vector(focus if focus is not None else target)
        self.cam.data.dof.focus_distance = (f - Vector(loc)).length
        if lens:
            self.cam.data.lens = lens
        self.extra += [tuple(round(x, 4) for x in loc), tuple(round(x, 4) for x in target),
                       round(self.cam.data.lens, 3)]


# ================================================================== scene 1
def S1_view(S, u):
    """Top-down onto the disc (u = 0) to the centred, symmetric 3/4 view of disc, slabs and tree."""
    back = smooth((u - 0.68) / 0.32)            # the target stays on the disc while the camera tilts
    dist = lerp(5.0, 27.0, u ** 1.3)
    el = math.radians(lerp(89.0, 30.0, u))
    tgt = S.w(0, lerp(0.0, 5.4, back), lerp(0.25, 0.5, back))
    az = math.radians(-90.0)
    loc = tgt + Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))) * dist
    return loc, tgt


class S1(SceneBase):
    k, lead, fstop = 1, 0.8, 1.2

    def build(self):
        C, cam = self.coll, self.cam
        self.cols = []
        m = Mat("disc_cols", PAL["real"], 1.5, solid=True)
        self.disc_mat = m
        s = 0.3
        for q, r, d in hex_lattice(5):
            x, y = hex_xy(q, r, s)
            ob = mesh_obj(f"col_{q}_{r}", C, hex_prism_bm(s * 0.8, 0.2), m, self.w(x, y, 0))
            ob.rotation_euler = (0, 0, math.radians(30))
            self.cols.append((ob, d))
        assert len(self.cols) == 91
        self.slabs = Slabs(C, cam, self.O, y=SLAB_Y)
        self.tree = Tree(C, self.w(0, TREE_Y, 0.0), height=TREE_H)

    def state(self, t):
        c = self.c
        # disc: centre column ignites, rings grow out by distance
        for ob, d in self.cols:
            t0 = self.lead + 0.15 + (0.0 if d == 0 else 0.9 + d * 0.62)
            e = ramp(t, t0, 0.55)
            ob.scale = (0.25 + 0.75 * e, 0.25 + 0.75 * e, max(e, 1e-3))
            show(ob, e > 0.002)
        self.disc_mat.set(1.0, 1.5)
        # slabs rise one per spoken point, brightening as each is named
        for n, key in zip(SLAB_NAMES, ["grammar", "body", "operators", "youth", "fitness"]):
            t0 = c(key)
            self.slabs.set(n, rise=ramp(t, t0 - 0.2, 0.9), hi=bump(t, t0, 0.3, 0.9, 0.9))
        self.tree.set(ramp(t, c("artefact") - 0.1, 2.0))
        # camera: top-down onto the igniting column, then one eased tilt to a low 3/4 view
        u = clamp01((t - 1.2) / 9.0)
        u = u * u * (3 - 2 * u)
        loc, tgt = S1_view(self, u)
        focus = self.w(0, lerp(0, SLAB_Y, ramp(t, c("grammar") - 1, 2.0)), 1.0)
        self.camera(loc, tgt, focus, lens=30)


# ================================================================== scene 2
class S2(SceneBase):
    k, fstop = 2, 1.6

    def build(self):
        C, cam, D = self.coll, self.cam, self.D
        self.slabs = Slabs(C, cam, self.w(2.25 * 2, 0, 5.2), y=0.0)   # grammar at x = 0
        self.top = self.w(0, 0, 6.4)
        # wire icosphere: the rule (planned: no rule has passed)
        self.ico_m = Mat("ico", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.55)
        self.ico = wire(mesh_obj("ico", C, bm, self.ico_m, self.top), 0.018)
        # hypothetical wiring drawn by the rule (illustrative, wire)
        ring = [self.top + Vector((2.3 * math.cos(a), 0.9 * math.sin(a), -0.35 + 0.45 * math.sin(2 * a)))
                for a in [math.radians(x) for x in (200, 250, 300, 340, 20)]]
        self.hyp_pos = ring
        self.hyp_disc_m = Mat("hyp_disc", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
        self.hyp_discs = []
        for i, p in enumerate(ring):
            ob = wire(mesh_obj(f"hyp_disc{i}", C, hex_ring_bm(0.34), self.hyp_disc_m, p), 0.016)
            ob.rotation_euler = (math.radians(70), 0, 0)
            self.hyp_discs.append(ob)
        pairs = [(0, 1, 1), (1, 3, -1), (4, 2, 1), (2, 0, -1)]
        self.hyp_curves = []
        for i, (a, b, sg) in enumerate(pairs):
            p0, p1 = np.array(ring[a]), np.array(ring[b])
            cc = (p0 + p1) / 2 + np.array([0, -0.4, 0.9])
            mw = Mat(f"hyp_c{i}", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
            ob = curve_obj(f"hyp_c{i}", C, [qbez(p0, p1, cc, 20)], 0.012, [mw])
            self.hyp_curves.append((ob, mw, PAL["exc"] if sg > 0 else PAL["inh"]))
        self.hyp_k_m = Mat("hyp_k", PAL["wire"], WIRE_STRENGTH, WIRE_ALPHA)
        bm = bmesh.new()
        for (a, b, sg) in pairs:
            p = ring[b]
            for (du, dv) in [(0, 0), (0, 1), (1, 0), (1, -1)]:
                x, y = flyvis_xy(du, dv, 0.11)
                hex_ring_bm(0.05, 0.0, bm, center=(p.x - self.O.x + x, p.z + y))
        kob = mesh_obj("hyp_k", C, bm, self.hyp_k_m)
        kob.rotation_euler = (math.radians(90), 0, 0)
        kob.location = self.O + Vector((0, ring[0].y - 0.08, 0))
        self.hyp_k = wire(kob, 0.01)
        # streams: thin lines from the sphere to each element (drawn along their length)
        self.stream_m = Mat("stream", PAL["wire"], 1.2, 0.25)
        self.streams = curve_obj("streams", C, [qbez(self.top, p, (self.top + p) / 2 + Vector((0, 0, 0.3)), 10)
                                                for p in ring], 0.006, [self.stream_m])
        # the real bank: 65 stacked discs, three bands, 604 curves
        types = D["types"]
        self.ordered, zs = stack_layout(types, 0.125, 0.55)
        ztop = -0.8
        self.zs = {n: self.O.z + ztop + z for n, z in zs.items()}
        self.axis = self.w(0, 0, 0)
        self.disc_m = Mat("bank_discs", PAL["real"], 1.1, 0.5, solid=True)
        bm = bmesh.new()
        for tt in self.ordered:
            hex_prism_bm(1.05, 0.03, bm, center=(0, 0), z0=self.zs[tt["name"]] - self.O.z)
        self.discs = mesh_obj("bank_discs", C, bm, self.disc_m, self.O)
        R = 1.05
        spl, idx, rad = [], [], []
        for cell in D["real"]:
            spl.append(arc_between(self.O, self.zs[cell["src"]], self.zs[cell["tar"]],
                                   pair_angle(cell["src"], cell["tar"]), R))
            idx.append(0 if cell["sign"] > 0 else 1)
            rad.append(0.35 + 0.35 * math.log1p(cell["n_syn_total"]))
        assert len(spl) == 604
        self.exc_m = Mat("bank_exc", PAL["exc"], 1.3, 0.75)
        self.inh_m = Mat("bank_inh", PAL["inh"], 1.3, 0.75)
        self.curves = curve_obj("bank_curves", C, spl, 0.0085, [self.exc_m, self.inh_m], idx, rad)
        fc = next(i for i, x in enumerate(D["real"]) if (x["src"], x["tar"]) == ("Mi9", "T4d"))
        self.focus_m = Mat("focus_curve", PAL["inh"] if D["real"][fc]["sign"] < 0 else PAL["exc"], 4.0)
        self.focus_curve = curve_obj("focus_curve", C, [spl[fc]], 0.02, [self.focus_m])
        # dotted line from the icosphere down to the bank
        self.dot_m = Mat("dots", PAL["wire"], 1.4, 0.55)
        self.dots = curve_obj("dots", C, dashes(self.top - Vector((0, 0, 0.6)),
                                                self.w(0, 0, ztop + 0.25), 16, 0.45), 0.012, [self.dot_m])
        # column averaging, shown on Mi9 -> T4d: an enlarged T4d lattice beside the stack
        az = math.radians(S2_END_AZ)                      # the lattice faces the end camera
        right = Vector((-math.sin(az), math.cos(az), 0))      # camera-right at the end
        zt4 = self.zs["T4d"]
        self.lat_c = Vector((self.O.x, self.O.y, zt4 + 1.4)) + right * 3.7
        self.lat_root = empty("lat_root", C, self.lat_c)
        self.lat_root.rotation_euler = (math.radians(74), 0, az + math.pi / 2)
        self.lat_m = Mat("lat", PAL["real"], 0.9, 0.55)
        s = 0.34
        bm = bmesh.new()
        self.lat_cols = [hex_xy(q, r, s) for q, r, d in hex_lattice(2)]
        for x, y in self.lat_cols:
            hex_ring_bm(s * 0.92, 0.0, bm, center=(x, y))
        lat = wire(mesh_obj("lat", C, bm, self.lat_m), 0.014)
        parent(lat, self.lat_root)
        self.lat = lat
        self.lead_m = Mat("leader", PAL["real"], 1.0, 0.5)
        rim = Vector((self.O.x, self.O.y, zt4)) + right * 1.05
        self.leader = curve_obj("leader", C, [[tuple(rim), tuple(self.lat_c - right * 1.05 - Vector((0, 0, 0.3)))]],
                                0.008, [self.lead_m])
        kern = D["focus"]["kernel"]
        nmax = max(o["n_syn"] for o in kern["offsets"])
        kcol = PAL["inh"] if kern["sign"] < 0 else PAL["exc"]
        ks = s * 0.40

        def kernel_bm(scale_n, bm=None, at=(0, 0), k=ks):
            bm = bm or bmesh.new()
            for o, f in zip(kern["offsets"], scale_n):
                x, y = flyvis_xy(o["du"], o["dv"], k)
                r = k * 0.95 * (0.35 + 0.65 * math.sqrt(min(1.0, o["n_syn"] * f / nmax)))
                hex_prism_bm(r, 0.02, bm, center=(at[0] + x, at[1] + y))
            return bm

        rng = np.random.default_rng(3)            # illustrative jitter of "individual" kernels
        self.indiv = []
        starts = [(-2, 1), (1, -2), (2, 0)]
        for i, (q, r) in enumerate(starts):
            mi = Mat(f"indiv{i}", kcol, 1.1, 0.45)
            ob = mesh_obj(f"indiv{i}", C, kernel_bm(rng.uniform(0.55, 1.45, len(kern["offsets"]))), mi)
            parent(ob, self.lat_root)
            self.indiv.append((ob, mi, Vector((*hex_xy(q, r, s), 0.0))))
        self.avg_m = Mat("avg", kcol, 2.4)
        self.avg = mesh_obj("avg", C, kernel_bm([1.0] * len(kern["offsets"])), self.avg_m)
        parent(self.avg, self.lat_root)
        bm = bmesh.new()
        for x, y in self.lat_cols:
            kernel_bm([1.0] * len(kern["offsets"]), bm, at=(x, y), k=ks * 0.5)
        self.copies_m = Mat("copies", kcol, 1.8)
        self.copies = mesh_obj("copies", C, bm, self.copies_m)
        parent(self.copies, self.lat_root)
        self.copies.location = (0, 0, 0.03)
        lm = Mat("lat_lab", PAL["text"], 0.75)
        self.lat_label = (text("lat_lab", C, "Mi9 \u2192 T4d", 0.42, lm,
                               self.lat_c + Vector((0, 0, 1.55)), cam), lm)

    def state(self, t):
        c = self.c
        # the grammar slab slides forward and folds into the wire icosphere
        fold = ramp(t, c("seed") + 0.2, 1.4)
        for n in SLAB_NAMES:
            if n == "grammar":
                continue
            self.slabs.set(n, alpha=1.0 - ramp(t, 0.1, 0.8))
        gs = self.slabs.obs["grammar"]
        gs.location = self.slabs.base["grammar"] + Vector((0, -1.2 * fold, 0.0))
        gs.scale = (1 - 0.85 * fold, 1.0, max(1 - 0.8 * fold, 1e-3))
        self.slabs.set("grammar", rise=1 - 0.8 * fold, alpha=1 - ramp(t, c("seed") + 1.0, 0.6))
        gs.location = self.slabs.base["grammar"] + Vector((0, -1.2 * fold, 1.0 * fold))
        ico = ramp(t, c("seed") + 1.0, 0.8)
        self.ico.scale = (max(ico, 1e-3),) * 3
        self.ico.rotation_euler = (0.3, 0.0, 0.25 * t)
        self.ico_m.set(WIRE_ALPHA * ico * (1 + 0.8 * bump(t, c("rule"), 0.3, 1.0, 0.8)))
        show(self.ico, ico > 0.002)
        # four beats of hypothetical wiring (all wire)
        ty = ramp(t, c("types"), 0.7)
        for ob in self.hyp_discs:
            ob.scale = (max(ty, 1e-3),) * 3
            show(ob, ty > 0.002)
        self.hyp_disc_m.set(WIRE_ALPHA * 1.3)
        pc = ramp(t, c("pairs"), 0.9)
        sg = ramp(t, c("sign"), 0.6)
        for ob, mw, col in self.hyp_curves:
            ob.data.bevel_factor_end = max(pc, 1e-4)
            show(ob, pc > 0.002)
            mw.set(0.35 + 0.4 * sg, WIRE_STRENGTH, tuple(lerp(a, b, sg) for a, b in zip(PAL["wire"], col)))
        wh = ramp(t, c("where"), 0.6)
        self.hyp_k_m.set(WIRE_ALPHA * 1.6 * wh)
        show(self.hyp_k, wh > 0.002)
        st = max(ramp(t, c("types"), 1.2), 0)
        self.streams.data.bevel_factor_end = max(st, 1e-4)
        self.stream_m.set(0.25 * st * (1 - 0.6 * ramp(t, c("regen"), 1.0)))
        show(self.streams, st > 0.002)
        # the bank below, solid; revealed as the camera comes down
        rv = ramp(t, c("regen") - 0.2, 1.4)
        self.disc_m.set(0.5 * rv, 1.1)
        show(self.discs, rv > 0.002)
        dr = ramp(t, c("regen") + 0.3, 2.2)
        self.curves.data.bevel_factor_end = max(dr, 1e-4)
        show(self.curves, dr > 0.002)
        fk = window(t, c("template") - 0.3, 99, 0.6, 0.5)
        self.exc_m.set(0.75 * (1 - 0.55 * fk))
        self.inh_m.set(0.75 * (1 - 0.55 * fk))
        self.focus_m.set(fk)
        show(self.focus_curve, fk > 0.002)
        dt = ramp(t, c("regen"), 1.2)
        self.dots.data.bevel_factor_end = max(dt, 1e-4)
        self.dot_m.set(0.55 * dt)
        show(self.dots, dt > 0.002)
        # column averaging: separate kernels hover over separate columns, merge, then the one
        # averaged kernel is copied onto every column
        la = ramp(t, c("template") - 0.3, 0.6)
        self.lat_m.set(0.55 * la)
        self.lead_m.set(0.5 * la)
        show(self.lat, la > 0.002)
        self.leader.data.bevel_factor_end = max(la, 1e-4)
        show(self.leader, la > 0.002)
        lo, lm = self.lat_label
        lm.set(la)
        show(lo, la > 0.002)
        t_ind = c("template") + 0.2
        mg = ramp(t, c("template") + 1.6, 1.1)
        for i, (ob, mi, p0) in enumerate(self.indiv):
            a = ramp(t, t_ind + 0.25 * i, 0.5) * (1 - ramp(t, c("template") + 2.5, 0.4))
            ob.location = p0.lerp(Vector((0, 0, 0)), mg) + Vector((0, 0, 0.35 * (1 - mg) + 0.02))
            mi.set(0.5 * a)
            show(ob, a > 0.002)
        av = ramp(t, c("template") + 2.4, 0.5) * (1 - ramp(t, c("averaged") + 0.6, 0.5))
        self.avg_m.set(av, 2.4)
        show(self.avg, av > 0.002)
        cp = ramp(t, c("averaged") - 0.1, 0.8)
        self.copies_m.set(cp)
        show(self.copies, cp > 0.002)
        # camera: near the rule, then one eased move down to the bank with a quarter orbit
        u = ramp(t, c("regen") - 0.4, 4.8)
        az0 = math.radians(-90)
        az1 = math.radians(S2_END_AZ)
        az = lerp(az0, az1, u)
        el = math.radians(lerp(10, 12, u))
        dist = lerp(9.0, 23.5, u)
        right = Vector((-math.sin(az), math.cos(az), 0))
        tgt = self.w(0, 0, lerp(5.9, -5.9, u)) + right * lerp(0, 1.5, u)
        loc = tgt + Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))) * dist
        focus = self.top.lerp(self.w(0, 0, -4.6), u)
        focus = focus.lerp(self.lat_c, ramp(t, c("template") - 0.8, 1.2))
        self.camera(loc, tgt, focus, lens=35)


# ================================================================== scene 3
class S3(SceneBase):
    k, fstop = 3, 1.4

    def build(self):
        C, cam = self.coll, self.cam
        self.slabs = Slabs(C, cam, self.w(0, 3.5, 0), y=0.0)
        self.rail_m = Mat("rails", PAL["solid"], 2.0, solid=True)
        self.xs = (-2.3, 2.3)
        self.hts = (2.6, 5.0)
        self.rails = []
        for i, (x, h) in enumerate(zip(self.xs, self.hts)):
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.055, radius2=0.055, depth=h,
                                  matrix=Matrix.Translation((0, 0, h / 2)))
            self.rails.append(mesh_obj(f"rail{i}", C, bm, self.rail_m, self.w(x, 0, 0)))
        lm = Mat("rail_lab", PAL["text"], 0.75)
        self.rail_labels = [text("lab_cheap", C, "cheap", 0.36, lm, self.w(self.xs[0], 0, -0.45), cam),
                            text("lab_exp", C, "expensive", 0.36, lm, self.w(self.xs[1], 0, -0.45), cam)]
        self.rail_lab_m = lm
        # six individuals on each rail (illustrative heights: no axis, no values)
        self.zc = [0.35 + 0.38 * i for i in range(6)]
        perm = [2, 0, 4, 1, 5, 3]
        self.ze = [0.55 + 0.8 * perm[i] for i in range(6)]
        self.sph_m = Mat("sph", PAL["solid"], 2.6, solid=True)
        self.sph = []
        for side, zz in ((0, self.zc), (1, self.ze)):
            for i, z in enumerate(zz):
                bm = bmesh.new()
                bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.13)
                self.sph.append((mesh_obj(f"sph{side}{i}", C, bm, self.sph_m,
                                          self.w(self.xs[side], -0.02, z)), side, i))
        self.line_m = Mat("lines", PAL["solid"], 1.2, 0.8)
        self.lines = curve_obj("lines", C, [[tuple(self.w(self.xs[0], 0, self.zc[i])),
                                             tuple(self.w(self.xs[1], 0, self.ze[i]))] for i in range(6)],
                               0.012, [self.line_m])
        # two individuals re-run twice each: ghost copies that drift over their neighbours
        self.ghost_m = Mat("ghosts", PAL["solid"], 1.4, 0.35)
        self.gline_m = Mat("glines", PAL["solid"], 0.8, 0.3)
        self.ghosts = []
        for i, drift in ((1, (1.15, 1.9)), (4, (-1.4, -2.25))):
            for d in drift:
                bm = bmesh.new()
                bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.13)
                ob = mesh_obj(f"ghost{i}_{d}", C, bm, self.ghost_m, self.w(self.xs[1], 0.02, self.ze[i]))
                ln = curve_obj(f"gl{i}_{d}", C, [[tuple(self.w(self.xs[0], 0, self.zc[i])),
                                                  tuple(self.w(self.xs[1], 0, self.ze[i]))]], 0.008,
                               [self.gline_m])
                self.ghosts.append((ob, ln, i, d))
        gm = Mat("pause_big", PAL["text"], 1.0)
        self.pause = (pause_glyph("pause_big", C, gm, self.w(0, -0.8, 2.6), 1.5, cam), gm)

    def state(self, t):
        c = self.c
        # the youth slab comes forward and opens into two rails
        op = ramp(t, c("before") + 0.4, 1.6)
        for n in SLAB_NAMES:
            if n != "youth":
                self.slabs.set(n, alpha=1 - ramp(t, 0.1, 0.8))
        ys = self.slabs.obs["youth"]
        ys.location = self.slabs.base["youth"].lerp(self.w(0, 0, 0), op)
        ys.scale = (lerp(1, 0.2, op), 1, lerp(1, 1.6, op))
        self.slabs.set("youth", rise=lerp(1, 1.6, op), alpha=1 - ramp(t, c("before") + 1.4, 0.6))
        ys.location = self.slabs.base["youth"].lerp(self.w(0, 0, 0), op)
        ys.location.x = self.slabs.base["youth"].x * (1 - op) + self.O.x * op
        g, gm = self.slabs.glyph
        g.location = ys.location + Vector((0, -0.25, 1.2))
        cheap = ramp(t, c("cheap") - 0.4, 0.9)
        exp_ = ramp(t, c("expensive") - 0.2, 0.9)
        for ob, h, e, x in zip(self.rails, self.hts, (cheap, exp_), self.xs):
            ob.scale = (1, 1, max(e, 1e-3))
            show(ob, e > 0.002)
        paused = ramp(t, c("paused") - 0.1, 1.2)
        self.rail_m.set(1.0, lerp(2.0, 0.22, paused), tuple(lerp(a, b, paused) for a, b in zip(PAL["solid"], PAL["dim"])))
        la = max(cheap, 0) * 1.0
        for ob, e in zip(self.rail_labels, (cheap, exp_)):
            show(ob, e > 0.002)
        self.rail_lab_m.set(min(1, la), 0.75)
        for ob, side, i in self.sph:
            e = ramp(t, (c("cheap") if side == 0 else c("expensive")) + 0.3 + 0.12 * i, 0.5)
            ob.scale = (max(e, 1e-3),) * 3
            show(ob, e > 0.002)
        self.sph_m.set(1.0, lerp(2.6, 0.3, paused), tuple(lerp(a, b, paused) for a, b in zip(PAL["solid"], PAL["dim"])))
        ln = ramp(t, c("expensive") + 1.0, 1.0)
        self.lines.data.bevel_factor_end = max(ln, 1e-4)
        show(self.lines, ln > 0.002)
        self.line_m.set(0.8 * (1 - 0.6 * paused))
        gh = ramp(t, c("runs"), 0.8)
        drift = ramp(t, c("runs") + 0.3, 2.6)
        for ob, lnob, i, d in self.ghosts:
            z = self.ze[i] + d * drift
            ob.location = self.w(self.xs[1], 0.03, z)
            ob.scale = (max(gh, 1e-3),) * 3
            show(ob, gh > 0.002)
            set_curve_points(lnob, [[tuple(self.w(self.xs[0], 0, self.zc[i])), tuple(self.w(self.xs[1], 0, z))]])
            show(lnob, gh > 0.002)
        self.ghost_m.set(0.4 * gh * (1 - 0.5 * paused), lerp(1.4, 0.25, paused))
        self.gline_m.set(0.3 * gh * (1 - 0.5 * paused))
        self.extra.append(round(drift, 4))
        pg, pm = self.pause
        pa = ramp(t, c("paused") + 0.4, 0.9)
        pm.set(pa, 1.0)
        for ch in pg.children:
            show(ch, pa > 0.002)
        # camera: one slow push-in across the tangle
        u = ramp(t, 0.0, 15.8)
        loc = self.w(lerp(-1.4, 0.8, u), lerp(-19.0, -15.5, u), lerp(3.4, 3.0, u))
        tgt = self.w(lerp(-0.2, 0.4, u), 0, lerp(1.45, 1.6, u))
        self.camera(loc, tgt, self.w(0.8, 0, 2.5), lens=38)


# ================================================================== scene 4
class S4(SceneBase):
    k, fstop = 4, 1.8

    def build(self):
        C, cam, D = self.coll, self.cam, self.D
        self.slabs = Slabs(C, cam, self.w(2.6, 5.0, 0), y=0.0, labels=True)
        # the exam: a flat solid plate with the bank's 65 x 65 existence table on it
        P = 3.4
        self.P = P
        self.plate_m = Mat("plate", PAL["real"], 0.35, solid=True)
        self.plate = mesh_obj("plate", C, box_bm(P, P, 0.08, center=(0, 0, -0.04)), self.plate_m, self.O)
        names = [t["name"] for t in stack_layout(D["types"], 1, 0)[0]]
        idx = {n: i for i, n in enumerate(names)}
        cell = P * 0.94 / 65
        bm = bmesh.new()
        for x in D["real"]:
            i, j = idx[x["src"]], idx[x["tar"]]
            cx = -P * 0.47 + (j + 0.5) * cell
            cy = P * 0.47 - (i + 0.5) * cell
            bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=cell * 0.42,
                                  matrix=Matrix.Translation((cx, cy, 0.004)))
        self.tiles_m = Mat("tiles", PAL["real"], 2.2)
        self.tiles = mesh_obj("tiles", C, bm, self.tiles_m, self.O)
        self.seal_m = Mat("seal", PAL["solid"], 2.6)
        self.seal, self.clasp = seal_ring("seal", C, self.seal_m, P * 0.77, 0.035, self.w(0, 0, 0.02))
        # three rules, as crystals
        self.cry = []
        for i in range(3):
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.26, radius2=0.0, depth=0.42,
                                  matrix=Matrix.Translation((0, 0, 0.21)))
            bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.0, radius2=0.26, depth=0.42,
                                  matrix=Matrix.Translation((0, 0, -0.21)))
            m = Mat(f"cry{i}", PAL["solid"], 2.6, solid=True)
            ob = mesh_obj(f"cry{i}", C, bm, m)
            self.cry.append((ob, m))
        # rule 1 cracks: two halves (hidden until the crack)
        self.halves = []
        for j, sgn in enumerate((1, -1)):
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.26, radius2=0.0, depth=0.42,
                                  matrix=Matrix.Translation((0, 0, 0.21 * sgn)) @
                                  (Matrix.Identity(4) if sgn > 0 else Matrix.Rotation(math.pi, 4, "X")))
            m = Mat(f"half{j}", PAL["fail"], 2.4, solid=True)
            self.halves.append((mesh_obj(f"half{j}", C, bm, m), m, sgn))
        self.lane_y = (-0.9, 0.0, 0.9)
        self.x_in = -9.5
        self.land1 = self.w(-0.8, -0.9, 0.34)
        self.stop2 = self.w(-4.25, 0.0, 0.62)
        self.land21 = self.w(0.6, 0.6, 1.62)
        # gate arch in rule 2's lane, before the plate
        ax = -3.75
        arch = [(0, -0.7, 0.0), (0, -0.7, 1.0)] + \
            [(0, -0.7 * math.cos(a), 1.0 + 0.7 * math.sin(a)) for a in np.linspace(0, math.pi, 24)][1:] + \
            [(0, 0.7, 0.0)]
        self.arch_m = Mat("arch", PAL["solid"], 1.6)
        self.arch = curve_obj("arch", C, [arch], 0.035, [self.arch_m])
        self.arch.location = self.w(ax, 0, 0)
        self.arch.rotation_euler = (0, 0, math.radians(32))
        # the two layers of rule 2.1's result above the plate
        self.lay = {}
        for key, z, lab in (("where", 0.55, "where pairs sit"), ("which", 1.05, "which pairs connect")):
            m = Mat(f"lay_{key}", PAL["real"], 0.8, 0.12)
            ob = mesh_obj(f"lay_{key}", C, box_bm(P, P, 0.01, center=(0, 0, z)), m, self.O)
            em = Mat(f"lay_edge_{key}", PAL["real"], 1.6, 0.8)
            h = P / 2
            edge = curve_obj(f"lay_edge_{key}", C, [[tuple(self.w(x, y, z)) for x, y in
                                                     ((-h, -h), (h, -h), (h, h), (-h, h), (-h, -h))]],
                             0.012, [em])
            lm = Mat(f"lay_lab_{key}", PAL["text"], 0.75)
            lo = text(f"lay_lab_{key}", C, lab, 0.34, lm, self.w(h + 0.8, -h + 0.2, z), cam, align="LEFT")
            self.lay[key] = (ob, m, edge, em, lo, lm)
        # four ticks on the upper layer; the fourth only half, amber, with a low notch
        self.ticks = []
        for i in range(4):
            x0 = -0.95 + i * 0.62
            pts = [(x0 - 0.14, -P / 2 - 0.05, 1.28), (x0 - 0.02, -P / 2 - 0.05, 1.14),
                   (x0 + 0.22, -P / 2 - 0.05, 1.5)]
            pts = [tuple(self.w(*p)) for p in pts]
            m = Mat(f"tick{i}", PAL["amber"] if i == 3 else PAL["solid"], 2.6)
            ob = curve_obj(f"tick{i}", C, [pts], 0.03, [m])
            self.ticks.append((ob, m))
            if i == 3:                    # the unlit half of the fourth tick, as a dim outline
                self.tick_ghost_m = Mat("tick_ghost", PAL["dim"], 0.6)
                self.tick_ghost = curve_obj("tick_ghost", C, [pts], 0.022, [self.tick_ghost_m])
        x3 = -0.95 + 3 * 0.62
        self.notch_m = Mat("notch", PAL["amber"], 2.4)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=3, radius1=0.07, radius2=0.0, depth=0.1)
        self.notch = mesh_obj("notch", C, bm, self.notch_m, self.w(x3 - 0.02, -P / 2 - 0.05, 1.02))
        self.notch.rotation_euler = (math.pi, 0, 0)
        # the red FAIL frame around rule 2.1's crystal and the plate (a box of 12 edges)
        h, z0, z1 = P / 2 + 0.25, -0.15, 2.2
        cs = [(-h, -h), (h, -h), (h, h), (-h, h)]
        edges = [[(x, y, z0), (x, y, z1)] for x, y in cs]
        for z in (z0, z1):
            edges += [[(cs[i][0], cs[i][1], z), (cs[(i + 1) % 4][0], cs[(i + 1) % 4][1], z)] for i in range(4)]
        self.fail_m = Mat("failframe", PAL["fail"], 3.0)
        self.frame = curve_obj("failframe", C, edges, 0.028, [self.fail_m])
        self.frame.location = self.O + Vector((0, 0, 1.0))
        for sp in self.frame.data.splines:          # pivot at the box centre, so it can close in
            for pt in sp.points:
                pt.co.z -= 1.0
        # regularity numbers: a small faceless plate off to the side, lit from the start
        sp = self.w(-5.6, 2.6, 2.3)
        self.side_c = sp
        self.side_m = Mat("side", PAL["grey"], 1.1, solid=True)
        self.side = mesh_obj("side", C, box_bm(1.0, 0.05, 0.7), self.side_m, sp)
        self.side.rotation_euler = (0, 0, math.radians(-38))
        bm = bmesh.new()
        for i in range(4):
            box_bm(0.62 - 0.1 * (i % 2), 0.02, 0.045, center=(-0.05 * (i % 2), -0.04, 0.2 - i * 0.13), bm=bm)
        self.rows_m = Mat("rows", PAL["solid"], 1.3)
        rows = mesh_obj("rows", C, bm, self.rows_m)
        parent(rows, self.side)
        # the amber thread (no seal) from that plate to rules 2 and 2.1
        self.thread_m = Mat("thread", PAL["amber"], 2.6)
        p_a = np.array(sp) + np.array([0.3, -0.1, -0.2])
        t2 = np.array(self.stop2)
        t21 = np.array(self.land21)
        self.threads = curve_obj("threads", C, [qbez(p_a, t2 + np.array([0, 0, 0.25]),
                                                     (p_a + t2) / 2 + np.array([0, -0.6, 0.9]), 24),
                                                qbez(p_a, t21 + np.array([-0.2, 0, 0.25]),
                                                     (p_a + t21) / 2 + np.array([0, -0.8, 1.6]), 30)],
                                 0.016, [self.thread_m])

    def crystal_pos(self, i, t, t_in, t_arrive):
        y = self.lane_y[i]
        start = self.w(self.x_in, y, 0.9)
        end = [self.land1, self.stop2, self.land21][i]
        u = ramp(t, t_in, t_arrive - t_in)
        p = start.lerp(end, u)
        p.z += 0.35 * math.sin(math.pi * u)
        return p, u

    def state(self, t):
        c = self.c
        for n in SLAB_NAMES:
            if n != "grammar":
                self.slabs.set(n, alpha=0.55 * (1 - ramp(t, 0.1, 1.0)) if n != "youth" else
                               0.8 * (1 - ramp(t, 0.1, 1.0)))
        self.slabs.set("grammar", hi=0.35 + 0.65 * bump(t, c("main") + 0.1, 0.4, 1.2, 1.0))
        # the exam arrives first and is sealed before anything else appears
        ex = ramp(t, 0.15, 0.8)
        self.plate_m.set(ex, 0.35)
        self.tiles_m.set(ex, 2.2)
        show(self.plate, ex > 0.002)
        show(self.tiles, ex > 0.002)
        sl = ramp(t, 0.7, 1.1)
        self.seal.data.bevel_factor_end = max(sl, 1e-4)
        show(self.seal, sl > 0.002)
        lock = ramp(t, 1.8, 0.15)
        flash = bump(t, 1.8, 0.1, 0.05, 0.5)
        emph = bump(t, c("exam"), 0.5, 2.2, 1.0)
        self.seal_m.set(1.0, 2.6 + 6.0 * flash + 2.0 * emph)
        self.clasp.scale = (max(lock, 1e-3),) * 3
        show(self.clasp, lock > 0.002)
        # regularity plate: lit from the start (before the crystals form)
        sd = ramp(t, 0.2, 0.8)
        self.side_m.set(sd, 1.1 + 1.0 * bump(t, c("whatnot"), 0.4, 2.0, 1.0))
        self.rows_m.set(sd)
        show(self.side, sd > 0.002)
        for ch in self.side.children:
            show(ch, sd > 0.002)
        # crystals: one per beat
        t_in = [c("three") - 0.1, c("three") + 0.45, c("three") + 1.0]
        t_arr = [c("none") + 0.35, c("none") + 0.95, c("r21") + 0.8]
        for i, (ob, m) in enumerate(self.cry):
            p, u = self.crystal_pos(i, t, t_in[i], t_arr[i])
            ob.location = p
            ob.rotation_euler = (0, 0, 0.6 * t + i)
            a = ramp(t, t_in[i], 0.4)
            show(ob, a > 0.002)
            if i == 0:
                red = ramp(t, t_arr[0], 0.25)
                crack = ramp(t, t_arr[0] + 0.35, 0.5)
                m.set(a, 2.6, tuple(lerp(x, y, red) for x, y in zip(PAL["solid"], PAL["fail"])))
                show(ob, a > 0.002 and crack < 0.01)
                for hob, hm, sgn in self.halves:
                    hob.location = p + Vector((0.12 * sgn * crack, -0.05 * sgn * crack, 0.1 * sgn * crack - 0.06 * crack))
                    hob.rotation_euler = (0.5 * sgn * crack, 0.3 * crack, 0.6 * t)
                    hm.set(1.0, lerp(2.4, 0.9, ramp(t, t_arr[0] + 1.2, 1.5)))
                    show(hob, crack >= 0.01)
            elif i == 1:
                dim = ramp(t, t_arr[1] + 0.35, 0.8)
                m.set(a, lerp(2.6, 0.25, dim), tuple(lerp(x, y, dim) for x, y in zip(PAL["solid"], PAL["dim"])))
            else:
                m.set(a, 2.6)
        arch_red = ramp(t, t_arr[1] - 0.05, 0.3)
        self.arch_m.set(ramp(t, c("three") + 0.2, 0.6),
                        1.6 + 1.2 * arch_red, tuple(lerp(x, y, arch_red) for x, y in zip(PAL["solid"], PAL["fail"])))
        # rule 2.1 on the plate: two layers; "where" turns red, "which" fills four ticks
        ly = ramp(t, t_arr[2] + 0.1, 0.7)
        red = ramp(t, c("r21") + 1.6, 0.6)
        for key, (ob, m, edge, em, lo, lm) in self.lay.items():
            show(ob, ly > 0.002)
            show(edge, ly > 0.002)
            show(lo, ly > 0.002)
            lm.set(ly)
            if key == "where":
                m.set(ly * lerp(0.12, 0.2, red), 0.8 + 0.2 * red, tuple(lerp(x, y, red) for x, y in zip(PAL["real"], PAL["fail"])))
                em.set(0.8 * ly, 1.6 + 1.0 * red, tuple(lerp(x, y, red) for x, y in zip(PAL["real"], PAL["fail"])))
            else:
                m.set(ly * 0.2, 1.2)
                em.set(ly, 2.2)
        for i, (ob, m) in enumerate(self.ticks):
            t0 = c("which") + 0.55 + 0.45 * i if i < 3 else c("lowest") + 0.2
            d = ramp(t, t0, 0.45)
            ob.data.bevel_factor_end = max(d * (0.5 if i == 3 else 1.0), 1e-4)
            show(ob, d > 0.002)
            m.set(1.0, 2.6)
        tg = ramp(t, c("lowest") + 0.2, 0.45)
        show(self.tick_ghost, tg > 0.002)
        self.tick_ghost_m.set(tg, 0.6)
        nt = ramp(t, c("lowest") + 0.7, 0.4)
        self.notch.scale = (max(nt, 1e-3),) * 3
        show(self.notch, nt > 0.002)
        fr = ramp(t, c("lowest") + 1.6, 0.9)          # the frame closes in around crystal and plate
        self.frame.scale = (lerp(1.12, 1.0, fr),) * 3
        show(self.frame, fr > 0.002)
        self.fail_m.set(fr, 3.0)
        # "what was not": the amber thread, no seal
        th = ramp(t, c("whatnot") + 0.2, 1.6)
        self.threads.data.bevel_factor_end = max(th, 1e-4)
        show(self.threads, th > 0.002)
        # camera: tracks slowly left to right with the crystals
        u = ramp(t, 0.0, 13.0)
        u2 = ramp(t, c("whatnot") - 0.5, 3.0)
        loc = self.w(lerp(-9.0, -5.2, u) - 0.6 * u2, lerp(-8.4, -9.6, u) - 0.8 * u2, lerp(4.6, 5.0, u) + 0.3 * u2)
        tgt = self.w(lerp(-3.2, -0.6, u) - 0.9 * u2, lerp(0.4, 0.8, u), lerp(1.0, 1.0, u))
        focus = self.w(lerp(-3.0, 0.3, u), 0.0, 0.8)
        self.camera(loc, tgt, focus, lens=32)


# ================================================================== scene 5
class Stack30:
    """A 30-disc stack, kernel footprints on the discs, and connection curves."""

    def __init__(self, name, coll, types, cells, centre, colour, spacing=0.1, R=0.95, tile=0.062):
        self.name, self.centre, self.R = name, Vector(centre), R
        self.ordered, zs = stack_layout(types, spacing, 0.3)
        self.height = -min(zs.values())
        self.z = {n: centre[2] + z for n, z in zs.items()}
        self.disc_m = Mat(f"{name}_discs", PAL["real"], 1.0, 0.45, solid=True)
        bm = bmesh.new()
        for t in self.ordered:
            hex_prism_bm(R, 0.025, bm, center=(0, 0), z0=self.z[t["name"]] - centre[2])
        self.discs = mesh_obj(f"{name}_discs", coll, bm, self.disc_m, self.centre)
        # kernel footprint cap: every column offset (du, dv) used by any connection of this bank,
        # one hex tile each, in three brightness steps by how many connections use it
        cnt = {}
        for c in cells:
            for du, dv, n in c["offsets"]:
                cnt[(du, dv)] = cnt.get((du, dv), 0) + 1
        self.max_offset = max(max(abs(du), abs(dv), abs(du + dv)) for du, dv in cnt)
        tile = 0.105
        bms = [bmesh.new() for _ in range(3)]
        for (du, dv), n in cnt.items():
            x, y = flyvis_xy(du, dv, tile)
            lvl = 0 if n <= 2 else (1 if n <= 10 else 2)
            hex_prism_bm(tile * 0.88, 0.02, bms[lvl], center=(x, y), z0=0.0)
        self.foot_m = []
        self.foot = []
        for lvl, bm in enumerate(bms):
            m = Mat(f"{name}_foot{lvl}", colour, [0.8, 1.6, 3.0][lvl])
            ob = mesh_obj(f"{name}_foot{lvl}", coll, bm, m, self.centre + Vector((0, 0, 0.45)))
            ob.rotation_euler = (0, 0, math.radians(30))
            self.foot_m.append(m)
            self.foot.append(ob)
        self.cells = cells
        self.curve_m = Mat(f"{name}_curves", colour, 1.2, 0.6)
        spl = [arc_between(self.centre, self.z[c["src"]], self.z[c["tar"]], pair_angle(c["src"], c["tar"]), R)
               for c in cells]
        rad = [0.35 + 0.3 * math.log1p(c["n_syn_total"]) for c in cells]
        self.curves = curve_obj(f"{name}_curves", coll, spl, 0.009, [self.curve_m], None, rad)

    def objs(self):
        return [self.discs, self.curves] + self.foot

    def set_foot(self, a):
        for m, ob in zip(self.foot_m, self.foot):
            m.set(a)
            show(ob, a > 0.002)


class S5(SceneBase):
    k, fstop = 5, 2.4

    def build(self):
        C, cam, D, P = self.coll, self.cam, self.D, self.P
        types30 = P["types"]
        self.names30 = {t["name"] for t in types30}
        # the 65-disc bank it starts from (as in scene 2), then 35 discs fade and it shrinks
        self.ordered65, zs65 = stack_layout(D["types"], 0.125, 0.55)
        self.b65_m = Mat("b65", PAL["real"], 1.0, 0.45, solid=True)
        bm_keep, bm_drop = bmesh.new(), bmesh.new()
        spans = []
        for t in self.ordered65:
            keep = t["name"] in self.names30
            bm = bm_keep if keep else bm_drop
            n0 = len(bm.verts)
            hex_prism_bm(1.05, 0.03, bm, center=(0, 0), z0=zs65[t["name"]])
            if keep:
                spans.append((t["name"], n0, len(bm.verts), zs65[t["name"]]))
        self.b65_start = self.w(0, 0, 4.9)
        self.b65_keep = mesh_obj("b65_keep", C, bm_keep, self.b65_m, self.b65_start)
        self.b65_dm = Mat("b65d", PAL["real"], 1.0, 0.45, solid=True)
        self.b65_dropob = mesh_obj("b65_drop", C, bm_drop, self.b65_dm, self.b65_start)
        # the two 30-type stacks (kept apart all scene)
        self.xl, self.xr = -3.9, 3.9
        ztop = 4.6
        self.ztop = ztop
        # shape key: the 30 kept discs close ranks into the 30-type layout (same types, same order)
        _, zs30 = stack_layout(types30, 0.1, 0.3)
        kb = self.b65_keep.shape_key_add(name="basis")
        key = self.b65_keep.shape_key_add(name="packed")
        me = self.b65_keep.data
        for name, a, b, z65 in spans:
            for vi in range(a, b):
                co = me.vertices[vi].co
                key.data[vi].co = (co.x * 0.95 / 1.05, co.y * 0.95 / 1.05, co.z - z65 + zs30[name])
        self.b65_key = key
        fv, fw = P["arms"]["flyvis30"], P["arms"]["flywire30"]
        self.L = Stack30("flyvis30", C, types30, fv["cells"], self.w(self.xl, 0, ztop), PAL["real"])
        self.Rr = Stack30("flywire30", C, types30, fw["cells"], self.w(self.xr, 0, ztop), PAL["real"])
        lm = Mat("stack_lab", PAL["text"], 0.75)
        self.stack_lab_m = lm
        self.lab_l = text("lab_fv", C, "flyvis, same 30 types", 0.34, lm, self.w(self.xl, 0, ztop + 1.25), cam)
        lm2 = Mat("stack_lab2", PAL["text"], 0.75)
        self.stack_lab2_m = lm2
        self.lab_r = text("lab_fw", C, "FlyWire", 0.34, lm2, self.w(self.xr, 0, ztop + 1.25), cam)
        # the 99-shuffle fans behind each stack: ghost copies (wire)
        self.fans = []
        for side, st, arm in ((-1, self.L, fv), (1, self.Rr, fw)):
            bm = bmesh.new()             # each ghost: the stack's outline (a hex prism), wire
            bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=st.R, radius2=st.R, depth=st.height,
                                  matrix=Matrix.Translation((0, 0, -st.height / 2)))
            gob = wire(mesh_obj(f"ghost_{arm is fw}", C, bm, Mat(f"gtmp{side}", PAL["wire"], 1, 0)), 0.03)
            dg = bpy.context.evaluated_depsgraph_get()
            gme = bpy.data.meshes.new_from_object(gob.evaluated_get(dg))
            bpy.data.objects.remove(gob)
            gm = Mat(f"fan{side}", PAL["wire"], 1.2, 0.3, blended=True)
            gme.materials.clear()
            gme.materials.append(gm.m)
            obs = []
            for j in range(99):
                ob = link(bpy.data.objects.new(f"fan{side}_{j}", gme), C)
                obs.append(ob)
            self.fans.append((side, st, obs, gm))
        # the shuffle shown once, on FlyWire's nearest ghost: curves slide to the shuffled
        # targets (harness shuffled_bank, seed 0); in/out bars keep their length
        st = self.Rr
        real = {(c["src"], c["tar"]) for c in fw["cells"]}
        shuf = {tuple(x) for x in fw["shuffle0"]}
        self.demo_pairs = []
        for t in st.ordered:
            s = t["name"]
            rt = sorted(x[1] for x in real if x[0] == s)
            stt = sorted(x[1] for x in shuf if x[0] == s)
            assert len(rt) == len(stt)
            common = set(rt) & set(stt)
            pr = [(x, x) for x in sorted(common)]
            pr += list(zip(sorted(set(rt) - common, key=lambda n: st.z[n]),
                           sorted(set(stt) - common, key=lambda n: st.z[n])))
            self.demo_pairs += [(s, a, b) for a, b in pr]
        self.demo_off = Vector((2.3, 0.9, 0))
        self.demo_c = st.centre + self.demo_off
        self.demo_m = Mat("demo_curves", PAL["wire"], 1.6, 0.55)
        self.demo = curve_obj("demo", C, self.demo_splines(0.0), 0.008, [self.demo_m])
        outd = {t["name"]: 0 for t in st.ordered}
        ind = dict(outd)
        for (s, tt) in real:
            outd[s] += 1
            ind[tt] += 1
        for (s, tt) in shuf:
            outd[s] -= 1
            ind[tt] -= 1
        assert all(v == 0 for v in outd.values()) and all(v == 0 for v in ind.values())
        outd = {t["name"]: 0 for t in st.ordered}
        ind = dict(outd)
        for (s, tt) in real:
            outd[s] += 1
            ind[tt] += 1
        mx = max(max(outd.values()), max(ind.values()))
        bm = bmesh.new()
        for t in st.ordered:
            n = t["name"]
            z = st.z[n] - st.centre.z
            L1 = 0.9 * outd[n] / mx
            L2 = 0.9 * ind[n] / mx
            box_bm(L1, 0.03, 0.06, center=(-st.R - 0.15 - L1 / 2, 0, z + 0.03), bm=bm)
            box_bm(L2, 0.03, 0.06, center=(st.R + 0.15 + L2 / 2, 0, z - 0.03), bm=bm)
        self.bars_m = Mat("degbars", PAL["solid"], 1.8, 0.9)
        self.bars = mesh_obj("degbars", C, bm, self.bars_m, self.demo_c)
        # pillars: per rank, the real margin (bright) beside the 99 shuffle margins (grey ticks),
        # one height scale for both stacks
        allv = [v for a in P["arms"].values() for r in a["ranks"].values() for v in [r["real"]] + r["shuffles"]]
        self.K = 2.0 / max(allv)
        self.base_z = -1.35
        self.pillars = {}
        self.row_x = {}
        for arm, xs in (("flyvis30", self.xl), ("flywire30", self.xr)):
            A = P["arms"][arm]
            bl_m = Mat(f"base_{arm}", PAL["grey"], 1.0, 0.6)
            curve_obj(f"base_{arm}", C, [[tuple(self.w(xs - 1.9, 0, self.base_z)),
                                          tuple(self.w(xs + 1.9, 0, self.base_z))]], 0.008, [bl_m])
            for r in (1, 2, 3, 4):
                x = xs + (r - 2.5) * 1.0
                self.row_x[(arm, r)] = x
                v = A["ranks"][str(r)]["real"]
                pm = Mat(f"pil_{arm}{r}", PAL["solid"], 2.4, solid=True)
                pob = mesh_obj(f"pil_{arm}{r}", C, box_bm(0.17, 0.17, 1.0, center=(0, 0, 0.5)), pm,
                               self.w(x - 0.17, 0, self.base_z))
                bm = bmesh.new()
                for sv in A["ranks"][str(r)]["shuffles"]:
                    box_bm(0.3, 0.12, 0.012, center=(0, 0, sv * self.K), bm=bm)
                sh = A["ranks"][str(r)]["shuffles"]
                box_bm(0.3, 0.1, (max(sh) - min(sh)) * self.K, bm=bm,
                       center=(0, 0.02, (max(sh) + min(sh)) / 2 * self.K))
                tm = Mat(f"band_{arm}{r}", PAL["grey"], 0.9, 0.45)
                tob = mesh_obj(f"band_{arm}{r}", C, bm, tm, self.w(x + 0.14, 0, self.base_z))
                rlm = Mat(f"rlab_{arm}{r}", PAL["text"], 0.7)
                rl = text(f"rlab_{arm}{r}", C, str(r), 0.32, rlm, self.w(x, -0.3, self.base_z - 1.2), cam)
                self.pillars[(arm, r)] = dict(v=v, top=max(A["ranks"][str(r)]["shuffles"]), p=pob, pm=pm,
                                              ticks=tob, tm=tm, lab=rl, lm=rlm, base=bl_m)
        # the seal glyph on each row's rank-1 slot (headline r = 1, fixed before the run)
        self.seals = []
        for arm in ("flyvis30", "flywire30"):
            x = self.row_x[(arm, 1)]
            sm = Mat(f"seal5_{arm}", PAL["solid"], 2.6)
            ring, clasp = seal_ring(f"seal5_{arm}", C, sm, 0.3, 0.02, self.w(x, 0, self.base_z))
            ring.rotation_euler = (math.radians(90), 0, 0)
            ring.location = self.w(x, -0.3, self.base_z - 1.2)
            clasp.location = self.w(x, -0.3, self.base_z - 1.2 - 0.3)
            clasp.rotation_euler = (math.radians(90), 0, 0)
            self.seals.append((ring, clasp, sm))
        # the amber flag on the flyvis rank-1 pillar
        pv = self.pillars[("flyvis30", 1)]
        top = self.base_z + pv["v"] * self.K
        fx = self.row_x[("flyvis30", 1)] - 0.17
        self.flag_m = Mat("flag", PAL["amber"], 2.8)
        self.flag_pole = curve_obj("flagpole", C, [[tuple(self.w(fx, 0, top)), tuple(self.w(fx, 0, top + 0.95))]],
                                   0.018, [self.flag_m])
        bm = bmesh.new()
        v1 = bm.verts.new((0, 0, 0.95))
        v2 = bm.verts.new((0.48, 0, 0.8))
        v3 = bm.verts.new((0, 0, 0.62))
        bm.faces.new((v1, v2, v3))
        self.flag_cloth = mesh_obj("flagcloth", C, bm, self.flag_m, self.w(fx, 0, top))
        self.flag_base = self.w(fx, 0, top)

    def demo_splines(self, e):
        st = self.Rr
        out = []
        for s, a, b in self.demo_pairs:
            za = st.z[a] + (st.z[b] - st.z[a]) * e
            out.append(arc_between(self.demo_c, st.z[s], za, pair_angle(s, a), st.R, 12))
        return out

    def state(self, t):
        c = self.c
        # 65 -> 30: the bank moves left, 35 discs fade, the 30 settle into the flyvis stack
        mv = ramp(t, 0.3, 2.0)
        dr = ramp(t, 0.1, 0.9)
        self.b65_dm.set(0.45 * (1 - dr))
        show(self.b65_dropob, dr < 0.998)
        pos = self.b65_start.lerp(self.w(self.xl, 0, self.ztop), mv)
        sc = lerp(0.55, 1.0, mv)
        self.b65_keep.location = pos
        self.b65_dropob.location = pos
        self.b65_keep.scale = (sc, sc, sc)
        self.b65_dropob.scale = (sc, sc, sc)
        self.b65_key.value = mv
        self.extra.append(round(mv, 4))
        a65 = 1 - ramp(t, 2.1, 0.5)
        self.b65_m.set(0.45 * a65)
        show(self.b65_keep, a65 > 0.002)
        show(self.b65_dropob, a65 > 0.002 and dr < 0.998)
        la = ramp(t, 1.9, 0.6)
        for ob in self.L.objs():
            show(ob, la > 0.002)
        self.L.disc_m.set(0.45 * la)
        self.L.set_foot(la)
        self.L.curve_m.set(0.6 * la)
        self.stack_lab_m.set(la)
        show(self.lab_l, la > 0.002)
        # FlyWire rises on the right
        rr = ramp(t, c("female") - 0.2, 1.4)
        if not hasattr(self, "rr_base"):
            self.rr_base = {ob.name: ob.location.copy() for ob in self.Rr.objs()}
        for ob in self.Rr.objs():
            ob.location = self.rr_base[ob.name] + Vector((0, 0, -2.5 * (1 - rr)))
            show(ob, rr > 0.002)
        self.Rr.disc_m.set(0.45 * rr)
        self.Rr.set_foot(rr)
        self.Rr.curve_m.set(0.6 * rr)
        self.stack_lab2_m.set(rr)
        show(self.lab_r, rr > 0.002)
        # fans of 99 shuffles spread out behind each stack
        fan = ramp(t, c("term") + 0.6, 2.2)
        for side, st, obs, gm in self.fans:
            for j, ob in enumerate(obs):
                # 99 small copies fan out from the stack into three half-rings behind it
                ring = 0 if j < 27 else (1 if j < 60 else 2)
                k0, cnt = [(0, 27), (27, 33), (60, 39)][ring]
                a = math.pi * (0.04 + 0.92 * (j - k0) / (cnt - 1))
                r = [1.75, 2.3, 2.85][ring]
                goal = st.centre + Vector((math.cos(a) * r, 0.25 + math.sin(a) * r, -st.height * 0.62))
                e = smooth(clamp01(fan * 1.7 - 0.7 * j / 98))
                ob.location = st.centre.lerp(goal, e)
                ob.scale = (lerp(1.0, 0.32, e),) * 3
                show(ob, fan > 0.002)
            gm.set(0.3 * fan * (1 - 0.45 * ramp(t, c("every"), 1.5)))
        self.extra.append(round(fan, 4))
        # the one shuffle shown: FlyWire's nearest ghost, rewired; in/out bars unchanged
        dm = ramp(t, c("term") + 1.4, 0.8) * (1 - ramp(t, c("every") + 0.4, 0.8))
        rw = ramp(t, c("term") + 2.8, 2.4)
        self.demo_m.set(0.55 * dm)
        self.bars_m.set(0.9 * dm)
        show(self.demo, dm > 0.002)
        show(self.bars, dm > 0.002)
        if dm > 0.002:
            set_curve_points(self.demo, self.demo_splines(rw))
        self.extra.append(round(rw, 4))
        # the seal lands on the rank-1 slots first, then the pillars rise
        se = ramp(t, c("term") + 4.0, 0.9)
        for ring, clasp, sm in self.seals:
            ring.data.bevel_factor_end = max(se, 1e-4)
            show(ring, se > 0.002)
            lk = ramp(t, c("term") + 4.9, 0.15)
            clasp.scale = (max(lk, 1e-3),) * 3
            show(clasp, lk > 0.002)
            sm.set(1.0, 2.6 + 5.0 * bump(t, c("term") + 4.9, 0.1, 0.05, 0.5))
        rows = ramp(t, c("term") + 3.2, 0.8)
        for (arm, r), q in self.pillars.items():
            q["base"].set(0.6 * rows)
            q["tm"].set(0.55 * rows)
            q["lm"].set(rows)
            show(q["ticks"], rows > 0.002)
            show(q["lab"], rows > 0.002)
            t0 = c("every") + 0.15 * (r - 1) if arm == "flywire30" else c("thirty") + 0.15 * (r - 1)
            g = ramp(t, t0, 1.1)
            q["p"].scale = (1, 1, max(q["v"] * self.K * g, 1e-4))
            show(q["p"], g > 0.002)
        fl = ramp(t, c("neartie") + 0.3, 0.8)
        self.flag_pole.data.bevel_factor_end = max(fl, 1e-4)
        show(self.flag_pole, fl > 0.002)
        cl = ramp(t, c("neartie") + 0.9, 0.5)
        self.flag_cloth.scale = (max(cl, 1e-3), 1, 1)
        show(self.flag_cloth, cl > 0.002)
        # camera: pulls back slowly so both stacks and the flag stay in frame
        u = ramp(t, 0.0, 18.4)
        loc = self.w(lerp(0.3, 0.0, u), lerp(-18.0, -18.8, u), lerp(8.4, 8.6, u))
        tgt = self.w(0, 0.6, lerp(0.9, 0.5, u))
        self.camera(loc, tgt, self.w(0, 0, 1.2), lens=lerp(36, 35, u))


# ================================================================== scene 6
class S6(SceneBase):
    k, fstop = 6, 1.6

    def build(self):
        C, cam, P = self.coll, self.cam, self.P
        self.slabs = Slabs(C, cam, self.O, y=SLAB_Y)
        self.tree = Tree(C, self.w(0, TREE_Y, 0.0), height=TREE_H)
        # red mark on grammar: no rule has passed
        g = self.slabs.base["grammar"]
        self.mark_m = Mat("mark", PAL["fail"], 3.0)
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=0.12)
        self.mark = mesh_obj("mark", C, bm, self.mark_m, g + Vector((0.55, -0.12, 2.2)))
        # the gate: a closed arch between slabs and tree, with an empty number slot
        gy = GATE_Y
        self.gate_m = Mat("gate", PAL["solid"], 1.8)
        hw, hh = 1.35, 2.3
        arch = [(-hw, gy, 0), (-hw, gy, hh)] + [(-hw * math.cos(a), gy, hh + 0.9 * math.sin(a))
                                                 for a in np.linspace(0, math.pi, 24)][1:] + [(hw, gy, 0)]
        bars = [[(x, gy, 0), (x, gy, hh + 0.9 * math.sqrt(max(0, 1 - (x / hw) ** 2)) - 0.05)]
                for x in np.linspace(-hw, hw, 7)[1:-1]]
        self.gate = curve_obj("gate", C, [[tuple(self.w(*p)) for p in arch]] +
                              [[tuple(self.w(*p)) for p in b] for b in bars], 0.03, [self.gate_m])
        self.slot_c = self.w(0, gy - 0.12, hh + 0.35)
        sw, sh = 0.9, 0.42
        self.slot_m = Mat("slot", PAL["solid"], 2.4)
        self.slot = curve_obj("slot", C, [[tuple(self.slot_c + Vector(p)) for p in
                                           ((-sw / 2, 0, -sh / 2), (sw / 2, 0, -sh / 2), (sw / 2, 0, sh / 2),
                                            (-sw / 2, 0, sh / 2), (-sw / 2, 0, -sh / 2))],
                                          [tuple(self.slot_c + Vector((-0.14, -0.02, 0))),
                                           tuple(self.slot_c + Vector((0.14, -0.02, 0)))]], 0.022, [self.slot_m])
        # thin line from the youth slab to the slot
        y0 = self.slabs.base["youth"] + Vector((0, 0, self.slabs.h + 0.05))
        self.yline_m = Mat("yline", PAL["solid"], 1.8, 0.9)
        self.yline = curve_obj("yline", C, [qbez(y0, self.slot_c + Vector((0.45, 0, -0.1)),
                                                 (y0 + self.slot_c) / 2 + Vector((0.3, 0, 1.2)), 24)],
                               0.012, [self.yline_m])
        # generation zero: the tree's root becomes a small solid grey-blue hex prism
        self.root_m = Mat("root", PAL["real"], 2.6, solid=True)
        self.root = mesh_obj("root", C, hex_prism_bm(0.32, 0.3), self.root_m, self.tree.root)
        # the two stacks of scene 5, small and far apart, a dotted bridge with a question mark
        types30 = P["types"]
        self.mini = []
        for x in (-4.3, 4.3):
            m = Mat(f"mini{x}", PAL["real"], 1.1, 0.5, solid=True)
            ordered, zs = stack_layout(types30, 0.06, 0.14)
            bm = bmesh.new()
            for tt in ordered:
                hex_prism_bm(0.42, 0.014, bm, center=(0, 0), z0=zs[tt["name"]])
            ob = mesh_obj(f"mini{x}", C, bm, m, self.w(x, -3.4, 2.1))
            self.mini.append((ob, m))
        lm = Mat("mini_lab", PAL["text"], 0.7)
        self.mini_labs = [text("ml_fv", C, "flyvis", 0.26, lm, self.w(-4.3, -3.4, 2.5), cam),
                          text("ml_fw", C, "FlyWire", 0.26, lm, self.w(4.3, -3.4, 2.5), cam)]
        self.mini_lab_m = lm
        p0, p1 = np.array(self.w(-3.7, -3.4, 1.4)), np.array(self.w(3.7, -3.4, 1.4))
        arcp = qbez(p0, p1, (p0 + p1) / 2 + np.array([0, 0, 1.6]), 40)
        segs = [[tuple(arcp[i]), tuple(arcp[i + 1])] for i in range(0, 39, 2)]
        self.bridge_m = Mat("bridge", PAL["solid"], 1.8)
        self.bridge = curve_obj("bridge", C, segs, 0.018, [self.bridge_m])
        self.q_m = Mat("qmark", PAL["text"], 1.0)
        self.q = text("qmark", C, "?", 1.1, self.q_m, self.w(0, -3.45, 2.95), cam)
        # the sealed plate that lands before the bridge
        self.sp_m = Mat("sp", PAL["real"], 0.6, solid=True)
        self.sp_c = self.w(0, -4.7, 0.35)
        self.splate = mesh_obj("splate", C, box_bm(1.0, 1.0, 0.05), self.sp_m, self.sp_c)
        self.sp_seal_m = Mat("sp_seal", PAL["solid"], 2.6)
        self.sp_seal, self.sp_clasp = seal_ring("sp_seal", C, self.sp_seal_m, 0.72, 0.022, self.sp_c)

    def state(self, t):
        c = self.c
        for n, key in zip(SLAB_NAMES, ["grammar", "body", "operators", "youth", "fitness"]):
            k2 = {"grammar": "grammar", "youth": "youth", "body + brain": "body",
                  "operators": "operators", "fitness": "operators"}[n]
            self.slabs.set(n, hi=bump(t, c(k2) + (0.25 if n == "fitness" else 0.0), 0.3, 0.8, 0.8))
        self.tree.set(1.0)
        mk = ramp(t, c("nopass"), 0.5)
        self.mark.scale = (max(mk, 1e-3),) * 3
        show(self.mark, mk > 0.002)
        ga = ramp(t, c("nothing") - 0.3, 0.9)
        self.gate.data.bevel_factor_end = max(ga, 1e-4)
        show(self.gate, ga > 0.002)
        sl = ramp(t, c("nothing") + 0.4, 0.6)
        self.slot_m.set(sl)
        show(self.slot, sl > 0.002)
        yl = ramp(t, c("nothing") + 1.2, 1.3)
        self.yline.data.bevel_factor_end = max(yl, 1e-4)
        show(self.yline, yl > 0.002)
        rt = ramp(t, c("nothing") + 2.2, 0.8)
        self.root.scale = (max(rt, 1e-3),) * 3
        show(self.root, rt > 0.002)
        ms = ramp(t, c("nexxt") - 0.1, 0.9)
        for ob, m in self.mini:
            m.set(0.5 * ms)
            show(ob, ms > 0.002)
        self.mini_lab_m.set(ms)
        for ob in self.mini_labs:
            show(ob, ms > 0.002)
        br = ramp(t, c("share"), 1.2)
        self.bridge.data.bevel_factor_end = 1.0
        self.bridge_m.set(br)
        show(self.bridge, br > 0.002)
        qa = ramp(t, c("share") + 1.0, 0.5)
        self.q_m.set(qa)
        show(self.q, qa > 0.002)
        land = ramp(t, c("registered") + 0.1, 0.9)
        self.splate.location = self.sp_c + Vector((0, 0, 1.6 * (1 - land)))
        self.sp_m.set(land)
        show(self.splate, land > 0.002)
        ss = ramp(t, c("registered") + 0.8, 0.8)
        self.sp_seal.data.bevel_factor_end = max(ss, 1e-4)
        show(self.sp_seal, ss > 0.002)
        lk = ramp(t, c("registered") + 1.6, 0.15)
        self.sp_clasp.scale = (max(lk, 1e-3),) * 3
        show(self.sp_clasp, lk > 0.002)
        self.sp_seal_m.set(1.0, 2.6 + 5.0 * bump(t, c("registered") + 1.6, 0.1, 0.05, 0.5))
        # camera: the scene-1 view, then one eased pull back that brings the stacks in; hold
        u = ramp(t, c("nothing") - 0.8, 7.5)
        loc0, tgt0 = S1_view(self, 1.0)
        dist = lerp((loc0 - tgt0).length, 31.0, u)
        el = math.radians(lerp(30.0, 30.0, u))
        tgt = tgt0.lerp(self.w(0, 3.8, 1.0), u)
        az = math.radians(-90.0)
        loc = tgt + Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))) * dist
        self.camera(loc, tgt, self.w(0, lerp(SLAB_Y, 1.0, u), 1.2), lens=30)


SCENES = [S1, S2, S3, S4, S5, S6]


# ------------------------------------------------------------------ render setup
def setup_render(samples):
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.fps = FPS
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.image_settings.compression = 15
    e = sc.eevee
    e.taa_render_samples = samples
    e.use_shadows = False
    e.use_raytracing = False
    e.bokeh_max_size = 60
    try:
        sc.view_settings.view_transform = VIEW
        if VIEW == "AgX":
            sc.view_settings.look = "AgX - Medium High Contrast"
    except TypeError as x:
        print("colour management left at default:", x)
    world = bpy.data.worlds.new("world")
    sc.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0, 0, 0, 1)
    bg.inputs["Strength"].default_value = 0.0
    # compositor: faint radial background + bloom (Glare, Bloom mode)
    ng = bpy.data.node_groups.new("comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    N = ng.nodes
    rl = N.new("CompositorNodeRLayers")
    out = N.new("NodeGroupOutput")
    ell = N.new("CompositorNodeEllipseMask")
    ell.inputs["Size"].default_value = (0.95, 1.1)
    blur = N.new("CompositorNodeBlur")
    blur.inputs["Size"].default_value = (360, 360)
    grad = N.new("ShaderNodeMix")
    grad.data_type = "RGBA"
    grad.inputs[6].default_value = (*PAL["bg0"], 1)
    grad.inputs[7].default_value = (*PAL["bg1"], 1)
    add = N.new("ShaderNodeMix")
    add.data_type = "RGBA"
    add.blend_type = "ADD"
    add.inputs[0].default_value = 1.0
    glare = N.new("CompositorNodeGlare")
    glare.inputs["Type"].default_value = "Bloom"
    glare.inputs["Threshold"].default_value = BLOOM[0]
    glare.inputs["Size"].default_value = BLOOM[1]
    glare.inputs["Strength"].default_value = BLOOM[2]
    L = ng.links.new
    L(ell.outputs[0], blur.inputs["Image"])
    L(blur.outputs[0], grad.inputs[0])
    L(rl.outputs["Image"], add.inputs[6])
    L(grad.outputs[2], add.inputs[7])
    L(add.outputs[2], glare.inputs["Image"])
    L(glare.outputs[0], out.inputs[0])
    return sc


def frame_key(S, sc):
    h = hashlib.sha1()
    h.update(repr([m.vals for m in Mat.all]).encode())
    h.update(repr(S.extra).encode())
    for ob in S.coll.all_objects:
        h.update(ob.name.encode())
        h.update(bytes([ob.hide_render]))
        h.update(np.round(np.array(ob.matrix_world), 5).tobytes())
        if ob.type == "CURVE":
            h.update(repr((round(ob.data.bevel_factor_end, 5),)).encode())
    return h.hexdigest()


def activate(scenes, S, sc):
    for o in scenes:
        o.coll.hide_render = o is not S
    sc.camera = S.cam


# ------------------------------------------------------------------ main
def main():
    global FONT
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    def opt(name, default=None):
        return a[a.index(name) + 1] if name in a else default

    build = Path(opt("--build"))
    samples = int(opt("--samples", "64"))
    pct = int(opt("--percent", "100"))
    only = [int(x) for x in opt("--scenes", "1,2,3,4,5,6").split(",")]
    stills = opt("--stills")
    TL = json.loads((build / "timeline.json").read_text(encoding="utf-8"))
    D = json.loads(BANK_JSON.read_text(encoding="utf-8"))
    P = json.loads(PROJ_JSON.read_text(encoding="utf-8"))
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    FONT = bpy.data.fonts.load(FONT_FILE) if Path(FONT_FILE).exists() else None
    sc = setup_render(samples)
    sc.render.resolution_percentage = pct
    scenes = [cls(D, P) for cls in SCENES]
    print(f"built ({time.time() - t0:.1f}s)", flush=True)
    if stills:
        out = build / "stills"
        out.mkdir(parents=True, exist_ok=True)
        for item in stills.split(","):
            k, ts = item.split(":")
            S = scenes[int(k) - 1]
            activate(scenes, S, sc)
            S.extra = []
            S.state(float(ts))
            sc.render.filepath = str(out / f"s{k}_t{float(ts):05.2f}.png")
            bpy.ops.render.render(write_still=True)
            print("still", item, f"({time.time() - t0:.1f}s)", flush=True)
        return
    info = {}
    for k in only:
        S = scenes[k - 1]
        seg = TL["scenes"][k - 1]
        activate(scenes, S, sc)
        # global frame indices, so the cuts sit on the audio timeline without rounding drift
        g0 = int(round(seg["start"] * FPS))
        g1 = int(round(seg["end"] * FPS)) if k < 6 else int(math.ceil(TL["total"] * FPS))
        f_first = g0 - (PAD if k > 1 else 0)
        f_last = g1 + (PAD if k < 6 else 0)
        out = build / "frames" / f"s{k}"
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        prev_key, prev_file, rendered, n = None, None, 0, 0
        for f in range(f_first, f_last):
            S.extra = []
            S.state(f / FPS - seg["start"])
            key = frame_key(S, sc)
            n += 1
            fn = out / f"f_{n:05d}.png"
            if key == prev_key:
                shutil.copyfile(prev_file, fn)
            else:
                sc.render.filepath = str(fn)
                bpy.ops.render.render(write_still=True)
                rendered += 1
                prev_key, prev_file = key, fn
            if n % 48 == 0:
                print(f"S{k} frame {n}/{f_last - f_first} rendered {rendered} ({time.time() - t0:.0f}s)",
                      flush=True)
        info[k] = {"frames": n, "rendered": rendered, "first_frame_offset": f_first}
        (out / "info.json").write_text(json.dumps(info[k]), encoding="utf-8")
    print(f"done ({time.time() - t0:.0f}s): {info}", flush=True)


main()
