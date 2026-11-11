#!/usr/bin/env python3
"""OLYMPOS-KO zemin dokulari + renk olcumu (ekran goruntulerinden).

1) Zemin duzlemi yukaridan gorunuse cevrilir (duzelt.py; kamera: dusey gorus acisi 60 derece,
   ufuk satiri sahne basina olculdu).
2) En yuksek cozunurluklu temiz bolgeden N x N karo kesilir; kenarlar, karonun hemen disindaki
   GERCEK devam pikselleriyle b piksellik bantta harmanlanir -> ek yeri gorunmeden doser.
3) Buyuk olcekli parlaklik/renk dalgasi (renk haritasi) dokudan ayrilir:  doku = karo / alcak_geciren * ortalama.
4) Renk: ortalama sRGB, Lab, doygunluk, ilintili renk sicakligi (McCamy).
"""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
from duzelt import *
B=os.path.dirname(os.path.abspath(__file__)); REF=os.path.join(B,"..","..","referans_gorseller")
OUT=os.path.join(B,"..","..","kaynak","zemin")
FOV=60.0
ORAN=0.80          # karo, sigan en buyuk karenin bu kadarini kaplar (kameraya yakin = net taraf)
def odak(H): return H/2/np.tan(np.radians(FOV/2))

# ad: (kare, ufuk_y, temiz zemin kutusu (goruntu), dislanan kutular, ppu, N)
# ad: (kare, ufuk_y, temiz zemin kutusu (goruntu), dislanan goruntu kutulari, kaba ppu, N, serit)
# serit: duzeltilmis gorunuste (kaba ppu'da) sutun araligi -> yol boyunca uzanan doku seridini secer (yoksa None)
ZEMINLER={
 "kum":        ("hud_ekranlar/hud_01.png", 232, (0,560,1560,912),  [(1020,630,1250,870),(1160,640,1560,840),(0,560,300,700)], 128, 256, None),
 "tas_doseme": ("hud_ekranlar/hud_04.png", 470, (60,650,1040,915), [], 96, 256, (0,348)),
 "tas_tugla":  ("hud_ekranlar/hud_04.png", 470, (60,650,1040,915), [], 96, 128, (364,444)),
 "tas_arnavut":("hud_ekranlar/hud_03.png", 480, (330,690,1012,915),[], 96, 128, (206,328)),
 "cim":        ("oyun_ici/v2_hedef.jpg",   150, (200,620,1250,1060),[], 128, 256, None),
}
# karakter boyu, o sahnenin biriminde (kamera yuksekligi = 1): ekrandaki boydan hesaplandi
KARAKTER={"kum":0.206,"tas_doseme":0.271,"tas_tugla":0.271,"tas_arnavut":0.294,"cim":0.191}
# gok ve gorus mesafesi sonundaki duz renk (medyan piksel). Zeminde mesafeyle solma OLCULMEDI:
# Moradon yolunda y=550..640 satir ortalamalari sabit (125,120,99) -> kademeli sis yok.
ORTAM={
 "moradon": dict(gok="#ADC6D6", uzak="#D0EA84", kaynak="hud_03 (1100,330)-(1230,370) / (1090,508)-(1230,516)"),
 "kale":    dict(gok="#AEC7D7", uzak="#C0D47E", kaynak="hud_02 (480,405)-(590,440) / (470,474)-(600,478)"),
 "kir":     dict(gok="#BFCDDB", uzak="#B2C7D4", kaynak="v2_hedef (700,5)-(1050,40) / (700,120)-(1100,134)"),
}
def srgb2lin(c): c=c/255.0; return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def renk_olc(rgb):
    lin=srgb2lin(np.asarray(rgb,float))
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X,Y,Z=M@lin; x,y=X/(X+Y+Z),Y/(X+Y+Z)
    n=(x-0.3320)/(0.1858-y); cct=449*n**3+3525*n**2+6823.3*n+5520.33
    def f(t): return np.where(t>0.008856,np.cbrt(t),7.787*t+16/116)
    fx,fy,fz=f(X/0.95047),f(Y),f(Z/1.08883); L=116*fy-16; a=500*(fx-fy); b=200*(fy-fz)
    mx,mn=max(rgb),min(rgb)
    return dict(srgb=[int(round(v)) for v in rgb], hex="#%02X%02X%02X"%tuple(int(round(v)) for v in rgb),
                xy=[round(float(x),4),round(float(y),4)], cct_K=int(round(float(cct))), Lab=[round(float(L),1),round(float(a),1),round(float(b),1)],
                doygunluk=round((mx-mn)/mx,3), parlaklik_Y=round(float(Y),3))
def duz_alan(img,yh,alan,dis,ppu,xbant=None):
    H,W=img.shape[:2]; f=odak(H); cx,cy=W/2,H/2; phi=np.arctan((H/2-yh)/f)
    x0,y0,x1,y1=alan
    X,Z=geri(np.array([x0,x1,x0,x1],float),np.array([y0,y0,y1,y1],float),f,phi,cx,cy)
    X0,X1,Z0,Z1=X.min(),X.max(),Z.min(),Z.max()
    a,ok=duzelt(img,f,phi,X0,X1,Z0,Z1,ppu)
    nz,nx=a.shape[:2]
    XX,ZZ=np.meshgrid(X0+(np.arange(nx)+0.5)/ppu,Z1-(np.arange(nz)+0.5)/ppu)
    px,py=izdusum(XX,ZZ,f,phi,cx,cy)
    m=ok&(px>=x0)&(px<=x1)&(py>=y0)&(py<=y1)
    for (a0,b0,a1,b1) in dis: m&=~((px>=a0)&(px<=a1)&(py>=b0)&(py<=b1))
    if xbant is not None: m&=(XX>=xbant[0])&(XX<=xbant[1])
    return a,m,dict(f=f,phi=float(np.degrees(phi)),X0=float(X0),Z1=float(Z1),Z0=float(Z0))
def en_iyi_pencere(m,n):
    """tamami maske icinde kalan n x n pencerelerden en alttaki (kameraya en yakin = en net)"""
    ii=np.pad(m.astype(np.int64),((1,0),(1,0))).cumsum(0).cumsum(1)
    s=ii[n:,n:]-ii[:-n,n:]-ii[n:,:-n]+ii[:-n,:-n]
    ok=np.argwhere(s==n*n)
    if len(ok)==0: return None
    y=ok[:,0].max(); xs=ok[ok[:,0]==y][:,1]
    return int(xs[len(xs)//2]),int(y)
def doser_yap(P,N,b):
    """P: (N+b) x (N+b) yama -> N x N; sol/ust bant, sag/alt kenarin gercek devamiyla harmanlanir."""
    T=P[:N,:N].copy(); w=((np.arange(b)+0.5)/b)
    w=w*w*(3-2*w)
    T[:,:b]=P[:N,N:N+b]*(1-w)[None,:,None]+T[:,:b]*w[None,:,None]
    alt=P[N:N+b,:N].copy()
    alt[:,:b]=P[N:N+b,N:N+b]*(1-w)[None,:,None]+alt[:,:b]*w[None,:,None]
    T[:b,:]=alt*(1-w)[:,None,None]+T[:b,:]*w[:,None,None]
    return T
def calis():
    os.makedirs(os.path.join(OUT,"dokular"),exist_ok=True); rapor={}
    for ad,(kare,yh,alan,dis,ppu,N,serit) in ZEMINLER.items():
        img=yukle(os.path.join(REF,kare))
        a,m,k=duz_alan(img,yh,alan,dis,ppu)
        xb=None
        if serit is not None:
            xb=(k["X0"]+serit[0]/ppu,k["X0"]+serit[1]/ppu); a,m,k=duz_alan(img,yh,alan,dis,ppu,xb)
        Image.fromarray(np.clip(a*m[...,None],0,255).astype(np.uint8)).save(os.path.join(OUT,"duz_%s.png"%ad))
        genel=a[m].mean(0); genel_std=a[m].std(0)
        b=N//8
        # sigan en buyuk kare (birim) -> karo, onun %ORAN'ini kaplasin; ppu buna gore yeniden secilir
        lo,hi=8,min(m.shape)
        while lo<hi:
            mid=(lo+hi+1)//2
            if en_iyi_pencere(m,mid) is not None: lo=mid
            else: hi=mid-1
        kenar=ORAN*lo/ppu; ppu=(N+b)/kenar
        a,m,k=duz_alan(img,yh,alan,dis,ppu,xb)
        p=en_iyi_pencere(m,N+b)
        if p is None: print(ad,"pencere bulunamadi",a.shape,m.sum()); continue
        x,y=p; P=a[y:y+N+b,x:x+N+b]
        alc=ndimage.gaussian_filter(P,[N/5.0,N/5.0,0],mode="reflect")
        ort=P.reshape(-1,3).mean(0)
        duzP=np.clip(P/np.maximum(alc,1)*ort,0,255)
        T=doser_yap(duzP,N,b)
        Image.fromarray(T.astype(np.uint8)).save(os.path.join(OUT,"dokular","zemin_%s.png"%ad))
        r=renk_olc(genel); r.update(karo_px=N,karo_birim=round(N/ppu,3),ppu=round(ppu,1),ufuk_y=yh,odak_px=round(k["f"],1),
                                           kamera_egimi_derece=round(k["phi"],1),std=[round(float(v),1) for v in genel_std],
                                           kaynak=kare,pencere=[x,y],karakter_birim=KARAKTER[ad],
                                           karo_karakter_boyu=round(N/ppu/KARAKTER[ad],2))
        rapor[ad]=r
        print("%-10s %s  CCT %5d K  Lab %s  doyg %.2f  karo %d px = %.2f birim  (duz %dx%d, pencere %d,%d)"%(
            ad,r["hex"],r["cct_K"],r["Lab"],r["doygunluk"],N,N/ppu,a.shape[1],a.shape[0],x,y))
    for o in ORTAM.values():
        for k in ("gok","uzak"):
            h=o[k]; o[k+"_olcum"]=renk_olc([int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)])
    rapor["_ortam"]=ORTAM
    json.dump(rapor,open(os.path.join(OUT,"zemin_olcumleri.json"),"w"),indent=1,ensure_ascii=False)
    return rapor
if __name__=="__main__": calis()
