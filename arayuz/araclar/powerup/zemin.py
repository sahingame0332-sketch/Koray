"""Magaza temel sprite'i (272..2409 x 0..1220, opak): s08 (Package sayfasi) + 
 - sutun1 satir1 kartinin alti geri cozulur (lineer: B = O / T_KART), ikon/yazi/dugme/cerceve izleri inpaint
 - secili Package sekmesi -> s01'deki normal hali
 - Cash degeri '0' silinir (Text)
Sekme sprite'lari: normal + secili (6 x 2), orijinal piksel."""
import numpy as np, json, cv2
from scipy import ndimage
import ortak as O
A8=O.yukle(8); A1=O.yukle(1); Z=A8.copy()
# kart 1 (kategori) : cerceve (662,285)-(949,573) dugme (734,533)-(879,598) — sutun araligi 335.33
dx=-335
cx0,cy0,cx1,cy1=997+dx,285,1284+dx,573
ic=np.zeros(Z.shape[:2],bool); ic[cy0+3:cy1-2,cx0+3:cx1-2]=True
Z[ic]=O.srgb(O.lin(A8[ic])/O.T_KART)
bozuk=np.zeros(Z.shape[:2],bool)
bozuk[cy0-3:cy1+4,cx0-3:cx0+5]=True; bozuk[cy0-3:cy1+4,cx1-4:cx1+4]=True
bozuk[cy0-3:cy0+5,cx0-3:cx1+4]=True; bozuk[cy1-4:cy1+4,cx0-3:cx1+4]=True
bozuk[530:601,1069+dx-3:1215+dx+3]=True                                # dugme
# ikon / ad / fiyat: ic bolgede beklenen dokudan sapan acik pikseller
# ikon (+cerceve), ad (2 satir), para + fiyat: acik dikdortgenler
for x0,y0,x1,y1 in [(752,312,860,420),(678,408,942,474),(728,458,910,530)]: bozuk[y0:y1,x0:x1]=True
Z8=np.clip(Z,0,255).astype(np.uint8)
Zi=cv2.inpaint(Z8[...,::-1].copy(),bozuk.astype(np.uint8)*255,25,cv2.INPAINT_NS)[...,::-1].astype(float)
# doku: cevredeki ince doku (yuksek frekans) aynalanmis komsu bloktan eklenir
yuk=Z-ndimage.gaussian_filter(Z,(6,6,0))
gurultu=np.roll(yuk,-345,axis=1)            # komsu temiz bolgenin (sutun 2: s08'de kart yok) ince dokusu
Z=np.where(bozuk[...,None],ndimage.gaussian_filter(Zi,(4,4,0))+gurultu*0.8,Z)
# Package sekmesi normal
sx0,sx1=322,612
Z[738:822,sx0:sx1]=A1[738:822,sx0:sx1]
# Cash '0' : kutu ici (1800..2390 x 112..160) acik gri rakam -> satir komsu dokusu
kx0,kx1,ky0,ky1=2262,2330,110,162
R=Z[ky0:ky1,kx0:kx1]; m=ndimage.binary_dilation(R.mean(-1)>70,np.ones((5,5)))
fill=cv2.inpaint(np.clip(R,0,255).astype(np.uint8)[...,::-1].copy(),m.astype(np.uint8)*255,5,cv2.INPAINT_TELEA)[...,::-1]
Z[ky0:ky1,kx0:kx1]=fill
np.save('zemin_tam.npy',Z)
O.kaydet('magaza_zemin.png',Z[O.Y0:O.Y1,O.X0:O.X1])
# sekmeler: y ust sinirlari (tan cerceve), yukseklik 72 (+pay)
SEK=[('MainPage',259),('PowerUP',354),('Premiums',452),('Scrolls',549),('Special',646),('Package',744)]
SECILI={'MainPage':1,'PowerUP':2,'Premiums':4,'Scrolls':5,'Special':7,'Package':8}
cik={}
for i,(ad,y) in enumerate(SEK):
    y0,y1=y-6,y+80
    nor=(O.yukle(2) if ad=='MainPage' else A1)[y0:y1,sx0:sx1]; sec=O.yukle(SECILI[ad])[y0:y1,sx0:sx1]
    O.kaydet('sekme_%s.png'%ad,nor); O.kaydet('sekme_%s_secili.png'%ad,sec)
    cik[ad]=[sx0-O.X0,y0,sx1-sx0,y1-y0]
json.dump(cik,open('sekmeler.json','w'),indent=1); print(cik)
