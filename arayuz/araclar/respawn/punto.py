#!/usr/bin/env python3
"""Respawn yazilari: font + punto (oyun_ici/punto.py IoU yontemi)."""
import os, sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","oyun_ici"))
import punto as P
import numpy as np
from PIL import Image
P.REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","referans_gorseller","respawn")
LS="/usr/share/fonts/truetype/liberation/"
P.ADAY.update({"LiberationSans-Bold":LS+"LiberationSans-Bold.ttf"})
O=np.asarray(Image.open(os.path.join(P.REF,"respawn.jpg")).convert("RGB")).astype(float)
for ad,t,k in (("baslik","Respawn",(2240,670,2440,705)),("satir1","Press OK to teleport back to there re-",(2040,710,2640,745)),
               ("satir2","spawn point.",(2240,748,2440,785)),("dugme","Confirm",(2280,964,2398,992))):
    b=O[k[1]:k[3],k[0]:k[2]]; l=b.max(2); m=l>np.percentile(l,90); c=np.median(b[m],0)
    ys,xs=np.nonzero(np.abs(b-c).max(2)<60)
    print(ad,"renk #%02X%02X%02X"%tuple(int(v) for v in c),"murek x %d-%d y %d-%d"%(k[0]+xs.min(),k[0]+xs.max(),k[1]+ys.min(),k[1]+ys.max()))
    P.olc(ad,t,"respawn",k,tuple(c),tol=60)
