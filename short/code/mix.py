"""Build the final audio: voice, music bed (step-up on 'Run!'), drone, SFX peaks on word times, blackout silence, loudness."""
import numpy as np, subprocess, json, math, os, sys
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))+"/"; B=R+"build/"; SR=44100
WORDS=json.load(open(B+"words_final.json")); VOICE=json.load(open(B+"words_pre.json"))
T=lambda i:WORDS[i][1]; E=lambda i:WORDS[i][2]
NAR_END=37.7; MON_T0=NAR_END+0.22
def load(path,sr=SR):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac","1","-ar",str(sr),"-"],capture_output=True).stdout,np.float32).copy()
def db(x): return 20*np.log10(max(x,1e-9))
def rms_db(x): return db(np.sqrt(np.mean(x**2)))
def gain(x,d): return (x*10**(float(d)/20)).astype(np.float32)
tD=T(88)+0.06; tB=T(92)-0.04
pre_len=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",B+"mon_pre.wav"]))
nar=load(B+"nar.wav"); mon=load(B+"mon.wav"); mon_len=len(mon)/SR
mw=[x for x in VOICE["words"] if x[3]==22]
MON_WORDS=[(w[0],MON_T0+(w[1]-VOICE["split"])*(mon_len/pre_len),MON_T0+(w[2]-VOICE["split"])*(mon_len/pre_len)) for w in mw]
MON_END=MON_T0+mon_len; END_T=MON_END+1.5
N=int(END_T*SR)+SR
# ---- voice: speech median at -15 dB (frame RMS over speech frames)
fr=nar[:len(nar)//441*441].reshape(-1,441); fdb=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
med=np.median(fdb[fdb>-40]); vg=-15-med; nar=gain(nar,vg); mon=gain(mon,vg+1.0)
print("voice median %.1f dB -> gain %.1f dB"%(med,vg))
mix_v=np.zeros(N,np.float32); mix_v[:len(nar)]+=nar; i0=int(MON_T0*SR); mix_v[i0:i0+len(mon)]+=mon[:N-i0]
# ---- music bed: find the step-up in track 564 and place it on "Run!"
mus=load(R+"sfx/music/564.mp3")
w=int(0.25*SR); e=np.array([rms_db(mus[i:i+w]) for i in range(0,len(mus)-w,w//2)]); hop=0.125
rise=[(e[i+4:i+12].mean()-e[i-8:i-2].mean(),i) for i in range(int(100/0.125),min(len(e)-14,int(200/0.125)))]
best=max(rise); step_t=(best[1]+4)*hop; print("music step-up at %.2fs (+%.1f dB)"%(step_t,best[0]))
run_t=T(75); start=step_t-run_t
bed=mus[int(start*SR):int(start*SR)+N]; bed=np.pad(bed,(0,N-len(bed)))
bed=gain(bed,-21-rms_db(bed[:int((tD)*SR)]))
# ducking 4 dB under every word, fast attack ~10 ms, release 0.25 s
duck=np.zeros(N,np.float32); words=[(w[1],w[2]) for w in WORDS]+[(a,b) for _,a,b in MON_WORDS]
for a,b in words: duck[int(max(0,a-0.03)*SR):int(b*SR)]=1.0
def smooth_env(x,att=0.01,rel=0.25):
    out=np.zeros_like(x); y=0.0; ca=math.exp(-1/(att*SR)); cr=math.exp(-1/(rel*SR))
    for i in range(0,len(x),8):
        v=x[i]; c=ca if v>y else cr; y=c*y+(1-c)*v; out[i:i+8]=y
    return out
bed*=10**(-4*smooth_env(duck)/20)
# blackout: dead at tD, quiet return at tB, fade out ending 0.5 s before monster speaks
env=np.ones(N,np.float32); t=np.arange(N)/SR
env[(t>=tD)&(t<tB)]=0.0
env[t>=tB]=10**(-9/20)
f0,f1=MON_T0-1.3,MON_T0-0.5
env[t>=f1]=0; m=(t>=f0)&(t<f1); env[m]*=1-(t[m]-f0)/(f1-f0)
# 5 ms ramps at the hard cuts
for c,up in ((tD,False),(tB,True)):
    k=int(0.005*SR); i=int(c*SR); ramp=np.linspace(0,1,k)
    env[i:i+k]*= ramp if up else 1
    if not up: env[i-k:i]*=1-ramp[:k]*0  # dead on the word, no pre-fade
bed*=env
# drone, -34 dB, same blackout gating
dr=load(R+"sfx/2510.mp3"); dr=np.tile(dr,int(N/len(dr))+1)[:N]; dr=gain(dr,-34-rms_db(dr)); dr*=env
# ---- SFX with peak on word
def sfx(file,d,at,tail=None,peak_at_end=False):
    x=load(R+f"sfx/{file}.mp3"); pk=np.abs(x).argmax()
    x=gain(x,d-db(np.abs(x).max())); 
    if tail: 
        n=int(tail*SR); 
        if len(x)>pk+n: x=x[:pk+n].copy(); x[-int(0.4*SR):]*=np.linspace(1,0,int(0.4*SR))
    return x,int(at*SR)-pk
S=[("1143",-15,T(20)),                         # first vanishing: deep impact
   ("2182",-19,T(35)),("194",-20,T(37)-0.1),   # shutter slam, door slam
   ("2299",-14,T(58)),("2300",-17,T(60)),("2299",-14,T(61)),("2300",-17,T(65)),   # chase steps
   ("197",-20,T(77)+0.1),("197",-20,T(78)+0.1),("197",-20,T(79)+0.35),           # knocks
   ("790",-21,tD-0.15),("788",-15,tD-0.0),("2782",-11,tD+0.35),                    # riser -> boom -> big boom
   ("724",-15,tB),                              # braam as lights return
   ("190",-18,T(116)+0.25),                     # door creak
   ("2908",-11,MON_END),("677",-19,MON_END)]    # trailer hit + sting after the last word
sfxmix=np.zeros(N,np.float32)
for f,d,at in S:
    x,i=sfx(f,d,at,tail=(0.9 if f in("2782","788") else None))
    if i<0: x=x[-i:]; i=0
    n=min(len(x),N-i); sfxmix[i:i+n]+=x[:n]
# silence window: nothing but the booms' own tails is allowed after tD+1.0 until tB (kill anything stray)
sfxmix[int((tD+1.0)*SR):int(tB*SR)]=0
tot=mix_v+bed+dr+sfxmix
tot=tot[:int(END_T*SR)].astype(np.float32)
np.save(B+"mix_f32.npy",tot)
def lufs(x):
    o=subprocess.run(["ffmpeg","-nostats","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","ebur128","-f","null","-"],input=x.astype(np.float32).tobytes(),capture_output=True).stderr.decode()
    return float(o.split("I:")[-1].split("LUFS")[0])
# mix to -13 LUFS, then tanh soft clip at 0.75; trim pre-gain so the clipped result lands at -14 (what survives AAC)
g=-13-lufs(tot)
for _ in range(4):
    x=(0.75*np.tanh(gain(tot,g)/0.75)).astype(np.float32); l=lufs(x)
    if abs(l+14)<0.15: break
    g+= (-14-l)
print("pre-clip gain %.1f dB, final %.1f LUFS"%(g,l))
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-ac","2",B+"final_audio.wav"],input=x.tobytes(),check=True)
print("audio done, length %.2fs, peak %.1f dBFS"%(len(x)/SR,db(np.abs(x).max())))
json.dump({"END_T":END_T,"MON_WORDS":MON_WORDS,"tD":tD,"tB":tB,"MON_T0":MON_T0},open(B+"timing.json","w"))
