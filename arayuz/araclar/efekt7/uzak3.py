#!/usr/bin/env python3
"""Efekt 7 eki — yapraklar katmani + uzak onizleme. uzak_<kayit>.json eslemesini kullanir.
Yapraklar: O - (zemin + kirmizi + olcekli efekt7) artigi; sari (R,G >> B) ve efekt 7'nin olcekli kapsami disinda kalan kucuk parcalar.
Kare, hedefin zeminine gore hedef boyu biriminde saklanir (uzak olcekte, 2x buyutulmus).
Cikti: kaynak/efekt7/yapraklar/ (devir 1), onizlemeler/efekt7_uzak.mp4 / .png
Kullanim: uzak3.py KLASOR a"""
import os, sys, json, glob, subprocess, tempfile, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from ortak import kirmizi
import uzak; uzak.ARKA_KAT="arka_temiz"
from uzak import yakin_isik, olcekle, BIL, HM, K7, YAKIN_ZEMIN, YAKIN_BOY
from uzak2 import KAYIT
ONZ=os.path.join(K7,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(K7,"..","char_info","fonts","Roboto-Bold.ttf"),22)
AURA=dict(olcek=0.30,yakin=(731,567),a=(1038,620))   # aura agirlik merkezi (yakin / uzak kayit)
YAY_X=950                          # yakin kayitta kilic yayi bu x'in sagi (oyuncu tarafi)
YAY_YAKIN=(1130,990)               # yakin kayitta yayin sag-alt ucu
# uzak kayitta: yayin sag-alt ucu (oyuncunun onu, ayak hizasi) ve olcek (uzak yay boyu / yakin yay boyu: 105 / 750)
KAYIT_OYUNCU={"a":dict(ayak=(1365,705),boy=100,yay=(1300,695),olcek=0.14)}
def duzelt(dev):
    """bastaki 'yok' ama isikli kareler: kesik 0..ilk eslesene dogrusal (efektin acilisi)"""
    ilk=next(j for j,d in enumerate(dev) if d["efekt"]!="yok")
    bas=[j for j in range(ilk) if dev[j]["kirmizi"]>0.2]
    if bas:
        n1=dev[ilk]["kare"]
        for q,j in enumerate(bas): dev[j]["efekt"]="kesik_aura_tum"; dev[j]["kare"]=int(round(n1*(q+0.5)/(len(bas)+0.5)))
    return dev
def calis(klasor,ad):
    cfg=KAYIT[ad]; J=json.load(open(os.path.join(K7,"uzak_%s.json"%ad))); fs=sorted(glob.glob(os.path.join(klasor,ad,"k_*.png")))
    Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
    Bo=np.median([Y(i) for i in cfg["once"]],0); Bs=np.median([Y(i) for i in cfg["sonra"]],0)
    Z=cfg["zemin"]; k=AURA["olcek"]        
    rm=np.load(os.path.join(K7,"uzak_hedef_%s.npy"%ad))
    r2=np.zeros(rm.shape,bool)
    for dev in J["devirler"]:
        for d in dev:
            if d["efekt"]=="yildiz_tum" and d["kirmizi"]>0.3:
                O=Y(d["kayit_kare"]); r2|=(O[...,0]-Bo[...,0]>40)&(O[...,0]>O[...,1]+60)
    r2=ndimage.binary_opening(r2,np.ones((2,2))); l,n=ndimage.label(r2); sz=ndimage.sum(r2,l,range(1,n+1)); r2=l==(1+np.argmax(sz))
    rm=ndimage.binary_fill_holes(ndimage.binary_closing(r2,np.ones((5,5)))); np.save(os.path.join(K7,"uzak_hedef_%s.npy"%ad),rm); Kr=kirmizi(Bo.mean(2))
    W2=int(1.6*cfg["boy"]); X0,Y0=Z[0]-W2,Z[1]-int(1.9*cfg["boy"]); X1,Y1=Z[0]+W2,Z[1]+int(0.5*cfg["boy"])   # yaprak kutusu (uzak)
    od=os.path.join(K7,"yapraklar"); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    cache={}
    # on plan (cit, direk): cim olmayan zemin pikselleri, hedefin onunde -> aurayi orter (Unity'de derinlik testi)
    cim=(Bo[...,1]>=Bo[...,0]-6)&(Bo[...,1]>Bo[...,2]+10)
    onp=~cim; onp[:,:Z[0]-int(1.2*cfg["boy"])]=False; onp[:,Z[0]+int(1.2*cfg["boy"]):]=False; onp[:Z[1]-int(1.6*cfg["boy"])]=False; onp[Z[1]+10:]=False
    onp&=~ndimage.binary_dilation(rm,np.ones((3,3))); onp=ndimage.binary_opening(onp,np.ones((3,3)))
    l,n=ndimage.label(onp)
    if n: sz=ndimage.sum(onp,l,range(1,n+1)); onp=np.isin(l,1+np.where(sz>=150)[0])     # yalniz buyuk on plan (tas direk); ince cit uzaktan secilmiyor
    def model(e,n):
        """hedef parcasi (yakin x<YAY_X) hedefe bagli; kilic yayi (x>=YAY_X) oyuncuya bagli (yay oyuncunun onunde cikiyor)"""
        if (e,n) not in cache:
            E=yakin_isik(e,n); sari=(np.minimum(E[...,0],E[...,1])-E[...,2])>(E[...,2]-E[...,1])   # yay sari; aura pembe kalir
            yay=sari.copy(); yay[:,:YAY_X]=False; yay=ndimage.binary_dilation(yay,np.ones((5,5)))&sari
            Eh=np.where(yay[...,None],0,E); Ek=np.where(yay[...,None],E,0)
            cache[(e,n)]=olcekle(Eh,k,AURA["yakin"],AURA[ad])+olcekle(Ek,KAYIT_OYUNCU[ad]["olcek"],YAY_YAKIN,KAYIT_OYUNCU[ad]["yay"])
        return cache[(e,n)]
    kareler=[]; yap_say=0; zam=[]
    for dv,dev in enumerate(J["devirler"]):
        dev=duzelt(dev)
        for d in dev:
            i=d["kayit_kare"]; O=Y(i)
            v=((O[...,0]-Bo[...,0])/np.maximum(Kr[...,0]-Bo[...,0],20))[rm&(Kr[...,0]-Bo[...,0]>40)]
            s=round(float(np.clip(np.quantile(v,0.5),0,1)),3) if len(v) else 0.0; d["kirmizi"]=s      # hedef siluetinde (2. efektin kirmizisindan)
            R=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo)
            if d["efekt"]!="yok":
                M=model(d["efekt"],d["kare"]); M=np.where(onp[...,None],0,M); R=R+M; kap=ndimage.binary_dilation(M.max(2)>6,np.ones((9,9)))
            else: kap=np.zeros(rm.shape,bool)
            D=np.minimum(O-R,O-Bs-(R-Bo)); D=np.clip(D,0,255)
            yap=(np.minimum(D[...,0],D[...,1])-D[...,2]>18)&(D[...,1]>25)&~kap&~ndimage.binary_dilation(rm,np.ones((5,5)))
            yap=ndimage.binary_opening(yap,np.ones((2,2))); l,n=ndimage.label(yap)
            if n: sz=ndimage.sum(yap,l,range(1,n+1)); yap=np.isin(l,1+np.where((sz>=4)&(sz<=400))[0])
            yap[:Y0]=False; yap[Y1:]=False; yap[:,:X0]=False; yap[:,X1:]=False
            Yk=np.where(ndimage.binary_dilation(yap,np.ones((3,3)))[...,None],D,0)
            if dv==0:
                Image.fromarray(np.clip(Yk[Y0:Y1,X0:X1],0,255).astype(np.uint8)).save(os.path.join(od,"yapraklar_%02d.png"%yap_say)); yap_say+=1
                zam.append(dict(kare=yap_say-1,efekt=d["efekt"],efekt_kare=d["kare"],kirmizi=s))
            kareler.append((i,O,np.clip(R+Yk,0,255),d))
    json.dump(dict(kayit=ad,olcek_uzak=k,hedef_boy_uzak_px=cfg["boy"],kutu_hedefe_gore=[(X0-Z[0])/cfg["boy"],(Y0-Z[1])/cfg["boy"],(X1-X0)/cfg["boy"],(Y1-Y0)/cfg["boy"]],
                   fps=30.0,zamanlama=zam),open(os.path.join(K7,"gercek_zamanlama.json"),"w"),indent=1)
    # onizleme
    KIRP=(Z[0]-int(3.2*cfg["boy"]),Z[1]-int(2.6*cfg["boy"]),Z[0]+int(3.2*cfg["boy"]),Z[1]+int(0.9*cfg["boy"])); Wv=700
    d_=tempfile.mkdtemp(); t=0; ornek=[]
    for i,O,R,d in kareler:
        a=Image.fromarray(O.astype(np.uint8)).crop(KIRP); r=Image.fromarray(R.astype(np.uint8)).crop(KIRP)
        h=int(Wv*a.height/a.width); a=a.resize((Wv,h),Image.LANCZOS); r=r.resize((Wv,h),Image.LANCZOS)
        c=Image.new("RGB",(2*Wv+10,h+36),(24,24,28)); c.paste(a,(0,36)); c.paste(r,(Wv+10,36)); dr=ImageDraw.Draw(c)
        dr.text((6,6),"UZAK — ORİJİNAL (gerçek hız)",font=F,fill=(200,200,200)); dr.text((Wv+16,6),"YENİ (zemin + efekt 7 + yapraklar)",font=F,fill=(140,230,140))
        c.save(os.path.join(d_,"a_%04d.png"%t)); t+=1
        if i in (28,31,34,40,45): ornek.append(c)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d_+"/a_%04d.png","-vf","format=yuv420p","-c:v","libx264","-crf","19",os.path.join(ONZ,"efekt7_uzak_%s.mp4"%ad)],check=True)
    shutil.rmtree(d_)
    o=Image.new("RGB",(ornek[0].width,sum(x.height+6 for x in ornek)),(24,24,28)); yy=0
    for x in ornek: o.paste(x,(0,yy)); yy+=x.height+6
    o.save(os.path.join(ONZ,"efekt7_uzak_%s.png"%ad)); print(t,"kare, yaprak karesi",yap_say)
if __name__=="__main__": calis(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else "a")
