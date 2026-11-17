#!/usr/bin/env python3
"""Efekt 9: kayit 20-27-52 (tablet 2266x1488, 60 -> 30 kare/sn, gercek hiz). Iki efekt:
 "skill": Gloomwing'e vurus — kesik + havada pembe patlama + gokten kirmizi isin + yerde pembe halka + yatay sari parlama + sari yildiz
          (kareler 66-91; kamera sabit). Mob zemini = secim halkasi merkezi (522,812).
 "altin": oyuncunun ustunde altin-turuncu patlama (kareler 19-28) — oyuncuya bagli (ayak 1130,1020 civari; olculur).
E = clip(min(O - Bonce, O - Bsonra)): hareket eden mob/oyuncu, sonradan dusen sandik, isim etiketleri duser. Yesil artis (oyuncu teni,
yon oku) ve kararan pikseller komsu isiktan doldurulur. Doyan cekirdekte isigin kendi rengi. HUD (alt/ust/sag) disarida.
Kullanim: cikar9.py KLASOR   (KLASOR/k_%04d.png 30 kare/sn; kayit depoya konmaz)"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt9")
KX,KY,KX1,KY1=0,140,1700,1330
EFEKT={"skill":dict(aralik=range(66,92),once=range(56,66),sonra=range(92,100),capa=(522,812),capa_ad="mob_zemini",boy=None),
       "altin":dict(aralik=range(19,29),once=range(14,19),sonra=range(30,37),capa=(1130,1020),capa_ad="oyuncu_ayagi",boy=290,merkez=(1135,880),yaricap=330,gri_ust=60,oyuncu_temizle=False)}
def temizle(E,esik=8):
    mx=E.max(2); tut=ndimage.binary_opening(mx>esik,np.ones((2,2)))|(mx>90)
    l,n=ndimage.label(tut)
    if n: s=ndimage.sum(mx>esik,l,range(1,n+1)); tut=np.isin(l,1+np.where(s>=40)[0])            # kumlanma (tek tuk noktalar) atilir
    return ndimage.gaussian_filter(np.where(tut[...,None],E,0),[0.6,0.6,0])
def calis(k,secim=None):
    fs=sorted(glob.glob(os.path.join(k,"k_*.png")))
    Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)[KY:KY1,KX:KX1]
    bilgi=json.load(open(os.path.join(OUT,"bilgi.json"))) if os.path.exists(os.path.join(OUT,"bilgi.json")) else {}
    for ad,c in EFEKT.items():
        if secim and ad not in secim: continue
        Bo=np.median([Y(i) for i in c["once"]],0); Bs=np.median([Y(i) for i in c["sonra"]],0)
        K=[]
        for i in c["aralik"]:
            O=Y(i); D=np.minimum(O-Bo,O-Bs); Dx=np.maximum(O-Bo,O-Bs)
            # guclu renkli isik: zeminlerden biri (mob/oyuncu eski yeri) isigin altinda kaliyorsa ona uyan zemin (max) kullanilir
            dmx=Dx.max(2); renkli=((Dx.max(2)-Dx.min(2))>35)|(O.max(2)>228)
            guclu=ndimage.binary_opening((dmx>60)&renkli&(D.max(2)>40),np.ones((3,3)))   # iki zemine gore de isik eklenmis olmali (secim halkasi gibi sabit nesne degil)
            D=np.where(guclu[...,None],Dx,D)
            # kayit en parlak yerde 246'da doyuyor: doyan cekirdekte isigin kendi rengi
            w8=(np.clip((O.max(2)-240)/6.0,0,1)*(D.max(2)>60))[...,None]                  # yalniz gercek doyma (kayitta 246)
            E=np.clip(w8*O+(1-w8)*D,0,255)
            Dp=np.clip(D,0,None); yesil=(Dp[...,1]>Dp[...,0]*1.3)&(Dp[...,1]>Dp[...,2]*1.6)
            E=E*(np.clip((Dp.max(2)-7)/10,0,1)*~yesil)[...,None]                               # sonuk dis hale de kalsin
            # renksiz (gri/lavanta) artis = hareket eden mob/oyuncu govdesi; saf kirmizi = mob hasar boyamasi (ayri paket)
            dmx=np.maximum(Dp.max(2),1); sat=(Dp.max(2)-Dp.min(2))/dmx
            ust_gri=c.get("gri_ust",185)                                               # altin patlamanin beyaz cekirdegi renksiz: orada yalniz sonuk gri atilir
            govde_rengi=(O[...,2]>=0.85*O[...,1])&(np.abs(O[...,0]-O[...,1])<25)               # gri/lavanta govde (isik sarimsi: B << G)
            gri=(sat<0.28)&(Dp.max(2)>15)&(Dp.max(2)<ust_gri)&(O.max(2)<235)&govde_rengi
            kirmizi=np.zeros_like(Dp[...,0],bool) if True else (Dp[...,0]>25)&(Dp[...,0]>2.0*Dp[...,1]+12)&(Dp[...,0]>2.0*Dp[...,2]+12)&(O.max(2)<240)
            oy=np.zeros_like(gri); oy[650-KY:1080-KY,980:1340]=True                       # oyuncu govdesi bolgesi: parlak beyaz zirh da
            if c.get("oyuncu_temizle",True):
                sari_k=(np.minimum(Dp[...,0],Dp[...,1])>1.5*Dp[...,2]+8)
                gri|=oy&(Dp.max(2)>15)&~sari_k
            E=E*(~(gri|kirmizi))[...,None]
            lab=lambda X: ((X[...,0]>170)&(X[...,1]<110)&(X[...,2]<120))|((X[...,2]>190)&(X[...,1]>170)&(X[...,0]<140))
            yakin_lab=ndimage.binary_dilation(lab(Bo)|lab(Bs),np.ones((41,41)))                 # etiketler zeminde de var (yazi yerinde)
            etiket=lab(O)&yakin_lab                                                              # turuncu-kirmizi efekt halkasi etiket sayilmaz
            etiket=ndimage.binary_dilation(ndimage.binary_closing(etiket,np.ones((5,9))),np.ones((7,7)))     # ad etiketleri (kirmizi/camgobegi + siyah kenar)
            yab=(np.minimum(O-Bo,O-Bs).min(2)<-25)|ndimage.binary_dilation(gri|kirmizi,np.ones((3,3)))|etiket
            m=ndimage.binary_dilation(yab|ndimage.binary_dilation(yesil&(Dp.max(2)>20),np.ones((3,3))),np.ones((5,5)))&(w8[...,0]<0.3)
            E=yumusak_doldur(E,m,n=10,k=11)
            # fizik siniri: isik, orijinalde gorulen artistan fazla olamaz (dolgu komsudan parlaklik tasimasin); yalniz ad etiketlerinin alti serbest
            sinir=np.clip(D,0,255)+4
            E=np.where(etiket[...,None],E,np.minimum(E,sinir))
            E[:245-KY,:300]=0                                                       # sol ust HUD (oyuncu bilgisi); isin bundan sagda/asagida
            if c.get("yaricap"):                                                     # efekt disi (baska yaratik) yumusak kesilir
                yy,xx=np.mgrid[0:E.shape[0],0:E.shape[1]]; r=np.hypot(xx+KX-c["merkez"][0],(yy+KY-c["merkez"][1])*1.1)
                E=E*np.clip((c["yaricap"]-r)/60,0,1)[...,None]
            K.append(temizle(E))
        K=np.stack(K); mx=K.max(3).max(0); ys,xs=np.nonzero(mx>8)
        x0,y0,x1,y1=max(0,xs.min()-6),max(0,ys.min()-6),min(K.shape[2],xs.max()+7),min(K.shape[1],ys.max()+7)
        od=os.path.join(OUT,ad); os.makedirs(od,exist_ok=True)
        for f in os.listdir(od): os.remove(os.path.join(od,f))
        for n,E in enumerate(K): Image.fromarray(np.clip(E[y0:y1,x0:x1],0,255).round().astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,n)))
        X,Yy,W,H=KX+x0,KY+y0,x1-x0,y1-y0; ca=c["capa"]
        bilgi[ad]=dict(kaynak_kareler=[c["aralik"][0],c["aralik"][-1]+1],kare=len(K),fps=30.0,kutu_ekran=[int(X),int(Yy),int(W),int(H)],
                       capa=c["capa_ad"],capa_ekran=list(ca),pivot=[round((ca[0]-X)/W,4),round(1-(ca[1]-Yy)/H,4)],en_boy=round(H/W,4),
                       oyuncu_boyu_px=290)
        np.save(os.path.join(OUT,"zemin_%s.npy"%ad),Bo.astype(np.uint8))
        print(ad,bilgi[ad])
    json.dump(bilgi,open(os.path.join(OUT,"bilgi.json"),"w"),indent=1)
if __name__=="__main__": os.makedirs(OUT,exist_ok=True); calis(sys.argv[1],sys.argv[2:])
