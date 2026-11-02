"""Draw flat cartoon face decals (1024x578, transparent bg) with Pillow. Features stay in the middle 45%."""
from PIL import Image, ImageDraw
import os, math
W,H=1024,578; OUT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","build","faces"))+"/"
K=(0,0,0,255)
def canvas(): 
    im=Image.new("RGBA",(W,H),(0,0,0,0)); return im,ImageDraw.Draw(im)
def eye(d,cx,cy,rx=22,ry=46,fill=True):
    d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=K)
def brow(d,x0,y0,x1,y1,w=18): d.line((x0,y0,x1,y1),fill=K,width=w)
def smile(d,cx,cy,w,h,t=16,a0=15,a1=165): d.arc((cx-w,cy-h,cx+w,cy+h),a0,a1,fill=K,width=t)
def frown(d,cx,cy,w,h,t=16): d.arc((cx-w,cy,cx+w,cy+2*h),195,345,fill=K,width=t)
def make():
    cx,cy,ex=W//2,H//2,90   # feature width ~ +-230px (45%)
    faces={}
    im,d=canvas(); eye(d,cx-ex,cy-30);eye(d,cx+ex,cy-30); smile(d,cx,cy+10,120,70); faces["smile"]=im
    im,d=canvas(); eye(d,cx-ex,cy-30,22,36);eye(d,cx+ex,cy-30,22,36); brow(d,cx-ex-40,cy-95,cx-ex+40,cy-95); brow(d,cx+ex-40,cy-95,cx+ex+40,cy-95); d.line((cx-70,cy+70,cx+70,cy+70),fill=K,width=16); faces["stern"]=im
    im,d=canvas(); eye(d,cx-ex,cy-20,22,36);eye(d,cx+ex,cy-20,22,36); brow(d,cx-ex-45,cy-110,cx-ex+45,cy-70,20); brow(d,cx+ex+45,cy-110,cx+ex-45,cy-70,20); frown(d,cx,cy+55,100,45); faces["angry"]=im
    im,d=canvas(); 
    for s in(-1,1): d.ellipse((cx+s*ex-34,cy-70,cx+s*ex+34,cy+4),outline=K,width=10); d.ellipse((cx+s*ex-8,cy-38,cx+s*ex+8,cy-20),fill=K)
    brow(d,cx-ex-40,cy-115,cx-ex+30,cy-135,14); brow(d,cx+ex+40,cy-115,cx+ex-30,cy-135,14); d.arc((cx-70,cy+40,cx+70,cy+110),200,340,fill=K,width=14); faces["scared"]=im
    im,d=canvas()
    for s in(-1,1): d.ellipse((cx+s*ex-40,cy-85,cx+s*ex+40,cy-5),outline=K,width=10); d.ellipse((cx+s*ex-6,cy-48,cx+s*ex+6,cy-36),fill=K)
    d.ellipse((cx-55,cy+30,cx+55,cy+130),fill=K); faces["panic"]=im
    im,d=canvas()
    for s in(-1,1): d.ellipse((cx+s*ex-30,cy-60,cx+s*ex+30,cy+0),outline=K,width=10)
    d.ellipse((cx-24,cy+45,cx+24,cy+105),fill=K); faces["shock"]=im
    im,d=canvas(); eye(d,cx-ex,cy-25,22,34);eye(d,cx+ex,cy-25,22,34); brow(d,cx-ex-40,cy-85,cx-ex+40,cy-100,16); brow(d,cx+ex+40,cy-85,cx+ex-40,cy-100,16); d.line((cx-60,cy+55,cx+60,cy+50),fill=K,width=16); faces["determined"]=im
    im,d=canvas(); eye(d,cx-ex,cy-30); d.arc((cx+ex-30,cy-45,cx+ex+30,cy-5),200,340,fill=K,width=16); smile(d,cx,cy+10,120,70); faces["wink"]=im
    for k,v in faces.items(): v.save(OUT+k+".png")
    # monster: white glowing face. hollow tilted eyes (rings, no pupils) + grin too wide with gaps between teeth
    im,d=canvas(); Wt=(255,255,255,255)
    for s in(-1,1):
        e=Image.new("RGBA",(220,140),(0,0,0,0)); ed=ImageDraw.Draw(e); ed.ellipse((10,30,210,110),outline=Wt,width=14)
        e=e.rotate(s*-24,expand=True,resample=Image.BICUBIC); im.alpha_composite(e,(cx+s*115-e.width//2,cy-215-e.height//2+60))
    d=ImageDraw.Draw(im)
    mw=330; d.chord((cx-mw,cy-90,cx+mw,cy+130),0,180,fill=Wt)
    n=13
    for i in range(1,n):  # black gaps between teeth
        x=cx-mw+i*(2*mw/n); d.line((x,cy+60,x,cy+215),fill=(0,0,0,0),width=11)
    im2=Image.new("RGBA",(W,H),(0,0,0,0)); 
    arr=im.load()
    for i in range(1,n):
        x=int(cx-mw+i*(2*mw/n))
        for xx in range(x-8,x+9):
            for yy in range(cy-30,cy+150): 
                if 0<=xx<W and 0<=yy<H: arr[xx,yy]=(0,0,0,0)
    im.save(OUT+"monster.png")
if __name__=="__main__": make(); print(sorted(os.listdir(OUT)))
