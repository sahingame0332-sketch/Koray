#!/usr/bin/env python3
"""Efekt 10 — hareketli surum: kullanicinin cizdigi 4 kare + sonrasi referans klipten (patlama_son_hali, 30 kare/sn).
Zaman ölçeği: kullanicinin verdigi saniyeler 10 sn'lik yavas cekime gore (10 sn = 20 gercek kare) -> 1 yavas sn = 2 kare.
  kare 1: 00:00 (k0) · kare 2: 00:04 (k8) · kare 3: (verilmedi; ara: k15) · kare 4: 00:11 (k22)
  sonrasi: klibin sari evresi (klip kareleri 20-30, ayni yontemle cikarilmis isik katmani; kure_ref/anim/kure_NN.png), kare 4 olcegiyle (1.513)
Anahtar kareler arasinda 2 karelik yumusak gecis. Tuval 920x920, merkez ortada; isik toplamali (siyah = saydam).
Cikti: kareler/oynatma/oynat_NN.png (saydam), onizlemeler/efekt10_oynat.gif (gercek hiz), efekt10_oynat_yavas.mp4, efekt10_oynat_tablo.jpg"""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); E=os.path.join(B_,"..","..","kaynak","efekt10"); K=os.path.join(E,"kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
TUVAL=920; OLC4=1.10*1.25*1.10
def yukle(yol,olcek):
    im=Image.open(yol).convert("RGBA"); n=round(im.width*olcek); im=im.resize((n,n),Image.LANCZOS)
    t=Image.new("RGBA",(TUVAL,TUVAL),(0,0,0,0)); t.alpha_composite(im,((TUVAL-n)//2,(TUVAL-n)//2))
    a=np.asarray(t).astype(np.float32)/255; return a[...,:3]*a[...,3:4]          # isik (on-carpimli)
anahtar=[(0,yukle(os.path.join(K,"olcekli","kare_01.png"),1.0)),
         (8,yukle(os.path.join(K,"olcekli","kare_02.png"),1.0)),
         (15,yukle(os.path.join(K,"olcekli","kare_03.png"),1.0))]
klip=[yukle(os.path.join(E,"kure_ref","anim","kure_%02d.png"%n),OLC4) for n in range(20,30)]
for i,L in enumerate(klip): anahtar.append((24+i,L))                                   # k23 gecis, k24.. klip sari evre
son=24+len(klip)-1
for j,g in enumerate((0.6,0.35,0.15)): anahtar.append((son+1+j,klip[-1]*g))              # klibin son karesi 3 karede soner
anahtar.append((son+4,np.zeros_like(klip[0])))
N=anahtar[-1][0]+1
def kare(t):
    for (t0,A),(t1,B) in zip(anahtar[:-1],anahtar[1:]):
        if t0<=t<=t1:
            gec=2 if t1-t0>2 else (t1-t0)                                               # tutma, son 2 karede gecis
            u=np.clip((t-(t1-gec))/gec,0,1) if gec>0 else 0
            return A*(1-u)+B*u
    return anahtar[-1][1]
od=os.path.join(K,"oynatma"); os.makedirs(od,exist_ok=True)
for f in os.listdir(od): os.remove(os.path.join(od,f))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),22)
for t in range(N):
    L=np.clip(kare(t),0,1); al=L.max(2); rgb=np.where(al[...,None]>1e-4,L/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(od,"oynat_%02d.png"%t))
    s=Image.fromarray((L*255).round().astype(np.uint8)).resize((460,460),Image.LANCZOS)
    ImageDraw.Draw(s).text((8,6),"kare %d/%d  (yavas %.1f sn)"%(t+1,N,t/2),font=F,fill=(150,150,150)); s.save(os.path.join(od,"siyah_%02d.png"%t))
pal="split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a"
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",od+"/siyah_%02d.png","-vf","tpad=stop=12,"+pal,"-loop","0",os.path.join(ONZ,"efekt10_oynat.gif")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","2","-i",od+"/siyah_%02d.png","-vf","fps=30","-c:v","libx264","-crf","12","-pix_fmt","yuv420p",os.path.join(ONZ,"efekt10_oynat_yavas.mp4")],check=True)
o=Image.new("RGB",(8*230,((N+7)//8)*230))
for t in range(N): o.paste(Image.open(os.path.join(od,"siyah_%02d.png"%t)).resize((230,230)),((t%8)*230,(t//8)*230))
o.save(os.path.join(ONZ,"efekt10_oynat_tablo.jpg"),quality=88); print("tamam",N,"kare")
