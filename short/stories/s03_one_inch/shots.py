# Story 3 "One Inch" -- Noah's bedroom (built away from town at RX,RY)
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.35
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
RX, RY = 300.0, 300.0
def P(x, y, z=0.0): return (RX + x, RY + y, z)
hide(cap_root, True)
for k_ in (BOY,) + tuple(KIDS): hide(k_.root, True)
wood = mat("floor", hexc("#B07A45")); wall_m = mat("rwall", hexc("#7E6CB8")); trim = mat("rtrim", hexc("#4B3B7A"))
box("rfloor", (30, 30, 0.6), P(0, 0, -0.3), wood)
box("rback", (30, 1, 13), P(0, 14.5, 6.5), wall_m); box("rleft", (1, 30, 13), P(-14.5, 0, 6.5), wall_m); box("rright", (1, 30, 13), P(14.5, 0, 6.5), wall_m)
box("rbase", (30, 0.4, 0.8), P(0, 14, 0.4), trim)
win_glow = mat("rwindow", hexc("#9EB8FF"), emit=1.6)
box("rwin", (6.5, 0.3, 5.5), P(5.5, 13.9, 7.5), win_glow); box("rwinframe", (7.2, 0.2, 6.2), P(5.5, 14.0, 7.5), trim)
# bed (head toward -y)
box("bedbase", (9.5, 14.5, 1.8), P(-8, 6.5, 0.9), mat("bedbase", hexc("#5B3A22"))); box("mattress", (9, 14, 1.0), P(-8, 6.5, 2.3), mat("mattress", hexc("#3FA7D6")))
box("pillow", (6, 2.6, 0.9), P(-8, 1.3, 3.2), mat("pillow", hexc("#F4F4F4")))
# bedside table + lamp (the lamp moves one inch per "night")
box("table", (3.6, 3.6, 3.0), P(2, 12, 1.5), mat("table", hexc("#6B4423")))
LAMP = empty("lamp", P(2, 12, 3.0))
box("lbase", (1.0, 1.0, 1.6), (0, 0, 0.8), pole_mat, LAMP); box("lshade", (2.4, 2.4, 1.9), (0, 0, 2.5), mat("lshade", hexc("#FFC773"), emit=2.2), LAMP)
_ll = light("roomlamp", "POINT", 260, hexc("#FFC773"), P(2, 11.5, 5.8), radius=0.5); _ll.data.use_shadow = False
_fill = light("moonfill", "POINT", 650, hexc("#9EB8FF"), P(0, 3, 11.5), radius=1.0); _fill.data.use_shadow = False
_gl = light("goatlight", "POINT", 380, hexc("#9EB8FF"), P(-1.5, 8, 9), radius=0.6); _gl.data.use_shadow = False
for l_ in (_ll, _fill, _gl): LIGHTS_CULL.append(l_)
# chair, shoes, rug (all slide one inch at a time)
CHAIR = empty("rchair", P(7, 9, 0)); cm_ = mat("rchair", hexc("#D98A2B"))
box("cs", (3.6, 3.6, 0.5), (0, 0, 3.3), cm_, CHAIR); box("cb", (3.6, 0.5, 3.6), (0, 1.55, 5.3), cm_, CHAIR)
for lx, ly in ((-1.5, -1.5), (1.5, -1.5), (-1.5, 1.5), (1.5, 1.5)): box("cl", (0.4, 0.4, 3.1), (lx, ly, 1.55), cm_, CHAIR)
SHOES = empty("shoes", P(9, 3, 0)); sh_m = mat("rshoe", hexc("#E23B2E"))
box("shoeL", (1.3, 2.6, 0.9), (-0.9, 0, 0.45), sh_m, SHOES); box("shoeR", (1.3, 2.6, 0.9), (0.9, 0, 0.45), sh_m, SHOES)
RUG = empty("rrug", P(2, 0, 0)); box("rug", (10, 7, 0.18), (0, 0, 0.1), mat("rrug", hexc("#C0392B")), RUG); box("rugstripe", (10, 1.2, 0.2), (0, 0, 0.12), mat("rrug2", hexc("#F1C40F")), RUG)
# door on the right wall
box("rdoor", (0.5, 5.4, 8.4), P(14.1, -3, 4.2), door_mat); box("rdoorbolt", (0.5, 0.8, 0.3), P(13.8, -5.2, 4.4), steel_m if "steel_m" in globals() else mat("rsteel", hexc("#B8BFCC")))
# bookshelf with the camera
box("shelf", (1.8, 7, 9.5), P(-13.2, 1, 4.75), mat("shelf", hexc("#5B3A22")))
for z_ in (2.5, 5, 7.5): box("book", (1.2, 5.5, 0.9), P(-13.0, 1, z_), mat("books", hexc("#B03A8C")))
box("cam", (1.5, 1.3, 1.1), P(-12.9, 1, 10.1), mat("camera", hexc("#2A2A30"))); REC = box("rec", (0.3, 0.3, 0.3), P(-12.0, 1, 10.5), mat("recled", hexc("#FF2020"), emit=6.0))
# desk + monitor (left wall, near the front)
box("desk", (3.2, 8, 0.5), P(-12.6, -9.5, 4.0), mat("desk", hexc("#6B4423"))); box("deskleg", (0.5, 0.5, 4.0), P(-11.4, -12.5, 2.0), mat("desk", hexc("#6B4423"))); box("deskleg", (0.5, 0.5, 4.0), P(-11.4, -6.5, 2.0), mat("desk", hexc("#6B4423")))
SCREEN_M = mat("screen", hexc("#5E9BEB"), emit=0.8)
box("monitor", (0.4, 4.6, 3.2), P(-13.3, -9.5, 6.2), mat("mon", hexc("#2A2A30"))); SCREEN = box("screen", (0.2, 4.0, 2.6), P(-13.0, -9.5, 6.2), SCREEN_M)
_sl = light("screenlight", "POINT", 220, hexc("#7FB5FF"), P(-10.5, -9.5, 6.4), radius=0.4); _sl.data.use_shadow = False; LIGHTS_CULL.append(_sl)
# goat in a little shirt, watching from the corner
class Goat:
    def __init__(self):
        wm = mat("goatwhite", hexc("#EFEAD8")); hm = mat("horn", hexc("#C9B98A")); sm_ = mat("goatshirt", hexc("#E23B2E"))
        self.root = empty("Goat", P(-1.5, 12.2, 0)); self.piv = empty("goatpiv", (0, 0, 0), self.root)
        box("gbody", (1.9, 3.2, 2.1), (0, 0, 2.8), wm, self.piv); box("shirt", (2.2, 2.0, 2.2), (0, 0.4, 2.85), sm_, self.piv)
        for lx, ly in ((-0.6, -1.1), (0.6, -1.1), (-0.6, 1.1), (0.6, 1.1)): box("gleg", (0.55, 0.55, 1.7), (lx, ly, 0.85), wm, self.piv)
        self.head = empty("ghead", (0, -1.7, 4.4), self.piv); box("gh", (1.4, 1.6, 1.5), (0, -0.3, 0.4), wm, self.head)
        for sx_ in (-0.5, 0.5): box("horn", (0.28, 0.28, 0.9), (sx_, 0.1, 1.5), hm, self.head, rot=(0, math.radians(sx_ * 25), 0))
        box("beard", (0.3, 0.3, 0.7), (0, -1.0, -0.2), hm, self.head)
        self.face = face_patch("gface", 0.95, 1.0, self.head, (0, -0.3, 0.4), deg=90); self.face.rotation_euler.z = math.pi; self.face.data.materials[0] = face_mat("stern"); self.facename = "stern"
    def set_face(self, n):
        if n != self.facename: self.face.data.materials[0] = face_mat(n); self.facename = n
GOAT = Goat()
NOAH2 = Kid("Noah2", 1.0, "#1E78D2", "#2B3A67")
# ---------------------------------------------------------------- shots
C = []
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=P(*c0), t0=P(*t0), fov=fov)
    if c1: d["c1"] = P(*c1)
    if t1: d["t1"] = P(*t1)
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
S(0.0,      (0, -13, 8.5), (0, 4, 3), 62, c1=(0, -11.5, 8.2))                                  # 1 the room, Noah asleep
S(W(6),     (-1, -2, 6), (2, 12, 4), 38, c1=(0, -1, 6))                                        # 2 lamp
S(W(9),     (2, -1, 6), (7, 9, 3.5), 40, c1=(3, 0, 6))                                         # 3 chair
S(W(12),    (6, -9, 4), (9, 3, 0.8), 40, c1=(6, -8, 4))                                        # 4 shoes
S(W(18),    (-4, -10, 3), (2, 0, 0.3), 40, c1=(-3, -9, 3))                                     # 5 one inch, never more (rug)
S(W(22),    (0, -11, 6), (6, -3, 4), 46, c1=(1, -10, 6))                                       # 6 Noah tells his sister
S(W(27),    (7, -11, 5.5), (10, -3, 4), 40, c1=(7, -10, 5.5))                                  # 7 she shrugged
S(W(29),    (6, -9, 5.5), (10.5, -3, 4.6), 34, c1=(6, -8, 5.5))                               # 8 maybe it's a ghost
S(W(33),    (-2, -12, 6.4), (3.5, -3, 4.7), 34, c1=(-1, -11, 6.4))                             # 9 did not believe
S(W(39),    (-4, -9, 5.5), (-9, 0, 4), 48, c1=(-3, -8, 5.5))                                   # 10 set a trap
S(W(44),    (-5, -8, 9), (-12.5, 1, 9.5), 36, c1=(-5, -7, 9))                                  # 11 camera on the shelf
S(W(49),    (-11.5, 1, 10.2), (5, 6, 3), 68, c1=(-11.5, 1, 10.4))                              # 12 the camera's view of the room
S(W(52),    (5, -9, 5.5), (12, -3, 5), 38, c1=(5, -8, 5.5))                                    # 13 lock twice
S(W(57),    (1, -2, 7), (4, 13.5, 7), 40, c1=(1, 0, 7))                                        # 14 window twice
S(W(62),    (-2, -11, 7), (-8, 5, 3), 56, c1=(-2, -10, 7))                                     # 15 went to sleep
S(W(67),    (0, -12, 8), (5, 13.5, 7), 52, c1=(0, -10, 8))                                     # 16 in the morning
S(W(70),    (0, -3, 6), (2, 12, 4), 38, c1=(1, -2, 6))                                         # 17 lamp had moved
S(W(74),    (2, -1, 6), (7, 9, 3.5), 42, c1=(3, 0, 6))                                         # 18 chair had moved
S(W(78),    (6, -9, 4), (9, 3, 0.8), 40, c1=(6, -8, 4))                                        # 19 shoes had moved
S(W(82),    (-5, -10, 6), (2, 0, 0.3), 52, c1=(-4, -9, 6))                                     # 20 even the rug
S(W(87),    (-3, -6, 6.5), (-11, -9, 5), 46, c1=(-3, -7, 6.5))                                 # 21 pressed play
S(W(90),    (-6, -7, 5.5), (-13, -9.5, 5.8), 32, c1=(-6, -8, 5.5))                             # 22 nothing happened (screen)
S(W(95),    (-8, -4, 6.5), (-8, 6.5, 3.6), 48, c1=(-8, -3, 6.5))                               # 23 Noah sat up
S(W(99),    (-8, 11.5, 5.4), (-8, 6, 4.6), 30, c1=(-8, 11.0, 5.4))                             # 24 eyes closed
S(W(103),   (0, -12, 7), (0, 4, 3.5), 58, c1=(0, -11, 7))                                      # 25 walked slowly across the room
S(W(109),   (0, -2, 6), (2, 12, 4), 40, c1=(1, -1, 6))                                         # 26 nudged the lamp
S(W(115),   (3, -1, 6), (7, 9, 3.5), 42, c1=(4, 0, 6))                                         # 27 then the chair
S(W(118),   (6, -9, 4), (9, 3, 0.8), 40, c1=(6, -8, 4))                                        # 28 then the shoes
S(W(121),   (-4, -10, 3), (2, 0, 0.3), 42, c1=(-3, -9, 3))                                     # 29 then the rug
S(W(124),   (2, -11, 7), (-6, 4, 3), 56, c1=(1, -10, 7))                                       # 30 back to bed
S(W(132),   (-9, -3, 5.4), (-9, -9.5, 4.8), 32, c1=(-9, -2, 5.4))                              # 31 stared at the screen
S(W(137),   (-3, -6, 6), (-11, -9, 5), 50, c1=(-3, -7, 6))                                     # 32 for a long time
S(W(141),   (2, -8, 5.5), (-1.5, 12, 3), 58, c1=(2, -6, 5.5))                                     # 33 in the corner of the frame
S(W(147),   (-1, 2, 4.4), (-1.5, 12.2, 3.6), 42, c1=(-1, 3, 4.4))                                # 34 a goat in a little shirt
S(W(153),   (-1, 3.5, 4.8), (-1.5, 12.2, 4.0), 34, c1=(-1, 4.5, 4.8))                            # 35 watching him too
S(MON_T0 - 0.02, (-1, 5.0, 4.6), (-1.5, 12.2, 4.2), 28, c1=(-1, 6.0, 4.6))                      # 36 Sleep well.
S(MON_END - 0.2, (-3, 2, 5.5), (-1.5, 12.2, 3.6), 46, c1=(-3, 3, 5.5))                                 # 37 final hold
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

# ---------------------------------------------------------------- actors
def E(*p): return list(p)
NOAH_SPEC = dict(vis=[(T(22), T(62)), (T(87), END_T + 1)],
    wp=[(0, 4, 0, 0)],  # placeholder, replaced below
    face=E((0, "stern")), pose=E((0, POSES["idle"])))
_nw = [(T(22), RX + 3.5, RY - 3, -90), (T(39), RX + 3.5, RY - 3, -90), (T(44), RX - 9, RY - 1, 90), (T(49), RX - 9, RY - 1, 90), (T(52), RX + 10, RY - 3.5, -90),
       (T(57), RX + 10, RY - 3.5, -90), (T(60), RX + 4, RY + 10, 0), (T(62), RX + 4, RY + 10, 0),
       (T(87), RX - 8.8, RY - 9.5, 90), (END_T + 1, RX - 8.8, RY - 9.5, 90)]
NOAH_SPEC["wp"] = _nw
NOAH_SPEC["gait"] = [(T(39), T(44), "walk"), (T(49), T(52), "walk"), (T(57), T(60), "walk")]
NOAH_SPEC["face"] = E((0, "stern"), (T(33), "stern"), (T(52), "determined"), (T(57), "determined"), (T(87), "stern"), (T(132), "shock"))
NOAH_SPEC["pose"] = E((0, POSES["idle"]), (T(55), POSES["point"]), (T(60), POSES["idle"]), (T(88), POSES["point"]), (T(92), POSES["idle"]))
SIS_SPEC = dict(vis=[(T(22), T(40))], wp=[(0, RX + 10.5, RY - 3, 90)], face=E((0, "smile"), (T(29), "smile")), pose=E((0, POSES["idle"]), (T(27), POSES["brace"])))
SLEEP = [(0, 0), (T(97), 1)]
# Noah2 sleeper: lies in bed, sits up, sleepwalks (nudging objects), lies down again
N2 = [(0, RX - 8, RY + 6.5, 0), (T(97), RX - 8, RY + 5.5, 0), (T(103), RX - 8, RY + 5.5, 0), (T(109), RX + 2, RY + 8.5, -20), (T(112), RX + 2, RY + 8.5, -20),
      (T(115), RX + 6, RY + 6.5, 20), (T(117), RX + 6, RY + 6.5, 20), (T(120), RX + 7, RY + 1.5, 0), (T(123) - 0.2, RX + 7, RY + 1.5, -90), (T(123), RX + 4, RY - 0.5, -90), (T(124), RX + 4, RY - 0.5, -90),
      (T(130), RX - 8, RY + 5.5, 180), (T(131), RX - 8, RY + 6.5, 0), (END_T + 1, RX - 8, RY + 6.5, 0)]
N2_SPEC = dict(vis=[(0, T(22)), (T(62), END_T + 1)], wp=N2, face=E((0, "sleep"), (T(131) + 0.3, "sleep")),
    pose=E((0, POSES["idle"]), (T(97), POSES["crouch"]), (T(103), POSES["reach"]), (T(130), POSES["idle"])), gait=[(T(103), T(112), "walk"), (T(112), T(120), "walk"), (T(120), T(130), "walk")])
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC), (NOAH2, N2_SPEC)]

def story_update(t):
    hide(cap_root, True)
    # Noah2: lying in bed outside the sleepwalk window
    lying = (t < T(22)) or (T(62) <= t < T(97)) or (t >= T(131))
    if lying:
        NOAH2.root.rotation_euler = (math.radians(90), 0, 0); NOAH2.root.location = (RX - 8, RY + 6.5, 2.9)
        NOAH2.arms[0].rotation_euler.x = NOAH2.arms[1].rotation_euler.x = 0
    elif T(97) <= t < T(103):
        NOAH2.root.location = (RX - 8, RY + 5.0, 3.1); NOAH2.root.rotation_euler = (0, 0, 0)
    # the one-inch nudges
    d = lambda t0: 1.0 * (1 if t >= t0 else 0)
    LAMP.location = P(2 + d(T(8)) + d(T(71)) + d(T(112)), 12, 3.0)
    CHAIR.location = P(7 + d(T(11)) + d(T(75)) + d(T(117)), 9, 0)
    SHOES.location = P(9 + d(T(14)) + d(T(79)) + d(T(120)), 3, 0)
    RUG.location = P(2 + d(T(84)) + d(T(123)), 0, 0)
    REC.hide_render = (int(t * 2) % 2 == 0)
    SCREEN_M.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.8 if t >= T(87) else 0.15
    # goat arrives in the corner
    hide(GOAT.root, t < T(146))
    GOAT.set_face("smile" if t >= T(153) else "stern")
    tilt = 24 * (back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0)
    GOAT.head.rotation_euler = (0, math.radians(tilt), 0)
