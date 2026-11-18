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
# katmanlar RGBA (on-carpimli "uzerine"): saydam cikti icin gercek alfa tutulur
Ca=np.zeros((H,W),np.float32)
def uzerine(col,al):
    global C,Ca
    al=np.clip(al,0,1); C=C*(1-al[...,None])+col*al[...,None]; Ca=Ca*(1-al)+al
def interp(R_,dur):
    rr=np.array([d[0] for d in dur],np.float32)
    col=np.stack([np.interp(R_,rr,[rk(d[1])[c] for d in dur]) for c in range(3)],-1); al=np.interp(R_,rr,[d[2] for d in dur]); return col,al
# seftali kirmizisi = gunes cevresindeki sicaklik dalgasi (korona): kutupsal fBm gurultu ile dalgali, alevli kenar + ince taneli doku
from scipy import ndimage
def fbm(seed,olcekler,agir):
    rg=np.random.default_rng(seed); n=np.zeros((H,W),np.float32)
    for sc,w_ in zip(olcekler,agir):
        z=rg.standard_normal((H//sc+3,W//sc+3)).astype(np.float32)
        z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:H,:W]; n+=w_*z/ (z.std()+1e-6)
    return n/np.sqrt(sum(w_*w_ for w_ in agir))
# kutupsal koordinatta gurultu: aciya gore uzayan (radyal) alev dillleri
th=(A+np.pi)/(2*np.pi); Pn=np.zeros((H,W),np.float32); rg=np.random.default_rng(5)
for k,(na,nr,w_) in enumerate([(30,3,0.7),(64,5,0.6),(120,8,0.4)]):
    z=rg.standard_normal((nr+4,na)).astype(np.float32)
    zr=np.clip(R/220*nr,0,nr+2); za=th*na
    i0=np.floor(za).astype(int)%na; i1=(i0+1)%na; fa=za-np.floor(za); j0=np.floor(zr).astype(int); fj=zr-j0
    v=lambda j,i: z[np.clip(j,0,nr+3),i]
    sm=lambda f: f*f*(3-2*f)
    Pn+=w_*((v(j0,i0)*(1-sm(fa))+v(j0,i1)*sm(fa))*(1-sm(fj))+(v(j0+1,i0)*(1-sm(fa))+v(j0+1,i1)*sm(fa))*sm(fj))
Pn/=1.15; Pn=ndimage.gaussian_filter(Pn,2.0)
tane=ndimage.gaussian_filter(fbm(9,[2,3],[1.0,0.5]),0.8)                                                  # ince taneli doku (fotograftaki gibi)
Rw=R-9*Pn                                                                    # dalgali yaricap: alev dilleri disari tasar
col,al=interp(Rw,[(0,"#E6A49C",0.8),(112,"#E0A098",0.8),(124,"#D8948C",0.7),(140,"#CC8880",0.48),(154,"#B87A74",0.24),(166,"#8A5E58",0.0)])   # kenara dogru azalan sicaklik dalgasi
al=al*np.clip(0.9+0.1*Pn+0.05*tane,0,1)*np.interp(R,[0,146,166],[1,1,0])   # olculer sabit: dis sinir 166'yi gecmez
col=col*np.clip(1+0.04*tane+0.08*Pn,0.85,1.15)[...,None]
# sicak parlak damarlar (korona isiltisi)
damar=np.clip(Pn-0.4,0,1)*np.exp(-((Rw-120)/22)**2)
col=col+ndimage.gaussian_filter(damar,3)[...,None]*rk("#F2C0A8")*0.35
uzerine(np.clip(col,0,1),al)
# 3) ince, yogun sicaklik dalgasi katmani (r~108-122): sik, yuksek kontrastli titresim
rg3=np.random.default_rng(31); z3=ndimage.gaussian_filter1d(rg3.standard_normal(220).astype(np.float32),1.2,mode="wrap")
i3=(th*220).astype(int)%220; tit=z3[i3]/ (z3.std()+1e-6)
Ry=R-4*tit-3*Pn
yog_al=np.exp(-((Ry-114)/6.5)**2)*np.clip(0.75+0.25*tit+0.08*tane,0,1)*0.9
uzerine(np.broadcast_to(rk("#F0B49A"),C.shape)*np.clip(1+0.12*tit,0.85,1.2)[...,None],yog_al)
# 2) atesbulutu: titanyumun hemen disinda bir tik daha kirmizi, dalgali bulut (r~84-108)
bul=ndimage.gaussian_filter(fbm(41,[6,12,24],[0.6,1.0,0.8]),1.5)
Rb=R-6*bul-4*Pn
ab_col,ab_al=interp(Rb,[(0,"#D4625A",0.0),(80,"#D4625A",0.85),(92,"#C85850",0.85),(102,"#B85048",0.6),(110,"#A84A44",0.0)])
ab_al=ab_al*np.clip(0.7+0.3*bul+0.06*tane,0,1)
uzerine(np.clip(ab_col*np.clip(1+0.15*bul,0.8,1.25)[...,None],0,1),ab_al)
# titanyum beyaz: buyuk, opak; kenari seftaliye yumusak gecer
col,al=interp(R,[(0,"#FFFFFF",1.0),(76,"#FEFEFE",1.0),(86,"#F8DBC3",0.8),(96,"#EBB8A8",0.0)])
uzerine(col,al)
# supernova yansimasi: seftaliden disari, parantezlere kadar cok soluk sicak isik; filamanli (radyal ince lifler + dalgali bulutsu), uzaklastikca azalir
rg2=np.random.default_rng(13); fil=np.zeros((H,W),np.float32)
for na,w_ in [(90,1.0),(180,0.6),(360,0.35)]:
    z=ndimage.gaussian_filter1d(rg2.standard_normal(na+1).astype(np.float32),0.8,mode="wrap"); z[-1]=z[0]
    za=th*na; i0=np.floor(za).astype(int)%na; f=za-np.floor(za); fil+=w_*(z[i0]*(1-f)+z[(i0+1)%na]*f)
fil=np.clip(0.5+0.35*fil,0,1)                                                 # radyal lifler (acıya gore)
bulut=np.clip(0.6+0.4*ndimage.gaussian_filter(fbm(17,[16,32],[1.0,0.7]),4),0,1) # dalgali bulutsu
uz=np.clip((R-150)/12,0,1)*np.exp(-np.clip(R-158,0,None)/58)                    # seftali kenarindan disari azalir
sn_al=0.28*uz*(0.45+0.55*fil)*bulut*np.clip(1-((R-150)/210)**2,0,1)
sn_col=np.stack([np.interp(R,[150,200,260,330],[rk(c)[k] for c in ("#E8A89C","#D49084","#B87A74","#9A6A66")]) for k in range(3)],-1)
uzerine(sn_col,sn_al)
# parantezler: dis kenar sabit yay, ic kenar ortada iceri siskin (sari kisim parantezin icinde -> orta kalin), uclar incelip solar
yan=np.abs(np.cos(A)); aci=np.degrees(np.arccos(np.clip(yan,0,1)))
# geometri: once tam halka — ic kenar yuvarlak (r=200), dis kenar yanlardan siskin ustten basik elips (yatay 282, dikey 206);
# boylece halka yanlarda kalin, ustte-altta ince olur; sonra ince ust/alt kisim silinir -> kalin, sivri uclu sag-sol parantezler
ic_r=200.0; ea,eb=282.0,206.0
dis_r=1/np.sqrt((np.cos(A)/ea)**2+(np.sin(A)/eb)**2)
kal=np.maximum(dis_r-ic_r,0)
uc=np.clip((kal-14)/26,0,1)                                                    # ince ust/alt kisim silinir (yumusak)
u=(R-ic_r)/np.maximum(kal,1e-3)
renkler=[(0.0,"#FCE65E"),(0.5,"#FEF486"),(0.72,"#E2F8A0"),(1.0,"#A8E8B0")]                          # yalniz sari + yesil   # ic genis sari -> acik yesil -> yesil (dis)
uu=np.clip(u,0,1); col=np.stack([np.interp(uu,[q[0] for q in renkler],[rk(q[1])[c] for q in renkler]) for c in range(3)],-1)
op=np.clip(np.minimum(u/0.1,(1-u)/0.08),0,1)*uc*0.92*(kal>0.5)
cizgi=np.clip(0.86+0.14*fil+0.04*ndimage.gaussian_filter(tane,2.5),0.6,1.1)        # ışık lifleri / pürüz
op=ndimage.gaussian_filter(op*cizgi,3.0)*0.95                                         # yumusak, parlayan kenar
col=np.stack([ndimage.gaussian_filter(col[...,c],3.0) for c in range(3)],-1)
uzerine(col,op)
os.makedirs(K,exist_ok=True)
# parlama tasmasi: parlak bolgeler cevreye yayilir (ekran karisimi), beyaz asiri pozlanmis gibi tasar
lum=C.max(2); parlak=C*np.clip((np.minimum(C[...,2],lum)-0.75)/0.25,0,1)[...,None]          # yalniz beyaza yakin (cekirdek) tasar; renkli parantez beyazlasmaz
bloom=sum(w_*np.stack([ndimage.gaussian_filter(parlak[...,c],sg) for c in range(3)],-1) for sg,w_ in [(6,0.55),(18,0.45),(48,0.35),(110,0.25)])
yay=sum(w_*np.stack([ndimage.gaussian_filter(C[...,c],sg) for c in range(3)],-1) for sg,w_ in [(10,0.14),(35,0.12)])   # genel hafif sis
C=1-(1-C)*(1-np.clip(bloom,0,1))*(1-np.clip(yay,0,1))
Ca=np.maximum(Ca,np.clip(C.max(2),0,1))
# ince tane (fotograftaki gibi), isikli yerlerde
gr=np.random.default_rng(23).standard_normal((H,W)).astype(np.float32); gr=ndimage.gaussian_filter(gr,0.7)
C=np.clip(C*(1+0.045*gr[...,None]*np.clip(C.max(2)*1.5,0,1)[...,None]),0,1)
img=(np.clip(C,0,1)*255).round().astype(np.uint8)                      # siyah fon uzerinde (C on-carpimli)
Image.fromarray(img).save(os.path.join(K,"kure.png"))
rgb=(np.clip(C/np.maximum(Ca,1e-4)[...,None],0,1)*255).round().astype(np.uint8); al=(np.clip(Ca,0,1)*255).round().astype(np.uint8)
Image.fromarray(np.dstack([rgb,al])).save(os.path.join(K,"kure_saydam.png"))
# zemin uzerinde onizleme (arkasi secilir mi): fotograftaki toprak rengi
zem=np.array([0x86,0x6C,0x5E],np.float32)/255; zg=(np.clip(C+zem*(1-Ca[...,None]),0,1)*255).astype(np.uint8)
# onizleme: fotograf (kirpilmis) | yeni
ref=Image.open(os.path.join(os.path.expanduser("~"),".claude","uploads","7667fcb8-b488-59d0-b1d8-f55ffb36b68a","0d1e98a9-image.jpg")).convert("RGB").crop((638-420,440-330,638+420,440+330)).resize((960,754))
new=Image.fromarray(img).crop((960-672,540-528,960+672,540+528)).resize((960,754))
nz=Image.fromarray(zg).crop((960-672,540-528,960+672,540+528)).resize((960,754))
o=Image.new("RGB",(2880,754)); o.paste(ref,(0,0)); o.paste(nz,(960,0)); o.paste(new,(1920,0)); o.save(os.path.join(ONZ,"efekt10_kure.png"))
print("tamam")
