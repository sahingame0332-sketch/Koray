#!/usr/bin/env python3
"""Efekt 8 pembe aura: kare kare kucuk delikler (cit cubugu izleri, cim dokusu, sikistirma gurultusu) pürüzsüz doldurulur.
Yalniz pembe-mor-gokkusagi bolgesi (B >= G olan isik) islenir; sari kivilcimlar/kesikler/yildiz (R,G >> B) aynen kalir.
  1) gri kapanis 9x9 (her kanal): ince karanlik delikleri komsu isikla doldurur
  2) medyan 5x5: tek piksellik noktalar
  3) gauss sigma 2.2: kumlanmayi giderir, renk gecisi yumusar
Renk: dolgu yeni renk uydurmaz — her piksel komsu gercek renklerden (kapanis = yerel en parlak, medyan = yerel ortanca).
Ham kareler kaynak/efekt8/skill_<kat>_ham/ altinda saklanir."""
import os, sys, json, shutil, numpy as np
from PIL import Image
from scipy import ndimage
from cikar8 import OUT
def puruzsuz(E):
    """aura bolgesinde: kapanis 17x17 (kalin cit cubuklari dahil delikler) -> medyan 7 -> gauss 3;
    keskin sari parcalar (kivilcim, kesik, yatay parlama cizgisi: yerel ortalamadan cok parlak ve sari) orijinal kalir."""
    mx=E.max(2)
    aura=ndimage.gaussian_filter((mx>10).astype(np.float32),12)                    # genis isik bolgesi
    aura=np.clip((aura-0.25)/0.35,0,1)
    C=np.stack([ndimage.grey_closing(E[...,c],size=(17,17)) for c in range(3)],-1)
    C=np.stack([ndimage.median_filter(C[...,c],size=7) for c in range(3)],-1)
    S=ndimage.gaussian_filter(C,[3,3,0])
    yerel=ndimage.gaussian_filter(mx,6)
    sari=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx,1)
    keskin=((mx-yerel)>22)&(sari>0.2)
    keskin=ndimage.gaussian_filter(ndimage.binary_dilation(keskin,np.ones((3,3))).astype(np.float32),1.0)
    w=(aura*(1-keskin))[...,None]
    out=w*S+(1-w)*np.maximum(E,S*aura[...,None]*0)      # keskin bolgede orijinal
    out=np.where(keskin[...,None]>0.5,np.maximum(E,S),out)
    return np.clip(out,0,255), w[...,0]
if __name__=="__main__":
    b=json.load(open(os.path.join(OUT,"bilgi.json")))
    for kat in ("arka","on"):
        src=os.path.join(OUT,"skill_"+kat); ham=os.path.join(OUT,"skill_%s_ham"%kat)
        if not os.path.isdir(ham): shutil.copytree(src,ham)
        for n in range(b["kare"]):
            E=np.asarray(Image.open(os.path.join(ham,"skill_%s_%02d.png"%(kat,n))).convert("RGB"),dtype=np.float32)
            P,_=puruzsuz(E); Image.fromarray(P.round().astype(np.uint8)).save(os.path.join(src,"skill_%s_%02d.png"%(kat,n)))
    print("tamam")
