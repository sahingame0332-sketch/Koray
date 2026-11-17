#!/usr/bin/env python3
"""Efekt 10 TAM dongu (kayit 20-20-35) -> tek GIF (siyah fon, 30 kare/sn):
altin yapraklar + dort koseli yildiz parlamalari -> pembe aura -> yatay sari parlama -> sari yildiz patlamasi.
Cikarilan: oyuncu (mobun sagi, kutu), kilic kesikleri (beyaz-mavi yaylar: bu skillin ve sonraki skillin), mob govdesi,
isim etiketleri (JustForFARM / xOdin / can cubugu), secim halkasi. Aura saga-sola simetrik: oyuncu + etiket tarafi sol yanin aynasiyla,
mob govdesi komsu isikla doldurulur. Son kareden sonra 4 kare sondurme (kayitta sonraki skill basliyor)."""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","tam"); ONZ=os.path.join(B_,"..","..","onizlemeler")
J=json.load(open(os.path.join(K,"bilgi.json"))); X,Y,W,H=J["kutu_ekran"]
rm=np.load(os.path.join(K,"mob_maskesi.npy")); mobd=ndimage.binary_dilation(rm,np.ones((15,15)))
yy,xx=np.mgrid[0:H,0:W]; sx=xx+X; sy=yy+Y
AURA=(900,699); AURA_R=270; PARLAMA_Y=699; HALKA=(922,894,147,60)
oyuncu=((sx>1045)&(sy>600)|(sx>990)&(sy>800))&(sx<1420)&(sy<1110)
etiket=(sx>1015)&(sx<1255)&(sy>540)&(sy<675)
r=np.hypot(sx-AURA[0],sy-AURA[1])
ay=np.clip(2*AURA[0]-2*X-xx,0,W-1).astype(int)
hb=np.abs(np.hypot((sx-HALKA[0])/HALKA[2],(sy-HALKA[1])/HALKA[3])-1)<0.2
def kucuk_sari(E,mx):
    s=(E.max(2)>30)
    lb,n=ndimage.label(ndimage.binary_dilation(s,np.ones((3,3))))
    if not n: return np.zeros_like(s)
    sz=ndimage.sum(s,lb,range(1,n+1)); cm=ndimage.center_of_mass(s,lb,range(1,n+1))
    return np.isin(lb,[i+1 for i in range(n) if sz[i]<2500 and np.hypot(cm[i][1]+X-AURA[0],cm[i][0]+Y-AURA[1])>150])
fs=sorted(glob.glob(os.path.join(K,"skill","skill_*.png")))
Ls=np.median([np.asarray(Image.open(f).convert("RGB"),dtype=np.float32).max(2) for f in fs[4:12]],0)
kar=(Ls<14)&(r<205)&~oyuncu&~etiket                                             # halkanin ici aydinlik: surekli karanlik = mob govdesi
lb,n=ndimage.label(kar); dok=np.unique(lb[mobd&kar]); dok=dok[dok>0]
MOB=ndimage.binary_dilation(np.isin(lb,dok)|rm,np.ones((9,9)))
MOB=ndimage.binary_closing(MOB,np.ones((15,15)))
ri=np.clip(r,0,AURA_R+60).astype(int)
def radyal(E,bilinmeyen):
    """bilinmeyen pikselleri ayni yaricaptaki bilinen piksellerin ortalamasiyla doldurur (aura dairesel)"""
    q=(~bilinmeyen)&(r<AURA_R+60)
    say=np.bincount(ri[q],minlength=AURA_R+61).astype(np.float64)
    P=np.stack([np.bincount(ri[q],weights=E[...,c][q],minlength=AURA_R+61) for c in range(3)],-1)/np.maximum(say,1)[:,None]
    ok=say>30
    for c in range(3): P[:,c]=np.interp(np.arange(len(P)),np.where(ok)[0],P[ok,c]) if ok.any() else 0
    P=ndimage.uniform_filter1d(P,9,axis=0)
    return np.where(bilinmeyen[...,None],P[ri],E)
out=[]
for ki,f in enumerate(fs):
    E=np.asarray(Image.open(f).convert("RGB"),dtype=np.float32); mx=np.maximum(E.max(2),1)
    yap=ndimage.binary_dilation(kucuk_sari(E,mx),np.ones((5,5)))                  # yapraklar / yildiz parlamalari: korunur
    sari=(np.minimum(E[...,0],E[...,1])-E[...,2])/mx>0.3
    cizgi=(np.abs(sy-PARLAMA_Y)<12)&sari                                           # yatay parlama cizgisi: korunur
    pembe=(E[...,0]>1.25*E[...,1])&(E[...,2]>=0.9*E[...,1])
    bm=(E[...,2]>0.85*E[...,0])&(E[...,1]>0.7*E[...,0])&(mx>15)&((r>235)|(ki>=13)|(ki<=3))&(r>110)&~pembe&(sy>620)    # beyaz-mavi kesik yaylari
    sil=(oyuncu&~yap&~cizgi)|(ndimage.binary_dilation(bm,np.ones((15,15)))&~(yap&((sy<620)|((ki<=12)&(sx<AURA[0])))))
    E=np.where(sil[...,None],0,E)
    # mob govdesi: ayni yaricaptaki aura rengi (dairesel); mob kirmizisi artigi: komsudan
    kir=ndimage.binary_dilation((E[...,0]>2.2*E[...,1]+8)&(E[...,0]>2*E[...,2]+8),np.ones((5,5)))&~MOB
    E=yumusak_doldur(np.where(kir[...,None],0,E),kir,n=10,k=11)
    # mob govdesi: yatay parlama bandi disinda komsudan (bant parlak cizgisi kaynaga karismaz),
    # bant icinde satir satir sol-sag arasi dogrusal (parlama cizgisi mobun arkasindan kesintisiz gecer)
    band=np.abs(sy-PARLAMA_Y)<16
    kay=MOB|band|sil|etiket
    F=yumusak_doldur(np.where(kay[...,None],0,E),kay,n=16,k=15)
    Hh=E.copy(); xs_=np.arange(W)
    for yb in np.where(band.any(1))[0]:
        bil=~(MOB[yb]|sil[yb]|etiket[yb])
        if bil.sum()>2:
            for c in range(3): Hh[yb,:,c]=np.interp(xs_,xs_[bil],E[yb,bil,c])
    hedef=MOB|(band&(sil|etiket)&(r<AURA_R+40))
    F=np.where(band[...,None],np.maximum(Hh,F),F)
    wm=np.maximum(ndimage.gaussian_filter(hedef.astype(np.float32),4),hedef)[...,None]
    E=F*wm+E*(1-wm)
    sil=sil|etiket
    # oyuncu tarafi: sol yanin aynasi (yumusak gecis)
    ayg=sil&(r<AURA_R+40)
    w=np.maximum(ndimage.gaussian_filter(ayg.astype(np.float32),12),ayg)[...,None]
    E=E[yy,ay]*w+E*(1-w)
    # kalan kucuk delikler: aura bolgesinde gri kapanis 15 + medyan 5; keskin sari parcalar (parlama, yildiz isinlari, yapraklar) aynen
    au=np.clip((AURA_R+20-r)/40,0,1)
    C=np.stack([ndimage.median_filter(ndimage.grey_closing(E[...,c],size=(15,15)),size=5) for c in range(3)],-1)
    keskin=(sari&(E.max(2)>ndimage.uniform_filter(E.max(2),25)+20))|yap
    w=(au*~ndimage.binary_dilation(keskin,np.ones((3,3))))[...,None]
    E=E*(1-w)+np.maximum(E,C)*w
    # kalan karanlik lekeler (aura icinde, yerel isigin yarisindan karanlik)
    L=E.max(2); ref=ndimage.gaussian_filter(L,12)
    lek=(r<AURA_R+50)&(L<0.55*ref)&(ref>14)&~MOB
    lek=ndimage.binary_dilation(lek,np.ones((3,3)))
    E=yumusak_doldur(np.where(lek[...,None],0,E),lek,n=10,k=9)
    # secim halkasi bandi
    E=yumusak_doldur(np.where(hb[...,None],0,E),hb,n=12,k=13)
    out.append(np.clip(E,0,255))
son=out[-1]; out+=[son*a for a in (0.7,0.45,0.25,0.1)]
M=np.max([k.max(2) for k in out],0); ys,xs=np.nonzero(M>6)
a,b,c,d=max(0,xs.min()-20),max(0,ys.min()-20),min(W,xs.max()+21),min(H,ys.max()+21)
od=os.path.join(K,"gif"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
t=tempfile.mkdtemp(); seq=list(range(len(out)))+[None]*12; ims=[]
for j,n in enumerate(seq):
    A=out[n][b:d,a:c] if n is not None else np.zeros((d-b,c-a,3))
    im=Image.fromarray(A.round().astype(np.uint8))
    if n is not None: im.save(os.path.join(od,"efekt10_tam_%02d.png"%n)); ims.append(im)
    s=720/im.width; im.resize((720,int(im.height*s)//2*2),Image.LANCZOS).save(os.path.join(t,"a_%03d.png"%j))
g=os.path.join(ONZ,"efekt10_tam.gif")
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",t+"/a_%03d.png","-vf","split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a","-loop","0",g],check=True)
shutil.rmtree(t); print("kutu",(X+a,Y+b,c-a,d-b),os.path.getsize(g)//1024,"KB")
tw=300; th=int(tw*ims[0].height/ims[0].width); o=Image.new("RGB",(7*tw,3*th))
for j,im in enumerate(ims[:21]): o.paste(im.resize((tw,th)),((j%7)*tw,(j//7)*th))
o.save(os.path.join(ONZ,"efekt10_tam_tablo.jpg"),quality=90)
