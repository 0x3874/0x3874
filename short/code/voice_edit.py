"""Cut the raw ElevenLabs take in real silence, re-space pauses, atempo, split monster line."""
import numpy as np, subprocess, json, re, difflib, random, sys
B="/home/user/0x3874/short/build/"; SR=44100; random.seed(7)
TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.22
raw=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",B+"voice_raw.wav","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout,np.float32)
words=json.load(open(B+"words_raw.json"))
lines=[l.strip() for l in open("/home/user/0x3874/short/script_lines.txt") if l.strip()]
norm=lambda t:re.sub(r"[^a-z0-9']","",t.lower())
S=[(norm(t),li) for li,l in enumerate(lines) for t in l.split()]
W=[norm(w[0]) for w in words]
sm=difflib.SequenceMatcher(None,[s[0] for s in S],W,autojunk=False)
m={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): m[b+k]=a+k
line_of=[S[m[i]][1] if i in m else None for i in range(len(words))]
for i in range(len(words)):          # fill gaps
    if line_of[i] is None: line_of[i]=line_of[i-1] if i else 0
# silences at -44 dB >=0.06 s
out=subprocess.run(["ffmpeg","-i",B+"voice_raw.wav","-af","silencedetect=n=-44dB:d=0.06","-f","null","-"],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; se=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
sil=list(zip(ss,se))
N=len(words); 
def pause_for(i):  # pause after word i
    if i==N-1: return None
    if words[i][0].strip(".,!?").lower()=="dies": return 0.95
    if line_of[i+1]!=line_of[i]:
        if line_of[i+1]==17: return 0.06+0.30+0.15   # longest, right before the twist
        return 0.06+random.uniform(0.08,0.30)
    return 0.11
chunks=[]; cur=0.0; cuts=[]
for i in range(N-1):
    p=pause_for(i)
    lo,hi=words[i][2]-0.05,words[i+1][1]+0.05
    c=[s for s in sil if s[1]>lo and s[0]<hi and s[1]-s[0]>=0.07]
    if not c: continue
    s,e=max(c,key=lambda s:s[1]-s[0])
    cuts.append((i,s,e,p))
# build
timeline=[]; segs=[]; t0=0.0; out_t=0.0; wmap={}
bounds=[(0.0,None)]+[(c,) for c in cuts]
pos=0.0; pieces=[]
for (i,s,e,p) in cuts:
    pieces.append((pos,s+0.035)); pieces.append(("gap",p)); pos=e-0.035
pieces.append((pos,len(raw)/SR))
audio=[]; cursor=0.0; chunk_starts=[]
for pc in pieces:
    if pc[0]=="gap":
        audio.append(np.zeros(int(pc[1]*SR),np.float32)); cursor+=pc[1]
    else:
        a,b=pc; chunk_starts.append((a,b,cursor)); audio.append(raw[int(a*SR):int(b*SR)].copy()); cursor+=b-a
def remap(t):
    for a,b,c in chunk_starts:
        if a-1e-6<=t<=b+1e-6: return c+t-a
    # in a removed region: snap to nearest chunk
    best=min(chunk_starts,key=lambda x:min(abs(t-x[0]),abs(t-x[1]))); return best[2]+(0 if t<best[0] else best[1]-best[0])
final=np.concatenate(audio)
# fades 5 ms at chunk joins
wt=[(w[0],remap(w[1]),remap(w[2]),line_of[k]) for k,w in enumerate(words)]
# split monster (last line index) 
mon_idx=[k for k,x in enumerate(wt) if x[3]==len(lines)-1]
split_t=(wt[mon_idx[0]-1][2]+wt[mon_idx[0]][1])/2
nar=final[:int(split_t*SR)]; mon=final[int(split_t*SR):]
def save(x,name):
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-",name],input=x.tobytes(),check=True)
save(nar,B+"nar_pre.wav"); save(mon,B+"mon_pre.wav")
json.dump({"words":wt,"split":split_t,"tempo":TEMPO,"mon_first":mon_idx[0]},open(B+"words_pre.json","w"))
sub=lambda i,o,f:subprocess.run(["ffmpeg","-v","error","-y","-i",i,"-af",f,o],check=True)
sub(B+"nar_pre.wav",B+"nar.wav",f"atempo={TEMPO}")
# monster: pitch down 5 st (asetrate+atempo), slow .92, echo, lowpass
r=2**(-5/12)
sub(B+"mon_pre.wav",B+"mon.wav",f"asetrate={int(SR*r)},aresample={SR},atempo={0.92/r:.5f},aecho=0.8:0.7:55|110:0.4|0.25,lowpass=f=6500")
d=lambda f:float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
print("cuts",len(cuts),"of",N-1,"| narration s",round(d(B+'nar.wav'),2),"monster s",round(d(B+'mon.wav'),2))
