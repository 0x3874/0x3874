"""Roblox-style horror Short, built from code in Blender (bpy).
Usage: python3 build.py MODE OUT [a b]   MODE = stills | full | frame
State is a pure function of time, applied per frame by a frame_change handler (hard-snapped, no interpolation).
"""
import bpy, sys, math, json, os, random
from mathutils import Vector, Euler, Matrix, Quaternion

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")) + "/"
FPS = 30
MODE = sys.argv[1] if len(sys.argv) > 1 else "stills"
OUT = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else ROOT + "build/stills/"
RANGE = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else None

WORDS = json.load(open(ROOT + "build/words_final.json"))
NAR_END = 37.7
VOICE = json.load(open(ROOT + "build/words_pre.json"))
def T(i): return WORDS[i][1]
MON_T0 = NAR_END + 0.22                    # monster line starts
MON_LATE = MON_T0 + 1.15                   # approx start of "late" (refined below)
END_T = MON_T0 + 1.74 + 1.5

def lin(c):  # sRGB -> linear
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h, a=1.0):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (lin(r), lin(g), lin(b), a)

# ------------------------------------------------------------------ scene / render
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.fps = FPS
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try: sc.render.engine = eng; break
    except TypeError: pass
ev = sc.eevee
ev.taa_render_samples = int(os.environ.get("SAMPLES", "12" if MODE in ("stills", "frame") else "32"))
for a, v in (("use_shadows", True), ("use_raytracing", True)):
    if hasattr(ev, a): setattr(ev, a, v)
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.view_settings.exposure = 0.0
sc.render.use_motion_blur = False
sc.render.film_transparent = False
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
sc.render.resolution_percentage = int(os.environ.get("PCT", "50" if MODE in ("stills", "frame") else "100"))

# ------------------------------------------------------------------ helpers
_cube = bpy.data.meshes.new("cube")
_cube.from_pydata([(x, y, z) for x in (-.5, .5) for y in (-.5, .5) for z in (-.5, .5)], [],
                  [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
_cube.update()
MATS = {}
def mat(name, color, emit=0.0, rough=1.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    n = m.node_tree.nodes; b = n["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs: b.inputs[k].default_value = 0.0
    if emit:
        b.inputs["Emission Color"].default_value = color
        b.inputs["Emission Strength"].default_value = emit
    MATS[name] = m; return m
def setemit(m, color, strength):
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Emission Color"].default_value = color
    b.inputs["Emission Strength"].default_value = strength

def box(name, size, loc, m, parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, _cube); sc.collection.objects.link(o)
    o.scale = size; o.location = loc; o.rotation_euler = rot
    if not o.data.materials: o.data.materials.append(m)   # shared mesh: one dummy slot
    o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = m
    if parent: o.parent = parent
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); sc.collection.objects.link(o)
    o.location = loc
    if parent: o.parent = parent
    return o
def light(name, kind, energy, color, loc, **kw):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = color[:3]
    if kind == "SPOT":
        d.spot_size = math.radians(kw.get("cone", 90)); d.spot_blend = kw.get("blend", 0.3)
    d.shadow_soft_size = kw.get("radius", 0.3)
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    return o
_DESC = {}
def hide(root, flag):
    if root.name not in _DESC:
        out = []; st = [root]
        while st:
            o = st.pop(); out.append(o); st.extend(o.children)
        _DESC[root.name] = out
    for o in _DESC[root.name]:
        if o.hide_render != flag: o.hide_render = flag
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def back(x, s=2.2):
    x = max(0.0, min(1.0, x)); c3 = s + 1; return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2

# ------------------------------------------------------------------ world
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
nt = w.node_tree; nt.nodes.clear()
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
nrm = nt.nodes.new("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"
sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
geo = nt.nodes.new("ShaderNodeNewGeometry"); neg = nt.nodes.new("ShaderNodeVectorMath"); neg.operation = "SCALE"; neg.inputs["Scale"].default_value = -1.0
nt.links.new(geo.outputs["Incoming"], neg.inputs[0]); nt.links.new(neg.outputs[0], nrm.inputs[0])
sep2 = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(nrm.outputs[0], sep2.inputs[0])
mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs[1].default_value = 0.0; mr.inputs[2].default_value = 0.8
nt.links.new(sep2.outputs["Z"], mr.inputs[0])
ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = hexc("#212B54"); ramp.color_ramp.elements[1].color = hexc("#060917")
nt.links.new(mr.outputs[0], ramp.inputs[0])
vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.feature = "DISTANCE_TO_EDGE" if False else "F1"; vor.inputs["Scale"].default_value = 90
vor.voronoi_dimensions = "4D"; vor.inputs["Randomness"].default_value = 1.0
nt.links.new(nrm.outputs[0], vor.inputs["Vector"])
sr = nt.nodes.new("ShaderNodeMapRange"); sr.inputs[1].default_value = 0.0; sr.inputs[2].default_value = 0.045; sr.inputs[3].default_value = 1.0; sr.inputs[4].default_value = 0.0
nt.links.new(vor.outputs["Distance"], sr.inputs[0])
stars = nt.nodes.new("ShaderNodeMath"); stars.operation = "MULTIPLY"; stars.inputs[1].default_value = 14.0
nt.links.new(sr.outputs[0], stars.inputs[0])
sm = nt.nodes.new("ShaderNodeMath"); sm.operation = "MULTIPLY"
nt.links.new(stars.outputs[0], sm.inputs[0]); nt.links.new(mr.outputs[0], sm.inputs[1])
mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "ADD"; mix.inputs[0].default_value = 1.0
nt.links.new(ramp.outputs[0], mix.inputs[6])
sc_col = nt.nodes.new("ShaderNodeCombineColor");
for i in range(3): nt.links.new(sm.outputs[0], sc_col.inputs[i])
nt.links.new(sc_col.outputs[0], mix.inputs[7])
bg = nt.nodes.new("ShaderNodeBackground"); nt.links.new(mix.outputs[2], bg.inputs[0])
bg2 = nt.nodes.new("ShaderNodeBackground"); nt.links.new(ramp.outputs[0], bg2.inputs[0]); bg2.inputs["Strength"].default_value = 5.0
lp = nt.nodes.new("ShaderNodeLightPath"); mixs = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mixs.inputs[0]); nt.links.new(bg2.outputs[0], mixs.inputs[1]); nt.links.new(bg.outputs[0], mixs.inputs[2])
wo = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mixs.outputs[0], wo.inputs[0])
WORLD_BG2 = bg2
WORLD_BG = bg
SKY_MAP = mr
# sky dome rotation drives star twinkle/drift: rotate the vector via mapping on Generated is skipped; stars drift via vor w
moon = light("moon", "SUN", 0.55, hexc("#9EB8FF"), (0, 0, 50), radius=0.02)
moon.data.angle = math.radians(1.0)
moon.rotation_euler = Euler((math.radians(52), math.radians(8), math.radians(-35)))
moon_disc = bpy.data.objects.new("moon_disc", bpy.data.meshes.new("md")); sc.collection.objects.link(moon_disc)
bpy.ops.mesh.primitive_uv_sphere_add(radius=14, location=(-380, 520, 330)); md = bpy.context.object
md.data.materials.append(mat("moon_disc", hexc("#9EB8FF"), emit=3.0)); MOON_MAT = md.data.materials[0]
bpy.data.objects.remove(moon_disc)

# ------------------------------------------------------------------ ground
def noise_mat(name, c0, c1, scale):
    m = bpy.data.materials.new(name); m.use_nodes = True; n = m.node_tree.nodes; l = m.node_tree.links
    b = n["Principled BSDF"]; b.inputs["Roughness"].default_value = 1.0
    t = n.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = 4
    r = n.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = hexc(c0); r.color_ramp.elements[1].color = hexc(c1)
    l.new(t.outputs["Fac"], r.inputs[0]); l.new(r.outputs[0], b.inputs["Base Color"]); return m
grass = noise_mat("grass", "#336B24", "#42802B", 0.35)
road = noise_mat("road", "#212126", "#2E2E33", 0.6)
g = box("grass", (700, 400, 1), (0, 0, -0.5), grass)
r = box("road", (700, 16, 1.02), (0, 0, -0.5), road)
walk = mat("walk", hexc("#6E7488"))
for y in (-11, 11): box("sidewalk", (700, 6, 1.1), (0, y, -0.45), walk)
yel = mat("yellow", hexc("#FAC726"), emit=0.0)
for x in range(-340, 340, 14): box("line", (7, 0.6, 1.05), (x, 0, -0.45), yel)

# ------------------------------------------------------------------ houses
HOUSE_X = list(range(-135, 136, 30))
wall_cols = ["#B4543A", "#3F7CAC", "#C9A14A", "#6B4E9E", "#4F8F5F", "#A83A55", "#2D8A8A", "#C86A2F", "#7A8F3A", "#456EA9"]
win_mat = mat("window", hexc("#FCC773"), emit=3.0)
porch_mat = mat("porchbulb", hexc("#FFD9A0"), emit=6.0)
dark_mat = mat("black_inside", hexc("#050506"))
roof_mat = mat("roof", hexc("#2A2530"))
door_mat = mat("door", hexc("#5B3A22"))
HOUSES = {}
LIGHTS_CULL = []
for side, ys, fy in (("N", 1, 24.0), ("S", -1, -24.0)):
    for i, x in enumerate(HOUSE_X):
        c = hexc(wall_cols[(i * 3 + (0 if side == "N" else 4)) % len(wall_cols)])
        wm = mat(f"wall{side}{i}", c)
        hroot = empty(f"house{side}{i}", (x, fy, 0))
        box("body", (20, 16, 11), (0, 8, 5.5), wm, hroot)
        box("roof", (22, 18, 3), (0, 8, 12.5), roof_mat, hroot)
        box("chimney", (2, 2, 5), (6, 11, 15), roof_mat, hroot)
        # front face is at y = -ys*0 : local y=0 plane faces street
        box("dark", (4.6, 0.3, 8.0), (0, -0.15, 4.0), dark_mat, hroot)
        hinge = empty("hinge", (-2.3, -0.45, 0), hroot)
        box("leaf", (4.6, 0.4, 8.0), (2.3, 0, 4.0), door_mat, hinge)
        for wx in (-7, 7):
            box("win", (3.6, 0.3, 3.6), (wx, -0.1, 6.4), win_mat, hroot)
        box("porchbulb", (0.7, 0.7, 0.7), (3.6, -1.2, 9.2), porch_mat, hroot)
        pl = light(f"porch{side}{i}", "POINT", 650, hexc("#FFD9A0"), (x + (3.6 if ys == 1 else -3.6), fy - ys * 2.0, 9.0), radius=0.3)
        pl.data.use_shadow = False
        HOUSES[(side, i)] = {"root": hroot, "hinge": hinge, "x": x, "ys": ys, "porch": pl, "front_y": fy}
        LIGHTS_CULL.append(pl)
        if side == "S": hroot.rotation_euler.z = math.pi  # S houses face +y ; flip so local -y faces street...
# For S side: root rotated 180deg about z so local +y points to -y world (away from street); local -ys*... handled by rotation
for (side, i), h in HOUSES.items():
    if side == "N": h["root"].rotation_euler.z = 0.0
    # N: local +y (ys=+1) is toward back (+world y); front = local y=0. Porch light local -y toward street -> world y smaller: ok
SHUT = []
_h5 = HOUSES[("N", 5)]["root"]
for hx, sgn in ((-8.8, 1), (-5.2, -1)):
    hp = empty("shutter_hinge", (hx, -0.35, 6.4), _h5); box("flap", (1.8, 0.2, 3.8), (sgn * 0.9, 0, 0), mat("shutter", hexc("#2F5D3A")), hp); SHUT.append((hp, sgn))
NOAH_HOUSE = ("N", 3)     # x=-45
NEIGH_HOUSE = ("N", 4)    # x=-15
assert HOUSES[NOAH_HOUSE]["x"] == -45 and HOUSES[NEIGH_HOUSE]["x"] == -15

# ------------------------------------------------------------------ lamps (13.2 tall, 30 apart)
pole_mat = mat("pole", hexc("#1B1B22"))
LAMPS = []
for k, x in enumerate(range(-105, 106, 30)):
    is_last = (x == -15)
    y = 11 if is_last else -11
    p = empty(f"lamp{k}", (x, y, 0))
    box("pole", (0.5, 0.5, 13.2), (0, 0, 6.6), pole_mat, p)
    box("arm", (0.4, 3.0, 0.4), (0, 1.6 if y < 0 else -1.6, 13.0), pole_mat, p)
    bm = bpy.data.materials.new(f"bulb{k}"); bm.use_nodes = True
    bm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1
    off = (0, 3.0 if y < 0 else -3.0, 12.7)
    if is_last:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(x, y, 12.9)); gl = bpy.context.object; gl.parent = p
        gl.location = (0, 0, 12.9); gl.data.materials.append(bm); gl.data.polygons.foreach_set("use_smooth", [True] * len(gl.data.polygons))
        L = light(f"lampL{k}", "POINT", 9000, hexc("#FFBD6B"), (x, y, 12.5), radius=0.6)
    else:
        box("bulb", (1.4, 1.4, 0.6), off, bm, p)
        L = light(f"lampL{k}", "SPOT", 4200, hexc("#FFBD6B"), (x + off[0], y + off[1], 12.4), cone=118, blend=0.35, radius=0.5)
        L.rotation_euler = Euler((0, 0, 0))   # points -Z
    LAMPS.append({"x": x, "y": y, "bulb": bm, "light": L, "last": is_last, "e": L.data.energy, "emit": 14 if is_last else 9})
    LIGHTS_CULL.append(L)
LAST = [l for l in LAMPS if l["last"]][0]

# ------------------------------------------------------------------ street props: swing set, rocking chair, clock, cap, shutters
swing_root = empty("swing", (60, -17, 0)); sw_top = box("swtop", (0.4, 12, 0.4), (0, 0, 9), pole_mat, swing_root)
for sy in (-5.8, 5.8): box("swleg", (0.4, 0.4, 9), (0, sy, 4.5), pole_mat, swing_root, rot=(0, 0, 0))
swing_piv = empty("swpiv", (0, 0, 9), swing_root)
box("chain", (0.12, 0.12, 5), (0, 0, -2.5), pole_mat, swing_piv); box("seat", (1.6, 3.0, 0.3), (0, 0, -5.1), mat("seat", hexc("#E0463C")), swing_piv)
chair_root = empty("chair", (22, 17, 0))  # on a porch-ish spot, north sidewalk side (overridden for wide shots)
chair_piv = empty("chpiv", (0, 0, 0), chair_root)
cm = mat("chair", hexc("#C07A32"))
box("cseat", (3, 3, 0.4), (0, 0, 2.3), cm, chair_piv); box("cback", (3, 0.4, 3.6), (0, -1.4, 4.2), cm, chair_piv)
for sx in (-1.3, 1.3): box("crock", (0.35, 4.2, 0.35), (sx, 0, 0.3), cm, chair_piv)
capm = mat("cap", hexc("#EC1C24"))
cap_root = empty("capG", (-78, 9.2, 0)); cap_piv = empty("cappiv", (0, 0, 0.6), cap_root)
box("capdome", (1.8, 1.8, 0.9), (0, 0, 0.3), capm, cap_piv); box("capbill", (1.8, 1.0, 0.2), (0, 1.3, 0.0), capm, cap_piv)
clock_root = empty("clock", (-75, 23.6, 9.7), None)
box("cface", (3.2, 0.3, 3.2), (0, 0, 0), mat("cface", hexc("#F2F2F2")), clock_root)
hand_piv = empty("hands", (0, -0.25, 0), clock_root); box("sec", (0.12, 0.1, 1.4), (0, 0, 0.7), mat("sech", hexc("#EC1C24")), hand_piv)
box("min", (0.25, 0.1, 1.0), (0, 0.05, 0.5), pole_mat, clock_root)

# ------------------------------------------------------------------ characters
head_yel = mat("skin", hexc("#F5CD30"))
FACE_IMG = {}
def face_mat(name):
    if name in FACE_IMG: return FACE_IMG[name]
    m = bpy.data.materials.new("face_" + name); m.use_nodes = True; n = m.node_tree.nodes; l = m.node_tree.links
    n.clear(); out = n.new("ShaderNodeOutputMaterial")
    img = bpy.data.images.load(ROOT + f"build/faces/{name}.png"); img.alpha_mode = "STRAIGHT"
    t = n.new("ShaderNodeTexImage"); t.image = img; t.interpolation = "Linear"
    if name == "monster":
        em = n.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1, 1, 1, 1); em.inputs["Strength"].default_value = 6.0
        tr = n.new("ShaderNodeBsdfTransparent"); mx = n.new("ShaderNodeMixShader")
        l.new(t.outputs["Alpha"], mx.inputs[0]); l.new(tr.outputs[0], mx.inputs[1]); l.new(em.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
        m.node_tree.nodes["Material Output"] if False else None
    else:
        bsdf = n.new("ShaderNodeBsdfDiffuse"); bsdf.inputs["Color"].default_value = (0, 0, 0, 1)
        tr = n.new("ShaderNodeBsdfTransparent"); mx = n.new("ShaderNodeMixShader")
        l.new(t.outputs["Alpha"], mx.inputs[0]); l.new(tr.outputs[0], mx.inputs[1]); l.new(bsdf.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"): m.surface_render_method = "DITHERED"
    FACE_IMG[name] = m; return m
def face_patch(name, radius, height, parent, loc, deg=130, seg=26):
    me = bpy.data.meshes.new(name); verts = []; faces = []; uvs = []
    for i in range(seg + 1):
        a = math.radians(-deg / 2 + deg * i / seg)
        for j, z in enumerate((-height / 2, height / 2)):
            verts.append((math.sin(a) * radius, math.cos(a) * radius, z))
    for i in range(seg): faces.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    me.from_pydata(verts, [], faces); me.update()
    uv = me.uv_layers.new(name="UV")
    for poly in me.polygons:
        for li in poly.loop_indices:
            vi = me.loops[li].vertex_index; i, j = divmod(vi, 2); uv.data[li].uv = (i / seg, j)
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.parent = parent; o.location = loc
    me.materials.append(face_mat("smile")); return o

class Kid:
    def __init__(self, name, scale, torso, legs, skin="#F5CD30", cap=False):
        self.name = name; s = scale
        self.root = empty(name, (0, 0, 2 * s)); self.root.scale = (s, s, s)
        self.body = empty(name + "_body", (0, 0, 0), self.root)
        tm, lm = mat(f"{name}_t", hexc(torso)), mat(f"{name}_l", hexc(legs)); skm = mat(f"{name}_s", hexc(skin)); shoe = mat(f"{name}_sh", hexc("#1B1B22"))
        box("torso", (2, 1, 2), (0, 0, 1.0), tm, self.body)
        hd = empty("headpiv", (0, 0, 2.0), self.body); self.headpiv = hd
        bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=1.22, vertices=32, location=(0, 0, 0)); h = bpy.context.object
        h.parent = hd; h.location = (0, 0, 0.61); h.data.materials.append(skm)
        bv = h.modifiers.new("bev", "BEVEL"); bv.width = 0.22; bv.segments = 3
        h.data.polygons.foreach_set("use_smooth", [True] * len(h.data.polygons))
        self.face = face_patch(name + "_face", 0.64, 0.9, hd, (0, 0, 0.61)); self.facename = "smile"
        self.arms = []; self.legs = []
        for sx in (-1, 1):
            ap = empty("arm", (sx * 1.5, 0, 1.9), self.body); box("arm", (1, 1, 2), (0, 0, -1), skm if False else tm, ap)
            box("hand", (1.02, 1.02, 0.5), (0, 0, -1.85), skm, ap); self.arms.append(ap)
            lp = empty("leg", (sx * 0.5, 0, 0), self.body); box("leg", (1, 1, 1.62), (0, 0, -0.81), lm, lp)
            box("shoe", (1.02, 1.04, 0.38), (0, 0.02, -1.81), shoe, lp); self.legs.append(lp)
        if cap:
            cm_ = mat("headcap", hexc("#EC1C24")); box("capdome", (1.35, 1.35, 0.45), (0, 0, 1.38), cm_, hd); box("capbill", (1.2, 0.8, 0.12), (0, 0.9, 1.2), cm_, hd)
            self.cap_parts = list(hd.children)[-2:]
        self.base_scale = s
    def set_face(self, name):
        if name != self.facename:
            self.face.data.materials[0] = face_mat(name); self.facename = name

NOAH = Kid("Noah", 1.0, "#1E78D2", "#2B3A67")
SIS = Kid("Sis", 0.8, "#FF4FA3", "#6B2D8F")
BOY = Kid("Boy", 1.0, "#F29A1A", "#3C3C46", cap=True)
KIDS = [Kid(f"K{i}", 1.0 if i % 2 else 0.9, c, l) for i, (c, l) in enumerate(
    [("#28B463", "#2B3A67"), ("#E74C3C", "#34495E"), ("#9B59B6", "#2C3E50"), ("#F1C40F", "#1F618D")])]
ALL_KIDS = [NOAH, SIS, BOY] + KIDS
flash_mat = mat("flashbody", hexc("#2A2A30"))
flash_body = box("flashlight", (0.5, 1.4, 0.5), (0, 0, 0), flash_mat)
flash_spot = light("flash", "SPOT", 1400, hexc("#FFF3D6"), (0, 0, 0), cone=34, blend=0.25, radius=0.1)
bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=3.6, depth=22, vertices=24, location=(0, 0, 0)); beam = bpy.context.object
bm_ = bpy.data.materials.new("beam"); bm_.use_nodes = True; nn = bm_.node_tree.nodes; ll = bm_.node_tree.links; nn.clear()
em = nn.new("ShaderNodeEmission"); em.inputs["Color"].default_value = hexc("#FFF3D6"); em.inputs["Strength"].default_value = 0.6; tr = nn.new("ShaderNodeBsdfTransparent"); mx = nn.new("ShaderNodeMixShader"); o_ = nn.new("ShaderNodeOutputMaterial")
mx.inputs[0].default_value = 0.06; ll.new(tr.outputs[0], mx.inputs[1]); ll.new(em.outputs[0], mx.inputs[2]); ll.new(mx.outputs[0], o_.inputs[0])
if hasattr(bm_, "surface_render_method"): bm_.surface_render_method = "BLENDED"
beam.data.materials.append(bm_); beam.hide_render = True; beam.visible_shadow = False

# monster
class Monster:
    def __init__(self):
        mm = mat("monster", hexc("#0D0D0F")); self.root = empty("Monster", (0, 0, 0)); self.legs = []
        for sx in (-1, 1):
            lp = empty("mleg", (sx * 0.55, 0, 4.4), self.root); box("mlegbox", (0.62, 0.62, 4.4), (0, 0, -2.2), mm, lp); self.legs.append(lp)
        self.upper = empty("upper", (0, 0, 4.4), self.root)
        box("chest", (1.6, 0.7, 3.4), (0, 0, 1.7), mm, self.upper)
        self.headpiv = empty("mheadpiv", (0, 0, 3.4), self.upper)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.86, depth=1.8, vertices=32, location=(0, 0, 0)); h = bpy.context.object
        h.parent = self.headpiv; h.location = (0, 0, 0.9); h.data.materials.append(mm); h.modifiers.new("b", "BEVEL").width = 0.2
        self.face = face_patch("mface", 0.88, 1.2, self.headpiv, (0, 0, 0.9)); self.face.data.materials[0] = face_mat("monster")
        self.arms = []
        for sx in (-1, 1):
            ap = empty("marm", (sx * 1.1, 0, 3.3), self.upper); box("marmbox", (0.34, 0.34, 5.8), (0, 0, -2.9), mm, ap)
            for fi, fx in enumerate((-0.2, 0, 0.2)):
                fp = empty("fing", (fx, 0, -5.8), ap); box("finger", (0.1, 0.1, 1.1), (0, 0, -0.55), mm, fp, rot=(math.radians(8), 0, 0))
            self.arms.append(ap)
MON = Monster()

# ------------------------------------------------------------------ camera
camd = bpy.data.cameras.new("cam"); camd.sensor_fit = "VERTICAL"; camd.sensor_height = 36.0; camd.clip_start = 0.3; camd.clip_end = 900
cam = bpy.data.objects.new("cam", camd); sc.collection.objects.link(cam); sc.camera = cam
def look(cam, pos, tgt, roll=0.0):
    cam.location = pos
    d = Vector(tgt) - Vector(pos); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    if roll: cam.rotation_euler.rotate_axis("Z", roll)
def set_fov(deg): camd.lens = 18.0 / math.tan(math.radians(deg) / 2.0)


# ------------------------------------------------------------------ per-frame state
POSES = {  # larm, rarm, lleg, rleg, lean, headyaw, headpitch  (degrees; +arm = forward swing)
    "idle": (0, 0, 0, 0, 0, 0, 0), "walk": (0, 0, 0, 0, 0, 0, 0), "scared": (35, 35, 0, 0, -6, 0, -8),
    "panic": (150, 150, 0, 0, -10, 0, -10), "look": (20, 20, 0, 0, -8, 150, 0), "point": (0, 95, 0, 0, 0, 0, 0),
    "grab": (0, 60, 0, 0, 3, 0, -6), "flash": (0, 52, 0, 0, 3, 0, 0), "brace": (60, 60, 0, 0, 0, 0, -12), "pound": (0, 90, 0, 0, 3, 0, -8),
    "crouch": (50, 50, 55, 55, 10, 0, 0), "side": (0, 70, 0, 0, 3, -85, 0),
}
def lerp(a, b, k): return a + (b - a) * k
def track_val(ev, t, dur=0.14, ease=back):
    """ev: list of (t, vec). hold then snap with back ease. returns vec"""
    cur = None; prev = None
    for i, e in enumerate(ev):
        if e[0] <= t: cur = e; prev = ev[i - 1] if i else e
    if cur is None: return ev[0][1]
    k = ease((t - cur[0]) / dur)
    return tuple(lerp(p, c, k) for p, c in zip(prev[1], cur[1]))
def wp_val(wps, t):
    if t <= wps[0][0]: return wps[0][1:]
    for a, b in zip(wps, wps[1:]):
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / max(1e-6, b[0] - a[0]); return tuple(lerp(p, q, k) for p, q in zip(a[1:], b[1:]))
    return wps[-1][1:]
def ang_wp(wps, t):  # waypoints (t,x,y,rotdeg) with angle interp shortest
    if t <= wps[0][0]: return wps[0][1:]
    for a, b in zip(wps, wps[1:]):
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / max(1e-6, b[0] - a[0]); d = ((b[3] - a[3] + 180) % 360) - 180
            return (lerp(a[1], b[1], k), lerp(a[2], b[2], k), a[3] + d * k)
    return wps[-1][1:]

def apply_kid(kid, spec, t):
    vis = any(a <= t <= b for a, b in spec["vis"]) if spec.get("vis") else True
    hide(kid.root, not vis)
    if not vis: return
    x, y, rz = ang_wp(spec["wp"], t)
    gait = None
    for a, b, g in spec.get("gait", []):
        if a <= t <= b: gait = g
    pose = track_val(spec["pose"], t) if spec.get("pose") else POSES["idle"]
    larm, rarm, lleg, rleg, lean, hyaw, hpit = pose
    s = kid.base_scale; bob = 0.0
    if gait in ("run", "walk"):
        f, la, aa = (2.5, 52, 58) if gait == "run" else (1.8, 28, 32)
        ph = 2 * math.pi * f * t + spec.get("phase", 0); sw = math.sin(ph)
        lleg, rleg = la * sw, -la * sw
        larm, rarm = -aa * sw, aa * sw
        if gait == "run": lean = 9
        if spec.get("flasharm") and gait == "run": rarm = 52
        bob = 0.25 * s * abs(math.cos(ph))
    else:
        hyaw += 4 * math.sin(2 * math.pi * 0.5 * t + spec.get("phase", 0))   # idle sway so nothing is dead still
        bob = 0.05 * math.sin(2 * math.pi * 0.9 * t)
    kid.root.location = (x, y, 2 * s + bob); kid.root.rotation_euler = (0, 0, math.radians(rz))
    kid.body.rotation_euler = (-math.radians(lean), 0, 0)
    kid.arms[0].rotation_euler.x = math.radians(larm); kid.arms[1].rotation_euler.x = math.radians(rarm)
    kid.legs[0].rotation_euler.x = math.radians(lleg); kid.legs[1].rotation_euler.x = math.radians(rleg)
    kid.headpiv.rotation_euler = (math.radians(hpit), 0, math.radians(hyaw))
    if spec.get("face"):
        fe = [e for e in spec["face"] if e[0] <= t]; kid.set_face(fe[-1][1] if fe else spec["face"][0][1])

def flick(t, t_dead):
    """lit while sum of two sines > -0.25 during the 0.12 s before death, dead after"""
    if t >= t_dead: return 0.0
    if t >= t_dead - 0.12: return 1.0 if (math.sin(61 * t) + math.sin(37 * t)) > -0.25 else 0.0
    return 1.0

def update(frame):
    t = frame / FPS
    # kids
    for kid, spec in KID_SPECS: apply_kid(kid, spec, t)
    # monster
    apply_monster(t)
    sh = shot_at(t)
    p0, t0, p1, t1 = sh["c0"], sh["t0"], sh.get("c1", sh["c0"]), sh.get("t1", sh["t0"])
    k = smooth((t - sh["start"]) / max(1e-6, sh["end"] - sh["start"]))
    def res(v): return resolve(v, t)
    pos = tuple(lerp(a, b, k) for a, b in zip(res(p0), res(p1))); tg = tuple(lerp(a, b, k) for a, b in zip(res(t0), res(t1)))
    look(cam, pos, tg, math.radians(sh.get("roll", 0))); set_fov(sh["fov"] + (sh.get("fov1", sh["fov"]) - sh["fov"]) * k)
    # props
    swing_piv.rotation_euler.x = math.radians(12 * math.sin(2 * math.pi * 0.38 * t))
    chair_piv.rotation_euler.x = math.radians(9 * math.sin(2 * math.pi * 0.75 * t))
    hand_piv.rotation_euler.y = -math.radians(6 * math.floor(t))     # second hand ticks once per second
    cap_piv.rotation_euler.y = math.radians(14 * math.sin(2 * math.pi * 0.9 * t))
    hide(cap_root, t < T(20) + 0.0)
    for hp, sgn in SHUT:
        hp.rotation_euler.z = math.radians(-sgn * 100 * (1 - back((t - T(35)) / 0.14)) if t >= T(35) else -sgn * 100)
    # world states
    dark = in_blackout(t)
    for L in LAMPS:
        on = lamp_on(L, t)
        setemit(L["bulb"], hexc("#FFBD6B") if on else hexc("#2A2A2E"), L["emit"] if on else 0.0)
        L["light"].data.energy = L["e"] if on else 0.0
    wl = 0.0 if dark else (3.0)
    setemit(win_mat, hexc("#FCC773"), wl if windows_lit(t) else 0.0)
    setemit(porch_mat, hexc("#FFD9A0"), 0.0 if dark else 6.0)
    for h in HOUSES.values(): h["porch"].data.energy = 0.0 if dark else 650
    for hk, h in HOUSES.items():
        h["hinge"].rotation_euler.z = math.radians(door_angle(hk, t))
    bg.inputs["Strength"].default_value = 0.12 if dark else 1.0; WORLD_BG2.inputs["Strength"].default_value = 0.08 if dark else 5.0
    moon.data.energy = 0.04 if dark else 0.55
    setemit(MOON_MAT, hexc("#9EB8FF"), 0.04 if dark else 3.0)
    # flashlight
    on = flash_on(t); fx = flash_pose(t)
    flash_spot.data.energy = 1400 if on else 0.0
    beam.hide_render = not on
    if fx:
        origin, direction = fx
        flash_body.location = origin; flash_spot.location = origin
        q = Vector(direction).to_track_quat("-Z", "Y"); flash_spot.rotation_euler = q.to_euler(); beam.rotation_euler = Vector(direction).to_track_quat("Z", "Y").to_euler()
        beam.location = Vector(origin) + Vector(direction).normalized() * 11.0
        flash_body.rotation_euler = q.to_euler()
    flash_body.hide_render = fx is None
    # light culling: only lights near the camera (keeps Eevee fast)
    for Lo in LIGHTS_CULL:
        near = (Lo.location - Vector(pos)).length < 85
        Lo.hide_render = not near
    # sky drift so empty dark shots still move
    for n in (vor,): n.inputs["W"].default_value = t * 0.02 if "W" in n.inputs else 0
    sc.frame_current = frame

def on_frame(scene, *a): update(scene.frame_current)
bpy.app.handlers.frame_change_pre.clear(); bpy.app.handlers.frame_change_pre.append(on_frame)
bpy.app.handlers.render_pre.clear(); bpy.app.handlers.render_pre.append(lambda s, *a: update(s.frame_current))

exec(open(ROOT + "code/shots.py").read())
# ------------------------------------------------------------------ run
sc.frame_start, sc.frame_end = 0, int(END_T * FPS)
os.makedirs(OUT, exist_ok=True)
if MODE == "stills":
    for i, sh in enumerate(SHOTS):
        mid = int(((sh["start"] + sh["end"]) / 2) * FPS)
        sc.frame_set(mid); update(mid)
        sc.render.filepath = f"{OUT}/s{i:02d}_f{mid}.png"; bpy.ops.render.render(write_still=True)
        print("still", i, mid, flush=True)
elif MODE == "frame":
    f = int(sys.argv[3]); update(f); sc.render.filepath = f"{OUT}/f{f}.png"; bpy.ops.render.render(write_still=True)
else:
    a, b = RANGE if RANGE else (sc.frame_start, sc.frame_end)
    sc.render.filepath = OUT + "/f_"; sc.frame_start, sc.frame_end = a, b
    bpy.ops.render.render(animation=True)
