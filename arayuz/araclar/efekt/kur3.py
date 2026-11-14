#!/usr/bin/env python3
"""Ates havuzu dogrulamasi: efekt sonrasi zemin (B) + eklemeli kare  <->  ayni anin orijinali; ucuncu satir efektin kendisi.
Kullanim: kur3.py VIDEO -> onizlemeler/efekt3_onizleme.png"""
import os, sys, json, glob, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar3 import KUTU, ARALIK, ONCE
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
x,y,w,h=KUTU
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["ffmpeg","-v","error","-y","-i",sys.argv[1],"-vf","fps=30,crop=%d:%d:%d:%d"%(w,h,x,y),d+"/k_%04d.png"],check=True)
    fs=sorted(glob.glob(d+"/k_*.png")); Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB")).astype(float)
    B=np.median(np.stack([Y(i) for i in ONCE]),0)
    sec=[0,5,10,15,20,26,32,37]; olc=0.5; sat=[[],[],[]]; hata=[]
    for n in sec:
        O=Y(ARALIK[0]+n); E=np.asarray(Image.open(os.path.join(K,"ates_havuzu","ates_havuzu_%02d.png"%n))).astype(float)
        R=np.clip(B+E,0,255); hata.append(np.abs(R-O).mean())
        for j,A in enumerate((O,R,E)): sat[j].append(Image.fromarray(A.astype(np.uint8)).resize((int(w*olc),int(h*olc))))
ww,hh=sat[0][0].size
c=Image.new("RGB",(ww*len(sec)+110,hh*3+40),(24,24,28)); dr=ImageDraw.Draw(c)
dr.text((8,6),"Karakter alti ates havuzu — 39 kare, 30 kare/sn · ort. fark (orijinal <-> zemin+efekt) %.1f / 255"%np.mean(hata),font=F,fill=(255,220,120))
for k,(et,rk) in enumerate((("ORIJINAL",(200,200,200)),("YENI",(140,230,140)),("EFEKT",(255,170,90)))):
    dr.text((6,34+hh*k+hh//2),et,font=F,fill=rk)
    for i,im in enumerate(sat[k]): c.paste(im,(105+i*ww,34+hh*k))
for i,n in enumerate(sec): dr.text((108+i*ww,36),"%.2f sn"%(n/30),font=F,fill=(255,255,0))
c.save(os.path.join(ONZ,"efekt3_onizleme.png")); print("fark %.2f"%np.mean(hata),c.size)
