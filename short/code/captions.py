"""One-word-at-a-time captions: Montserrat ExtraBold 104 px, white, 13 px black outline, black shadow 4 right / 7 down @60%, key nouns red,
centred horizontally, vertical middle at 64% of the frame. Writes PNGs + an ffconcat list at 30 fps."""
import json, re, os
from PIL import Image, ImageDraw, ImageFont
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))+"/"; B=R+"build/"; OUT=B+"caps/"; os.makedirs(OUT,exist_ok=True)
W,H=1080,1920; FPS=30
tm=json.load(open(B+"timing.json")); END_T=tm["END_T"]
words=[(re.sub(r"[^A-Za-z0-9']","",w[0]),w[1],w[2]) for w in json.load(open(B+"words_final.json"))]
words+= [(re.sub(r"[^A-Za-z0-9']","",w[0]),w[1],w[2]) for w in tm["MON_WORDS"]]
RED={"lamp","lamps","cap","boy","light","shutters","doors","door","flashlight","sister","house","lock","black","winter"}
font=ImageFont.truetype(R+"fonts/Montserrat-ExtraBold.ttf",104)
def title(w): return w[:1].upper()+w[1:].lower() if not w.lower().startswith("noah") else "Noah's"
def render(word,red):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); 
    d=ImageDraw.Draw(im); x,y=W/2,0.64*H
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.text((x+4,y+7),word,font=font,anchor="mm",fill=(0,0,0,153),stroke_width=13,stroke_fill=(0,0,0,153))
    im.alpha_composite(sh)
    d.text((x,y),word,font=font,anchor="mm",fill=(236,28,36,255) if red else (255,255,255,255),stroke_width=13,stroke_fill=(0,0,0,255))
    return im
items=[]
for i,(w,a,b) in enumerate(words):
    if not w: continue
    start=max(0,a-0.03); nxt=words[i+1][1]-0.03 if i+1<len(words) and words[i+1][1]-0.03>start else None
    end=nxt if nxt else b+0.25
    if i==len(words)-1: end=b+0.25
    fn=OUT+f"w{i:03d}.png"; render(title(w),w.lower() in RED).save(fn); items.append((start,end,fn))
Image.new("RGBA",(W,H),(0,0,0,0)).save(OUT+"blank.png")
lines=["ffconcat version 1.0"]; t=0.0
snap=lambda x: round(x*FPS)/FPS
for s,e,fn in items:
    s,e=snap(s),snap(e)
    if s>t+1e-6: lines+= [f"file {OUT}blank.png",f"duration {s-t:.5f}"]
    if e>s: lines+= [f"file {fn}",f"duration {e-max(s,t):.5f}"]
    t=max(t,e)
lines+= [f"file {OUT}blank.png",f"duration {max(0.05,END_T-t):.5f}",f"file {OUT}blank.png"]
open(B+"caps.txt","w").write("\n".join(lines)+"\n"); print(len(items),"captions, ends",round(t,2))
