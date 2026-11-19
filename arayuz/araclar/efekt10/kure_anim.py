#!/usr/bin/env python3
"""Efekt 10 pembe patlama — onaylı birinci kareden (kareler/kare_01.png) hareketli surum, klipteki akisla
(patlama_son_hali, 30 kare/sn; olculen: pembe evre 10 kare, sari evre 10 kare):
  0      : patlama ANINDA tam boyda ve en parlak cikar (klipte buyume yok)
  0-9    : pembe evre — kare_01; hafif genisleme (1.00 -> 1.06), parlaklik hafif titresim
  10-12  : sariya donus — renk sariya (#F5F495) kayar, ortadan GENIS YATAY SARI PARLAMA dogar (klipte ekranin yarisini kaplar)
  12-19  : sari parlama ve kure disari genisleyerek soner
Tuval 1208x604 (yatay parlama sigsin), merkez ortada. Isik toplamali (siyah fon = saydam).
Cikti: kaynak/efekt10/kareler/anim/*.png (saydam) + onizlemeler/efekt10_patlama.gif, _saydam.gif, _yavas10.mp4, _tablo.jpg"""
import os, subprocess, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
src=np.asarray(Image.open(os.path.join(K,"kare_01.png")).convert("RGBA")).astype(np.float32)/255
S=src.shape[0]; W,H=2*S,S
L0=np.zeros((H,W,3),np.float32); L0[:,S//2:S//2+S]=src[...,:3]*src[...,3:4]   # isik (on-carpimli), genis tuvalde
cy,cx=(H-1)/2,(W-1)/2; yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx,dy=xx-cx,yy-cy
SARI=np.array([0xF5,0xF4,0x95],np.float32)/255
def olcekle(L,s):
    return np.stack([ndimage.map_coordinates(L[...,c],[dy/s+cy,dx/s+cx],order=1,cval=0) for c in range(3)],-1)
def kare(t):
    if t<10:                                         # pembe evre
        s=1.0+0.06*t/9; g=1.0-0.04*(t%2); y=0.0; p=0.0
    else:                                            # sari evre
        u=(t-10)/9; s=1.06+0.20*u; g=(1-u)**0.9; y=min(1.0,(t-9)/3); p=min(1.0,(t-9)/2)*(1-u)**1.2
    L=olcekle(L0,s)
    lum=L.max(2,keepdims=True); L=L*(1-y)+lum*SARI*y
    if p>0:                                          # genis yatay sari parlama: cekirdek cizgi + genis yatay hale
        hx=S*(0.9+0.4*min(1,(t-9)/4))
        cizgi=np.exp(-(dy/2.5)**2)*np.clip(1-np.abs(dx)/hx,0,1)**0.7
        hale=np.exp(-(dy/(S*0.20))**2)*np.exp(-(dx/(hx*0.75))**2)
        L=L+(cizgi[...,None]*1.3+hale[...,None]*1.4)*SARI*p
    return np.clip(L*g,0,1)
N=20; od=os.path.join(K,"anim"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
for i in range(N):
    L=kare(i); al=L.max(2); rgb=np.where(al[...,None]>1e-4,L/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(od,"patlama_%02d.png"%i))
    Image.fromarray((L*255).round().astype(np.uint8)).save(os.path.join(od,"siyah_%02d.png"%i))
pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",od+"/siyah_%02d.png","-vf","tpad=stop=10,scale=900:-2,"+pal,"-loop","0",os.path.join(ONZ,"efekt10_patlama.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",od+"/patlama_%02d.png","-vf","scale=900:-2,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=40","-loop","0",os.path.join(ONZ,"efekt10_patlama_saydam.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","%.3f"%(N/10),"-i",od+"/siyah_%02d.png","-vf","fps=30","-c:v","libx264","-crf","12","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_patlama_yavas10.mp4")],check=True)
o=Image.new("RGB",(5*320,4*160))
for i in range(N): o.paste(Image.open(os.path.join(od,"siyah_%02d.png"%i)).resize((320,160)),((i%5)*320,(i//5)*160))
o.save(os.path.join(ONZ,"efekt10_patlama_tablo.jpg"),quality=90)
print("tamam")
