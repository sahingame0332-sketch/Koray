#!/usr/bin/env python3
"""Ornek haritalar: kontrol (katman agirliklari) ve renk haritasi.
  kontrol_moradon_yol.png : R=doseme G=tugla B=arnavut. Serit genislikleri hud_04'te olculdu
                            (tugla seridi 0.958 birim = 3.5 karakter boyu). Harita 32 karakter boyu genislik.
  kontrol_kum_cim.png     : R=kum G=cim. hud_01'in duzeltilmis gorunusunden: yesillik (G-R) esiklenip yumusatildi.
  renk_haritasi_kum.png   : kum alaninin buyuk olcekli renk dalgasi / ortalama * 0.5  (gri 0.5 = degisiklik yok, x2 carpilir)."""
import os, numpy as np
from PIL import Image
from scipy import ndimage
from zemin import *
D=os.path.join(OUT,"dokular")
def moradon():
    W=128; a=np.zeros((8,W,3),np.uint8); pb=W/32.0
    x1=int(round(14.25*pb)); x2=int(round(17.75*pb))
    a[:,:x1,0]=255; a[:,x1:x2,1]=255; a[:,x2:,2]=255
    Image.fromarray(a).save(os.path.join(D,"kontrol_moradon_yol.png"))
def kum_cim():
    img=yukle(os.path.join(REF,"hud_ekranlar/hud_01.png"))
    a,m,k=duz_alan(img,232,(0,470,2266,905),[(1020,630,1250,870),(1160,640,1560,840),(0,470,330,700),(1560,760,2266,905),(1900,470,2266,905)],64)
    # sigan en buyuk kare
    lo,hi=8,min(m.shape)
    while lo<hi:
        mid=(lo+hi+1)//2
        if en_iyi_pencere(m,mid) is not None: lo=mid
        else: hi=mid-1
    x,y=en_iyi_pencere(m,lo); P=a[y:y+lo,x:x+lo]
    yes=ndimage.gaussian_filter(P[:,:,1]-P[:,:,0],3)            # cim: G>R ; kum: R>G
    w=np.clip((yes+25)/30.0,0,1); w=ndimage.gaussian_filter(w,2)
    c=np.zeros((lo,lo,3)); c[:,:,0]=(1-w)*255; c[:,:,1]=w*255
    Image.fromarray(c.astype(np.uint8)).resize((128,128),Image.BILINEAR).save(os.path.join(D,"kontrol_kum_cim.png"))
    Image.fromarray(np.clip(P,0,255).astype(np.uint8)).save(os.path.join(OUT,"duz_kum_cim_kare.png"))
    return dict(kenar_birim=round(lo/64.0,2),kenar_karakter_boyu=round(lo/64.0/KARAKTER["kum"],1),cim_orani=round(float(w.mean()),3))
def renk_haritasi():
    img=yukle(os.path.join(REF,"hud_ekranlar/hud_01.png"))
    a,m,k=duz_alan(img,232,(0,560,1560,912),[(1020,630,1250,870),(1160,640,1560,840),(0,560,300,700)],64)
    lo,hi=8,min(m.shape)
    while lo<hi:
        mid=(lo+hi+1)//2
        if en_iyi_pencere(m,mid) is not None: lo=mid
        else: hi=mid-1
    x,y=en_iyi_pencere(m,lo); P=a[y:y+lo,x:x+lo]
    alc=ndimage.gaussian_filter(P,[lo/10.0,lo/10.0,0],mode="reflect"); ort=P.reshape(-1,3).mean(0)
    h=np.clip(alc/ort*127.5,0,255)
    Image.fromarray(h.astype(np.uint8)).resize((64,64),Image.BILINEAR).save(os.path.join(D,"renk_haritasi_kum.png"))
    oran=alc/ort
    return dict(kenar_birim=round(lo/64.0,2),kenar_karakter_boyu=round(lo/64.0/KARAKTER["kum"],1),
                en_koyu=round(float(oran.mean(2).min()),3),en_acik=round(float(oran.mean(2).max()),3),std=round(float(oran.mean(2).std()),3))
if __name__=="__main__":
    moradon(); k=kum_cim(); r=renk_haritasi(); print("kum/cim kontrol:",k); print("renk haritasi:",r)
    import json
    p=os.path.join(OUT,"zemin_olcumleri.json"); j=json.load(open(p)); j["_haritalar"]=dict(kontrol_kum_cim=k,renk_haritasi_kum=r,
        kontrol_moradon_yol=dict(genislik_karakter_boyu=32,doseme=[0,14.25],tugla=[14.25,17.75],arnavut=[17.75,32],not_="tugla seridi 3.5 karakter boyu olculdu; digerleri ekran disina tasiyor"))
    json.dump(j,open(p,"w"),indent=1,ensure_ascii=False)
