#!/usr/bin/env python3
"""Item Remove penceresi (tek telefon goruntusu 2712x1220).
Dis kutu (1067,470)-(1763,852) = 696 x 382; cerceve 3 px ten cizgi + 2 px koyu ic cizgi (opak, orijinal piksel).
Ic zemin: duz siyah, alfa 0.92 (sol + ust kenar olcumu: t 0.071-0.087, orta tonda 0.08) -> ayri siyah Image.
OK (1244,774)-(1406,829), Cancel (1427,774)-(1593,829): opak, yazilariyla birlikte orijinal piksel (sabit etiket).
Degisen / ayri yazilar (Text): baslik, soru, esya adi, adet.
Cikti: kaynak/item_remove/pencere.png (cerceve + dugmeler, ici saydam), olculer.json
Kullanim: cikar.py EKRAN.jpg"""
import os, sys, json, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(B_,"..","..","kaynak","item_remove"); os.makedirs(OUT,exist_ok=True)
I=np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float)
X0,Y0,X1,Y1=1067,470,1763,852; CER=5
OK=(1244,774,1406,829); CANCEL=(1427,774,1593,829)
P=I[Y0:Y1,X0:X1]; H,W=P.shape[:2]; yy,xx=np.mgrid[Y0:Y1,X0:X1]
cer=(xx<X0+CER)|(xx>=X1-CER)|(yy<Y0+CER)|(yy>=Y1-CER)
dug=np.zeros_like(cer)
for b in (OK,CANCEL): dug|=(xx>=b[0])&(xx<b[2])&(yy>=b[1])&(yy<b[3])
al=(cer|dug).astype(float)
Image.fromarray(np.dstack([P,al*255]).astype(np.uint8),"RGBA").save(os.path.join(OUT,"pencere.png"))
pj=json.load(open('punto.json')) if os.path.exists('punto.json') else {}
yazi={k:dict(metin=v['metin'],merkez=[v['kutu'][0]+v['kutu'][2]/2-X0,v['kutu'][1]+v['kutu'][3]/2-Y0],renk=v['renk']) for k,v in pj.items() if k in('baslik','soru','esya','adet')}
json.dump(dict(ekran=[2712,1220],sprite=[X0,Y0,W,H],cerceve=CER,ic_alfa=0.92,
    ok=[OK[0]-X0,OK[1]-Y0,OK[2]-OK[0],OK[3]-OK[1]],cancel=[CANCEL[0]-X0,CANCEL[1]-Y0,CANCEL[2]-CANCEL[0],CANCEL[3]-CANCEL[1]],
    font="RobotoSlab-Bold",punto=28,harf_araligi=2.0,yazi=yazi),open(os.path.join(OUT,"olculer.json"),"w"),indent=1)
print('pencere',W,H)
