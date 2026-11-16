#!/usr/bin/env python3
"""Efekt 9 paketlerinin benzetimi: ORIJINAL | ZEMIN + 3 PAKET | VURUS paketi | KESIK paketi | ALTIN paketi (siyah zemin = oyundaki eklemeli isik).
Cikti: onizlemeler/efekt9_paketler.mp4 / .jpg.  Kullanim: paket_onizle9.py KLASOR"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar9 import KX, KY, KX1, KY1
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt9"); A=os.path.join(B_,"..","..","unity_kaynak","Assets"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),18)
J=json.load(open(os.path.join(K,"paket_olculer.json"))); BIL=json.load(open(os.path.join(K,"bilgi.json")))
fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png"))); Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
PK={"vurus":("OlymposEfekt9Vurus1298",BIL["skill"]["kaynak_kareler"][0]),"kesik":("OlymposEfekt9Kesik1298",BIL["skill"]["kaynak_kareler"][0]),"altin":("OlymposEfekt9Altin1298",BIL["altin"]["kaynak_kareler"][0])}
def parca(ad,i):
    E=np.zeros((1488,2266,3),np.float32); p,i0=PK[ad]; n=i-i0
    if 0<=n<J[ad]["kare"]:
        x,y,w,h=J[ad]["kutu_ekran"]; E[y:y+h,x:x+w]=np.asarray(Image.open(os.path.join(A,p,"Textures",ad,"%s_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
    return E
KIRP=(0,140,1700,1330); Wv=420
def k(X): im=Image.fromarray(np.clip(X,0,255).astype(np.uint8)).crop(KIRP); return im.resize((Wv,int(Wv*im.height/im.width)),Image.LANCZOS)
BOS={"skill":np.zeros((1488,2266,3),np.float32),"altin":np.zeros((1488,2266,3),np.float32)}
for ad in ("skill","altin"): BOS[ad][KY:KY1,KX:KX1]=np.load(os.path.join(K,"zemin_%s.npy"%ad)).astype(np.float32)
d=tempfile.mkdtemp(); t=0; ornek=[]
for bol,ii in (("skill",range(62,96)),("altin",range(15,32))):
    for tek in range(2):
        for i in ii:
            P={a:parca(a,i) for a in PK}; T=P["vurus"]+P["kesik"]+P["altin"]
            sut=[("ORİJİNAL",Y(i)),("ZEMİN + 3 PAKET",BOS[bol]+T),("VURUŞ (mobda)",P["vurus"]),("KESİK (karakter)",P["kesik"]),("ALTIN (karakter)",P["altin"])]
            ims=[k(v) for _,v in sut]; hh=ims[0].height
            c=Image.new("RGB",(5*Wv+40,hh+30),(24,24,28)); dr=ImageDraw.Draw(c)
            for j,(ad,_) in enumerate(sut): c.paste(ims[j],(j*(Wv+10),30)); dr.text((j*(Wv+10)+6,6),ad,font=F,fill=(255,220,120) if j>1 else (200,200,200) if j==0 else (140,230,140))
            c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
            if tek==0 and i in (67,71,77,87,20,24): ornek.append(c)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","20",os.path.join(ONZ,"efekt9_paketler.mp4")],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(q.height+6 for q in ornek)),(24,24,28)); yy=0
for q in ornek: o.paste(q,(0,yy)); yy+=q.height+6
o.save(os.path.join(ONZ,"efekt9_paketler.jpg"),quality=88); print(t,"kare")
