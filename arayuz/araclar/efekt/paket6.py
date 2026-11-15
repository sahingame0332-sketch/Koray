#!/usr/bin/env python3
"""Altinci set -> Unity kaynak klasoru: kareleri kopyalar, olculeri hesaplar, kurucuyu (Editor) yazar, referans .jpg'leri keser.
Kullanim: paket6.py VIDEO   (VIDEO yalniz referans kesitleri icin; depoya konmaz)"""
import os, sys, json, glob, shutil, subprocess, tempfile
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt")
R=os.path.join(B_,"..","..","unity_kaynak","Assets","OlymposYakinSkill1298")
AYAK=(1360,828); BOY=243.0; UFUK=261.0          # ayak (ekran), boy (px), zemin ufku: olcek(y) = (y-UFUK)/(AYAK.y-UFUK) (secim halkalarindan)
AD={"stroke":"Stroke","stab":"Stab","stab2":"Stab2"}
bil=json.load(open(os.path.join(K,"efekt_bilgisi.json")))
satir=[]; olcu={}
for ad in ("stroke","stab","stab2"):
    b=bil["yakin_"+ad]
    for kn,kb in b["katmanlar"].items():
        x,y,w,h=kb["kutu_ekran"]
        cap=AYAK if kn=="karakter" else tuple(b["hedef"])
        olcek=(cap[1]-UFUK)/(AYAK[1]-UFUK)
        gen=w/(BOY*olcek); piv=((cap[0]-x)/w, 1-(cap[1]-y)/h)
        ust=0.08 if (kn=="hedef" and y==0) else 0.0          # isin kaydin ustunde kesiliyor
        d=os.path.join(R,"Textures","%s_%s"%(ad,kn)); shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
        fs=sorted(glob.glob(os.path.join(K,"yakin_%s_%s"%(ad,kn),"*.png")))
        for f in fs: shutil.copy(f,os.path.join(d,os.path.basename(f)))
        olcu["%s_%s"%(ad,kn)]=dict(kutu_ekran=[x,y,w,h],capa_ekran=list(cap),derinlik_olcegi=round(olcek,4),genislik_karakter=round(gen,4),
                                   en_boy=round(h/w,4),pivot=[round(piv[0],4),round(piv[1],4)],ust_sonum=ust,kare=len(fs))
        satir.append('            new Katman("%s", "%s", %.4ff, %.4ff, %.4ff, %.4ff, %.2ff),'%(ad,kn,gen,h/w,piv[0],piv[1],ust))
        print(ad,kn,olcu["%s_%s"%(ad,kn)])
json.dump(dict(kaynak="telefon kaydi 2712x1220, 30 kare/sn",karakter_ayak_ekran=AYAK,karakter_boyu_px=BOY,zemin_ufku_y=UFUK,
               aciklama="genislik_karakter: kare genisligi / (karakter boyu * derinlik olcegi). Hedef katmani hedefin derinliginde olculdu.",
               katmanlar=olcu),open(os.path.join(R,"yakin_skill_olculer.json"),"w"),indent=1,ensure_ascii=False)
cs=open(os.path.join(B_,"paket6_kurucu.cs.tmpl"),encoding="utf-8").read().replace("//KATMANLAR//","\n".join(satir))
open(os.path.join(R,"Editor","OlymposYakinSkillBuilder.cs"),"w",encoding="utf-8").write(cs)
# referans: her skill'in en dolu karesi (orijinal kayittan, efekt bolgesi)
rd=os.path.join(R,"Referans"); shutil.rmtree(rd,ignore_errors=True); os.makedirs(rd)
t=tempfile.mkdtemp()
for ad in ("stroke","stab","stab2"):
    b=bil["yakin_"+ad]; k0=b["kaynak_kareler"][0]
    ps=[max(kb["parlaklik"]) for kb in b["katmanlar"].values()]
    pk=list(b["katmanlar"].values())[0]["parlaklik"]; j=max(range(len(pk)),key=lambda i:sum(kb["parlaklik"][i] for kb in b["katmanlar"].values()))
    subprocess.run(["ffmpeg","-v","error","-y","-i",sys.argv[1],"-vf","fps=30,select=eq(n\\,%d),crop=1500:1140:560:0"%(k0+j),"-frames:v","1",os.path.join(t,"r.png")],check=True)
    Image.open(os.path.join(t,"r.png")).convert("RGB").save(os.path.join(rd,"%s.jpg"%ad),quality=90)
shutil.rmtree(t)
