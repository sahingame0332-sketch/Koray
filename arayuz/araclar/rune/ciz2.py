#!/usr/bin/env python3
"""Ikinci ozgun run dairesi — neon (mor/mavi/yesil) tur. Stok gorsel KOPYALANMADI; ayni turde kendi tasarim.
Runler: gercek eski Futhark alfabesi (kamu malı yazı sistemi), cizgi olarak cizildi.
Doku duzeni ciz.py ile ayni: R dis cizgi, G ic cizgi, B dis isilti, A ic isilti.  Cikti: kaynak/rune/rune2_cizgi.png"""
import os, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFilter
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","rune")
N=1024; S=4; M=N*S; C=M/2; random.seed(24)
def yeni(): return Image.new("L",(M,M),0)
def daire(d,r,w,c=(C,C),dolu=False): d.ellipse((c[0]-r,c[1]-r,c[0]+r,c[1]+r),outline=255,width=int(w),fill=0 if dolu else None)
def kutup(r,a,c=(C,C)): return (c[0]+r*math.cos(a),c[1]+r*math.sin(a))
# eski Futhark (x 0..2, y 0..4; cizgi zincirleri)
F={"f":[[(0,4),(0,0)],[(0,1.2),(2,0)],[(0,2.3),(2,1.1)]],"u":[[(0,4),(0,0),(2,1),(2,4)]],
   "th":[[(0,0),(0,4)],[(0,1),(1.6,2),(0,3)]],"a":[[(0,4),(0,0)],[(0,0),(2,1)],[(0,1.1),(2,2.1)]],
   "r":[[(0,4),(0,0),(1.6,1),(0,2),(1.6,4)]],"k":[[(2,0),(0,2),(2,4)]],"g":[[(0,0),(2,4)],[(2,0),(0,4)]],
   "w":[[(0,4),(0,0),(1.6,1),(0,2)]],"h":[[(0,0),(0,4)],[(2,0),(2,4)],[(0,1.2),(2,2.8)]],"n":[[(1,0),(1,4)],[(0,1.4),(2,2.6)]],
   "i":[[(1,0),(1,4)]],"j":[[(1,0.6),(0,2),(1,3.4)],[(1.2,0.6),(2,2),(1.2,3.4)]],"ei":[[(1,0),(1,4)],[(1,0),(2,0.9)],[(1,4),(0,3.1)]],
   "p":[[(0,4),(0,0),(1.6,1)],[(0,4),(1.6,3)]],"z":[[(1,0),(1,4)],[(0,0),(1,1.6),(2,0)]],"s":[[(1.4,0),(0,1.4),(2,2.6),(0.6,4)]],
   "t":[[(1,0),(1,4)],[(0,1),(1,0),(2,1)]],"b":[[(0,4),(0,0),(1.6,1),(0,2),(1.6,3),(0,4)]],"e":[[(0,4),(0,0),(1,1.4),(2,0),(2,4)]],
   "m":[[(0,4),(0,0),(2,1.8)],[(2,4),(2,0),(0,1.8)]],"l":[[(0,4),(0,0),(1.6,1.1)]],"ng":[[(1,0.6),(2,2),(1,3.4),(0,2),(1,0.6)]],
   "d":[[(0,0),(0,4),(2,0),(2,4),(0,0)]],"o":[[(0,4),(1.8,1.6),(1,0.4),(0.2,1.6),(2,4)]]}
HARF=list(F)
def run(d,merkez,aci,boy,w,ad):
    sx=boy/4*0.75; sy=boy/4; ca,sa=math.cos(aci),math.sin(aci)
    def t(p): x=(p[0]-1)*sx; y=(p[1]-2)*sy; return (merkez[0]+x*ca-y*sa, merkez[1]+x*sa+y*ca)
    for z in F[ad]: d.line([t(p) for p in z],fill=255,width=int(w),joint="curve")
def bant(d,r,boy,w,adim,ofset=0,atla=()):
    n=int(2*math.pi*r/adim)
    for i in range(n):
        a=2*math.pi*i/n+ofset
        if any(abs((a-b+math.pi)%(2*math.pi)-math.pi)<g for b,g in atla): continue
        run(d,kutup(r,a),a+math.pi/2,boy,w,random.choice(HARF))
W=S*3.0
dis=yeni(); d=ImageDraw.Draw(dis)
R0=M*0.47
MED=[(-math.pi/2+i*math.pi/3) for i in range(6)]; MR=S*62; RM=R0-S*58
daire(d,R0,W*1.4); daire(d,R0-S*116,W*1.2)
bant(d,RM,S*58,W*1.5,S*50,0.0,[(a,0.24) for a in MED])          # kalin run bandi, madalyonlarda bosluk
daire(d,R0+S*14,W*0.6)
for i,a in enumerate(MED):                                       # 6 madalyon: cift cember + buyuk run + ince run halkasi
    c=kutup(RM,a); daire(d,MR,W*1.2,c,dolu=True); daire(d,MR-S*12,W*0.6,c)
    n=14
    for k in range(n):
        b=2*math.pi*k/n; run(d,kutup(MR-S*6,b,c),b+math.pi/2,S*9,W*0.45,random.choice(HARF))
    run(d,c,0,S*58,W*1.7,["m","ng","d","z","o","g"][i])
    for s in (-1,1):                                             # madalyonun iki yaninda kucuk isaret
        cc=kutup(R0+S*34,a+s*0.13); daire(d,S*6,W*0.6,cc)
for i in range(6):                                               # madalyon arasi dis isaretler
    a=-math.pi/2+math.pi/6+i*math.pi/3; p=kutup(R0+S*30,a); q=kutup(R0+S*58,a); d.line([p,q],fill=255,width=int(W*0.8)); daire(d,S*7,W*0.6,q)
ic=yeni(); d=ImageDraw.Draw(ic)
R1=R0-S*150
daire(d,R1,W*0.8)
bant(d,R1-S*16,S*18,W*0.6,S*20,0.1)                               # ince run cemberi
daire(d,R1-S*32,W*0.8)
R2=R1-S*32
for k in range(2):                                               # heksagram
    p=[kutup(R2,-math.pi/2+k*math.pi/3+i*2*math.pi/3) for i in range(3)]; d.polygon(p,outline=255,width=int(W*0.8))
for i in range(4):                                               # 4 kollu pusula yildizi (uzun)
    a=i*math.pi/2; d.polygon([kutup(R1+S*40,a),kutup(R2*0.42,a+math.pi/4),kutup(R2*0.36,a),kutup(R2*0.42,a-math.pi/4)],outline=255,width=int(W*0.7))
for i in range(6):                                               # rozet: 6 doner elips
    a=i*math.pi/6
    pts=[(C+R2*0.62*math.cos(t)*math.cos(a)-R2*0.30*math.sin(t)*math.sin(a), C+R2*0.62*math.cos(t)*math.sin(a)+R2*0.30*math.sin(t)*math.cos(a)) for t in np.linspace(0,2*math.pi,180)]
    d.line(pts+[pts[0]],fill=255,width=int(W*0.55))
daire(d,R2*0.36,W*1.0); daire(d,R2*0.30,W*0.6)
for i in range(6):                                               # ic cember uzerinde kucuk runlu daireler
    c=kutup(R2*0.80,-math.pi/2+i*math.pi/3+math.pi/6); daire(d,S*14,W*0.6,c,dolu=True); run(d,c,0,S*14,W*0.5,random.choice(HARF))
def kucult(im): return im.resize((N,N),Image.LANCZOS)
D=kucult(dis); I=kucult(ic)
def isilti(im):
    a=np.asarray(im.filter(ImageFilter.GaussianBlur(6))).astype(float)*0.6+np.asarray(im.filter(ImageFilter.GaussianBlur(18))).astype(float)*1.4
    return Image.fromarray(np.clip(a*1.6,0,255).astype(np.uint8))
Image.merge("RGBA",(D,I,isilti(D),isilti(I))).save(os.path.join(OUT,"rune2_cizgi.png")); print("tamam")
