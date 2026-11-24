"""Orijinal <-> yeni (sprite + siyah zemin + Text) dort pencere; fark x4. -> onizlemeler/upgrade_onizleme.png
Calisma klasoru: pencere.py ve secim.py ciktilari."""
import numpy as np, json, os
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
FD='/home/user/Koray/arayuz/kaynak/char_info/fonts/'
SB=FD+'RobotoSlab-Bold.ttf'; SR=FD+'RobotoSlab-Regular.otf'
YAZI={'deger':(SR,27,0.0,(240,242,245)),'oran':(SR,39,1.5,(225,225,227)),'para':(SB,34,1.0,(255,255,255))}
def yaz(im,metin,merkez,tur):
    f,p,s,renk=YAZI[tur]; F=ImageFont.truetype(f,p); w=int(sum(F.getlength(c) for c in metin)+s*len(metin))+60
    T=Image.new('L',(w,110),0); d=ImageDraw.Draw(T); x=20.0
    for c in metin: d.text((x,25),c,font=F,fill=255); x+=F.getlength(c)+s
    A=np.asarray(T); ys,xs=np.nonzero(A>110)
    if metin in '-': cy=(ys.min()+ys.max()+1)/2
    else:
        # dikey: rakam govdesinin merkezi (virgul kuyrugu haric) -> buyuk harf yuksekligi
        cap=F.getbbox('0',anchor='ls'); cy=25+F.getbbox('0')[1]+(F.getbbox('0')[3]-F.getbbox('0')[1])/2
    cx=(xs.min()+xs.max()+1)/2
    im.paste(Image.new('RGB',T.size,renk),(int(round(merkez[0]-cx)),int(round(merkez[1]-cy))),T)
CFG={'item':dict(yazilar=[('-',(1329.5,597),'deger'),('-',(1876,597),'deger'),('5,042,580',(1860,852.5),'para')]),
     'aksesuar':dict(yazilar=[('-',(1328.5,623.5),'deger'),('-',(1884.5,623.5),'deger'),('5,042,580',(1862,854),'para')]),
     'hizli':dict(yazilar=[('5,042,580',(1860,863),'para')])}
paneller=[]
for ad,c in CFG.items():
    z=np.load(ad+'_coz.npz'); a,C,U,Bt,O=z['a'],z['C'],z['U'],z['arka'],z['O']
    kutu=json.load(open(ad+'_cfg.json'))['kutu']; X0,Y0=kutu[0],kutu[1]
    T0=0.105; R=a[...,None]*C+(1-a[...,None])*np.where(U[...,None],Bt*T0,Bt)
    im=Image.fromarray(R.clip(0,255).astype(np.uint8))
    for m,(x,y),t in c['yazilar']: yaz(im,m,(x-X0,y-Y0),t)
    paneller.append((ad,O,np.asarray(im).astype(float)))
# secim
cf=json.load(open('secim_cfg.json')); X0,Y0,W,H=cf['sprite']
O=np.asarray(Image.open('secim.jpg').convert('RGB'),float)[Y0:Y0+H,X0:X0+W]
sp=np.asarray(Image.open('secim_sprite.png')).astype(float); a=sp[...,3:]/255
gx,gy,gw,gh=cf['govde']; U=np.zeros((H,W),bool); U[gy:gy+gh,gx:gx+gw]=True
Bt=np.where(U[...,None],O/(1-cf['alfa']),O).clip(0,255)
R=a*sp[...,:3]+(1-a)*np.where(U[...,None],Bt*(1-cf['alfa']),Bt)
paneller.insert(0,('secim',O,R))
f2=ImageFont.truetype(SB,24); satirlar=[]
for ad,O,R in paneller:
    d=np.abs(O-R).mean(-1); print(ad,'ortalama fark',d.mean().round(2))
    h,w=O.shape[:2]; P=Image.new('RGB',(w*3+40,h+40),(20,20,20)); dr=ImageDraw.Draw(P)
    P.paste(Image.fromarray(O.astype(np.uint8)),(0,40)); P.paste(Image.fromarray(R.clip(0,255).astype(np.uint8)),(w+20,40))
    P.paste(Image.fromarray(np.clip(d*4,0,255).astype(np.uint8)).convert('RGB'),(2*w+40,40))
    ad2={'secim':'SELECT UPGRADE','item':'ITEM UPGRADE','aksesuar':'ACCESSORY UPGRADE','hizli':'FAST UPGRADE'}[ad]
    dr.text((4,6),ad2+' - ORIJINAL',font=f2,fill=(255,255,0)); dr.text((w+24,6),'YENI',font=f2,fill=(255,255,0)); dr.text((2*w+44,6),'FARK x4  (ort. %.1f/255)'%d.mean(),font=f2,fill=(255,255,0))
    satirlar.append(P)
os.makedirs('cikti',exist_ok=True)
for (ad,_,_),P in zip(paneller,satirlar): P.save('cikti/onizleme_%s.png'%ad)
