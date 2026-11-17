#!/usr/bin/env python3
"""Efekt 10 -> tek GIF (siyah fon, 30 kare/sn): pembe patlama + dagilan altin isiklar (yapraklar) + sari patlama/yatay parlama.
Cikarilan: oyuncu govdesi (renksiz pikseller, oyuncu kutusu), kilic kesigi yaylari (oyuncu tarafindaki buyuk sari bilesenler).
Mob silueti (kayitta mob isigin onunde duruyor) komsu isikla doldurulur: efekt tek basina, deliksiz.
Kayitta 96. kareden sonra ekran kontrol merkezi ile bulaniklasiyor; son kare (parlama) 4 karede sondurulur (eklenen kareler: 17-20)."""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10"); ONZ=os.path.join(B_,"..","..","onizlemeler")
J=json.load(open(os.path.join(K,"bilgi.json"))); X,Y,W,H=J["kutu_ekran"]
Z=np.load(os.path.join(K,"zemin_kutu.npy")).astype(np.float32).mean(2)               # efektsiz zemin (kutu): cit cubuklari = ince karanlik dikey yapilar
yy0,xx0=np.mgrid[0:Z.shape[0],0:Z.shape[1]]
CIT=(Z<ndimage.median_filter(Z,size=(1,15))-12)&(xx0+X>1440)&(xx0+X<1600)&(yy0+Y>620)&(yy0+Y<960)
CIT=ndimage.binary_dilation(CIT,np.ones((3,3)))
rm=np.load(os.path.join(K,"mob_maskesi.npy")); mobd=ndimage.binary_dilation(rm,np.ones((9,9)))
yy,xx=np.mgrid[0:H,0:W]; sx=xx+X; sy=yy+Y
AURA=(1365,765); AURA_R=170; HALKA=(1380,927,100,55)
oyuncu=(sx>1040)&(sx<1265)&(sy>630)&(sy<900)
out=[]
for ki,f in enumerate(sorted(glob.glob(os.path.join(K,"skill","skill_*.png")))):
    E=np.asarray(Image.open(f).convert("RGB"),dtype=np.float32); mx=np.maximum(E.max(2),1)
    doy=(mx-E.min(2))/mx
    sil=oyuncu&(doy<0.35)&(mx>8)                                                  # renksiz: oyuncu govdesi
    govde=ndimage.binary_dilation(sil,np.ones((7,7)))
    sar=(E.max(2)>40)&((np.minimum(E[...,0],E[...,1])-E[...,2])/mx>0.25)
    lb,n=ndimage.label(ndimage.binary_dilation(sar,np.ones((3,3))))
    if n:
        sz=ndimage.sum(sar,lb,range(1,n+1)); cm=ndimage.center_of_mass(sar,lb,range(1,n+1))
        kes=[i+1 for i in range(n) if ki<=9 and sz[i]>500 and cm[i][1]+X<1300 and abs(cm[i][0]+Y-770)>12]   # kesik yayi (yatay parlama cizgisi y~770 kalir)
        sil|=np.isin(lb,kes)
    kesik=ndimage.binary_dilation(sil&~(oyuncu&(doy<0.35)&(mx>8)),np.ones((17,17)))
    sil=ndimage.binary_dilation(sil,np.ones((7,7)))|kesik
    if ki<=9:                                                                       # kesik zamani: oyuncu tarafinda pembe olmayan genis isik = kesik parlamasi
        kucuk=np.zeros_like(sil); lb2,n2=ndimage.label(E.max(2)>25)
        if n2:
            sz2=ndimage.sum(np.ones_like(sil),lb2,range(1,n2+1)); kucuk=np.isin(lb2,1+np.where(sz2<500)[0])
        pembe=(E[...,2]>=0.95*E[...,1])&(E[...,0]>1.25*E[...,1])
        sil|=(sx<1290)&~pembe&~kucuk&(np.abs(sy-770)>6)
    E=np.where(sil[...,None],0,E)
    # aura icindeki karanliklar (mob govdesi, kesilen oyuncu): yerel isik duzeyinin yarisindan karanlik pikseller komsudan doldurulur
    r=np.hypot(sx-AURA[0],sy-AURA[1])
    dol=mobd|(CIT&(r<AURA_R+60))
    for _ in range(2):
        L=E.max(2); v=(~dol).astype(np.float32)
        ref=ndimage.gaussian_filter(L*v,14)/np.maximum(ndimage.gaussian_filter(v,14),1e-3)
        dol|=(r<AURA_R)&(L<0.5*ref)&(ref>25)&~sil
        dol=ndimage.binary_closing(dol,np.ones((5,5)))
        E=yumusak_doldur(np.where(dol[...,None],0,E),dol,n=12,k=13)
    # oyuncu ve kesik cikarilan yer (auranin sol yani): aura saga-sola simetrik -> sag yanin aynasi
    ay=np.clip(2*AURA[0]-2*X-xx,0,W-1).astype(int)
    ayna=E[yy,ay]
    w=ndimage.gaussian_filter((sil&(r<AURA_R+30)).astype(np.float32),3)[...,None]
    E=np.maximum(E,ayna*w)
    L=E.max(2); v=(~sil).astype(np.float32)
    ref=ndimage.gaussian_filter(L*v,10)/np.maximum(ndimage.gaussian_filter(v,10),1e-3)
    h2=sil&(r<AURA_R+60)&(L<0.6*ref)&(ref>6)
    E=yumusak_doldur(np.where(h2[...,None],0,E),h2,n=12,k=13)
    # ince engeller (cit cubuklari, secim halkasi cizgisi): aura bolgesinde gri kapanis 13x13 + medyan 5 (Efekt 8 puruzsuz yontemi);
    # keskin sari parcalar (yapraklar, yatay parlama) aynen kalir
    au=np.clip((AURA_R+20-r)/40,0,1)*np.clip((ndimage.gaussian_filter(E.max(2),10)-12)/20,0,1)
    C=np.stack([ndimage.median_filter(ndimage.grey_closing(E[...,c],size=(13,13)),size=5) for c in range(3)],-1)
    keskin=(np.minimum(E[...,0],E[...,1])-E[...,2]>60)&(E.max(2)>ndimage.uniform_filter(E.max(2),21)+25)
    w=(au*~ndimage.binary_dilation(keskin,np.ones((3,3))))[...,None]
    E=E*(1-w)+np.maximum(E,C)*w
    hb=np.abs(np.hypot((sx-HALKA[0])/HALKA[2],(sy-HALKA[1])/HALKA[3])-1)<0.24      # secim halkasi bandi (cizgi + isaretler) -> komsu auradan
    E=yumusak_doldur(np.where(hb[...,None],0,E),hb,n=12,k=13)
    out.append(np.clip(E,0,255))
son=out[-1]; out+= [son*a for a in (0.7,0.45,0.25,0.1)]
M=np.max([k.max(2) for k in out],0); ys,xs=np.nonzero(M>6)
a,b,c,d=max(0,xs.min()-20),max(0,ys.min()-20),min(W,xs.max()+21),min(H,ys.max()+21)
od=os.path.join(K,"gif"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
t=tempfile.mkdtemp(); seq=list(range(len(out)))+[None]*12; ims=[]
for j,n in enumerate(seq):
    A=out[n][b:d,a:c] if n is not None else np.zeros((d-b,c-a,3))
    im=Image.fromarray(A.round().astype(np.uint8))
    if n is not None: im.save(os.path.join(od,"efekt10_%02d.png"%n)); ims.append(im)
    s=720/im.width; im.resize((720,int(im.height*s)//2*2),Image.LANCZOS).save(os.path.join(t,"a_%03d.png"%j))
g=os.path.join(ONZ,"efekt10_gif.gif")
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",t+"/a_%03d.png","-vf","split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a","-loop","0",g],check=True)
shutil.rmtree(t); print("kutu",(X+a,Y+b,c-a,d-b),os.path.getsize(g)//1024,"KB")
tw=300; th=int(tw*ims[0].height/ims[0].width); o=Image.new("RGB",(7*tw,3*th))
for j,im in enumerate(ims[:21]): o.paste(im.resize((tw,th)),((j%7)*tw,(j//7)*th))
o.save(os.path.join(ONZ,"efekt10_gif_tablo.jpg"),quality=90)
