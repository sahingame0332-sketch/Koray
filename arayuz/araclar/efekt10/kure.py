#!/usr/bin/env python3
"""Efekt 10 pembe patlama — doruk ani tek kare, TARIFE GORE (kullanicinin verdigi katman tarifi), TOPLAMALI (additive/screen) isik.
1) Ic cekirdek: sinirlari keskin olmayan, isinsal dagilan daire. #FFFFFF -> kisa mesafede #FFF2E6 (acik sampanya) -> #FFD1BA (pastel seftali).
2) Orta katman: (a) dairesel bulutsu duman: #F4A482 (sicak seftali) -> #8C4A38 (kizil kahve) -> #6E5C6B (dumanli gri-mor), disa dogru solar;
   (b) merkezden disa firlayan keskin, capraz isik huzmeleri: #FFF77D (limon) cekirdek #FFFFD6 (krem).
3) Dis katman: kure kesiti gibi, uclara dogru incelip sivrilen ic ice hilal yaylar; keskin prizma: #FFD700 (altin) -> #80FF00 (lime)
   -> #00E5CC (turkuaz) -> en dis ince #2962FF (kobalt) cizgi.
Karisim: toplamali — zemini kapatmaz, ustune isik ekler (zeminde onizleme: ekran karisimi).
Cikti: kaynak/efekt10/kure/kure.png (siyah fon), kure_saydam.png (alfa = parlaklik; Unity'de Blend One One / eklemeli), onizlemeler/efekt10_kure*.png"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure"); ONZ=os.path.join(B_,"..","..","onizlemeler")
W,H=1920,1080; s=1.6
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx=xx-W/2+0.5; dy=yy-H/2+0.5; R=np.hypot(dx,dy)/s; A=np.arctan2(dy,dx); th=(A+np.pi)/(2*np.pi)
def rk(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],np.float32)/255
L=np.zeros((H,W,3),np.float32)                                         # toplamali isik tamponu
def ekle(m,col,g=1.0):
    global L; L+=np.clip(m,0,None)[...,None]*(col if np.ndim(col)==3 else np.asarray(col)[None,None,:])*g
def renk_r(Rq,dur):  # yaricapa gore renk gecisi
    rr=[d[0] for d in dur]; return np.stack([np.interp(Rq,rr,[rk(d[1])[c] for d in dur]) for c in range(3)],-1)
def fbm(seed,olc,agr):
    rg=np.random.default_rng(seed); n=np.zeros((H,W),np.float32)
    for sc,w_ in zip(olc,agr):
        z=rg.standard_normal((H//sc+3,W//sc+3)).astype(np.float32); z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:H,:W]; n+=w_*z/(z.std()+1e-6)
    return n/np.sqrt(sum(w_*w_ for w_ in agr))
def acisal(seed,na,sig=1.0):
    z=ndimage.gaussian_filter1d(np.random.default_rng(seed).standard_normal(na).astype(np.float32),sig,mode="wrap"); z/=z.std()+1e-6
    za=th*na; i0=np.floor(za).astype(int)%na; f=za-np.floor(za); f=f*f*(3-2*f); return z[i0]*(1-f)+z[(i0+1)%na]*f
tane=ndimage.gaussian_filter(fbm(9,[2,3],[1.0,0.5]),0.8)
# ---------- 2a) dumanli hale (bulutsu, dairesel; disa dogru doygunlugu azalir) ----------
duman=np.clip(0.72+0.28*ndimage.gaussian_filter(fbm(17,[10,24,48],[0.6,1.0,0.8]),2),0.35,1.2)
dal=0.6*acisal(5,40,1.5)+0.4*acisal(6,90,1.0)
Rd=R-10*dal
dcol=renk_r(Rd,[(0,"#F4A482"),(105,"#F4A482"),(150,"#C07050"),(180,"#8C4A38"),(225,"#7A5050"),(260,"#6E5C6B"),(330,"#6E5C6B")])
dyog=np.interp(Rd,[0,95,110,150,200,260,320],[0,0.0,0.95,0.6,0.28,0.12,0.0])
ekle(dyog*duman*(0.9+0.1*tane),dcol,1.0)
# ---------- 1) ic cekirdek: isinsal dagilan, keskin olmayan ----------
isinsal=0.5*acisal(21,64,0.8)+0.5*acisal(22,150,0.6)                    # kenarda isinsal saçilma
Rc=R-7*np.clip(isinsal,-1.5,2.5)*np.clip((R-55)/30,0,1)
ccol=renk_r(Rc,[(0,"#FFFFFF"),(68,"#FFFFFF"),(80,"#FFF2E6"),(94,"#FFD1BA"),(130,"#FFD1BA")])
cyog=np.interp(Rc,[0,70,84,98,118],[2.6,2.4,1.5,0.7,0.0])
ekle(cyog,ccol,1.0)
# ---------- 2b) keskin capraz isik huzmeleri ----------
rg=np.random.default_rng(44)
huzme=[]; 
for k in range(12):
    taban=np.radians([45,135,225,315][k%4])+rg.uniform(-0.38,0.38) if k<8 else rg.uniform(0,2*np.pi)   # agirlikla capraz
    huzme.append((taban,rg.uniform(150,330),rg.uniform(2.0,4.5),rg.uniform(0.6,1.0)))
hm=np.zeros((H,W),np.float32); hc=np.zeros((H,W),np.float32)
for a,uz,en,g in huzme:
    d=np.abs(np.angle(np.exp(1j*(A-a))))*R                                  # isina dik uzaklik (kure olceginde)
    boy=np.clip(1-R/uz,0,1)*np.clip((R-60)/25,0,1)                           # cekirdekten cikar, uca dogru solar
    w=en*(0.4+0.6*np.clip(1-R/uz,0,1))
    hm=np.maximum(hm,g*boy*np.exp(-(d/w)**2)); hc=np.maximum(hc,g*boy**1.5*np.exp(-(d/(w*0.35))**2))
ekle(hm,rk("#FFF77D"),1.3); ekle(hc,rk("#FFFFD6"),1.2)
# ---------- 3) dis katman: ic ice prizmatik hilal yaylar ----------
def hilal(ic_r,ea,eb,g,kob):
    dis_r=1/np.sqrt((np.cos(A)/ea)**2+(np.sin(A)/eb)**2); kal=np.maximum(dis_r-ic_r,0)
    uc=np.clip((kal-12)/24,0,1)
    u=(R-ic_r)/np.maximum(kal,1e-3); ic=(u>=0)&(u<=1)
    dur=[(0.0,"#FFD700"),(0.30,"#FFD700"),(0.42,"#80FF00"),(0.62,"#80FF00"),(0.74,"#00E5CC"),(0.90,"#00E5CC"),(0.93,"#2962FF"),(1.0,"#2962FF")]
    col=np.stack([np.interp(np.clip(u,0,1),[q[0] for q in dur],[rk(q[1])[c] for q in dur]) for c in range(3)],-1)
    kenar=np.clip(np.minimum(u/0.04,(1-u)/0.03),0,1)                         # keskin sinir
    yog=kenar*uc*ic*(0.85+0.15*np.clip(1-np.abs(u-0.5)*2,0,1))
    yog=yog*(1+kob*np.clip((u-0.9)/0.1,0,1))                                  # en dis kobalt cizgi belirgin
    return yog,col
for ic_r,ea,eb,g in [(200,282,206,0.62),(286,318,290,0.30)]:                  # ana hilal + disindaki ince ikinci yay
    yog,col=hilal(ic_r,ea,eb,g,0.6); ekle(ndimage.gaussian_filter(yog,0.8),col,g)
# ---------- parlama (bloom) ve tane ----------
parlak=np.clip(L-0.7,0,None)
bloom=sum(w_*np.stack([ndimage.gaussian_filter(parlak[...,c],sg) for c in range(3)],-1) for sg,w_ in [(6,0.5),(20,0.4),(55,0.3),(120,0.2)])
L=L+bloom
L=L*(1+0.04*tane[...,None]*np.clip(L.max(2),0,1)[...,None])
img=np.clip(1-np.exp(-1.25*L),0,1)                                         # siyah fonda (toplamali isik, yumusak doyum)
os.makedirs(K,exist_ok=True)
Image.fromarray((img*255).round().astype(np.uint8)).save(os.path.join(K,"kure.png"))
al=img.max(2); rgb=np.where(al[...,None]>1e-4,img/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kure_saydam.png"))
zem=np.array([0x86,0x6C,0x5E],np.float32)/255; zg=1-(1-zem)*(1-img)            # zeminde ekran karisimi
ref=Image.open(os.path.join(os.path.expanduser("~"),".claude","uploads","7667fcb8-b488-59d0-b1d8-f55ffb36b68a","0d1e98a9-image.jpg")).convert("RGB").crop((638-420,440-330,638+420,440+330)).resize((960,754))
kes=lambda a: Image.fromarray((a*255).round().astype(np.uint8)).crop((960-672,540-528,960+672,540+528)).resize((960,754))
o=Image.new("RGB",(2880,754)); o.paste(ref,(0,0)); o.paste(kes(zg),(960,0)); o.paste(kes(img),(1920,0)); o.save(os.path.join(ONZ,"efekt10_kure.png"))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),30)
out=Image.new("RGB",(2920,814),(20,20,24)); d=ImageDraw.Draw(out)
for i,(im,t) in enumerate([(ref,"REFERANS (fotoğraf)"),(kes(zg),"YENİ — toprak zeminde"),(kes(img),"YENİ — siyah fonda")]):
    out.paste(im,(i*980,60)); d.text((i*980+12,14),t,font=F,fill=(255,220,120))
out.save(os.path.join(ONZ,"efekt10_kure_referansli.png"))
Image.fromarray((img*255).round().astype(np.uint8)).crop((960-300,540-300,960+300,540+300)).save(os.path.join(ONZ,"efekt10_kure_merkez.png"))
Image.fromarray((img*255).round().astype(np.uint8)).crop((960-560,540-460,960+560,540+460)).resize((840,690)).save(os.path.join(ONZ,"efekt10_kure_yakin.png"))
print("tamam")
