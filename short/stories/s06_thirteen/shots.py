# Story 6 "Thirteen" -- a stairwell with twelve steps, and one more
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.45
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
RX, RY = 300.0, 300.0
def P(x, y, z=0.0): return (RX + x, RY + y, z)
hide(cap_root, True)
for k_ in (BOY, SIS) + tuple(KIDS): hide(k_.root, True)
wall_m = mat("swall", hexc("#2F6B78")); wood_m = mat("swood", hexc("#8C5A3A")); floor_m = mat("sfloor", hexc("#5B3A22")); trim_m = mat("strim", hexc("#C9A66B"))
box("hfloor", (13, 60, 0.5), P(0, 17, -0.25), floor_m)
box("lwall", (1, 60, 30), P(-6.9, 17, 15), wall_m); box("rwall", (1, 60, 30), P(6.9, 17, 15), wall_m); box("bwall", (14, 1, 30), P(0, 47.5, 15), wall_m); box("fwall", (14, 1, 30), P(0, -12.5, 15), wall_m)
box("hceil", (14, 60, 0.5), P(0, 17, 28), mat("sceil", hexc("#1B3A44")))
# twelve steps (solid blocks) + landing; the 13th "step" is a foot
for i_ in range(1, 13): box("step", (12.4, 2.2, 1.1 * i_), P(0, 3.1 + 2.2 * (i_ - 1), 0.55 * i_), wood_m if i_ % 2 else mat("step2", hexc("#A06A44")))
box("landing", (12.4, 17, 14.3), P(0, 39, 7.15), wood_m)
ang = math.degrees(math.atan2(14.5, 27))
box("handrail", (0.4, 30.6, 0.4), P(-5.6, 15.5, 11.5), trim_m, rot=(math.radians(ang), 0, 0))
for y_ in (4, 10, 16, 22, 28): box("baluster", (0.25, 0.25, 4.5), P(-5.6, y_, 1.1 * ((y_ - 2) / 2.2) + 2.4), trim_m)
# front door (opens at "came home late"), moon window, sister's door with a warm slit of light
DHINGE = empty("fdoorhinge", P(-2.6, -11.8, 0)); box("fdoor", (5.2, 0.5, 9.0), (2.6, 0, 4.5), door_mat, DHINGE)
box("moonwin", (4.5, 0.3, 6.0), P(0, 46.9, 20.5), mat("smoon", hexc("#9EB8FF"), emit=1.5))
box("sdoor", (0.4, 4.2, 9), P(-6.3, 40, 18.8), door_mat); box("slit", (0.1, 3.8, 0.25), P(-6.1, 40, 14.5), mat("slit", hexc("#FFC773"), emit=5.0))
# lights
DAY = light("daylamp", "POINT", 900, hexc("#FFD9A0"), P(0, 8, 20), radius=0.8); DAY.data.use_shadow = False
HALLMOON = light("hallmoon", "POINT", 520, hexc("#9EB8FF"), P(0, 40, 22), radius=0.8); HALLMOON.data.use_shadow = False
FOOTLIGHT = light("footglow", "POINT", 200, hexc("#FF9A3C"), P(0, 28, 15.4), radius=0.4); FOOTLIGHT.data.use_shadow = False
HALLFILL = light("hallfill", "POINT", 160, hexc("#6E8FD6"), P(0, 2, 11), radius=0.8); HALLFILL.data.use_shadow = False
for l_ in (DAY, HALLMOON, FOOTLIGHT, HALLFILL): LIGHTS_CULL.append(l_)
# the foot
FOOTM = mat("foot", hexc("#0D0D0F"), emit=0.0)
FOOT = empty("foot", P(0, 29.5, 0))
box("footbody", (4.2, 5.4, 1.5), (0, 0, 13.55), FOOTM, FOOT)
TOES = []
for tx in (-0.9, 0.9):
    hp = empty("toepiv", (tx, -2.7, 14.0), FOOT); box("toe", (0.8, 3.4, 0.8), (0, -1.7, 0), FOOTM, hp); TOES.append(hp)
box("footheel", (3.0, 1.6, 2.2), (0, 3.0, 14.2), FOOTM, FOOT)
def stair_z(y):
    return 0.0 if y < 2 else (1.1 * (y - 2) / 2.2 if y < 28.4 else 14.3)
MH_CACHE = {}
def MH_pos(t):
    bpy.context.view_layer.update(); w_ = MON.headpiv.matrix_world @ Vector((0, 0, 0.9)); return (w_.x, w_.y, w_.z)
def resolve(v, t):
    if isinstance(v, str) and v == "MH": return MH_pos(t)
    if isinstance(v, tuple) and len(v) == 4 and v[0] == "N":
        r = NOAH.root.location; y = r.y + v[2]
        return (r.x + v[1], y, max(stair_z(r.y - RY) + 2.0 + v[3], stair_z(y - RY) + 2.6))
    return v
C = []
def _cam(c, tg, fov):
    if isinstance(c, str) or c[0] == "N" or isinstance(tg, str) or tg[0] == "N": return c if (isinstance(c, str) or c[0] == "N") else P(*c)
    K = 1.6 if fov <= 40 else 1.2
    x, y, z = tg[0] + (c[0] - tg[0]) * K, tg[1] + (c[1] - tg[1]) * K, tg[2] + (c[2] - tg[2]) * K
    y = max(-10.5, min(46, y)); x = max(-5.2, min(5.2, x)); z = max(z, stair_z(y) + 2.6)
    return P(x, y, z)
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    pc = lambda v: v if (isinstance(v, str) or v[0] == "N") else P(*v)
    d = dict(c0=_cam(c0, t0, fov), t0=pc(t0), fov=fov)
    if c1: d["c1"] = _cam(c1, t1 or t0, fov)
    if t1: d["t1"] = pc(t1)
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
def N(dx, dy, dz): return ("N", dx, dy, dz)
S(0.0,      (0, -6, 2), (0, 22, 12), 58, c1=(0, -4, 2.4))                        # 1 the staircase
S(W(6),     (0, -8, 6), (0, 20, 10), 56, c1=(0, -6, 6))                          # 2 older than the houses
S(W(9),     (3, 4, 3), (-2, 12, 5), 44, c1=(3, 5, 3.4))                          # 3 old wood
S(W(16),    (0, 26, 15), (-6, 41, 19), 50, c1=(0, 27, 15))                       # 4 nobody explains why
S(W(19),    (4, -4, 4), (0, 2, 3), 40, c1=(4, -3, 4))                            # 5 Noah had always counted
S(W(23),    (5, 8, 5), (0, 8, 4), 44, c1=(5, 10, 6))                             # 6 twelve
S(W(28),    (0, 18, 8), (0, 32, 16), 50, c1=(0, 19, 8.4))                        # 7 hall to his bedroom
S(W(32),    (4, 20, 12), (0, 10, 6), 50, c1=(4, 21, 12))                         # 8 twelve steps back
S(W(35),    (0, 6, 5), (0, -9, 5), 50, c1=(0, 5, 5))                             # 9 came home late
S(W(41),    (0, -6, 6), (0, 18, 9), 58, c1=(0, -4, 6))                           # 10 the house was dark
S(W(45),    (0, 26, 17), (-6, 40, 17.5), 40, c1=(0, 27, 17))                     # 11 sister asleep upstairs
S(W(51),    (3, -3, 3), (0, 4, 3), 44, c1=(3, -2, 3.2))                          # 12 he climbed slowly
S(W(54),    (0, 14, 12), (0, 3, 4.8), 38, c1=(0, 14, 12))                        # 13 counted without meaning to
S(W(59),    (3, 0, 1.2), (0, 3, 2), 44, c1=(3, 1, 1.4))                          # 14 one two three
S(W(62),    N(0, 9, 6), N(0, 0, 3.8), 40, c1=N(0, 8, 6))                         # 15 four five six seven
S(W(66),    N(4, -3, 2), N(0, 2, 3.2), 44, c1=N(4, -2, 2))                       # 16 eight nine ten
S(W(69),    N(0, 8, 5.5), N(0, 0, 4.2), 36, c1=N(0, 7, 5.5))                     # 17 eleven twelve
S(W(71),    N(3, -6, 3), N(0, 0, 3), 36, c1=N(3, -5.5, 3))                       # 18 he stopped
S(W(73),    (3, 24, 16), (0, 29.5, 14.8), 38, c1=(3, 25, 16))                    # 19 one more step
S(W(78),    (2, 26, 16), (0, 29.5, 14.4), 30, c1=(2, 27, 15.8))                  # 20 it had never been there
S(W(83),    N(0, 1, 6.4), (0, -9, 0), 60, c1=N(0, 1, 6.4))                       # 21 looked down at the dark hallway
S(W(90),    N(0, 8, 5), N(0, 0, 4.6), 32, c1=N(0, 7, 5))                         # 22 looked back up
S(W(94),    (2, 25, 16.5), (0, 29.5, 14.8), 34, c1=(2, 26, 16.2))                # 23 the 13th step was warm
S(W(99),    (-2, 26, 15.6), (0, 29.5, 14.6), 28, c1=(-2, 26.5, 15.4))            # 24 it was breathing
S(W(102),   (3, 20, 14), (0, 29.5, 14.5), 44, c1=(3, 21, 14))                    # 25 slowly it shifted
S(W(105),   (2, 25, 15.5), (0, 30, 14.6), 30, c1=(2, 26, 15.2))                  # 26 two long toes
S(W(112),   N(0, 8, 5), N(0, 0, 4.7), 30, c1=N(0, 7, 5))                         # 27 Noah understood the rule
S(W(116),   (3, 22, 16), (0, 29.5, 14.8), 38, c1=(3, 23, 16))                    # 28 it was never a step
S(W(121),   (0, -6, 2), (0, 29, 12), 60, c1=(0, -4, 2.4))                        # 29 the foot of something
S(W(128),   (0, 18, 8), (0, 30, 18), 64, c1=(0, 19, 8))                          # 30 across the whole house
S(W(132),   N(0, 8, 5), N(0, 0, 4.7), 30, c1=N(0, 7, 5))                         # 31 Noah did not move
S(W(136),   (3, 24, 15.6), (0, 29.5, 16), 40, c1=(3, 25, 15.8))                  # 32 the foot began to lift
S(W(141),   (0, 4, 3), (0, 30, 18), 64, c1=(0, 6, 3.4))                          # 33 the whole house
S(W(145),   (0, 20, 15), "MH", 30, c1=(0, 21, 15), t1="MH")                      # 34 breathed in
S(MON_T0 - 0.02, (0, 22, 16.8), "MH", 24, c1=(0, 23, 16.8), t1="MH")             # 35 Fourteen.
S(MON_END, (0, 2, 6), (0, 29, 15), 56, c1=(0, 4, 6))                             # 36 hold
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
SHUT = []
def flash_on(t): return t >= T(41)
def flash_pose(t):
    if t < T(41): return None
    bpy.context.view_layer.update()
    hand = NOAH.arms[1].matrix_world @ Vector((0, 0.35, -1.8)); rz = NOAH.root.rotation_euler.z
    d = Vector((-math.sin(rz), math.cos(rz), 0.25 if t >= T(83) else 0.0)); return (tuple(hand), tuple(d))
def E(*p): return list(p)
_sy = lambda i: 3.1 + 2.2 * (i - 1)
NW = [(T(23) - 0.3, RX, RY - 1, 0), (T(23), RX, RY + 0.5, 0), (T(31), RX, RY + 38, 0), (T(32), RX, RY + 38, 180), (T(34), RX, RY + 0.5, 180), (T(34) + 0.2, RX, RY + 0.5, 180)]
NOAH_SPEC = dict(vis=[(T(23) - 0.3, T(34) + 0.3), (T(37) - 0.2, END_T + 1)],
    wp=NW + [(T(37), RX, RY - 11, 0), (T(40), RX, RY, 0), (T(57), RX, RY, 0)] + [(T(58 + i), RX, RY + _sy(i), 0) for i in range(1, 13)] + [(T(83), RX, RY + _sy(12), 0), (T(84), RX, RY + _sy(12), 0), (END_T + 1, RX, RY + _sy(12), 0)],
    face=E((0, "stern"), (T(37), "stern"), (T(73), "scared"), (T(112), "shock"), (T(132), "panic")),
    pose=E((0, POSES["idle"]), (T(40), POSES["flash"]), (T(83), POSES["look"]), (T(90), POSES["flash"]), (T(132), POSES["scared"])),
    gait=[(T(23), T(31), "walk"), (T(32), T(34), "walk"), (T(37), T(40), "walk"), (T(57), T(70), "walk")], flasharm=True)
NOAH_SPEC["wp"] = sorted(NOAH_SPEC["wp"], key=lambda e: e[0])
KID_SPECS = [(NOAH, NOAH_SPEC)]
def apply_monster(t):
    vis = t >= T(124); hide(MON.root, not vis)
    if not vis: return
    MON.root.location = (RX, RY + 33.5, 14.3); MON.root.rotation_euler.z = math.pi
    lift = 35 * smooth((t - T(136)) / 0.8) if t >= T(136) else 0.0
    MON.legs[0].rotation_euler.x = math.radians(lift); MON.legs[1].rotation_euler.x = 0
    bend = 72 * smooth((t - T(141)) / 1.1) if t >= T(141) else 0.0
    MON.upper.rotation_euler.x = -math.radians(bend)
    k = back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0
    MON.headpiv.rotation_euler = (math.radians(bend * 0.92), math.radians(24) * k, 0)
    for ap in MON.arms: ap.rotation_euler.x = math.radians(8 + 20 * smooth((t - T(141)) / 1.1))
def story_update(t):
    hide(cap_root, True)
    z = stair_z(NOAH.root.location.y - RY); NOAH.root.location.z = z + 2.0
    hide(FOOT, t < T(73))
    warm = 0.5 + (1.4 if t >= T(98) else 0.0)
    b = FOOTM.node_tree.nodes["Principled BSDF"]; b.inputs["Emission Color"].default_value = hexc("#FF9A3C"); b.inputs["Emission Strength"].default_value = (0.12 + (0.35 if t >= T(98) else 0.0)) if t >= T(73) else 0.0
    FOOTLIGHT.data.energy = (30 if t < T(98) else 90) if t >= T(73) else 0.0
    br = 1.0 + (0.05 * math.sin(2 * math.pi * 0.8 * t) if t >= T(99) else 0.0)
    FOOT.scale = (1, 1, br)
    shift = 14 * back((t - T(103)) / 0.14) if t >= T(103) else 0.0
    FOOT.rotation_euler.z = math.radians(shift)
    curl = 70 * smooth((t - T(108)) / 0.9) if t >= T(108) else 0.0
    for tp in TOES: tp.rotation_euler.x = math.radians(curl)
    DAY.data.energy = 900 if T(19) <= t < T(41) else 0.0
    DHINGE.rotation_euler.z = math.radians(-85 * smooth((t - T(36)) / 0.7)) if t >= T(36) else 0.0
