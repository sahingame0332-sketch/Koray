#!/usr/bin/env python3
"""NPC alim-satim adet / para penceresi (Buy|Sell Item Count, Need|Earn Money). 4 telefon goruntusu (2712x1220), ayni pencere.
Pencere dis kutusu (1665,542)-(2281,794) = 616 x 252; arkasi NPC dukkan penceresi (hep ayni yerde, pencere kapali hali yok).
Saydamlik: arkadan sizan yazi "Total Amount" disarida 255 -> icerde ~19; dukkan dugme zemini 65 -> ~1.5
  => b = 19 (a/255)^1.86 (genie/gorev ile ayni dogrusal olmayan iliski) -> orta tonda (60-110) gecen ~%3 -> alfa 0.97.
Krom (siyaha karsi): alfa = (max-25)/35, RGB = O/alfa; sizinti (<=20) esikte kalir. Cerceve + Confirm/Cancel opak, renk orijinal.
Degisen: esya adi, ikinci satir, sayi -> Text. Giris kutusu yalniz "adet" modunda: ayri sprite.
Ciktilar kaynak/npc_alimsatim/: pencere.png (622 x 258), giris_kutusu.png (404 x 40), olculer.json"""
import os, json, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); REF=os.path.join(B_,"..","..","referans_gorseller","npc_alimsatim")
OUT=os.path.join(B_,"..","..","kaynak","npc_alimsatim"); os.makedirs(OUT,exist_ok=True)
def Y(k): return np.asarray(Image.open(os.path.join(REF,k+".jpg")).convert("RGB")).astype(float)
def krom(O,t0=25.0,T=60.0):
    al=np.clip((O.max(2)-t0)/(T-t0),0,1); rgb=np.where(al[...,None]>0,np.clip(O/np.maximum(al[...,None],1e-3),0,255),0); return rgb,al
SX,SY,SX1,SY1=1662,539,2284,797
DIS=(1665,542,2281,794); IC=(1669,546,2276,790)
CONFIRM=(1765,693,1951,743); CANCEL=(1971,693,2159,743)
P=Y("al_para")[SY:SY1,SX:SX1]; H,W=P.shape[:2]; yy,xx=np.mgrid[SY:SY1,SX:SX1]
rgb,al=krom(P)
ic=(xx>=IC[0])&(xx<IC[2])&(yy>=IC[1])&(yy<IC[3]); dis=(xx>=DIS[0])&(xx<DIS[2])&(yy>=DIS[1])&(yy<DIS[3])
opak=(dis&~ic)
for b in (CONFIRM,CANCEL): opak|=(xx>=b[0])&(xx<b[2])&(yy>=b[1])&(yy<b[3])
rgb=np.where(opak[...,None],P,rgb); al=np.where(opak,1.0,al)
al=np.where(dis,al,0)
al[(yy>=553)&(yy<628)&ic&~opak]=0                    # esya adi + ikinci satir (Text)
Image.fromarray(np.dstack([rgb,al*255]).astype(np.uint8),"RGBA").save(os.path.join(OUT,"pencere.png"))
# giris kutusu (adet modu)
GX,GY,GX1,GY1=1752,637,2156,679
G=Y("al_adet")[GY:GY1,GX:GX1].copy(); grgb,gal=krom(G,t0=12.0,T=60.0)
gal[644-GY:672-GY,1760-GX:1792-GX]=0                 # sayi "1" (Text)
Image.fromarray(np.dstack([grgb,gal*255]).astype(np.uint8),"RGBA").save(os.path.join(OUT,"giris_kutusu.png"))
# saydamlik olcumu
A=Y("al_adet"); L=A.mean(2)
k_ust=np.percentile(L[710:740,1672:1760],99); k_dug=np.median(A[650:690,2200:2270].mean(2)); a_dug=np.median(A[650:690,2283:2300].mean(2))
g=np.log(max(k_dug,0.5)/k_ust)/np.log(a_dug/255.0)
oran=np.mean([k_ust*(v/255.0)**g/v for v in range(60,111)])
json.dump(dict(sprite=[SX,SY,W,H],dis_kutu=[DIS[0],DIS[1],DIS[2]-DIS[0],DIS[3]-DIS[1]],ic=[IC[0],IC[1],IC[2]-IC[0],IC[3]-IC[1]],
               confirm=[CONFIRM[0],CONFIRM[1],CONFIRM[2]-CONFIRM[0],CONFIRM[3]-CONFIRM[1]],cancel=[CANCEL[0],CANCEL[1],CANCEL[2]-CANCEL[0],CANCEL[3]-CANCEL[1]],
               giris=[GX,GY,GX1-GX,GY1-GY],
               yazi=dict(font="RobotoSlab-Bold",punto=25,harf_araligi=2.0,renk="#EBEBEB",baslik_merkez=[1982,574],satir2_merkez=[1985,607.5],
                         sayi=dict(font="RobotoSlab-Bold",punto=26,renk="#F0DCDC",sol=1768,merkez_y=656.5)),
               saydamlik=dict(ust_sizinti=round(float(k_ust),1),dugme_sizinti=round(float(k_dug),1),dugme_dis=round(float(a_dug),1),us=round(float(g),2),alfa=round(1-float(oran),3))),
          open(os.path.join(OUT,"olculer.json"),"w"),indent=1)
print("alfa",round(1-oran,3),"us",round(g,2))
