# Story 7 "One Percent" -- Noah on his roof (house x=-45), phone at one percent
def W(i): return T(i) - 0.04
_mon_len = _wl(SD + "mon.wav")
MON_LATE = MON_T0 + 0.4
MON_END = MON_T0 + _mon_len
END_T = MON_END + 1.5
HX = -45.0; RZ = 14.0
hide(cap_root, True); hide(MON.root, True)
for k_ in (BOY,) + tuple(KIDS): hide(k_.root, True)
# phone floating in front of Noah, screen toward the street
PH = empty("phone", (HX, 25.2, 16.5)); box("pbody", (2.1, 0.3, 3.7), (0, 0, 0), mat("phonebody", hexc("#1B1B22")), PH)
SCR_M = mat("phonescreen", hexc("#DDE8FF"), emit=0.6)
box("pscreen", (1.8, 0.1, 3.3), (0, -0.2, 0), SCR_M, PH)
batt = box("battout", (1.1, 0.12, 0.7), (0, -0.27, 0.3), mat("battgrey", hexc("#9AA3B5")), PH); box("battin", (0.9, 0.14, 0.5), (0, -0.28, 0.3), SCR_M, PH)
RED_F = box("battred", (0.1, 0.16, 0.45), (-0.4, -0.3, 0.3), mat("battred", hexc("#EC1C24"), emit=3.0), PH)
BOLT = [box("bolt1", (0.28, 0.14, 0.5), (0.05, -0.33, 0.45), mat("bolt", hexc("#FFD21F"), emit=4.0), PH, rot=(0, math.radians(25), 0)), box("bolt2", (0.28, 0.14, 0.5), (-0.05, -0.33, 0.1), mat("bolt", hexc("#FFD21F"), emit=4.0), PH, rot=(0, math.radians(25), 0))]
BUBBLE = [box("bubble", (1.6, 0.12, 0.65), (0, -0.3, -0.9), mat("bubble", hexc("#4DA6FF"), emit=1.2), PH)]
# charger cable from the wall plug up to the roof and across to the phone
CABLE_M = mat("cable", hexc("#F4F4F4"))
CABLE = [box("plug", (0.6, 0.3, 0.9), (HX + 3, 23.9, 1.4), mat("plug", hexc("#6B6B75"))), box("cablev", (0.15, 0.15, 12.8), (HX + 3, 23.85, 8.0), CABLE_M),
         box("cableh", (0.15, 4.0, 0.15), (HX + 3, 25.7, 14.1), CABLE_M), box("cablec", (3.2, 0.15, 0.15), (HX + 1.4, 27.6, 14.1), CABLE_M), box("cableup", (0.15, 0.15, 2.5), (HX - 0.2, 27.6, 15.3), CABLE_M)]
# sister at the window (stands on a box so her head is in the window)
SILL_TOP = 3.4; SX = -52.0
box("sill", (4.6, 1.5, SILL_TOP), (SX, 23.2, SILL_TOP / 2), mat("sill", hexc("#6B4423")))
# goat in sunglasses on the roof
class Goat:
    def __init__(self):
        wm = mat("goatwhite", hexc("#EFEAD8")); hm = mat("horn", hexc("#C9B98A"))
        self.root = empty("Goat", (-38.5, 29.5, RZ)); self.piv = empty("goatpiv", (0, 0, 0), self.root)
        box("gbody", (1.9, 3.2, 2.1), (0, 0, 2.8), wm, self.piv)
        for lx, ly in ((-0.6, -1.1), (0.6, -1.1), (-0.6, 1.1), (0.6, 1.1)): box("gleg", (0.55, 0.55, 1.7), (lx, ly, 0.85), wm, self.piv)
        self.head = empty("ghead", (0, -1.7, 4.4), self.piv); box("gh", (1.4, 1.6, 1.5), (0, -0.3, 0.4), wm, self.head)
        for sx_ in (-0.5, 0.5): box("horn", (0.28, 0.28, 0.9), (sx_, 0.1, 1.5), hm, self.head, rot=(0, math.radians(sx_ * 25), 0))
        box("beard", (0.3, 0.3, 0.7), (0, -1.0, -0.2), hm, self.head); box("shades", (1.55, 0.25, 0.45), (0, -1.15, 0.75), mat("shades", hexc("#0D0D0F")), self.head)
        self.face = face_patch("gface", 0.95, 1.0, self.head, (0, -0.3, 0.4), deg=90); self.face.rotation_euler.z = math.pi; self.face.data.materials[0] = face_mat("smile")
        self.thumb = empty("thumb", (1.4, -1.3, 3.5), self.piv)
        box("fist", (0.8, 0.8, 0.8), (0, 0, 0), wm, self.thumb); box("thumbup", (0.3, 0.3, 0.8), (0, 0, 0.7), wm, self.thumb)
GOAT = Goat()
def resolve(v, t): return v
C = []
def S(start, c0, t0, fov, c1=None, t1=None, fov1=None, **kw):
    d = dict(c0=c0, t0=t0, fov=fov)
    if c1: d["c1"] = c1
    if t1: d["t1"] = t1
    if fov1: d["fov1"] = fov1
    d.update(kw); C.append((start, d))
PHP = (HX, 25.2, 16.5)
S(0.0,      (-45, 20, 16.6), PHP, 30, c1=(-45, 19, 16.6))                           # 1 phone at one percent
S(W(6),     (-45, 0, 9), (-45, 27, 15), 56, c1=(-45, 2, 9))                          # 2 Noah, on the roof
S(W(11),    (-45, 17, 17.5), (-45, 27, 16.5), 30, c1=(-45, 16, 17.5))                # 3 one message to send
S(W(17),    (-46, 21, 16.6), PHP, 28, c1=(-46, 20, 16.6))                            # 4 brightness down
S(W(25),    (-42, 19, 16.8), (-45, 26.5, 16.2), 32, c1=(-42, 18, 16.8))              # 5 Wi-Fi
S(W(31),    (-48, 19, 16.8), (-45, 26.5, 16.2), 32, c1=(-48, 18, 16.8))              # 6 Bluetooth
S(W(36),    (-30, -2, 7), (-45, 24, 8), 56, c1=(-32, -1, 7))                         # 7 the lights
S(W(41),    (-10, -4, 8), (-60, 24, 8), 58, c1=(-12, -3, 8))                         # 8 lights in the whole house
S(W(46),    (-45, -6, 8), (-45, 24, 10), 60, c1=(-45, -4, 8))                        # 9 whole house
S(W(50),    (-52, 10, 10), (-47, 27, 15), 46, c1=(-51, 11, 10))                      # 10 climbs onto the roof
S(W(56),    (-45, 12, 14), (-45, 27, 17), 40, c1=(-45, 13, 14))                      # 11 one bar of signal
S(W(61),    (-30, 24, 15.5), (-45, 27, 15), 50, c1=(-31, 22, 15.5))                  # 12 drags the cable
S(W(68),    (-52, 10, 6), (-52, 23.4, 6.5), 34, c1=(-52, 11, 6))                     # 13 sister watches
S(W(75),    (-50, 14, 7), (-52, 23.4, 7), 30, c1=(-50, 13, 7))                       # 14 what are you doing
S(W(81),    (-45, 17, 17), (-45, 27, 16.5), 30, c1=(-45, 16, 17))                    # 15 saving my battery
S(W(86),    (-46, 21, 16.6), PHP, 28, c1=(-46, 20, 16.6))                            # 16 types slowly
S(W(92),    (-45, 20, 16.6), PHP, 26, c1=(-45, 19, 16.6))                            # 17 can you bring a charger
S(W(97),    (-45, 17, 17.2), (-45, 27, 16.5), 28, c1=(-45, 16, 17.2))                # 18 holds his breath
S(W(101),   (-44, 20, 16.8), PHP, 26, c1=(-44, 19, 16.8))                            # 19 presses send
S(W(104),   (-45, 20, 16.6), PHP, 26, c1=(-45, 19, 16.6))                            # 20 screen goes dark
S(W(108),   (-50, 12, 7), (-52, 23.4, 7), 36, c1=(-50, 13, 7))                       # 21 sister points
S(W(114),   (-45, 19, 16.6), PHP, 24, c1=(-45, 18.5, 16.6))                          # 22 look at the corner
S(W(118),   (-45, 18, 16.7), (-44.9, 25.2, 17.0), 20, c1=(-45, 17.5, 16.7))          # 23 lightning bolt
S(W(122),   (-45, 18, 16.6), (-45, 25.2, 16.9), 20, c1=(-45, 17.6, 16.6))            # 24 next to the one percent
S(W(128),   (-45, 2, 11), (-45, 27, 16), 50, c1=(-45, 4, 11))                        # 25 charging the whole time
S(W(135),   (-45, 16, 17), (-45, 27, 16.5), 34, c1=(-45, 15, 17))                    # 26 looks at the dark house
S(W(141),   (-40, 12, 4), (-45, 24, 3), 40, c1=(-41, 12, 4))                         # 27 looks at the cable
S(W(146),   (-38, 10, 13), (-39, 27, 15.5), 44, c1=(-38, 11, 13))                    # 28 a goat in
S(W(150),   (-38, 16, 17), (-39, 29, 16.5), 30, c1=(-38, 15, 17))                    # 29 sunglasses, thumbs up
S(MON_T0 - 0.02, (-38.8, 19, 17), (-39, 29, 17), 24, c1=(-38.8, 18, 17))             # 30 Fully charged.
S(MON_END, (-42, 2, 10), (-42, 27, 15), 54, c1=(-42, 4, 10))                         # 31 hold
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
def windows_lit(t): return t < T(40)
def door_angle(hk, t): return 0.0
def flash_on(t): return False
def flash_pose(t): return None
SHUT = []
def apply_monster(t): hide(MON.root, True)
def E(*p): return list(p)
NOAH_SPEC = dict(vis=[(0, END_T + 1)], wp=[(0, HX, 27.2, 180)],
    face=E((0, "scared"), (T(11), "stern"), (T(17), "determined"), (T(97), "scared"), (T(104), "panic"), (T(128), "shock"), (T(135), "stern"), (T(146), "smile")),
    pose=E((0, POSES["brace"]), (T(56), POSES["panic"]), (T(61), POSES["brace"])))
SIS_SPEC = dict(vis=[(T(68) - 0.1, END_T + 1)], wp=[(0, SX, 23.0, 180)], face=E((0, "smile"), (T(75), "stern"), (T(108), "smile")),
    pose=E((0, POSES["idle"]), (T(108), POSES["point"])))
KID_SPECS = [(NOAH, NOAH_SPEC), (SIS, SIS_SPEC)]
def story_update(t):
    hide(cap_root, True)
    NOAH.root.location.z = RZ + 2.0
    SIS.root.location.z = SILL_TOP + 1.6
    # phone screen states
    b = SCR_M.node_tree.nodes["Principled BSDF"]
    if T(104) <= t < T(114): b.inputs["Emission Strength"].default_value = 0.0; b.inputs["Base Color"].default_value = (0.01, 0.01, 0.01, 1)
    else:
        b.inputs["Base Color"].default_value = hexc("#DDE8FF"); b.inputs["Emission Color"].default_value = hexc("#DDE8FF")
        b.inputs["Emission Strength"].default_value = 0.6 if t < T(17) else 0.18
    dark = T(104) <= t < T(114)
    for o_ in BOLT: o_.hide_render = not (t >= T(118))
    for o_ in BUBBLE: o_.hide_render = not (T(92) <= t < T(104))
    RED_F.hide_render = dark
    for o_ in CABLE[2:]: o_.hide_render = t < T(61)
    CABLE[1].hide_render = t < T(61)
    hide(GOAT.root, t < T(146)); GOAT.thumb.hide_render = t < T(150)
    for ch in GOAT.thumb.children: ch.hide_render = t < T(150)
    tilt = 24 * (back((t - MON_LATE) / 0.14) if t >= MON_LATE else 0.0)
    GOAT.head.rotation_euler = (0, math.radians(tilt), 0)
