#!/usr/bin/env python3
"""NPC ustundeki "?" gorev rozeti — kaynak q_once (rozet merdivenin ustunde; sag alti duvarin ARKASINDA -> dunyada, derinlikli).
Karisim olcumu: basamak seritlerinin (dikey yuksek geciren) sapmasi rozet icinde azaliyor ->
  gecirgenlik t(r) = std_ic / std_dis  (merkez 0.55, hale 0.30, r>=185 ~1).  Merkezde isik zemine EKLENIYOR (renk 255'e
  dayaniyor ama seritler kaybolmuyor), kenarda ortuyor -> ikisini birden tasiyan ON-CARPIMLI (premultiplied) karisim:
  O = t*Bg + C ;  C(r) = medyan(O) - t*medyan(Bg)  (Unity: Blend One OneMinusSrcAlpha, rgb=C, a=1-t).
"?" harfi (koyu dis hatli) ve parilti yildizlari orijinal piksellerden, ayni dokuya on-carpimli eklenir.
Cikti: soru_rozeti.png (RGB = C on-carpimli, A = 1-t), 350x350, merkez (175,175)."""
from ortak import *
O=Y("q_once"); CX,CY,R=985,175,175                     # R=CY: ust kenar ekranin ustu
L=O.mean(2); hp=L-ndimage.uniform_filter1d(L,9,axis=0)
YY,XX=np.mgrid[0:O.shape[0],0:O.shape[1]]; RR=np.hypot(XX-CX,YY-CY)
duvar=XX>(1135-(YY-80)*0.33)
sari=(O[:,:,0]>175)&(O[:,:,1]>115)&(O[:,:,1]>O[:,:,2]+45)&(XX>=912)&(XX<=1052)&(YY>=90)&(YY<=262)
sari=ndimage.binary_opening(sari,np.ones((3,3)))
_l,_n=ndimage.label(sari); _b=ndimage.sum(sari,_l,range(1,_n+1)); sari=np.isin(_l,1+np.where(_b>=150)[0])   # yildiz kirintilari degil
harf=ndimage.binary_dilation(sari,np.ones((25,25)))
yildiz=ndimage.binary_dilation((O.min(2)>175)&(RR<R)&(YY>=95)&(O[:,:,2]<O[:,:,0]+10),np.ones((9,9)))   # ust bina/gokyuzu degil
ok=~duvar&(YY>=100)&(YY<=CY+R)&~harf&~yildiz&(O.max(2)<250)
dis=(XX>=700)&(XX<=800)&(YY>=100)&(YY<=335)
ref=np.std(hp[dis]); Bm=np.median(O[dis],0)
rb=np.arange(25,R+1,5.0); t=[];C=[];gec=[]
for b in rb:
    m=ok&(RR>=b-5)&(RR<b+5)
    if m.sum()<40: t.append(np.nan); C.append([np.nan]*3); continue
    tt=min(1.0,np.std(hp[m])/ref); t.append(tt); C.append(np.clip(np.median(O[m],0)-tt*Bm,0,255))
t=np.array(t); C=np.array(C,float)
ilk=np.where(~np.isnan(t))[0][0]; t[:ilk]=t[ilk]; C[:ilk]=C[ilk]        # harfin altindaki en ic halkalar: ilk olculen deger
t=ndimage.uniform_filter1d(t,3); C=ndimage.uniform_filter1d(C,3,axis=0)
t[-3:]=np.maximum(t[-3:],[0.9,0.95,1.0]); C[-3:]*=np.array([0.5,0.25,0.0])[:,None]
H=W=2*R; yy,xx=np.mgrid[0:H,0:W]; rr=np.hypot(xx-R+0.5,yy-R+0.5)
a=1-np.interp(rr,rb,t,left=t[0],right=1.0)
Cg=np.stack([np.interp(rr,rb,C[:,k],left=C[0,k],right=0) for k in range(3)],-1)
# gorunen bolgeden harf + yildiz
P=O[CY-R:CY+R,CX-R:CX+R]; X=xx+CX-R; Yy=yy+CY-R
D=np.clip((1-a[...,None])*Bm+Cg,0,255)
sr=sari[CY-R:CY+R,CX-R:CX+R]
yl=yildiz[CY-R:CY+R,CX-R:CX+R]&~duvar[CY-R:CY+R,CX-R:CX+R]&~ndimage.binary_dilation(sr,np.ones((9,9)))
Ey=np.where(yl[...,None],np.clip(P-D,0,255),0)
# dis hat: sari govdeden uzakliga gore OLCULEN koyuluk profili (cevre boyunca medyan) -> kesintisiz yumusak golge
dist=ndimage.distance_transform_edt(~sr)
kd=np.clip((D.mean(2)-P.mean(2))/np.maximum(D.mean(2),1),0,1)       # 1 = tam siyah
dprof=[np.percentile(kd[(dist>=d-0.5)&(dist<d+0.5)],80) for d in range(1,13)]   # seritlerin acik yarisi golgeyi gizliyor -> ust %20
# kd 'koyuluk' (1-P/D) ust %20 ile bile seritlerle karisik; golge katmaninin alfasi a ve rengi g icin  P = (1-a)D + a*g
# en koyu kesitte (x 970, y 150: P~(77,40,21), D~(200,90,60)) g~(45,22,12) varsayilip a = kd/(1-g/D) ~ kd*1.3
golge=np.clip(np.interp(dist,np.arange(1,13),dprof,right=0)*1.3,0,1)*(dist>0)
grenk=np.median(P[(dist>=1)&(dist<4)],0)*0                           # golge rengi siyaha yakin (olculen ~koyu kahve)
grenk=np.array([45.,22.,12.])   # golge cekirdegi: en koyu kesitlerden (x 970/y 150 cevresi) ~koyu kahve
la=np.where(sr,1.0,golge); la=ndimage.gaussian_filter(la,0.6)
P=np.where(sr[...,None],P,grenk)                                     # golge pikselleri: olculen golge rengi
print("golge profili",np.round(dprof,2),"renk",np.round(grenk))
Ctot=la[...,None]*P+(1-la[...,None])*Cg+Ey
Atot=la+(1-la)*a
yaz("soru_rozeti",np.dstack([np.clip(Ctot,0,255),Atot*255]))
json.dump(dict(kaynak="q_once",merkez=[CX,CY],boyut=H,karisim="premultiplied: Blend One OneMinusSrcAlpha",
               r=rb.tolist(),gecirgenlik=np.round(t,3).tolist(),C=np.round(C,1).tolist(),zemin_medyan=np.round(Bm,1).tolist()),
          open(os.path.join(OUT,"..","rozet_olculer.json"),"w"),indent=0)
for i in range(0,len(rb),3): print("r %3d t %.2f C %s"%(rb[i],t[i],np.round(C[i])))
