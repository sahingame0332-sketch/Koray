#!/usr/bin/env python3
"""Shader'in (Olympos/Rune Ates Halkasi) numpy benzetimi + sahneye bindirme (karakterin ayagi, perspektifle basik elips).
Cikti: onizlemeler/rune_onizleme.png (zaman serisi) ve rune_onizleme_tek.png"""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","rune"); ONZ=os.path.join(B_,"..","..","onizlemeler")
T=np.asarray(Image.open(os.path.join(K,"rune_cizgi.png"))).astype(float)/255
G=np.asarray(Image.open(os.path.join(K,"rune_gurultu.png"))).astype(float)/255
N=T.shape[0]
# shader ile ayni parametreler
DIS_HIZ=0.25; IC_HIZ=-0.4; ALEV_HIZ=1.6; RENK_CEKIRDEK=np.array([1.0,0.78,0.38]); RENK_ALEV=np.array([1.0,0.36,0.04]); RENK_KOR=np.array([0.8,0.08,0.0])
DUVAR_HIZ=1.4; DUVAR_BOY=0.12       # alev duvari: yukseklik / cap (yere yakin alevler)
def ornek(tex,u,v):
    x=np.clip(u*(tex.shape[1]-1),0,tex.shape[1]-1); y=np.clip(v*(tex.shape[0]-1),0,tex.shape[0]-1)
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int); x1=np.minimum(x0+1,tex.shape[1]-1); y1=np.minimum(y0+1,tex.shape[0]-1); fx=x-x0; fy=y-y0
    if tex.ndim==3: fx=fx[...,None]; fy=fy[...,None]
    return (tex[y0,x0]*(1-fx)+tex[y0,x1]*fx)*(1-fy)+(tex[y1,x0]*(1-fx)+tex[y1,x1]*fx)*fy
def gur(u,v): return ornek(G,u%1,v%1)
def kare(t,boyut=512,guc=1.0):
    v,u=np.mgrid[0:boyut,0:boyut]/(boyut-1.0)
    x=u-0.5; y=v-0.5; r=np.hypot(x,y)*2; a=np.arctan2(y,x)
    def don(aci):
        c,s=math.cos(aci),math.sin(aci); return 0.5+(x*c-y*s), 0.5+(x*s+y*c)
    # alev titresimi: kutupsal gurultu ile UV bukulmesi
    n=gur(a/(2*math.pi)*6, r*1.5-t*ALEV_HIZ)
    buk=(n-0.5)*0.006
    u1,v1=don(t*DIS_HIZ); u2,v2=don(t*IC_HIZ)
    Ld=ornek(T,u1+buk,v1+buk); Li=ornek(T,u2-buk,v2+buk)
    cizgi=Ld[...,0]+Li[...,1]; isil=Ld[...,2]+Li[...,3]
    tit=0.75+0.5*gur(a/(2*math.pi)*3+t*0.3, t*0.7)
    # alev dilleri: dis halkanin disina ve run bandindan yukari (kutupsal, disa akan)
    dil=gur(a/(2*math.pi)*14, r*2.2-t*ALEV_HIZ*1.3)
    halka=np.exp(-((r-0.93)/0.05)**2)+0.6*np.exp(-((r-0.62)/0.05)**2)
    alev=np.clip((dil-0.40)*3.4,0,1)*halka*tit*1.3
    renk=(cizgi[...,None]*RENK_CEKIRDEK*0.95 + isil[...,None]*RENK_ALEV*0.55*tit[...,None]
          + alev[...,None]*(RENK_ALEV*0.9+RENK_KOR*0.4) + (alev**2)[...,None]*RENK_CEKIRDEK*0.6)
    renk*= (r<1.02)[...,None]
    return np.clip(renk*guc,0,1.6)
def duvar(t,cap,basik,guc,W,H,merkez):
    """Halkanin kenarindan yukselen alev duvari (silindir, eklemeli): ekran pikseli -> (aci, yukseklik)."""
    yy,xx=np.mgrid[0:H,0:W].astype(float); R=cap/2*0.97; Rb=R*basik; Hh=cap*DUVAR_BOY
    E=np.zeros((H,W,3)); c=np.clip((xx-merkez[0])/R,-1,1); ic=np.abs((xx-merkez[0])/R)<1
    for isaret,arka in ((1,0.55),(-1,1.0)):
        a=isaret*np.arccos(c); yb=merkez[1]+Rb*np.sin(a); h=(yb-yy)/Hh
        m=ic&(h>=0)&(h<=1)
        n=gur(a/(2*math.pi)*10+0.13*np.sin(t), h*1.2-t*DUVAR_HIZ); n2=gur(a/(2*math.pi)*23, h*2.5-t*DUVAR_HIZ*1.7)
        v=np.clip((0.55*n+0.45*n2)-h*0.85-0.12,0,1)*3.0*(1-h)**0.6
        renk=v[...,None]*RENK_ALEV+np.clip(v-0.5,0,1)[...,None]*RENK_CEKIRDEK+ (v*(h>0.45))[...,None]*RENK_KOR*0.4
        E+=np.where(m[...,None],renk*arka,0)
    return np.clip(E*guc*255*0.8,0,255)
def sahne_bindir(S,E,merkez,cap,basik=0.42):
    h=int(cap*basik); e=Image.fromarray((np.clip(E,0,1)*255).astype(np.uint8)).resize((cap,h),Image.LANCZOS)
    e=np.asarray(e).astype(float); O=S.copy(); x0=int(merkez[0]-cap/2); y0=int(merkez[1]-h/2)
    xa,ya=max(0,x0),max(0,y0); xb,yb=min(O.shape[1],x0+cap),min(O.shape[0],y0+h)
    O[ya:yb,xa:xb]+=e[ya-y0:yb-y0,xa-x0:xb-x0]; return O
S=np.asarray(Image.open(os.path.join(B_,"..","..","referans_gorseller","rune","sahne.jpg")).convert("RGB")).astype(float)
MERKEZ=(343,302); CAP=264                 # karakterin ayagi; cap 1.6 karakter boyu (karakter ~165 px)
zam=[0.1,0.25,0.6,1.2,2.0,2.4]; guc=[0.25,0.7,1,1,1,0.4]          # acilis, kalis, sonus
ims=[]
# karakter (efektin ONUNDE): kutu icindeki yesil olmayan pikseller
yy,xx=np.mgrid[0:S.shape[0],0:S.shape[1]]
kar=(xx>=292)&(xx<=392)&(yy>=145)&(yy<=318)&~((S[...,1]>S[...,0]*1.12)&(S[...,1]>S[...,2]*1.3))
from scipy import ndimage
kar=ndimage.binary_opening(kar,np.ones((3,3))); kar=ndimage.gaussian_filter(kar.astype(float),1.0)[...,None]
for t,g in zip(zam,guc):
    O=sahne_bindir(S,kare(t,512,g),MERKEZ,CAP)
    O=np.clip(O+duvar(t,CAP,0.42,g,S.shape[1],S.shape[0],MERKEZ)*(1-0.0*kar),0,255)
    # karakter zeminin onunde: zemin halkasini ortsun (alev duvarinin on yarisi karakterin onunde kalir)
    O=O*(1-kar)+np.clip(S+duvar(t,CAP,0.42,g,S.shape[1],S.shape[0],MERKEZ)*0.0,0,255)*kar
    ims.append(Image.fromarray(O.astype(np.uint8)).crop((90,60,600,480)))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),20)
w,h=ims[0].size; c=Image.new("RGB",(w*3+20,h*2+70),(24,24,28)); d=ImageDraw.Draw(c)
d.text((8,6),"Run ates halkasi (ozgun tasarim) — karakterin altinda, eklemeli; zaman serisi",font=F,fill=(255,220,120))
for i,im in enumerate(ims):
    X=(i%3)*(w+10); Y=40+(i//3)*(h+30); c.paste(im,(X,Y)); d.text((X+6,Y+4),"%.1f sn"%zam[i],font=F,fill=(255,255,0))
c.save(os.path.join(ONZ,"rune_onizleme.png"))
Image.fromarray((np.clip(kare(1.2,700),0,1)*255).astype(np.uint8)).save(os.path.join(ONZ,"rune_onizleme_tek.png"))
print(c.size)
