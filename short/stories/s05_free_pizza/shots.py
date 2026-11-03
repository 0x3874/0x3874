# Story 5 "Free Pizza" -- kitchen at RX,RY; Noah stands on the table and shrinks with every slice
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.5
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
RX, RY = 300.0, 300.0
def P(x, y, z=0.0): return (RX + x, RY + y, z)
TT = 3.4                                   # table top height
hide(cap_root, True); hide(MON.root, True)
for k_ in (BOY,) + tuple(KIDS): hide(k_.root, True)
tile_a = mat("tileA", hexc("#F2EBD3")); tile_b = mat("tileB", hexc("#3AA0A0")); wall_m = mat("kwall", hexc("#F2B544"))
for i_ in range(-5, 5):
    for j_ in range(-5, 5): box("tile", (3, 3, 0.4), P(i_ * 3 + 1.5, j_ * 3 + 1.5, -0.2), tile_a if (i_ + j_) % 2 == 0 else tile_b)
box("kback", (30, 1, 14), P(0, 15.5, 7), wall_m); box("kleft", (1, 31, 14), P(-15.5, 0, 7), wall_m); box("kright", (1, 31, 14), P(15.5, 0, 7), wall_m)
box("kceil", (31, 31, 0.5), P(0, 0, 14.25), wall_m)
box("kwin", (7, 0.3, 5.5), P(-6, 14.9, 8), mat("kwinglow", hexc("#9EB8FF"), emit=1.4))
box("cab", (10, 3, 6.5), P(8, 13.8, 3.25), mat("cab", hexc("#8C5A3A"))); box("cabtop", (10.4, 3.4, 0.5), P(8, 13.8, 6.7), mat("cabtop", hexc("#CFCFD8")))
# table
tbl = mat("table", hexc("#B07A45"))
box("tabletop", (22, 13, 0.8), P(0, 2, TT - 0.4), tbl)
for lx, ly in ((-10, -3.6), (10, -3.6), (-10, 7.6), (10, 7.6)): box("tleg", (0.9, 0.9, TT - 0.8), P(lx, ly, (TT - 0.8) / 2), tbl)
# pizza: 8 wedges that can be eaten
cheese_m = mat("cheese", hexc("#F5B82E")); crust_m = mat("crust", hexc("#C7852E")); pep_m = mat("pep", hexc("#C0392B"))
def make_wedge(i, r=5.6, h=0.6, n=6, ctr=(0, 2)):
    a0, a1 = math.radians(i * 45), math.radians((i + 1) * 45)
    me = bpy.data.meshes.new(f"wedge{i}"); V = []; F = []
    V.append((0, 0, h)); V.append((0, 0, 0))
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n; V.append((math.cos(a) * r, math.sin(a) * r, h)); V.append((math.cos(a) * r, math.sin(a) * r, 0))
    for k in range(n):
        t0, b0, t1, b1 = 2 + 2 * k, 3 + 2 * k, 4 + 2 * k, 5 + 2 * k
        F += [(0, t0, t1), (1, b1, b0), (t0, b0, b1, t1)]
    F += [(0, 1, 3, 2), (0, 2 + 2 * n, 3 + 2 * n, 1)]
    me.from_pydata(V, [], F); me.update(); me.materials.append(cheese_m)
    o = bpy.data.objects.new(f"wedge{i}", me); sc.collection.objects.link(o); o.location = (RX + ctr[0], RY + ctr[1], TT + 0.0)
    for p_ in me.polygons: p_.use_smooth = False
    # crust ring + pepperoni as children
    am = (a0 + a1) / 2
    box("crustpiece", (1.0, 4.4, h + 0.35), (math.cos(am) * (r - 0.35), math.sin(am) * (r - 0.35), (h + 0.35) / 2), crust_m, o, rot=(0, 0, am))
    box("pep", (0.9, 0.9, 0.18), (math.cos(am) * 3.2, math.sin(am) * 3.2, h + 0.05), pep_m, o)
    return o
WEDGES = [make_wedge(i) for i in range(8)]
# pizza box, ladder
box("pbox", (12.5, 12.5, 0.7), P(0, 2, TT + 0.35 - 0.001 - 0.7 + 0.0), mat("boxbase", hexc("#E8D6B0")))
LID = empty("lid", P(0, 8.6, TT + 0.2)); box("lidslab", (12.5, 0.4, 9.5), (0, 0, 4.0), mat("boxlid", hexc("#D9B779")), LID); box("lidtext", (6.5, 0.45, 2.0), (0, -0.05, 4.8), mat("boxred", hexc("#E23B2E")), LID)
LADDER = empty("ladder", P(-6.6, 2, TT))
for lx in (-0.5, 0.5): box("rail", (0.12, 0.12, 2.6), (lx, 0, 1.3), mat("lad", hexc("#8C5A3A")), LADDER)
for z_ in (0.5, 1.1, 1.7, 2.3): box("rung", (1.0, 0.1, 0.1), (0, 0, z_), mat("lad", hexc("#8C5A3A")), LADDER)
_l1 = light("kitchenlamp", "POINT", 1200, hexc("#FFD9A0"), P(0, 1, 14), radius=0.8); LIGHTS_CULL.append(_l1)
_l2 = light("kitchenfill", "POINT", 500, hexc("#9EB8FF"), P(-6, 10, 9), radius=0.8); _l2.data.use_shadow = False; LIGHTS_CULL.append(_l2)
# goat chef
class Goat:
    def __init__(self):
        wm = mat("goatwhite", hexc("#EFEAD8")); hm = mat("horn", hexc("#C9B98A"))
        self.root = empty("Goat", P(0, 10.0, 0)); self.piv = empty("goatpiv", (0, 0, 0), self.root)
        box("gbody", (1.9, 3.2, 2.1), (0, 0, 2.8), wm, self.piv); box("apron", (2.1, 1.6, 2.2), (0, 0, 2.85), mat("apron", hexc("#F4F4F4")), self.piv)
        for lx, ly in ((-0.6, -1.1), (0.6, -1.1), (-0.6, 1.1), (0.6, 1.1)): box("gleg", (0.55, 0.55, 1.7), (lx, ly, 0.85), wm, self.piv)
        self.head = empty("ghead", (0, -1.7, 4.4), self.piv); box("gh", (1.4, 1.6, 1.5), (0, -0.3, 0.4), wm, self.head)
        for sx_ in (-0.5, 0.5): box("horn", (0.28, 0.28, 0.9), (sx_, 0.1, 1.5), hm, self.head, rot=(0, math.radians(sx_ * 25), 0))
        box("hatband", (1.5, 1.5, 0.4), (0, -0.2, 1.3), mat("hat", hexc("#F4F4F4")), self.head); box("hat", (1.3, 1.3, 1.6), (0, -0.2, 2.2), mat("hat", hexc("#F4F4F4")), self.head)
        box("beard", (0.3, 0.3, 0.7), (0, -1.0, -0.2), hm, self.head)
        self.face = face_patch("gface", 0.95, 1.0, self.head, (0, -0.3, 0.4), deg=90); self.face.rotation_euler.z = math.pi; self.face.data.materials[0] = face_mat("smile"); self.facename = "smile"
GOAT = Goat(); HELD = make_wedge(7); HELD.parent = GOAT.head; HELD.location = (0, -1.6, -0.3); HELD.scale = (0.5, 0.5, 0.5); HELD.rotation_euler = (math.radians(70), 0, math.radians(90))
# ---------------------------------------------------------------- shots (N-relative coordinates scale with Noah)
NX, NY = -8.7, 2.0
def NS(t):
    return track_val([(a, (v,)) for a, v in ((0, 1.0), (T(30), 0.9), (T(37), 0.78), (T(44), 0.66), (T(51), 0.54), (T(59), 0.42), (T(78), 0.32), (T(88), 0.22))], t, 0.14)[0]
def resolve(v, t):
    if isinstance(v, tuple) and len(v) == 4 and v[0] == "N":
        s = NS(t); return (RX + NX + v[1] * s, RY + NY + v[2] * s, TT + v[3] * s)
    return v
C = []
def _ks(c, tg, fov):
    K = 2.0 if fov <= 34 else (1.7 if fov <= 48 else 1.25)
    if isinstance(c, tuple) and c[0] == "N" and isinstance(tg, tuple) and tg[0] == "N":
        return ("N",) + tuple(tg[i] + (c[i] - tg[i]) * K for i in (1, 2, 3))
    return (tg[0] + (c[0] - tg[0]) * K, tg[1] + (c[1] - tg[1]) * K, tg[2] + (c[2] - tg[2]) * K)
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=_ks(c0, t0, fov), t0=t0, fov=fov)
    if c1: d["c1"] = _ks(c1, t1 or t0, fov)
    if t1: d["t1"] = t1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
def N(dx, dy, dz): return ("N", dx, dy, dz)
S(0.0,      P(0, -14, 8), P(0, 2, 4), 52, c1=P(0, -12.5, 7.6))                                  # 1 the table
S(W(2),     N(0, -9, 2.6), N(0, 0, 2.4), 40, c1=N(0, -8, 2.6))                                  # 2 Noah got smaller
S(W(6),     P(3, -6, 7), P(0, 2, 4.2), 40, c1=P(2, -5, 6.6))                                    # 3 free pizza
S(W(12),    P(0, -4, 7), P(0, 8.6, 6.5), 40, c1=P(0, -3, 7))                                    # 4 the box said
S(W(15),    P(0, -3, 7.4), P(0, 8.6, 7.4), 36, c1=P(0, -2, 7.4))                                # 5 eat all eight slices
S(W(19),    N(0, -8, 2.8), N(0, 0, 2.5), 32, c1=N(0, -7, 2.8))                                  # 6 not a careful reader
S(W(25),    N(4, -9, 3), N(3, 0, 2.4), 40, c1=N(3, -8, 3))                                      # 7 first slice
S(W(30),    N(0, -6.5, 2.7), N(0, 0, 2.5), 30, c1=N(0, -5.5, 2.7))                              # 8 nothing happened
S(W(32),    N(4, -9, 3), N(3, 0, 2.4), 40, c1=N(3, -8, 3))                                      # 9 second slice
S(W(37),    N(0, -7, 1.2), N(0, 0, 1.3), 36, c1=N(0, -6, 1.2))                                  # 10 pants loose
S(W(41),    N(0, -8, 1.0), N(0, 0, 0.5), 34, c1=N(0, -7, 1.0))                                  # 11 shoes too big
S(W(49),    N(0, -10, 3), N(0, 0, 2.4), 44, c1=N(0, -9, 3))                                     # 12 shirt a tent
S(W(57),    P(0, -9, 6), P(0, 2, 4.2), 46, c1=P(0, -8, 5.8))                                    # 13 the fifth
S(W(60),    N(-3, -4, 0.6), N(4, 3, 1.5), 60, c1=N(-3, -3, 0.7))                                # 14 big as a bed
S(W(68),    N(0, -7, 2.7), N(0, 0, 2.4), 32, c1=N(0, -6, 2.7))                                  # 15 thought about stopping
S(W(72),    P(0, -1, 5.6), P(0, 2, 4.2), 34, c1=P(0, -0.5, 5.4))                                # 16 the cheese smelled so good
S(W(78),    N(-6, -10, 0.5), N(3, 0, 3), 64, c1=N(-6, -9, 0.6))                                 # 17 table a mountain
S(W(86),    N(0, -8, 2.0), N(0, 0, 1.8), 40, c1=N(0, -7, 2.0))                                  # 18 the seventh
S(W(89),    N(-4, -7, 2), N(2, 0, 3), 48, c1=N(-4, -6, 2.2))                                    # 19 ladder
S(W(97),    N(0, -7, 3), N(0, 0, 2.5), 44, c1=N(0, -6, 3))                                      # 20 climbed, slipped
S(W(103),   P(-6, -12, 5), P(8, -6, 3), 56, c1=P(-5, -11, 5))                                   # 21 sister walked in
S(W(108),   P(7, -8, 5.2), P(7, -4, 4), 34, c1=P(7, -7, 5.2))                                   # 22 empty plate
S(W(114),   P(2, -6, 7), P(0, 8.6, 6.4), 40, c1=P(2, -5, 7))                                    # 23 the box
S(W(119),   P(8, -8, 5.5), P(0, 4, 3.5), 50, c1=P(8, -7, 5.5))                                  # 24 around the room
S(W(124),   P(7, -8, 5.2), P(7, -4, 4), 30, c1=P(7, -7, 5.2))                                   # 25 Noah?
S(W(127),   N(0, -5, 1.5), N(0, 0, 1.2), 30, c1=N(0, -4, 1.5))                                  # 26 waved from the crust
S(W(132),   P(5, -9, 6), P(5, -3, 4.6), 40, c1=P(5, -8, 6))                                     # 27 picked him up
S(W(139),   P(6, -9, 5.2), P(6, -3, 4.4), 30, c1=P(6, -8, 5.2))                                 # 28 missed the small print
S(W(144),   P(6, -9, 5.2), P(6, -3, 4.4), 28, c1=P(6, -8.4, 5.2))                               # 29 she said
S(W(146),   P(0, -8, 7), P(0, 2, 4.2), 40, c1=P(0, -7, 6.8))                                    # 30 slice eight missing
S(W(150),   P(0, -6, 6), P(0, 10, 4.8), 46, c1=P(0, -4, 6))                                     # 31 a goat in a chef's
S(W(154),   P(0, 3, 5.6), P(0, 10, 5.2), 32, c1=P(0, 4, 5.6))                                   # 32 hat held it up
S(MON_T0 - 0.02, P(0, 4.5, 5.6), P(0, 10, 5.4), 26, c1=P(0, 5.5, 5.6))                          # 33 Extra cheese?
S(MON_END, P(0, -12, 7), P(0, 5, 4.5), 50, c1=P(0, -10, 7))                                     # 34 final hold
SHOTS = []
for i, (st, d) in enumerate(C):
    d["start"] = st; d["end"] = C[i + 1][0] if i + 1 < len(C) else END_T; SHOTS.append(d)
def shot_at(t):
    cur = SHOTS[0]
    for s_ in SHOTS:
        if s_["start"] <= t: cur = s_
    return cur
def in_blackout(t): return False
def lamp_on(L, t): return True
def windows_lit(t): return True
def door_angle(hk, t): return 0.0
def flash_on(t): return False
def flash_pose(t): return None
SHUT = []
def apply_monster(t): hide(MON.root, True)
def E(*p): return list(p)
NOAH_SPEC = dict(vis=[(0, END_T + 1)], wp=[(0, RX + NX, RY + NY, 180)],
    face=E((0, "smile"), (T(30), "shock"), (T(37), "stern"), (T(44), "scared"), (T(59), "scared"), (T(68), "determined"), (T(72), "smile"), (T(88), "panic"), (T(103), "scared"), (T(127), "smile"), (T(133), "shock"), (T(150), "shock")),
    pose=E((0, POSES["idle"]), (T(25), POSES["reach"]), (T(29), POSES["idle"]), (T(32), POSES["reach"]), (T(36), POSES["idle"]), (T(127), POSES["panic"]), (T(133), POSES["scared"])))
SIS_SPEC = dict(vis=[(T(103) - 0.2, END_T + 1)], wp=[(T(103) - 0.2, RX + 13, RY - 9, 57), (T(108), RX + 7, RY - 5.5, 57), (T(109), RX + 7, RY - 5.5, 0), (END_T + 1, RX + 7, RY - 5.5, 0)],
    face=E((0, "smile"), (T(108), "shock"), (T(124), "shock"), (T(139), "smile")), pose=E((0, POSES["idle"]), (T(131), POSES["reach"])), gait=[(T(103) - 0.2, T(108), "walk")], phase=0.5)
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC)]
for i_, tw in enumerate((29, 36, 48, 56, 67, 77, 97, 146)): pass
EAT = [T(29), T(36), T(48), T(56), T(67), T(77), T(97), T(146)]
def story_update(t):
    hide(cap_root, True)
    s = NS(t); climb = 0.0
    if T(97) <= t < T(103):
        u = (t - T(97)) / 5.0; climb = 1.6 * s * (smooth(min(1, u * 2)) if t < T(99) else (0 if t < (T(99) + 0.4) else smooth((t - (T(99) + 0.4)) / 1.2)))
    NOAH.root.scale = (s, s, s)
    NOAH.root.location = (RX + NX, RY + NY, TT + 2 * s + climb)
    if t >= T(133):
        bpy.context.view_layer.update()
        hp = SIS.arms[1].matrix_world @ Vector((0, 0.5, -1.9)); NOAH.root.location = (hp.x, hp.y, hp.z + 0.2 * s); NOAH.root.rotation_euler.z = math.radians(180)
    elif t < T(133): NOAH.root.rotation_euler.z = math.radians(180)
    for w_, te in zip(WEDGES, EAT): hide(w_, t >= te)
    hide(HELD, t < T(150)); hide(GOAT.root, t < T(149))
    LID.rotation_euler.x = math.radians(-18)
    hide(LADDER, not (T(88) <= t < T(133)))
    tilt = 24 * (back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0)
    GOAT.head.rotation_euler = (0, math.radians(tilt), 0)
