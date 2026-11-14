#!/usr/bin/env python3
"""Dorduncu efekt: moba uygulanan "Manes Of Fire" (tablet kaydi 2266x1488, 60 kare/sn, 21-40-04; depoya konmaz).
Gokten inen ince turuncu isin + dusen kirmizi prizma + mobun uzerinde yanan ates + yerde donen sari run halkalari.
Kamera kare 100-235 arasi sabit. Zemin B = efekt oncesi 100-118 (mob ve secim halkasi ayni yerde).
2 karede bir -> 30 kare/sn. Temizlik cikar2.sira ile ayni (UI maskeleri, karakter silueti, kararan/sicak olmayan pikseller).
Kullanim: cikar4.py VIDEO"""
import os, sys, json
from cikar import OUT
from cikar2 import sira
KUTU=(1215,0,520,940)
if __name__=="__main__":
    v=sys.argv[1]; p=os.path.join(OUT,"efekt_bilgisi.json"); r=json.load(open(p)) if os.path.exists(p) else {}
    r["manes_of_fire"]=sira("manes_of_fire",v,KUTU,range(100,119),list(range(118,216,2)),
        maskeler=[(1215,686,1364,774),(1292,604,1562,652)],siluet=[(1215,690,1262,880)],fps_kayit=60.0)
    r["manes_of_fire"].update(kaynak="tablet 2266x1488, 60 kare/sn",mob_ayagi=[1405,822],mob_boyu_px=140)
    json.dump(r,open(p,"w"),indent=1); print(r["manes_of_fire"]["kare_sayisi"],"kare",r["manes_of_fire"]["fps"],"fps")
