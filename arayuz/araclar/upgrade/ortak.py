"""Upgrade pencereleri ortak: arka sahne (secim.jpg = Select Upgrade goruntusu; diger uc goruntuyle piksel piksel ayni kamera),
kirli arka plan maskesi, katman cozumu (matting)."""
import numpy as np
from PIL import Image
from scipy import ndimage
T0=0.105                     # govde gecirgenligi (olculen 0.103-0.107) -> siyah zemin alfa 0.895
def yukle(k): return np.asarray(Image.open(k+'.jpg').convert('RGB'),float)
def kirli_maske(B):
    """secim.jpg'de pencere arkasini kirleten ogeler: Select Upgrade penceresi, skill carki, Open dugmesi, NPC,
    animasyonlu efektler (simsek: mavi-beyaz; altigen cizgi: yesil-sari)"""
    H,W=B.shape[:2]; m=np.zeros((H,W),bool)
    for x0,y0,x1,y1 in [(1855,330,2266,832),(690,850,1238,1335),(968,610,1264,708),(1585,1095,1800,1395)]:
        m[y0:y1,x0:x1]=True
    R,G,Bb=B[...,0],B[...,1],B[...,2]
    sim=((R>150)&(G>170)&(Bb>200))|((Bb>170)&(Bb>R+45)&(Bb>G+10)&(G>120))   # simsek (beyaz-mavi); havuz suyu (G>B) haric
    yes=(G>120)&(G>Bb+60)&(G>=R-5)
    ef=ndimage.binary_dilation(sim|yes,np.ones((9,9)))
    l,n=ndimage.label(ef); s=ndimage.sum(ef,l,range(1,n+1)); ef=np.isin(l,1+np.nonzero(s>40)[0])
    return m|ef
def coz(O,B,U,kirli,opak,grup=None,esik=22):
    """Katman cozumu. taban = B*T0 (siyah zemin altinda, U) ya da B (U disi).
    U icinde: krom (taban'dan belirgin acik) -> opak (a=1, C=O). Geri kalan 'ic' pikseller tasarim gruplarina ayrilir
      (grup: 0 govde, 1.. panel / yuva icleri / kutu icleri ...). Her grupta temiz piksellerle  O = k*taban + c  dogrusu
      uydurulur -> a = 1-k, C = c/a (karartan ya da hafif acan ortu). Gruptaki butun ic pikseller (kirli olanlar dahil) bu degeri alir.
    U disinda: |O-B| < 10 -> a=0, degilse opak. opak maskesi: zorla opak."""
    tab=np.where(U[...,None],B*T0,B)
    lum=O.mean(-1); tl=tab.mean(-1)
    ic=U&(lum<=0.6*tl+esik)&~opak
    a=np.where(U,1.0,np.where(np.abs(O-B).max(-1)<10,0.0,1.0)); C=O.copy()
    temiz=ic&~kirli; sonuc={}
    if grup is None: grup=np.zeros(ic.shape,int)
    # grup 0 = otomatik: ic piksellerin 4-bagli bilesenleri (cizgiler bolgeleri ayirir); >0 = tasarim grubu (birlikte olculur)
    oto,_=ndimage.label(ic&(grup==0)); grup=np.where(grup>0,grup,np.where(oto>0,oto+10000,0))
    for g in np.unique(grup[ic]):
        m=ic&(grup==g); t=m&temiz
        if m.sum()<40: a[m]=np.nan; continue             # cok kucuk: komsudan
        if t.sum()<50: t=m
        x=tl[t]; y=lum[t]
        k=float(np.clip(np.polyfit(x,y,1)[0],0,1)) if np.ptp(x)>5 else 1.0
        al=1-k
        cc=np.array([np.median(O[...,j][t]-k*tab[...,j][t]) for j in range(3)])
        if al>0.85: a[m]=1.0; C[m]=O[m]                     # opak dokulu ic (yuva zemini): orijinal piksel
        else: a[m]=al; C[m]=np.clip(cc/al,0,255) if al>1e-3 else 0
        sonuc[int(g)]=(round(al,3),[round(float(v),1) for v in (np.clip(cc/al,0,255) if al>1e-3 else cc)],int(t.sum()))
    bos=np.isnan(a)
    if bos.any():
        _,(iy,ix)=ndimage.distance_transform_edt(bos,return_indices=True); a=a[iy,ix]; C=np.where(bos[...,None],C[iy,ix],C)
    ka=kirli&~U
    a=np.where(ka&(np.abs(O-B).max(-1)<10),1.0,a)
    a=np.where(opak,1.0,a); C=np.where(opak[...,None],O,C)
    return a,C,sonuc
def bilesim(a,C,B,U):
    tab=np.where(U[...,None],B*T0,B); return a[...,None]*C+(1-a[...,None])*tab

def yuva_hizali(a,C,kaynak,hedefler,w,h,ara=5):
    """bos yuva sablonunu (cerceve dahil, kaynak sol-ust, w x h) her hedefe kopyalar; hedef konumu sablonun kenar
    halkasiyla +-ara piksel aranarak hizalanir (yuva araligi tam esit degil). Vurgulu (altin) kenarlar da gri olur."""
    x0,y0=kaynak; Ts=C[y0:y0+h,x0:x0+w].mean(-1).copy(); Ta=a[y0:y0+h,x0:x0+w].copy(); Tc=C[y0:y0+h,x0:x0+w].copy()
    halka=np.zeros((h,w),bool); halka[:6]=halka[-6:]=True; halka[:,:6]=halka[:,-6:]=True
    for x,y in hedefler:
        ic=C[y+8:y+h-8,x+8:x+w-8]; sat=ic.max(-1)-ic.min(-1)
        if np.percentile(ic.mean(-1),99)<70 and np.percentile(sat,99)<40:
            # bos yuva (ikon yok): yalniz kenar halkasinda altin vurgu var mi?
            kr=C[y:y+h,x:x+w]; ks=(kr[...,0]-kr[...,2])[halka]
            if np.percentile(ks,90)<35: continue
        en=None
        for dy in range(-ara,ara+1):
            for dx in range(-ara,ara+1):
                R=C[y+dy:y+dy+h,x+dx:x+dx+w].mean(-1)
                if R.shape!=Ts.shape: continue
                e=np.median(np.abs(R-Ts)[halka])
                if en is None or e<en[0]: en=(e,dx,dy)
        _,dx,dy=en
        a[y+dy:y+dy+h,x+dx:x+dx+w]=Ta; C[y+dy:y+dy+h,x+dx:x+dx+w]=Tc
def yuva_kopyala(a,C,kaynak,hedefler,w,h):
    """bos yuva sablonunu (kaynak sol-ust) hedeflere kopyala (dinamik ikonlari siler)"""
    x0,y0=kaynak
    for x,y in hedefler:
        a[y:y+h,x:x+w]=a[y0:y0+h,x0:x0+w]; C[y:y+h,x:x+w]=C[y0:y0+h,x0:x0+w]
def yazi_sil(a,C,x0,y0,x1,y1,esik=60):
    """kutudaki acik renkli yaziyi (lum>esik) satir boyunca komsu koyu piksellerle doldurur"""
    sl=np.s_[y0:y1,x0:x1]; L=C[sl].mean(-1); m=ndimage.binary_dilation(L>esik,np.ones((3,3)))
    if not m.any(): return
    _,(iy,ix)=ndimage.distance_transform_edt(m,return_indices=True)
    for arr in (C[sl],):
        arr[m]=arr[iy[m],ix[m]]
    a[sl][m]=a[sl][iy[m],ix[m]]

def kutular(O,U,en=(40,200),boy=(25,200)):
    """gri kenar cizgisiyle cevrili kutularin ic dikdortgenleri (x,y,w,h) — yuva / deger kutusu olcumu"""
    ys,xs=np.nonzero(U); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    P=O[y0:y1,x0:x1]; L=P.mean(-1); S=P.max(-1)-P.min(-1)
    cizgi=(L>50)&(S<40); ic=ndimage.binary_fill_holes(cizgi)&~cizgi; ic=ndimage.binary_opening(ic,np.ones((5,5)))
    l,n=ndimage.label(ic); r=[]
    for i,sl in enumerate(ndimage.find_objects(l)):
        h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
        if en[0]<w<en[1] and boy[0]<h<boy[1] and (l[sl]==i+1).mean()>0.85: r.append((x0+sl[1].start,y0+sl[0].start,w,h))
    return sorted(r,key=lambda q:(q[1]//20,q[0]))
