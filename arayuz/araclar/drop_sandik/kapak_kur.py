"""Kapak dokusu (oval kubbe), bantlar DUZ:
 1) b goruntusunden geri izdusum (on yari + tepe), 2) her satirda ic bantlarin merkezine gore satir hizalama,
 3) sutun siniflamasi (ahsap / bant-kenar) satirlarin medyanindan -> dik bant maskesi,
 4) bant/kenar sutunlari ayrik model: satir isigi(phi) x sutun profili(x) (ikisi de orijinal piksellerden),
 5) on yari tepe ekseninde aynalanip arka yariya (simetrik golgelenme: tepe en parlak, oval gorunum)."""
import numpy as np
from PIL import Image
from scipy import ndimage
import doku as Dk
from mesh import kesit
a,HB,HL,L,n=Dk.a,Dk.HB,Dk.HL,Dk.L,Dk.n; PX=Dk.PX
W,H=int(L*PX),int(1.4*(a+HL)*PX); u,v=Dk.izgara(W,H); phi=v*np.pi
kz,ky=kesit(phi,a,HL,n); e=1e-3; kz2,ky2=kesit(np.clip(phi+e,0,np.pi),a,HL,n); kz1,ky1=kesit(np.clip(phi-e,0,np.pi),a,HL,n)
tz,ty=kz2-kz1,ky2-ky1; nz,ny=ty,-tz; nn=np.hypot(nz,ny)+1e-12
p=np.stack([u*L,HB+ky,kz],-1); nr=np.stack([np.zeros_like(u),ny/nn,nz/nn],-1)
T,_=Dk.yuzey(p,nr,['b'],(H,W),0.12)
on=slice(H//2,H)                        # satir 0 = arka taban (phi=pi); alt yari = on + tepe
I=T[on].copy(); ok=np.isfinite(I).all(-1); print('on yari dolu',ok.mean().round(3))
I=Dk.doldur(I); h=I.shape[0]
# 2) satir hizalama: ic iki bant
sat=I.max(-1)-I.min(-1); gum=ndimage.uniform_filter1d((sat<38).astype(float),5,axis=1)>0.5
x0,x1=int(0.12*W),int(0.88*W); mer=np.full((h,2),np.nan)
for y in range(h):
    if not ok[y].mean()>0.6: continue
    l,k=ndimage.label(gum[y,x0:x1])
    if k<2: continue
    sl=ndimage.find_objects(l); boy=np.array([s[0].stop-s[0].start for s in sl]); sec=np.sort(np.argsort(boy)[-2:])
    if boy[sec].min()<6: continue
    mer[y]=[x0+(sl[j][0].start+sl[j][0].stop)/2 for j in sec]
iy=np.isfinite(mer).all(1); hedef=np.median(mer[iy],0); yy=np.arange(h)
for j in range(2): mer[:,j]=np.interp(yy,yy[iy],ndimage.median_filter(mer[iy,j],9))
# uclardaki bantlar icin de capa: ahsap-bant gecisi (sol: ilk ahsap, sag: son ahsap)
odun=(sat>45)&(I.mean(-1)>25)
def kenar(y,sol):
    r=odun[y]; idx=np.nonzero(r[:W//2] if sol else r[W//2:])[0]
    if len(idx)<3: return np.nan
    return idx[0] if sol else W//2+idx[-1]
ks=np.array([kenar(y,True) for y in range(h)],float); kg=np.array([kenar(y,False) for y in range(h)],float)
for arr in (ks,kg):
    g=np.isfinite(arr)&iy; arr[:]=np.interp(yy,yy[g],ndimage.median_filter(arr[g],9))
hks,hkg=np.median(ks),np.median(kg)
O=np.zeros_like(I); xt=np.arange(W)+0.5
for y in range(h):
    xs=np.interp(xt,np.r_[0,hks,hedef,hkg,W],np.r_[0,ks[y],mer[y],kg[y],W])
    for c in range(3): O[y,:,c]=np.interp(xs-0.5,np.arange(W),I[y,:,c])
# 3) sutun siniflamasi
satO=O.max(-1)-O.min(-1); orta=slice(int(0.15*h),int(0.9*h))
odun_sut=np.median(satO[orta],0)>40
odun_sut=ndimage.binary_opening(odun_sut,np.ones(3)); odun_sut=ndimage.binary_closing(odun_sut,np.ones(3))
# 4) bant/kenar sutunlari: satir isigi x sutun profili
B=~odun_sut; sat_isik=np.median(O[:,B].mean(-1),1)[:,None]+1e-3          # satir basina (h,)
prof=np.median(O[:,B]/sat_isik[:,:,None],0)                              # (nB,3)
O2=O.copy(); O2[:,B]=sat_isik[:,:,None]*prof[None]
# gecis yumusat (1 px)
m=ndimage.gaussian_filter(B.astype(float),0.6)[None,:,None]; O=O*(1-m)+O2*m
# 4b) bant duzeni fotograftan olculen oranlara (g ve a: uc bant 0.125, ahsap 0.10, ic bant 0.11, orta ahsap 0.33)
satO=O.max(-1)-O.min(-1); gm=np.median(satO[orta],0)<12
l,k=ndimage.label(gm); sl=ndimage.find_objects(l); kos=sorted([(s_[0].start,s_[0].stop) for s_ in sl if s_[0].stop-s_[0].start>=4])
print('gumus sutun araliklari',kos)
if len(kos)==4:
    src=[0,kos[0][1],kos[1][0],kos[1][1],kos[2][0],kos[2][1],kos[3][0],W]
    hed=W*np.array([0,.125,.225,.335,.665,.775,.875,1.0])
    xs=np.interp(np.arange(W)+0.5,hed,src)
    O=np.stack([np.stack([np.interp(xs-0.5,np.arange(W),O[y,:,c]) for c in range(3)],-1) for y in range(O.shape[0])])
BANT=[.125,.225,.335,.665,.775,.875]
# 4c) olculen duzene gore son temizlik: bant sutunlari = satir isigi x sutun profili (cekirdekten), bant-ahsap
#     arasinda fotograftaki gibi koyu golge cizgisi (ahsap kenari 2 px karartilir); gecis karisimi (turuncu) kalmaz
kn=np.r_[0,BANT,1]*W; xc=np.arange(W)+0.5
bant=np.zeros(W,bool); cek=np.zeros(W,bool)
for j in range(0,8,2):
    bant|=(xc>=kn[j])&(xc<kn[j+1]); cek|=(xc>=kn[j]+(2 if j>0 else 0))&(xc<kn[j+1]-(2 if j<6 else 0))
isik=np.median(O[:,cek].mean(-1),1)[:,None]+1e-3
prof=np.stack([np.median(O[:,i]/isik,0) for i in range(W)])          # her sutun icin (3,)
for j in range(0,8,2):                                                # bant kenar sutunlari: ayni bantin cekirdek profili kenara uzatilir
    ii=np.nonzero((xc>=kn[j])&(xc<kn[j+1]))[0]; cc=ii[cek[ii]]
    for i in ii:
        if not cek[i]: prof[i]=prof[cc[np.argmin(abs(cc-i))]]
O=np.where(bant[None,:,None],isik[:,:,None]*prof[None],O)
# ahsap seridinin bant komsusu 6 px'i (kaynakta bant/ahsap karisimi -> turuncu cizgi) iceriden ahsapla doldurulur
O0=O.copy()
for x in kn[1:-1]:
    for i in range(W):
        if bant[i] or abs(xc[i]-x)>6: continue
        ref=int(np.clip(x+(7 if xc[i]>x else -7),0,W-1))
        if not bant[ref]: O[:,i]=O0[:,ref]
kenar=np.zeros(W)
for x in kn[1:-1]:
    d=np.abs(xc-x); kenar=np.maximum(kenar,np.clip(1-(d-0.5)/2.0,0,1)*(~bant))
O=O*(1-0.45*kenar[None,:,None])
# 5) ayna: tam doku = [arka yari (aynalanmis on), on yari]
F=np.concatenate([O[::-1],O],0)[:H]
if F.shape[0]<H: F=np.concatenate([F,O[-(H-F.shape[0]):]],0)
Dk.kaydet('kapak',F); print('bant sutunlari',np.nonzero(np.diff(B.astype(int)))[0])
