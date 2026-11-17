#!/usr/bin/env python3
"""Efekt 10 GIF'lerinin 10 saniyelik yavas cekim onizlemesi: kayittan cikan kareler 10 sn'ye yayilir,
araya kareler arasi karisim (ffmpeg framerate filtresi) konur ki akici gorunsun; sol ustte kaynak kare numarasi."""
import os, glob, subprocess, tempfile, shutil
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),18)
for ad,d,on in (("efekt10_tam_yavas",os.path.join(K,"tam","gif"),"efekt10_tam_"),("efekt10_yavas",os.path.join(K,"gif"),"efekt10_")):
    fs=sorted(glob.glob(os.path.join(d,on+"[0-9][0-9].png"))); n=len(fs); t=tempfile.mkdtemp()
    for j,f in enumerate(fs):
        im=Image.open(f).convert("RGB"); im=im.resize((640,int(640*im.height/im.width)//2*2),Image.LANCZOS)
        ImageDraw.Draw(im).text((8,6),"kare %d/%d  (1/%.0f hiz)"%(j+1,n,10/(n/30)),font=F,fill=(150,150,150))
        im.save(os.path.join(t,"a_%03d.png"%j))
    out=os.path.join(ONZ,ad+".gif")
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","%.5f"%(n/10.0),"-i",t+"/a_%03d.png",
        "-vf","framerate=fps=20:interp_start=0:interp_end=255,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a",
        "-loop","0",out],check=True)
    shutil.rmtree(t)
    d_=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip()
    print(ad,n,"kare ->",d_,"sn",os.path.getsize(out)//1024,"KB")
