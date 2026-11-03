# Week 2, Story 2 "Which Door?" -- a hallway with three doors
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.35
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
RX, RY = 300.0, 300.0
def P(x, y, z=0.0): return (RX + x, RY + y, z)
hide(cap_root, True); hide(MON.root, True)
for k_ in (BOY, SIS) + tuple(KIDS): hide(k_.root, True)
box("ground", (260, 260, 1), P(0, 0, -0.55), mat("hgrass", hexc("#3E8F2B")))
wall_m = mat("hwall", hexc("#F2D6A0")); floor_m = mat("hfloor2", hexc("#8C5A3A")); trim = mat("htrim", hexc("#6B4423"))
box("hfloor", (40, 30, 0.5), P(0, 0, -0.25), floor_m)
box("hl", (1, 30, 12), P(-20.5, 0, 6), wall_m); box("hr", (1, 30, 12), P(20.5, 0, 6), wall_m)
DOORX = (-9, 0, 9)
for x0, x1 in ((-20, -12), (-6, -3), (3, 6), (12, 20)): box("hback", (x1 - x0, 1, 12), P((x0 + x1) / 2, 14.3, 6), wall_m)
box("lintel", (40, 1, 3), P(0, 14.3, 10.5), wall_m)
DOORC = ("#E23B2E", "#2F7DE0", "#2FA84F")
HD = []
for i_, (cx, col) in enumerate(zip(DOORX, DOORC)):
    hp = empty(f"dhinge{i_}", P(cx - 3, 13.7, 0)); box("dleaf", (6, 0.4, 9), (3, 0, 4.5), mat(f"door{i_}", hexc(col)), hp); HD.append(hp)
    box("aback", (7, 0.5, 10), P(cx, 23.6, 5), mat(f"alc{i_}", hexc(col))); box("aside", (0.5, 9, 10), P(cx - 3.6, 19, 5), mat(f"alc{i_}", hexc(col))); box("aside", (0.5, 9, 10), P(cx + 3.6, 19, 5), mat(f"alc{i_}", hexc(col))); box("afloor", (7, 9, 0.4), P(cx, 19, -0.1), floor_m)
    lt = light(f"alcove{i_}", "POINT", 380, hexc(col), P(cx, 17, 9), radius=0.6); lt.data.use_shadow = False; LIGHTS_CULL.append(lt)
box("sign", (9, 0.3, 2.6), P(0, 13.5, 10.6), mat("sign", hexc("#F4F4F4"))); box("signline", (6, 0.35, 0.3), P(0, 13.3, 10.9), mat("signink", hexc("#1B1B22"))); box("signline", (4, 0.35, 0.3), P(0, 13.3, 10.2), mat("signink", hexc("#1B1B22")))
lamp = light("halllamp", "POINT", 1400, hexc("#FFE4B5"), P(0, 4, 13), radius=1.0); LIGHTS_CULL.append(lamp)
fill = light("hallfill2", "POINT", 600, hexc("#9EB8FF"), P(0, -8, 12), radius=1.0); fill.data.use_shadow = False; LIGHTS_CULL.append(fill)
# pillows (red), trampoline (blue), desk + goat (green)
_pr = random.Random(3); pcol = [mat(f"pil{i}", hexc(c)) for i, c in enumerate(("#F8C8DC", "#FFFFFF", "#FFE1A8", "#C8E6FF"))]
for i_ in range(26):
    x_ = DOORX[0] + _pr.uniform(-2.6, 2.6); y_ = _pr.uniform(15.5, 22.5); h_ = 6.0 - abs(x_ - DOORX[0]) * 0.8 - abs(y_ - 19) * 0.5
    box("pillow", (_pr.uniform(2.2, 3.2), _pr.uniform(2.2, 3.2), 2.0), P(x_, y_, max(1.0, h_ * _pr.uniform(0.55, 0.9))), pcol[_pr.randrange(4)], rot=(0, 0, _pr.uniform(0, 3)))
TR = empty("tramp", P(0, 19, 0)); box("tframe", (6.6, 6.6, 0.5), (0, 0, 2.2), mat("tframe", hexc("#1B1B22")), TR); box("tmat", (5.6, 5.6, 0.3), (0, 0, 2.5), mat("tmat", hexc("#4DA6FF"), emit=0.4), TR)
for lx, ly in ((-2.8, -2.8), (2.8, -2.8), (-2.8, 2.8), (2.8, 2.8)): box("tleg", (0.4, 0.4, 2.2), (lx, ly, 1.1), mat("tframe", hexc("#1B1B22")), TR)
box("desk", (6.4, 2.6, 3.0), P(DOORX[2], 18.2, 1.5), mat("deskw", hexc("#6B4423"))); box("plate", (1.4, 0.2, 0.5), P(DOORX[2] + 1.4, 17.0, 3.25), mat("plate", hexc("#FFD21F"), emit=0.5))
class Goat:
    def __init__(self):
        wm = mat("goatwhite", hexc("#EFEAD8")); hm = mat("horn", hexc("#C9B98A"))
        self.root = empty("Goat", P(DOORX[2], 21.0, 0)); self.piv = empty("goatpiv", (0, 0, 0), self.root)
        box("gbody", (1.9, 3.2, 2.1), (0, 0, 2.8), wm, self.piv); box("suit", (2.2, 3.0, 2.3), (0, 0, 2.85), mat("suit", hexc("#2B3A67")), self.piv); box("tie", (0.4, 0.2, 1.4), (0, -1.55, 3.0), mat("tie", hexc("#EC1C24")), self.piv)
        for lx, ly in ((-0.6, -1.1), (0.6, -1.1), (-0.6, 1.1), (0.6, 1.1)): box("gleg", (0.55, 0.55, 1.7), (lx, ly, 0.85), wm, self.piv)
        self.head = empty("ghead", (0, -1.7, 4.4), self.piv); box("gh", (1.4, 1.6, 1.5), (0, -0.3, 0.4), wm, self.head)
        for sx_ in (-0.5, 0.5): box("horn", (0.28, 0.28, 0.9), (sx_, 0.1, 1.5), hm, self.head, rot=(0, math.radians(sx_ * 25), 0))
        box("beard", (0.3, 0.3, 0.7), (0, -1.0, -0.2), hm, self.head)
        self.face = face_patch("gface", 0.95, 1.0, self.head, (0, -0.3, 0.4), deg=90); self.face.rotation_euler.z = math.pi; self.face.data.materials[0] = face_mat("stern"); self.facename = "stern"
    def set_face(self, n):
        if n != self.facename: self.face.data.materials[0] = face_mat(n); self.facename = n
GOAT = Goat()
ROOF = box("roofled", (14, 10, 1), P(-30, 3, 9.5), mat("roofx", hexc("#5E4A6B"))); box("roofsnowcap", (14.4, 10.4, 0.3), P(-30, 3, 10.1), mat("roofy", hexc("#8C6FA0")))
# --- shots
def resolve(v, t): return v
C = []
def _kk(c, tg, fov):
    if tg[0] < -21 or c[0] < -21 or tg[2] > 9: return c          # the roof shots are placed by hand
    K = 2.2 if fov <= 34 else (1.8 if fov <= 48 else 1.25)
    x, y, z = tg[0] + (c[0] - tg[0]) * K, tg[1] + (c[1] - tg[1]) * K, tg[2] + (c[2] - tg[2]) * K
    return (max(-19, min(19, x)), max(-14.0, min(12.5, y)), max(2.5, z))
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    pc = lambda v: P(*v)
    d = dict(c0=pc(_kk(c0, t0, fov)), t0=pc(t0), fov=fov)
    if c1: d["c1"] = pc(_kk(c1, t1 or t0, fov))
    if t1: d["t1"] = pc(t1)
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
S(0.0,      (0, -14, 5), (0, 14, 5), 56, c1=(0, -12, 5))                       # 1 three doors
S(W(5),     (2, -3, 5.5), (0, 12, 5), 46, c1=(2, -2, 5.5))                     # 2 Noah in a hallway
S(W(10),    (0, 2, 5), (-9, 14, 5), 50, c1=(0, 2, 5), t1=(9, 14, 5))           # 3 with three doors
S(W(13),    (-9, 3, 5), (-9, 14, 5), 36, c1=(-9, 4, 5))                        # 4 red
S(W(16),    (0, 3, 5), (0, 14, 5), 36, c1=(0, 4, 5))                           # 5 blue
S(W(19),    (9, 3, 5), (9, 14, 5), 36, c1=(9, 4, 5))                           # 6 green
S(W(23),    (0, 0, 9), (0, 13.6, 10.4), 34, c1=(0, 1, 9))                      # 7 the sign
S(W(28),    (0, -6, 5.5), (0, 4, 4.6), 34, c1=(0, -5, 5.5))                    # 8 not a good decision maker
S(W(35),    (-3, -4, 5), (-9, 10, 4.5), 44, c1=(-3, -3, 5))                    # 9 picked red
S(W(38),    (-9, 2, 5.5), (-9, 18, 4), 46, c1=(-9, 3, 5.5))                    # 10 behind the red door
S(W(44),    (-5, 5, 8), (-9, 19, 3.5), 50, c1=(-5, 6, 8))                      # 11 mountain of pillows
S(W(47),    (-14, 4, 5), (-9, 14, 3), 50, c1=(-14, 5, 5))                      # 12 dove in
S(W(50),    (-9, 7, 6), (-9, 18, 2.5), 42, c1=(-9, 8, 6))                      # 13 sank
S(W(58),    (-6, 0, 5), (-9, 10, 4), 46, c1=(-6, 1, 5))                        # 14 ten minutes to climb out
S(W(66),    (-3, -3, 5), (0, 10, 4.5), 46, c1=(-3, -2, 5))                     # 15 picked blue
S(W(70),    (0, 3, 5.5), (0, 18, 4), 44, c1=(0, 4, 5.5))                       # 16 behind the blue door
S(W(74),    (4, 5, 7), (0, 18, 3), 50, c1=(4, 6, 7))                           # 17 giant trampoline
S(W(78),    (0, 5, 5), (0, 18, 4), 46, c1=(0, 6, 5))                           # 18 bounced once
S(W(81),    (-3, 5, 5), (0, 18, 5), 46, c1=(-3, 6, 5))                         # 19 twice
S(W(82),    (3, 5, 5), (0, 18, 6), 46, c1=(3, 6, 5))                           # 20 three times
S(W(84),    (-8, -10, 10), (-12, 10, 12), 64, c1=(-8, -9, 10))                 # 21 out of the house
S(W(91),    (-24, -4, 12), (-30, 3, 10.5), 46, c1=(-24, -3, 12))               # 22 landed on the roof
S(W(96),    (-26, -2, 12), (-30, 3, 11), 30, c1=(-26, -1, 12))                 # 23 upside down
S(W(98),    (-4, -6, 5), (-14, 8, 4), 50, c1=(-4, -5, 5))                      # 24 back inside, dizzy
S(W(103),   (6, -2, 5), (9, 14, 5), 44, c1=(6, -1, 5))                         # 25 only one door left
S(W(108),   (9, -3, 5), (9, 6, 4.6), 32, c1=(9, -2, 5))                        # 26 deep breath
S(W(114),   (9, 3, 5.5), (9, 16, 4.5), 40, c1=(9, 4, 5.5))                     # 27 opened it slowly
S(W(118),   (7, 2, 6), (9, 20, 4), 44, c1=(7, 3, 6))                           # 28 a goat in a tiny suit
S(W(127),   (9, 13, 4.8), (9, 20.5, 3.4), 34, c1=(9, 14, 4.8))                 # 29 a tiny desk
S(W(131),   (9, 14, 5.2), (9, 21, 4.6), 30, c1=(9, 15, 5.2))                   # 30 the goat looked up
S(MON_T0 - 0.02, (9, 15, 5.2), (9, 21, 4.8), 24, c1=(9, 16, 5.2))              # 31 You're hired.
S(MON_END, (0, -8, 6), (5, 16, 5), 52, c1=(0, -6, 6))                          # 32 hold
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
FACE = E((0, "smile"), (T(28), "stern"), (T(35), "determined"), (T(47), "shock"), (T(50), "panic"), (T(63), "stern"), (T(78), "smile"), (T(79), "panic"), (T(92), "shock"), (T(99), "scared"), (T(108), "determined"), (T(113), "scared"), (T(120), "shock"))
NOAH_SPEC = dict(vis=[(0, T(58)), (T(62), END_T + 1)], wp=[(0, RX + 0, RY + 4, 0)], face=FACE, pose=E((0, POSES["idle"]), (T(28), POSES["scared"]), (T(30), POSES["idle"])))
KID_SPECS = [(NOAH, NOAH_SPEC)]
def E_(t0, t1, a, b): return a + (b - a) * max(0.0, min(1.0, (t - t0) / (t1 - t0))) if False else None
def story_update(t):
    hide(cap_root, True)
    # Noah's route is scripted here (position, heading, height)
    x, y, z, rz, rx = 0.0, 4.0, 2.0, 0.0, 0.0
    lerp_ = lambda a, b, k: a + (b - a) * max(0.0, min(1.0, k))
    u = lambda a, b: (t - a) / (b - a)
    if t < T(28): x, y, rz = 0.0, 4.0, 0.0
    elif t < T(35): x, y, rz = 0.0, 4.0, 180
    elif t < T(47): x, y, rz = lerp_(0, -9, u(T(35), T(37))), lerp_(4, 10, u(T(35), T(38))), 0
    elif t < T(50): k = u(T(47), (T(49) + 0.2)); x, y, z, rz, rx = -9, lerp_(10, 17, k), 2.0 + 3.0 * math.sin(math.pi * min(1, k)), 0, -60 * min(1, k)
    elif t < T(58): k = u(T(50), T(57)); x, y, z, rz, rx = -9, 17.5, lerp_(3.0, 0.4, k), 0, -80
    elif t < T(66): k = u(T(62), T(66)); x, y, rz = -9, lerp_(15, 9, k), 180
    elif t < T(78): k = u(T(66), T(69)); x, y, rz = lerp_(-9, 0, k), lerp_(9, 8, k), 0 if t < T(78) else 0
    elif t < T(85):
        x, y = 0, 18.0; rz = 180
        ph = [(T(78) + 0.2, 1.0, 3.0), (T(81), 0.9, 5.0), (T(82.2) if False else (T(82) + 0.2), 1.2, 8.0)]
        z = 2.0 + 0.5
        for t0_, d_, h_ in ph:
            if t0_ <= t < t0_ + d_: z = 2.5 + 2.0 + h_ * math.sin(math.pi * (t - t0_) / d_)
    elif t < T(92): k = u(T(85), T(92)); x, y, z, rz = lerp_(0, -30, k), lerp_(18, 3, k), 4.5 + 20 * math.sin(math.pi * k), 180
    elif t < T(99): x, y, z, rz, rx = -30, 3, 10.0 + 2.0, 180, 180
    elif t < T(103): k = u(T(99), T(103)); x, y, rz = lerp_(-17, -8, k), 6, 90 + 20 * math.sin(t * 8)
    elif t < T(108): x, y, rz = 0, 5, 180
    elif t < T(115): k = u(T(108), T(112)); x, y, rz = lerp_(0, 9, k), lerp_(5, 8, k), 0 if k < 1 else 180
    else: x, y, rz = 9, 8, 180
    NOAH.root.location = (RX + x, RY + y, z + (0 if rx != 180 else 0)); NOAH.root.rotation_euler = (math.radians(rx), 0, math.radians(rz))
    # doors
    for hp, t0_ in zip(HD, (T(37), T(69), T(115))):
        hp.rotation_euler.z = math.radians(-95 * smooth((t - t0_) / (0.5 if t0_ != T(115) else 1.6))) if t >= t0_ else 0.0
    # trampoline bounce squash
    TR.scale = (1, 1, 1)
    hide(GOAT.root, t < T(115))
    GOAT.set_face("smile" if t >= T(131) else "stern")
    tilt = 24 * (back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0)
    GOAT.head.rotation_euler = (0, math.radians(tilt), 0)
