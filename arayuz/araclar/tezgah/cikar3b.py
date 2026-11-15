#!/usr/bin/env python3
"""3B tezgah icin yuz dokulari: iki fotograftaki yuzler homografi ile duz dikdortgene acilir.
Geometri (fotograflardan): alcak sandik + ustte one egik teshir tahtasi (arkasi yuksek).
  ON fotograf: ust tahta (sancak + esyalar) ve on yuz (asili sancak, mavi ortu).  YAN fotograf: sol yan yuz (kirmizi perde, mavi ortu).
Kose noktalari elle olculdu (izgara: arayuz/16-tezgah.md ek 2). Arka yuz fotografta yok -> yan yuzun dokusu kullanilir.
Cikti: kaynak/tezgah/3b/{ust,on,yan}.png"""
import os, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(B_,"..","..","referans_gorseller","tezgah")
OUT=os.path.join(B_,"..","..","kaynak","tezgah","3b"); os.makedirs(OUT,exist_ok=True)
def homografi(src,dst):
    A=[];b=[]
    for (x,y),(u,v) in zip(src,dst):
        A+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; b+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(b,float))
def ac(dosya,koseler,w,h):
    """koseler: sol-ust, sag-ust, sag-alt, sol-alt (fotograf pikseli) -> w x h duz doku"""
    im=Image.open(os.path.join(R,dosya)).convert("RGB")
    hedef=[(0,0),(w,0),(w,h),(0,h)]
    c=homografi(hedef,koseler)            # PIL: cikis -> giris
    return im.transform((w,h),Image.PERSPECTIVE,tuple(c),Image.BICUBIC)
YUZ={"ust":("tezgah.jpg",[(1560,701),(1748,728),(1757,849),(1545,845)],512,374),
     "on": ("tezgah.jpg",[(1545,846),(1757,860),(1735,1033),(1531,986)],512,387),
     "yan":("tezgah_yan.jpg",[(1141,551),(1244,531),(1262,655),(1179,697)],330,512)}
for ad,(d,k,w,h) in YUZ.items():
    ac(d,k,w,h).save(os.path.join(OUT,ad+".png")); print(ad,w,h)
