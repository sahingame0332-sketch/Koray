#!/usr/bin/env python3
"""Efekt 8 onizleme: ORIJINAL | YENI (zemin + mob kirmizisi + skill isigi, karsilastirma icin) | YALNIZ SKILL (zemin + skill, kirmizi yok).
Cikti: onizlemeler/efekt8_onizleme.png, efekt8_animasyon.mp4"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar8 import OUT, KX, KY, KX1, KY1, kirmizi
B_=os.path.dirname(os.path.abspath(__file__)); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
b=json.load(open(os.path.join(OUT,"bilgi.json"))); rm=np.load(os.path.join(OUT,"mob_maskesi.npy")); Bo=np.load(os.path.join(OUT,"zemin.npy")).astype(np.float32)
fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png")))
Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)[KY:KY1,KX:KX1]
x,y,w,h=b["kutu_ekran"]; x-=KX; y-=KY; Kr=kirmizi(Bo.mean(2))
# karsilastirma icin mob maskesi: en kirmizi karede (yildizin kirmizisi) kirmiziya donen pikseller, siki
from scipy import ndimage
_O=Y(b["kaynak_kareler"][0]+int(np.argmax(b["kirmizi_gucu"][15:]))+15)
rm=rm&(((_O[...,0]-Bo[...,0])>35)&(_O[...,0]>_O[...,1]+55)); rm=ndimage.binary_closing(rm,np.ones((3,3)))
rm=ndimage.gaussian_filter(rm.astype(np.float32),0.8)>0.5
def yap(n,kirmizi_ile):
    s=b["kirmizi_gucu"][n] if kirmizi_ile else 0.0
    R=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo).copy()
    E=np.asarray(Image.open(os.path.join(OUT,"skill","skill_%02d.png"%n)).convert("RGB"),dtype=np.float32); R[y:y+h,x:x+w]+=E
    return np.clip(R,0,255)
KIRP=(250,150,1450,1000); Wv=560
def k(A): im=Image.fromarray(A.astype(np.uint8)).crop(KIRP); return im.resize((Wv,int(Wv*im.height/im.width)),Image.LANCZOS)
N=b["kare"]; ilk=b["kaynak_kareler"][0]
d=tempfile.mkdtemp(); t=0; ornek=[]; fark=[]
for tek in range(3):
    for n in list(range(-6,N))+[N]*10:
        nn=min(max(n,0),N-1); O=Y(ilk+n) if 0<=n<N else (Y(ilk-6+n+6) if n<0 else Y(ilk+N))
        if 0<=n<N: R1=yap(nn,True); R2=yap(nn,False)
        else: R1=R2=Bo
        if tek==0 and 0<=n<N: fark.append(float(np.abs(R1-O).mean()))
        a=k(O); r1=k(R1); r2=k(R2); hh=a.height
        c=Image.new("RGB",(3*Wv+20,hh+36),(24,24,28)); c.paste(a,(0,36)); c.paste(r1,(Wv+10,36)); c.paste(r2,(2*Wv+20,36)); dr=ImageDraw.Draw(c)
        dr.text((6,8),"ORİJİNAL (gerçek hız)",font=F,fill=(200,200,200)); dr.text((Wv+16,8),"YENİ: zemin + skill (+ mob kırmızısı)",font=F,fill=(140,230,140))
        dr.text((2*Wv+26,8),"YALNIZ SKILL EFEKTİ",font=F,fill=(255,220,120))
        c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
        if tek==0 and n in (2,5,8,12,15,21): ornek.append(c)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","19",os.path.join(ONZ,"efekt8_animasyon.mp4")],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(q.height+6 for q in ornek)),(24,24,28)); yy=0
for q in ornek: o.paste(q,(0,yy)); yy+=q.height+6
o.save(os.path.join(ONZ,"efekt8_onizleme.png")); print(t,"kare, ort fark",round(np.mean(fark),2))
