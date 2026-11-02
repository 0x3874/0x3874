"""Audio for one story folder: voice, music bed (step-up on a chosen word), drone, SFX peaks on words, loudness -> final_audio.wav + timing.json"""
import numpy as np, subprocess, json, math, os, sys, wave
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))+"/"; S=os.path.abspath(sys.argv[1])+"/"; SR=44100
cfg=json.load(open(S+"story.json")); WORDS=json.load(open(S+"words_final.json")); VOICE=json.load(open(S+"words_pre.json"))
T=lambda i:WORDS[i][1]
def pcm(p): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout,np.float32).copy()
def db(x): return 20*np.log10(max(float(x),1e-9))
def rms_db(x): return db(np.sqrt(np.mean(x**2)))
def gain(x,d): return (x*10**(float(d)/20)).astype(np.float32)
def dur(p):
    with wave.open(p) as w: return w.getnframes()/w.getframerate()
nar=pcm(S+"nar.wav"); mon=pcm(S+"mon.wav"); NAR_END=dur(S+"nar.wav"); MON_T0=NAR_END+0.22; mon_len=dur(S+"mon.wav"); MON_END=MON_T0+mon_len; END_T=MON_END+1.5
N=int(END_T*SR)+SR
fr=nar[:len(nar)//441*441].reshape(-1,441); fdb=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9); vg=-15-np.median(fdb[fdb>-40])
nar=gain(nar,vg); mon=gain(mon,vg+1.0)
voice=np.zeros(N,np.float32); voice[:len(nar)]+=nar; i0=int(MON_T0*SR); voice[i0:i0+len(mon)]+=mon[:N-i0]
# music bed: step-up of track 564 lands on step_word
mus=pcm(R+"sfx/music/564.mp3"); STEP=144.88
start=STEP-T(cfg["step_word"]); bed=mus[int(start*SR):int(start*SR)+N]; bed=np.pad(bed,(0,N-len(bed)))
bed=gain(bed,-21-rms_db(bed[:int(T(cfg["step_word"])*SR)]))
duck=np.zeros(N,np.float32)
mw=[x for x in VOICE["words"] if x[3]==cfg["monster_line"]]
for w in WORDS: duck[int(max(0,w[1]-0.03)*SR):int(w[2]*SR)]=1.0
def env(x,att=0.01,rel=0.25):
    o=np.zeros_like(x); y=0.0; ca=math.exp(-1/(att*SR)); cr=math.exp(-1/(rel*SR))
    for i in range(0,len(x),8):
        v=x[i]; c=ca if v>y else cr; y=c*y+(1-c)*v; o[i:i+8]=y
    return o
bed*=10**(-4*env(duck)/20)
t=np.arange(N)/SR; g=np.ones(N,np.float32); f0,f1=MON_T0-1.3,MON_T0-0.5
g[t>=f1]=0; m=(t>=f0)&(t<f1); g[m]=1-(t[m]-f0)/(f1-f0); bed*=g
dr=pcm(R+"sfx/2510.mp3"); dr=np.tile(dr,int(N/len(dr))+1)[:N]; dr=gain(dr,-34-rms_db(dr))*g
def sfx(f,d,at,tail=None):
    x=pcm(R+f"sfx/{f}.mp3"); pk=int(np.abs(x).argmax()); x=gain(x,d-db(np.abs(x).max()))
    if tail:
        n=int(tail*SR)
        if len(x)>pk+n: x=x[:pk+n].copy(); x[-int(0.4*SR):]*=np.linspace(1,0,int(0.4*SR))
    return x,int(at*SR)-pk
fx=np.zeros(N,np.float32)
for f,d,(kind,i,off) in cfg["sfx"]:
    at = MON_END if kind=="mon_end" else T(i)+off
    x,k=sfx(f,d,at,tail=(1.0 if f in("788","2782") else None))
    if k<0: x=x[-k:]; k=0
    n=min(len(x),N-k); fx[k:k+n]+=x[:n]
tot=(voice+bed+dr+fx)[:int(END_T*SR)].astype(np.float32)
def lufs(x):
    o=subprocess.run(["ffmpeg","-nostats","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","ebur128","-f","null","-"],input=x.astype(np.float32).tobytes(),capture_output=True).stderr.decode()
    return float(o.split("I:")[-1].split("LUFS")[0])
gg=-13-lufs(tot)
for _ in range(4):
    x=(0.75*np.tanh(gain(tot,gg)/0.75)).astype(np.float32); l=lufs(x)
    if abs(l+14)<0.15: break
    gg+=-14-l
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-ac","2",S+"final_audio.wav"],input=x.tobytes(),check=True)
json.dump({"END_T":END_T,"MON_T0":MON_T0,"MON_WORDS":[(w[0],MON_T0+0.03,MON_T0+0.03+mon_len*0.55) for w in mw[:1]]},open(S+"timing.json","w"))
print("audio %.2fs, %.1f LUFS, peak %.1f dBFS"%(len(x)/SR,l,db(np.abs(x).max())))
