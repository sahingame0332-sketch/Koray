#!/usr/bin/env python3
"""Efekt 9 onizleme: ORIJINAL | YENI (efektsiz zemin + efekt) | YALNIZ EFEKT (siyah zemin = oyundaki eklemeli isik).
Cikti: onizlemeler/efekt9_onizleme.png, efekt9_animasyon.mp4.  Kullanim: kur9.py KLASOR"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar9 import OUT, KX, KY, KX1, KY1
B_=os.path.dirname(os.path.abspath(__file__)); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
b=json.load(open(os.path.join(OUT,"bilgi.json"))); fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png")))
Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)[KY:KY1,KX:KX1]
AD={"skill":"SKILL (Gloomwing'e vuruş)","altin":"ALTIN PATLAMA (oyuncuda)"}
KIRP=(0,0,1700,1190); Wv=560
def k(A): im=Image.fromarray(np.clip(A,0,255).astype(np.uint8)).crop(KIRP); return im.resize((Wv,int(Wv*im.height/im.width)),Image.LANCZOS)
d=tempfile.mkdtemp(); t=0; ornek=[]; fark={}
for ad in ("skill","altin"):
    c=b[ad]; Bo=np.load(os.path.join(OUT,"zemin_%s.npy"%ad)).astype(np.float32); x,y,w,h=c["kutu_ekran"]; x-=KX; y-=KY; i0=c["kaynak_kareler"][0]; N=c["kare"]; f=[]
    for tek in range(2):
        for n in list(range(-4,N))+[N]*8:
            E=np.zeros_like(Bo)
            if 0<=n<N: E[y:y+h,x:x+w]=np.asarray(Image.open(os.path.join(OUT,ad,"%s_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
            O=Y(min(max(i0+n,0),len(fs)-1)); R=Bo+E
            if tek==0 and 0<=n<N: f.append(float(np.abs(np.clip(R,0,255)-O).mean()))
            a=k(O); r1=k(R); r2=k(E); hh=a.height
            cc=Image.new("RGB",(3*Wv+20,hh+36),(24,24,28)); cc.paste(a,(0,36)); cc.paste(r1,(Wv+10,36)); cc.paste(r2,(2*Wv+20,36)); dr=ImageDraw.Draw(cc)
            dr.text((6,8),"ORİJİNAL — "+AD[ad],font=F,fill=(200,200,200)); dr.text((Wv+16,8),"YENİ (zemin + efekt)",font=F,fill=(140,230,140)); dr.text((2*Wv+26,8),"YALNIZ EFEKT (siyah zemin)",font=F,fill=(255,220,120))
            cc.save(os.path.join(d,"a_%04d.png"%t)); t+=1
            if tek==0 and n in ((2,5,8,12,18,22) if ad=="skill" else (1,3,5,7)): ornek.append(cc)
    fark[ad]=round(float(np.mean(f)),2)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","19",os.path.join(ONZ,"efekt9_animasyon.mp4")],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(q.height+6 for q in ornek)),(24,24,28)); yy=0
for q in ornek: o.paste(q,(0,yy)); yy+=q.height+6
o.save(os.path.join(ONZ,"efekt9_onizleme.png")); print(t,"kare; ort fark",fark)
