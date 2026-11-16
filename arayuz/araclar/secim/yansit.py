import numpy as np, glob
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from zemin import *
fs=sorted(glob.glob('G/k_*.png'))
a=lambda i: np.asarray(Image.open(fs[i]).convert('RGB'),dtype=np.float32)
med=lambda r: np.median([a(i) for i in r],0)
p=np.load('rect.npy'); a1,b1,R0=p[2],p[3],p[6]
H=np.asarray(Image.open('halka_doku.png')).astype(np.float32); N=512; K=1.35
okd=np.asarray(Image.open('ok_doku.png')).astype(np.float32)
x0,y0,w,h,cx,yuc,Yb,Yalt,hb,sw=np.load('ok_meta2.npy')
vv,uu=np.mgrid[0:1220,0:2712]+0.5; Xs,Ds=zemine(uu,vv)
def koy(B,D_,kx,ky):
    r=np.stack([ndimage.map_coordinates(D_[...,c],[ky,kx],order=1,cval=0) for c in range(4)],-1)
    return r[...,:3]+(1-r[...,3:]/255)*B
# halka: kare 73 (Stroke sonu), zemin 76-79
B1=med(range(76,80)); O1=med(range(72,76))
kx=(Xs-a1)/(K*R0)*(N/2)+N/2; ky=-(Ds-b1)/(K*R0)*(N/2)+N/2
R1=koy(B1,H,kx,ky)
# ok: stab ornegi (136-139), zemin 141-145; kanonik -> orn(360) -> zemin
T,L,Rr=map(np.array,[(137.5,275),(111,149),(246,202.5)])
OX,OY,hh,ww=np.load('ok_kanon.npy')[0]
dst=[(OX,OY-hh),(OX-ww,OY),(OX+ww,OY)]
best=None
for LL,RR in ((L,Rr),(Rr,L)):
    A=[];b=[]
    for (x,y),(u,v) in zip([T,LL,RR],dst): A+=[[x,-y,1,0],[y,x,0,1]]; b+=[u,v]
    q=np.linalg.lstsq(np.array(A,float),np.array(b,float),rcond=None)[0]; e=np.abs(np.array(A,float)@q-b).sum()
    if best is None or e<best[0]: best=(e,q)
q=best[1]
X0,D0=zemine(1330,850); ox=180+(Xs-X0)*PXU; oy=180-(Ds-D0)*PXU          # orn koordinati
cxk=q[0]*ox-q[1]*oy+q[2]; cyk=q[1]*ox+q[0]*oy+q[3]                       # kanonik
O2=med(range(136,140)); B2=med(range(141,146))
R2=koy(B2,okd,cxk-x0,cyk-y0)
F=ImageFont.truetype('/home/user/Koray/arayuz/kaynak/char_info/fonts/Roboto-Bold.ttf',22)
def panel(O,R,kut,bas):
    x,y,w_,h_=kut; A=Image.fromarray(np.clip(O,0,255).astype(np.uint8)).crop((x,y,x+w_,y+h_)); Bm=Image.fromarray(np.clip(R,0,255).astype(np.uint8)).crop((x,y,x+w_,y+h_))
    c=Image.new('RGB',(w_*2+10,h_+36),(24,24,28)); c.paste(A,(0,36)); c.paste(Bm,(w_+10,36)); d=ImageDraw.Draw(c)
    d.text((6,6),bas+' — ORİJİNAL',font=F,fill=(200,200,200)); d.text((w_+16,6),'YENİ (zemin + doku)',font=F,fill=(140,230,140)); return c
def onde(B):
    sol=(B[...,1]<0.75*B[...,0])&(B[...,2]<0.75*B[...,0])&(B[...,0]>55)      # solucan, kirmizi etiketler (zemindeki on plan)
    return ndimage.binary_dilation(ndimage.binary_opening(sol,np.ones((2,2))),np.ones((3,3)))
R1=np.where(onde(B1)[...,None],O1,R1); R2=np.where(onde(B2)[...,None],O2,R2)
p1=panel(O1,R1,(1100,790,440,350),'Seçim halkası'); p2=panel(O2,R2,(1180,740,300,260),'Yön oku')
m1=(R1!=B1).any(2)&(vv<1138); m2=(R2!=B2).any(2)
print('halka ort fark',round(float(np.abs(R1-O1)[m1].mean()),2),'ok ort fark',round(float(np.abs(R2-O2)[m2].mean()),2))
o=Image.new('RGB',(p1.width,p1.height+p2.height+10),(24,24,28)); o.paste(p1,(0,0)); o.paste(p2,(0,p1.height+10))
o.save('/home/user/Koray/arayuz/onizlemeler/secim_onizleme.png'); print(o.size)
