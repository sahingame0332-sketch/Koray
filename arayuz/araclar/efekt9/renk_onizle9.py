#!/usr/bin/env python3
"""Onizleme: ORIJINAL | PEMBE PATLAMA (siyah fon) | SARI PATLAMA + YILDIZ (siyah fon) | SARI KESIK (siyah fon). Gercek hiz + 1/4 hiz.
Cikti: onizlemeler/efekt9_renk.mp4 / .jpg   Kullanim: renk_onizle9.py KLASOR"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt9"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),22)
J=json.load(open(os.path.join(K,"paket_olculer.json"))); fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png")))
Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
def yer(klasor,ad,n,kutu):
    E=np.zeros((1488,2266,3),np.float32); p=os.path.join(K,klasor,"%s_%02d.png"%(ad,n))
    if os.path.exists(p): x,y,w,h=kutu; E[y:y+h,x:x+w]=np.asarray(Image.open(p).convert("RGB"),dtype=np.float32)
    return E
KIRP=(60,170,1560,1140); W=470
def k(X): im=Image.fromarray(np.clip(X,0,255).astype(np.uint8)).crop(KIRP); return im.resize((W,int(W*im.height/im.width)),Image.LANCZOS)
d=tempfile.mkdtemp(); t=0; ornek=[]
for yavas in (1,4):
    for n in range(-3,J["vurus"]["kare"]+6):
        i=66+n; nn=min(max(n,0),J["vurus"]["kare"]-1); var=0<=n<J["vurus"]["kare"]
        col=[("ORİJİNAL",Y(i)),("PEMBE PATLAMA",yer("renk_pembe","pembe",n,J["vurus"]["kutu_ekran"]) if var else np.zeros((1488,2266,3))),
             ("SARI PATLAMA + YILDIZ",yer("renk_sari","sari",n,J["vurus"]["kutu_ekran"]) if var else np.zeros((1488,2266,3))),
             ("SARI KESİK",yer("paket_kesik","kesik",n,J["kesik"]["kutu_ekran"]) if var else np.zeros((1488,2266,3)))]
        ims=[k(v) for _,v in col]; hh=ims[0].height
        c=Image.new("RGB",(4*W+30,hh+64),(20,20,22)); dr=ImageDraw.Draw(c)
        for j,(ad,_) in enumerate(col): c.paste(ims[j],(j*(W+10),34)); dr.text((j*(W+10)+6,6),ad,font=F,fill=(200,200,200) if j==0 else (255,170,220) if j==1 else (255,220,120))
        dr.text((6,hh+38),"kare %d · %.3f sn%s"%(n,n/30.0,"  (1/4 hız)" if yavas>1 else ""),font=F,fill=(180,180,180))
        for _ in range(yavas): c.save(os.path.join(d,"a_%05d.png"%t)); t+=1
        if yavas==1 and n in (2,6,10,14,18,22): ornek.append(c)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%05d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","17",os.path.join(ONZ,"efekt9_renk.mp4")],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(q.height+4 for q in ornek)),(20,20,22)); yy=0
for q in ornek: o.paste(q,(0,yy)); yy+=q.height+4
o.save(os.path.join(ONZ,"efekt9_renk.jpg"),quality=90); print(t)
