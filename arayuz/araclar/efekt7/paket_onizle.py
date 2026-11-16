#!/usr/bin/env python3
"""Efekt 7 PAKETININ benzetimi: pakette giden dokular (unity_kaynak/.../Textures) + shader matematigi:
  arka katman: eklemeli, mobun silueti orter (derinlik testi) ; on katman: eklemeli
  hasar kirmizisi: Olympos/Efekt7 Hasar Kirmizi = dst * (1 - s + s c) + s b, c=(0.60,0.95,0.75), b=(162,5,0)/255 (kanal basina)
Solda orijinal kayit, sagda paket. Cikti: onizlemeler/efekt7_paket.mp4 / .png"""
import os, sys, json, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from ortak import *
B_=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(B_,"..","..","unity_kaynak","Assets","OlymposEfekt7_1298","Textures")
K7=os.path.join(B_,"..","..","kaynak","efekt7"); ONZ=os.path.join(B_,"..","..","onizlemeler")
BIL=json.load(open(os.path.join(K7,"bilgi.json"))); HM=np.load(os.path.join(K7,"hedef_maskesi.npy"))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),22)
C=np.array([0.60,0.95,0.75]); Bk=np.array([162,5,0.])
AD={"kesik_aura":"kesik_aura (kesik + pembe aura)","yildiz":"yildiz (yıldız vuruşu + kırmızı)"}
MOD=sys.argv[1] if len(sys.argv)>1 else "tam"     # tam | hasar | skill | karakter | vurus
AS=os.path.join(B_,"..","..","unity_kaynak","Assets")
if MOD=="vurus": R=os.path.join(AS,"OlymposEfekt7Hasar1298","Textures")
def paket(ad,Bo,n):
    b=BIL[ad]; s=b["kirmizi_gucu"][n] if MOD in ("tam","hasar") else 0.0
    Rr=np.where(HM[...,None],Bo*(1-s+s*C)+s*Bk,Bo).copy()
    if MOD=="karakter":
        c=BIL["karakter_kesik"]; x,y,w,h=c["kutu_ekran"]
        if n<c["kare"]:
            E=np.asarray(Image.open(os.path.join(AS,"OlymposEfekt7Karakter1298","Textures","karakter_kesik","karakter_kesik_%02d.png"%n)).convert("RGB"),dtype=np.float32)
            Rr[y:y+h,x:x+w]+=E
        return np.clip(Rr,0,255)
    for kat in (("arka","on") if MOD!="hasar" else ()):
        x,y,w,h=b[kat]["kutu_ekran"]
        E=np.asarray(Image.open(os.path.join(R,"%s_%s"%(ad,kat),"%s_%s_%02d.png"%(ad,kat,n))).convert("RGB"),dtype=np.float32)
        if kat=="arka": E=np.where(HM[y:y+h,x:x+w,None],0,E)
        Rr[y:y+h,x:x+w]+=E
    return np.clip(Rr,0,255)
KIRP=(150,226,1750,1060); W=900
def k(A): im=Image.fromarray(A.astype(np.uint8)).crop(KIRP); return im.resize((W,int(W*im.height/im.width)),Image.LANCZOS)
d=tempfile.mkdtemp(); t=0; ornek=[]; fark={}
for ad,(olay,t0,t1) in ((("kesik_aura",("C",0,0)),) if MOD=="karakter" else (("kesik_aura",("C",0,0)),("yildiz",("B",0,0)))):
    Bo=med(TEMIZ); b=BIL[ad]; N=b["kare"]; f=[]
    for tekrar in range(2):
        for n in list(range(N))+[N]*12:
            O=Y(b["kaynak_kareler"][min(n,N-1)]) if n<N else Bo; P=paket(ad,Bo,min(n,N-1)) if n<N else Bo
            if tekrar==0 and n<N: f.append(float(np.abs(P-O)[~ovr_maske()].mean()))
            a=k(O); r=k(P); c=Image.new("RGB",(2*W+10,a.height+40),(24,24,28)); c.paste(a,(0,40)); c.paste(r,(W+10,40)); dr=ImageDraw.Draw(c)
            dr.text((8,8),"ORİJİNAL — "+AD[ad],font=F,fill=(200,200,200)); dr.text((W+18,8),{"tam":"UNITY PAKETİ (dokular + shader hesabı)","hasar":"YALNIZ MOB HASAR RENGİ paketi","skill":"YALNIZ SKILL IŞIKLARI paketi","karakter":"YALNIZ KARAKTER (kılıç kesiği) paketi","vurus":"YALNIZ MOBDAKİ HASAR EFEKTİ paketi"}[MOD],font=F,fill=(140,230,140))
            c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
            if tekrar==0 and n in ((2,4,8,14) if ad=="kesik_aura" else (2,4,5)): ornek.append(c)
    fark[ad]=round(float(np.mean(f)),2)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","19",os.path.join(ONZ,"efekt7_paket%s.mp4"%("" if MOD=="tam" else "_"+MOD))],check=True)
shutil.rmtree(d)
o=Image.new("RGB",(ornek[0].width,sum(x.height+6 for x in ornek)),(24,24,28)); yy=0
for x in ornek: o.paste(x,(0,yy)); yy+=x.height+6
o.save(os.path.join(ONZ,"efekt7_paket%s.png"%("" if MOD=="tam" else "_"+MOD))); print(t,"kare",fark)
