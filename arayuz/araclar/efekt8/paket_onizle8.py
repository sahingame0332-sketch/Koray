#!/usr/bin/env python3
"""Efekt 8 PAKETININ benzetimi (pakete giden dokular): ARKA katman mobun silueti tarafindan ortulur (derinlik testi), ON katman eklenir.
Sutunlar: ORIJINAL | PAKET (yalniz skill) | PAKET + OlymposMobHasar1298 (shader formulu: renk*(1-s+s c)+s b).
Cikti: onizlemeler/efekt8_paket.mp4 / .png.  Kullanim: paket_onizle8.py KLASOR"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar8 import OUT, KX, KY, KX1, KY1
B_=os.path.dirname(os.path.abspath(__file__)); ONZ=os.path.join(B_,"..","..","onizlemeler")
T=os.path.join(B_,"..","..","unity_kaynak","Assets","OlymposEfekt8_1298","Textures")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
b=json.load(open(os.path.join(OUT,"bilgi.json"))); rm=np.load(os.path.join(OUT,"mob_maskesi.npy")); Bo=np.load(os.path.join(OUT,"zemin.npy")).astype(np.float32)
fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png")))
Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)[KY:KY1,KX:KX1]
x,y,w,h=b["kutu_ekran"]; x-=KX; y-=KY
C=np.array([0.60,0.95,0.75]); Bk=np.array([162,5,0.])
def paket(n,kirmizi):
    s=b["kirmizi_gucu"][n] if kirmizi else 0.0
    R=np.where(rm[...,None],Bo*(1-s+s*C)+s*Bk,Bo).copy()
    for kat in ("arka","on"):
        E=np.asarray(Image.open(os.path.join(T,"skill_"+kat,"skill_%s_%02d.png"%(kat,n))).convert("RGB"),dtype=np.float32)
        if kat=="arka": E=np.where(rm[y:y+h,x:x+w,None],0,E)
        R[y:y+h,x:x+w]+=E
    return np.clip(R,0,255)
KIRP=(250,150,1450,1000); Wv=560
def k(A): im=Image.fromarray(A.astype(np.uint8)).crop(KIRP); return im.resize((Wv,int(Wv*im.height/im.width)),Image.LANCZOS)
N=b["kare"]; ilk=b["kaynak_kareler"][0]; d=tempfile.mkdtemp(); t=0; ornek=[]; fark=[]
for tek in range(3):
    for n in list(range(-6,N))+[N]*10:
        if 0<=n<N: O=Y(ilk+n); P1=paket(n,False); P2=paket(n,True)
        else: O=Y(ilk+n) if n<0 else Y(ilk+N); P1=P2=Bo
        if tek==0 and 0<=n<N: fark.append(float(np.abs(P2-O).mean()))
        a=k(O); r1=k(P1); r2=k(P2); hh=a.height
        c=Image.new("RGB",(3*Wv+20,hh+36),(24,24,28)); c.paste(a,(0,36)); c.paste(r1,(Wv+10,36)); c.paste(r2,(2*Wv+20,36)); dr=ImageDraw.Draw(c)
        dr.text((6,8),"ORİJİNAL (gerçek hız)",font=F,fill=(200,200,200)); dr.text((Wv+16,8),"EFEKT 8 PAKETİ (yalnız skill)",font=F,fill=(255,220,120))
        dr.text((2*Wv+26,8),"EFEKT 8 + MOB HASAR paketi",font=F,fill=(140,230,140))
        c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
        if tek==0 and n in (2,5,8,12,15,21): ornek.append(c)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","19",os.path.join(ONZ,"efekt8_paket.mp4")],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(q.height+6 for q in ornek)),(24,24,28)); yy=0
for q in ornek: o.paste(q,(0,yy)); yy+=q.height+6
o.save(os.path.join(ONZ,"efekt8_paket.png")); print(t,"kare; paket+hasar <-> orijinal ort fark",round(np.mean(fark),2))
