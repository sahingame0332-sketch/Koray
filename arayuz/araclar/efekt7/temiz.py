#!/usr/bin/env python3
"""Efekt 7 eki: arka katmandaki on-plan ortusu (cit cubuklari, direk) dolgusu. Efekt 7 kareleri DEGISMEZ; yeni klasor <ad>_arka_temiz.
Aura dunyada mobun ve citin ARKASINDA: kayitta citin ince dikey cubuklari aurayi koyu cizgiler halinde kesiyor. Unity'de derinlik
testi ortecegi icin dokuda bu izler olmamali. Yatay gri kapanis (genislik 11) ince cubuklari doldurur; mob silueti (genis) kalir,
sonra mob silueti icini zaten mob ortecek."""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
K7=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt7")
B=json.load(open(os.path.join(K7,"bilgi.json")))
for ad in ("kesik_aura","yildiz","kesik_aura_tum","yildiz_tum"):
    s=os.path.join(K7,"%s_arka"%ad); d=os.path.join(K7,"%s_arka_temiz"%ad); os.makedirs(d,exist_ok=True)
    for f in sorted(os.listdir(s)):
        E=np.asarray(Image.open(os.path.join(s,f)).convert("RGB"),dtype=np.float32)
        C=np.stack([ndimage.grey_closing(E[...,c],size=(1,11)) for c in range(3)],-1)
        C=np.stack([ndimage.grey_closing(C[...,c],size=(5,1)) for c in range(3)],-1)
        Image.fromarray(np.clip(np.maximum(E,C),0,255).astype(np.uint8)).save(os.path.join(d,f.replace("_arka_","_arka_temiz_")))
    B[ad]["arka_temiz"]=B[ad]["arka"]; print(ad,len(os.listdir(d)))
json.dump(B,open(os.path.join(K7,"bilgi.json"),"w"),indent=1)
