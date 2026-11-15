#!/usr/bin/env python3
"""Kendi skill efektleri: hareketli onizleme (GIF + MP4). Her hucre: efekt oncesi zemin (kayittan medyan) + eklemeli kare.
Kullanim: anim5.py KLASOR -> onizlemeler/efekt5_animasyon.gif / .mp4"""
import os, sys, glob, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar5 import EFEKT, kareler, Y
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),17)
AD={"dokum_yildizlari":"Döküm yıldızları","hide":"Hide","light_feet":"Light Feet","kedi_gozu":"Cat's / Lupine Eyes",
    "evade":"Evade","safety":"Safety","cure":"Cure Disease / Curse","magic_shield":"Magic Shield"}
KIRP=(110,30,610,830); HW,HH=250,400
cache={}; zem={}; ef={}
for ad,v,once,aralik in EFEKT:
    if v not in cache: cache[v]=kareler(os.path.join(sys.argv[1],v+".mp4"))
    zem[ad]=np.median(np.stack([Y(cache[v][1][i]) for i in once]),0)
    ef[ad]=sorted(glob.glob(os.path.join(K,ad,"*.png")))
N=max(len(v) for v in ef.values())+20
d=tempfile.mkdtemp(); kareler_=[]
for t in range(N):
    c=Image.new("RGB",(HW*4,(HH+26)*2),(24,24,28)); dr=ImageDraw.Draw(c)
    for k,(ad,v,once,aralik) in enumerate(EFEKT):
        fs=ef[ad]; i=t%(len(fs)+20)
        E=np.asarray(Image.open(fs[i]).convert("RGB")).astype(np.float32) if i<len(fs) else 0
        im=Image.fromarray(np.clip(zem[ad]+E,0,255).astype(np.uint8)).crop(KIRP).resize((HW,HH),Image.LANCZOS)
        X=(k%4)*HW; Yy=(k//4)*(HH+26); c.paste(im,(X,Yy+26)); dr.text((X+6,Yy+4),AD[ad],font=F,fill=(255,220,120))
    p=os.path.join(d,"a_%04d.png"%t); c.save(p)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","format=yuv420p","-c:v","libx264","-crf","20",
                os.path.join(ONZ,"efekt5_animasyon.mp4")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer",
                os.path.join(ONZ,"efekt5_animasyon.gif")],check=True)
import shutil; shutil.rmtree(d)
print(N,"kare")
