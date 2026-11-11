#!/usr/bin/env python3
"""Videonun [t0,t1] araligindaki karelerinin piksel medyanini alir (H.265 gurultusunu bastirir)."""
import sys, subprocess, tempfile, glob, os, numpy as np
from PIL import Image
def medyan(video,t0,t1,cikti,azami=24):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t0),"-i",video,"-t",str(t1-t0),"-vsync","0",d+"/k_%04d.png"],check=True)
        fs=sorted(glob.glob(d+"/k_*.png"))
        if len(fs)>azami: fs=fs[::max(1,len(fs)//azami)][:azami]
        st=np.stack([np.asarray(Image.open(f).convert("RGB")) for f in fs])
        m=np.median(st,axis=0).astype(np.uint8)
        Image.fromarray(m).save(cikti)
        return len(fs), float(st.std(0).mean())
if __name__=="__main__":
    v,t0,t1,c=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
    n,s=medyan(v,t0,t1,c); print("%s  kare=%d  ort.std=%.2f"%(c,n,s))
