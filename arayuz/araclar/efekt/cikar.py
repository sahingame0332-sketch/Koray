#!/usr/bin/env python3
"""Skill / vurus efektleri: video karelerinden eklemeli (additive) isik katmani.
Kamera sabit (zemin farki < 0.3), efekt toplamsal parlatma (efektte artan piksel 148 971, kararan 4 606):
   E = clip(O - B, 0, 255)       B = efektten hemen onceki karelerin medyani
Unity'de Additive karisimla (Blend One One) ayni zemine eklenince orijinal kare geri gelir.
Duzeltmeler: ad etiketleri (UI, efektin ustunde) ve karakter/mob silueti (efektin onunde) bolgeleri
komsulardan difuzyonla doldurulur; isinmayan koyu artiklar (yaratik animasyonu) silinir.
Kullanim: cikar.py VIDEO      (video kullanicinin kaydi; depoya konmaz — kamera goruntusu iceriyor)"""
import os, sys, json, subprocess, tempfile, glob
import numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(B_,"..","..","kaynak","efekt")
def kareler(video,kutu,i0,i1):
    x,y,w,h=kutu
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vf","crop=%d:%d:%d:%d"%(w,h,x,y),"-vsync","0",d+"/k_%04d.png"],check=True)
        fs=sorted(glob.glob(d+"/k_*.png"))
        return {i:np.asarray(Image.open(fs[i]).convert("RGB")).astype(np.float32) for i in range(i0,i1)}
def doldur(E,m):
    """m icini en yakin bilinen pikselle doldurur, sonra yalniz m icinde yumusatir"""
    if not (~m).any(): return E
    _,(iy,ix)=ndimage.distance_transform_edt(m,return_indices=True)
    F=E[iy,ix]
    for _ in range(6):
        Y=ndimage.uniform_filter(F,[9,9,0]); F=np.where(m[...,None],Y,E)
    return F
def temizle(E,esik=22):
    """isinmayan, sonuk artiklari sil (yaratik animasyonu, sikistirma)"""
    mx=E.max(2); sicak=(E[:,:,0]>=E[:,:,2])
    E=np.where(((mx<esik)|((~sicak)&(mx<70)))[...,None],0,E)
    return ndimage.gaussian_filter(E,[0.6,0.6,0])
def sira(ad,video,kutu,once,i0,i1,adim,maskeler,siluet=None):
    K=kareler(video,kutu,min(once[0],i0),i1)
    B=np.median(np.stack([K[i] for i in range(once[0],once[1],2)]),0)
    os.makedirs(os.path.join(OUT,ad),exist_ok=True)
    for f in glob.glob(os.path.join(OUT,ad,"*.png")): os.remove(f)
    H,W=B.shape[:2]; M=np.zeros((H,W),bool)
    for (a,b,c,d) in maskeler: M[b-kutu[1]:d-kutu[1],a-kutu[0]:c-kutu[0]]=True
    bilgi=[]
    for n,i in enumerate(range(i0,i1,adim)):
        O=K[i]; E=np.clip(O-B,0,255)
        m=M.copy()
        if siluet is not None:                       # efektin onundeki karakter: E dusuk ve ortami parlak efektli
            a,b,c,d=siluet; s=np.zeros((H,W),bool); s[b-kutu[1]:d-kutu[1],a-kutu[0]:c-kutu[0]]=True
            m|=s                                     # karakter/mob: efektin onunde cizilir, isiginda parlar -> tamamen doldurulur
        if m.any(): E=doldur(E,m)
        E=temizle(E)
        Image.fromarray(np.clip(E,0,255).astype(np.uint8)).save(os.path.join(OUT,ad,"%s_%02d.png"%(ad,n)))
        bilgi.append(float(E.max(2).mean()))
    return dict(kare_sayisi=len(bilgi),fps=60.0/adim,ekran_kutu=list(kutu),kaynak_kareler=[i0,i1,adim],ortalama_parlaklik=[round(v,2) for v in bilgi])
if __name__=="__main__":
    v=sys.argv[1]; r={}
    # Pillar of Fire: kare 110..160 (t = 1.83 - 2.67 sn); ad etiketleri UI'dir, efektin ustunde cizilir
    r["ates_sutunu"]=sira("ates_sutunu",v,(800,150,500,710),(96,110),110,162,2,
                          [(855,575,1130,615),(1030,645,1235,722)])
    # karaktere vurus: kare 178..194; 196'dan sonra kayit ekrani karariyor (Kontrol Merkezi) -> efektin sonu kayitta yok
    # isik yaricapi ~200 px (180-182. karelerde) -> genis kutu
    r["vurus"]=sira("vurus",v,(870,560,450,420),(160,176),178,196,2,
                    [(855,575,1130,615),(1030,645,1235,722)],siluet=(1104,730,1152,852))
    json.dump(r,open(os.path.join(OUT,"efekt_bilgisi.json"),"w"),indent=1)
    for k,x in r.items(): print(k,x["kare_sayisi"],"kare",x["fps"],"fps",x["ekran_kutu"])
