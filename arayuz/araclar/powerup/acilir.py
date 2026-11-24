"""Acilir pencereler: satin alma ayrintisi (s11 / arka s05), paket icerigi (s09 / s08), basari bildirimi (s12) + gri ortu,
Cash Code sayfasi (s10, tam ekran opak siyah). Ic govdeler opak (olculdu: arkadaki magaza hic gorunmuyor).
Dinamik yazi/ikonlar silinir (Text/Image). Cash Code'daki ucuncu taraf marka logosu (e-pin satici) ALINMADI: bos logo yuvasi."""
import numpy as np, json, cv2
from scipy import ndimage
import ortak as O
cik={}
def sil(P,rects,ic_kutu=None):
    m=np.zeros(P.shape[:2],bool)
    for x0,y0,x1,y1 in rects: m[y0:y1,x0:x1]=True
    return cv2.inpaint(np.clip(P,0,255).astype(np.uint8)[...,::-1].copy(),m.astype(np.uint8)*255,5,cv2.INPAINT_TELEA)[...,::-1].astype(float)
def siyah(P,rects):
    """govde duz siyaha yakin: silinen dikdortgen, govdenin medyan rengiyle + ayni satirdaki ince gurultu"""
    for x0,y0,x1,y1 in rects:
        ref=np.concatenate([P[y0:y1,max(0,x0-40):x0].reshape(-1,3),P[y0:y1,x1:x1+40].reshape(-1,3)])
        P[y0:y1,x0:x1]=np.median(ref,0)
    return P
def acilir(ad,i,b,kutu,govde,silinecek,esik=14,disari=()):
    P=O.yukle(i); Bk=O.yukle(b) if b else None
    x0,y0,x1,y1=kutu; Q=P[y0:y1,x0:x1].copy()
    if Bk is not None:
        a=(np.abs(P-Bk).max(-1)>esik)[y0:y1,x0:x1]
        izin=np.zeros(a.shape,bool)
        for dx0,dy0,dx1,dy1 in disari: izin[dy0-y0:dy1-y0,dx0-x0:dx1-x0]=True     # govde disina tasan ogeler (X, dugme)
        a=ndimage.binary_closing(a&izin,np.ones((3,3))).astype(float)
    else: a=np.ones(Q.shape[:2])
    gx0,gy0,gx1,gy1=govde; a[gy0-y0:gy1-y0,gx0-x0:gx1-x0]=1
    a=np.maximum(a,ndimage.gaussian_filter(a,0.6)*(a>0))
    Q=siyah(Q,[(r[0]-x0,r[1]-y0,r[2]-x0,r[3]-y0) for r in silinecek])
    O.kaydet('%s.png'%ad,Q,a); cik[ad]=dict(kutu=[x0,y0,x1-x0,y1-y0],govde=list(govde)); print(ad,cik[ad])
acilir('ayrinti',11,5,(1026,256,1692,996),(1030,264,1682,950),
       [(1225,268,1475,310),(1296,318,1400,418),(1305,422,1380,465),(1045,462,1330,510),(1310,828,1375,878)],
       disari=[(1640,256,1692,330),(1205,950,1470,996)])
acilir('paket_icerik',9,8,(912,158,1830,1038),(918,188,1800,1028),[],disari=[(1745,158,1830,235)])
acilir('basari',12,None,(1024,575,1688,804),(1024,575,1688,804),[(1150,630,1545,690)])
# basari ortusu yok (Unity: tam ekran Image). Cash Code: oyun alani (opak siyah) + cerceve + ogeler
P=O.yukle(10); Q=P[0:1220,O.X0:O.X1].copy()
Q=siyah(Q,[(1020-O.X0,610,1445-O.X0,658)]); Q[890:1035,480-O.X0:780-O.X0]=Q[890:1035,800-O.X0:1100-O.X0]   # logo yerine yandaki bos siyah
O.kaydet('cashcode.png',Q); cik['cashcode']=dict(kutu=[O.X0,0,O.X1-O.X0,1220],giris=[780,583,904,98],use=[1093,682,257,101],
   x=[2305,254,64,64],logo_yuvasi=[480,890,300,145],placeholder_merkez=[1231,633])
json.dump(cik,open('acilir.json','w'),indent=1)
