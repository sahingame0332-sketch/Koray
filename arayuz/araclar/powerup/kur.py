"""Kurucunun benzetimi -> orijinal | yeni | fark x4 (onizlemeler/powerup_*.png). Lineer uzayda karistirma (oyundaki gibi).
Ikonlar (oyun verisi) onizleme icin orijinalden kesilir; yazilar olculen font/punto ile cizilir."""
import numpy as np, json, os
from PIL import Image, ImageDraw, ImageFont
import ortak as O
LS='/usr/share/fonts/truetype/liberation/'; FD='/home/user/Koray/arayuz/kaynak/char_info/fonts/'
F=lambda f,p:ImageFont.truetype({'LB':LS+'LiberationSans-Bold.ttf','RB':FD+'Roboto-Bold.ttf'}[f],p)
spr=lambda ad:np.asarray(Image.open(ad+'.png')).astype(float)
def koy(alt,ad,x,y):
    s=spr(ad); O.ustune(alt,s[...,:3],s[...,3]/255,int(x),int(y))
def yazi(alt,t,f,p,renk,x,y,hiza='orta',aralik=0.0,sar=None,satir=26,kontur=None):
    """x: hiza='orta' -> murekkep merkezi, 'sol' -> sol kenar; y: ilk satirin murekkep orta yuksekligi (rakam/buyuk harf)"""
    Fn=F(f,p); satirlar=[t]
    if sar:
        satirlar=[]; cur=''
        for w in t.split(' '):
            c=(cur+' '+w).strip()
            if Fn.getlength(c)<=sar or not cur: cur=c
            else: satirlar.append(cur); cur=w
        satirlar.append(cur)
    im=Image.fromarray(np.clip(alt,0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    for k,s in enumerate(satirlar):
        w=sum(Fn.getlength(c) for c in s)+aralik*(len(s)-1); bb=Fn.getbbox('H')
        cy=(bb[1]+bb[3])/2; xx=x-w/2 if hiza=='orta' else x; yy=y+k*satir-cy
        if kontur:
            x2=xx
            for c in s:
                for ox,oy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)): d.text((x2+ox,yy+oy),c,font=Fn,fill=kontur)
                x2+=Fn.getlength(c)+aralik
        for c in s: d.text((xx,yy),c,font=Fn,fill=renk); xx+=Fn.getlength(c)+aralik
    alt[:]=np.asarray(im).astype(float)
def hex2(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
KAT=dict(x0=662,dx=335.33,y=[285,747],kart='kart_kategori',ikon=(102,39),ad_y=143.5,para=(85,187),fiyat=(133,205),sar=227)
ANA=dict(x0=663,dx=347.4,y=[304,743],kart='kart_ana',ikon=(103,47),ad_y=149.5,para=(87,188),fiyat=(133,206),sar=215)
SEKME=json.load(open('sekmeler.json'))
def magaza(secili,kartlar,duzen,kaynak,cash=0,dy=0,kay=None):
    Z=np.zeros((1220,2712,3))+np.array([30,30,22.]); koy(Z,'magaza_zemin',O.X0,0)
    x,y,w,h=SEKME[secili]; koy(Z,'sekme_%s_secili'%secili,O.X0+x,y)
    yazi(Z,str(cash),'LB',37,hex2('#BEAAAB'),2294,131.5)
    A=O.yukle(kaynak)
    for i,(ad,fiyat) in enumerate(kartlar):
        r,c=divmod(i,5); kx=int(round(duzen['x0']+c*duzen['dx'])); ky=duzen['y'][r]+dy
        koy(Z,duzen['kart'],kx-2,ky-2)
        if duzen is KAT and fiyat<=cash:
            koy(Z,'dugme_kategori_uygun',kx+407-335,ky+248)
        ix,iy=kx+duzen['ikon'][0],ky+duzen['ikon'][1]
        Z[iy:iy+84,ix:ix+84]=A[iy:iy+84,ix:ix+84]                          # ikon (oyun verisi)
        yazi(Z,ad,'RB',22,hex2('#CBBBB9'),kx+144,ky+duzen['ad_y'],sar=duzen['sar'])
        koy(Z,'para_ikonu',kx+duzen['para'][0],ky+duzen['para'][1])
        fs='{:,}'.format(fiyat).replace(',','.')
        yazi(Z,fs,'LB',31,hex2('#FDDE24' if fiyat<=cash else '#F94922'),kx+duzen['fiyat'][0]-3,ky+duzen['fiyat'][1],hiza='sol',aralik=1.5,kontur=(45,14,6))
    if kay:                                                    # kaydirma tutamagi: 9-dilim (ust/alt 10 px) dikey uzatma
        h=spr('kaydirma'); y0,y1=kay; L=y1-y0+1; u,a_=h[:10],h[-10:]; orta=h[10:-10]
        idx=np.linspace(0,len(orta)-1,max(L-20,1)).astype(int); H=np.concatenate([u,orta[idx],a_],0)
        O.ustune(Z,H[...,:3],H[...,3]/255,2347,y0-4)
    return Z
def panel(ad,O_,Y):
    d=np.abs(O_-Y).mean(-1); sl=np.s_[:,250:2460]
    h,w=d[sl].shape; P=Image.new('RGB',(w*3+40,h+50),(20,20,20)); dr=ImageDraw.Draw(P); f=F('LB',30)
    P.paste(Image.fromarray(O_[sl].astype(np.uint8)),(0,50)); P.paste(Image.fromarray(np.clip(Y[sl],0,255).astype(np.uint8)),(w+20,50))
    P.paste(Image.fromarray(np.clip(d[sl]*4,0,255).astype(np.uint8)).convert('RGB'),(2*w+40,50))
    dr.text((6,8),ad+' - ORIJINAL',font=f,fill=(255,255,0)); dr.text((w+26,8),'YENI',font=f,fill=(255,255,0)); dr.text((2*w+46,8),'FARK x4 (ort. %.1f/255)'%d[sl].mean(),font=f,fill=(255,255,0))
    os.makedirs('cikti',exist_ok=True); P.resize((P.width//2,P.height//2)).save('cikti/%s.png'%ad); print(ad,'fark',d[sl].mean().round(2))
SCR=[('Scroll of Health 2000 Up',150),('Scroll of Health 1500 Up',100),('Scroll of Health 1000 Up',75),('Teleport Scroll',0),('Scroll of Armor 400 Up',150),
     ('Scroll of Armor 350 Up',100),('Scroll of Armor 300 Up',75),('Scroll of Attack',100),('Speed Scroll',50),('Scroll of Lion',75)]
MAIN=[('Scroll of Health 2000 Up',150),('Scroll of Armor 400 Up',150),('Scroll Of Experience',200),('Genie Spirit (24 Hours)',250),('5000x Premium Mp Potion',400),
      ('Trina\'s Piece',800),('Red Potion[NO TRADE]',30),('Karivdis',550),('5000x Premium Hp Potion',400)]
if __name__=='__main__':
    Y=magaza('MainPage',MAIN,ANA,1); panel('magaza_main',O.yukle(1),Y)
    Y5=magaza('Scrolls',SCR,KAT,5)
    # kaydirma cubugu (handle) — onizlemede s05 konumu
    Y5=magaza('Scrolls',SCR,KAT,5,kay=(270,680)); np.save('Y5.npy',Y5); panel('magaza_scrolls',O.yukle(5),Y5)
    # satin alma ayrintisi (s11 = s05 + pencere)
    Y=Y5.copy(); koy(Y,'ayrinti',1026,256); A11=O.yukle(11)
    Y[325:409,1305:1389]=A11[325:409,1305:1389]
    yazi(Y,'Teleport Scroll','LB',29,hex2('#BFADAD'),1355,293.5,aralik=0.5)
    yazi(Y,'(1)','LB',36,hex2('#BFADAD'),1351,441.5,aralik=1.5)
    yazi(Y,'Teleport Scroll.','RB',33,hex2('#FCE7E6'),1052,485.5,hiza='sol')
    yazi(Y,'0','LB',37,hex2('#FDDE24'),1351.5,851)
    panel('ayrinti',A11,Y)
    # basari: gri ortu (lineer a .24, g .24) + pencere + mesaj
    Y=O.srgb(O.lin(Y5)*(1-O.ORTU_A)+O.ORTU_A*O.ORTU_G); koy(Y,'basari',1024,575)
    yazi(Y,'Purchase Succcessfully','LB',30,hex2('#FCE7E6'),1351,662.5); panel('basari',O.yukle(12),Y)
    # cash code
    Y=np.zeros((1220,2712,3))+np.array([30,30,22.]); koy(Y,'cashcode',O.X0,0)
    yazi(Y,'Enter Your Epin or Gift Code','LB',29,hex2('#FDE6E6'),1232.5,636,aralik=0.5); panel('cashcode',O.yukle(10),Y)
    EK={2:('PowerUP',[('Alsaydes [Fairy] Voucher',1000),('Star Aura ( Wings Type )',1000),('Solar Tattoo Voucher',1000),('Patho\'s Glove',400),('Vip Key Coupon',200),
            ('Valkrie Armor Certificate',750),('Gryphon Armor Certificate',750),('Bahamut Armor Certificate',750),('Yeniceri Armor Certificate',750),('Costumes Armor Voucher',750)],0,(270,819)),
        3:('PowerUP',[('Valkrie Armor Certificate',750),('Gryphon Armor Certificate',750),('Bahamut Armor Certificate',750),('Yeniceri Armor Certificate',750),('Costumes Armor Voucher',750),
            ('Magic Bag Coupon',100),('(+1) Talisman Voucher',2400)],2,(560,1108)),
        4:('Premiums',[('Switch Premium',2800),('Clan Premium',8500),('Job Change',8000)],0,None),
        6:('Scrolls',[('Scroll of Dexterity',100),('Scroll of Strength',100),('Scroll of Magic Power',100),('Scroll of Health',100),('Scroll Of Experience',200),
            ('NP increase scroll',500),('Name Change Scroll',750),('Clan Name Change Scroll',1500),('Duration Scroll',150)],2,(699,1108)),
        7:('Special',[('5000x Premium Mp Potion',400),('Merchant Search List',300),('Character Seal Scroll',2500),('Ibex HP Potion (1080 HP)',1200),('Crisis MP Potion (2880 MP)',1200),
            ('Red Potion[NO TRADE]',30),('Blue Potion[NO TRADE]',30)],2,(851,1108))}
    for i,(sek,L,dy,kay) in EK.items():
        Y=magaza(sek,L,KAT,i,dy=dy,kay=kay); panel('magaza_%02d_%s'%(i,sek.lower()),O.yukle(i),Y)
    Y8=magaza('Package',[('Full Package Bundle [NO TRADE]',5000)],KAT,8); panel('magaza_package',O.yukle(8),Y8)
    Y=Y8.copy(); koy(Y,'paket_icerik',912,158); panel('paket_icerik',O.yukle(9),Y)
