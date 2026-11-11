#!/usr/bin/env python3
"""Roboto Slab Bold ile HUD etiketlerinin puntosunu olcer (IoU taramasi)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
F="/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf"
def murek(m):
    ys,xs=np.nonzero(m)
    return None if len(xs)==0 else m[ys.min():ys.max()+1, xs.min():xs.max()+1]
def ciz(t,p):
    f=ImageFont.truetype(F,p); im=Image.new("L",(1600,240),0)
    ImageDraw.Draw(im).text((40,40),t,font=f,fill=255); return murek(np.asarray(im)>128)
def iou(a,b):
    h,w=max(a.shape[0],b.shape[0]),max(a.shape[1],b.shape[1])
    A=np.zeros((h,w),bool);B=np.zeros((h,w),bool)
    A[:a.shape[0],:a.shape[1]]=a;B[:b.shape[0],:b.shape[1]]=b
    return (A&B).sum()/max(1,(A|B).sum())
def hedef(kare,kutu,esik,doy):
    a=np.asarray(Image.open(P%kare).convert("RGB")).astype(int)[kutu[1]:kutu[3],kutu[0]:kutu[2]]
    return murek((a.max(2)>esik)&((a.max(2)-a.min(2))<doy))
ISLER=[
 ("alt bar butonu","Character",1,(216,1420,396,1466),185,55),
 ("alt bar butonu","Commands",1,(1518,1420,1692,1466),185,55),
 ("alt bar butonu","Inventory",1,(1714,1420,1879,1466),185,55),
 ("MykoMobile","MykoMobile.com/net",1,(900,1420,1340,1470),175,200),
 ("sag panel","Active Events",1,(1950,196,2260,238),185,55),
 ("sag panel","Channel 1",1,(1950,246,2260,290),150,200),
 ("sag panel","Diez - 1",1,(1950,100,2260,142),150,200),
 ("sag panel","CR : 00:15:35",1,(1950,146,2260,190),150,200),
 ("Time Left","Time Left : 540 Minute(s)",1,(1950,76,2260,98),185,70),
 ("karakter adi","xMegaTon",1,(55,124,300,170),185,70),
 ("seviye","41",1,(360,124,430,170),150,200),
 ("HP","419/419",1,(150,10,350,52),200,55),
 ("MP","1162/1162",1,(150,54,350,94),200,55),
 ("Exp","Exp. %0,07",1,(150,96,350,132),185,55),
 ("altin","1526,490",2,(230,170,420,215),150,200),
 ("gorev basligi","Hunt :KOBOLD",1,(76,272,320,314),150,200),
 ("gorev satiri","KOBOLD",1,(76,316,250,350),150,200),
 ("sekme","SHOUT",1,(170,982,310,1022),185,55),
 ("sekme","NOTICES",1,(640,982,810,1022),185,55),
 ("sekme secili","ALL CHAT",1,(10,982,150,1022),185,70),
 ("Information","Information",1,(880,1334,1098,1368),170,70),
 ("giris","Enter text...",1,(20,1332,320,1376),150,70),
 ("bildirim","Acele Edin, %10 Bonus Cash",1,(55,924,620,952),185,60),
 ("sohbet satiri","RelaxPikachU59 : 6",1,(30,1160,400,1200),185,60),
]
for ad,metin,kare,kutu,e,d in ISLER:
    h=hedef(kare,kutu,e,d)
    if h is None or h.shape[0]<5: print("%-16s %-26s -> olculemedi"%(ad,metin)); continue
    en=(0,0)
    for p in range(8,80):
        m=ciz(metin,p)
        if m is None: continue
        v=iou(h,m)
        if v>en[0]: en=(v,p)
    print("%-16s %-26s murek %3dx%-3d  PUNTO %2d  (IoU %.3f)"%(ad,metin,h.shape[1],h.shape[0],en[1],en[0]))
