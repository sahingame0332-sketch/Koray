"""Select Upgrade menusu (yalniz secim.jpg'de var). Govde: duz siyah alfa 0.93 (sol kenar olcumu t 0.073).
Krom (baslik cubugu, gri kenar cizgileri, 4 dugme) opak orijinal piksel; govde ici saydam (siyah Image ayri).
Sol altta pencerenin USTUNE cizilen NPC parsomen ikonu (1862-1935, 690-826) pencereye ait degil: govde sayilir."""
import numpy as np, json
from PIL import Image
from scipy import ndimage
O=np.asarray(Image.open('secim.jpg').convert('RGB'),float)
X0,Y0,X1,Y1=1846,335,2266,832
P=O[Y0:Y1,X0:X1]; H,W=P.shape[:2]; yy,xx=np.mgrid[Y0:Y1,X0:X1]
BASLIK=(1846,335,2264,404)
DUG={'item':(1881,418,2241,496),'fast':(1881,511,2241,590),'accessory':(1881,605,2241,683),'close':(1936,717,2181,782)}
GOVDE=(1860,404,2256,826)
a=np.zeros((H,W))
def kutu(r): return (xx>=r[0])&(xx<r[2])&(yy>=r[1])&(yy<r[3])
a[kutu(BASLIK)]=1
for r in DUG.values(): a[kutu(r)]=1
# kenar cizgileri: govde siniri disi + govdenin 3 px kenari (gri cizgi, opak)
g=kutu(GOVDE); ic=kutu((GOVDE[0]+4,GOVDE[1],GOVDE[2]-4,GOVDE[3]-5))
kenar=kutu((GOVDE[0]-2,GOVDE[1],GOVDE[2]+3,GOVDE[3]+6))&~ic
a[kenar&(P.mean(-1)>40)]=1
# dugme kenarlarindaki yumusak gecis (koyu golge) zaten dugme kutusunda
C=P.copy()
Image.fromarray(np.dstack([C,a*255]).clip(0,255).astype(np.uint8),'RGBA').save('secim_sprite.png')
json.dump(dict(sprite=[X0,Y0,W,H],govde=[GOVDE[0]-X0,GOVDE[1]-Y0,GOVDE[2]-GOVDE[0],GOVDE[3]-GOVDE[1]],alfa=0.93,
               dugmeler={k:[v[0]-X0,v[1]-Y0,v[2]-v[0],v[3]-v[1]] for k,v in DUG.items()}),open('secim_cfg.json','w'),indent=1)
print('secim sprite',W,H)
