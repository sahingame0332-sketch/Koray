#!/usr/bin/env python3
"""Kurucunun benzetimi: arka sahne (pencere ici O/(1-a), yazilar komsudan doldurulmus) + siyah zemin (alfa 0.92)
+ pencere.png (cerceve + OK/Cancel) + Text (Roboto Slab Bold 28, +2 px harf araligi, ortali).
Cikti: onizlemeler/item_remove_onizleme.png (orijinal | yeni | fark x4) ve ortalama fark.
Kullanim: kur.py EKRAN.jpg"""
import os, sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","item_remove")
ON=os.path.join(B_,"..","..","onizlemeler"); FONT=os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf")
J=json.load(open(os.path.join(K,"olculer.json"))); X0,Y0,W,H=J['sprite']; A=J['ic_alfa']
O=np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float)
spr=np.asarray(Image.open(os.path.join(K,"pencere.png"))).astype(float)
# arka sahne tahmini
P=O[Y0:Y0+H,X0:X0+W]; yaz=(P.min(2)>120)|((P[...,0]>120)&(P[...,1]>120))
yaz=ndimage.binary_dilation(yaz,np.ones((5,5))); ic=spr[...,3]<128
S=P/(1-A); bad=yaz&ic
_,(iy,ix)=ndimage.distance_transform_edt(bad,return_indices=True); S=S[iy,ix]
S=np.clip(ndimage.uniform_filter(S,(3,3,1)),0,255)
Y=S*(1-A)                                          # siyah zemin alfa A
al=spr[...,3:4]/255; Y=Y*(1-al)+spr[...,:3]*al
# yazilar
im=Image.fromarray(Y.clip(0,255).astype(np.uint8)); f=ImageFont.truetype(FONT,J['punto'])
for k,v in J['yazi'].items():
    t=v['metin']; s=J['harf_araligi']; L=Image.new('L',(W,H),0); d=ImageDraw.Draw(L)
    w=sum(f.getlength(c) for c in t)+s*(len(t)-1); x=20.0
    # murekkep kutusu merkezine hizala
    T=Image.new('L',(int(w)+60,90),0); dt=ImageDraw.Draw(T)
    for c in t: dt.text((x,20),c,font=f,fill=255); x+=f.getlength(c)+s
    a=np.asarray(T); ys,xs=np.nonzero(a>110); cx,cy=(xs.min()+xs.max()+1)/2,(ys.min()+ys.max()+1)/2
    ox,oy=int(round(v['merkez'][0]-cx)),int(round(v['merkez'][1]-cy))
    renk=tuple(int(v['renk'][i:i+2],16) for i in (1,3,5))
    im.paste(Image.new('RGB',T.size,renk),(ox,oy),T)
Yn=np.asarray(im).astype(float)
fark=np.abs(Yn-P).mean(2); print('ortalama fark',round(fark.mean(),2),'/255; yazi bolgesi',round(fark[25:175,100:600].mean(),2))
sc=2; a=Image.fromarray(P.astype(np.uint8)).resize((W*sc,H*sc),Image.NEAREST); b=im.resize((W*sc,H*sc),Image.NEAREST)
c=Image.fromarray(np.clip(fark*4,0,255).astype(np.uint8)).convert('RGB').resize((W*sc,H*sc),Image.NEAREST)
C=Image.new('RGB',(W*sc*2+20,H*sc*2+60),(20,20,20)); C.paste(a,(0,30)); C.paste(b,(W*sc+20,30)); C.paste(c,(0,H*sc+60))
# tam ekran yeni
tam=Image.fromarray(O.astype(np.uint8)).copy(); tam.paste(im,(X0,Y0)); tam=tam.resize((W*sc+20, int((W*sc+20)*1220/2712)))
C.paste(tam,(W*sc+20,H*sc+60))
d=ImageDraw.Draw(C); f2=ImageFont.truetype(FONT,22)
d.text((8,2),'ORIJINAL (2x)',font=f2,fill=(255,255,0)); d.text((W*sc+28,2),'YENI: sprite + siyah zemin 0.92 + Text (2x)',font=f2,fill=(255,255,0))
d.text((8,H*sc+32),'FARK x4',font=f2,fill=(255,255,0)); d.text((W*sc+28,H*sc+32),'YENI, tam ekranda',font=f2,fill=(255,255,0))
C.save(os.path.join(ON,"item_remove_onizleme.png")); im.save(os.path.join(K,"benzetim.png"))
