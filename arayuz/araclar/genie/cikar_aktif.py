#!/usr/bin/env python3
"""Genie AKTIF durumu:
  1) Skill kilidi: genie calisirken her hizli slot ikonunun ustune yari saydam acik gri asma kilit biner.
     g_once (kilitsiz) ve g_aktif (kilitli) ayni HUD konumunda: O3 = (1-a)*O1 + a*L.
     8 farkli ikon -> piksel basina en kucuk kareler: d = aL - a*O1  (bilinmeyen aL[3], a). Kilit = (L, a).
  2) GENIE rozeti (karakterin basinin ustu): pembe isik halkasi + sari GENIE yazisi; arka sahne cevreden
     yumusak doldurulur, rozet O=(1-a)*Bg+a*Pembe modeliyle alfali sprite olarak ayrilir; harfler/yildizlar opak."""
import json, numpy as np
from scipy import ndimage
from ortak import *
O1=Y("g_once"); O3=Y("g_aktif")
MER=[(2342,633),(2012,743),(2125,720),(2240,720),(2366,743),(2490,746),(1942,845),(2052,843)]
R=48
def a_ilk(c,L=np.array([205.,205,210])):
    x,y=c; o1=O1[y-R:y+R,x-R:x+R]; o3=O3[y-R:y+R,x-R:x+R]
    v=L-o1; return np.clip(((o3-o1)*v).sum(2)/np.maximum((v*v).sum(2),200),0,1)
# merkez inceltme: kilit alfasinin agirlik merkezi (ikon halkasinin icinde)
yy,xx=np.mgrid[-R:R,-R:R]; ic=(xx**2+yy**2)<40**2
MER2=[]
for c in MER:
    a=a_ilk(c)*ic; a=np.where(a>0.15,a,0)
    cy,cx=ndimage.center_of_mass(a); MER2.append((int(round(c[0]+cx-R+0.5)),int(round(c[1]+cy-R+0.5))))
print("merkezler",MER2)
D=[];Q=[]
for (x,y) in MER2:
    D.append(O3[y-R:y+R,x-R:x+R]-O1[y-R:y+R,x-R:x+R]); Q.append(O1[y-R:y+R,x-R:x+R])
D=np.stack(D); Q=np.stack(Q)          # (k,H,W,3)
H=W=2*R; aL=np.zeros((H,W,3)); al=np.zeros((H,W))
for i in range(H):
    for j in range(W):
        # bilinmeyenler: aL0,aL1,aL2,a ; denklem: d_kc = aL_c - a*Q_kc
        A=np.zeros((len(MER2)*3,4)); b=np.zeros(len(MER2)*3)
        for k in range(len(MER2)):
            for c in range(3):
                A[k*3+c,c]=1; A[k*3+c,3]=-Q[k,i,j,c]; b[k*3+c]=D[k,i,j,c]
        s=np.linalg.lstsq(A,b,rcond=None)[0]; aL[i,j]=s[:3]; al[i,j]=s[3]
al=np.clip(al,0,1)*ic; al=np.where(al>0.06,al,0)
L=np.where(al[...,None]>0.02,aL/np.maximum(al[...,None],1e-3),0)
L=np.clip(L,0,255)
print("kilit alfa maks %.2f, ortalama renk (a>0.3) %s"%(al.max(),np.round(L[al>0.3].mean(0))))
yaz("genie_kilit",np.dstack([L,al*255]))
json.dump(dict(merkezler=MER2,boyut=2*R,ikon_capi=118),open(os.path.join(OUT,"..","kilit_olculer.json"),"w"),indent=1)

# ---------------- 2) GENIE rozeti ----------------
CX,CY,RR=1355,375,150
x0,y0=CX-RR,CY-RR
O=O3[y0:CY+RR,x0:CX+RR].copy(); h,w=O.shape[:2]
yy,xx=np.mgrid[0:h,0:w]; r=np.hypot(xx-RR,yy-RR)
bilinmeyen=r<128
etiket=(yy+y0>=452)                                   # ad etiketleri (rozetin onunde) -> zemin hesabina katilmaz
bil=~bilinmeyen&~etiket
_,(iy,ix)=ndimage.distance_transform_edt(~bil,return_indices=True)
Bg=O[iy,ix]
for _ in range(40):
    Bg=np.where(bil[...,None],O,ndimage.uniform_filter(Bg,[25,25,0]))
# model: normal (alfa) karisim  O = (1-a)*Bg + a*P ; P = halkanin pembe rengi (en doygun %2)
D=O-Bg
halka=(r>60)&(r<128)&(yy+y0<452)
sat=(O[:,:,0]+O[:,:,2])/2-O[:,:,1]
P=np.median(O[halka&(sat>np.percentile(sat[halka],98))],0)
V=P-Bg; a=np.clip((D*V).sum(2)/np.maximum((V*V).sum(2),300),0,1)
a=np.where(r<135,a,0); a=np.where(a>0.06,a,0)
renk=np.broadcast_to(P,O.shape).copy()
# GENIE harfleri ve parilti yildizlari: opak, renk dogrudan orijinalden
yk=(xx+x0>=1262)&(xx+x0<=1445)&(yy+y0>=368)&(yy+y0<=422)
harf=yk&(O[:,:,0]>170)&(O[:,:,1]>120)&(O[:,:,1]>O[:,:,2]+20)
harf=ndimage.binary_closing(harf,np.ones((3,3)))
yildiz=(O.min(2)>190)&(r<135)&~harf
yildiz=ndimage.binary_dilation(yildiz,np.ones((3,3)))&(O.min(2)>150)
for m,g in ((harf,1.0),(yildiz,0.95)):
    renk=np.where(m[...,None],O,renk); a=np.where(m,np.maximum(a,g),a)
# ad etiketinin ortdugu alt kenar: ust yarinin aynasi (halka simetrik)
alt=(yy+y0>=452)&(r<135)
a=np.where(alt,a[::-1],a); a=ndimage.gaussian_filter(a,0.6)*(a>0)
a=a*np.clip((130-r)/14.0,0,1)                          # halkanin dis isigi ~r 116-130'da biter
print("pembe P",np.round(P))
from PIL import Image
Image.fromarray(np.dstack([np.clip(renk,0,255),a*255]).astype(np.uint8),"RGBA").save(os.path.join(OUT,"genie_rozet.png"))
d=json.load(open(os.path.join(OUT,"..","kilit_olculer.json")))
d["rozet"]=dict(merkez=[CX,CY],boyut=2*RR,yazi=[1270,375,165,40],not_="normal alfa karisimi; karakter basinin ustu, ad etiketinin hemen ustu")
json.dump(d,open(os.path.join(OUT,"..","kilit_olculer.json"),"w"),indent=1)
print("rozet",a.shape)
