#!/usr/bin/env python3
"""Efekt 8 pembe-beyaz patlama (aura) — yalniz patlama, BEYAZ zemin uzerinde. Kaynak: arka katman (pürüzsüz), sari kivilcim/kesik/
yatay cizgi cikarilir. Eklemeli isik -> on-carpimsiz RGBA: alfa = max(R,G,B)/255, renk = E/alfa (isigin kendi rengi). Beyaz uzerine: alfa harmanlama.
Cikti: onizlemeler/efekt8_patlama_beyaz.png (kare kare), .mp4; kaynak/efekt8/patlama_rgba/ (saydam PNG kareleri)."""
import os, json, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from cikar8 import OUT
import sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
b=json.load(open(os.path.join(OUT,"bilgi.json"))); N=b["kare"]
od=os.path.join(OUT,"patlama_rgba"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
KES=(330,0,1200,820)                         # patlama bolgesi (kare icinde; ust kesilmesin)
MERKEZ=(805-330,600-0)                       # mobun govdesi (patlama merkezi), kare icinde
RM=np.load(os.path.join(OUT,"mob_maskesi.npy"))[KES[1]:KES[3],KES[0]:KES[2]]      # mob_maskesi ile skill kareleri ayni kokenli (700,150)
DIKIS=ndimage.binary_dilation(RM,np.ones((9,9)))&~ndimage.binary_erosion(RM,np.ones((9,9)))   # arka/on katman birlesim cizgisi
DIKIS_W=ndimage.gaussian_filter(DIKIS.astype(np.float32),2)[...,None]
KUKLA=ndimage.binary_dilation(RM,np.ones((15,15)))                                  # kukla + 7 px kenar
KUKLA_W=ndimage.gaussian_filter(ndimage.binary_dilation(KUKLA,np.ones((9,9))).astype(np.float32),4)[...,None]
SON=13                                                                              # patlama 0.47 sn'de bitiyor; sonrasi oyuncu kirintisi
kareler=[]
for n in range(N):
    E=np.asarray(Image.open(os.path.join(OUT,"skill_arka","skill_arka_%02d.png"%n)).convert("RGB"),dtype=np.float32)   # yalniz arka: kukla izi yok
    E=np.clip(E,0,255)[KES[1]:KES[3],KES[0]:KES[2]]
    # kukla silueti (+ kenar) icini cevredeki isiktan yumusak doldur: once izotropik dolgu, sonra genis gauss
    E=yumusak_doldur(E,KUKLA,n=16,k=21)
    E=KUKLA_W*ndimage.gaussian_filter(E,[6,6,0])+(1-KUKLA_W)*E
    if n>SON: E=np.zeros_like(E)
    mx=E.max(2); sari=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx,1)
    yerel=ndimage.gaussian_filter(mx,6)
    kivilcim=((mx-yerel)>18)&(sari>0.2)                                   # keskin sari parca (kivilcim, kesik, yatay cizgi)
    kivilcim|=ndimage.binary_opening(sari>0.45,np.ones((1,15)))&(mx>40)    # yatay sari cizgi
    pemb=(E[...,2]>=E[...,1]-6)|(mx>200)                                   # pembe-mor-beyaz isik
    l,nn=ndimage.label(pemb&(mx>10)); 
    if nn:
        sz=ndimage.sum(np.ones_like(mx),l,range(1,nn+1))
        yy,xx=np.mgrid[0:mx.shape[0],0:mx.shape[1]]; uz=np.hypot(xx-MERKEZ[0],yy-MERKEZ[1])
        tut=[i+1 for i in range(nn) if sz[i]>=1500 and uz[l==i+1].min()<260]    # yalniz merkezdeki patlama govdesi (oyuncu kirintisi degil)
        pemb&=np.isin(l,tut)
    pemb=ndimage.binary_fill_holes(pemb)
    # ayiklanan keskin sari parcalarin yeri bos kalmasin: patlama icinde komsu isiktan doldur
    kiv=ndimage.binary_dilation(kivilcim,np.ones((5,5)))
    yy,xx=np.mgrid[0:mx.shape[0],0:mx.shape[1]]; r=np.hypot((xx-MERKEZ[0])/1.15,yy-MERKEZ[1])
    govde=ndimage.binary_fill_holes(ndimage.binary_closing(pemb|kiv,np.ones((15,15))))
    E=yumusak_doldur(E,kiv&govde,n=14,k=15)
    # auranin ustundeki sari kivilcimlar (buyuklugune bakmadan): cekirdegin ustu, sari ya da yesilimsi-sari
    mx4=E.max(2); sr4=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx4,1)
    ust=((sr4>0.08)&(mx4>20)&(yy<MERKEZ[1]-110)&(r>120))|((n<=4)&(mx4>15)&(yy<MERKEZ[1]-90)&(np.abs(xx-MERKEZ[0])<80)&(sr4>-0.02))
    ust=ndimage.binary_dilation(ndimage.binary_opening(ust,np.ones((3,3))),np.ones((15,15)))
    if ust.any(): E=yumusak_doldur(E*(~ust)[...,None],ust,n=12,k=15); E=np.minimum(E,ndimage.gaussian_filter(E,[3,3,0])*1.0+np.where(ust[...,None],0,255))
    if n<=3:                                                                       # ilk karelerde cekirdekteki kesik kanatlari: yumusak cekirdek
        cw=ndimage.gaussian_filter(np.clip((150-r)/40,0,1),4)[...,None]
        E=cw*ndimage.gaussian_filter(E,[7,7,0])+(1-cw)*E
    pencere=np.clip((360-r)/70,0,1)                                         # patlama dairesi disi (kesik izi) yumusak kesilir
    # kilic kesigi izi: patlama cekirdegi ve yatay cizgi disinda kalan sari-krem isik (patlama pembe-mor: B >= G)
    mx2=E.max(2); sr=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx2,1)
    kesik=(sr>0.10)&(mx2>15)&(r>150)&(np.abs(yy-MERKEZ[1])>12)&(xx<MERKEZ[0]-140)&(n<=9)   # kesik yalniz solda, halka sonrasi yok
    kesik=ndimage.binary_dilation(ndimage.binary_opening(kesik,np.ones((3,3))),np.ones((25,25)))   # kesik + halesi
    # kesigin yeri: aura yatay simetrik -> merkezden aynalanan (sag yarinin) temiz aura ile doldurulur; gecis yumusak
    xm=np.clip(2*MERKEZ[0]-xx,0,mx.shape[1]-1); Ea=E[yy,xm]
    kw=ndimage.gaussian_filter(kesik.astype(np.float32),5)[...,None]
    E=kw*Ea+(1-kw)*E
    # kalan skill izi: aura yatay simetrik — sol yari (cekirdek disi) sag yarinin aynasi; cekirdekte (ilk kareler) ayna ile minimum
    xm2=np.clip(2*MERKEZ[0]-xx,0,mx.shape[1]-1); Eb=E[yy,xm2]
    sol=np.clip(((MERKEZ[0]-xx)-10)/30,0,1)*np.clip((r-100)/40,0,1)
    cizgi=(np.abs(yy-MERKEZ[1])<=6)&(n>=4)                                            # yatay patlama cizgisi (0.13 sn'den sonra) kendi kalsin
    sol=np.where(cizgi,0,sol); sol=ndimage.gaussian_filter(sol,3)[...,None]
    E=sol*Eb+(1-sol)*E
    if n<=5:
        cek=(np.clip((140-r)/40,0,1)*(~cizgi))
        cek=ndimage.gaussian_filter(cek,3)[...,None]
        E=cek*ndimage.gaussian_filter(np.minimum(E,Eb),[2,2,0])+(1-cek)*E
    # patlama disi kucuk sari/beyaz kivilcimlar (tum kareler)
    mx3=E.max(2); sr3=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx3,1)
    yerel3=ndimage.gaussian_filter(mx3,12)
    kv=((sr3>0.10)|((mx3-yerel3)>25))&(mx3>25)&(r>140)&~cizgi
    lb,nl=ndimage.label(kv)
    if nl:
        sz=ndimage.sum(np.ones_like(mx3),lb,range(1,nl+1)); kv=np.isin(lb,1+np.where(sz<3000)[0])
        kd=ndimage.binary_dilation(kv,np.ones((11,11)))
        E=yumusak_doldur(E*(~kd)[...,None],kd,n=10,k=11)
    # auranin ustundeki sari kivilcimlar (buyuklugune bakmadan): cekirdegin ustu, sari ya da yesilimsi-sari
    mx4=E.max(2); sr4=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx4,1)
    ust=((sr4>0.08)&(mx4>20)&(yy<MERKEZ[1]-110)&(r>120))|((n<=4)&(mx4>15)&(yy<MERKEZ[1]-90)&(np.abs(xx-MERKEZ[0])<80)&(sr4>-0.02))
    ust=ndimage.binary_dilation(ndimage.binary_opening(ust,np.ones((3,3))),np.ones((15,15)))
    if ust.any(): E=yumusak_doldur(E*(~ust)[...,None],ust,n=12,k=15); E=np.minimum(E,ndimage.gaussian_filter(E,[3,3,0])*1.0+np.where(ust[...,None],0,255))
    pencere=np.clip((360-r)/70,0,1)                                         # patlama dairesi disi (kesik izi) yumusak kesilir
    # kilic kesigi izi: patlama cekirdegi ve yatay cizgi disinda kalan sari-krem isik (patlama pembe-mor: B >= G)
    mx2=E.max(2); sr=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx2,1)
    kesik=(sr>0.10)&(mx2>15)&(r>150)&(np.abs(yy-MERKEZ[1])>12)&(xx<MERKEZ[0]-140)&(n<=9)   # kesik yalniz solda, halka sonrasi yok
    kesik=ndimage.binary_dilation(ndimage.binary_opening(kesik,np.ones((3,3))),np.ones((25,25)))   # kesik + halesi
    # kesigin yeri: aura yatay simetrik -> merkezden aynalanan (sag yarinin) temiz aura ile doldurulur; gecis yumusak
    xm=np.clip(2*MERKEZ[0]-xx,0,mx.shape[1]-1); Ea=E[yy,xm]
    kw=ndimage.gaussian_filter(kesik.astype(np.float32),5)[...,None]
    E=kw*Ea+(1-kw)*E
    # kalan skill izi (ilk kareler: kesik cekirdegin icinden geciyor, ust/yanlarda kivilcimlar)
    if n<=7:
        mx3=E.max(2); ince=(mx3-ndimage.gaussian_filter(mx3,10))>20                       # keskin, ince parlak cizgi
        ince&=(xx<MERKEZ[0]+30)&(np.abs(yy-MERKEZ[1])>10)                                 # sol taraf (kesik), yatay patlama cizgisi haric
        iz=ndimage.binary_dilation(ince,np.ones((15,15)))
        xm2=np.clip(2*MERKEZ[0]-xx,0,mx.shape[1]-1); Eb=E[yy,xm2]
        iw=ndimage.gaussian_filter(iz.astype(np.float32),4)[...,None]
        E=iw*np.minimum(Eb,ndimage.gaussian_filter(E,[8,8,0]))+(1-iw)*E
        # patlama govdesi disindaki kucuk sari kivilcimlar
        mx3=E.max(2); sr3=(np.minimum(E[...,0],E[...,1])-E[...,2])/np.maximum(mx3,1)
        lb,nl=ndimage.label((sr3>0.12)&(mx3>25)&(r>170))
        if nl:
            sz=ndimage.sum(np.ones_like(mx3),lb,range(1,nl+1)); kv=np.isin(lb,1+np.where(sz<2500)[0])
            E=E*(1-ndimage.gaussian_filter(ndimage.binary_dilation(kv,np.ones((9,9))).astype(np.float32),3))[...,None]
    m=ndimage.gaussian_filter((govde|kesik).astype(np.float32),3)*pencere
    E=E*m[...,None]
    a=np.clip(E.max(2)/255.0,0,1); C=E/np.maximum(a[...,None],1e-3)
    rgba=np.dstack([np.clip(C,0,255),a*255]).round().astype(np.uint8)
    Image.fromarray(rgba,"RGBA").save(os.path.join(od,"patlama_%02d.png"%n))
    beyaz=a[...,None]*C+(1-a[...,None])*255.0
    kareler.append(Image.fromarray(np.clip(beyaz,0,255).astype(np.uint8)))
# kare kare tablo (patlamanin goruldugu kareler)
dolu=[n for n in range(N) if np.asarray(kareler[n]).min()<235]
W=300; H=int(W*kareler[0].height/kareler[0].width)
c=Image.new("RGB",(6*W,((len(dolu)+5)//6)*(H+26)),(255,255,255)); d=ImageDraw.Draw(c)
for k,n in enumerate(dolu):
    X=(k%6)*W; Yy=(k//6)*(H+26); c.paste(kareler[n].resize((W,H),Image.LANCZOS),(X,Yy+26)); d.text((X+6,Yy+3),"kare %d (%.2f sn)"%(n,n/30),font=F,fill=(60,60,60))
c.save(os.path.join(ONZ,"efekt8_patlama_beyaz.png"))
t=tempfile.mkdtemp()
for i,n in enumerate(list(range(N))*3): kareler[n].save(os.path.join(t,"a_%04d.png"%i))
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",t+"/a_%04d.png","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p","-c:v","libx264","-crf","18",os.path.join(ONZ,"efekt8_patlama_beyaz.mp4")],check=True)
shutil.rmtree(t); print("dolu kareler",dolu)
