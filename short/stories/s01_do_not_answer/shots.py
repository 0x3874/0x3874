# Story 1 "Do Not Answer" -- exec'd inside build.py (STORY=s01_do_not_answer)
def W(i): return T(i) - 0.04
_cfg = json.load(open(SD + "story.json"))
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.05
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
HX, HBACK = -45.0, 40.0                 # Noah's house x, back wall y
YARD_N = 66.0                           # back fence line

# ---------------------------------------------------------------- yard set
fence_m = mat("fence", hexc("#8C6A43")); post_m = mat("post", hexc("#5E4529"))
for x in range(-70, -19, 3):
    if not (-48.5 < x < -42.0): box("post", (0.6, 0.6, 4.4), (x, YARD_N, 2.2), post_m)
box("gpostL", (0.6, 0.6, 4.4), (-48.4, YARD_N, 2.2), post_m); box("gpostR", (0.6, 0.6, 4.4), (-42.0, YARD_N, 2.2), post_m)
for z in (1.4, 3.0):
    box("rail", (21.6, 0.35, 0.5), (-59.2, YARD_N, z), fence_m); box("rail", (22.0, 0.35, 0.5), (-31.0, YARD_N, z), fence_m)
for y in range(int(HBACK) + 3, int(YARD_N), 3):
    box("spost", (0.6, 0.6, 4.4), (-70, y, 2.2), post_m); box("spost", (0.6, 0.6, 4.4), (-20, y, 2.2), post_m)
for x in (-70, -20):
    for z in (1.4, 3.0): box("srail", (0.35, 26, 0.5), (x, 53, z), fence_m)
# gate: hinge at x=-48, leaf 5.4 long, opens inward (toward the house)
GATE = empty("gatehinge", (-48, YARD_N, 0))
box("gleaf", (5.4, 0.3, 3.8), (2.7, 0, 2.2), mat("gate", hexc("#A07A4D")), GATE)
box("gbrace", (5.8, 0.2, 0.5), (2.7, -0.2, 2.2), post_m, GATE, rot=(0, math.radians(20), 0))
# gap in the fence for the gate: remove nothing; the gate sits in the rails line (rails are opened by gate leaf covering)
# back door + porch light
BDOOR_X = -52.0
box("bdark", (4.6, 0.3, 8.0), (BDOOR_X, HBACK + 0.1, 4.0), dark_mat)
BHINGE = empty("bhinge", (BDOOR_X - 2.3, HBACK + 0.45, 0))
box("bleaf", (4.6, 0.4, 8.0), (2.3, 0, 4.0), door_mat, BHINGE)
box("bporchbulb", (0.7, 0.7, 0.7), (BDOOR_X + 3.4, HBACK + 1.0, 9.4), porch_mat)
_pl = light("backporch", "POINT", 650, hexc("#FFD9A0"), (BDOOR_X + 3.4, HBACK + 2.0, 9.2), radius=0.3); _pl.data.use_shadow = False
# kitchen window (glow) + counter hiding Mom's legs
KX = -37.0
box("kwin", (6.4, 0.3, 5.2), (KX, HBACK + 0.1, 5.8), mat("kwinglow", hexc("#FCC773"), emit=0.75))
box("kframe", (7.0, 0.2, 5.8), (KX, HBACK + 0.0, 5.8), mat("kframe", hexc("#3A3A44")))
box("counter", (7.0, 1.6, 3.4), (KX, HBACK + 2.0, 1.7), mat("counter", hexc("#7A4B2A")))
_kl = light("kitchenlight", "POINT", 520, hexc("#FFC773"), (KX, HBACK + 4.5, 5.5), radius=0.6); _kl.data.use_shadow = False
for L_ in (_pl, _kl): LIGHTS_CULL.append(L_)
MOM = Kid("Mom", 1.0, "#D94F7A", "#3B4A6B", skin="#F5CD30")
hide(cap_root, True)


# ---------------------------------------------------------------- set dressing: depth layers so no wide shot is empty
_rnd = random.Random(11)
trunk_m = mat("trunk", hexc("#6B4423")); leaf_m = [mat(f"leaf{i}", hexc(c)) for i, c in enumerate(("#2E7D32", "#256B2B", "#3A8F3A"))]
dleaf_m = mat("dleaf", hexc("#10261A")); dtrunk_m = mat("dtrunk", hexc("#0C1712"))
def tree(x, y, h=11, dark=False):
    box("trunk", (1.4, 1.4, h * 0.55), (x, y, h * 0.275), dtrunk_m if dark else trunk_m)
    for i_ in range(3):
        w_ = h * (0.62 - i_ * 0.14); box("leaf", (w_, w_, h * 0.28), (x, y, h * (0.5 + i_ * 0.2)), dleaf_m if dark else leaf_m[i_ % 3])
def bush(x, y, w=3.2):
    box("bush", (w, w * 0.8, w * 0.7), (x, y, w * 0.35), leaf_m[_rnd.randrange(3)])
for (x_, y_, h_) in ((-82, 48, 13), (-76, 62, 11), (-8, 50, 14), (-12, 64, 12), (-88, 78, 15), (-70, 86, 12), (-22, 84, 14), (-4, 92, 16), (-100, 60, 12), (8, 70, 13)):
    tree(x_, y_, h_)
for x_ in range(-260, 140, 11): tree(x_ + _rnd.uniform(-3, 3), 150 + _rnd.uniform(-8, 8), _rnd.uniform(15, 26), dark=True)
for (hx, hy, c_) in ((-120, 104, "#8B3A3A"), (-6, 112, "#3B6EA8"), (60, 100, "#5E8F4F"), (-150, 125, "#B58A3A")):
    wm_ = mat(f"far{hx}", hexc(c_)); box("fhouse", (22, 16, 11), (hx, hy, 5.5), wm_); box("froof", (24, 18, 3), (hx, hy, 12.5), roof_mat)
    box("fwin", (3.4, 0.3, 3.4), (hx - 5, hy - 8.1, 6.2), win_mat); box("fwin", (3.4, 0.3, 3.4), (hx + 5, hy - 8.1, 6.2), win_mat)
for x_ in (-66, -60, -26, -22, -64.5, -24): bush(x_, HBACK + 3.2, 3.4)
for x_ in (-66, -63, -27, -24): bush(x_, YARD_N - 2.0, 2.6)
for i_, (x_, y_) in enumerate(((-52, 46), (-50.6, 51), (-49.2, 56), (-47.6, 61))): box("stone", (2.2, 2.2, 0.25), (x_, y_, 0.12), mat("stone", hexc("#8A8F9C")))
box("shed", (7, 6, 6.5), (-28, 58, 3.25), mat("shed", hexc("#9B4A3A"))); box("shedroof", (8, 7, 1), (-28, 58, 6.9), roof_mat)
tuft_m = mat("tuft", hexc("#4E9A3A"))
for _ in range(90):
    x_, y_ = _rnd.uniform(-69, -21), _rnd.uniform(HBACK + 3, YARD_N - 1)
    if -53 < x_ < -43 and y_ > 44: continue
    for k_ in range(3): box("tuft", (0.18, 0.18, _rnd.uniform(0.7, 1.4)), (x_ + k_ * 0.25, y_ + _rnd.uniform(-0.2, 0.2), 0.5), tuft_m, rot=(0, _rnd.uniform(-0.3, 0.3), 0))

# ---------------------------------------------------------------- shots
C = []
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=c0, t0=t0, fov=fov)
    if c1: d["c1"] = c1
    if t1: d["t1"] = t1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
NY = 46.5   # Noah's y after backing away
S(0.0,      (152, -5, 9), (-40, 3, 6), 64, c1=(142, -5, 8.6))                         # 1 wide town, doors shut
S(W(8),     (-45, 6, 5), (-45, 24, 5), 46, c1=(-45, 9, 5))                           # 2 Noah's front door
S(W(11),    (6, 5, 10), (-15, 11, 12), 42, c1=(4, 6, 10.5))                          # 3 the street lamp
S(W(15),    (30, 3, 6), (60, -17, 5.5), 50, c1=(33, 3, 6))                           # 4 swing drifting: nobody explains
S(W(18),    (-45, 63, 7), (-45, 45, 4), 56, c1=(-45, 61, 6.6))                       # 5 yard, Noah's back to us
S(W(23),    (-45, 41, 5.4), (-45, 53, 4.5), 46, c1=(-45, 43, 5.2))                       # 6 Noah in the yard, smiling
S(W(29),    (-45, 47, 4.5), (-45, 66, 4), 54, c1=(-45, 49, 4.6))                     # 7 the fence, a voice
S(W(35),    (-31, 52, 4.8), (-45, 52, 4.5), 42, c1=(-32, 52, 4.8))                   # 8 profile: it sounded like mom
S(W(38),    (-45, 61, 5.6), (-45, 52, 4.7), 36, c1=(-45, 60, 5.6))                   # 9 his face
S(W(41),    (-45, 59, 5.2), (-45, 52, 4.7), 30, c1=(-45, 58, 5.2), fov1=27)          # 10 froze
S(W(43),    (-45, 55, 6), (-40, 40, 5.5), 40, c1=(-44, 54, 6))                       # 11 kitchen window
S(W(47),    (KX, 48, 5.6), (KX, 41, 4.9), 30, c1=(KX, 47, 5.5))                      # 12 mom stirring
S(W(52),    (KX, 45, 4.9), (KX, 41, 4.7), 22, c1=(KX, 44, 4.9))                      # 13 lips closed
S(W(54),    (-52, 44, 5), (-45, 56, 5), 56, c1=(-51, 45, 5))                         # 14 voice again
S(W(58),    (-57, 57, 4.2), (-45, 66, 3.4), 52, c1=(-55, 58, 4.2))                   # 15 the fence slats
S(W(60),    (-45, 60, 5.8), (-45, 52, 4.7), 34, c1=(-45, 59, 5.8))                   # 16 half a second late
S(W(64),    (-45, 62, 5), (-45, 50, 4), 50, c1=(-45, 60, 5))                         # 17 Noah backs toward the house
S(W(69),    (-52, 50, 5), (-45, 66, 3.2), 48, c1=(-50, 53, 5))                   # 18 the gate swings open
S(W(74),    (-54, 54, 3.2), (-45, 68, 3.2), 50, c1=(-52, 58, 3.2))                         # 19 nothing behind it
S(W(78),    (-45, 44, 13), (-45, 58, 3), 62, c1=(-45, 45, 12))                       # 20 only the dark, listening
S(W(82),    (-51, 51, 5), (-45, NY, 4.8), 28, c1=(-50, 51, 5))                       # 21 a third time
S(W(85),    (-45, 58, 1.3), (-45, 74, 2), 50, c1=(-45, 66.5, 1.3))                   # 22 softer, closer (through the gate)
S(W(87),    (-45, 58, 5.4), (-45, NY, 4.7), 32, c1=(-45, 57, 5.4))                       # 23 he finally understood
S(W(92),    (KX, 46, 5), (KX, 41, 4.8), 24, c1=(KX, 45, 5))                          # 24 it can only repeat
S(W(96),    (-34, 50, 3.8), (-45, 66, 3.6), 50, c1=(-35, 54, 3.8))                   # 25 the gate, the dark
S(W(100),   (-45, 57, 5.4), (-45, NY, 4.7), 34, c1=(-45, 56, 5.4))                   # 26 anything you answer
S(W(104),   (-37, 50, 5), (-45, NY, 4.6), 38, c1=(-38, 50, 5))                       # 27 it keeps
S(W(108),   (-45, 58, 5.5), (-45, NY, 4.7), 36, c1=(-45, 57, 5.5))                   # 28 covered his mouth
S(W(110),   (-45, 46, 5.5), (-45, 66, 6), 56, c1=(-45, 48, 5.5))                     # 29 behind the fence
S(W(113),   (-45, 58, 1.6), (-45, 67.5, 7.5), 52, c1=(-45, 62, 1.8))                 # 30 far too tall
S(W(118),   (-45, 59, 8.8), (-45, 68, 8.7), 30, c1=(-45, 61, 8.8))                   # 31 head tilted
S(W(121),   (-44, 54, 5.5), (BDOOR_X, 40.5, 4.5), 56, c1=(-45, 53, 5.5))             # 32 the back door opens
S(W(125),   (BDOOR_X, 46, 4.3), (BDOOR_X, 40.8, 3.8), 30, c1=(BDOOR_X, 45, 4.3))     # 33 sister whispers
S(W(130),   (BDOOR_X, 43.5, 3.8), (-45, 66.5, 8), 52, c1=(BDOOR_X, 44.5, 3.9))       # 34 the dark answers
S(MON_T0 - 0.02, (-45, 59, 8.9), (-45, 68, 8.9), 28, c1=(-45, 61, 8.9))             # 35 "Coming." head snaps
SHOTS = []
for i, (st, d) in enumerate(C):
    d["start"] = st; d["end"] = C[i + 1][0] if i + 1 < len(C) else END_T; SHOTS.append(d)
def shot_at(t):
    cur = SHOTS[0]
    for s_ in SHOTS:
        if s_["start"] <= t: cur = s_
    return cur
def resolve(v, t): return v

# ---------------------------------------------------------------- world state: night, nothing dies in this one
def in_blackout(t): return False
def lamp_on(L, t): return True
def windows_lit(t): return True
def door_angle(hk, t): return 0.0
def flash_on(t): return False
def flash_pose(t): return None
SHUT = []

# ---------------------------------------------------------------- actors
def E(*p): return list(p)
FACE_NOAH = E((0, "smile"), (T(31), "stern"), (T(37), "scared"), (T(41), "shock"), (T(57), "scared"), (T(64), "panic"), (T(70), "scared"),
              (T(88), "shock"), (T(100), "panic"), (T(113), "shock"), (T(125), "scared"))
POSE_NOAH = E((0, POSES["idle"]), (T(30), POSES["scared"]), (T(41), POSES["brace"]), (T(64), POSES["scared"]), (T(106), POSES["cover"]), (T(112), POSES["scared"]))
NOAH_WP = [(5.3, -45, 52, 180), (T(31) - 0.05, -45, 52, 180), (T(31) + 0.12, -45, 52, 0), (T(65), -45, 52, 0), (T(68) + 0.5, -45, NY, 0), (END_T + 1, -45, NY, 0)]
NOAH_SPEC = dict(vis=[(5.3, END_T + 1)], wp=NOAH_WP, pose=POSE_NOAH, face=FACE_NOAH, gait=[(T(65), T(68) + 0.5, "walk")])
MOM_SPEC = dict(vis=[(0, END_T + 1)], wp=[(0, KX, HBACK + 1.0, 0)], pose=E((0, POSES["idle"])), face=E((0, "stern")), gait=[(0, END_T + 1, "stir")])
SIS_SPEC = dict(vis=[(T(122), END_T + 1)], wp=[(0, BDOOR_X, HBACK + 1.4, 0)], pose=E((0, POSES["idle"]), (T(125), POSES["scared"])), face=E((0, "smile"), (T(125), "scared")))
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC), (MOM, MOM_SPEC)]
for k_ in (BOY,) + tuple(KIDS): hide(k_.root, True)

def apply_monster(t):
    vis = t >= T(111)
    hide(MON.root, not vis)
    if not vis: return
    MON.root.location = (-45, 68.5, 0); MON.root.rotation_euler.z = math.pi
    for lp in MON.legs: lp.rotation_euler.x = 0
    for i_, ap in enumerate(MON.arms): ap.rotation_euler.x = math.radians(4 + 3 * math.sin(t * 1.3 + i_))
    MON.upper.rotation_euler.x = 0
    k1 = back((t - T(120)) / 0.14) if t >= T(120) else 0.0
    k2 = back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0
    MON.headpiv.rotation_euler = (0, math.radians(14 * k1 + 24 * k2), 0)

def story_update(t):
    GATE.rotation_euler.z = math.radians(-78 * smooth((t - T(70)) / 1.5))
    BHINGE.rotation_euler.z = math.radians(88 * smooth((t - T(122)) / 0.7))
    hide(cap_root, True)
