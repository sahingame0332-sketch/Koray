#!/usr/bin/env python3
"""Respawn penceresi (karakter olunce): tek ekran goruntusu (2712x1220), pencereSIZ kare yok.
Pencere: dis koyu cizgi + tan cerceve, dis kutu (1985,645)-(2685,1031) = 700 x 386.
Zemin saydamligi: pencere ici ust seritteki cim / hemen ustundeki cim parlaklik orani 0.067-0.091 -> alfa ~0.92.
Krom: pencere icinde arkadan sizan sahne = yerel karanlik taban (gri acma 21 px); R = O - taban,
siyaha karsi cozulur (alfa = (max R - t0)/(T - t0), RGB = R/alfa). Cerceve ve dugme opak, renk orijinal.
Cikti: kaynak/respawn/respawn_pencere.png (704 x 390, yazilar orijinal piksellerden), respawn_bos.png (yazisiz)."""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B_,"..","..","referans_gorseller","respawn","respawn.jpg")
OUT=os.path.join(B_,"..","..","kaynak","respawn"); os.makedirs(OUT,exist_ok=True)
O=np.asarray(Image.open(REF).convert("RGB")).astype(float)
SX,SY,SX1,SY1=1983,643,2687,1033                  # sprite (2 px pay)
WX0,WY0,WX1,WY1=1986,646,2685,1031               # pencere dis kutusu (koyu dis cizgi dahil)
IX0,IY0,IX1,IY1=1991,653,2680,1026               # ic (cerceve haric)
P=O[SY:SY1,SX:SX1]; H,W=P.shape[:2]
yy,xx=np.mgrid[SY:SY1,SX:SX1]
ic=(xx>=IX0)&(xx<IX1)&(yy>=IY0)&(yy<IY1)
dis=(xx>=WX0)&(xx<WX1)&(yy>=WY0)&(yy<WY1)
# --- saydamlik olcumu ---
L=O.mean(2)
oran=[L[655:690,a:b].mean()/L[610:644,a:b].mean() for a,b in ((2000,2200),(2400,2600))]   # 2200-2400: arkada kirmizi skill ikonu (olcum disi)
oran+= [L[900:1020,2600:2676].mean()/L[900:1020,2690:2712].mean()]
alfa=round(1-float(np.mean(oran)),3)
# --- krom ---
taban=ndimage.grey_opening(P.max(2),size=(21,21))
R=np.clip(P-taban[...,None],0,255)
T,t0=60.0,8.0
al=np.clip((R.max(2)-t0)/(T-t0),0,1)
# yalniz yazilar: parlak cekirdek (>110) cevresi 2 px; arkadaki sonuk skill carki izleri (<110) atilir
yazi=ndimage.binary_dilation(P.max(2)>110,np.ones((5,5)))
al=np.where(yazi,al,0)
rgb=np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0)
# opak parcalar: cerceve halkasi + Confirm dugmesi -> renk dogrudan orijinal
DUG=(2255,951,2419,1009)
opak=(dis&~ic)|((xx>=DUG[0])&(xx<DUG[2])&(yy>=DUG[1])&(yy<DUG[3]))
rgb=np.where(opak[...,None],P,rgb); al=np.where(opak,1.0,al)
al=np.where(dis,al,0)
K=np.dstack([rgb,al*255])
Image.fromarray(K.astype(np.uint8),"RGBA").save(os.path.join(OUT,"respawn_pencere.png"))
# --- yazisiz surum (Text ile kullanmak icin): baslik + mesaj saydam, dugme yazisi dugme dokusuyla ---
Kb=K.copy()
Kb[(yy>=670)&(yy<790)&ic,3]=0
dy0,dy1=962,995                                   # "Confirm" murek x 2291-2386, y 969-986
for x in range(2287,2391):                         # dugmenin yazisiz sutunlarindan (2266-2285) ileri-geri
    s=list(range(2266,2286))+list(range(2285,2265,-1)); k=s[(x-2287)%len(s)]
    Kb[dy0-SY:dy1-SY,x-SX]=K[dy0-SY:dy1-SY,k-SX]
Image.fromarray(Kb.astype(np.uint8),"RGBA").save(os.path.join(OUT,"respawn_bos.png"))
json.dump(dict(sprite=[SX,SY,W,H],dis_kutu=[WX0,WY0,WX1-WX0,WY1-WY0],ic=[IX0,IY0,IX1-IX0,IY1-IY0],dugme=[DUG[0],DUG[1],DUG[2]-DUG[0],DUG[3]-DUG[1]],
               olculen_oranlar=[round(float(v),3) for v in oran],alfa=alfa),open(os.path.join(OUT,"olculer.json"),"w"),indent=1)
print("alfa",alfa,"oranlar",np.round(oran,3))
