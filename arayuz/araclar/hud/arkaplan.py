#!/usr/bin/env python3
"""Onizleme icin HUD'sız bir oyun sahnesi: HUD dikdortgenleri komsu dunyadan doldurulur."""
import numpy as np
from PIL import Image, ImageFilter
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
a=np.asarray(Image.open(P%2).convert("RGB")).astype(float).copy()
def yatay(x0,y0,x1,y1,kaynak):      # kaynak: 'sol' veya 'sag'
    for y in range(y0,y1):
        src=a[y,kaynak] if False else None
    k=slice(x1,x1+40) if kaynak=="sag" else slice(max(0,x0-40),x0)
    for y in range(y0,y1):
        c=a[y,k].mean(0); a[y,x0:x1]=c
def dikey(x0,y0,x1,y1,kaynak):
    k=slice(y1,y1+40) if kaynak=="alt" else slice(max(0,y0-40),y0)
    for x in range(x0,x1):
        c=a[k,x].mean(0); a[y0:y1,x]=c
dikey(0,0,660,250,"alt")          # durum plakasi + MPC
dikey(0,250,420,440,"alt")        # gorev takibi
yatay(1900,0,2266,300,"sol")      # sag ust panel
yatay(1930,290,2266,480,"sol")    # kamera dugmeleri
dikey(1480,760,2266,1400,"ust")   # beceri carki
dikey(0,900,1420,1400,"ust")      # sohbet
dikey(0,1400,2266,1488,"ust")     # alt bar
im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
im.save("dunya.png"); print("dunya.png",im.size)
