# exec'd inside build.py: shot list, actor timelines, and world-state functions (all pure functions of time t)
def W(i): return T(i) - 0.04
tD = T(88) + 0.06               # last lamp (and everything) dies
tB = W(92)                      # lights come back
def in_blackout(t): return tD <= t < tB

# monster line timing (from the pre-tempo word times, scaled to the processed file)
import wave
def _wav_len(p):
    with wave.open(p) as w_: return w_.getnframes() / w_.getframerate()
_pre_len = _wav_len(ROOT + "build/mon_pre.wav")
_mon_len = _wav_len(ROOT + "build/mon.wav")
_mw = [x for x in VOICE["words"] if x[3] == 22]
MON_LATE = MON_T0 + (_mw[-1][1] - VOICE["split"]) * (_mon_len / _pre_len)
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5

# ---------------------------------------------------------------- shots (start time, camera)
N_DOOR = (-45, 24); NB = HOUSES[NOAH_HOUSE];
C = []  # (start, dict)
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=c0, t0=t0, fov=fov);
    if c1: d["c1"] = c1
    if t1: d["t1"] = t1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
OPEN_C0, OPEN_T0 = (152, -5, 9), (-40, 3, 6)
S(0.0,       OPEN_C0, OPEN_T0, 64, c1=(142, -5, 8.6))                                   # 1 wide, town obeying
S(W(6),      (34, 0, 7), (-15, 11, 8), 52, c1=(30, 0, 7))                               # 2 the unlit last lamp
S(W(9),      (-3, 3, 11), (-15, 11, 12.6), 36, c1=(-5, 4, 11.4))                        # 3 close on globe, lights at "lit"
S(W(12),     (30, 3, 6), (60, -17, 5.5), 50, c1=(33, 3, 6))                             # 4 swing drifting
S(W(15),     (-30, -2, 4.2), (-75, 8, 4), 54, c1=(-34, -1, 4.2))                         # 5 boy alone
S(W(18),     (-60, 2.5, 5.5), (-80, 10, 6), 46, c1=(-62, 3, 5.5))                        # 6 boy caught
S(W(21),     (-72, 0, 3.4), (-78, 9.2, 0.8), 40, c1=(-73, 1, 3.0))                      # 7 cap rocking
S(W(27),     (-75, 3, 9.7), (-75, 23.6, 9.7), 38, c1=(-75, 6, 9.7))                    # 8 clock
S(W(32),     (85, -2, 3.5), (30, -9.5, 4), 54, c1=(80, -2, 3.5))                        # 9 running home
S(W(34),     (10, 2, 6.5), (10, 24, 6.5), 38, c1=(10, 5, 6.5))                          # 10 shutter
S(W(36),     (15, 4, 5), (15, 24, 4.5), 38, c1=(15, 7, 5))                              # 11 door bolt
S(W(38),     (-45, 12, 5.4), (-45, 20, 5.2), 38, c1=(-45, 13, 5.4))                     # 12 Noah decides
S(W(40),     (-3, -8, 8), (-15, 9, 3), 58, c1=(-5, -7, 7.5))                            # 13 sister alone
S(W(46),     (-45, 6, 5.6), (-45, 20, 4.4), 44, c1=(-45, 7.5, 5.4))                     # 14 grabs
S(W(49),     (-40, 9, 5), (-45, 19.5, 4), 38, c1=(-41, 10.5, 4.8))                      # 15 flashlight on
S(W(54),     (115, -3, 7), (-60, 2, 6), 60, c1=(110, -3, 7))                            # 16 something tall
S(W(58),     (-48, 3, 2.2), (-98, 2, 6), 44, c1=(-50, 3, 2.3))                          # 17 step one
S(W(60),     (-48, 3, 2.2), (-72, 2, 6.5), 44, c1=(-49, 3, 2.3))                        # 18 then... another
S(W(62),     (-56, 6, 5.2), (-33, 9, 4.8), 36, c1=(-54, 6, 5.2))                        # 19 Noah looks back
S(W(65),     (-18, 1, 2.0), (-42, 2, 6), 40, c1=(-20, 1.5, 2.0), fov1=36)               # 20 it is closer
S(W(68),     (-40, 0, 3.5), (-15, 9.5, 3.5), 50, c1=(-36, 0, 3.5))                      # 21 finds her
S(W(71),     (8, 3, 5), (-12, 9.5, 5.3), 40, c1=(6, 3.5, 5))                            # 22 under the last lamp
S(W(75),     (11, 6, 5.4), (-10, 9.5, 4.8), 34, c1=(9, 6, 5.4))                        # 23 Run!
S(W(76),     (-11, -1, 4), (-13, 18, 4), 56, c1=(-11, 1, 4))                            # 24 run to the door
S(W(79),     (-24, 5, 5.6), (-15, 22.5, 4.6), 40, c1=(-23, 6, 5.6))                   # 25 pounding
S(W(81),     (-4, 19, 5.3), (-14.5, 21.5, 4.7), 38, c1=(-5, 19.5, 5.3))                 # 26 nobody answers
S(W(83),     (5, 4, 8), (-14, 8, 8.5), 56, c1=(3, 4.5, 8.2))                             # 27 last lamp, dark behind
S(W(86),     (4, 3, 12.5), (-15, 11, 12.8), 40, c1=(3, 4, 12.5))                        # 28 flicker
S(tD,        (20, -8, 2), (-20, 24, 14), 62, c1=(19, -8, 2.2))                          # 29 roofs, stars, silence
S(W(89),     (-50, -6, 2.5), (10, 26, 14), 66, c1=(-48, -6, 2.6))                       # 30 more roofs
S(tB,        OPEN_C0, OPEN_T0, 64, c1=(142, -5, 8.6))                                   # 31 same wide, but wrong
S(W(96),     (60, -8, 5.2), (60, 24, 5.2), 62, c1=(-20, -8, 5.2), t1=(-20, 24, 5.2))    # 32 slide along the empty houses
S(W(100),    (-45, 2, 4.9), (-45, 16, 4.6), 36, c1=(-45, 3, 4.9))                       # 33 two-shot
S(W(106),    (-52, 4, 5), (-45, 16, 4.6), 34, c1=(-50, 5, 5))                           # 34 two-shot closer
S(W(110),    (-30, 8, 5.4), (-45, 17, 4.8), 38, c1=(-31, 8, 5.4))                       # 35 Noah turns
S(W(116),    (-45, 2, 6), (-45, 24, 5), 46, c1=(-45, 3, 6))                             # 36 door opens onto black
S(W(120),    (-45, 0, 6.5), (-45, 24, 6.5), 58, c1=(-45, 1, 6.5))                       # 37 it bends out
S(MON_T0 - 0.02, ("MC", 0), ("MD", 0), 60, c1=("MC", 0), t1=("MD", 0))                  # 38 from its height
S(MON_LATE - 0.04, ("MHC", 13.0), "MH", 40, c1=("MHC", 14.0), t1="MH")                  # 39 last word, head snaps
SHOTS = []
for i, (st, d) in enumerate(C):
    d["start"] = st; d["end"] = C[i + 1][0] if i + 1 < len(C) else END_T; SHOTS.append(d)
def shot_at(t):
    cur = SHOTS[0]
    for s_ in SHOTS:
        if s_["start"] <= t: cur = s_
    return cur

# ---------------------------------------------------------------- monster
M_STEPS = [(0, (-125, 2, -90)), (T(56), (-115, 2, -90)), (T(58), (-98, 2, -90)), (T(60), (-80, 2, -90)), (T(61), (-64, 2, -90)),
           (T(65), (-50, 2, -90)), (T(67), (-40, 3, -90)), (T(72), (-32, 4.5, -90)), (T(75), (-26, 5, -90)), (T(86), (-22, 5.5, -90))]
M_VIS = [(T(55), tD), (W(18) + 0.0, T(20) + 0.02), (W(119), END_T + 1)]
def monster_bend(t): return 72 * smooth((t - W(120)) / 1.5)
def apply_monster(t):
    if t < W(118): vis = any(a <= t <= b for a, b in M_VIS[:2])
    else: vis = True
    # the caught-boy scene: monster behind the boy
    hide(MON.root, not vis)
    if not vis: return
    if t < W(110):
        if t < T(21):  # behind the boy
            pos = (-86, 12.5, -100); arms = (80 if t >= T(19) else 5)
        else:
            pos = track_val([(a, v) for a, v in M_STEPS], t, 0.14)
            arms = 6
        x, y, rz = pos
        n = sum(1 for a, _ in M_STEPS if a <= t)
        lleg = 22 if n % 2 else -22; rleg = -lleg
        MON.legs[0].rotation_euler.x = math.radians(lleg); MON.legs[1].rotation_euler.x = math.radians(rleg)
        MON.arms[0].rotation_euler.x = math.radians(arms + 4 * math.sin(t * 2)); MON.arms[1].rotation_euler.x = math.radians(arms - 4 * math.sin(t * 2))
        MON.root.location = (x, y, 0); MON.root.rotation_euler.z = math.radians(rz)
        MON.upper.rotation_euler.x = 0
        MON.headpiv.rotation_euler = (0, 0, 0)
    else:  # in the doorway: emerge, bend, last word
        MON.root.location = (-45, 27.0, 0); MON.root.rotation_euler.z = math.radians(180)
        MON.upper.rotation_euler.x = -math.radians(monster_bend(t))
        k = back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0
        MON.headpiv.rotation_euler = (math.radians(monster_bend(t) * 0.92), math.radians(24) * k, 0)   # head looks level; snaps sideways on the last word
        for ap in MON.arms: ap.rotation_euler.x = math.radians(10 + 30 * smooth((t - W(120)) / 1.5))
        for lp in MON.legs: lp.rotation_euler.x = 0

def MH_pos(t):
    bpy.context.view_layer.update(); w_ = MON.headpiv.matrix_world @ Vector((0, 0, 0.9)); return (w_.x, w_.y, w_.z)
def _old_MH(t):
    th = math.radians(monster_bend(t)); h = 4.3 + 3.4 + 0.9 - 4.3  # head centre above hip pivot
    hip = Vector((-45, 27.0, 4.4)); off = Vector((0, 0, 3.4 + 0.9))
    off = Vector((0, off.z * math.sin(th) * -1 * -1, off.z * math.cos(th)))   # forward (-y world) when facing south
    return (hip.x, hip.y - abs(off.y), hip.z + off.z)
def resolve(v, t):
    if isinstance(v, str):
        if v == "MH": return MH_pos(t)
    if isinstance(v, tuple) and v and v[0] == "MHC": return (-45, v[1], MH_pos(t)[2])
    if isinstance(v, tuple) and v and v[0] == "MC": return (-45, 20.5 + 0.0, 9.6 - 0.4 * smooth((t - MON_T0) / 1.7))
    if isinstance(v, tuple) and v and v[0] == "MD": return (-44.5, 15.0, 3.8)
    return v

# ---------------------------------------------------------------- kids
def E(*pairs): return list(pairs)
FACE_NOAH = E((0, "determined"), (W(46), "determined"), (W(62), "scared"), (W(64), "panic"), (W(68), "scared"), (W(75), "panic"), (W(88), "shock"), (tB, "shock"), (W(100), "scared"), (W(110), "shock"))
FACE_SIS = E((0, "scared"), (W(75), "panic"), (W(88), "shock"), (W(100), "scared"), (W(116), "shock"))
NOAH_WP = [(0, -45, 20, 180), (16.0, -45, 20, 180), (16.5, -45, 10.5, -90), (20.9, -12.5, 9.5, -90), (21.5, -10, 9.5, -90),
           (22.6, -10, 9.5, -90), (23.3, -10, 9.5, 0), (23.9, -15, 21.0, 0), (tD + 0.3, -15, 21.0, 0), (tB - 0.01, -15, 21.0, 0),
           (tB, -46, 15.5, 180), (T(110), -46, 15.5, 180), (W(115) + 0.5, -46, 15.5, 0), (END_T + 1, -46, 15.5, 0)]
NOAH_POSE = E((0, POSES["idle"]), (W(46), POSES["idle"]), (T(47), POSES["grab"]), (T(48.5 if False else 49), POSES["flash"]), (16.0, POSES["flash"]), (W(62), POSES["look"]),
              (W(65), POSES["flash"]), (W(71), POSES["scared"]), (W(75), POSES["panic"]), (23.3, POSES["flash"]), (W(79), POSES["pound"]), (W(81), POSES["side"]), (W(86), POSES["scared"]),
              (tB, POSES["scared"]), (W(110), POSES["idle"]))
NOAH_SPEC = dict(vis=[(W(38) - 0.3, END_T + 1)], wp=NOAH_WP, pose=NOAH_POSE, face=FACE_NOAH,
                 gait=[(16.0, 20.9, "run"), (23.3, 23.9, "run")], flasharm=True)
SIS_SPEC = dict(vis=[(W(40) - 0.3, END_T + 1)], wp=[(0, -13, 9.5, 180), (22.6, -13, 9.5, 180), (23.3, -13, 9.5, 0), (23.9, -15, 22.2, 0), (tB - 0.01, -15, 22.2, 0),
                                                    (tB, -43.5, 15.5, 180), (T(112), -43.5, 15.5, 180), (T(116), -43.5, 15.5, 0), (END_T + 1, -43.5, 15.5, 0)],
                pose=E((0, POSES["crouch"]), (W(71), POSES["scared"]), (W(75), POSES["panic"]), (tB, POSES["scared"])), face=FACE_SIS,
                gait=[(23.3, 23.9, "run")], phase=1.0)
BOY_SPEC = dict(vis=[(4.0, T(20))], wp=[(4.0, -64, 9.2, 90), (T(18), -78, 9.2, 90), (T(18) + 0.05, -78, 9.2, 90), (T(20), -78, 9.2, 90)],
                pose=E((0, POSES["idle"]), (W(18), POSES["scared"]), (T(19), POSES["panic"])), face=E((0, "smile"), (W(18), "scared"), (T(19), "panic")),
                gait=[(4.0, T(18), "walk")])
def runner(x0, y0, x1, y1, t0, t1, ph, face="panic", rz=-90):
    return dict(vis=[(t0 - 1.0, t1 + 0.6)], wp=[(t0 - 1.0, x0, y0, rz), (t0, x0, y0, rz), (t1, x1, y1, rz), (t1 + 0.6, x1, y1 - 0.0, rz)], face=E((0, face)),
                gait=[(t0 - 1.0, t1, "run")], phase=ph)
KSP = [
    dict(vis=[(0, 1.9)], wp=[(0, 62, 9, 90), (1.9, 28, 9, 90)], face=E((0, "smile")), gait=[(0, 1.9, "walk")], phase=0.0),               # S1 commuters
    dict(vis=[(0, 1.9)], wp=[(0, 80, -9.5, 90), (1.9, 44, -9.5, 90)], face=E((0, "stern")), gait=[(0, 1.9, "walk")], phase=2.0),
    dict(vis=[(1.4, 2.5)], wp=[(1.4, -2, 8.5, 90), (2.5, -14, 8.5, 90)], face=E((0, "smile")), gait=[(1.4, 2.5, "walk")], phase=1.0),    # S2 passer by
    runner(10, -9, 62, -9, T(32) - 0.2, T(33) + 0.9, 0.0), runner(2, -10.5, 56, -10.5, T(32) - 0.2, T(33) + 0.9, 1.4),
    runner(22, -9.6, 70, -9.6, T(32) - 0.2, T(33) + 0.9, 0.7), runner(-4, -11, 48, -11, T(32) - 0.2, T(33) + 0.9, 2.1),
]
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC), (BOY, BOY_SPEC)]
# commuter kids: K0,K1 used for S1 and S2, K2.. share runners (distinct kids; reuse is fine across shots)
_pool = [KIDS[0], KIDS[1], KIDS[2], KIDS[3]]
KID_SPECS += [(_pool[0], KSP[0]), (_pool[1], KSP[1])]
_extra = [KSP[2], KSP[3], KSP[4], KSP[5]]
# S2 passer-by uses K2; runners use K0,K1,K2,K3 after their commute shot ended (times don't overlap)
KID_SPECS += [(_pool[2], KSP[2])]
RUN_SPECS = KSP[3:]
for k_, s_ in zip(_pool, RUN_SPECS):
    # merge: runner spec is used instead of commuter when t > 8
    pass
def _wrap(kid, a, b):
    return (kid, dict(vis=a["vis"] + b["vis"], wp=sorted(a["wp"] + b["wp"], key=lambda e: e[0]), face=a["face"], gait=a["gait"] + b["gait"], phase=a["phase"] if "phase" in a else 0))
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC), (BOY, BOY_SPEC)]
KID_SPECS.append(_wrap(_pool[0], KSP[0], RUN_SPECS[0])); KID_SPECS.append(_wrap(_pool[1], KSP[1], RUN_SPECS[1]))
KID_SPECS.append(_wrap(_pool[2], KSP[2], RUN_SPECS[2])); KID_SPECS.append((_pool[3], RUN_SPECS[3]))

# ---------------------------------------------------------------- lamps, windows, doors, flashlight
def lamp_on(L, t):
    if L["last"] and t < T(11) + 0.06: return False
    if in_blackout(t): return False
    if t < tD: return bool(flick(t, tD))
    return True
def windows_lit(t): return not in_blackout(t)
def door_angle(hk, t):
    side, i = hk
    if hk == NOAH_HOUSE:
        if t < T(116): return 0.0
        if t < tB: return 0.0
        return -80 * smooth((t - T(116)) / 1.2) if t >= T(116) else 0.0
    if t >= tB: return -100.0 if hk != NOAH_HOUSE else 0.0
    if hk == ("N", 5):           # the door that bolts
        if t < T(37) - 0.1: return -80.0
        k = back((t - (T(37) - 0.1)) / 0.14); return -80 * (1 - k)
    return 0.0
def flash_on(t):
    if t < T(49) or t >= tD: return False
    if t >= tD - 0.12: return bool(flick(t, tD))
    return True
def flash_pose(t):
    if t < T(47) + 0.12 or t > tD + 0.2: return None
    bpy.context.view_layer.update()
    hand = NOAH.arms[1].matrix_world @ Vector((0, 0.35, -1.8))
    rz = NOAH.root.rotation_euler.z; d = Vector((-math.sin(rz), math.cos(rz), -0.18))
    return (tuple(hand), tuple(d))
