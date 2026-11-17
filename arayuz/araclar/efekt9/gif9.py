#!/usr/bin/env python3
"""Efekt 9 vurus -> uc GIF (siyah fon = oyundaki eklemeli isik, 30 kare/sn):
  1) isin_halka : gokten inen turuncu-kirmizi isin + ona bagli yerdeki pembe dalga halkasi
  2) patlama    : havaya sacilan altin yapraklar + pembe patlama + sari patlama + yildiz (isin ve halka haric)
  3) sari       : yalniz sari patlama + yildiz
Kaynak: paket_vurus (kayittan, temizlenmis), renk_pembe / renk_sari (renk_ayir9.py). Parca kareleri kaynak/efekt9/gif_<ad>/ altina da yazilir.
Cikti: onizlemeler/efekt9_gif_isin_halka.gif, efekt9_gif_patlama.gif, efekt9_gif_sari.gif (+ efekt9_gif_tablo.jpg)"""
import os, json, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','efekt'))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt9"); ONZ=os.path.join(B_,"..","..","onizlemeler")
J=json.load(open(os.path.join(K,"paket_olculer.json"))); x,y,w,h=J["vurus"]["kutu_ekran"]; N=J["vurus"]["kare"]
MERKEZ=(485,665); ZEMIN=(522,812)
yy,xx=np.mgrid[0:h,0:w]; dx=xx+x-MERKEZ[0]; dy=yy+y-MERKEZ[1]; r=np.hypot(dx,dy)
gx=xx+x-ZEMIN[0]; gy=yy+y-ZEMIN[1]
yer=np.hypot(gx/250.0,gy/105.0)                                            # yerdeki halka elipsi (secim halkasinin cevresi)
kolon=np.abs(dx-0.275*dy)/1.037                                            # isin ekseni: ust (374,262) -> merkez -> yer halkasi (522,812)
koni=np.clip((45+0.45*np.maximum(-dy,0)-kolon)/25,0,1)*(dy<170)            # isin parlamasi (yukari genisleyen koni) + yere inen cekirdek
koni=np.where(dy>0,np.clip((22-kolon)/8,0,1)*(dy<150),koni)
oku=lambda d,ad,n: np.asarray(Image.open(os.path.join(K,d,"%s_%02d.png"%(ad,n))).convert("RGB"),dtype=np.float32)
P={k:[] for k in ("isin_halka","patlama","sari")}
for n in range(N):
    E=oku("paket_vurus","vurus",n); Pe=oku("renk_pembe","pembe",n); Se=oku("renk_sari","sari",n)
    R,G,B=E[...,0],E[...,1],E[...,2]; mx=np.maximum(E.max(2),1)
    # yapraklar (kucuk, merkezden uzak bilesenler)
    yap=np.zeros(E.shape[:2],bool); lb,nl=ndimage.label(E.max(2)>25)
    if nl:
        sz=ndimage.sum(np.ones(E.shape[:2]),lb,range(1,nl+1)); cm=ndimage.center_of_mass(np.ones(E.shape[:2]),lb,range(1,nl+1))
        yap=np.isin(lb,[i+1 for i in range(nl) if sz[i]<3000 and np.hypot(cm[i][1]+x-MERKEZ[0],cm[i][0]+y-MERKEZ[1])>90])
    yapd=ndimage.binary_dilation(yap,np.ones((7,7)))
    # isin: turuncu-kirmizi ton, koni icinde; patlama cekirdeginde (r<70) yalniz dar cekirdek
    turuncu=np.clip((0.88-G/np.maximum(R,1))/0.2,0,1)*(B<=G+10)
    dar=np.clip((14-kolon)/6,0,1)
    isin=turuncu*np.where(r<80,dar,koni)*(~yapd)
    # isin icindeki karanlik siluetler (oyuncu/mob govdesi gecmis) -> komsu isikla doldur
    I=E*isin[...,None]; S=ndimage.gaussian_filter(I.max(2),12); S2=ndimage.gaussian_filter((isin>0.3).astype(np.float32),12)
    ref=S/np.maximum(S2,1e-3)
    delik=((koni>0.5)&(r>80)&(I.max(2)<0.45*ref)&(ref>12)&(~yapd)&(S2>0.35)) | (n>=10)&((koni>0.6)&(dy<-30)&(r<220)&(isin<0.3)&(~yapd))
    I=yumusak_doldur(np.where(delik[...,None],0,I),delik,n=10,k=11)
    # halka: yerdeki pembe dalga (elips bandi)
    pembe=np.clip(((B-G)/mx+0.02)/0.12,0,1)*(R>20)
    bant=np.clip((1.25-yer)/0.15,0,1)*np.clip((gy+60)/30,0,1)
    halka=pembe*bant
    Hh=E*halka[...,None]; S=ndimage.gaussian_filter(Hh.max(2),10); S2=ndimage.gaussian_filter((halka>0.3).astype(np.float32),10)
    ref=S/np.maximum(S2,1e-3)
    hd=(bant>0.5)&(Hh.max(2)<0.45*ref)&(ref>15)&(S2>0.3)
    Hh=yumusak_doldur(np.where(hd[...,None],0,Hh),hd,n=10,k=11)
    IH=np.maximum(I,Hh)
    wi=np.clip(ndimage.gaussian_filter(np.maximum(isin,halka),1.5),0,1)[...,None]
    # patlama: pembe (deliksiz) + sari + altin yapraklar; isin ve halka cikarilir
    yap=ndimage.gaussian_filter(yapd.astype(np.float32),1.5)[...,None]
    PT=np.maximum(Pe*(1-wi)+Se, E*yap)
    for k,v in (("isin_halka",IH),("patlama",PT),("sari",Se)): P[k].append(np.clip(v,0,255))
def gif(ad,kareler,genislik=640):
    M=np.max([k.max(2) for k in kareler],0); ys,xs=np.nonzero(M>6)
    a,b,c,d=max(0,xs.min()-20),max(0,ys.min()-20),min(w,xs.max()+21),min(h,ys.max()+21)
    od=os.path.join(K,"gif_"+ad); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    t=tempfile.mkdtemp(); ims=[]
    seq=list(range(len(kareler)))+[None]*12                                 # sonunda 0.4 sn bos (dongu)
    for j,n in enumerate(seq):
        A=kareler[n][b:d,a:c] if n is not None else np.zeros((d-b,c-a,3))
        im=Image.fromarray(A.round().astype(np.uint8))
        if n is not None: im.save(os.path.join(od,"%s_%02d.png"%(ad,n)))
        s=genislik/im.width; im=im.resize((genislik,int(im.height*s)//2*2),Image.LANCZOS); im.save(os.path.join(t,"a_%03d.png"%j)); ims.append(im)
    out=os.path.join(ONZ,"efekt9_gif_%s.gif"%ad)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",t+"/a_%03d.png","-vf","split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a","-loop","0",out],check=True)
    shutil.rmtree(t); print(ad,"kutu",(x+a,y+b,c-a,d-b),os.path.getsize(out)//1024,"KB"); return ims
T={k:gif(k,v) for k,v in P.items()}
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
sec=[2,5,8,11,14,17,20,23]; ad={"isin_halka":"1) IŞIN + YERDE PEMBE DALGA","patlama":"2) YAPRAKLAR + PEMBE + SARI PATLAMA + YILDIZ","sari":"3) SARI PATLAMA + YILDIZ"}
sat=[]
for k in T:
    th=[im.resize((220,int(220*im.height/im.width))) for im in (T[k][n] for n in sec)]; hh=max(i.height for i in th)
    c=Image.new("RGB",(8*224,hh+30),(24,24,28)); dr=ImageDraw.Draw(c); dr.text((6,4),ad[k],font=F,fill=(255,220,120))
    for j,i in enumerate(th): c.paste(i,(j*224,30))
    sat.append(c)
o=Image.new("RGB",(8*224,sum(s.height+6 for s in sat)),(24,24,28)); yy0=0
for s in sat: o.paste(s,(0,yy0)); yy0+=s.height+6
o.save(os.path.join(ONZ,"efekt9_gif_tablo.jpg"),quality=90)
