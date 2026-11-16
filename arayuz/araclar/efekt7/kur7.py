#!/usr/bin/env python3
"""Dogrulama: efekt oncesi zemin + hedef kirmizisi (s) + arka katman + on katman <-> orijinal (ayni oyun zamani).
Ayrica ikinci olay (A / D) ile karsilastirma: ayni efektin tekrari. Cikti: onizlemeler/efekt7_onizleme.png, efekt7_animasyon.mp4"""
import os, sys, json, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from ortak import *
from zaman import benzersiz
from cikar7 import OUT, EFEKT, KX, KY, KX1, KY1
ONZ=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
B_=json.load(open(os.path.join(OUT,"bilgi.json"))); Z=json.load(open("zaman.json")); hm=np.load(os.path.join(OUT,"hedef_maskesi.npy")) if os.path.exists(os.path.join(OUT,"hedef_maskesi.npy")) else np.load("hedef_maskesi.npy")
AD={"kesik_aura":"1. efekt — kesik + pembe aura","yildiz":"2. efekt — yıldız vuruşu + kırmızı"}
TEKRAR={"kesik_aura":"A","yildiz":"D"}
def yeniden(ad,Bo,n):
    b=B_[ad]; s=b["kirmizi_gucu"][n]; L=Bo.mean(2)
    R=np.where(hm[...,None],Bo+s*(kirmizi(L)-Bo),Bo).copy()
    for kat in ("arka","on"):
        x,y,w,h=b[kat]["kutu_ekran"]; E=np.asarray(Image.open(os.path.join(OUT,"%s_%s"%(ad,kat),"%s_%s_%02d.png"%(ad,kat,n))).convert("RGB"),dtype=np.float32)
        if kat=="arka": E=np.where(hm[y:y+h,x:x+w,None],0,E)        # mob arkadaki isigi ortuyor
        R[y:y+h,x:x+w]+=E
    return np.clip(R,0,255)
KIRP=(300,226,1450,1060)
def k(A,w=345): im=Image.fromarray(A.astype(np.uint8)).crop(KIRP); return im.resize((w,int(w*im.height/im.width)),Image.LANCZOS)
satirlar=[]; anim=[]; ozet={}
for ad,(olay,t0,t1) in EFEKT.items():
    b=B_[ad]; E_,o,s=OLAY[olay]; Bo=med(o); N=b["kare"]
    E2,o2,s2=OLAY[TEKRAR[ad]]; u2=benzersiz(list(range(E2[0]-12,E2[-1]+8))); t2=np.array([Z[i] for i in u2])
    # tekrarin baslangici: kirmizi/ isik basladigi an; ilk olayla ayni goreli zaman
    sec=[int(round(j*(N-1)/5)) for j in range(6)]
    w=345; h=int(w*(KIRP[3]-KIRP[1])/(KIRP[2]-KIRP[0]))
    c=Image.new("RGB",(110+6*w,36+2*h),(24,24,28)); d=ImageDraw.Draw(c); hata=[]
    m=~ovr_maske()
    for j,n in enumerate(sec):
        O=Y(b["kaynak_kareler"][n]); R=yeniden(ad,Bo,n); hata.append(np.abs(R-O)[m].mean())
        c.paste(k(O),(108+j*w,34)); c.paste(k(R),(108+j*w,34+h)); d.text((112+j*w,38),"%.2f sn"%(n/30),font=F,fill=(255,255,0))
    ozet[ad]=round(float(np.mean(hata)),2)
    d.text((6,6),"%s — %d kare (30 kare/sn, %.2f sn) · ort. fark %.1f/255"%(AD[ad],N,N/30,ozet[ad]),font=F,fill=(255,220,120))
    d.text((6,34+h//2),"ORİJİNAL",font=F,fill=(200,200,200)); d.text((6,34+h+h//2),"YENİ",font=F,fill=(140,230,140))
    satirlar.append(c); anim.append((ad,Bo,b))
o=Image.new("RGB",(satirlar[0].width,sum(s.height+8 for s in satirlar)),(24,24,28)); yy=0
for s in satirlar: o.paste(s,(0,yy)); yy+=s.height+8
o.save(os.path.join(ONZ,"efekt7_onizleme.png")); print(ozet)
d=tempfile.mkdtemp(); t=0; W=640
for ad,Bo,b in anim:
    for rep in range(2):
        for n in list(range(b["kare"]))+[b["kare"]]*12:
            O=Y(b["kaynak_kareler"][min(n,b["kare"]-1)]) if n<b["kare"] else Bo; R=yeniden(ad,Bo,n) if n<b["kare"] else Bo
            a=k(O,W); r=k(R,W); c=Image.new("RGB",(2*W+10,a.height+34),(24,24,28)); c.paste(a,(0,34)); c.paste(r,(W+10,34)); dr=ImageDraw.Draw(c)
            dr.text((6,6),AD[ad]+" — ORİJİNAL",font=F,fill=(200,200,200)); dr.text((W+16,6),"YENİ (zemin + efekt)",font=F,fill=(140,230,140))
            c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","format=yuv420p","-c:v","libx264","-crf","20",os.path.join(ONZ,"efekt7_animasyon.mp4")],check=True)
shutil.rmtree(d); json.dump(ozet,open(os.path.join(OUT,"fark.json"),"w")); print(t,"kare")
