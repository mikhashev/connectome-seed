"""Blender animation: the real connectome bank, then the harness's shuffle of it, narrated.

Explanatory video, not evidence. Same data as the static figure (tools/viz/bank_scene.py, which
this script imports for its layout helpers): scene_data.json from export_bank_scene_data.py, i.e.
REAL and shuffled_bank(REAL, seed=0) of results/genome/c6/harness.py. The timeline comes from
<build>/timing.json written by bank_narration.py, so every visual cue hangs on a caption's
start / end time.

What moves, and what that motion does and does not mean:
  * Rewiring: the harness keeps every type's out- and in-degree (double-edge swaps). The video
    draws it as: each type keeps its own outgoing lines and their receiving ends slide around the
    circle to the shuffled targets. Which real line becomes which shuffled line is a drawing
    choice (pairs that exist in both banks stay put; the rest are matched in circle order per
    sending type). The harness does not track lines through the swaps.
  * During rewiring lines are grey (existence only): in the harness the kernels are dealt only
    after the rewiring. Then the colours and widths of the shuffled bank fade in, and the one
    followed kernel (Mi9 -> T4d) is drawn travelling to the cell it was dealt to (Tm9 -> T1).
  * Matrices, degree bars, kernel inset: drawn from the JSON, identical in construction on both
    sides.

Frames whose picture is identical to the previous frame are copied, not re-rendered.

Run (headless; normally via make_bank_video.py):
    "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background \
        --python tools/viz/bank_animation.py -- --build <build_dir> [--data scene_data.json]
        [--stills 3.5,20,...] [--percent 100]
Writes <build>/frames/f_00001.png ... (or <build>/stills/t_<sec>.png with --stills).
"""

import hashlib
import json
import math
import shutil
import sys
import textwrap
import time
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bank_scene as BS          # noqa: E402  (layout helpers; its main() does not run on import)
import bank_video_script as VS   # noqa: E402

FPS = 30
RES = (1920, 1080)
ORTHO = 44.0                      # world units across the frame in the main shot
HALF_H = ORTHO * RES[1] / RES[0] / 2
R = 7.0                           # circle radius
K = R / BS.R_CIRCLE               # scale of the static figure's widths
C = np.array([-9.5, 1.9])         # circle centre
PANEL_X = 12.0                    # right-hand panel centre
MY = -60.0                        # world y of the matrix shot
NPT = 24                          # points per chord
WHITE = np.array([1.0, 1.0, 1.0])
GREY_LINE = np.array([0.52, 0.52, 0.52])
CAPTION_Y = -HALF_H + 1.72
BAR_TOP = -HALF_H + 3.45

COLS = dict(BS.COL)
COLS.update({"text": (0.012, 0.012, 0.012), "text2": (0.07, 0.07, 0.07), "focus_text": (0.80, 0.50, 0.0),
             "bar": (0.45, 0.45, 0.45), "capbar": (0.94, 0.94, 0.94), "rule": (0.75, 0.75, 0.75)})


# ------------------------------------------------------------------ small maths
def clamp01(x):
    return max(0.0, min(1.0, x))


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ramp(t, t0, dur):
    return smooth((t - t0) / dur) if dur > 0 else float(t >= t0)


def window(t, t_in, t_out, fin=0.4, fout=0.4):
    """0 before t_in, fades to 1, fades back to 0 ending at t_out."""
    return min(ramp(t, t_in, fin), 1.0 - ramp(t, t_out - fout, fout))


def wrap(d):
    return (d + math.pi) % (2 * math.pi) - math.pi


# ------------------------------------------------------------------ materials with fade groups
class Mats:
    """Every material belongs to a fade group; per frame its emission colour is
    white + (rgb - white) * visibility(group). The page is white, so this is a fade."""

    def __init__(self):
        self.items = []           # (material, emission node, rgb, group)

    def get(self, group, rgb, name=None):
        m = BS.flat_material(name or f"m_{group}_{len(self.items)}", rgb)
        em = next(n for n in m.node_tree.nodes if n.type == "EMISSION")
        self.items.append([m, em, np.array(rgb, float), group])
        return m

    def bind_objects(self):
        """Remember which objects carry which fade group, to hide them when fully faded (a
        white, faded text would otherwise still cover what lies under it)."""
        group_of = {it[0].name: it[3] for it in self.items}
        self.objs = []
        for ob in bpy.data.objects:
            mats = [s.material for s in ob.material_slots if s.material]
            gs = {group_of[m.name] for m in mats if m and m.name in group_of}
            if len(gs) == 1:
                self.objs.append((ob, gs.pop()))

    def apply(self, vis, override=None):
        for ob, g in self.objs:
            ob.hide_render = vis.get(g, 1.0) < 0.004
        state = []
        for it in self.items:
            m, em, rgb, g = it
            col = (override or {}).get(m.name, rgb)
            v = vis.get(g, 1.0)
            c = WHITE + (np.asarray(col) - WHITE) * v
            em.inputs["Color"].default_value = (*c, 1.0)
            state.append(tuple(np.round(c, 3)))
        return state


def load_fonts():
    f = {}
    for key, fn in [("reg", "segoeui.ttf"), ("bold", "seguisb.ttf")]:
        p = Path("C:/Windows/Fonts") / fn
        f[key] = bpy.data.fonts.load(str(p)) if p.exists() else None
    return f


FONTS = {}


def txt(coll, body, loc, size, mat, align_x="CENTER", rot=0.0, bold=False, align_y="CENTER"):
    ob = BS.text(coll, body, loc, size, mat, align_x=align_x, align_y=align_y, rot=rot)
    fnt = FONTS.get("bold" if bold else "reg")
    if fnt:
        ob.data.font = fnt
    return ob


def disc_mesh(name, coll, centres, radius, mat, segments=16, z=0.0):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for c in centres:
        bmesh.ops.create_circle(bm, cap_ends=True, segments=segments, radius=radius,
                                matrix=Matrix.Translation((c[0], c[1], z)))
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def line_curve(name, coll, mat, pts, r, z=0.0):
    cu = BS.new_curve(name, coll, mat)
    BS.add_spline(cu, [Vector((p[0], p[1], z)) for p in pts], r, r, z)
    return cu


def rect_mesh(name, coll, rects, mat, z=0.0):
    """rects: (x0, y0, x1, y1) each."""
    verts, faces = [], []
    for x0, y0, x1, y1 in rects:
        k = len(verts)
        verts += [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]
        faces.append((k, k + 1, k + 2, k + 3))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


# ------------------------------------------------------------------ chord ribbons (one mesh)
class Ribbons:
    """N ribbons of NPT points each, fixed topology; coordinates and colours set per frame."""

    def __init__(self, name, coll, n, z_of):
        self.n = n
        self.z = np.repeat(np.asarray(z_of, float), 2 * NPT)
        me = bpy.data.meshes.new(name)
        verts = np.zeros((n * 2 * NPT, 3))
        faces = []
        for c in range(n):
            b = c * 2 * NPT
            for i in range(NPT - 1):
                faces.append((b + i, b + i + 1, b + NPT + i + 1, b + NPT + i))
        me.from_pydata(verts.tolist(), [], faces)
        self.attr = me.color_attributes.new("col", "FLOAT_COLOR", "POINT")
        m = bpy.data.materials.new(name + "_mat")
        m.use_nodes = True
        nt = m.node_tree
        for nd in list(nt.nodes):
            nt.nodes.remove(nd)
        at = nt.nodes.new("ShaderNodeAttribute")
        at.attribute_name = "col"
        em = nt.nodes.new("ShaderNodeEmission")
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(at.outputs["Color"], em.inputs["Color"])
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        me.materials.append(m)
        self.me = me
        self.ob = bpy.data.objects.new(name, me)
        coll.objects.link(self.ob)

    def set(self, pts, w0, w1, rgb):
        """pts (n, NPT, 2); w0, w1 (n,) half-widths at the two ends; rgb (n, 3)."""
        d = np.gradient(pts, axis=1)
        L = np.linalg.norm(d, axis=2, keepdims=True)
        nrm = np.stack([-d[..., 1], d[..., 0]], -1) / np.maximum(L, 1e-9)
        s = np.linspace(0, 1, NPT)[None, :, None]
        w = (w0[:, None, None] * (1 - s) + w1[:, None, None] * s)
        left, right = pts + nrm * w, pts - nrm * w
        xy = np.concatenate([left, right], axis=1).reshape(-1, 2)
        co = np.column_stack([xy, self.z]).astype(np.float32)
        self.me.vertices.foreach_set("co", co.ravel())
        col = np.repeat(np.column_stack([rgb, np.ones(len(rgb))]), 2 * NPT, axis=0)
        self.attr.data.foreach_set("color", col.astype(np.float32).ravel())
        self.me.update()
        return hashlib.sha1(np.round(co, 4).tobytes() + np.round(col, 3).tobytes()).hexdigest()


def bez(p0, p1, s):
    c = C + ((p0 + p1) / 2 - C) * 0.15
    s = s[:, None]
    return (1 - s) ** 2 * p0 + 2 * s * (1 - s) * c + s ** 2 * p1


def loop(p, s):
    d = (p - C) / np.linalg.norm(p - C)
    perp = np.array([-d[1], d[0]])
    a = 2 * math.pi * s[:, None]
    return p + d * (0.35 * K) * (1 - np.cos(a)) + perp * (0.18 * K) * np.sin(a)


def on_circle(a):
    return C + R * np.array([math.cos(a), math.sin(a)])


def geom(a_src, a_t0, a_t1, loop0, loop1, e, p=1.0):
    """Chord from the source at angle a_src; its target slides from a_t0 to a_t1 (e in [0,1]);
    loop0 / loop1 say whether the start / end state is a self-loop; p = drawn fraction."""
    s = np.linspace(0, p, NPT)
    ps = on_circle(a_src)
    if not loop0 and not loop1:
        return bez(ps, on_circle(a_t0 + wrap(a_t1 - a_t0) * e), s)
    g0 = loop(ps, s) if loop0 else bez(ps, on_circle(a_t0), s)
    g1 = loop(ps, s) if loop1 else bez(ps, on_circle(a_t1), s)
    return g0 * (1 - e) + g1 * e


def half_width(n_syn):
    return BS.width(n_syn) * K


# ------------------------------------------------------------------ scene build
class Scene:
    def __init__(self, D, timing):
        self.D, self.T = D, timing
        self.cue = {c["id"]: c for c in timing["chunks"]}
        BS.clear_scene()
        FONTS.update(load_fonts())
        self.sc = bpy.context.scene
        self.M = Mats()
        self.coll = {}
        for name in ["circle", "panel", "matrix", "cards", "hud"]:
            c = bpy.data.collections.new(name)
            self.sc.collection.children.link(c)
            self.coll[name] = c
        self.ordered, self.ang, self.step = BS.type_angles(D["types"])
        self.label_objs = {}
        self.build_circle()
        self.build_chords()
        self.build_panel()
        self.build_matrices()
        self.build_cards()
        self.build_camera_and_hud()
        self.setup_render()
        self.M.bind_objects()

    # --- circle: nodes, labels, group arcs
    def build_circle(self):
        cl, M = self.coll["circle"], self.M
        pos = [on_circle(self.ang[t["name"]]) for t in self.ordered]
        disc_mesh("nodes", cl, pos, 0.12, M.get("circle", COLS["node"]), z=0.6)
        for g in BS.GROUP_ORDER:
            names = [t["name"] for t in self.ordered if t["group"] == g]
            a0, a1 = self.ang[names[0]] + self.step / 2, self.ang[names[-1]] - self.step / 2
            arc = [a0 + (a1 - a0) * i / 40 for i in range(41)]
            pts = [C + (R + 2.45) * np.array([math.cos(x), math.sin(x)]) for x in arc]
            line_curve(f"arc_{g}", cl, M.get("circle", COLS[g]), pts, 0.08)
            am = (a0 + a1) / 2
            lp = C + (R + 3.05) * np.array([math.cos(am), math.sin(am)])
            rot = math.atan2(math.sin(am - math.pi / 2), math.cos(am - math.pi / 2))
            if not (-math.pi / 2 + 0.3 < rot <= math.pi / 2 + 0.3):
                rot = math.atan2(math.sin(rot + math.pi), math.cos(rot + math.pi))
            txt(cl, BS.GROUP_LABEL[g], (lp[0], lp[1], 0.7), 0.6, M.get("circle", COLS[g]),
                rot=rot, bold=True)
        hi = {"Mi9", "T4d", "Tm9", "T1"}
        for t in self.ordered:
            a = self.ang[t["name"]]
            lp = C + (R + 0.62) * np.array([math.cos(a), math.sin(a)])
            left = math.cos(a) < 0
            mat = M.get("circle", COLS["text"], name=f"lab_{t['name']}") if t["name"] in hi \
                else M.get("circle", COLS["text"])
            ob = txt(cl, t["name"], (lp[0], lp[1], 0.7), 0.38, mat,
                     align_x="RIGHT" if left else "LEFT", rot=a + math.pi if left else a)
            self.label_objs[t["name"]] = ob

    # --- chords: pairing real -> shuffled per source
    def build_chords(self):
        D = self.D
        real = {(c["src"], c["tar"]): c for c in D["real"]}
        shuf = {(c["src"], c["tar"]): c for c in D["shuffled"]}
        chords = []
        for t in self.ordered:
            s = t["name"]
            rt = [k[1] for k in real if k[0] == s]
            st = [k[1] for k in shuf if k[0] == s]
            assert len(rt) == len(st), s          # out-degree kept (harness invariant)
            common = set(rt) & set(st)
            pairs = [(x, x) for x in sorted(common)]
            key = lambda n: (self.ang[n] - self.ang[s]) % (2 * math.pi)  # noqa: E731
            pairs += list(zip(sorted(set(rt) - common, key=key), sorted(set(st) - common, key=key)))
            for t0, t1 in pairs:
                chords.append({"src": s, "t0": t0, "t1": t1,
                               "real": real[(s, t0)], "shuf": shuf[(s, t1)]})
        assert len(chords) == 604
        self.chords = chords
        n = len(chords)
        fr, fs = tuple(D["focus"]["real_cell"]), tuple(D["focus"]["shuffled_cell"])
        self.i_focus_real = next(i for i, c in enumerate(chords) if (c["src"], c["t0"]) == fr)
        self.i_focus_shuf = next(i for i, c in enumerate(chords) if (c["src"], c["t1"]) == fs)
        self.a_src = np.array([self.ang[c["src"]] for c in chords])
        self.a_t0 = np.array([self.ang[c["t0"]] for c in chords])
        self.a_t1 = np.array([self.ang[c["t1"]] for c in chords])
        self.loop0 = np.array([c["src"] == c["t0"] for c in chords])
        self.loop1 = np.array([c["src"] == c["t1"] for c in chords])
        self.moves = np.array([c["t0"] != c["t1"] for c in chords])
        self.w_real = np.array([half_width(c["real"]["n_syn_total"]) for c in chords])
        self.w_shuf = np.array([half_width(c["shuf"]["n_syn_total"]) for c in chords])
        sign_rgb = {1: np.array(COLS["exc"]), -1: np.array(COLS["inh"])}
        self.c_real = np.array([sign_rgb[c["real"]["sign"]] for c in chords])
        self.c_shuf = np.array([sign_rgb[c["shuf"]["sign"]] for c in chords])
        rng = np.random.default_rng(1)       # animation stagger only; nothing to do with data
        self.stagger_slide = rng.random(n)
        self.stagger_deal = rng.random(n)
        order = np.argsort((math.pi / 2 - self.a_src) % (2 * math.pi), kind="stable")
        self.stagger_draw = np.empty(n)
        self.stagger_draw[order] = np.arange(n) / n
        # thick lines underneath thin ones
        z = np.empty(n)
        z[np.argsort(-self.w_real, kind="stable")] = np.arange(n) * 0.0006
        self.rib = Ribbons("chords", self.coll["circle"], n, z)
        self.foc = Ribbons("focus_chord", self.coll["circle"], 1, [0.5])
        fk = D["focus"]
        self.f_ang = [(self.ang[fk["real_cell"][0]], self.ang[fk["real_cell"][1]]),
                      (self.ang[fk["shuffled_cell"][0]], self.ang[fk["shuffled_cell"][1]])]
        self.f_w = max(half_width(chords[self.i_focus_real]["real"]["n_syn_total"]), 0.06 * K)

    # --- right-hand panel: titles, legend, stats, kernel inset
    def build_panel(self):
        P, M, D = self.coll["panel"], self.M, self.D
        n_real = len(D["real"])
        seed = D["provenance"]["seed"]
        inv = D["provenance"]["invariants_reported_by_harness"]
        fk = D["focus"]
        x = PANEL_X
        txt(P, "real bank", (x, 10.4, 0), 1.1, M.get("title_real", COLS["text"]), bold=True)
        txt(P, "flyvis FIB-25/FIB-19 type-level template: 65 types, "
               f"{n_real} connections", (x, 9.35, 0), 0.52, M.get("title_real", COLS["text2"]))
        txt(P, f"shuffled bank (seed {seed})", (x, 10.4, 0), 1.1,
            M.get("title_shuf", COLS["text"]), bold=True)
        txt(P, f"shuffled_bank(REAL, seed={seed}) from the C6 harness", (x, 9.35, 0), 0.52,
            M.get("title_shuf", COLS["text2"]))
        # legend
        y0 = 7.6
        rows = [("exc", "excitatory (sign +1)"), ("inh", "inhibitory (sign \u22121)")]
        for i, (k, lab) in enumerate(rows):
            y = y0 - i * 0.95
            line_curve(f"leg_{k}", P, M.get("legend", COLS[k]), [(x - 6.5, y), (x - 4.6, y)], 0.07)
            txt(P, lab, (x - 4.2, y, 0), 0.5, M.get("legend", COLS["text"]), align_x="LEFT")
        y = y0 - 2 * 0.95
        cu = BS.new_curve("leg_taper", P, M.get("legend", COLS["text2"]))
        BS.add_spline(cu, [Vector((x - 6.5 + 1.9 * i / 10, y, 0)) for i in range(11)], 0.13, 0.03, 0)
        txt(P, "thick end = sending type, thin end = receiving type", (x - 4.2, y, 0), 0.5,
            M.get("legend", COLS["text"]), align_x="LEFT")
        txt(P, "line width grows with the mean synapse count", (x - 4.2, y - 0.95, 0), 0.5,
            M.get("legend", COLS["text"]), align_x="LEFT")
        # shuffle statistics
        stats = [("stats1", "kept: every type's number of outgoing and incoming connections"),
                 ("stats2", f"moved: {inv['cells_changed']} of the {n_real} connections to a new "
                            f"(sending, receiving) pair; {n_real - inv['cells_changed']} stay"),
                 ("stats3", f"then: all {n_real} kernels, each with its sign, dealt at random; "
                            "none keeps its own")]
        for i, (g, s) in enumerate(stats):
            txt(P, s, (x - 8.6, 7.6 - i * 1.0, 0), 0.55, M.get(g, COLS["text"]), align_x="LEFT")
        # kernel inset
        kern = fk["kernel"]
        kx, ky = x, -2.6
        lat_r = max(max(abs(o["du"]), abs(o["dv"]), abs(o["du"] + o["dv"]))
                    for o in kern["offsets"] + kern["hull"]) + 1
        hs = 3.9 / (1.5 * lat_r + 1)
        hexr = hs * 0.98
        lat = [(kx + 1.5 * v * hs, ky - math.sqrt(3) * (u + v / 2) * hs)
               for u in range(-lat_r, lat_r + 1) for v in range(-lat_r, lat_r + 1)
               if abs(u + v) <= lat_r]
        ob = disc_mesh("kernel_lattice", P, lat, hexr * 0.97, M.get("kernel", COLS["grid"]),
                       segments=6, z=-0.02)
        ob.modifiers.new("wire", "WIREFRAME").thickness = 0.03
        nmax = max(o["n_syn"] for o in kern["offsets"])
        kcol = COLS["exc"] if kern["sign"] > 0 else COLS["inh"]
        kmat = M.get("kernel", kcol)
        for o in kern["offsets"]:
            px, py = kx + o["xy"][0] * hs, ky + o["xy"][1] * hs
            r = hexr * (0.35 + 0.62 * math.sqrt(o["n_syn"] / nmax))
            disc_mesh(f"kcell_{o['du']}_{o['dv']}", P, [(px, py)], r, kmat, segments=6)
            txt(P, f"{o['n_syn']:.1f}", (px, py, 0.05), 0.42, M.get("kernel", COLS["label_on"]),
                bold=True)
        if kern["hull"]:
            disc_mesh("kernel_hull", P, [(kx + h["xy"][0] * hs, ky + h["xy"][1] * hs)
                                         for h in kern["hull"]], hexr * 0.3,
                      M.get("kernel", COLS["hull"]), segments=6)
        ring = [(kx + math.cos(a) * 4.4, ky + math.sin(a) * 4.4)
                for a in (2 * math.pi * i / 64 for i in range(65))]
        line_curve("kernel_ring", P, M.get("kernel", COLS["focus"]), ring, 0.06)
        foot = "hexagon size ~ mean synapses at that column offset (value printed)"
        if kern["hull"]:
            foot += "; grey dot = hull-filled offset"
        txt(P, foot, (kx, ky - 5.0, 0), 0.46, M.get("kernel", COLS["text2"]))
        a, b = fk["real_cell"]
        c, d = fk["shuffled_cell"]
        txt(P, f"kernel of {a} \u2192 {b}", (kx, 3.35, 0), 0.62, M.get("khdr_real", COLS["text"]),
            bold=True)
        txt(P, "mean synapses per column offset, hexagonal lattice", (kx, 2.55, 0), 0.5,
            M.get("khdr_real", COLS["text2"]))
        txt(P, f"the same kernel now sits at {c} \u2192 {d}", (kx, 3.35, 0), 0.62,
            M.get("khdr_shuf", COLS["text"]), bold=True)
        txt(P, f"({a} \u2192 {b} is empty after this shuffle)" if not fk["real_cell_in_shuffled"]
            else f"({a} \u2192 {b} holds another kernel now)", (kx, 2.55, 0), 0.5,
            M.get("khdr_shuf", COLS["text2"]))

    # --- matrix shot
    def build_matrices(self):
        X, M, D = self.coll["matrix"], self.M, self.D
        idx = {t["name"]: i for i, t in enumerate(self.ordered)}
        n = len(self.ordered)
        cell = 0.185
        side = n * cell
        top = MY + 7.9
        outdeg = {t["name"]: 0 for t in self.ordered}
        indeg = dict(outdeg)
        for c in D["real"]:
            outdeg[c["src"]] += 1
            indeg[c["tar"]] += 1
        mx = max(max(outdeg.values()), max(indeg.values()))
        seed = D["provenance"]["seed"]
        for key, x0, title, focus in [
                ("real", -18.2, "real bank", D["focus"]["real_cell"]),
                ("shuffled", 3.4, f"shuffled bank (seed {seed})", D["focus"]["shuffled_cell"])]:
            groups = {+1: [], -1: [], 0: []}
            for c in D[key]:
                i, j = idx[c["src"]], idx[c["tar"]]
                cx, cy = x0 + (j + 0.5) * cell, top - (i + 0.5) * cell
                f = [c["src"], c["tar"]] == list(focus)
                h = cell * (0.62 if f else 0.45)
                groups[0 if f else c["sign"]].append((cx - h, cy - h, cx + h, cy + h))
            rect_mesh(f"mx_{key}_exc", X, groups[1], M.get("matrix", COLS["exc"]))
            rect_mesh(f"mx_{key}_inh", X, groups[-1], M.get("matrix", COLS["inh"]))
            rect_mesh(f"mx_{key}_foc", X, groups[0], M.get("matrix", COLS["focus"]), z=0.05)
            fr = [(x0, top), (x0 + side, top), (x0 + side, top - side), (x0, top - side), (x0, top)]
            line_curve(f"mx_{key}_frame", X, M.get("matrix", COLS["grid"]), fr, 0.025, z=-0.01)
            k = 0
            for g in BS.GROUP_ORDER[:-1]:
                k += sum(1 for t in self.ordered if t["group"] == g)
                d = k * cell
                line_curve(f"mx_{key}_v{g}", X, M.get("matrix", COLS["grid"]),
                           [(x0 + d, top), (x0 + d, top - side)], 0.018, z=-0.01)
                line_curve(f"mx_{key}_h{g}", X, M.get("matrix", COLS["grid"]),
                           [(x0, top - d), (x0 + side, top - d)], 0.018, z=-0.01)
            # degree bars: out-degree right of each row, in-degree under each column
            L = 2.3
            deg_o = [(x0 + side + 0.2, top - (i + 0.92) * cell,
                      x0 + side + 0.2 + L * outdeg[t["name"]] / mx, top - (i + 0.08) * cell)
                     for i, t in enumerate(self.ordered)]
            deg_i = [(x0 + (j + 0.08) * cell, top - side - 0.2 - L * indeg[t["name"]] / mx,
                      x0 + (j + 0.92) * cell, top - side - 0.2)
                     for j, t in enumerate(self.ordered)]
            rect_mesh(f"deg_{key}", X, deg_o + deg_i, M.get("matrix", COLS["bar"], name=f"bar_{key}"))
            cx = x0 + side / 2
            txt(X, title, (cx, MY + 10.6, 0), 1.0, M.get("matrix", COLS["text"]), bold=True)
            txt(X, "receiving type \u2192", (cx, top + 0.45, 0), 0.45, M.get("matrix", COLS["text2"]))
            txt(X, "\u2190 sending type", (x0 - 0.45, top - side / 2, 0), 0.45,
                M.get("matrix", COLS["text2"]), rot=math.pi / 2)
            txt(X, "outgoing per type", (x0 + side + 0.2 + L + 0.45, top - side / 2, 0), 0.45,
                M.get("matrix", COLS["text2"]), rot=-math.pi / 2)
            txt(X, "incoming per type", (cx, top - side - 0.2 - L - 0.5, 0), 0.45,
                M.get("matrix", COLS["text2"]))
            txt(X, f"{len(D[key])} connections", (cx, MY + 9.5, 0), 0.6,
                M.get("matrix", COLS["text2"]))

    # --- title, caveats, end card
    def build_cards(self):
        Cc, M = self.coll["cards"], self.M
        txt(Cc, VS.TITLE, (0, 2.6, 0), 1.55, M.get("title", COLS["text"]), bold=True)
        txt(Cc, VS.SUBTITLE, (0, 0.8, 0), 0.8, M.get("title", COLS["text2"]))
        txt(Cc, "Caveats", (0, MY + 6.0, 1), 1.3, M.get("cav_title", COLS["text"]), bold=True)
        for i, s in enumerate(VS.CAVEATS):
            txt(Cc, s, (0, MY + 3.4 - i * 1.9, 1), 0.9, M.get(f"cav{i + 1}", COLS["text"]))
        txt(Cc, "Sources", (0, MY + 5.6, 1), 1.3, M.get("end", COLS["text"]), bold=True)
        for i, s in enumerate(VS.END_LINES):
            txt(Cc, s, (0, MY + 3.4 - i * 1.3, 1), 0.9, M.get("end", COLS["text"]))
        txt(Cc, "Explanatory illustration, not evidence. Rendered in Blender; "
                "synthetic voice (Kyutai pocket-tts).",
            (0, MY + 3.4 - len(VS.END_LINES) * 1.3 - 0.4, 1), 0.6,
            M.get("end", COLS["text2"]))

    # --- camera and the caption strip that rides with it
    def build_camera_and_hud(self):
        cam_d = bpy.data.cameras.new("camera")
        cam_d.type = "ORTHO"
        cam_d.ortho_scale = ORTHO
        cam_d.clip_start, cam_d.clip_end = 1.0, 200.0
        cam = bpy.data.objects.new("camera", cam_d)
        cam.location = (0.0, 0.0, 60.0)
        self.sc.collection.objects.link(cam)
        self.sc.camera = cam
        self.cam = cam
        hud = bpy.data.objects.new("hud", None)
        self.coll["hud"].objects.link(hud)
        hud.parent = cam
        hud.location = (0.0, 0.0, -40.0)
        self.hud = hud
        H, M = self.coll["hud"], self.M
        bar = rect_mesh("caption_bar", H, [(-ORTHO / 2 - 1, -HALF_H - 1, ORTHO / 2 + 1, BAR_TOP)],
                        M.get("hud", COLS["capbar"]))
        rule = rect_mesh("caption_rule", H, [(-ORTHO / 2 - 1, BAR_TOP, ORTHO / 2 + 1, BAR_TOP + 0.05)],
                         M.get("hud", COLS["rule"]))
        for o in (bar, rule):
            o.parent = hud
        self.caps = []
        for i, c in enumerate(self.T["chunks"]):
            body = "\n".join(textwrap.wrap(c["text"], 72))
            ob = txt(H, body, (0, CAPTION_Y, 0.1), 0.95, M.get(f"cap{i}", COLS["text"]))
            ob.data.space_line = 1.05
            ob.parent = hud
            self.caps.append(ob)

    def setup_render(self):
        sc = self.sc
        world = bpy.data.worlds.new("world")
        sc.world = world
        world.use_nodes = True
        bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
        bg.inputs["Color"].default_value = (1, 1, 1, 1)
        sc.render.resolution_x, sc.render.resolution_y = RES
        sc.render.fps = FPS
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        sc.render.image_settings.compression = 15
        try:
            sc.view_settings.view_transform = "Standard"
        except TypeError as e:
            print("view transform left at default:", e)
        for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
            try:
                sc.render.engine = eng
                break
            except TypeError:
                continue
        if hasattr(sc, "eevee"):
            sc.eevee.taa_render_samples = 16
        print("engine:", sc.render.engine)

    # ------------------------------------------------------------------ one frame
    def at(self, id_, key="start"):
        return self.cue[id_][key]

    def state(self, t):
        a = self.at
        vis = {}
        # title card
        vis["title"] = min(ramp(t, 0.25, 0.8), 1 - ramp(t, a("types") - 0.5, 0.6))
        # circle
        vis["circle"] = ramp(t, a("types") - 0.3, 0.8)
        vis["title_real"] = vis["circle"] * (1 - ramp(t, a("shuffle"), 0.6))
        vis["title_shuf"] = ramp(t, a("shuffle") + 0.7, 0.6)
        vis["legend"] = window(t, a("lines"), a("focus"))
        vis["stats1"] = window(t, a("degrees"), a("tables") - 0.8)
        vis["stats2"] = window(t, a("degrees") + 2.4, a("tables") - 0.8)
        vis["stats3"] = window(t, a("deal"), a("tables") - 0.8)
        vis["kernel"] = max(window(t, a("focus") + 1.2, a("shuffle") + 0.6),
                            window(t, a("deal") + 0.6, a("tables") - 0.8))
        vis["khdr_real"] = window(t, a("focus") + 1.2, a("shuffle") + 0.6)
        vis["khdr_shuf"] = window(t, a("deal") + 0.6, a("tables") - 0.8)
        dim_mx = ramp(t, a("cav1") - 0.3, 0.8)
        vis["matrix"] = 1 - 0.96 * dim_mx
        vis["cav_title"] = window(t, a("cav1") - 0.2, a("source") - 0.1)
        for i in (1, 2, 3):
            vis[f"cav{i}"] = window(t, a(f"cav{i}") - 0.2, a("source") - 0.1)
        vis["end"] = ramp(t, a("source") - 0.1, 0.6)
        vis["hud"] = 1.0
        chunks = self.T["chunks"]
        for i, c in enumerate(chunks):
            t_out = chunks[i + 1]["start"] - 0.35 if i + 1 < len(chunks) else self.T["total"] + 1
            vis[f"cap{i}"] = window(t, c["start"] - 0.3, t_out, 0.15, 0.15)

        # highlights
        over = {}
        h_real = window(t, a("focus"), a("shuffle") + 0.3, 0.4, 0.4)
        h_shuf = window(t, a("deal") + 0.6, a("tables") - 0.8, 0.4, 0.4)
        ft = np.array(COLS["focus_text"])
        tx = np.array(COLS["text"])
        fk = self.D["focus"]
        hl = {n: 0.0 for n in ("Mi9", "T4d", "Tm9", "T1")}
        for n in fk["real_cell"]:
            hl[n] = max(hl[n], h_real)
        for n in fk["shuffled_cell"]:
            hl[n] = max(hl[n], h_shuf)
        for n, h in hl.items():
            over[f"lab_{n}"] = tx + (ft - tx) * h
            self.label_objs[n].scale = (1 + 0.6 * h,) * 3
        bar_hi = window(t, a("same"), a("same", "end") + 0.6, 0.4, 0.5)
        bc = np.array(COLS["bar"]) + (np.array(COLS["focus_text"]) - np.array(COLS["bar"])) * bar_hi
        over["bar_real"] = over["bar_shuffled"] = bc

        # camera
        main, zoom = np.array([0.0, 0.0, ORTHO]), np.array([4.0, -1.8, 38.0])
        mxs = np.array([0.0, MY, ORTHO])
        z_in = ramp(t, a("kernel"), 1.4) * (1 - ramp(t, a("shuffle") - 0.2, 1.2))
        cam = main + (zoom - main) * z_in
        pan = ramp(t, a("tables") - 0.8, 1.5)
        cam = cam + (mxs - cam) * pan
        self.cam.location = (cam[0], cam[1], 60.0)
        self.cam.data.ortho_scale = cam[2]
        self.hud.scale = (cam[2] / ORTHO,) * 3

        # chords
        draw = ramp(t, a("lines") - 0.1, 3.0)
        p = np.clip((draw * 1.6 - self.stagger_draw * 0.6), 0, 1)
        grey = ramp(t, a("shuffle"), 1.0)
        slide_u = clamp01((t - (a("shuffle") + 1.0)) / (a("degrees", "end") - a("shuffle") - 1.0))
        e = np.array([smooth((slide_u - 0.6 * s) / 0.4) for s in self.stagger_slide]) * self.moves
        deal0 = a("deal") + 2.6
        d = np.array([smooth((t - deal0 - 1.6 * s) / 0.5) for s in self.stagger_deal])
        dim = 0.85 * window(t, a("focus"), a("shuffle") + 0.2, 0.6, 0.6) \
            + 0.55 * window(t, a("deal") + 0.4, deal0 + 1.0, 0.5, 0.8)
        n = len(self.chords)
        pts = np.stack([geom(self.a_src[i], self.a_t0[i], self.a_t1[i], self.loop0[i],
                             self.loop1[i], e[i], max(p[i], 1e-3)) for i in range(n)])
        w_grey = 0.028
        w = self.w_real + (w_grey - self.w_real) * grey
        w = w + (self.w_shuf - w) * d
        w = np.where(p > 1e-3, w, 0.0)
        col = self.c_real + (GREY_LINE - self.c_real) * grey
        col = col + (self.c_shuf - col) * d[:, None]
        col = col + (WHITE - col) * dim
        col = WHITE + (col - WHITE) * vis["circle"]
        h1 = self.rib.set(pts, w, 0.25 * w, col)

        # followed kernel
        fv = max(window(t, a("focus"), a("shuffle") + 0.2, 0.4, 0.4),
                 window(t, a("deal"), a("tables") + 1.0, 0.4, 0.4))
        tr = ramp(t, a("deal") + 0.6, 2.2)
        (s0, t0), (s1, t1) = self.f_ang
        a_s = s0 + wrap(s1 - s0) * tr
        a_t = t0 + wrap(t1 - t0) * tr
        fp = geom(a_s, a_t, a_t, False, False, 0.0)[None]
        fw = np.array([self.f_w * 1.4 * (fv > 1e-3)])
        fc = (WHITE + (np.array(COLS["focus"]) - WHITE) * fv * vis["circle"])[None]
        h2 = self.foc.set(fp, fw, fw * 0.36, fc)

        mstate = self.M.apply(vis, over)
        key = hashlib.sha1(repr((h1, h2, mstate, tuple(np.round(cam, 4)),
                                 tuple(round(o.scale[0], 4) for o in self.label_objs.values()))
                                ).encode()).hexdigest()
        return key


# ------------------------------------------------------------------ main
def main():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    def opt(name, default=None):
        return a[a.index(name) + 1] if name in a else default

    build = Path(opt("--build"))
    data = Path(opt("--data", str(BS.DEFAULT_JSON)))
    stills = opt("--stills")
    pct = int(opt("--percent", "100"))
    D = json.loads(data.read_text(encoding="utf-8"))
    T = json.loads((build / "timing.json").read_text(encoding="utf-8"))
    t0 = time.time()
    S = Scene(D, T)
    S.sc.render.resolution_percentage = pct
    print(f"scene built ({time.time() - t0:.1f}s)")
    if stills:
        out = build / "stills"
        out.mkdir(parents=True, exist_ok=True)
        for ts in stills.split(","):
            S.state(float(ts))
            S.sc.render.filepath = str(out / f"t_{float(ts):06.2f}.png")
            bpy.ops.render.render(write_still=True)
        print(f"stills done ({time.time() - t0:.1f}s)")
        return
    out = build / "frames"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    nf = int(math.ceil(T["total"] * FPS))
    prev_key, prev_file, rendered = None, None, 0
    for f in range(nf):
        key = S.state(f / FPS)
        fn = out / f"f_{f + 1:05d}.png"
        if key == prev_key:
            shutil.copyfile(prev_file, fn)
        else:
            S.sc.render.filepath = str(fn)
            bpy.ops.render.render(write_still=True)
            rendered += 1
            prev_key, prev_file = key, fn
        if f % 150 == 0:
            print(f"frame {f + 1}/{nf}  rendered {rendered}  ({time.time() - t0:.0f}s)", flush=True)
    (build / "frames_info.json").write_text(json.dumps(
        {"frames": nf, "fps": FPS, "rendered": rendered, "seconds": round(time.time() - t0, 1)}),
        encoding="utf-8")
    print(f"done: {nf} frames, {rendered} rendered ({time.time() - t0:.0f}s)")


main()
