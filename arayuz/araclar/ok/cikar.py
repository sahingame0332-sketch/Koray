#!/usr/bin/env python3
"""Shadow Hunter oku: gorsel + ucus olcumu. Kaynak: kullanicinin telefon kaydi (2712x1220) -> 60 kare/sn kareler (depoya konmaz).
1) Ok gorseli (kare 97, karakterin hemen onunde, en buyuk ve net hali): zemin = 94..124 medyani (ok her pikselde kisa kalir).
   Alfa: artis yonunun ok rengine (krem) izdusumu  a = <O-B, C-B> / |C-B|^2 ; renk = B + (O-B)/a.  Sonra ok yatay (uc saga) dondurulur.
2) Ucus: uc noktasi kare kare (izle.py ile ayni) -> sure, ekran yolu, yay (dogrudan sapma).
Kullanim: cikar.py KARE_KLASORU"""
import os, sys, glob, json, math, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(B_,"..","..","kaynak","ok"); os.makedirs(OUT,exist_ok=True)
fs=sorted(glob.glob(sys.argv[1]+'/k_*.png'))
Y=lambda i: np.asarray(Image.open(fs[i]).convert('RGB')).astype(np.float32)
X0,Y0,X1,Y1=1095,535,1310,620
B=np.median(np.stack([Y(i)[Y0:Y1,X0:X1] for i in list(range(102,124))]),0)    # ok bu bolgeden gecmis (97-101 haric)
O=Y(97)[Y0:Y1,X0:X1]
C=np.array([238.,232.,196.])                                       # ok/iz rengi (olculen: bas 230,224,196; iz 236,230,160)
V=C-B; D=O-B
a=np.clip((D*V).sum(2)/np.maximum((V*V).sum(2),400),0,1)
# ok basinin golgeli (koyu, zeytin-gri) yuzu krem yonune izdusmez: genel farkla da opaklik ver (bas opak bir nesne)
# ucgen bas: kremi net piksellerin (x < 1180) dis bukey zarfi -> opak (alfa 1, renk orijinal). Golgeli taban dahil.
from PIL import ImageDraw
ys_,xs_=np.nonzero((a>0.35)&(np.arange(a.shape[1])[None,:]<1180-X0))
def zarf(p):
    p=sorted(set(map(tuple,p)))
    def cr(o,a_,b_): return (a_[0]-o[0])*(b_[1]-o[1])-(a_[1]-o[1])*(b_[0]-o[0])
    lo=[];up=[]
    for q in p:
        while len(lo)>=2 and cr(lo[-2],lo[-1],q)<=0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up)>=2 and cr(up[-2],up[-1],q)<=0: up.pop()
        up.append(q)
    return lo[:-1]+up[:-1]
zm=Image.new("L",(a.shape[1]*4,a.shape[0]*4),0); ImageDraw.Draw(zm).polygon([(x*4+2,y*4+2) for x,y in zarf(np.c_[xs_,ys_])],fill=255)
bas=np.asarray(zm.resize((a.shape[1],a.shape[0]),Image.LANCZOS)).astype(float)/255
a=np.maximum(a,bas)
a=np.where(a>0.06,a,0); a=ndimage.median_filter(a,3)
a[:,1285-X0:]=0                                                        # sagda karakterin yayi/eli
# yalniz okun bileseni (yay/el ve uzak gurultu disari)
lab,n=ndimage.label(ndimage.binary_dilation(a>0.2,np.ones((5,5)))); s=ndimage.sum(a>0.2,lab,range(1,n+1)); ana=lab==(1+np.argmax(s))
a=a*ndimage.binary_dilation(ana,np.ones((5,5)))
renk=np.clip(B+D/np.maximum(a[...,None],1e-3),0,255); renk=np.where(a[...,None]>0.02,renk,C)
renk=np.where((bas>0.5)[...,None],O,renk)                              # opak basta renk = orijinal
spr=np.dstack([renk,a*255])
# yon: uc (1174,569) -> kuyruk; ok sola-yukari gidiyor. Yatay, uc saga olacak sekilde dondur.
uc=np.array([1130.,557.]); kuy=np.array([1254.,588.]); d=uc-kuy; aci=math.degrees(math.atan2(d[1],d[0]))   # gorsel uc (ucgen basin ucu) ve iz sonu
im=Image.fromarray(spr.astype(np.uint8),"RGBA").rotate(aci,resample=Image.BICUBIC,expand=True)   # PIL: saat yonu tersi; y asagi
im=im.rotate(180,expand=True) if False else im
A=np.asarray(im); ys,xs=np.nonzero(A[...,3]>8); im=im.crop((xs.min()-2,ys.min()-2,xs.max()+3,ys.max()+3))
# uc saga bakmali: en parlak/genis bas sag yarida mi?
A=np.asarray(im).astype(float); w=A.shape[1]
gen=(A[...,3]>60).sum(0)                                              # sutun basina kalinlik: bas (ucgen) en kalin
if gen[:w//3].max()>gen[-w//3:].max(): im=im.transpose(Image.FLIP_LEFT_RIGHT)   # bas saga
im.save(os.path.join(OUT,"ok.png")); print("ok sprite",im.size,"aci %.1f"%aci)
# ucus
yol={95:(1249,590),97:(1174,569),99:(1039,529),100:(977,512),104:(869,484),105:(774,460),106:(725,449),108:(680,439),109:(640,431),
     110:(598,423),111:(565,417),113:(530,411),114:(487,404)}
P=np.array(list(yol.values()),float); t=(np.array(list(yol))-94)/60.0
p0=np.array([1290.,598.]); p1=np.array([250.,350.])               # cikis (yay eli) ve vurus (patlama merkezi, kare 123)
ch=p1-p0; L=np.linalg.norm(ch); nrm=np.array([ch[1],-ch[0]])/L
sapma=[float((p-p0)@nrm) for p in P]
json.dump(dict(fps_kayit=60,cikis_karesi=94,vurus_karesi=123,ucus_suresi_sn=round((123-94)/60,3),cikis_ekran=p0.tolist(),vurus_ekran=p1.tolist(),
               uc_yolu={str(k):v for k,v in yol.items()},dogrudan_sapma_px=[round(s,1) for s in sapma],en_cok_yay_px=round(max(sapma),1),
               kiris_px=round(float(L),1),yay_orani=round(max(sapma)/L,4),karakter_boyu_px=300,ok_ekran_uzunlugu_kare97=80),
          open(os.path.join(OUT,"olculer.json"),"w"),indent=1)
print("sure %.3f sn, kiris %.0f px, yay %.1f px (%.2f%%)"%((123-94)/60,L,max(sapma),100*max(sapma)/L))
