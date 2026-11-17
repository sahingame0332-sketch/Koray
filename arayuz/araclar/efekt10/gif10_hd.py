#!/usr/bin/env python3
"""Efekt 10 HD (kayit 21-09-10, kareler 578-616, 60 kare/sn TUM kareler, 1:1 piksel):
mob kucuk ve alcak -> aura neredeyse hic kapanmiyor; doldurma yalniz kucuk mob silueti icin.
Temizlenen: baska yuruyen mob (renksiz gri leke), mob hasar kirmizisi, mob silueti (komsu isik; parlama bandi satir satir).
Ciktilar: kaynak/efekt10/hd/temiz/*.png (kayipsiz), onizlemeler/efekt10_hd.gif (gercek hiz, 1:1),
efekt10_hd_yavas10.mp4 + .gif (10 sn, kare tutma = karistirma yok, net)."""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","hd"); ONZ=os.path.join(B_,"..","..","onizlemeler")
J=json.load(open(os.path.join(K,"bilgi.json"))); X,Y,W,H=J["kutu_ekran"]
rm=np.load(os.path.join(K,"mob_maskesi.npy")); mobd=ndimage.binary_dilation(rm,np.ones((5,5)))
yy,xx=np.mgrid[0:H,0:W]; sx=xx+X; sy=yy+Y
AURA=(1636,722); AURA_R=105; PARLAMA_Y=724; ILK=3                                  # ilk 3 kare (575-577) efektsiz
r=np.hypot(sx-AURA[0],sy-AURA[1])
fs=sorted(glob.glob(os.path.join(K,"skill","skill_*.png")))[ILK:]
Ls=np.median([np.asarray(Image.open(f).convert("RGB"),dtype=np.float32).max(2) for f in fs[8:22]],0)
kar=(Ls<0.35*ndimage.gaussian_filter(Ls,10))&(r<AURA_R*0.8)
lb,n=ndimage.label(kar|rm); dok=np.unique(lb[rm]); dok=dok[dok>0]
MOB=ndimage.binary_closing(ndimage.binary_dilation(np.isin(lb,dok)|mobd,np.ones((3,3))),np.ones((7,7)))
band=np.abs(sy-PARLAMA_Y)<7
out=[]
for f in fs:
    E=np.asarray(Image.open(f).convert("RGB"),dtype=np.float32); mx=np.maximum(E.max(2),1)
    doy=(mx-E.min(2))/mx
    gri=((doy<0.35)|((doy<0.6)&(mx<60)&(E[...,2]>=E[...,0]*0.8)))&(mx>6)&(mx<90)&(r>AURA_R*1.1)                                        # yuruyen diger mob / govde izleri (renksiz)
    lbg,ng=ndimage.label(ndimage.binary_dilation(gri,np.ones((5,5))))
    if ng:
        sz=ndimage.sum(gri,lbg,range(1,ng+1)); pk=ndimage.maximum(mx,lbg,range(1,ng+1)); gri=np.isin(lbg,1+np.where((sz>40)&(np.array(pk)<110))[0])
    E=np.where(ndimage.binary_dilation(gri,np.ones((5,5)))[...,None],0,E)
    kir=ndimage.binary_dilation((E[...,0]>2.0*E[...,1]+6)&(E[...,0]>1.8*E[...,2]+6),np.ones((3,3)))
    hed=MOB|(kir&(r<AURA_R*1.2))
    kay=hed|band
    F=yumusak_doldur(np.where(kay[...,None],0,E),kay,n=10,k=7)
    Hh=E.copy(); xs_=np.arange(W)
    for yb in np.where(band.any(1))[0]:
        bil=~hed[yb]
        if bil.sum()>2:
            for c in range(3): Hh[yb,:,c]=np.interp(xs_,xs_[bil],E[yb,bil,c])
    F=np.where(band[...,None],np.maximum(Hh,F),F)
    w=np.maximum(ndimage.gaussian_filter(hed.astype(np.float32),1.5),hed)[...,None]
    E=F*w+E*(1-w)
    E=np.where((kir&(r>=AURA_R*1.2))[...,None],0,E)
    out.append(np.clip(E,0,255))
son=out[-1]; out+=[son*a for a in (0.75,0.55,0.38,0.24,0.13,0.06)]                # kayitta sonraki vurus geliyor: 6 kare (0.1 sn) sondurme
M=np.max([k.max(2) for k in out],0); ys,xs=np.nonzero(M>6)
a,b,c,d=max(0,xs.min()-16),max(0,ys.min()-16),min(W,xs.max()+17),min(H,ys.max()+17)
a,c=a-(c-a)%2*0,c+(c-a)%2; d=d+(d-b)%2
od=os.path.join(K,"temiz"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
for j,A in enumerate(out): Image.fromarray(A[b:d,a:c].round().astype(np.uint8)).save(os.path.join(od,"efekt10_hd_%02d.png"%j))
print("kutu",(X+a,Y+b,c-a,d-b),"kare",len(out))
pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=none"
g=os.path.join(ONZ,"efekt10_hd.gif")
subprocess.run(["ffmpeg","-v","error","-y","-framerate","60","-i",od+"/efekt10_hd_%02d.png","-vf","tpad=stop=24,"+pal,"-loop","0",g],check=True)
# 10 sn yavas cekim: kare tutma (karistirma yok), 2x buyutme (yakin komsu degil lanczos), sol ustte kare no
F_=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),22)
t=tempfile.mkdtemp(); n=len(out)
for j in range(n):
    im=Image.open(os.path.join(od,"efekt10_hd_%02d.png"%j)).convert("RGB"); im=im.resize((im.width*2,im.height*2),Image.LANCZOS)
    ImageDraw.Draw(im).text((10,8),"kare %d/%d   ~1/%.0f hiz"%(j+1,n,10/(n/60)),font=F_,fill=(140,140,140)); im.save(os.path.join(t,"a_%03d.png"%j))
fr="%.5f"%(n/10.0)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",fr,"-i",t+"/a_%03d.png","-vf","fps=30","-c:v","libx264","-preset","slow","-crf","8","-pix_fmt","yuv444p",os.path.join(ONZ,"efekt10_hd_yavas10.mp4")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",fr,"-i",t+"/a_%03d.png","-vf","fps=30","-c:v","libx264","-preset","slow","-crf","12","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_hd_yavas10_uyumlu.mp4")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate",fr,"-i",t+"/a_%03d.png","-vf",pal,"-loop","0",os.path.join(ONZ,"efekt10_hd_yavas10.gif")],check=True)
shutil.rmtree(t)
for e in ("efekt10_hd.gif","efekt10_hd_yavas10.mp4","efekt10_hd_yavas10_uyumlu.mp4","efekt10_hd_yavas10.gif"): print(e,os.path.getsize(os.path.join(ONZ,e))//1024,"KB")
tw=240; ims=[Image.open(os.path.join(od,"efekt10_hd_%02d.png"%j)) for j in range(0,n,2)]; th=int(tw*ims[0].height/ims[0].width)
o=Image.new("RGB",(8*tw,((len(ims)+7)//8)*th))
for j,im in enumerate(ims): o.paste(im.resize((tw,th)),((j%8)*tw,(j//8)*th))
o.save(os.path.join(ONZ,"efekt10_hd_tablo.jpg"),quality=92)
