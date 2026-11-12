#!/usr/bin/env python3
"""OlymposMerchantBuilder.cs'in Python benzetimi: ayni sprite + koordinat + punto ile her pencereyi
yeniden kurar, orijinal kareyle yan yana koyar.  Cikti: onizlemeler/merchant_*.png"""
from PIL import ImageDraw, ImageFont
from ortak import *
ONZ=os.path.join(B,"..","..","onizlemeler"); KF=os.path.join(B,"..","..","kaynak","char_info","fonts")
FONT={"RB":KF+"/Roboto-Bold.ttf","RR":KF+"/Roboto-Regular.ttf","SB":KF+"/RobotoSlab-Bold.ttf","SR":"/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf"}
_f={}
def fnt(k,p):
    if (k,p) not in _f: _f[(k,p)]=ImageFont.truetype(FONT[k],p)
    return _f[(k,p)]
import json
BILGI=json.load(open(os.path.join(OUT,"..","sprite_bilgisi.json")))
def E(ad): return BILGI[ad]["ekran"][:2]
def kare(ad): return Image.open(os.path.join(REF,ad+".jpg")).convert("RGBA")
def spr(ad): return Image.open(os.path.join(OUT,ad+".png")).convert("RGBA")
PEMBE=(255,231,233,255); BEYAZ=(255,255,255,255); MOR=(202,137,231,255); KIRMIZI=(254,0,1,255)
YESIL=(152,191,42,255); ZEHIR=(129,194,103,255); DERECE=(136,194,115,255); SARI=(251,210,12,255); FIYATMOR=(180,42,153,255); ALTIN=(221,169,106,255)
class Tuval:
    def __init__(s,im): s.im=im; s.d=ImageDraw.Draw(im,"RGBA")
    def kutu(s,x,y,w,h,renk,alfa): s.im.alpha_composite(Image.new("RGBA",(int(w),int(h)),tuple(renk)+(int(round(alfa*255)),)),(int(round(x)),int(round(y))))
    def spr(s,ad,x,y,w=None,h=None):
        i=spr(ad) if isinstance(ad,str) else ad
        if w: i=i.resize((int(w),int(h)),Image.LANCZOS)
        s.im.alpha_composite(i,(int(round(x)),int(round(y))))
    def yaz(s,t,x,y,f,p,renk,hiza="sol",dis=0,egik=False):
        """y: 'lH' dizisinin murek tepesi (cikinti tepesi). x: sol / orta / sag murek kenari."""
        fo=fnt(f,p); l,tp,r,b=fo.getbbox(t); w=r-l; rt=fo.getbbox("lH")[1]
        if hiza=="orta": x-=w/2.0
        elif hiza=="sag": x-=w
        if not egik:
            s.d.text((x-l,y-rt),t,font=fo,fill=renk,stroke_width=dis,stroke_fill=(0,0,0,255)); return w
        k=Image.new("RGBA",(w+60,p*2),(0,0,0,0)); ImageDraw.Draw(k).text((20-l,10),t,font=fo,fill=renk)
        k=k.transform(k.size,Image.AFFINE,(1,0.21,-0.21*p,0,1,0),Image.BICUBIC)
        s.im.alpha_composite(k,(int(round(x-20)),int(round(y-rt-10)))); return w
    def gen(s,t,f,p): l,tp,r,b=fnt(f,p).getbbox(t); return r-l

# ----------------------------------------------------------------- esya bilgi penceresi
def bilgi(t,x0,y0,v,ciz=True):
    """v: ikon, ad, adRenk, tur, fiyat=(etiket,deger,renk)|None, statlar=[(metin,renk)], sinif=(metin,renk)|None,
       cins|None, derece|None, aciklama=[satirlar], dugmeler=[sprite adlari]. Donus: (genislik, yukseklik)"""
    sag=115+max(t.gen(v["ad"],"RB",36),t.gen(v["tur"],"RB",27))
    if v.get("fiyat"): sag=max(sag,12+t.gen(v["fiyat"][0]+v["fiyat"][1],"RB",32))
    for m,_ in v["statlar"]: sag=max(sag,12+t.gen(m,"RB",29))
    W=max(346,sag+33)
    s1=194 if v.get("fiyat") else 147
    n=len(v["statlar"]); s2=s1+36+38.7*(n-1)+48 if n else s1+30
    orta=[]
    if v.get("sinif"): orta.append(v["sinif"])
    if v.get("cins"): orta+= [("",PEMBE),(v["cins"],PEMBE)]
    if v.get("derece"): orta.append((v["derece"],DERECE))
    orta+=[(a,PEMBE) for a in v["aciklama"]]
    s3=s2+35+31.5*(len(orta)-1)+59; by=s3+13; H=int(round(by+65))
    if not ciz: return W,H
    t.kutu(x0,y0,W,H,(0,0,0),0.93)
    t.spr(v["ikon"],x0+12,y0+12,89,89); t.spr("ikon_cerceve",x0+5,y0+5)
    t.yaz(v["ad"],x0+115,y0+13,"RB",36,v["adRenk"]); t.yaz(v["tur"],x0+115,y0+50,"RB",27,v["adRenk"])
    if v.get("fiyat"): t.yaz(v["fiyat"][0]+v["fiyat"][1],x0+12,y0+139,"RB",32,v["fiyat"][2])
    for sy in (s1,s2,s3): t.kutu(x0+12,y0+sy,W-26,1,(74,68,60),1.0)
    for i,(m,r) in enumerate(v["statlar"]): t.yaz(m,x0+12,y0+s1+36+38.7*i,"RB",29,r)
    for i,(m,r) in enumerate(orta):
        if m: t.yaz(m,x0+W/2.0,y0+s2+35+31.5*i,"RB",27,r,"orta")
    for i,b in enumerate(v["dugmeler"]): t.spr(b,x0+12+161*i,y0+by)
    return W,H
BOW=dict(ikon="ikon_short_bow",ad="Short Bow(+5)",adRenk=MOR,tur="Upgrade Item",
         statlar=[("Attack Power : 31",PEMBE),("Poison Damage : 50",ZEHIR),("Required Dexterity : 80",KIRMIZI)],
         sinif=("(Rogue Item)",KIRMIZI),cins="(Bow)",derece="Item Grade : Low Class",aciklama=["A small bow that can","shoot far due to its","elasticity."])
BOOTS=dict(ikon="ikon_silan_boots",ad="Silan Boots",adRenk=PEMBE,tur="-",
           statlar=[("Defense Ability : 15",PEMBE),("Bonus HP : 15",YESIL),("Bonus MP : 15",YESIL),("Required Magic Power : 53",PEMBE)],
           sinif=("(Magician Item)",PEMBE),derece="Item Grade : Middle Class",aciklama=["A pair of shoes that would","look good on a mage."])
KNIFE=dict(ikon="ikon_knife",ad="Knife(+1)",adRenk=MOR,tur="Upgrade Item",fiyat=("Buy Price : ","3,188",SARI),
           statlar=[("Attack Power : 11",PEMBE),("Required Dexterity : 80",KIRMIZI)],cins="(Dagger)",derece="Item Grade : Low Class",
           aciklama=["This knife is more","powerful than","a dagger, and is suited","for stabbing."])
def D(v,**k): d=dict(v); d.update(k); return d

# ----------------------------------------------------------------- yuvalar
ENVANTER=[("ikon_hp_scroll",4,0),("ikon_zirh_scroll",3,0),("ikon_hiz_iksiri",2,0),None,("ikon_short_bow",0,5),("ikon_eldiven",0,0),("ikon_yuzuk",0,0),
          ("ikon_asa",0,0),None,("ikon_zirh",0,0),("ikon_bilezik",0,0),("ikon_kupe",0,0),("ikon_kupe",0,0),("ikon_pantolon",0,0),
          None,("ikon_sopa",0,0),("ikon_sopa",0,8)]
def yuva(t,x,y,w,h,e,dolu=None,pay=8):
    """(x,y,w,h): yuva halka kutusu. e=(ikon, adet, yukseltme)"""
    if e is None: return
    iw,ih=w-2*pay,h-2*pay
    t.spr(e[0],x+pay,y+pay,iw,ih)
    if dolu: t.spr(dolu,x,y)
    p=int(round(h*0.33))
    if e[2]: t.yaz("+%d"%e[2],x+w-pay-2,y+pay+3,"RB",p,(202,137,226,255),"sag")
    if e[1]: t.yaz(str(e[1]),x+w-pay-3,y+h-pay-int(p*0.80),"RB",int(round(h*0.27)),PEMBE,"sag",1)
def izgara(t,g,w,h,nc,liste,dolu,atla=()):
    for i,e in enumerate(liste):
        if i in atla: continue
        yuva(t,int(round(g[0]+g[1]*(i%nc))),int(round(g[2]+g[3]*(i//nc))),w,h,e,dolu)

CU=(1637.0,111.0,163.0,110.0); CE=(1613.8,99.67,414.0,100.9); PU=(974.7,120.31,228.8,121.17); PE=(967.8,103.64,588.9,104.4)
def create(t,ust=(),env_atla=()):
    t.kutu(1588,112,740,785,(0,0,0),0.95); t.kutu(1578,62,754,50,(0,0,0),0.95)
    t.spr("create_krom",*E("create_krom")); izgara(t,CE,103,101,7,ENVANTER,"yuva_dolu_create_env",env_atla); izgara(t,CU,102,100,6,list(ust),"yuva_dolu_create_ust")
def panel_menu():
    t=Tuval(kare("m_once")); t.kutu(2330,166,300,940,(0,0,0),0.94); t.spr("menu_krom",*E("menu_krom"))
    k=(2250,90,2700,1150); return kare("m_menu").crop(k),t.im.crop(k)
def panel_create():
    t=Tuval(kare("m_once")); create(t,ust=[("ikon_short_bow",0,5)],env_atla=(4,))
    k=(1540,30,2400,950); return kare("m_create_dolu").crop(k),t.im.crop(k)
def panel_fiyat():
    t=Tuval(kare("m_create")); t.kutu(1611,214,699,510,(0,0,0),0.97); t.spr("fiyat_krom",1605,208)
    t.yaz("99,999",1819,566,"RR",46,(235,223,205,255),"sol",0,True)
    k=(1560,170,2360,770); return kare("m_fiyat").crop(k),t.im.crop(k)
def panel_ipucu_remove():
    t=Tuval(kare("m_create_dolu")); bilgi(t,1270,196,D(BOW,fiyat=("Purchase Price : ","99,999",FIYATMOR),dugmeler=["btn_remove","btn_close"]))
    k=(1240,170,1700,940); return kare("m_ipucu_b").crop(k),t.im.crop(k)
def tezgah(t,liste):
    for i in range(4): t.kutu(1194+86*i,568,70,72,(0,0,0),0.87)
    t.spr("tezgah_krom",*E("tezgah_krom"))
    for i,e in enumerate(liste): yuva(t,1186+86*i,560,86,88,e,"yuva_dolu_tezgah")
def panel_tezgah():
    t=Tuval(kare("m_once")); tezgah(t,[("ikon_short_bow",0,5)])
    k=(1100,480,1620,760); return kare("m_tezgah").crop(k),t.im.crop(k)
def mpencere(t,ad,ust,altin):
    t.kutu(952,172,770,905,(0,0,0),0.89); t.kutu(958,122,762,48,(0,0,0),0.89)
    t.spr("mpencere_krom",*E("mpencere_krom"))
    t.yaz(ad+" Merchant",1335.5,131,"SR",33,ALTIN,"orta"); t.yaz(altin,1618,538,"RB",36,BEYAZ,"sag")
    izgara(t,PE,104,102,7,ENVANTER,"yuva_dolu_mp_env",(4,)); izgara(t,PU,117,114,6,list(ust),"yuva_dolu_mp_ust")
def panel_mpencere():
    t=Tuval(kare("m_tezgah")); mpencere(t,"xMegaTon",[("ikon_short_bow",0,5)],"523,455")
    k=(900,80,1790,1130); return kare("m_pencere2").crop(k),t.im.crop(k)
def panel_ipucu_pencere():
    t=Tuval(kare("m_pencere2")); bilgi(t,614,269,D(BOW,fiyat=("Purchase Price : ","99,999",FIYATMOR),dugmeler=["btn_close"]))
    k=(580,240,1040,1020); return kare("m_pencere_ipucu").crop(k),t.im.crop(k)
def panel_ipucu_tezgah():
    t=Tuval(kare("m_tezgah_hedef")); bilgi(t,820,452,D(BOW,dugmeler=["btn_close"]))
    k=(790,430,1240,1150); return kare("m_tezgah_ipucu").crop(k),t.im.crop(k)
def slave(t,satirlar):
    t.kutu(1452,98,952,1010,(0,0,0),0.95); t.spr("slave_krom",*E("slave_krom"))
    for i,(ik,sayac,durum) in enumerate(satirlar):
        y=294+92*i; t.spr("slave_satir",1460,y)
        t.spr(ik,1517,y+15,70,68); t.spr("slave_ikon_cerceve",1512,y+10); t.yaz("+5",1586,y+16,"RB",22,(202,137,226,255),"sag")
        t.yaz(sayac,1629,y+45,"SB",26,BEYAZ); t.yaz(durum,1925.5,y+44,"SB",28,BEYAZ,"orta")
def panel_slave():
    t=Tuval(kare("s_sonra")); slave(t,[("ikon_short_bow","1/0","Not sold yet.")])
    k=(1420,70,2470,1130); return kare("s_pencere2").crop(k),t.im.crop(k)
def panel_equip(kaynak,x0,dugme):
    o=kare(kaynak); t=Tuval(o.copy()); w,h=bilgi(t,x0,507,D(BOOTS,dugmeler=[dugme,"btn_close"]),ciz=False)
    t.kutu(x0,507,w,h,(0,0,0),1.0)          # tek kare var: alttaki orijinal kutu duz siyaha boyanir
    bilgi(t,x0,507,D(BOOTS,dugmeler=[dugme,"btn_close"]))
    k=(x0-40,480,x0+440,1140); return o.crop(k),t.im.crop(k)
def panel_npc():
    o=kare("f_npc"); t=Tuval(o.copy()); w,h=bilgi(t,1426,197,D(KNIFE,dugmeler=["btn_close"]),ciz=False)
    t.kutu(1426,197,w,h,(0,0,0),1.0); bilgi(t,1426,197,D(KNIFE,dugmeler=["btn_close"]))
    k=(1390,170,1810,900); return o.crop(k),t.im.crop(k)

def yan_yana(ad,o,y,olcek,baslik):
    if olcek!=1.0:
        o=o.resize((int(o.width*olcek),int(o.height*olcek)),Image.LANCZOS); y=y.resize(o.size,Image.LANCZOS)
    c=Image.new("RGB",(o.width*2+30,o.height+64),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((10,8),baslik,font=fnt("RB",22),fill=(255,220,120)); d.text((10,38),"ORİJİNAL",font=fnt("RB",16),fill=(200,200,200)); d.text((o.width+20,38),"YENİ",font=fnt("RB",16),fill=(140,230,140))
    c.paste(o.convert("RGB"),(10,60)); c.paste(y.convert("RGB"),(o.width+20,60)); c.save(os.path.join(ONZ,ad+".png")); return c
PANELLER=[("merchant_1_menu",panel_menu,0.55,"Komut menüsü (Open Merchant · Slave Merchant)"),
          ("merchant_2_create",panel_create,0.7,"Create a Merchant"),
          ("merchant_3_fiyat",panel_fiyat,0.8,"Fiyat girişi"),
          ("merchant_4_ipucu_remove",panel_ipucu_remove,0.8,"Tezgâhtaki eşya: Purchase Price · Remove / Close"),
          ("merchant_5_tezgah",panel_tezgah,1.0,"Tezgâh çubuğu (OPEN · WHISPER)"),
          ("merchant_6_pencere",panel_mpencere,0.62,"<ad> Merchant penceresi"),
          ("merchant_7_ipucu_pencere",panel_ipucu_pencere,0.8,"Merchant penceresinde eşya bilgisi"),
          ("merchant_8_ipucu_tezgah",panel_ipucu_tezgah,0.8,"Tezgâh yuvasında eşya bilgisi (fiyatsız)"),
          ("merchant_9_slave",panel_slave,0.6,"Slave Merchant"),
          ("merchant_10_equip",lambda: panel_equip("f_equip",1727,"btn_equip"),0.9,"Envanter: Equip / Close"),
          ("merchant_11_unequip",lambda: panel_equip("f_unequip",1816,"btn_unequip"),0.9,"Kuşanılmış eşya: UnEquip / Close"),
          ("merchant_12_npc",panel_npc,0.85,"NPC dükkânı eşya bilgisi (Buy Price)")]
if __name__=="__main__":
    import sys
    for ad,fn,olc,bas in PANELLER:
        if len(sys.argv)>1 and sys.argv[1] not in ad: continue
        o,y=fn(); c=yan_yana(ad,o,y,olc,bas); print(ad,c.size)
