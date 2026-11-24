"""Urun karti sprite'lari (kategori / ana sayfa / kategori-uygun dugme) + altin para ikonu.
Kart = cerceve (opak) + siyah ic (alfa 1-T, lineer) + Purchase dugmesi (opak, orijinal piksel). Ikon/ad/fiyat silinir (Text/Image).
Arka plan s08 (Package sayfasi: o konumlarda kart yok)."""
import numpy as np, json
from scipy import ndimage
import ortak as O
B=O.yukle(8); cik={}
def kart(ad,i,x,y,w,h,cer,dug,T):
    P=O.yukle(i)[y:y+h,x:x+w]; Bb=B[y:y+h,x:x+w]
    a=np.zeros((h,w)); C=np.zeros((h,w,3))
    yy,xx=np.mgrid[0:h,0:w]
    cx0,cy0,cx1,cy1=[v-o for v,o in zip(cer,(x,y,x,y))]      # cerceve dis kutusu
    ic=(xx>=cx0)&(xx<=cx1)&(yy>=cy0)&(yy<=cy1)
    a[ic]=1-T                                               # ic: siyah, lineer alfa
    serit=ic&~((xx>=cx0+4)&(xx<=cx1-4)&(yy>=cy0+4)&(yy<=cy1-4))
    # cerceve seridi: tahmin edilen ic renginden acik pikseller opak (cizgi), digerleri ic
    bek=O.srgb(O.lin(Bb)*T); acik=(P.mean(-1)>bek.mean(-1)+10)&serit
    a[acik]=1; C[acik]=P[acik]
    bx0,by0,bx1,by1=[v-o for v,o in zip(dug,(x,y,x,y))]
    d=(xx>=bx0)&(xx<=bx1)&(yy>=by0)&(yy<=by1); a[d]=1; C[d]=P[d]
    O.kaydet('kart_%s.png'%ad,C,a)
    # kontrol: orijinal arka plan uzerine
    R=B.copy(); O.ustune(R,C,a,x,y); fark=np.abs(R[y:y+h,x:x+w]-P).mean(-1)
    bos=~(ic&~serit&~d)|True
    cik[ad]=dict(kutu=[x,y,w,h],cerceve=list(cer),dugme=list(dug),gecirgenlik_lineer=T,fark=round(float(fark.mean()),2))
    print(ad,cik[ad])
kart('kategori',4,995,283,292,315,(997,285,1284,573),(1069,533,1214,598),O.T_KART)
kart('ana',1,1009,303,294,315,(1010,304,1301,594),(1034,559,1277,617),O.T_ANA)
# uygun (fiyat <= cash) dugme: s05 Teleport karti (sutun 4, satir 1): yalniz dugme
P=O.yukle(5); bx,by=1666+3,533; O.kaydet('dugme_kategori_uygun.png',P[by:by+66,1738-1+0:1738-1+146],None)
P4=O.yukle(4); O.kaydet('dugme_kategori.png',P4[533:599,1069:1215],None)
# altin para ikonu: s04 kart2 (1059..1110, 470..525) — arka plan bilinen kart ici
P=P4[462:522,1070:1125]; Bb=O.srgb(O.lin(B[462:522,1070:1125])*O.T_KART)
d=np.abs(P-Bb).max(-1); m=d>18
l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1))
# para: soldaki en buyuk bilesen (rakamlar sagda, kirmizi) — kirmizi baskin pikselleri at
kir=(P[...,0]>150)&(P[...,1]<110)
m=m&~ndimage.binary_dilation(kir,np.ones((5,5)))
l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1)); m=l==1+np.argmax(s)
import cv2
pts=np.argwhere(m)[:,::-1].astype(np.int32); hull=cv2.convexHull(pts)
mm=np.zeros(m.shape,np.uint8); cv2.fillPoly(mm,[hull],1); m=mm>0
al=ndimage.gaussian_filter(m.astype(float),0.7)*m+ndimage.gaussian_filter(m.astype(float),0.7)*(~m)*0.5
ys,xs=np.nonzero(m); y0,y1,x0,x1=ys.min(),ys.max()+2,xs.min(),xs.max()+2
O.kaydet('para_ikonu.png',P[y0:y1,x0:x1],al[y0:y1,x0:x1])
cik['para_ikonu']=dict(kutu=[int(1070+x0),int(462+y0),int(x1-x0),int(y1-y0)])
print('para ikonu',cik['para_ikonu'])
json.dump(cik,open('kart.json','w'),indent=1)
