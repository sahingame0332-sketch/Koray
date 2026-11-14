#!/usr/bin/env python3
"""AUTO ATTACK SETTINGS penceresi: sprite cikarimi.
  * Pencere kutusu (273,44)-(877,1152) ici: R = O - zemin_katkisi(B); krom siyaha karsi cozulur
    (alfa = (max(R)-t0)/(T-t0), RGB = R/alfa) -> Unity'de siyah zemin Image'i (alfa 0.93) ustunde orijinal.
  * Kutu disi (X dugmesinin tasan kismi, alt kose suslemeleri): fark maskesi = alfa, renk orijinalden.
  * Hareketli parcalar ayrilir: 4 kaydirici topuzu, onay isareti, deger yazilari (40 / %70 ...).
Ciktilar kaynak/genie/sprites: aa_pencere, aa_topuz, aa_onay  (+ olculer.json)"""
import json, numpy as np
from scipy import ndimage
from ortak import *
SX,SY,SX1,SY1=262,30,898,1192                         # sprite kutusu (ekran)
WX0,WY0,WX1,WY1=273,44,877,1152                       # pencere (siyah zemin) kutusu
O=Y("g_pencere")[SY:SY1,SX:SX1]; B=Y("g_once")[SY:SY1,SX:SX1]
H,W=O.shape[:2]
R=np.clip(O-zemin_katkisi(B),0,255)
T,t0=60.0,6.0
al=np.clip((R.max(2)-t0)/(T-t0),0,1)
rgb=np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0)
ic=np.zeros((H,W),bool); ic[WY0-SY:WY1-SY,WX0-SX:WX1-SX]=True
d=np.abs(O-B).max(2); da=np.clip((d-10)/25.0,0,1)
da=ndimage.binary_fill_holes(da>0.5)*1.0*np.maximum(da,0)+0  # dugme govdesi
al=np.where(ic,al,da); rgb=np.where(ic[...,None],rgb,O)
K=np.dstack([rgb,al*255])
def kx(x): return x-SX
def ky(y): return y-SY

# --- kaydirici topuzlari: (sol, ust, sag, alt) ekran; olcum izgaradan ---
TOPUZ=[(715,733,736,806),(638,811,658,884),(677,889,698,962),(548,967,569,1040)]
IZ=dict(x0=357,x1=760,y=[762,840,919,997],kalinlik=8)
t=TOPUZ[0]; top=K[ky(t[1]):ky(t[3]),kx(t[0]):kx(t[2])].copy()
# topuz kenari disinda kalan iz pikselleri -> saydam (topuz yuvarlak uclu dikdortgen)
g=top[:,:,3]>40; g=ndimage.binary_fill_holes(ndimage.binary_closing(g,np.ones((3,3))))
yaz("aa_topuz",top)
for k,(x0,y0,x1,y1) in enumerate(TOPUZ):
    iy=IZ["y"][k]; xa,xb=kx(x0)-2,kx(x1)+2
    for yy in range(ky(y0)-1,ky(y1)+1):
        row=K[yy,xa:xb]
        beyaz=(row[:,:3].min(1)>150)&(row[:,3]>200)          # ustteki etiket yazisi (topuzun ustunde cizili) korunur
        if abs(yy+SY-iy)<=11:                                   # iz bandi: soldaki/sagdaki iz pikselinden ara deger
            L=K[yy,xa-6:xa].mean(0); Rr=K[yy,xb:xb+6].mean(0); t=np.linspace(0,1,xb-xa)[:,None]
            dol=L*(1-t)+Rr*t
        else: dol=np.zeros_like(row)                           # pencere zemini: saydam
        K[yy,xa:xb]=np.where(beyaz[:,None],row,dol)
# --- onay isareti (3. kutu) ---
OX0,OY0,OX1,OY1=604,1028,664,1082
o=K[ky(OY0):ky(OY1),kx(OX0):kx(OX1)].copy()
m=(o[:,:,:3].min(2)>165)&(o[:,:,3]>150); m=ndimage.binary_dilation(m,np.ones((3,3)))
on=o.copy(); on[:,:,3]=np.where(m,on[:,:,3],0); yaz("aa_onay",on)
K[ky(OY0):ky(OY1),kx(OX0):kx(OX1)]=K[ky(OY0+54):ky(OY1+54),kx(OX0):kx(OX1)]   # bos kutu (4.) kopyasi
# --- deger yazilari ---
DEGER=[(790,752,850,790),(790,830,850,868),(790,908,850,946),(790,986,850,1024)]
for (x0,y0,x1,y1) in DEGER: K[ky(y0):ky(y1),kx(x0):kx(x1),3]=0
# --- kaydirici etiketleri ayri katman: orijinalde topuzun USTUNDE cizili (RECOVERY "AT" topuzu ortuyor) ---
ET=[(400,728,800,750),(400,806,800,830),(400,884,800,908),(400,962,800,986)]
E=np.zeros_like(K)
for (x0,y0,x1,y1) in ET:
    blk=K[ky(y0):ky(y1),kx(x0):kx(x1)]
    m=(blk[:,:,3]>30)&(blk[:,:,:3].min(2)>90); m=ndimage.binary_dilation(m,np.ones((3,3)))&(blk[:,:,3]>10)
    E[ky(y0):ky(y1),kx(x0):kx(x1)]=np.where(m[...,None],blk,0)
    blk[m]=0
yaz("aa_etiketler",E)
yaz("aa_pencere",K)
SLOT_X=[322,410,497,585,672,760]; SLOT_Y=[200,288,458,547]
json.dump(dict(sprite=[SX,SY,W,H],zemin=[WX0,WY0,WX1-WX0,WY1-WY0],alfa=ALFA_PENCERE,topuzlar=TOPUZ,iz=IZ,
               onay=[OX0,OY0,OX1-OX0,OY1-OY0],kutular=[[328,1036,43,40],[328,1090,43,40],[612,1036,43,40],[612,1090,43,40]],
               degerler=DEGER,etiketler=ET,slot_x=SLOT_X,slot_y=SLOT_Y,slot=[80,77],iksir=[[562,655,67,67],[649,655,67,67]],
               kapat=[816,45,74,74]),open(os.path.join(OUT,"..","pencere_olculer.json"),"w"),indent=1)
print("tamam",K.shape)
