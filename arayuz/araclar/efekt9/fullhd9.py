#!/usr/bin/env python3
"""Efekt 9 Full HD (1920x1080) onizleme.
 efekt9_fullhd.mp4            : yalniz paketler (efektsiz zemin + vurus + kesik + altin), oyun alani 16:9, gercek hiz + 1/4 hiz tekrar
 efekt9_fullhd_karsilastirma.mp4 : ust orijinal, alt paket (her biri 1920x540 alanda), kare sayaci; gercek hiz + 1/4 hiz
Kullanim: fullhd9.py KLASOR"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt9"); A=os.path.join(B_,"..","..","unity_kaynak","Assets"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),28)
J=json.load(open(os.path.join(K,"paket_olculer.json"))); BIL=json.load(open(os.path.join(K,"bilgi.json")))
fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png"))); Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
PK={"vurus":("OlymposEfekt9Vurus1298",BIL["skill"]["kaynak_kareler"][0]),"kesik":("OlymposEfekt9Kesik1298",BIL["skill"]["kaynak_kareler"][0]),"altin":("OlymposEfekt9Altin1298",BIL["altin"]["kaynak_kareler"][0])}
def parca(ad,i):
    E=np.zeros((1488,2266,3),np.float32); p,i0=PK[ad]; n=i-i0
    if 0<=n<J[ad]["kare"]:
        x,y,w,h=J[ad]["kutu_ekran"]; E[y:y+h,x:x+w]=np.asarray(Image.open(os.path.join(A,p,"Textures",ad,"%s_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
    return E
from cikar9 import EFEKT
Z={b:np.median(np.stack([Y(i) for i in c["once"]]),0) for b,c in EFEKT.items()}
KIRP=(0,140,2116,1330)                                    # 16:9 oyun alani (2116 x 1190)
def fhd(X,w=1920,h=1080): return Image.fromarray(np.clip(X,0,255).astype(np.uint8)).crop(KIRP).resize((w,h),Image.LANCZOS)
SIRA=[("skill",i) for i in range(58,100)]+[("altin",i) for i in range(12,38)]
d1=tempfile.mkdtemp(); d2=tempfile.mkdtemp(); t=0
for tekrar,yavas in ((0,1),(1,4)):
    for b,i in SIRA:
        P=np.clip(Z[b]+parca("vurus",i)+parca("kesik",i)+parca("altin",i),0,255)
        n_ef=i-EFEKT[b]["aralik"][0]; ad="VURUŞ + KESİK" if b=="skill" else "ALTIN PATLAMA"
        etiket="%s · kare %d · %.3f sn%s"%(ad,n_ef,n_ef/30.0,"  (1/4 hız)" if yavas>1 else "")
        a=fhd(P); dr=ImageDraw.Draw(a); dr.rectangle((0,0,1920,44),fill=(0,0,0)); dr.text((14,6),"UNITY PAKETİ — "+etiket,font=F,fill=(255,220,120))
        c=Image.new("RGB",(1920,1080),(16,16,18)); o=fhd(Y(i),960,540); p=fhd(P,960,540)
        c.paste(o,(0,270)); c.paste(p,(960,270)); dc=ImageDraw.Draw(c)
        dc.text((14,226),"ORİJİNAL",font=F,fill=(220,220,220)); dc.text((974,226),"UNITY PAKETİ (efektsiz zemin + 3 paket)",font=F,fill=(140,230,140))
        dc.text((14,830),etiket,font=F,fill=(255,220,120))
        for _ in range(yavas):
            a.save(os.path.join(d1,"a_%05d.png"%t)); c.save(os.path.join(d2,"a_%05d.png"%t)); t+=1
for d,ad in ((d1,"efekt9_fullhd.mp4"),(d2,"efekt9_fullhd_karsilastirma.mp4")):
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%05d.png","-vf","format=yuv420p","-c:v","libx264","-preset","slow","-crf","16",os.path.join(ONZ,ad)],check=True)
    shutil.rmtree(d)
print(t,"kare")
