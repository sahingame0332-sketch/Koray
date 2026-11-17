#!/usr/bin/env python3
"""Efekt 9 paketlerini kare kare denetler: R = zemin + vurus + kesik + altin (paket dokulari) <-> O (orijinal).
Yalniz efekt bolgesinde (|O - zemin| > 12 ya da paket isigi > 12) olculur. Cikti: kare basina ort/95.yuzdelik hata, eksik isik (O>R) ve
fazla isik (R>O) piksel orani; en kotu kareler icin goruntu (orijinal | paket | hata haritasi: kirmizi = eksik, mavi = fazla).
Kullanim: denetle9.py KLASOR [cikti.png]"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt9"); A=os.path.join(B_,"..","..","unity_kaynak","Assets")
J=json.load(open(os.path.join(K,"paket_olculer.json"))); BIL=json.load(open(os.path.join(K,"bilgi.json")))
fs=sorted(glob.glob(os.path.join(sys.argv[1],"k_*.png"))); Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
PK={"vurus":("OlymposEfekt9Vurus1298",BIL["skill"]["kaynak_kareler"][0]),"kesik":("OlymposEfekt9Kesik1298",BIL["skill"]["kaynak_kareler"][0]),"altin":("OlymposEfekt9Altin1298",BIL["altin"]["kaynak_kareler"][0])}
def parca(ad,i):
    E=np.zeros((1488,2266,3),np.float32); p,i0=PK[ad]; n=i-i0
    if 0<=n<J[ad]["kare"]:
        x,y,w,h=J[ad]["kutu_ekran"]; E[y:y+h,x:x+w]=np.asarray(Image.open(os.path.join(A,p,"Textures",ad,"%s_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
    return E
from cikar9 import EFEKT
Z={}
S={}
for b,c in EFEKT.items(): Z[b]=np.median(np.stack([Y(i) for i in c["once"]]),0); S[b]=np.median(np.stack([Y(i) for i in c["sonra"]]),0)
HUD=np.zeros((1488,2266),bool); HUD[:150]=True; HUD[:245,:420]=True; HUD[:,1700:]=True; HUD[1330:]=True
sonuc=[]; kotu=[]
for b,ii in (("skill",range(66,92)),("altin",range(19,29))):
    for i in ii:
        O=Y(i); T=parca("vurus",i)+parca("kesik",i)+parca("altin",i)
        R1=np.clip(Z[b]+T,0,255); R2=np.clip(S[b]+T,0,255)                 # mob/oyuncu hareket ediyor: her pikselde uyan zemin
        R=np.where((np.abs(O-R1).sum(2)<=np.abs(O-R2).sum(2))[...,None],R1,R2)
        isik=np.minimum(O-Z[b],O-S[b]).max(2)>12                       # orijinalde gercekten eklenmis isik (iki zemine gore de)
        govde=(O[...,2]>=0.85*O[...,1])&(np.abs(O[...,0]-O[...,1])<25)&(O.max(2)<235)          # hareket eden mob/oyuncu (efekt degil)
        govde=ndimage.binary_dilation(govde&(np.minimum(O-Z[b],O-S[b]).max(2)>12),np.ones((5,5)))
        ef=(isik|(T.max(2)>12))&~HUD&~govde
        d=(O-R)[ef]; a=np.abs(d).max(1)
        eksik=float(((O-R).max(2)>30)[ef].mean()); fazla=float(((R-O).max(2)>30)[ef].mean())
        sonuc.append((b,i,round(float(a.mean()),1),round(float(np.percentile(a,95)),1),round(eksik*100,1),round(fazla*100,1)))
        kotu.append((float(a.mean()),i,b,O,R,ef))
for s in sonuc: print(s)
if len(sys.argv)>2:
    kotu.sort(key=lambda x:-x[0]); r=[]
    for _,i,b,O,R,ef in kotu[:6]:
        H=np.zeros_like(O); D=O-R; H[...,0]=np.clip(D.max(2)*3,0,255); H[...,2]=np.clip((-D).max(2)*3,0,255); H[~ef]*=0.3
        c=lambda X: X[140:1330,0:1700]
        r.append(np.concatenate([c(O),c(R),c(H)],1).astype(np.uint8)[::3,::3])
    Image.fromarray(np.concatenate(r,0)).save(sys.argv[2])
