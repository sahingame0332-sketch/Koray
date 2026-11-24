"""Degisken yazilarin fontu + puntosu + harf araligi (Roboto Slab Bold / Roboto Bold), orijinal murekle IoU.
Calisma klasoru: item.jpg, item2.jpg, hizli.jpg"""
import numpy as np, json
from PIL import Image, ImageFont, ImageDraw
F={'RobotoSlab-Bold':'/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf',
   'Roboto-Bold':'/home/user/Koray/arayuz/kaynak/char_info/fonts/Roboto-Bold.ttf'}
SAT={'para':('item','5,042,580',(1780,826,1995,868)),'oran':('item2','%100,0',(1795,574,1960,620)),
     'coin':('item2','0',(1300,574,1360,620)),'tire':('item','-',(1300,574,1360,620))}
def murek(m):
    ys,xs=np.nonzero(m); return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(fn,t,p,s):
    f=ImageFont.truetype(F[fn],p); im=Image.new('L',(900,140),0); d=ImageDraw.Draw(im); x=20.0
    for ch in t: d.text((x,30),ch,font=f,fill=255); x+=f.getlength(ch)+s
    return murek(np.asarray(im)>110)
def iou(a,b):
    h=max(a.shape[0],b.shape[0])+4; w=max(a.shape[1],b.shape[1])+4; best=0
    for dy in range(-2,3):
        for dx in range(-3,4):
            A=np.zeros((h+8,w+8),bool); B=np.zeros((h+8,w+8),bool)
            A[4:4+a.shape[0],4:4+a.shape[1]]=a; B[4+dy:4+dy+b.shape[0],4+dx:4+dx+b.shape[1]]=b
            best=max(best,(A&B).sum()/(A|B).sum())
    return best
out={}
for ad,(k,t,(x0,y0,x1,y1)) in SAT.items():
    O=np.asarray(Image.open(k+'.jpg').convert('RGB')).astype(float)[y0:y1,x0:x1]
    m=O.min(2)>150; ys,xs=np.nonzero(m)
    col=np.median(O[m&(O.max(2)>np.percentile(O.max(2)[m],60))],0)
    h=murek(m)
    r=sorted(((iou(h,ciz(fn,t,p,s)),fn,p,float(s)) for fn in F for p in range(18,40) for s in (np.arange(0,3.01,0.5) if len(t)>1 else [0])),reverse=True)[:3]
    out[ad]=dict(metin=t,kutu=[int(x0+xs.min()),int(y0+ys.min()),int(np.ptp(xs)+1),int(np.ptp(ys)+1)],renk='#%02X%02X%02X'%tuple(int(v) for v in col),
                 en_iyi=[(round(v,3),fn,p,s) for v,fn,p,s in r])
    print(ad,out[ad],flush=True)
json.dump(out,open('punto.json','w'),indent=1)
