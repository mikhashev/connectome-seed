"""Blender scene: the real connectome bank vs one shuffled bank, side by side.

Explanatory figure, not evidence. It draws exactly the two objects the C6 harness compares:
REAL (results/genome/c6/harness.py:135-169) and shuffled_bank(REAL, seed) (harness.py:907).
The data come from tools/viz/export_bank_scene_data.py (run with the repo venv); this script
only reads that JSON, so it runs in Blender's bundled Python (no numpy, flyvis or torch needed).

Each panel has three parts, with identical coordinates on both sides so that only the wiring
differs:
  * circle: the 65 cell types on a circle, grouped by flyvis's own layout (retina,
    intermediate, output) in flyvis node order. One chord per non-empty (source, target) cell.
    Chord width grows with log(1 + total mean synapses of its in_json offsets); the chord is
    thick at the source and thin at the target (direction). Red = excitatory (sign +1), blue =
    inhibitory (sign -1). A cell with source == target is a small loop outside the circle.
  * matrix: the 65 x 65 existence table the harness tests (rows = source, columns = target),
    one square per non-empty cell, coloured by sign.
  * kernel inset: one offset kernel on flyvis's hex lattice (du, dv -> n_syn). It is the same
    content object on both sides: in the real bank it sits at Mi9 -> T4d, in the shuffled bank
    the harness moved it to another cell. That cell's chord and square are drawn in yellow.

Run (headless):
    "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background \
        --python tools/viz/bank_scene.py -- [scene_data.json] [--no-render]
Writes bank_scene.blend and bank_scene_preview.png next to the JSON.
"""

import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

# Data and renders live in the sibling data root, outside the repository.
DEFAULT_JSON = (Path(__file__).resolve().parents[3] / "connectome-seed-data" / "renderings"
                / "bank_scene" / "scene_data.json")

GROUP_ORDER = ["retina", "intermediate", "output"]
GROUP_LABEL = {"retina": "retina (input)", "intermediate": "intermediate", "output": "output"}
GROUP_GAP = 0.18            # radians of empty arc between groups
R_CIRCLE = 8.0
PANEL_DX = 23.0             # distance between the two panel centres
MATRIX_CELL = 0.2
COL = {
    "exc": (0.80, 0.18, 0.12), "inh": (0.13, 0.35, 0.80), "focus": (0.98, 0.72, 0.0),
    "node": (0.15, 0.15, 0.15), "text": (0.08, 0.08, 0.08), "grid": (0.80, 0.80, 0.80),
    "hull": (0.72, 0.72, 0.72), "label_on": (1.0, 1.0, 1.0),
    "retina": (0.35, 0.60, 0.30), "intermediate": (0.55, 0.40, 0.65), "output": (0.45, 0.45, 0.45),
    "bg": (1.0, 1.0, 1.0),
}


# ------------------------------------------------------------------ helpers
def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    render = "--no-render" not in a
    paths = [x for x in a if not x.startswith("--")]
    return (Path(paths[0]) if paths else DEFAULT_JSON), render


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def flat_material(name, rgb):
    """Emission-only material: flat colours for a diagram, independent of lighting."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em.inputs["Color"].default_value = (*rgb, 1.0)
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*rgb, 1.0)
    return m


def link(obj, coll):
    coll.objects.link(obj)
    return obj


def text(coll, body, loc, size, mat, align_x="CENTER", align_y="CENTER", rot=0.0, name=None):
    cu = bpy.data.curves.new(name or f"txt_{body[:20]}", "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = align_x
    cu.align_y = align_y
    ob = bpy.data.objects.new(cu.name, cu)
    ob.location = loc
    ob.rotation_euler = (0.0, 0.0, rot)
    ob.data.materials.append(mat)
    return link(ob, coll)


def type_angles(types):
    """Angle per type: groups in GROUP_ORDER, flyvis node order inside a group, clockwise from
    the top, with GROUP_GAP between groups."""
    ordered = [t for g in GROUP_ORDER for t in sorted((t for t in types if t["group"] == g),
                                                      key=lambda t: t["flyvis_order"])]
    assert len(ordered) == len(types) == 65
    step = (2 * math.pi - GROUP_GAP * len(GROUP_ORDER)) / len(ordered)
    ang, a, prev = {}, math.pi / 2 - GROUP_GAP / 2, None
    for t in ordered:
        if prev is not None and t["group"] != prev:
            a -= GROUP_GAP
        ang[t["name"]] = a
        a -= step
        prev = t["group"]
    return ordered, ang, step


def width(n_syn_total):
    return 0.015 + 0.020 * math.log1p(n_syn_total)


def chord_points(p0, p1, centre, n=24):
    """Quadratic Bezier from p0 to p1 bent towards the circle centre."""
    c = centre + ((p0 + p1) / 2 - centre) * 0.15
    return [(1 - s) ** 2 * p0 + 2 * s * (1 - s) * c + s ** 2 * p1
            for s in (i / (n - 1) for i in range(n))]


def loop_points(p, centre, n=20):
    """Small teardrop loop outside the circle for a source == target cell."""
    d = (p - centre).normalized()
    perp = Vector((-d.y, d.x, 0.0))
    pts = []
    for i in range(n):
        s = 2 * math.pi * i / (n - 1)
        pts.append(p + d * (0.35 * (1 - math.cos(s))) + perp * (0.18 * math.sin(s)))
    return pts


def add_spline(cu, pts, r0, r1, z):
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for i, q in enumerate(pts):
        f = i / (len(pts) - 1)
        sp.points[i].co = (q.x, q.y, z, 1.0)
        sp.points[i].radius = r0 + (r1 - r0) * f


def new_curve(name, coll, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.fill_mode = "FULL"
    cu.bevel_depth = 1.0          # the per-point radius carries the real width
    cu.bevel_resolution = 1
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu)
    link(ob, coll)
    return cu


# ------------------------------------------------------------------ one panel
def build_panel(coll, cells, types, focus_cell, origin, title, subtitle, kernel, kernel_note, M):
    ordered, ang, step = type_angles(types)
    cx, cy = origin
    centre = Vector((cx, cy, 0.0))
    pos = {n: centre + Vector((math.cos(a), math.sin(a), 0.0)) * R_CIRCLE for n, a in ang.items()}

    # nodes: one mesh of small spheres
    me = bpy.data.meshes.new(f"{coll.name}_types")
    bm = bmesh.new()
    for t in ordered:
        bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.14,
                                  matrix=Matrix.Translation(pos[t["name"]]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(me.name, me)
    me.materials.append(M["node"])
    link(ob, coll)

    # group arcs and labels, type labels
    for g in GROUP_ORDER:
        names = [t["name"] for t in ordered if t["group"] == g]
        a0, a1 = ang[names[0]] + step / 2, ang[names[-1]] - step / 2
        cu = new_curve(f"{coll.name}_arc_{g}", coll, M[g])
        pts = [centre + Vector((math.cos(a), math.sin(a), 0)) * (R_CIRCLE + 2.25)
               for a in (a0 + (a1 - a0) * i / 40 for i in range(41))]
        add_spline(cu, pts, 0.09, 0.09, 0.0)
        am = (a0 + a1) / 2
        lp = centre + Vector((math.cos(am), math.sin(am), 0)) * (R_CIRCLE + 2.9)
        rot = am - math.pi / 2                      # tangent to the arc
        rot = math.atan2(math.sin(rot), math.cos(rot))
        if not (-math.pi / 2 + 0.3 < rot <= math.pi / 2 + 0.3):   # keep the text upright
            rot = math.atan2(math.sin(rot + math.pi), math.cos(rot + math.pi))
        text(coll, GROUP_LABEL[g], lp, 0.55, M[g], rot=rot)
    for t in ordered:
        a = ang[t["name"]]
        lp = centre + Vector((math.cos(a), math.sin(a), 0)) * (R_CIRCLE + 0.95)
        left = math.cos(a) < 0
        text(coll, t["name"], lp, 0.27, M["text"], align_x="RIGHT" if left else "LEFT",
             rot=a + math.pi if left else a)

    # chords, one curve object per sign; the focus cell separately, on top
    curves = {+1: new_curve(f"{coll.name}_chords_exc", coll, M["exc"]),
              -1: new_curve(f"{coll.name}_chords_inh", coll, M["inh"])}
    fcu = new_curve(f"{coll.name}_chord_focus", coll, M["focus"])
    for c in cells:
        is_focus = (c["src"], c["tar"]) == tuple(focus_cell)
        w = width(c["n_syn_total"])
        p0, p1 = pos[c["src"]], pos[c["tar"]]
        pts = loop_points(p0, centre) if c["src"] == c["tar"] else chord_points(p0, p1, centre)
        if is_focus:
            add_spline(fcu, pts, max(w, 0.06) * 1.4, max(w, 0.06) * 0.5, 0.05)
        else:
            add_spline(curves[c["sign"]], pts, w, 0.25 * w, 0.0)

    # existence matrix, rows = source, columns = target, same type order as the circle
    idx = {t["name"]: i for i, t in enumerate(ordered)}
    n = len(ordered)
    mx0 = cx - R_CIRCLE - 1.0
    my0 = cy - R_CIRCLE - 4.2          # top edge of the matrix
    side = n * MATRIX_CELL
    me = bpy.data.meshes.new(f"{coll.name}_matrix")
    bm = bmesh.new()
    mats = [M["exc"], M["inh"], M["focus"]]
    for c in cells:
        i, j = idx[c["src"]], idx[c["tar"]]
        x = mx0 + (j + 0.5) * MATRIX_CELL
        y = my0 - (i + 0.5) * MATRIX_CELL
        is_f = (c["src"], c["tar"]) == tuple(focus_cell)
        res = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1,
                                    size=MATRIX_CELL * (1.1 if is_f else 0.45),
                                    matrix=Matrix.Translation((x, y, 0.0)))
        k = 2 if is_f else (0 if c["sign"] > 0 else 1)
        for f in {f for v in res["verts"] for f in v.link_faces}:
            f.material_index = k
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    link(bpy.data.objects.new(me.name, me), coll)
    # frame and group dividers
    gcu = new_curve(f"{coll.name}_matrix_grid", coll, M["grid"])
    corners = [Vector((mx0, my0, 0)), Vector((mx0 + side, my0, 0)),
               Vector((mx0 + side, my0 - side, 0)), Vector((mx0, my0 - side, 0)),
               Vector((mx0, my0, 0))]
    add_spline(gcu, corners, 0.02, 0.02, -0.01)
    k = 0
    for g in GROUP_ORDER[:-1]:
        k += sum(1 for t in ordered if t["group"] == g)
        d = k * MATRIX_CELL
        add_spline(gcu, [Vector((mx0 + d, my0, 0)), Vector((mx0 + d, my0 - side, 0))], .015, .015, -.01)
        add_spline(gcu, [Vector((mx0, my0 - d, 0)), Vector((mx0 + side, my0 - d, 0))], .015, .015, -.01)
    text(coll, "target type  \u2192", (mx0 + side / 2, my0 + 0.45, 0), 0.4, M["text"])
    text(coll, "source type  \u2192", (mx0 - 0.45, my0 - side / 2, 0), 0.4, M["text"],
         rot=-math.pi / 2)
    text(coll, "65 \u00d7 65 existence table (one square per non-empty cell)",
         (mx0, my0 - side - 0.55, 0), 0.34, M["text"], align_x="LEFT")

    # kernel inset on flyvis's hex lattice
    kx, ky = mx0 + side + 3.9, my0 - 5.2
    lat_r = max(max(abs(o["du"]), abs(o["dv"]), abs(o["du"] + o["dv"]))
                for o in kernel["offsets"] + kernel["hull"]) + 1
    hs = 3.6 / (1.5 * lat_r + 1)               # hex centre spacing scale: fits the ring
    hexr = hs * 0.98
    me = bpy.data.meshes.new(f"{coll.name}_kernel")
    bm = bmesh.new()
    nmax = max(o["n_syn"] for o in kernel["offsets"])
    kmat = [M["hull"], M["exc"] if kernel["sign"] > 0 else M["inh"]]
    # lattice background: radius 5 hex patch, flyvis default hex_to_pixel
    for u in range(-lat_r, lat_r + 1):
        for v in range(-lat_r, lat_r + 1):
            if abs(u + v) <= lat_r:
                x, y = 1.5 * v, -math.sqrt(3) * (u + v / 2)
                bmesh.ops.create_circle(bm, cap_ends=True, segments=6, radius=hexr * 0.97,
                                               matrix=Matrix.Translation((kx + x * hs, ky + y * hs, -0.02)))
    bm.to_mesh(me)
    bm.free()
    lat = bpy.data.objects.new(f"{coll.name}_kernel_lattice", me)
    link(lat, coll)
    lat.modifiers.new("wire", "WIREFRAME").thickness = 0.03
    lat.data.materials.append(M["grid"])
    me = bpy.data.meshes.new(f"{coll.name}_kernel_cells")
    bm = bmesh.new()
    for o in kernel["offsets"]:
        x, y = o["xy"]
        r = hexr * (0.35 + 0.62 * math.sqrt(o["n_syn"] / nmax))
        res = bmesh.ops.create_circle(bm, cap_ends=True, segments=6, radius=r,
                                      matrix=Matrix.Translation((kx + x * hs, ky + y * hs, 0.0)))
        for f in {f for v in res["verts"] for f in v.link_faces}:
            f.material_index = 1
        text(coll, f"{o['n_syn']:.1f}", (kx + x * hs, ky + y * hs, 0.05), 0.26, M["label_on"])
    for h in kernel["hull"]:
        x, y = h["xy"]
        res = bmesh.ops.create_circle(bm, cap_ends=True, segments=6, radius=hexr * 0.3,
                                      matrix=Matrix.Translation((kx + x * hs, ky + y * hs, 0.0)))
        for f in {f for v in res["verts"] for f in v.link_faces}:
            f.material_index = 0
    bm.to_mesh(me)
    bm.free()
    for m in kmat:
        me.materials.append(m)
    link(bpy.data.objects.new(me.name, me), coll)
    ring = new_curve(f"{coll.name}_kernel_ring", coll, M["focus"])
    pts = [Vector((kx + math.cos(a) * 4.0, ky + math.sin(a) * 4.0, 0))
           for a in (2 * math.pi * i / 64 for i in range(65))]
    add_spline(ring, pts, 0.05, 0.05, 0.0)
    for i, line in enumerate(kernel_note):
        text(coll, line, (kx, ky + 4.7 - i * 0.48 + 0.9, 0), 0.34 if i else 0.4, M["text"])
    text(coll, "offset kernel on flyvis's hex lattice: hexagon size ~ mean synapses",
         (kx, ky - 4.6, 0), 0.3, M["text"])
    text(coll, "at offset (du, dv), value printed; grey dot = hull-filled offset",
         (kx, ky - 5.05, 0), 0.3, M["text"])

    # titles
    text(coll, title, (cx, cy + R_CIRCLE + 4.3, 0), 0.95, M["text"])
    text(coll, subtitle, (cx, cy + R_CIRCLE + 3.5, 0), 0.42, M["text"])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    path, render = args()
    D = json.loads(path.read_text(encoding="utf-8"))
    clear_scene()
    sc = bpy.context.scene
    M = {k: flat_material(f"m_{k}", v) for k, v in COL.items() if k != "bg"}
    prov = D["provenance"]
    seed = prov["seed"]
    foc = D["focus"]
    inv = prov["invariants_reported_by_harness"]

    L = bpy.data.collections.new("real_bank")
    R = bpy.data.collections.new("shuffled_bank")
    sc.collection.children.link(L)
    sc.collection.children.link(R)
    n_real = len(D["real"])
    build_panel(L, D["real"], D["types"], foc["real_cell"], (-PANEL_DX / 2, 0.0),
                "real bank",
                f"flyvis fib25-fib19 v2.2 as the C6 harness reads it: {n_real} non-empty cells",
                foc["kernel"],
                [f"kernel of {foc['content_from'][0]} \u2192 {foc['content_from'][1]}",
                 f"sits at cell {foc['real_cell'][0]} \u2192 {foc['real_cell'][1]}"],
                M)
    moved = f"{foc['shuffled_cell'][0]} \u2192 {foc['shuffled_cell'][1]}"
    build_panel(R, D["shuffled"], D["types"], foc["shuffled_cell"], (PANEL_DX / 2, 0.0),
                f"shuffled bank (harness shuffled_bank, seed {seed})",
                f"{inv['cells_changed']} of {n_real} cells moved by degree-preserving swaps; "
                f"every kernel reassigned at random",
                foc["kernel"],
                [f"the same kernel ({foc['content_from'][0]} \u2192 {foc['content_from'][1]})",
                 f"now sits at cell {moved}",
                 f"({foc['real_cell'][0]} \u2192 {foc['real_cell'][1]} is empty here)"
                 if not foc["real_cell_in_shuffled"] else ""],
                M)

    # shared legend / caption
    C = bpy.data.collections.new("caption")
    sc.collection.children.link(C)
    y = -R_CIRCLE - 4.2 - 65 * MATRIX_CELL - 1.9
    lines = [
        "Kept by the shuffle: every type's out-degree and in-degree, and the multiset of the 604 kernels "
        "(offsets, hull, sign travel together).",
        "Changed: which (source, target) cells are non-empty, and which kernel sits in which cell. "
        f"Seed {seed}; target {prov['swaps_per_edge']} swaps per edge "
        f"({inv['successful_swaps']} successful swaps in {inv['attempts']} attempts).",
        "Chord: thick end = source, thin end = target; width ~ log(1 + total mean synapses); "
        "red = excitatory (+1), blue = inhibitory (-1); yellow = the followed kernel. "
        "Type positions are a drawing choice, identical on both sides.",
    ]
    for i, s in enumerate(lines):
        text(C, s, (0, y - i * 0.62, 0), 0.36, M["text"])

    # world, camera, light
    world = bpy.data.worlds.new("world")
    sc.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (*COL["bg"], 1.0)
    bg.inputs["Strength"].default_value = 1.0
    top, bottom = R_CIRCLE + 5.4, y - 2 * 0.62 - 0.6
    cam_d = bpy.data.cameras.new("camera")
    cam_d.type = "ORTHO"
    width_w = 2 * PANEL_DX + 1.0
    height_w = top - bottom
    cam_d.ortho_scale = max(width_w, height_w)
    cam = bpy.data.objects.new("camera", cam_d)
    cam.location = (0.0, (top + bottom) / 2, 60.0)
    sc.collection.objects.link(cam)
    sc.camera = cam
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.rotation_euler = (math.radians(30), 0, math.radians(20))
    sc.collection.objects.link(sun)

    sc.render.resolution_x = 3000
    sc.render.resolution_y = int(round(3000 * height_w / width_w))
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    try:
        sc.view_settings.view_transform = "Standard"
    except TypeError as e:
        print("view transform left at default:", e)
    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError as e:
        print("engine left at", sc.render.engine, e)
    if hasattr(sc, "eevee"):
        sc.eevee.taa_render_samples = 16

    out_dir = path.parent
    blend = out_dir / "bank_scene.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    print(f"saved {blend}  ({time.time() - t0:.1f}s)")
    if render:
        png = out_dir / "bank_scene_preview.png"
        sc.render.filepath = str(png)
        bpy.ops.render.render(write_still=True)
        print(f"rendered {png}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":      # Blender's --python runs this as __main__; bank_animation.py imports it
    main()
