"""Generic voice edit for a story folder: whisper words -> cut in real silence -> re-space pauses -> atempo -> split monster line (pitch -5 st, 0.92x, echo, lowpass)."""
import numpy as np, subprocess, json, re, difflib, random, sys, os, wave
from faster_whisper import WhisperModel
S=os.path.abspath(sys.argv[1])+"/"; SR=44100; random.seed(7)
cfg=json.load(open(S+"story.json")); TEMPO=cfg.get("tempo",1.25)
lines=[l.strip() for l in open(S+"script_lines.txt") if l.strip()]
def pcm(path,sr=SR): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac","1","-ar",str(sr),"-"],capture_output=True).stdout,np.float32).copy()
raw=pcm(S+"voice_raw.wav")
m=WhisperModel("large-v3-turbo",device="cpu",compute_type="int8")
seg,_=m.transcribe(pcm(S+"voice_raw.wav",16000),word_timestamps=True,language="en")
words=[(x.word.strip(),float(x.start),float(x.end)) for s in seg for x in s.words]
norm=lambda t:re.sub(r"[^a-z0-9']","",t.lower())
Sx=[(norm(t),li) for li,l in enumerate(lines) for t in l.split()]
sm=difflib.SequenceMatcher(None,[s[0] for s in Sx],[norm(w[0]) for w in words],autojunk=False)
mp={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): mp[b+k]=a+k
line_of=[Sx[mp[i]][1] if i in mp else None for i in range(len(words))]
for i in range(len(words)):
    if line_of[i] is None: line_of[i]=line_of[i-1] if i else 0
out=subprocess.run(["ffmpeg","-i",S+"voice_raw.wav","-af","silencedetect=n=-44dB:d=0.06","-f","null","-"],capture_output=True,text=True).stderr
sil=list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)],[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]))
N=len(words); tw=cfg.get("twist_line"); bw=cfg.get("blackout_word")
def pause_for(i):
    if bw and words[i][0].strip(".,!?\"").lower()==bw: return 0.95
    if line_of[i+1]!=line_of[i]:
        if tw is not None and line_of[i+1]==tw: return 0.06+0.30+0.15
        return 0.06+random.uniform(0.08,0.30)
    return 0.11
cuts=[]
for i in range(N-1):
    lo,hi=words[i][2]-0.05,words[i+1][1]+0.05
    c=[s for s in sil if s[1]>lo and s[0]<hi and s[1]-s[0]>=0.07]
    if c: s_,e_=max(c,key=lambda s:s[1]-s[0]); cuts.append((i,s_,e_,pause_for(i)))
pieces=[]; pos=0.0
for (i,s_,e_,p) in cuts: pieces.append((pos,s_+0.035)); pieces.append(("gap",p)); pos=e_-0.035
pieces.append((pos,len(raw)/SR))
audio=[]; cur=0.0; cs=[]
for pc in pieces:
    if pc[0]=="gap": audio.append(np.zeros(int(pc[1]*SR),np.float32)); cur+=pc[1]
    else: a,b=pc; cs.append((a,b,cur)); audio.append(raw[int(a*SR):int(b*SR)].copy()); cur+=b-a
def remap(t):
    for a,b,c in cs:
        if a-1e-6<=t<=b+1e-6: return c+t-a
    best=min(cs,key=lambda x:min(abs(t-x[0]),abs(t-x[1]))); return best[2]+(0 if t<best[0] else best[1]-best[0])
final=np.concatenate(audio); wt=[(w[0],remap(w[1]),remap(w[2]),line_of[k]) for k,w in enumerate(words)]
ml=cfg["monster_line"]; mi=[k for k,x in enumerate(wt) if x[3]==ml]
split=(wt[mi[0]-1][2]+wt[mi[0]][1])/2
def save(x,name): subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-",name],input=x.astype(np.float32).tobytes(),check=True)
save(final[:int(split*SR)],S+"nar_pre.wav"); save(final[int(split*SR):],S+"mon_pre.wav")
json.dump({"words":wt,"split":split,"tempo":TEMPO,"mon_first":mi[0],"monster_line":ml},open(S+"words_pre.json","w"))
sub=lambda i,o,f:subprocess.run(["ffmpeg","-v","error","-y","-i",i,"-af",f,o],check=True)
sub(S+"nar_pre.wav",S+"nar.wav",f"atempo={TEMPO}")
r=2**(-5/12); sub(S+"mon_pre.wav",S+"mon.wav",f"asetrate={int(SR*r)},aresample={SR},atempo={0.92/r:.5f},aecho=0.8:0.7:55|110:0.4|0.25,lowpass=f=6500")
def dur(p):
    with wave.open(p) as w: return w.getnframes()/w.getframerate()
# whisper again on the final narration (per spec) for word-keyed timing
seg,_=m.transcribe(pcm(S+"nar.wav",16000),word_timestamps=True,language="en")
fw=[(x.word.strip(),round(float(x.start),2),round(float(x.end),2)) for s in seg for x in s.words]
json.dump(fw,open(S+"words_final.json","w"))
print("cuts",len(cuts),"/",N-1,"| narration %.2fs monster %.2fs | final words %d | video ~%.1fs"%(dur(S+"nar.wav"),dur(S+"mon.wav"),len(fw),dur(S+"nar.wav")+0.22+dur(S+"mon.wav")+1.5))
