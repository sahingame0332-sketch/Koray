#!/usr/bin/env python3
"""Efekt 10 — tam GIF (kullanici): toplam 0.65 sn, 60 kare/sn -> 39 kare. Cizilen anahtar kareler (olcekli/, ayni tuval) sirasiyla:
  kare1 0-7 · kare2 8-15 · kare3 16-21 · kare4 22-25 · ara (parantezler disari, yarim) 26-27 · kare5 28-30 ·
  sonrasi (31-38): isin yanlara uzar ve soner, kure daha hizli soner (kare 5'ten turetilir)
Anahtar kareler arasinda 1 karelik yumusak gecis. Cikti: kareler/gif/efekt10_NN.png (saydam), onizlemeler/efekt10_patlama_tam.gif, _yavas.mp4, _tablo.jpg"""
import os, subprocess, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
CIK=900                                                                  # cikti tuvali (olcekli 2020'den kirpilip kucultulur)
def yukle(ad):
    a=np.asarray(Image.open(os.path.join(K,"olcekli",ad)).convert("RGBA")).astype(np.float32)/255
    return a[...,:3]*a[...,3:4]
k={n:yukle(ad) for n,ad in [(1,"kare_01.png"),(2,"kare_02.png"),(3,"kare_03.png"),(4,"kare_04.png"),("a","kare_04b_ara.png"),(5,"kare_05.png")]}
plan=[(1,0,7),(2,8,15),(3,16,21),(4,22,25),("a",26,27),(5,28,30)]
N=39; TV=k[1].shape[0]; c=(TV-1)/2
yy,xx=np.mgrid[0:TV,0:TV].astype(np.float32); dx,dy=xx-c,yy-c; R=np.hypot(dx,dy)
k5=k[5]; kure=np.clip(1-(np.abs(dy)>60)*0+0,0,1)
# kare 5'te isin ile kure ayrimi: isin = yatay bant (|dy|<~200 olcekli) ve sari; kure = gerisi
sar=np.clip((k5[...,1]-0.85*k5[...,0])/0.1+0.5,0,1)*np.clip((k5.max(2)-0.3)/0.3,0,1)
isin_m=ndimage.gaussian_filter(np.maximum(sar,(np.abs(dy)<40)*(np.abs(dx)>c*0)*1.0)*1.0,3)
def sonra(u):                                                             # u: 0..1 (31..38)
    s=1+0.35*u                                                            # isin yatayda uzar
    ix=np.stack([ndimage.map_coordinates(k5[...,ch],[yy,c+dx/s],order=1) for ch in range(3)],-1)
    im=np.stack([ndimage.map_coordinates(isin_m,[yy,c+dx/s],order=1)],-1)
    isin=ix*im*(1-u)**1.2
    kure=k5*(1-isin_m[...,None])*(1-u)**2.2
    return np.clip(1-(1-isin)*(1-kure),0,1)
kareler=[]
for t in range(N):
    if t<=30:
        for i,(n,a0,a1) in enumerate(plan):
            if a0<=t<=a1:
                F=k[n]
                if t==a1 and i+1<len(plan): F=0.5*F+0.5*k[plan[i+1][0]]      # 1 karelik gecis
                break
    else: F=sonra((t-30)/8)
    kareler.append(F)
x0=int(c-1000); x1=int(c+1000); y0=int(c-560); y1=int(c+560)                          # kure ve isin sigsin
od=os.path.join(K,"gif"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
for t,F in enumerate(kareler):
    F=F[max(0,y0):y1,max(0,x0):x1]
    al=F.max(2); rgb=np.where(al[...,None]>1e-4,F/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(od,"efekt10_%02d.png"%t))
    Image.fromarray((F*255).round().astype(np.uint8)).resize((1000,560),Image.LANCZOS).save(os.path.join(od,"siyah_%02d.png"%t))
pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
subprocess.run(["ffmpeg","-v","error","-y","-framerate","60","-i",od+"/siyah_%02d.png","-vf",pal,"-loop","0",os.path.join(ONZ,"efekt10_patlama_tam.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","4","-i",od+"/siyah_%02d.png","-vf","fps=30","-c:v","libx264","-crf","14","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_patlama_tam_yavas.mp4")],check=True)
o=Image.new("RGB",(8*225,5*126))
for t in range(N): o.paste(Image.open(os.path.join(od,"siyah_%02d.png"%t)).resize((225,126)),((t%8)*225,(t//8)*126))
o.save(os.path.join(ONZ,"efekt10_patlama_tam_tablo.jpg"),quality=88)
d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(ONZ,"efekt10_patlama_tam.gif")],capture_output=True,text=True).stdout.strip()
print("tamam",N,"kare, sure",d)
