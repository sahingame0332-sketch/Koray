#!/usr/bin/env python3
"""Merchant yazilari: font + punto (murek genisligi ve IoU)."""
import sys
from PIL import ImageDraw, ImageFont
from ortak import *
KF=os.path.join(B,"..","..","kaynak","char_info","fonts")
ADAY={"RB":KF+"/Roboto-Bold.ttf","RR":KF+"/Roboto-Regular.ttf","SB":KF+"/RobotoSlab-Bold.ttf","SR":"/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf"}
def murek(m):
    ys,xs=np.nonzero(m)
    return None if len(xs)<6 else m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(t,f,p):
    fo=ImageFont.truetype(ADAY[f],p); im=Image.new("L",(1600,240),0); ImageDraw.Draw(im).text((40,40),t,font=fo,fill=255); return murek(np.asarray(im)>128)
def iou(a,b):
    h,w=max(a.shape[0],b.shape[0]),max(a.shape[1],b.shape[1]); A=np.zeros((h,w),bool); Bm=np.zeros((h,w),bool)
    A[:a.shape[0],:a.shape[1]]=a; Bm[:b.shape[0],:b.shape[1]]=b; return (A&Bm).sum()/max(1,(A|Bm).sum())
def olc(ad,metin,kare,kutu,renk,tol=70):
    x0,y0,x1,y1=kutu; a=Y(kare)[y0:y1,x0:x1]; h=murek(np.abs(a-np.array(renk,float)).max(2)<tol)
    if h is None: print("%-18s olculemedi"%ad); return
    r=[]
    for f in ADAY:
        en=(0,0)
        for p in range(10,60):
            m=ciz(metin,f,p)
            if m is None: continue
            v=iou(h,m)
            if v>en[0]: en=(v,p,m.shape[1])
        r.append((en[0],en[1],f,en[2]))
    r.sort(reverse=True)
    print("%-18s %-22s murek %3dx%-3d @(%d,%d) | "%(ad,"'"+metin+"'",h.shape[1],h.shape[0],x0+np.nonzero(np.abs(a-np.array(renk,float)).max(2)<tol)[1].min(),y0+np.nonzero(np.abs(a-np.array(renk,float)).max(2)<tol)[0].min())+"  ".join("%s %d (%.2f, w%d)"%(f,p,v,w) for v,p,f,w in r[:3]))
def renk(ad,kare,kutu,mod="parlak"):
    x0,y0,x1,y1=kutu; s=Y(kare)[y0:y1,x0:x1].reshape(-1,3); key=s.max(1) if mod=="parlak" else s.max(1)-s.min(1)
    c=np.median(s[key>=np.percentile(key,96)],0).astype(int); print("%-18s #%02X%02X%02X"%(ad,*c))
if __name__=="__main__":
    W=(250,240,235)
    renk("merchant basligi","m_pencere2",(1110,122,1570,162),"doygun"); olc("merchant basligi","xMegaTon Merchant","m_pencere2",(1100,118,1580,172),(225,180,120),75)
    renk("altin","m_pencere2",(1480,530,1640,570)); olc("altin","523,455","m_pencere2",(1470,525,1650,575),W,60)
    olc("slave sayac","1/0","s_pencere2",(1600,320,1700,370),W,60); olc("slave durum","Not sold yet.","s_pencere2",(1780,320,2100,370),W,60)
    renk("slave durum","s_pencere2",(1780,320,2100,370))
    renk("+5 etiketi","m_create_dolu",(1690,165,1730,195),"doygun"); olc("+5 etiketi","+5","m_create_dolu",(1680,160,1735,200),(200,140,230),80)
    olc("+8 etiketi","+8","m_create",(1855,620,1915,660),(200,140,230),80)
    olc("adet","4","m_create",(1680,480,1712,512),W,60); olc("adet 3","3","m_create",(1780,480,1812,512),W,60)
    renk("purchase price","m_ipucu_b",(1280,330,1640,372),"doygun"); olc("purchase price","Purchase Price : 99,999","m_ipucu_b",(1276,326,1650,376),(190,60,190),90)
    renk("buy price","f_npc",(1432,337,1680,377),"doygun"); olc("buy price","Buy Price : 3,188","f_npc",(1428,333,1700,381),(249,210,20),80)
    renk("fiyat girisi","m_fiyat",(1730,560,1900,610)); 
    olc("ad (Silan)","Silan Boots","f_equip",(1835,512,2120,560),W,60); olc("stat","Required Magic Power : 53","f_equip",(1735,806,2120,850),W,60)
    olc("unequip?","Defense Ability : 15","f_unequip",(1824,690,2120,735),W,60)
    renk("rogue item","m_ipucu_b",(1380,630,1580,668),"doygun"); renk("bow turu","m_ipucu_b",(1420,694,1520,730)); renk("poison","m_ipucu_b",(1280,507,1580,540),"doygun")
