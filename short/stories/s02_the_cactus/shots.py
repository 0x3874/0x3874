# Story 2 "The Cactus" -- front lawn of Noah's house (x=-45), street side
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.12
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
LX, LY = -45.0, 18.0                  # lawn centre (cactus)
hide(cap_root, True)
for k_ in (BOY, KIDS[3]): hide(k_.root, True)
green = mat("cactus", hexc("#2FA84F")); dgreen = mat("cactus2", hexc("#1E7A3A")); pot_m = mat("pot", hexc("#C8683C")); spine_m = mat("spine", hexc("#F4F0C8"))
# --- cactus (a goat in disguise, but a perfectly good cactus until the end)
CAC = empty("cactus", (LX, LY, 0))
box("pot", (2.6, 2.6, 2.0), (0, 0, 1.0), pot_m, CAC); box("column", (1.8, 1.8, 4.4), (0, 0, 4.2), green, CAC)
box("armL", (1.6, 0.9, 0.9), (-1.3, 0, 4.6), green, CAC); box("armLup", (0.9, 0.9, 1.6), (-1.9, 0, 5.4), green, CAC)
box("armR", (1.6, 0.9, 0.9), (1.3, 0, 5.2), green, CAC); box("armRup", (0.9, 0.9, 1.4), (1.9, 0, 5.9), green, CAC)
for sx_, sz_ in ((-0.5, 3.2), (0.5, 4.0), (-0.5, 5.0), (0.5, 5.8)): box("spine", (0.12, 0.5, 0.12), (sx_, -0.95, sz_), spine_m, CAC)
cface = face_patch("cface", 0.95, 0.9, CAC, (0, 0, 4.7), deg=100); cface.data.materials[0] = face_mat("stern"); cface.rotation_euler.z = math.pi
# --- goat in a green cactus costume
class Goat:
    def __init__(self):
        wm = mat("goatwhite", hexc("#EFEAD8")); hm = mat("horn", hexc("#C9B98A")); gm = mat("costume", hexc("#2FA84F"))
        self.root = empty("Goat", (LX, LY, 0)); self.piv = empty("goatpiv", (0, 0, 0), self.root)
        box("gbody", (1.9, 3.2, 2.1), (0, 0, 2.8), wm, self.piv)
        box("costume", (2.3, 3.5, 2.4), (0, 0, 2.9), gm, self.piv)
        for sx_, sz_ in ((-0.6, 3.5), (0.6, 3.9), (-0.6, 2.3)): box("cspine", (0.12, 0.5, 0.12), (sx_, -1.8, sz_), spine_m, self.piv)
        self.legs = []
        for lx, ly in ((-0.6, -1.1), (0.6, -1.1), (-0.6, 1.1), (0.6, 1.1)):
            box("gleg", (0.55, 0.55, 1.7), (lx, ly, 0.85), wm, self.piv)
        self.head = empty("ghead", (0, -1.7, 4.4), self.piv)
        box("gh", (1.4, 1.6, 1.5), (0, -0.3, 0.4), wm, self.head)
        for sx_ in (-0.5, 0.5): box("horn", (0.28, 0.28, 0.9), (sx_, 0.1, 1.5), hm, self.head, rot=(0, math.radians(sx_ * 25), 0))
        box("beard", (0.3, 0.3, 0.7), (0, -1.0, -0.2), hm, self.head)
        self.face = face_patch("gface", 0.95, 1.0, self.head, (0, -0.3, 0.4), deg=90); self.face.rotation_euler.z = math.pi; self.facename = "smile"
        self.face.data.materials[0] = face_mat("smile")
    def set_face(self, n):
        if n != self.facename: self.face.data.materials[0] = face_mat(n); self.facename = n
GOAT = Goat(); GOAT.root.rotation_euler.z = 0     # head toward -y (the camera side)
# --- props
red_m = mat("mitt", hexc("#E23B2E")); hat_m = mat("hat", hexc("#8B5A2B")); steel = mat("steel", hexc("#B8BFCC")); tray_m = mat("tray", hexc("#D9B779"))
MITTS = [box("mitt", (1.25, 1.25, 1.1), (0, 0.05, -1.9), red_m, ap) for ap in NOAH.arms]
SHOVEL = [box("shaft", (0.3, 0.3, 6.5), (0, 1.1, -0.6), hat_m, NOAH.arms[1], rot=(math.radians(35), 0, 0)), box("blade", (1.8, 0.3, 2.0), (0, 3.6, 1.8), steel, NOAH.arms[1], rot=(math.radians(35), 0, 0))]
box("hat", (1.6, 1.6, 0.4), (0, 0, 1.45), hat_m, NOAH.headpiv); box("hattop", (1.2, 1.2, 0.5), (0, 0, 1.85), hat_m, NOAH.headpiv)
MINI = box("minicactus", (0.55, 0.55, 1.1), (0, 0, 2.4), green, NOAH.headpiv)
TRAY = box("tray", (2.6, 1.8, 0.2), (0, 1.3, -1.4), tray_m, SIS.arms[1])
CRANE = empty("crane", (LX - 2.6, LY - 1.0, 0))
box("mast", (0.3, 0.3, 7.0), (0, 0, 3.5), steel, CRANE); box("boom", (3.6, 0.3, 0.3), (1.8, 0, 7.0), steel, CRANE); box("line", (0.08, 0.08, 2.4), (3.4, 0, 5.8), steel, CRANE); box("hook", (0.8, 0.12, 0.12), (3.4, 0, 4.6), steel, CRANE)
# neighbours at their windows (heads at sill height)
sill_m = mat("sill", hexc("#6B4423"))
for hxn, wx_ in ((-75, -68), (-15, -22), (-15, -8)):
    box("sill", (4.2, 1.4, 3.4), (wx_, 23.2, 1.7), sill_m)
NB = [(KIDS[0], -68, "smile"), (KIDS[1], -22, "shock"), (KIDS[2], -8, "smile")]

# ---------------------------------------------------------------- shots
C = []
NOAH_X, SIS_X = -51.0, -39.0
def _adj(c, tg, fov):
    """keep Noah/Sis off the cactus line and pull cameras back so characters are not giants in frame"""
    shift = 0.0
    if 12 <= tg[1] <= 16 and -47 <= tg[0] <= -41: shift = NOAH_X - tg[0]; tg = (tg[0] + shift, tg[1], tg[2])
    elif 12 <= tg[1] <= 13 and -49 <= tg[0] <= -46: shift = SIS_X - tg[0]; tg = (tg[0] + shift, tg[1], tg[2])
    c = (c[0] + shift, c[1], c[2])
    K = 2.8 if fov <= 34 else (2.3 if fov <= 48 else 1.4)
    return (tg[0] + (c[0] - tg[0]) * K, tg[1] + (c[1] - tg[1]) * K, tg[2] + (c[2] - tg[2]) * K), tg
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    n0, nt0 = _adj(c0, t0, fov); d = dict(c0=n0, t0=nt0, fov=fov)
    if c1: n1, nt1 = _adj(c1, t1 or t0, fov); d["c1"] = n1; d["t1"] = nt1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
S(0.0,      (-45, 5, 3.2), (-45, 18, 3.2), 40, c1=(-45, 8, 3.4))                               # 1 hook: the cactus
S(W(6),     (-52, 6, 4.5), (-45, 13, 4.3), 44, c1=(-51, 7, 4.5))                              # 2 Noah says yes
S(W(9),     (-45, 7, 4.8), (-45, 13, 4.6), 32, c1=(-45, 8, 4.8))                              # 3 Noah was wrong
S(W(12),    (-38, 10, 3.2), (-45, 15, 3.2), 40, c1=(-39, 11, 3.2))                            # 4 bare hands
S(W(15),    (-45, 9, 3.2), (-45, 16, 3), 34, c1=(-45, 10, 3.2))                               # 5 that lasted one second
S(W(19),    (-52, 6, 4.6), (-46, 13, 4), 40, c1=(-51, 7, 4.6))                                # 6 oven mitts
S(W(22),    (-41, 10, 3.8), (-45, 16, 3.5), 30, c1=(-42, 11, 3.8))                            # 7 poked straight through
S(W(27),    (-60, 3, 5), (-45, 14, 4), 52, c1=(-58, 4, 5))                                    # 8 snow shovel
S(W(31),    (-38, 8, 5), (-45, 15, 4.5), 40, c1=(-39, 9, 5))                                  # 9 slid off
S(W(36),    (-45, 7, 5.6), (-45, 13, 5.4), 30, c1=(-45, 8, 5.6))                              # 10 landed in his hat
S(W(40),    (-52, 10, 4.5), (-46.5, 16, 3.5), 42, c1=(-51, 11, 4.5))                          # 11 tiny crane
S(W(45),    (-44, 11, 5), (-44.5, 17, 5), 36, c1=(-44, 12, 5.2))                              # 12 coat hanger
S(W(51),    (-36, 7, 6), (-46, 16, 5), 44, c1=(-37, 8, 6))                                    # 13 almost worked
S(W(54),    (-45, 9, 5), (-45, 17, 5), 30, c1=(-45, 10, 5))                                   # 14 wobbled
S(W(57),    (-40, 4, 3), (-45, 17, 5), 52, c1=(-40, 5, 3))                              # 15 tipped
S(W(60),    (-30, 3, 4), (-35, 12, 3.5), 50, c1=(-28, 4, 4))                                  # 16 Noah ran
S(W(63),    (-45, -2, 6), (-15, 24, 5.5), 55, c1=(-44, -1, 6))                                # 17 every neighbor
S(W(66),    (-22, 10, 5), (-22, 23.4, 4.8), 28, c1=(-22, 12, 5))                              # 18 watching from windows
S(W(70),    (-45, 5, 3), (-43, 13, 2.5), 44, c1=(-45, 6, 3))                                  # 19 sat on the grass
S(W(75),    (-45, 8, 4.4), (-43, 13, 3.6), 30, c1=(-45, 9, 4.4))                              # 20 sighed
S(W(77),    (-70, 6, 5), (-55, 12, 3.5), 50, c1=(-68, 7, 5))                                  # 21 his little sister
S(W(80),    (-52, 3, 4), (-52, 12, 3.5), 44, c1=(-51, 4, 4))                                  # 22 walked up with a tray
S(W(85),    (-48, 6, 4), (-47, 12.5, 3.6), 32, c1=(-48, 7, 4))                                # 23 ask it nicely
S(W(91),    (-43, 7, 5), (-43, 13, 4.5), 30, c1=(-43, 8, 5))                                  # 24 rolled his eyes
S(W(95),    (-45, 9, 4), (-45, 18, 3), 44, c1=(-45, 10, 4))                                   # 25 please
S(W(98),    (-45, 12, 3.3), (-45, 18, 3.4), 28, c1=(-45, 13, 3.4))                            # 26 did not move
S(W(103),   (-50, 8, 4.2), (-46, 13, 4), 40, c1=(-51, 8, 4.2))                                # 27 then a goat in a
S(W(108),   (-45, 11, 3.6), (-45, 18, 3.5), 32, c1=(-45, 12, 3.6))                            # 28 green costume
S(W(110),   (-45, 8, 3), (-45, 18, 3.2), 44, c1=(-45, 9, 3.2))                                # 29 stood up
S(W(112),   (-45, 2, 5), (-45, 18, 3.5), 50, c1=(-45, 3, 5))                                  # 30 it had been the cactus
S(W(117),   (-45, 10, 3.8), (-45, 18, 3.8), 26, c1=(-45, 12, 3.8))                            # 31 the whole time
S(W(120),   (-45, 8, 5), (-43, 13, 4.7), 28, c1=(-45, 9, 5))                                  # 32 Noah stared
S(W(122),   (-45, 11, 3.8), (-45, 18, 3.8), 24, c1=(-45, 12.5, 3.8))                          # 33 the goat winked
S(MON_T0 - 0.02, (-45, 10.5, 3.9), (-45, 18, 3.9), 22, c1=(-45, 12, 3.9))                     # 34 Nice try.
S(MON_END + 0.15, (-45, 0, 5), (-45, 16, 3.5), 52, c1=(-45, 2, 5.2))                          # 35 final wide hold
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

# ---------------------------------------------------------------- actors
def E(*p): return list(p)
FACE_NOAH = E((0, "smile"), (T(6), "determined"), (T(9), "scared"), (T(24), "shock"), (T(33), "angry"), (T(40), "determined"), (T(55), "shock"),
              (T(60), "panic"), (T(70), "stern"), (T(95), "determined"), (T(110), "shock"), (T(120), "shock"))
POSE_NOAH = E((0, POSES["idle"]), (T(12), POSES["reach"]), (T(17), POSES["scared"]), (T(20), POSES["idle"]), (T(21), POSES["reach"]), (T(24), POSES["brace"]),
              (T(27), POSES["idle"]), (T(29), POSES["shovel"]), (T(40), POSES["idle"]), (T(44), POSES["point"]), (T(54), POSES["brace"]), (T(60), POSES["idle"]),
              (T(71), POSES["crouch"]), (T(91), POSES["idle"]), (T(95), POSES["brace"]), (T(98), POSES["idle"]), (T(110), POSES["scared"]))
_FACE_CAM = [(T(9) - 0.05, T(12)), (T(36) - 0.05, T(40)), (T(75) - 0.05, T(80)), (T(91) - 0.05, T(95)), (T(120) - 0.05, END_T + 1)]
_pre = []
for a_, b_ in _FACE_CAM: _pre += [(a_, -51, 13, -50), (a_ + 0.12, -51, 13, 180), (b_, -51, 13, 180), (b_ + 0.12, -51, 13, -50)]
NOAH_WP = [(0, -51, 13, -50)] + [w for w in _pre if w[0] < T(60) or w[0] > T(70)] + [(T(60), -51, 13, -50), (T(60) + 0.12, -51, 13, -90), (T(62) + 0.4, -12, 12.4, -90), (T(68), -12, 12.4, -90), (T(68) + 0.2, -12, 12.4, 90),
           (T(70) - 0.4, -51, 13, 90), (T(70) - 0.2, -51, 13, -50), (END_T + 1, -51, 13, -50)]
NOAH_WP = sorted(NOAH_WP, key=lambda e: e[0])
NOAH_SPEC = dict(vis=[(0, END_T + 1)], wp=NOAH_WP, pose=POSE_NOAH, face=FACE_NOAH, gait=[(T(60), T(62) + 0.4, "run"), (T(68) + 0.2, T(70) - 0.4, "run")])
SIS_SPEC = dict(vis=[(T(77), END_T + 1)], wp=[(0, -72, 12, -90), (T(77), -72, 12, -90), (T(84), -39, 12.4, -90), (T(84) + 0.2, -39, 12.4, 40), (END_T + 1, -39, 12.4, 40)],
                pose=E((0, POSES["brace"]), (T(85), POSES["brace"])), face=E((0, "smile")), gait=[(T(77), T(84), "walk")], phase=1.2)
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC)]
for k_, x_, f_ in NB:
    KID_SPECS.append((k_, dict(vis=[(T(62) + 0.3, END_T + 1)], wp=[(0, x_, 22.5, 180)], face=E((0, f_), (T(110), "shock")), pose=E((0, POSES["idle"])))))
def apply_monster(t): hide(MON.root, True)

def story_update(t):
    hide(cap_root, True)
    # cactus / goat swap at "costume"
    swap = t >= T(110)
    hide(CAC, swap or (T(36) <= t < T(40) - 0.02))
    hide(GOAT.root, not swap)
    # cactus motion (snaps)
    cx, cy, cz, cs = LX, LY, 0.0, 1.0
    tip = 0.0
    if T(31) <= t < T(36): k = back((t - T(33)) / 0.14); cx, cy, cz, cs = LX, LY - 2.5 * k, 3.0 * k, 0.6
    if T(51) <= t < T(63): cz = 4.5 * smooth((t - T(51)) / 1.2)
    wob = 10 * math.sin(2 * math.pi * 3 * t) if T(54) <= t < T(59) else 0.0
    if T(59) <= t < T(63): tip = 80 * back((t - T(59)) / 0.3)
    CAC.location = (cx, cy, cz); CAC.scale = (cs, cs, cs); CAC.rotation_euler = (math.radians(wob + tip), 0, 0)
    for o_ in (CRANE,): hide(o_, not (T(44) <= t < T(63)))
    CRANE.rotation_euler = (math.radians(0.3 * (wob + tip)), 0, 0)
    # props
    for m_ in MITTS: m_.hide_render = not (T(19) <= t < T(27))
    for s_ in SHOVEL: s_.hide_render = not (T(27) <= t < T(40))
    MINI.hide_render = not (T(36) <= t < T(40))
    TRAY.hide_render = not (T(80) <= t < T(98))
    # goat reveal, wink, tilt
    k = back((t - T(110)) / 0.5)
    GOAT.piv.scale = (1, 1, 0.25 + 0.75 * k) if t >= T(110) else (1, 1, 0.25)
    GOAT.set_face("wink" if t >= T(122) else "smile")
    tilt = 24 * (back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0)
    GOAT.head.rotation_euler = (0, math.radians(tilt), 0)
    cface.hide_render = (CAC.hide_render)
