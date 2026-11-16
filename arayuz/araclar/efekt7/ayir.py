#!/usr/bin/env python3
"""Efekt 7 skill isiklarini ikiye ayirir (kareler degismez, yeni klasorler):
  KARAKTER: kilicin sari kesik yayi — oyuncunun onunde (yakin kayitta x >= 950), dikey uzun sari parca (> 150 px).
  HASAR (mobda): kalan her sey — arka katmanda pembe aura, kivilcimlar, yatay parlama; on katman (mob silueti) aynen; yildiz tamamen.
Cikti: kaynak/efekt7/karakter_kesik/ (kirpilmis), <efekt>_arka_hasar/ ; olcu json'a."""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
K7=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt7")
B=json.load(open(os.path.join(K7,"bilgi.json")))
OYUNCU_AYAK=(1300,1170); OYUNCU_BOY=620     # yakin kayit: oyuncu (ekrandan tahmin: bas ~590, ayak alt cubuk altinda)
def yay_maskesi(E,x0):
    R,G,Bb=E[...,0],E[...,1],E[...,2]
    sari=((np.minimum(R,G)-Bb)>(Bb-G))&(E.max(2)>25)
    s=sari.copy(); s[:,:max(0,950-x0)]=False
    l,n=ndimage.label(ndimage.binary_closing(s,np.ones((7,7))))
    m=np.zeros_like(s)
    for i,sl in enumerate(ndimage.find_objects(l)):
        if sl[0].stop-sl[0].start>150: m|=(l==i+1)
    m=ndimage.binary_dilation(m,np.ones((9,9)))&(E.max(2)>3)
    return ndimage.gaussian_filter(m.astype(np.float32),1.5)
def calis():
    ad="kesik_aura"; x0,y0,w,h=B[ad]["arka"]["kutu_ekran"]
    od=os.path.join(K7,"%s_arka_hasar"%ad); os.makedirs(od,exist_ok=True)
    K=[]
    for n in range(B[ad]["kare"]):
        E=np.asarray(Image.open(os.path.join(K7,"%s_arka"%ad,"%s_arka_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
        m=yay_maskesi(E,x0)[...,None]
        Image.fromarray(np.clip(E*(1-m),0,255).round().astype(np.uint8)).save(os.path.join(od,"%s_arka_hasar_%02d.png"%(ad,n)))
        K.append(E*m)
    K=np.stack(K); mx=K.max(3).max(0); ys,xs=np.nonzero(mx>6)
    a,b,c,d=max(0,xs.min()-6),max(0,ys.min()-6),min(w,xs.max()+7),min(h,ys.max()+7)
    son=max(i for i in range(len(K)) if K[i].max()>20)+1
    kd=os.path.join(K7,"karakter_kesik"); os.makedirs(kd,exist_ok=True)
    for f in os.listdir(kd): os.remove(os.path.join(kd,f))
    for n in range(son): Image.fromarray(np.clip(K[n][b:d,a:c],0,255).round().astype(np.uint8)).save(os.path.join(kd,"karakter_kesik_%02d.png"%n))
    X,Yy,W,H=x0+a,y0+b,c-a,d-b
    B["karakter_kesik"]=dict(kutu_ekran=[int(X),int(Yy),int(W),int(H)],kare=son,fps=30.0,oyuncu_ayak=OYUNCU_AYAK,oyuncu_boyu_px=OYUNCU_BOY,
        genislik_oyuncu_boyu=round(W/OYUNCU_BOY,4),en_boy=round(H/W,4),pivot=[round((OYUNCU_AYAK[0]-X)/W,4),round(1-(OYUNCU_AYAK[1]-Yy)/H,4)],
        not_="oyuncu boyu ve ayagi tahmin (ayak alt cubuk altinda kaliyor); kayitta hedef oyuncunun SOLUNDA")
    B[ad]["arka_hasar"]=B[ad]["arka"]
    json.dump(B,open(os.path.join(K7,"bilgi.json"),"w"),indent=1)
    print("karakter_kesik",B["karakter_kesik"])
if __name__=="__main__": calis()
