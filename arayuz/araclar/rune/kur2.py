#!/usr/bin/env python3
"""Neon run halkasi (rune2_cizgi.png) shader benzetimi: kur.py ile ayni, renk aciya gore mor -> mavi -> yesil.
Shader: "Olympos/Rune Neon Halkasi" / "Olympos/Rune Neon Duvari". kur_video ile ayni kare/karakter, cap 1.6, yogunluk 0.5."""
import os, sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","rune"); ONZ=os.path.join(B_,"..","..","onizlemeler")
T=np.asarray(Image.open(os.path.join(K,"rune2_cizgi.png"))).astype(float)/255
G=np.asarray(Image.open(os.path.join(K,"rune_gurultu.png"))).astype(float)/255
MOR=np.array([0.62,0.22,1.0]); MAVI=np.array([0.22,0.45,1.0]); YESIL=np.array([0.25,1.0,0.45]); BEYAZ=np.array([0.9,0.95,1.0])
DIS_HIZ=0.25; IC_HIZ=-0.4; ALEV_HIZ=1.6; DUVAR_HIZ=1.4; DUVAR_BOY=0.12
def ornek(tex,u,v):
    x=np.clip(u*(tex.shape[1]-1),0,tex.shape[1]-1); y=np.clip(v*(tex.shape[0]-1),0,tex.shape[0]-1)
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int); x1=np.minimum(x0+1,tex.shape[1]-1); y1=np.minimum(y0+1,tex.shape[0]-1); fx=x-x0; fy=y-y0
    if tex.ndim==3: fx=fx[...,None]; fy=fy[...,None]
    return (tex[y0,x0]*(1-fx)+tex[y0,x1]*fx)*(1-fy)+(tex[y1,x0]*(1-fx)+tex[y1,x1]*fx)*fy
def gur(u,v): return ornek(G,u%1,v%1)
def ton(a,t):
    """aciya gore 3 renk (mor-mavi-yesil), yavas kayar: 0..1 -> MOR,MAVI,YESIL,MOR"""
    p=((a/(2*math.pi)+t*0.05)%1)*3; i=np.floor(p).astype(int)%3; f=(p-np.floor(p))[...,None]; f=f*f*(3-2*f)
    R=np.stack([MOR,MAVI,YESIL]); return R[i]*(1-f)+R[(i+1)%3]*f
def kare(t,boyut=512,guc=1.0):
    v,u=np.mgrid[0:boyut,0:boyut]/(boyut-1.0); x=u-0.5; y=v-0.5; r=np.hypot(x,y)*2; a=np.arctan2(y,x)
    def don(aci): c,s=math.cos(aci),math.sin(aci); return 0.5+(x*c-y*s), 0.5+(x*s+y*c)
    n=gur(a/(2*math.pi)*6, r*1.5-t*ALEV_HIZ); buk=(n-0.5)*0.006
    u1,v1=don(t*DIS_HIZ); u2,v2=don(t*IC_HIZ)
    Ld=ornek(T,u1+buk,v1+buk); Li=ornek(T,u2-buk,v2+buk)
    cizgi=Ld[...,0]+Li[...,1]; isil=Ld[...,2]+Li[...,3]
    tit=0.75+0.5*gur(a/(2*math.pi)*3+t*0.3, t*0.7)
    dil=gur(a/(2*math.pi)*14, r*2.2-t*ALEV_HIZ*1.3)
    halka=np.exp(-((r-0.94)/0.05)**2)+0.6*np.exp(-((r-0.60)/0.05)**2)
    alev=np.clip((dil-0.40)*3.4,0,1)*halka*tit*1.3
    k=ton(a,t)
    renk=cizgi[...,None]*(BEYAZ*0.55+k*0.6) + isil[...,None]*k*0.65*tit[...,None] + alev[...,None]*k*1.0 + (alev**2)[...,None]*BEYAZ*0.35
    renk*=(r<1.02)[...,None]; return np.clip(renk*guc,0,1.6)
def duvar(t,cap,basik,guc,W,H,merkez):
    yy,xx=np.mgrid[0:H,0:W].astype(float); R=cap/2*0.97; Rb=R*basik; Hh=cap*DUVAR_BOY
    E=np.zeros((H,W,3)); c=np.clip((xx-merkez[0])/R,-1,1); ic=np.abs((xx-merkez[0])/R)<1
    for isaret,arka in ((1,0.55),(-1,1.0)):
        a=isaret*np.arccos(c); yb=merkez[1]+Rb*np.sin(a); h=(yb-yy)/Hh; m=ic&(h>=0)&(h<=1)
        hh=np.clip(h,0,1)
        n=gur(a/(2*math.pi)*10+0.13*np.sin(t), hh*1.2-t*DUVAR_HIZ); n2=gur(a/(2*math.pi)*23, hh*2.5-t*DUVAR_HIZ*1.7)
        v=np.clip((0.55*n+0.45*n2)-hh*0.85-0.12,0,1)*3.0*(1-hh)**0.6
        k=ton(-a+math.pi/2*0,t)                        # zemin dokusuyla ayni aci yonu (ust goruste y asagi)
        renk=v[...,None]*k+np.clip(v-0.5,0,1)[...,None]*BEYAZ*0.6
        E+=np.where(m[...,None],renk*arka,0)
    return np.clip(E*guc*255*0.8,0,255)
if __name__=="__main__":
    S=np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float)
    MERKEZ=(1130,846); CAP=176; BASIK=0.47; YOGUNLUK=0.5
    yy,xx=np.mgrid[0:S.shape[0],0:S.shape[1]]
    kutu=(xx>=1078)&(xx<=1182)&(yy>=735)&(yy<=858); lum=S.mean(2); cim=(lum<85)&(np.abs(S[...,0]-S[...,1])<35)
    kar=ndimage.binary_fill_holes(ndimage.binary_closing(ndimage.binary_opening(kutu&~cim,np.ones((2,2))),np.ones((5,5))))
    kar=ndimage.gaussian_filter(kar.astype(float),0.8)[...,None]
    def bindir(t,g):
        g=g*YOGUNLUK; h=int(CAP*BASIK)
        e=np.asarray(Image.fromarray((np.clip(kare(t,512,g),0,1)*255).astype(np.uint8)).resize((CAP,h),Image.LANCZOS)).astype(float)
        O=S.copy(); x0=int(MERKEZ[0]-CAP/2); y0=int(MERKEZ[1]-h/2); O[y0:y0+h,x0:x0+CAP]+=e
        D=duvar(t,CAP,BASIK,g,S.shape[1],S.shape[0],MERKEZ); on=(yy>MERKEZ[1])[...,None]
        O=O+D*(1-on); O=O*(1-kar)+S*kar; O=O+D*on; return np.clip(O,0,255)
    KIRP=(860,600,1400,905); zam=[0.15,0.6,1.2,2.4]; guc=[0.5,1,1,0.4]
    ims=[Image.fromarray(bindir(t,g).astype(np.uint8)).crop(KIRP) for t,g in zip(zam,guc)]
    orj=Image.fromarray(S.astype(np.uint8)).crop(KIRP); buyuk=Image.fromarray(bindir(1.2,1).astype(np.uint8)).crop(KIRP)
    F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),20)
    w,h=orj.size; c=Image.new("RGB",(w*2+10,(h+34)*3+44),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((8,8),"xDarKPasT + neon run halkasi (ozgun tasarim) — cap 1.6 x karakter boyu, yogunluk 0.5",font=F,fill=(255,220,120))
    c.paste(orj,(0,66)); d.text((6,44),"ORIJINAL KARE",font=F,fill=(200,200,200)); c.paste(buyuk,(w+10,66)); d.text((w+16,44),"EFEKTLI (1.2 sn)",font=F,fill=(140,230,140))
    for i,(im,t) in enumerate(zip(ims,zam)):
        X=(i%2)*(w+10); Y=44+(h+34)*(1+i//2)+22; c.paste(im,(X,Y)); d.text((X+6,Y-22),"%.2f sn"%t,font=F,fill=(255,255,0))
    c.save(os.path.join(ONZ,"rune2_karakter.png")); buyuk.resize((w*2,h*2),Image.LANCZOS).save(os.path.join(ONZ,"rune2_karakter_buyuk.png"))
    Image.fromarray((np.clip(kare(1.2,700),0,1)*255).astype(np.uint8)).save(os.path.join(ONZ,"rune2_onizleme_tek.png")); print(c.size)
