#!/usr/bin/env python3
"""Efekt 10 SIFIRDAN (kayit kullanilmadan, prosedurel): iki ayri efekt, siyah fon = eklemeli isik, 1024x1024, 60 kare/sn.
  sari_yildiz : ayri sari yildiz vurusu (referans: patlama_son_hali kareler 4-9): once uzun isinli buyuk yildiz,
                sonra kisa dikenli kucuk yildiz kuculup soner. ~0.2 sn.
  pembe       : pembe patlama (referans kareler 10-29 + yakin kamera olcumleri): beyaz cekirdek, pembe halka,
                gokkusagi halkasi (sari-yesil-turuncu-kirmizi-mor), mor dis hale, yatay isik cizgisi; sonda sariya donup soner. ~0.67 sn.
Renkler olculen degerlerden (bkz. arayuz/kaynak/efekt10/hd2). Tum parametreler asagida; degistirip yeniden uretilir."""
import os, subprocess, tempfile, shutil, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","sifirdan"); ONZ=os.path.join(B_,"..","..","onizlemeler")
N=1024; C=N/2; FPS=60
yy,xx=np.mgrid[0:N,0:N].astype(np.float32); dx=xx-C+0.5; dy=yy-C+0.5; R=np.hypot(dx,dy); A=np.arctan2(dy,dx)
def renk(h): h=h.lstrip("#"); return np.array([int(h[i:i+2],16) for i in (0,2,4)],np.float32)/255
def ease_out(t): return 1-(1-np.clip(t,0,1))**3
def pencere(t,a,b,c,d):  # 0 -> a..b yukselis -> c..d sonus
    t=np.asarray(t,dtype=np.float32); return np.clip((t-a)/max(b-a,1e-6),0,1)*np.clip((d-t)/max(d-c,1e-6),0,1)
def ekle(L,maske,rk,g=1.0): L+=maske[...,None]*rk[None,None,:]*g
def ton(L):  # eklemeli isik -> goruntu: doyunca beyaza kayar (oyundaki gibi)
    return np.clip(1-np.exp(-L*1.6),0,1)*255
def isinlar(rng,n,uzmin,uzmax,enmin,enmax):
    return [(rng.uniform(0,2*np.pi),rng.uniform(uzmin,uzmax),rng.uniform(enmin,enmax)) for _ in range(n)]
def isin_maskesi(lst,olcek,keskin=1.0):
    m=np.zeros((N,N),np.float32)
    for a,uz,en in lst:
        d=np.angle(np.exp(1j*(A-a)))                       # aci farki
        boy=uz*olcek; w=en*olcek*(1-np.clip(R/boy,0,1))    # uca dogru incelen ucgen
        on=np.clip(1-np.abs(d)*R/np.maximum(w,0.5),0,1)*(R<boy)
        m=np.maximum(m,on**keskin*(1-np.clip(R/boy,0,1))**0.6)
    return m
# ---------------- SARI YILDIZ ----------------
def sari_yildiz():
    rng=np.random.default_rng(7); n=13                       # 0.2 sn
    buyuk=isinlar(rng,18,260,470,9,20); kucuk=isinlar(rng,15,55,135,10,22)
    kareler=[]
    for i in range(n):
        t=i/(n-1); L=np.zeros((N,N,3),np.float32)
        g1=pencere(t,0,0.05,0.25,0.45)                        # buyuk isinli yildiz
        if g1>0:
            m=isin_maskesi(buyuk,0.85+0.3*ease_out(t/0.45))
            ekle(L,m,renk("#F2EE6A"),1.6*g1); ekle(L,m**3,renk("#FFFFE0"),1.2*g1)
            ekle(L,np.exp(-(R/150)**2),renk("#E8E070"),0.9*g1); ekle(L,np.exp(-(R/45)**2),renk("#FFFFF2"),1.5*g1)
        g2=pencere(t,0.25,0.4,0.55,1.0)                       # kisa dikenli kucuk yildiz, kuculerek soner
        if g2>0:
            s=1.15-0.45*np.clip((t-0.3)/0.7,0,1)
            m=isin_maskesi(kucuk,s,0.8)
            ekle(L,m,renk("#F6F2A0"),1.5*g2); ekle(L,m**2,renk("#FFFFF0"),1.0*g2)
            ekle(L,np.exp(-(R/(70*s))**2),renk("#F8F4C0"),1.2*g2); ekle(L,np.exp(-(R/(160*s))**2),renk("#C8C060"),0.35*g2)
        kareler.append(ton(L))
    return kareler
# ---------------- PEMBE PATLAMA ----------------
GOKKUSAGI=[("#FFF4A0",0.00),("#B8F080",0.18),("#F0B050",0.38),("#F06060",0.58),("#C050C0",0.80)]   # icten disa
def pembe():
    n=40; kareler=[]                                          # 0.67 sn
    rng=np.random.default_rng(3); cizgi_aci=rng.uniform(0,2*np.pi,90); cizgi_g=rng.uniform(0.3,1,90)
    for i in range(n):
        t=i/(n-1); L=np.zeros((N,N,3),np.float32)
        Rh=110+300*ease_out(t/0.55)                           # halka yaricapi (ease-out)
        pem=pencere(t,0,0.04,0.45,0.8)                        # pembe evre
        sar=pencere(t,0.35,0.55,0.7,1.0)                      # sari evre (sonda)
        # mor dis hale
        ekle(L,np.exp(-((R-Rh*1.05)/(Rh*0.35))**2)*(R>Rh*0.6),renk("#4C1535"),1.2*pem)
        # pembe-mercan halka (gokkusaginin ici)
        ekle(L,np.exp(-((R-Rh*0.62)/(Rh*0.20))**2),renk("#EA7A8E"),1.3*pem)
        ekle(L,np.exp(-((R-Rh*0.40)/(Rh*0.18))**2),renk("#F6A8C5"),1.4*pem)
        # gokkusagi halkasi
        gw=Rh*0.22
        for rk,o in GOKKUSAGI:
            ekle(L,np.exp(-((R-(Rh*0.80+o*gw))/(gw*0.16))**2),renk(rk),0.75*pencere(t,0.03,0.12,0.6,0.95))
        # radyal ince isinlar (aura dokusu)
        d=np.min(np.abs(np.angle(np.exp(1j*(A[...,None]-cizgi_aci[None,None,:]))))*R[...,None]/np.maximum(1.2+0*R[...,None],1)*1.0 + (1-cizgi_g[None,None,:])*0,axis=2)
        ekle(L,np.clip(1-d/2.0,0,1)*(R<Rh*0.95)*(R>40),renk("#F8C8D8"),0.35*pem)
        # beyaz cekirdek
        rc=55+60*ease_out(t/0.4)
        ekle(L,np.exp(-(R/rc)**2),renk("#FFFFFF"),2.4*pencere(t,0,0.02,0.4,0.85))
        ekle(L,np.exp(-(R/(rc*1.8))**2),renk("#FFE8F0"),0.9*pem)
        # sari evre: cekirdek ve hale sariya doner
        ekle(L,np.exp(-(R/(Rh*0.55))**2),renk("#F2F398"),1.4*sar); ekle(L,np.exp(-(R/(Rh*1.0))**2),renk("#817025"),0.5*sar)
        # yatay isik cizgisi
        uz=380+720*ease_out(t/0.4); uz=uz*(1-0.45*np.clip((t-0.42)/0.58,0,1))
        gc=pencere(t,0,0.03,0.85,1.0)
        boy=np.clip(1-np.abs(dx)/(uz/2),0,1)**0.7
        cr=renk("#FDFBD4")*(1-sar)+renk("#F5F495")*sar
        ekle(L,boy*np.exp(-(dy/2.2)**2),cr,2.0*gc); ekle(L,boy*np.exp(-(dy/9)**2),renk("#E8D070"),0.6*gc)
        ekle(L,boy**2*np.exp(-(dy/28)**2),renk("#AA804A"),0.35*gc)
        kareler.append(ton(L))
    return kareler
def yaz(ad,kareler):
    od=os.path.join(K,ad); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    for j,k in enumerate(kareler): Image.fromarray(k.round().astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,j)))
    pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
    subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(FPS),"-i",od+"/"+ad+"_%02d.png","-vf","tpad=stop=30,scale=720:-1:flags=lanczos,"+pal,"-loop","0",os.path.join(ONZ,"efekt10_sifirdan_%s.gif"%ad)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(FPS),"-i",od+"/"+ad+"_%02d.png","-vf","tpad=stop=30","-c:v","libx264","-crf","10","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_sifirdan_%s.mp4"%ad)],check=True)
    # 10 sn yavas cekim (kare tutma)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","%.4f"%(len(kareler)/10),"-i",od+"/"+ad+"_%02d.png","-vf","fps=30","-c:v","libx264","-crf","10","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_sifirdan_%s_yavas10.mp4"%ad)],check=True)
    print(ad,len(kareler),"kare")
yaz("sari_yildiz",sari_yildiz()); yaz("pembe",pembe())
