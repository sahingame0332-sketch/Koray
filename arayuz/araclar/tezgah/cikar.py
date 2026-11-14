#!/usr/bin/env python3
"""Yerdeki Merchant tezgahi (3B nesne: mavi ortulu alcak sandik + ustunde kirmizi sancak, parsomenler, kilic, yuzukler).
Tek ekran goruntusu (2712x1220). Tezgah opak bir nesne: maske = cim olmayan pikseller -> en buyuk parca -> dis bukey zarf
(nesnenin silueti dis bukey dortgen) -> 1.2 px yumusak kenar. Renk dogrudan orijinal (isik/sicaklik sahnedeki gibi).
Cikti: kaynak/tezgah/tezgah.png (+ olculer.json)"""
import os, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__))
import sys
OUT=os.path.join(B_,"..","..","kaynak","tezgah"); os.makedirs(OUT,exist_ok=True)
# (ad, kaynak, kutu, haric kutular (ekran), karakter boyu px, karakter ayagi)
GORUNUM={"on":("tezgah.jpg",(1490,680,1795,1050),[],427,[1365,1045]),
         "yan":("tezgah_yan.jpg",(1060,440,1292,712),[(1250,455,1300,500),(1270,660,1300,712)],332,[1360,956])}
ad=sys.argv[1] if len(sys.argv)>1 else "on"
dosya,(X0,Y0,X1,Y1),HARIC,KB,AYAK=GORUNUM[ad]
O=np.asarray(Image.open(os.path.join(B_,"..","..","referans_gorseller","tezgah",dosya)).convert("RGB")).astype(float)
P=O[Y0:Y1,X0:X1]; R,G,B=P[...,0],P[...,1],P[...,2]
mx=P.max(2); mn=P.min(2)
cim=(G>=R-4)&(G>B+8)&(mx<175)                                  # olive-yesil cim
cim|=(mx<60)&(G>=R-2)&(G>=B)                                     # koyu cim golgesi
m=~cim
for (a,b,c,d) in HARIC: m[b-Y0:d-Y0,a-X0:c-X0]=False
m=ndimage.binary_opening(m,np.ones((5,5))); l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1)); m=l==(s.argmax()+1)
m=ndimage.binary_closing(m,np.ones((7,7))); m=ndimage.binary_fill_holes(m)
# dis bukey zarf
ys,xs=np.nonzero(m); pts=np.c_[xs,ys]
def zarf(p):
    p=sorted(map(tuple,p)); 
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for q in p:
        while len(lo)>=2 and cross(lo[-2],lo[-1],q)<=0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up)>=2 and cross(up[-2],up[-1],q)<=0: up.pop()
        up.append(q)
    return lo[:-1]+up[:-1]
Z=zarf(pts)
S=4; im=Image.new("L",((X1-X0)*S,(Y1-Y0)*S),0); ImageDraw.Draw(im).polygon([(x*S+S/2,y*S+S/2) for x,y in Z],fill=255)
a=np.asarray(im.resize((X1-X0,Y1-Y0),Image.LANCZOS)).astype(float)/255
# zarf, siluetin ice donuk kosesindeki cimi de alir (yan gorunus: sancak sandiktan tasiyor) -> maskeyle kesistir
mk=ndimage.gaussian_filter(ndimage.binary_dilation(m,np.ones((3,3))).astype(float),1.0)
if ad=="yan": a=np.minimum(a,np.clip(mk*1.6,0,1))      # on gorunus dis bukey: zarf yeterli (koyu kenarlar cim sanilmasin)
ys,xs=np.nonzero(a>0.02); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
spr=np.dstack([P,a*255])[y0:y1,x0:x1]
Image.fromarray(spr.astype(np.uint8),"RGBA").save(os.path.join(OUT,"tezgah.png" if ad=="on" else "tezgah_%s.png"%ad))
# kose noktalari (sadelestirilmis): zarfin en uc 4-6 noktasi
p=os.path.join(OUT,"olculer.json"); J=json.load(open(p)) if os.path.exists(p) else {}
if "ekran_kutu" in J: J={"on":J}
J[ad]=dict(ekran_kutu=[int(X0+x0),int(Y0+y0),int(x1-x0),int(y1-y0)],zarf=[[int(X0+x),int(Y0+y)] for x,y in Z],
           karakter_boyu_px=KB,karakter_ayak=AYAK,yukseklik_karakter=round((y1-y0)/KB,3),en_boy=round((x1-x0)/(y1-y0),3))
json.dump(J,open(p,"w"),indent=0)
print("tezgah",spr.shape,"ekran",X0+x0,Y0+y0, "zarf nokta",len(Z))
