#!/usr/bin/env python3
"""Benzetim: ok sprite'i olculen uc yolunda (kare kare uc noktasi + yon) cizilir, sonra vurus kareleri (on-carpimli) bindirilir.
Zemin = oksuz kareler medyani. Orijinal <-> yeni. Cikti: onizlemeler/ok_onizleme.png
Kullanim: kur.py KARE_KLASORU"""
import os, sys, glob, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","ok"); ONZ=os.path.join(B_,"..","..","onizlemeler")
fs=sorted(glob.glob(sys.argv[1]+'/k_*.png')); Y=lambda i: np.asarray(Image.open(fs[i]).convert('RGB')).astype(np.float32)
J=json.load(open(os.path.join(K,"olculer.json"))); V=json.load(open(os.path.join(K,"vurus_olculer.json")))
ok=Image.open(os.path.join(K,"ok.png"))
Bg=np.median(np.stack([Y(i) for i in range(100,124)]),0)                       # zemin (ok her pikselde kisa kalir)
yol={int(k):v for k,v in J["uc_yolu"].items()}
hedef=np.array(J["vurus_ekran"]); cikis=np.array(J["cikis_ekran"])
def ok_ciz(im,uc,yon,uzunluk):
    s=uzunluk/ok.width; sp=ok.resize((max(2,int(ok.width*s)),max(2,int(ok.height*s))),Image.LANCZOS)
    aci=-math.degrees(math.atan2(yon[1],yon[0]))
    r=sp.rotate(aci,resample=Image.BICUBIC,expand=True)
    # sprite'in ucu (sag-orta) dondurulmus goruntude merkez + yon*uzunluk/2
    cx,cy=r.width/2,r.height/2; ux=cx+yon[0]*sp.width/2; uy=cy+yon[1]*sp.width/2
    im.alpha_composite(r,(int(round(uc[0]-ux)),int(round(uc[1]-uy))))
KIRP=(0,150,1500,990); sat=[];fark=[]
# olceklendirme: ok ekran uzunlugu uc noktasinin y'sine gore (kare 97: 160 px @ y 557; uzaklastikca kucuk, ufuk y~60)
def uzun(yy): return 160*(yy-60)/(557-60)
kareler=[97,100,104,109,113,123,126,132,141,150]
for i in kareler:
    O=Y(i); im=Image.fromarray(Bg.astype(np.uint8)).convert("RGBA")
    if i in yol:
        u=np.array(yol[i],float); yon=(hedef-cikis)/np.linalg.norm(hedef-cikis)
        ok_ciz(im,u,yon,uzun(u[1]))
    else:
        j=(i-122)//2
        if 0<=j<V["kare_sayisi"]:
            P=np.asarray(Image.open(os.path.join(K,"vurus","vurus_%02d.png"%j))).astype(np.float32)
            x,y,w,h=V["kutu"]; A=np.asarray(im).astype(np.float32)
            reg=A[y:y+h,x:x+w,:3]; A[y:y+h,x:x+w,:3]=np.clip(reg*(1-P[...,3:]/255)+P[...,:3],0,255); im=Image.fromarray(A.astype(np.uint8))
    N=np.asarray(im.convert("RGB")).astype(np.float32); fark.append(np.abs(N-O)[150:990,0:1500].mean())
    a=Image.fromarray(O.astype(np.uint8)).crop(KIRP).resize((375,210)); b=im.convert("RGB").crop(KIRP).resize((375,210))
    sat.append((i,a,b))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),16)
c=Image.new("RGB",(375*5+40,(210*2+50)*2),(24,24,28)); d=ImageDraw.Draw(c)
for k,(i,a,b) in enumerate(sat):
    X=(k%5)*(375+10); Yy=(k//5)*(210*2+50)
    d.text((X+4,Yy+4),"%.2f sn %s"%((i-94)/60,"(uçuş)" if i in yol else "(vuruş)"),font=F,fill=(255,220,120))
    c.paste(a,(X,Yy+26)); c.paste(b,(X,Yy+26+212))
d.text((4,c.height-22),"üst: ORİJİNAL · alt: YENİ (zemin + ok sprite ölçülen yolda + vuruş kareleri) · ort. fark %.1f/255"%np.mean(fark),font=F,fill=(200,200,200))
c.save(os.path.join(ONZ,"ok_onizleme.png")); print("fark %.2f"%np.mean(fark),c.size)
