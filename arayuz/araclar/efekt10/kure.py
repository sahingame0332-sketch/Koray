#!/usr/bin/env python3
"""Efekt 10 pembe patlama — doruk ani tek kare (kullanicinin tarifi + ic goruntu fotografindan olculen renkler).
Ortasi titanyum beyaz; kenari 1/3 seftali kirmizisi; 1/3 bosluk; sonra kureyi tutar gibi sag-sol kalin ( ) parantezler (sari + yesil).
Olculen (foto, merkez 638,440; olcek s ile buyutulur): beyaz cekirdek r<=72 (#FEFEFE), kenar #F8DBC3; seftali-kirmizi #D0968F/#C6887D r~140;
parantez icten disa: turuncu #F5CA7C -> sari #FEFD89 -> acik sari #FEFDB0 -> acik yesil #F5FDC0 -> yesil #CAFBBB, aci +-55 derece.
Cikti: kaynak/efekt10/kure/kure.png (siyah fon), kure_saydam.png (alfa = parlaklik), onizlemeler/efekt10_kure.png"""
import os, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure"); ONZ=os.path.join(B_,"..","..","onizlemeler")
W,H=1920,1080; s=1.6
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx=xx-W/2+0.5; dy=yy-H/2+0.5; R=np.hypot(dx,dy)/s; A=np.arctan2(dy,dx)
def rk(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],np.float32)/255
def bant(r0,w): return np.exp(-((R-r0)/w)**2)
C=np.zeros((H,W,3),np.float32)
def kat(m,c,a=1.0):   # "uzerine" katman (renk m alfa ile)
    global C; m=np.clip(m*a,0,1)[...,None]; C=C*(1-m)+rk(c)*m
# radyal renk gecisi (yumusak, cizgisiz): titanyum beyaz -> seftali -> seftali kirmizisi -> saydam
dur=[(0,"#FFFFFF",1.0),(70,"#FEFEFE",1.0),(92,"#F8DBC3",1.0),(118,"#E1A59F",0.97),(140,"#C98A80",0.9),(158,"#B07872",0.6),(178,"#6A4844",0.15),(195,"#000000",0.0)]
rr=np.array([d[0] for d in dur],np.float32)
for c in range(3):
    C[...,c]=np.interp(R,rr,[rk(d[1])[c]*d[2] for d in dur])
# parantezler: kureye esmerkezli kalin yaylar (sag-sol), uclara dogru incelir ve solar
yan=np.abs(np.cos(A)); aci=np.degrees(np.arccos(np.clip(yan,0,1)))
uc=np.clip((62-aci)/18,0,1)**1.2
mrk=236; yar=34*np.clip(1-(aci/80)**2,0.45,1)
u=(R-(mrk-yar))/(2*yar)
renkler=[(0.0,"#F2B860"),(0.18,"#FCE870"),(0.45,"#FEFA9A"),(0.7,"#D8F6A8"),(1.0,"#A8E8B0")]   # ic: turuncu-sari -> sari -> acik yesil -> yesil (dis)
uu=np.clip(u,0,1); col=np.stack([np.interp(uu,[q[0] for q in renkler],[rk(q[1])[c] for q in renkler]) for c in range(3)],-1)
op=np.clip(np.minimum(u,1-u)/0.12,0,1)*uc*0.92                            # yumusak kenar, hafif saydam
C=C*(1-op[...,None])+col*op[...,None]
dis=np.exp(-((R-(mrk+yar+8))/12)**2)*uc*0.45                              # dis zeytin-yesil hale
C=C+(rk("#55703A")*dis[...,None])
os.makedirs(K,exist_ok=True)
img=(np.clip(C,0,1)*255).round().astype(np.uint8)
Image.fromarray(img).save(os.path.join(K,"kure.png"))
a=img.max(2); rgb=np.where(a[...,None]>0,(img.astype(np.float32)*255/np.maximum(a,1)[...,None]).clip(0,255),0).astype(np.uint8)
Image.fromarray(np.dstack([rgb,a])).save(os.path.join(K,"kure_saydam.png"))
# onizleme: fotograf (kirpilmis) | yeni
ref=Image.open(os.path.join(os.path.expanduser("~"),".claude","uploads","7667fcb8-b488-59d0-b1d8-f55ffb36b68a","0d1e98a9-image.jpg")).convert("RGB").crop((638-420,440-330,638+420,440+330)).resize((960,754))
new=Image.fromarray(img).crop((960-672,540-528,960+672,540+528)).resize((960,754))
o=Image.new("RGB",(1920,754)); o.paste(ref,(0,0)); o.paste(new,(960,0)); o.save(os.path.join(ONZ,"efekt10_kure.png"))
print("tamam")
