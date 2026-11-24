"""Degisken yazilarin font + punto + harf araligi (orijinal murekkep IoU). Adaylar: Liberation Sans R/B (Arial olculu), Roboto R/B."""
import numpy as np, json
from PIL import Image, ImageFont, ImageDraw
LS='/usr/share/fonts/truetype/liberation/'; FD='/home/user/Koray/arayuz/kaynak/char_info/fonts/'
F={'LiberationSans-Regular':LS+'LiberationSans-Regular.ttf','LiberationSans-Bold':LS+'LiberationSans-Bold.ttf',
   'Roboto-Regular':FD+'Roboto-Regular.ttf','Roboto-Bold':FD+'Roboto-Bold.ttf'}
# ad: (goruntu, metin, kutu, murekkep kosulu)
SAT0={'kart_ad':(5,'Scroll of Health 2000',(690,418,925,446),'gri'),
     'kart_fiyat':(5,'150',(780,470,860,520),'kirmizi'),
     'rozet':(5,'30',(817,384,850,407),'beyaz'),
     'cash':(1,'0',(2270,112,2320,160),'gri'),
     'ayr_baslik':(11,'Teleport Scroll',(1225,268,1475,310),'gri'),
     'ayr_aciklama':(11,'Teleport Scroll.',(1045,462,1330,510),'beyaz'),
     'ayr_adet':(11,'(1)',(1305,422,1380,465),'gri'),
     'ayr_fiyat':(11,'0',(1310,828,1375,878),'sari'),
     'basari':(12,'Purchase Succcessfully',(1150,630,1545,690),'beyaz'),
     'placeholder':(10,'Enter Your Epin or Gift Code',(1020,610,1445,658),'beyaz')}
import sys
SAT={k:v for k,v in SAT0.items() if len(sys.argv)<2 or k in sys.argv[1:]}
def kosul(P,k):
    R,G,B=P[...,0],P[...,1],P[...,2]
    if k=='kirmizi': return (R>170)&(G<140)
    if k=='sari': return (R>170)&(G>150)&(B<90)
    if k=='gri': return P.min(-1)>130
    return P.min(-1)>160
def murek(m):
    ys,xs=np.nonzero(m); return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(fn,t,p,s):
    f=ImageFont.truetype(F[fn],p); im=Image.new('L',(1200,150),0); d=ImageDraw.Draw(im); x=20.0
    for ch in t: d.text((x,30),ch,font=f,fill=255); x+=f.getlength(ch)+s
    return murek(np.asarray(im)>110)
def iou(a,b):
    h=max(a.shape[0],b.shape[0])+4; w=max(a.shape[1],b.shape[1])+4; best=0
    for dy in range(-2,3):
        for dx in range(-3,4):
            A=np.zeros((h+8,w+8),bool); B=np.zeros((h+8,w+8),bool)
            A[4:4+a.shape[0],4:4+a.shape[1]]=a; B[4+dy:4+dy+b.shape[0],4+dx:4+dx+b.shape[1]]=b
            best=max(best,(A&B).sum()/(A|B).sum())
    return best
out={}
for ad,(i,t,(x0,y0,x1,y1),k) in SAT.items():
    P=np.asarray(Image.open('s%02d.jpg'%i).convert('RGB'),float)[y0:y1,x0:x1]; m=kosul(P,k); ys,xs=np.nonzero(m)
    col=np.median(P[m&(P.max(-1)>=np.percentile(P.max(-1)[m],50))],0); h=murek(m)
    r=sorted(((iou(h,ciz(fn,t,p,s)),fn,p,float(s)) for fn in F for p in range(int(h.shape[0]*0.9),int(h.shape[0]*2.0)+2) for s in ((0,0.5,1,1.5,2) if len(t)>1 else (0,))),reverse=True)[:2]
    out[ad]=dict(metin=t,merkez=[float(x0+(xs.min()+xs.max()+1)/2),float(y0+(ys.min()+ys.max()+1)/2)],yukseklik=int(h.shape[0]),
                 renk='#%02X%02X%02X'%tuple(int(v) for v in col),en_iyi=[(round(v,3),fn,p,s) for v,fn,p,s in r])
    print(ad,out[ad],flush=True)
import os
esk=json.load(open('punto.json')) if os.path.exists('punto.json') else {}
esk.update(out); json.dump(esk,open('punto.json','w'),indent=1)
