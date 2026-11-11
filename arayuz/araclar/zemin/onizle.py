#!/usr/bin/env python3
"""Cikarilan karolari, olculen kamerayla ayni ekran bolgesine yeniden cizer (Unity shader'inin
yaptigi is: dunya XZ -> karo UV) ve orijinalle yan yana koyar.  Cikti: onizlemeler/zemin_onizleme.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from zemin import *
ONZ=os.path.join(B,"..","..","onizlemeler"); KF=os.path.join(B,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf")
def karo(ad): return np.asarray(Image.open(os.path.join(OUT,"dokular","zemin_%s.png"%ad)).convert("RGB")).astype(np.float32)
def ciz(kare,yh,kutu,katman,ss=4):
    """katman(X,Z) -> (karo adi dizisi indeks haritasi). kutu: ekran bolgesi"""
    img=yukle(os.path.join(REF,kare)); H,W=img.shape[:2]; f=odak(H); phi=np.arctan((H/2-yh)/f)
    x0,y0,x1,y1=kutu; out=np.zeros((y1-y0,x1-x0,3),np.float32)
    for sy in range(ss):
        for sx in range(ss):
            xs,ys=np.meshgrid(np.arange(x0,x1)+(sx+0.5)/ss,np.arange(y0,y1)+(sy+0.5)/ss)
            X,Z=geri(xs,ys,f,phi,W/2,H/2)
            out+=katman(X,Z)
    return img[y0:y1,x0:x1],out/(ss*ss)
def ornek(ad,X,Z,rapor):
    T=karo(ad); N=T.shape[0]; b=rapor[ad]["karo_birim"]
    u=np.mod(X/b,1)*N; v=np.mod(-Z/b,1)*N
    u0=np.floor(u).astype(int)%N; v0=np.floor(v).astype(int)%N; u1=(u0+1)%N; v1=(v0+1)%N
    fu=(u-np.floor(u))[...,None]; fv=(v-np.floor(v))[...,None]
    return T[v0,u0]*(1-fu)*(1-fv)+T[v0,u1]*fu*(1-fv)+T[v1,u0]*(1-fu)*fv+T[v1,u1]*fu*fv
def main():
    rapor=json.load(open(os.path.join(OUT,"zemin_olcumleri.json")))
    F=lambda p: ImageFont.truetype(KF,p)
    paneller=[]
    o,y=ciz("hud_ekranlar/hud_01.png",232,(300,600,1020,900),lambda X,Z: ornek("kum",X,Z,rapor)); paneller.append(("Kum (Diez)",o,y,["kum"]))
    # Moradon yolu: seritler hud_04'te olculdu (birim): doseme | tugla 0.86 | arnavut
    def yol(X,Z,x_tugla,x_arnavut):
        a=ornek("tas_doseme",X,Z,rapor); b=ornek("tas_tugla",X,Z,rapor); c=ornek("tas_arnavut",X,Z,rapor)
        return np.where((X<x_tugla)[...,None],a,np.where((X<x_arnavut)[...,None],b,c))
    o,y=ciz("hud_ekranlar/hud_04.png",470,(60,650,1040,912),lambda X,Z: yol(X,Z,-2.37,-1.41)); paneller.append(("Taş yol (Moradon): döşeme · tuğla · arnavut",o,y,["tas_doseme","tas_tugla","tas_arnavut"]))
    o,y=ciz("oyun_ici/v2_hedef.jpg",150,(200,640,1250,1040),lambda X,Z: ornek("cim",X,Z,rapor)); paneller.append(("Çim (kır)",o,y,["cim"]))
    W=1660; satirlar=[]
    for bas,o,y,adlar in paneller:
        h=o.shape[0]; w=o.shape[1]; sc=min(1.0,700/w); wi,hi=int(w*sc),int(h*sc)
        c=Image.new("RGB",(W,hi+66),(24,24,28)); d=ImageDraw.Draw(c)
        d.text((10,6),bas,font=F(22),fill=(255,220,120)); d.text((10,36),"ORİJİNAL",font=F(15),fill=(200,200,200)); d.text((720,36),"YENİ (karo + aynı kamera)",font=F(15),fill=(140,230,140))
        c.paste(Image.fromarray(np.clip(o,0,255).astype(np.uint8)).resize((wi,hi),Image.LANCZOS),(10,58))
        c.paste(Image.fromarray(np.clip(y,0,255).astype(np.uint8)).resize((wi,hi),Image.LANCZOS),(720,58))
        x=1430
        for a in adlar:
            t=Image.open(os.path.join(OUT,"dokular","zemin_%s.png"%a)).convert("RGB"); t=t.resize((128,128),Image.LANCZOS) if len(adlar)>1 else t.resize((200,200),Image.LANCZOS)
            yy=58+ (0 if len(adlar)==1 else 0)
            r=rapor[a]
            if len(adlar)==1:
                c.paste(t,(1430,58)); d.rectangle([1430,264,1630,290],fill=tuple(r["srgb"]))
                d.text((1430,294),"%s · %d K · %.1f boy"%(r["hex"],r["cct_K"],r["karo_karakter_boyu"]),font=F(14),fill=(230,230,230))
        if len(adlar)>1:
            c2=Image.new("RGB",(W,hi+66+150),(24,24,28)); c2.paste(c,(0,0)); d=ImageDraw.Draw(c2); x=10
            for a in adlar:
                r=rapor[a]; t=Image.open(os.path.join(OUT,"dokular","zemin_%s.png"%a)).convert("RGB").resize((128,128),Image.LANCZOS)
                c2.paste(t,(x,hi+72)); d.rectangle([x+136,hi+72,x+176,hi+200],fill=tuple(r["srgb"]))
                d.text((x+184,hi+76),a,font=F(16),fill=(255,220,120)); d.text((x+184,hi+100),"%s · %d K"%(r["hex"],r["cct_K"]),font=F(14),fill=(230,230,230))
                d.text((x+184,hi+122),"karo = %.1f karakter boyu"%r["karo_karakter_boyu"],font=F(14),fill=(230,230,230)); x+=540
            c=c2
        satirlar.append(c)
    # ortam renkleri
    c=Image.new("RGB",(W,150),(24,24,28)); d=ImageDraw.Draw(c); d.text((10,6),"Gök ve uzak renk (ölçülen)",font=F(22),fill=(255,220,120)); x=10
    for ad,o in rapor["_ortam"].items():
        for k in ("gok","uzak"):
            h=o[k]; d.rectangle([x,44,x+110,104],fill=(int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)))
            d.text((x,108),"%s %s"%(ad,k),font=F(14),fill=(230,230,230)); d.text((x,126),"%s · %d K"%(h,o[k+"_olcum"]["cct_K"]),font=F(13),fill=(190,190,190)); x+=270
    satirlar.append(c)
    Ht=sum(s.height+8 for s in satirlar); o=Image.new("RGB",(W,Ht),(24,24,28)); y=0
    for s in satirlar: o.paste(s,(0,y)); y+=s.height+8
    os.makedirs(ONZ,exist_ok=True); o.save(os.path.join(ONZ,"zemin_onizleme.png")); print(o.size)
if __name__=="__main__": main()
