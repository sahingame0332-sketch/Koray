#!/usr/bin/env python3
"""Efekt 10 pembe patlama — onaylanan tek kareden (kure_ref_saydam.png) hareketli GIF.
Zamanlama 'patlama_son_hali' klibinden olculdu (30 kare/sn): pembe evre 10 kare (10-19), sari evre 10 kare (20-29), sonra biter.
  0-3   : patlama dogar — kucukten (0.55) tam boya, parlaklik artar
  3-10  : pembe evre — tam boy, hafif genisleme (1.00 -> 1.05)
  10-20 : sari evre — renk sariya doner (#F5F495, klipte merkez #F5F596 -> #EDECCC), yatay isik cizgisi, disari genisleyerek soner
Cikti: kaynak/efekt10/kure_ref/anim_gif/*.png (saydam), onizlemeler/efekt10_patlama.gif (siyah fon, gercek hiz),
efekt10_patlama_saydam.gif, efekt10_patlama_yavas10.mp4"""
import os, subprocess, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure_ref"); ONZ=os.path.join(B_,"..","..","onizlemeler")
src=np.asarray(Image.open(os.path.join(K,"kure_ref_saydam.png")).convert("RGBA")).astype(np.float32)/255
S=src.shape[0]; C=(S-1)/2
L0=src[...,:3]*src[...,3:4]                                                   # isik (on-carpimli)
def olcekle(L,s):
    yy,xx=np.mgrid[0:S,0:S].astype(np.float32); sy=(yy-C)/s+C; sx=(xx-C)/s+C
    return np.stack([ndimage.map_coordinates(L[...,c],[sy,sx],order=1,cval=0) for c in range(3)],-1)
sari=np.array([0xF5,0xF4,0x95],np.float32)/255
yy,xx=np.mgrid[0:S,0:S].astype(np.float32); dx,dy=xx-C,yy-C
def kare(t):
    if t<3:   s=0.55+0.45*(1-(1-t/3)**2); g=0.35+0.65*t/3; y=0
    elif t<10: s=1.0+0.05*(t-3)/7; g=1.0; y=0
    else:
        u=(t-10)/10; s=1.05+0.15*u; g=(1-u)**0.8; y=min(1,u*3.0)
    L=olcekle(L0,s)
    lum=L.max(2,keepdims=True)
    L=L*(1-y)+lum*sari*y                                                      # sariya donus (parlaklik korunur)
    if y>0:                                                                   # yatay isik cizgisi (sari evre)
        uz=S*0.48*(1-0.3*u); boy=np.clip(1-np.abs(dx)/uz,0,1)**0.6
        L=L+(boy*np.exp(-(dy/2.0)**2))[...,None]*sari*0.9*y+(boy*np.exp(-(dy/9)**2))[...,None]*sari*0.3*y
    return np.clip(L*g,0,1)
N=20; od=os.path.join(K,"anim_gif"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
for i in range(N):
    L=kare(i); al=L.max(2); rgb=np.where(al[...,None]>1e-4,L/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(od,"patlama_%02d.png"%i))
    Image.fromarray((L*255).round().astype(np.uint8)).save(os.path.join(od,"siyah_%02d.png"%i))
pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",od+"/siyah_%02d.png","-vf","tpad=stop=10,"+pal,"-loop","0",os.path.join(ONZ,"efekt10_patlama.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",od+"/patlama_%02d.png","-vf","split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=40","-loop","0",os.path.join(ONZ,"efekt10_patlama_saydam.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","%.3f"%(N/10),"-i",od+"/siyah_%02d.png","-vf","fps=30,pad=ceil(iw/2)*2:ceil(ih/2)*2","-c:v","libx264","-crf","12","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_patlama_yavas10.mp4")],check=True)
for e in ("efekt10_patlama.gif","efekt10_patlama_saydam.gif","efekt10_patlama_yavas10.mp4"): print(e,os.path.getsize(os.path.join(ONZ,e))//1024,"KB")
o=Image.new("RGB",(10*160,2*160))
for i in range(N): o.paste(Image.open(os.path.join(od,"siyah_%02d.png"%i)).resize((160,160)),((i%10)*160,(i//10)*160))
o.save(os.path.join(ONZ,"efekt10_patlama_tablo.jpg"),quality=90)
