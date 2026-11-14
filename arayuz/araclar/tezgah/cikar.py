#!/usr/bin/env python3
"""Yerdeki Merchant tezgahi (3B nesne: mavi ortulu alcak sandik + ustunde kirmizi sancak, parsomenler, kilic, yuzukler).
Tek ekran goruntusu (2712x1220). Tezgah opak bir nesne: maske = cim olmayan pikseller -> en buyuk parca -> dis bukey zarf
(nesnenin silueti dis bukey dortgen) -> 1.2 px yumusak kenar. Renk dogrudan orijinal (isik/sicaklik sahnedeki gibi).
Cikti: kaynak/tezgah/tezgah.png (+ olculer.json)"""
import os, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__))
O=np.asarray(Image.open(os.path.join(B_,"..","..","referans_gorseller","tezgah","tezgah.jpg")).convert("RGB")).astype(float)
OUT=os.path.join(B_,"..","..","kaynak","tezgah"); os.makedirs(OUT,exist_ok=True)
X0,Y0,X1,Y1=1490,680,1795,1050
P=O[Y0:Y1,X0:X1]; R,G,B=P[...,0],P[...,1],P[...,2]
mx=P.max(2); mn=P.min(2)
cim=(G>=R-4)&(G>B+8)&(mx<175)                                  # olive-yesil cim
cim|=(mx<60)&(G>=R-2)&(G>=B)                                     # koyu cim golgesi
m=~cim
m=ndimage.binary_opening(m,np.ones((5,5))); l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1)); m=l==(s.argmax()+1)
m=ndimage.binary_closing(m,np.ones((9,9))); m=ndimage.binary_fill_holes(m)
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
ys,xs=np.nonzero(a>0.02); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
spr=np.dstack([P,a*255])[y0:y1,x0:x1]
Image.fromarray(spr.astype(np.uint8),"RGBA").save(os.path.join(OUT,"tezgah.png"))
# kose noktalari (sadelestirilmis): zarfin en uc 4-6 noktasi
json.dump(dict(ekran_kutu=[int(X0+x0),int(Y0+y0),int(x1-x0),int(y1-y0)],zarf=[[int(X0+x),int(Y0+y)] for x,y in Z],
               karakter_boyu_px=427,karakter_ayak=[1365,1045]),open(os.path.join(OUT,"olculer.json"),"w"),indent=0)
print("tezgah",spr.shape,"ekran",X0+x0,Y0+y0, "zarf nokta",len(Z))
