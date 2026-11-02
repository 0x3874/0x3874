# Story 4 "The Snowman" -- snowy front lawn at Noah's house (x=-45)
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.6
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
SX, SY = -45.0, 17.0
hide(cap_root, True); hide(MON.root, True)
for k_ in (BOY, KIDS[2], KIDS[3]): hide(k_.root, True)
snow_m = mat("snow", hexc("#E8F0FF")); snow2 = mat("snow2", hexc("#D3E1FA"))
box("snowfield", (700, 110, 0.3), (0, 70, 0.1), snow_m)
for hk, h in HOUSES.items():
    if hk[0] == "N": box("roofsnow", (22.4, 18.4, 0.7), (h["x"], 32, 14.3), snow_m)
# --- snowman (grows every night)
SM = empty("snowman", (SX, SY, 0)); coal = mat("coal", hexc("#1B1B22")); carrot = mat("carrot", hexc("#FF8A1F")); red_m = mat("scarfred", hexc("#EC1C24"))
box("sb", (4.4, 4.4, 3.2), (0, 0, 1.6), snow_m, SM); box("sm", (3.4, 3.4, 2.7), (0, 0, 4.55), snow_m, SM)
SHEAD = empty("shead", (0, 0, 6.0), SM); box("sh", (2.5, 2.5, 2.4), (0, 0, 1.2), snow_m, SHEAD)
for sx_ in (-0.6, 0.6): box("eye", (0.32, 0.2, 0.32), (sx_, -1.3, 1.55), coal, SHEAD)
box("nose", (0.35, 1.2, 0.35), (0, -1.7, 1.1), carrot, SHEAD)
for i_, sz_ in enumerate((3.6, 4.4, 5.2)): box("btn", (0.4, 0.2, 0.4), (0, -1.75, sz_), coal, SM)
box("armL", (0.3, 0.3, 2.8), (-2.4, 0, 5.1), mat("stick", hexc("#6B4423")), SM, rot=(0, math.radians(35), 0)); box("armR", (0.3, 0.3, 2.8), (2.4, 0, 5.1), mat("stick", hexc("#6B4423")), SM, rot=(0, math.radians(-35), 0))
SHIRT = [box("shirt", (3.5, 3.5, 2.3), (0, 0, 4.55), mat("tinyshirt", hexc("#E23B2E")), SM)]
HORNS = [box("horn", (0.35, 0.35, 1.3), (sx_, 0.1, 2.9), mat("horn", hexc("#C9B98A")), SHEAD, rot=(0, math.radians(sx_ * 30), 0)) for sx_ in (-0.9, 0.9)]
BALL = bpy.ops.mesh.primitive_uv_sphere_add(radius=2.4, location=(0, 0, 2.4)) or bpy.context.object
BALL = bpy.context.object; BALL.data.materials.append(snow_m)
# --- sister's red scarf and Noah's props
SCARF = [box("scarf", (1.7, 1.7, 0.5), (0, 0, 2.05), red_m, SIS.body), box("scarftail", (0.5, 0.3, 1.6), (0.6, -0.9, 1.3), red_m, SIS.body)]
SCOOP = box("scoop", (1.0, 1.0, 0.8), (0, 1.0, -1.8), snow_m, SIS.arms[1])
sill_m = mat("sill", hexc("#6B4423")); WX = -38.0
box("sill", (6.6, 1.4, 3.6), (WX, 23.2, 1.8), sill_m)
# --- falling snow
FLAKES = [box("flake", (0.28, 0.28, 0.28), (0, 0, 0), snow_m) for _ in range(150)]
_fr = random.Random(5); FL = [(_fr.uniform(-85, -5), _fr.uniform(-2, 40), _fr.uniform(0, 18), _fr.uniform(2.0, 4.0), _fr.uniform(0, 6.28)) for _ in FLAKES]
# neighbours who only shrug
NBS = [(KIDS[0], -53, "smile"), (KIDS[1], -41, "stern")]

C = []
def _k(c, tg, fov):
    K = 2.6 if fov <= 34 else (2.2 if fov <= 48 else 1.4)
    return (tg[0] + (c[0] - tg[0]) * K, tg[1] + (c[1] - tg[1]) * K, max(1.2, tg[2] + (c[2] - tg[2]) * K))
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=_k(c0, t0, fov), t0=t0, fov=fov)
    if c1: d["c1"] = _k(c1, t1 or t0, fov)
    if t1: d["t1"] = t1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
S(0.0,      (-45, -2, 6), (-45, 17, 3.5), 52, c1=(-45, 0, 6))                              # 1 snowman, every night
S(W(5),     (-52, 3, 3.4), (-46, 15, 2.5), 44, c1=(-51, 4, 3.4))                           # 2 Monday: knees
S(W(13),    (-52, 3, 3.6), (-46, 15, 3), 44, c1=(-51, 4, 3.6))                             # 3 Tuesday: waist
S(W(17),    (-52, 3, 4), (-46, 15, 4), 44, c1=(-51, 4, 4))                                 # 4 Wednesday: shoulders
S(W(21),    (-45, 3, 1.6), (-45, 17, 6.5), 56, c1=(-45, 5, 1.6))                           # 5 Friday: taller than the porch
S(W(29),    (-30, 0, 7), (-45, 16, 4), 56, c1=(-32, 1, 7))                                 # 6 nobody knew why
S(W(34),    (-53, 5, 3), (-47, 14, 1.8), 42, c1=(-52, 6, 3))                               # 7 footprints
S(W(38),    (-45, 7, 1.8), (-45, 13.5, 0.3), 42, c1=(-45, 8, 1.8))                         # 8 there were none
S(W(41),    (-47, 0, 5), (-47, 10, 4), 46, c1=(-47, 1, 5))                                 # 9 he asked the neighbors
S(W(45),    (-47, -1, 5), (-47, 10, 4.3), 38, c1=(-47, 0, 5))                              # 10 they only shrugged
S(W(48),    (-38, 14, 6), (-38, 23, 5.8), 36, c1=(-38, 15, 6))                             # 11 alarm for midnight
S(W(55),    (-38, 8, 5.2), (-38, 23, 4.8), 40, c1=(-38, 9, 5.2))                           # 12 tiptoed to the window
S(W(60),    (-45, -2, 3), (-45, 20, 9), 62, c1=(-45, 0, 3))                                # 13 snow fell
S(W(66),    (-62, 5, 4), (-68, 17, 3), 46, c1=(-61, 6, 4))                                 # 14 figure in a red scarf
S(W(73),    (-58, 2, 5), (-58, 17, 3), 58, c1=(-56, 3, 5))                                 # 15 rolled a giant ball
S(W(80),    (-50, 9, 3.6), (-49, 16, 3.2), 32, c1=(-50, 10, 3.6))                          # 16 it was his little sister
S(W(85),    (-53, 6, 4), (-47, 16, 3.8), 44, c1=(-52, 7, 4))                               # 17 whispering to the snowman
S(W(91),    (-52, 9, 3.6), (-49, 16.5, 3.2), 30, c1=(-52, 10, 3.6))                        # 18 just a little bigger
S(W(97),    (-45, 5, 2.2), (-45, 17, 5.5), 52, c1=(-45, 7, 2.2))                           # 19 so Noah won't be sad
S(W(105),   (-38, 11, 5), (-38, 23, 4.8), 30, c1=(-38, 12, 5))                             # 20 eyes filled with tears
S(W(110),   (-40, 3, 4), (-42, 14, 3), 54, c1=(-41, 4, 4))                                 # 21 outside in his socks
S(W(116),   (-49, 7, 4.4), (-45, 15, 4), 40, c1=(-48, 8, 4.4))                             # 22 it's okay
S(W(120),   (-47, 9, 5), (-44, 15, 4.7), 30, c1=(-47, 10, 5))                              # 23 I'm not sad
S(W(123),   (-52, 8, 4), (-47, 15, 3.5), 40, c1=(-51, 9, 4))                               # 24 she grinned
S(W(129),   (-47, 9, 3.8), (-46, 15, 3.4), 30, c1=(-47, 10, 3.8))                          # 25 a scoop of snow
S(W(132),   (-60, 3, 6), (-45, 17, 5), 58, c1=(-58, 4, 6))                                 # 26 built it taller together
S(W(137),   (-45, -2, 5), (-45, 17, 5.5), 56, c1=(-45, 0, 5))                              # 27 at dawn
S(W(141),   (-46, 5, 5.5), (-45, 17, 5), 42, c1=(-46, 7, 5.5))                             # 28 a tiny shirt
S(W(145),   (-45, 7, 8.5), (-45, 17, 9.5), 36, c1=(-45, 8, 8.5))                           # 29 a goat's horns
S(MON_T0 - 0.02, (-45, 9, 9), (-45, 17, 9.4), 26, c1=(-45, 10.5, 9))                       # 30 Thank you.
S(MON_END, (-45, -1, 6), (-45, 17, 5.5), 54, c1=(-45, 1, 6))                               # 31 final hold
SHOTS = []
for i, (st, d) in enumerate(C):
    d["start"] = st; d["end"] = C[i + 1][0] if i + 1 < len(C) else END_T; SHOTS.append(d)
def shot_at(t):
    cur = SHOTS[0]
    for s_ in SHOTS:
        if s_["start"] <= t: cur = s_
    return cur
def resolve(v, t): return v
def in_blackout(t): return False
def lamp_on(L, t): return True
def windows_lit(t): return True
def door_angle(hk, t): return 0.0
def flash_on(t): return False
def flash_pose(t): return None
SHUT = []
def apply_monster(t): hide(MON.root, True)
def E(*p): return list(p)
NOAH_SPEC = dict(vis=[(0, T(48)), (T(55), T(110) - 0.05), (T(110), END_T + 1)],
    wp=[(0, -48.5, 13.6, -40), (T(34), -48.5, 13.6, -40), (T(38), -47, 14, -30), (T(41), -47, 14, -30), (T(42), -47, 9.8, 180), (T(48), -47, 9.8, 180),
        (T(55), -41, 22.8, 180), (T(56), -41, 22.8, 180), (T(59), -38, 22.8, 180), (T(109), -38, 22.8, 180), (T(110), -38, 12, 90), (T(116), -46.5, 14.5, 90), (END_T + 1, -46.5, 14.5, 90)],
    face=E((0, "stern"), (T(38), "scared"), (T(55), "stern"), (T(80), "shock"), (T(105), "scared"), (T(110), "scared"), (T(120), "smile")),
    pose=E((0, POSES["idle"]), (T(34), POSES["crouch"]), (T(41), POSES["idle"]), (T(129), POSES["reach"])),
    gait=[(T(55), T(59), "walk"), (T(110), T(116), "walk")])
SIS_SPEC = dict(vis=[(T(66), END_T + 1)],
    wp=[(T(66), -75, 17, -90), (T(79), -53, 17, -90), (T(80), -49, 16.8, -90), (T(110), -49, 16.8, -90), (T(116), -49, 16.8, -45), (END_T + 1, -49, 16.8, -60)],
    face=E((0, "determined"), (T(80), "smile"), (T(123), "smile")), pose=E((0, POSES["brace"]), (T(80), POSES["idle"]), (T(123), POSES["reach"])), gait=[(T(66), T(79), "walk")], phase=1.0)
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC)]
for k_, x_, f_ in NBS:
    KID_SPECS.append((k_, dict(vis=[(T(40), T(48) + 0.3)], wp=[(0, x_, 9.4, 180 if x_ > -47 else 180)], face=E((0, f_)), pose=E((0, POSES["idle"]), (T(45), POSES["scared"])))))
def story_update(t):
    hide(cap_root, True)
    # the snowman grows on its own nights
    sc_ = [(0, 0.12), (T(6), 0.28), (T(14), 0.42), (T(18), 0.56), (T(22), 1.15), (T(80), 1.2), (T(94), 1.3), (T(132), 1.45)]
    s_ = track_val([(a, (v,)) for a, v in sc_], t, 0.14)[0]
    SM.scale = (s_, s_, s_)
    for o_ in SHIRT: o_.hide_render = t < T(143)
    for o_ in HORNS: o_.hide_render = t < T(146)
    k = back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0
    SHEAD.rotation_euler = (0, math.radians(24 * k), 0)
    # giant ball rolls across the yard with Sis
    hide(BALL, not (T(66) <= t < T(80)))
    if T(66) <= t < T(80):
        bx = -75 + (-53 + 75) * min(1.0, (t - T(66)) / (T(79) - T(66))) + 3.5; BALL.location = (bx, 17, 2.4); BALL.rotation_euler = (0, math.radians((bx + 75) * 25), 0)
    SCOOP.hide_render = not (T(125) <= t < T(132))
    # snowfall (pure function of time, so renders stay frame-independent)
    for o_, (x0, y0, z0, sp, ph) in zip(FLAKES, FL):
        o_.location = (x0 + 1.5 * math.sin(t * 0.9 + ph), y0, (z0 - sp * t) % 18.0)
