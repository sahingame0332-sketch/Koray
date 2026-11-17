#!/usr/bin/env python3
"""Efekt 10 SIFIRDAN (prosedurel, kayit kullanilmadan) — 1920x1080 Full HD, 60 kare/sn, siyah fon = eklemeli isik.
Tum degerler kayitlardan olculdu (yakin kamera 21-39-19 = hd2, ic goruntu patlama_son_hali, IMG_0191-0196 parcaciklar):
  pembe       : beyaz cekirdek (0.2 R) -> seftali/pembe ic (0.2-0.4 R) -> mercan halka (0.4-0.68 R) -> koyu bordo-mor dis hale (0.68-1 R);
                kenarda gokkusagi (agirlikla sag-sol), ince radyal isinlar; R 133->253 px (ease-out, 0-270 ms);
                yatay isik cizgisi 380->1160 px, sonra 700->350; 270-330 ms pembenin kendi sari yildizi (7 isin), sari hale 330-600 ms soner;
                14 altin yaprak: aura kenarinda dogar (4 koseli parilti), her yone duz ucar, ~3.2 R yol, ~0.45 sn omur.
  sari_yildiz : AYRI vurus: 0-70 ms 20 uzun isinli buyuk limon sarisi yildiz, 70-200 ms 14 kisa dikenli kucuk yildiz kuculup soner."""
import os, subprocess, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","sifirdan"); ONZ=os.path.join(B_,"..","..","onizlemeler")
W,H=1920,1080; CX,CY=W/2,H/2; FPS=60
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx=xx-CX+0.5; dy=yy-CY+0.5; R=np.hypot(dx,dy); A=np.arctan2(dy,dx)
def renk(h): h=h.lstrip("#"); return np.array([int(h[i:i+2],16) for i in (0,2,4)],np.float32)/255
def ease_out(t): return 1-(1-np.clip(t,0,1))**3
def pen(t,a,b,c,d): return float(np.clip((t-a)/max(b-a,1e-6),0,1)*np.clip((d-t)/max(d-c,1e-6),0,1))
def ekle(L,m,rk,g=1.0):
    if g>0: L+=m[...,None]*rk[None,None,:]*g
def ton(L): return np.clip(1-np.exp(-L*1.5),0,1)*255            # eklemeli isik: doyunca beyaza kayar
def isin_maskesi(lst,olcek,cx=CX,cy=CY):
    m=np.zeros((H,W),np.float32); ddx=xx-cx; ddy=yy-cy; RR=np.hypot(ddx,ddy); AA=np.arctan2(ddy,ddx)
    for a,uz,en in lst:
        boy=uz*olcek; d=np.abs(np.angle(np.exp(1j*(AA-a))))*RR; w=en*olcek*(1-np.clip(RR/boy,0,1))
        m=np.maximum(m,np.clip(1-d/np.maximum(w,0.6),0,1)*(1-np.clip(RR/boy,0,1))**0.7)
    return m
def isinlar(rng,n,a,b,c,d,duzenli=False):
    a0=rng.uniform(0,2*np.pi)
    return [((a0+2*np.pi*k/n+rng.uniform(-0.12,0.12)) if duzenli else rng.uniform(0,2*np.pi),rng.uniform(a,b),rng.uniform(c,d)) for k in range(n)]
# ---------------- PEMBE PATLAMA ----------------
def yaprak_listesi(seed=11,n=14):
    rng=np.random.default_rng(seed); a0=rng.uniform(0,2*np.pi)
    return [dict(aci=a0+2*np.pi*k/n+rng.uniform(-0.2,0.2),hiz=rng.uniform(0.75,1.25),boy=rng.uniform(0.8,1.15),gec=rng.uniform(0,0.025)) for k in range(n)]
def yapraklar(L,ts,yap):
    for y in yap:
        tt=ts-y["gec"]
        if tt<0: continue
        g=pen(tt,0,0.015,0.36,0.47)
        if g<=0: continue
        s=y["hiz"]; r=150+s*1650*tt*(1-0.35*tt)                       # ~29 px/kare (60 k/sn) baslangic, hafif yavaslar
        ca,sa=np.cos(y["aci"]),np.sin(y["aci"]); px,py=CX+r*ca,CY+r*sa
        Lb=46*y["boy"]*s**0.4; Wb=Lb*0.27
        x0,x1=int(max(px-Lb-14,0)),int(min(px+Lb+14,W)); y0,y1=int(max(py-Lb-14,0)),int(min(py+Lb+14,H))
        if x0>=x1 or y0>=y1: continue
        X_=xx[y0:y1,x0:x1]-px; Y_=yy[y0:y1,x0:x1]-py; u=X_*ca+Y_*sa; w=-X_*sa+Y_*ca
        en=Wb*np.clip(1-(u/Lb)**2,0,1); gv=np.clip(1-np.abs(w)/np.maximum(en,0.3),0,1)*(np.abs(u)<Lb)
        hale=np.exp(-(w/(Wb*1.5))**2)*np.clip(1-(u/(Lb*1.3))**2,0,1)
        P=L[y0:y1,x0:x1]
        P+=gv[...,None]*renk("#E8EE9A")[None,None,:]*1.3*g; P+=(gv**2.5)[...,None]*renk("#FFFFF4")[None,None,:]*1.5*g
        P+=hale[...,None]*renk("#5E663F")[None,None,:]*0.9*g
        f=pen(tt,0,0.008,0.03,0.07)
        if f>0:
            Q=np.exp(-np.abs(X_)/2.5)*np.exp(-np.abs(Y_)/30)+np.exp(-np.abs(Y_)/2.5)*np.exp(-np.abs(X_)/30)
            P+=Q[...,None]*renk("#FFFFE8")[None,None,:]*2.2*f
GOK=[("#9FD8FF",-0.06),("#B8F080",-0.02),("#FFF080",0.02),("#F0A040",0.06),("#F05050",0.10)]   # gokkusagi: icten disa (mavi-yesil, sari, turuncu, kirmizi)
def pembe():
    n=37; yap=yaprak_listesi(); kare=[]
    rng=np.random.default_rng(3); ci=np.sort(rng.uniform(-np.pi,np.pi,120)); cg=rng.uniform(0.4,1,120)
    rg=np.random.default_rng(21); yildiz=[(a,u*(1+0.7*abs(np.cos(a))),e) for a,u,e in isinlar(rg,13,70,150,10,20,duzenli=True)]
    ka=rg.uniform(0,2*np.pi,24); dikenli=np.zeros((H,W),np.float32)
    for a_ in ka: dikenli=np.maximum(dikenli,np.exp(-(np.abs(np.angle(np.exp(1j*(A-a_))))/0.06)**2))
    yan=0.25+0.75*np.abs(np.cos(A))**1.5                             # gokkusagi agirlikla sag-sol
    # radyal isin dokusu (sabit)
    idx=np.searchsorted(ci,A).clip(1,119); d=np.minimum(np.abs(A-ci[idx-1]),np.abs(A-ci[idx]))*R
    doku=np.clip(1-d/1.8,0,1)*np.where(np.abs(A-ci[idx-1])<np.abs(A-ci[idx]),cg[idx-1],cg[idx])
    for i in range(n):
        ts=i/FPS; L=np.zeros((H,W,3),np.float32)
        Rh=133+120*ease_out(ts/0.27)
        p=pen(ts,0,0.01,0.25,0.33)                                    # pembe evre
        sb=ts/0.27                                                     # 0-1 icinde renk gecisi (erken: kahve/seftali -> doruk: mercan/pembe)
        x=R/Rh; yanc=np.abs(np.cos(A))**2
        ekle(L,np.exp(-((x-0.85)/0.38)**2),renk("#4C1535"),1.4*p)                                              # dis hale: yumusak bordo-mor sis
        ic=renk("#E8609E")[None,None,:]*(1-yanc[...,None])+renk("#F0A050")[None,None,:]*yanc[...,None]           # pembe; sag-sol seftali-turuncu
        g_ic=np.exp(-((x-0.42)/0.3)**2)*(0.5+0.7*min(sb,1))*p
        L+=g_ic[...,None]*ic*1.0
        ekle(L,np.exp(-((x-0.62)/0.14)**2)*(1-0.5*yanc),renk("#EA7A8E"),0.8*min(sb,1)*p)                      # mercan
        ekle(L,np.exp(-(x/0.2)**2),renk("#FFF8E8"),1.7*pen(ts,0,0.01,0.2,0.3))                                 # beyaz-seftali cekirdek
        ekle(L,doku*np.clip(x/0.25,0,1)*np.clip((1.1-x)/0.3,0,1),renk("#F8C0D0"),0.15*p)                       # radyal ince isinlar
        gk=pen(ts,0.17,0.22,0.27,0.34)
        yan3=0.1+0.9*np.abs(np.cos(A))**3
        for rk,o in GOK: ekle(L,np.exp(-((x-(0.98+o))/0.04)**2)*yan3,renk(rk),0.35*gk)                         # gokkusagi: soluk, yanlarda
        # pembenin kendi sari yildizi: duzensiz dikenli, yatay yayilan
        ys=pen(ts,0.27,0.29,0.32,0.38)
        if ys>0:
            m=isin_maskesi(yildiz,1.0+0.3*np.clip((ts-0.27)/0.08,0,1))
            ekle(L,m,renk("#F0EC50"),1.8*ys); ekle(L,m**3,renk("#FFFFC0"),0.8*ys)
        sh=pen(ts,0.27,0.30,0.33,0.46)
        Re=np.hypot(dx/1.8,dy)
        ekle(L,np.exp(-(Re/(60+35*dikenli))**2),renk("#ECEC60"),1.4*sh); ekle(L,np.exp(-(Re/170)**2),renk("#817025"),0.8*sh)
        # yatay isik cizgisi
        uz=(380+780*ease_out(ts/0.27)) if ts<0.27 else 1160-500*np.clip((ts-0.27)/0.33,0,1)
        gc=pen(ts,0,0.01,0.55,0.6)
        boy=np.clip(1-np.abs(dx)/(uz/2),0,1)**0.6
        sar=np.clip((ts-0.25)/0.06,0,1); cr=renk("#FDFBD4")*(1-sar)+renk("#F5F495")*sar
        ekle(L,boy*np.exp(-(dy/1.8)**2),cr,2.2*gc); ekle(L,boy*np.exp(-(dy/7)**2),renk("#E8D070"),0.7*gc)
        ekle(L,boy**2*np.exp(-(dy/22)**2),renk("#AA804A"),0.35*gc)
        yapraklar(L,ts,yap)
        kare.append(ton(L))
    return kare
# ---------------- AYRI SARI YILDIZ ----------------
def sari_yildiz():
    rng=np.random.default_rng(7); n=13; kare=[]
    buyuk=isinlar(rng,20,280,500,10,22); kucuk=isinlar(rng,14,70,170,12,26,duzenli=True)
    for i in range(n):
        ts=i/FPS; L=np.zeros((H,W,3),np.float32)
        g1=pen(ts,0,0.01,0.05,0.09)
        m=isin_maskesi(buyuk,0.9+0.2*np.clip(ts/0.08,0,1))
        ekle(L,m,renk("#F2EE6A"),1.8*g1); ekle(L,m**3,renk("#FFFFE0"),1.2*g1)
        ekle(L,np.exp(-(R/170)**2),renk("#E8E070"),1.0*g1); ekle(L,np.exp(-(R/50)**2),renk("#FFFFF2"),1.8*g1)
        g2=pen(ts,0.05,0.08,0.11,0.2)
        if g2>0:
            s=1.1-0.4*np.clip((ts-0.07)/0.13,0,1); m=isin_maskesi(kucuk,s)
            ekle(L,m,renk("#F6F2A0"),1.7*g2); ekle(L,m**2,renk("#FFFFF0"),1.1*g2)
            ekle(L,np.exp(-(R/(75*s))**2),renk("#F8F4C0"),1.3*g2); ekle(L,np.exp(-(R/(170*s))**2),renk("#C8C060"),0.4*g2)
        kare.append(ton(L))
    return kare
def yaz(ad,kare):
    od=os.path.join(K,ad); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    for j,k in enumerate(kare): Image.fromarray(k.round().astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,j)))
    pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
    src=["-framerate",str(FPS),"-i",od+"/"+ad+"_%02d.png"]
    subprocess.run(["ffmpeg","-v","error","-y"]+src+["-vf","tpad=stop=30,scale=960:-1:flags=lanczos,"+pal,"-loop","0",os.path.join(ONZ,"efekt10_sifirdan_%s.gif"%ad)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y"]+src+["-vf","tpad=stop=30","-c:v","libx264","-crf","10","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_sifirdan_%s.mp4"%ad)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","%.4f"%(len(kare)/10),"-i",od+"/"+ad+"_%02d.png","-vf","fps=30","-c:v","libx264","-crf","10","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_sifirdan_%s_yavas10.mp4"%ad)],check=True)
    print(ad,len(kare),"kare",flush=True)
if __name__=="__main__":
    import sys
    if "pembe" in sys.argv[1:] or len(sys.argv)==1: yaz("pembe",pembe())
    if "sari" in sys.argv[1:] or len(sys.argv)==1: yaz("sari_yildiz",sari_yildiz())
