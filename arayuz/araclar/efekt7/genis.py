#!/usr/bin/env python3
"""Genis aci onizleme: oyun ekraninin tamami (galeri seridi/paneli disinda), ust orijinal, alt yeni (zemin + hedef kirmizisi + iki katman).
Cikti: onizlemeler/efekt7_genis.mp4 ve efekt7_genis.png"""
import os, json, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from ortak import *
import kur7 as K
KIRP=(0,UST,SAG,1220); W=1280
def k(A): im=Image.fromarray(A.astype(np.uint8)).crop(KIRP); return im.resize((W,int(W*im.height/im.width)),Image.LANCZOS)
d=tempfile.mkdtemp(); t=0; kare=[]
for ad,Bo,b in K.anim:
    N=b["kare"]
    for n in list(range(N))+[N]*15:
        O=Y(b["kaynak_kareler"][min(n,N-1)]) if n<N else Bo; R=K.yeniden(ad,Bo,n) if n<N else Bo
        a=k(O); r=k(R); c=Image.new("RGB",(W,2*a.height+70),(24,24,28)); dr=ImageDraw.Draw(c)
        c.paste(a,(0,34)); c.paste(r,(0,a.height+70))
        dr.text((8,6),K.AD[ad]+" — ORİJİNAL",font=K.F,fill=(200,200,200)); dr.text((8,a.height+42),"YENİ (efektsiz zemin + efekt)",font=K.F,fill=(140,230,140))
        c.save(os.path.join(d,"a_%04d.png"%t))
        if n==int(N*0.3): kare.append(c)
        t+=1
ONZ=K.ONZ
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","format=yuv420p","-c:v","libx264","-crf","20",os.path.join(ONZ,"efekt7_genis.mp4")],check=True)
o=Image.new("RGB",(W*2+10,kare[0].height),(24,24,28)); o.paste(kare[0],(0,0)); o.paste(kare[1],(W+10,0)); o.save(os.path.join(ONZ,"efekt7_genis.png"))
shutil.rmtree(d); print(t,"kare")
