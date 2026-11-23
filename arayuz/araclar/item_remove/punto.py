#!/usr/bin/env python3
"""Item Remove: yazilarin fontu + puntosu + harf araligi (Roboto Slab Bold / Roboto Bold adaylari), orijinal murekle IoU.
Kullanim: punto.py EKRAN.jpg"""
import sys, numpy as np, json
from PIL import Image, ImageFont, ImageDraw
F={'RobotoSlab-Bold':'/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf',
   'Roboto-Bold':'/home/user/Koray/arayuz/kaynak/char_info/fonts/Roboto-Bold.ttf'}
I=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
X0,Y0=1050,455
SAT={'baslik':("Item Remove",(220,36,470,68),'sari'),
     'soru':("Do You want remove this Item?",(122,84,615,116),'beyaz'),
     'esya':("Wood Staff(+7)",(250,118,480,152),'beyaz'),
     'adet':("Count:1",(305,154,425,188),'beyaz'),
     'ok':("OK",(250,330,300,362),'beyaz'),
     'cancel':("Cancel",(410,330,510,362),'beyaz')}
def murek(m):
    ys,xs=np.nonzero(m); return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(fn,t,p,s):
    f=ImageFont.truetype(F[fn],p); im=Image.new('L',(1200,140),0); d=ImageDraw.Draw(im); x=20.0
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
for ad,(t,(x0,y0,x1,y1),renk) in SAT.items():
    O=I[Y0+y0:Y0+y1,X0+x0:X0+x1]; R,G,B=O[...,0],O[...,1],O[...,2]
    m=(R>140)&(G>140)&(B<110) if renk=='sari' else (O.min(2)>150)
    h=murek(m); ys,xs=np.nonzero(m)
    col=np.median(O[m& (O.max(2)>np.percentile(O.max(2)[m],60))],0)
    r=sorted(((iou(h,ciz(fn,t,p,s)),fn,p,s) for fn in F for p in range(18,34) for s in np.arange(0,3.01,0.5)),reverse=True)[:3]
    out[ad]=dict(metin=t,kutu=[int(X0+x0+xs.min()),int(Y0+y0+ys.min()),int(xs.ptp()+1) if hasattr(xs,'ptp') else int(np.ptp(xs)+1),int(np.ptp(ys)+1)],
                 renk='#%02X%02X%02X'%tuple(int(v) for v in col),en_iyi=[(round(v,3),fn,p,float(s)) for v,fn,p,s in r])
    print(ad,out[ad],flush=True)
json.dump(out,open('punto.json','w'),indent=1)
# ortak: dort satir ayni font/punto/aralik varsayimiyla toplam IoU
ort={}
for p in range(25,31):
    for s in np.arange(1,3.01,0.5):
        v=[]
        for ad in ('baslik','soru','esya','adet'):
            t,(x0,y0,x1,y1),renk=SAT[ad]; O=I[Y0+y0:Y0+y1,X0+x0:X0+x1]; R,G,B=O[...,0],O[...,1],O[...,2]
            m=(R>140)&(G>140)&(B<110) if renk=='sari' else (O.min(2)>150)
            v.append(iou(murek(m),ciz('RobotoSlab-Bold',t,p,s)))
        ort[(p,s)]=v
for k,v in sorted(ort.items(),key=lambda kv:-np.mean(kv[1]))[:5]: print('ortak',k,np.round(v,3),round(np.mean(v),3))
