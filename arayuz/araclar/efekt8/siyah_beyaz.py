#!/usr/bin/env python3
"""Temiz pembe patlama (patlama_rgba, beyaz_fon.py ciktisi) siyah ve beyaz zemin uzerinde yan yana.
Siyah zemin: oyundaki eklemeli gorunusun aynisi (alfa*renk = isik). Beyaz zemin: alfa harmanlama.
Cikti: onizlemeler/efekt8_patlama_siyah_beyaz.png / .mp4"""
import os, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar8 import OUT
B_=os.path.dirname(os.path.abspath(__file__)); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
fs=sorted(glob.glob(os.path.join(OUT,"patlama_rgba","patlama_*.png")))
def zemin(A,z): a=A[...,3:4]/255.0; return np.clip(a*A[...,:3]+(1-a)*z,0,255).astype(np.uint8)
dolu=[]; S=[];B=[]
for i,f in enumerate(fs):
    A=np.asarray(Image.open(f),dtype=np.float32); S.append(Image.fromarray(zemin(A,0))); B.append(Image.fromarray(zemin(A,255)))
    if A[...,3].max()>8: dolu.append(i)
W=280; H=int(W*S[0].height/S[0].width)
c=Image.new("RGB",(2*W*6+10*6,((len(dolu)+5)//6)*(H+26)),(128,128,128)); d=ImageDraw.Draw(c)
for k,i in enumerate(dolu):
    X=(k%6)*(2*W+10); Y=(k//6)*(H+26)
    c.paste(S[i].resize((W,H),Image.LANCZOS),(X,Y+26)); c.paste(B[i].resize((W,H),Image.LANCZOS),(X+W,Y+26))
    d.text((X+6,Y+3),"kare %d (%.2f sn) — siyah | beyaz"%(i,i/30),font=F,fill=(255,255,255))
c.save(os.path.join(ONZ,"efekt8_patlama_siyah_beyaz.png"))
t=tempfile.mkdtemp(); Wv=640; Hv=int(Wv*S[0].height/S[0].width)
for j,i in enumerate(list(range(len(fs)))*3):
    o=Image.new("RGB",(2*Wv,Hv+34),(40,40,40)); o.paste(S[i].resize((Wv,Hv),Image.LANCZOS),(0,34)); o.paste(B[i].resize((Wv,Hv),Image.LANCZOS),(Wv,34))
    dr=ImageDraw.Draw(o); dr.text((8,6),"SİYAH ZEMİN (oyundaki eklemeli görünüş)",font=F,fill=(255,255,255)); dr.text((Wv+8,6),"BEYAZ ZEMİN",font=F,fill=(255,255,255))
    o.save(os.path.join(t,"a_%04d.png"%j))
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",t+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","18",os.path.join(ONZ,"efekt8_patlama_siyah_beyaz.mp4")],check=True)
shutil.rmtree(t); print(dolu)
