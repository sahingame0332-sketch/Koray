#!/usr/bin/env python3
"""Genie yazilarinin fontu + puntosu (oyun_ici/punto.py yontemi: murek maskesi IoU)."""
import os, sys, numpy as np
from PIL import Image
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","oyun_ici"))
import punto as P
from ortak import REF
def renk(ad,kutu,esik):
    a=np.asarray(Image.open(os.path.join(REF,ad+".jpg")).convert("RGB")).astype(float)[kutu[1]:kutu[3],kutu[0]:kutu[2]]
    l=a.mean(2); m=l>np.percentile(l,esik); return np.median(a[m],0)
P.REF=REF
OLC=[("sure","Time Left : 244 Minute(s)","g_once",(2356,129,2650,150),97),
     ("sunucu","Ares - 1","g_once",(2440,155,2580,184),94),
     ("cr","CR : 01:18:08","g_once",(2380,198,2560,232),93),
     ("kanal","Channel 2","g_once",(2380,250,2560,284),93),
     ("deger40","40","g_pencere",(795,752,850,790),92),
     ("deger70","%70","g_pencere",(790,830,850,868),92)]
for ad,metin,kare,kutu,e in OLC:
    c=renk(kare,kutu,e); print(ad,"renk #%02X%02X%02X"%tuple(int(v) for v in c))
    P.olc(ad,metin,kare,kutu,tuple(c),tol=55)
