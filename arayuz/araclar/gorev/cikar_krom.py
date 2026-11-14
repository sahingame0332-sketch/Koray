#!/usr/bin/env python3
"""QuestList ve gorev detayi pencereleri: ham krom (genie/cikar_pencere.py yontemi).
Arka plan (q_open: ayni sahne, pencere yok) -> pencereden gecen isik  b = k*(a/255)^1.8  (genie ile ayni dogrusal olmayan
iliski; k pencere basina olculur). R = O - b ; krom siyaha karsi cozulur. Kutu disi (tasan susler, X): fark maskesi."""
from ortak import *
from scipy import ndimage
B=Y("q_open")
PENCERE=dict(liste=dict(kare="q_liste",sprite=(1040,372,1682,842),zemin=(1056,388,1622,829)),
             detay=dict(kare="q_detay",sprite=(1052,172,1648,1012),zemin=(1070,187,1629,998)))
def k_olc(O,Bk,z):
    x0,y0,x1,y1=z; a=Bk[y0:y1,x0:x1].reshape(-1,3); b=O[y0:y1,x0:x1].reshape(-1,3)
    m=(a>60)&(b<0.35*a)&(b>=2); r=b[m]/((a[m]/255.0)**1.8)      # JPEG sifirlari haric
    return float(np.median(r)), float(np.percentile(r,25))
bilgi={}
for ad,p in PENCERE.items():
    O=Y(p["kare"]); k,k25=k_olc(O,B,p["zemin"])
    sx0,sy0,sx1,sy1=p["sprite"]; o=O[sy0:sy1,sx0:sx1]; b=B[sy0:sy1,sx0:sx1]
    R=np.clip(o-k*(b/255.0)**1.8,0,255); T,t0=60.0,6.0
    al=np.clip((R.max(2)-t0)/(T-t0),0,1)
    rgb=np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0)
    # opak krom (baslik tasi, dugmeler, cerceve): arkadaki sahne katkisi yok -> renk dogrudan orijinal
    #   (cikarma, arkadaki ad etiketlerinin negatif hayaletini birakiyordu)
    opk=ndimage.binary_erosion(al>=0.97,np.ones((3,3)))
    rgb=np.where(opk[...,None],o,rgb)
    ic=np.zeros(al.shape,bool); zx0,zy0,zx1,zy1=p["zemin"]; ic[zy0-sy0:zy1-sy0,zx0-sx0:zx1-sx0]=True
    d=np.abs(o-b).max(2); da=np.clip((d-10)/25.0,0,1)
    al=np.where(ic,al,da); rgb=np.where(ic[...,None],rgb,o)
    yaz("_ham_"+ad,np.dstack([rgb,al*255]))
    # orta tonda (a=60..110) gecen oran -> Unity siyah zemin alfasi
    oran=k*(np.arange(60,111)/255.0)**1.8/np.arange(60,111)
    bilgi[ad]=dict(k=round(float(k),1),k_p25=round(float(k25),1),alfa=round(float(1-oran.mean()),3),sprite=p["sprite"],zemin=p["zemin"])
    print(ad,bilgi[ad])
json.dump(bilgi,open(os.path.join(OUT,"..","krom_olculer.json"),"w"),indent=1)
