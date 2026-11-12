#!/usr/bin/env python3
"""Adet penceresi ve satin alma onayinin benzetimi (tablet olceginde). Tek kare oldugu icin orijinal pencerenin
yeri once duz siyaha boyanir, sonra ayni sprite + koordinat + punto ile yeniden cizilir."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
B=os.path.dirname(os.path.abspath(__file__)); REF=os.path.join(B,"..","..","referans_gorseller","merchant"); OUT=os.path.join(B,"..","..","kaynak","merchant","sprites")
ONZ=os.path.join(B,"..","..","onizlemeler"); KF=os.path.join(B,"..","..","kaynak","char_info","fonts")
F={"RB":KF+"/Roboto-Bold.ttf","RR":KF+"/Roboto-Regular.ttf"}; _f={}
def fnt(k,p):
    if (k,p) not in _f: _f[(k,p)]=ImageFont.truetype(F[k],p)
    return _f[(k,p)]
def spr(ad): return Image.open(os.path.join(OUT,ad+".png")).convert("RGBA")
class T:
    def __init__(s,im): s.im=im; s.d=ImageDraw.Draw(im,"RGBA")
    def kutu(s,x,y,w,h,renk,a): s.im.alpha_composite(Image.new("RGBA",(int(w),int(h)),tuple(renk)+(int(round(a*255)),)),(int(x),int(y)))
    def spr(s,ad,x,y,w=None,h=None,carp=1.0):
        i=spr(ad) if isinstance(ad,str) else ad
        if w: i=i.resize((int(w),int(h)),Image.LANCZOS)
        if carp!=1.0:
            a=np.asarray(i).astype(float); a[:,:,:3]*=carp; i=Image.fromarray(a.astype(np.uint8),"RGBA")
        s.im.alpha_composite(i,(int(round(x)),int(round(y))))
    def yaz(s,t,x,y,f,p,renk,hiza="sol",dis=0,egik=False):
        fo=fnt(f,p); l,tp,r,b=fo.getbbox(t); w=r-l; rt=fo.getbbox("lH")[1]
        if hiza=="orta": x-=w/2.0
        elif hiza=="sag": x-=w
        if not egik: s.d.text((x-l,y-rt),t,font=fo,fill=renk,stroke_width=dis,stroke_fill=(0,0,0,255)); return w
        k=Image.new("RGBA",(w+80,p*2),(0,0,0,0)); ImageDraw.Draw(k).text((30-l,10),t,font=fo,fill=renk)
        k=k.transform(k.size,Image.AFFINE,(1,0.21,-0.21*p,0,1,0),Image.BICUBIC); s.im.alpha_composite(k,(int(round(x-30)),int(round(y-rt-10)))); return w
    def gen(s,t,f,p): l,tp,r,b=fnt(f,p).getbbox(t); return r-l
PEMBE=(217,195,195,255); SARI=(219,195,0,255)
def adet(t,x0,y0,sayi):
    t.kutu(x0+6,y0+6,728,531,(0,0,0),0.94); t.spr("adet_krom",x0,y0)
    t.yaz(sayi,x0+219,y0+377,"RR",46,(214,214,214,255),"sol",0,True)
def sarmala(t,parcalar,gen,f,p):
    """parcalar: [(kelime, renk)] ; kelime kelime sarar. Donus: satir listesi [[(kelime,renk)]]"""
    bos=t.gen("a a",f,p)-2*t.gen("a",f,p); sat=[[]]; w=0
    for k,r in parcalar:
        kw=t.gen(k,f,p)
        if sat[-1] and w+bos+kw>gen: sat.append([]); w=0
        w+= (bos if sat[-1] else 0)+kw; sat[-1].append((k,r,kw))
    return sat,bos
def onay(t,x0,y0,ikon,yuk,fiyat,oran,kalan,ok_acik):
    t.kutu(x0+5,y0+5,567,520,(0,0,0),0.99); t.spr("onay_krom",x0,y0)
    t.spr(ikon,x0+245,y0+30,84,82); t.spr("onay_ikon_cerceve",x0+238,y0+23)
    if yuk: t.yaz("+%d"%yuk,x0+331,y0+29,"RB",29,(202,137,226,255),"sag")
    t.spr("sure_oluk",x0+58,y0+144)
    w=int(round(455*oran))
    if w>0: t.spr(spr("sure_dolgu").resize((w,17),Image.BILINEAR),x0+60,y0+147)
    t.yaz(str(kalan),x0+60+w+4,y0+149,"RB",19,(255,255,255,255),"orta",1)
    par=[("[Price:",PEMBE),(fiyat,SARI),("]",PEMBE)]+[(k,PEMBE) for k in "Will you buy this item?".split()]
    sat,bos=sarmala(t,par,470,"RB",27); sat.append([(k,PEMBE,t.gen(k,"RB",27)) for k in "Please double check the price".split()])
    for i,s in enumerate(sat):
        top=sum(k[2] for k in s)+bos*(len(s)-1); x=x0+295.5-top/2.0
        for k,r,kw in s: t.yaz(k,x,y0+288+31*i,"RB",27,r); x+=kw+bos
    t.spr("btn_onay_zemin",x0+115,y0+437,carp=1.0 if ok_acik else 0.56); t.spr("yazi_ok",x0+162,y0+456)
    t.spr("btn_onay_zemin",x0+332,y0+437); t.spr("yazi_cancel",x0+346,y0+456)
def panel(kare,kutu,ciz,kirp):
    o=Image.open(os.path.join(REF,kare+".png")).convert("RGBA"); t=T(o.copy()); t.kutu(*kutu,(0,0,0),1.0); ciz(t)
    return o.crop(kirp),t.im.crop(kirp)
def yan(ad,o,y,bas):
    c=Image.new("RGB",(o.width*2+30,o.height+64),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((10,8),bas,font=fnt("RB",22),fill=(255,220,120)); d.text((10,38),"ORİJİNAL",font=fnt("RB",16),fill=(200,200,200)); d.text((o.width+20,38),"YENİ",font=fnt("RB",16),fill=(140,230,140))
    c.paste(o.convert("RGB"),(10,60)); c.paste(y.convert("RGB"),(o.width+20,60)); c.save(os.path.join(ONZ,ad+".png")); print(ad,c.size); return c
if __name__=="__main__":
    o,y=panel("t_adet",(1170,325,740,543),lambda t: adet(t,1170,325,"20"),(1130,290,1950,900)); a=yan("merchant_13_adet",o,y,"Toplu eşya koyma: adet girişi")
    o,y=panel("t_satinal",(864,416,577,530),lambda t: onay(t,864,416,"ikon_short_bow",5,"99,999,999",224/455.0,2,False),(830,385,1475,975)); b=yan("merchant_14_satinal",o,y,"Satın alma onayı (süre çubuklu)")
    c=Image.new("RGB",(max(a.width,b.width),a.height+b.height+10),(24,24,28)); c.paste(a,(0,0)); c.paste(b,(0,a.height+10)); c.save(os.path.join(ONZ,"merchant_adet_satinal_onizleme.png")); print(c.size)
