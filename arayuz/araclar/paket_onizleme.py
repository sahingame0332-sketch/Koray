# Paket iceriginden pencere onizlemesi uretir (Unity kurucusunun yerlesimi taklit edilir).
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

S = pathlib.Path("/tmp/claude-0/-home-user-Koray/7667fcb8-b488-59d0-b1d8-f55ffb36b68a/scratchpad")
CH = S/"pkg_tree/char/Assets/OlymposCharacter1298"
MO = S/"pkg_tree/menu/Assets/OlymposMenuOptions1298"
CR = CH/"Resources/OlymposCharacter1298"
MR = MO/"Resources/OlymposMenuOptions1298"
FONT = str(CH/"Fonts/RobotoSlab-Bold.ttf")
F = lambda n: ImageFont.truetype(FONT, n)
spr = lambda d,n: Image.open(d/(n+".png")).convert("RGBA")

# oyun dunyasi zemini (onizleme icin)
DUNYA = Image.open("/home/user/Koray/arayuz/referans_gorseller/moradon_onizleme_arkaplani.jpg").convert("RGB")
def zemin(w,h,alfa):
    d = DUNYA.resize((int(DUNYA.width*h/DUNYA.height), h), Image.LANCZOS)
    d = d.crop((0,0,w,h)) if d.width>=w else d.resize((w,h), Image.LANCZOS)
    return Image.alpha_composite(d.convert("RGBA"), Image.new("RGBA",(w,h),(0,0,0,int(round(alfa*255)))))

# ---- Character penceresi (654x1030) ----
W,H = 654,1030
SX,SY,AX0,AY0 = 654/760, 1030/1205, 303, 143
LX=lambda a:(a-AX0)*SX; LY=lambda a:(a-AY0)*SY; LW=lambda w:w*SX; LH=lambda h:h*SY
TAB_CIZGI = {0:(9,210), 1:(224,128), 2:(362,162), 3:(526,120)}

def yaz(d,t,f,x,y,w,h,c,hiza="orta"):
    bb=d.textbbox((0,0),t,font=f)
    ty = y+(h-(bb[3]-bb[1]))/2-bb[1]
    tx = x+(w-(bb[2]-bb[0]))/2-bb[0] if hiza=="orta" else x-bb[0]
    d.text((tx,ty),t,font=f,fill=c)
def yazA(d,t,f,ax,ay,aw,ah,c,hiza="orta"):
    yaz(d,t,f,LX(ax),LY(ay),LW(aw),LH(ah),c,hiza)

def character(sekme):
    im = zemin(W,H,0.92)
    im.alpha_composite(spr(CR,"window_frame"),(0,0))
    im.alpha_composite(spr(CR,"tabs_strip_plain").resize((637,92),Image.LANCZOS),(9,8))
    ux,uw = TAB_CIZGI[sekme]
    im.alpha_composite(spr(CR,"tab_underline").resize((uw,7),Image.LANCZOS),(ux,93))
    d=ImageDraw.Draw(im); f21=F(21)
    for t,(x,w) in zip(("CHAR INFO","QUESTS","CLAN","FRIENDS"),
                       ((15,200),(224,128),(365,156),(525,120))):
        yaz(d,t,f21,x,10,w,82,(244,244,244))

    if sekme == 0:
        im.alpha_composite(Image.open("/home/user/Koray/arayuz/onizlemeler/OLYMPOS_CharInfo_Unity_Onizleme.png")
                           .convert("RGBA").crop((0,100,W,H)),(0,100))
    elif sekme == 3:
        im.alpha_composite(spr(CR,"friends_icerik").resize((W,H),Image.LANCZOS),(0,0))
        d=ImageDraw.Draw(im)
        for i,(ad,c) in enumerate([("xDarKPasT",(240,40,40)),("PUSSCUTEZCAN",(240,40,40)),
                                   ("PUSSCU_TEZCAN",(46,230,46))]):
            yazA(d,ad,F(25),345,361+70.857*i,676,70,c)
        yazA(d,"1",F(57),660,931,46,56,(220,185,138))
    elif sekme == 2:
        bay = spr(CR,"clan_bayrak").resize((round(LW(196)),round(LH(169))),Image.LANCZOS)
        im.alpha_composite(bay,(round(LX(367)),round(LY(327))))
        im.alpha_composite(spr(CR,"clan_icerik").resize((W,H),Image.LANCZOS),(0,0))
        d=ImageDraw.Draw(im)
        yazA(d,"OLYMPOS",F(34),590,352,400,56,(244,244,244),"sol")
        yazA(d,"Grade: AccreditedKnight2",F(29),590,404,430,50,(244,244,244),"sol")
        uy=[("Leader","NxT_222",72,"Priest")]+[("Traine",n,72,"Priest") for n in
           ["Enestezi","Entelferit","Eruhlu","FATIHSULTANMEHMET","ErTuran","Erengel","SULTANABDULMECID"]]+[
           ("Traine","kerimmmm",72,"Rogue"),("Traine","YILDIRIMBEYAZID",72,"Priest"),
           ("Traine","S1KKO34",72,"Priest"),("Traine","xMegaTon",41,"Mage")]
        g=(60,230,60); f18=F(18)
        for i,(r_,n_,l_,j_) in enumerate(uy):
            ay=627+36.95*i
            yazA(d,r_,f18,350,ay,122,36.95,g); yazA(d,n_,f18,472,ay,342,36.95,g)
            yazA(d,str(l_),f18,814,ay,100,36.95,g); yazA(d,j_,f18,914,ay,115,36.95,g)
        yazA(d,"1",F(30),660,1099,46,40,(220,185,138))
        yazA(d,"16",F(19),627,1172,62,30,(244,244,244))
        yazA(d,"29/50",F(19),615,1217,74,32,(244,244,244))
    return im

# ---- Ana menu (321x989) ----
def ana_menu():
    w,h = 321,989
    im = zemin(w,h,0.92)
    im.alpha_composite(spr(MR,"ana_menu_cerceve"),(0,0))
    tam = Image.new("RGBA",(w,h+46),(0,0,0,0)); tam.alpha_composite(im,(0,46))
    k = spr(MR,"btn_kapat"); tam.alpha_composite(k,(w//2-k.width//2, 46-42))
    return tam

# ---- OPTIONS (854x1171) ----
ADLAR=["looting","cospre","vfx","game1","game2","game3","block","battle","pmblock","hide","sound"]
def options(sec):
    w,h = 854,1171
    im = zemin(w,h,0.95)
    im.alpha_composite(spr(MR,"panel_%02d_%s"%(sec,ADLAR[sec])),(1339-1018,283-166))
    for i,a in enumerate(ADLAR):
        dur = "secili" if i==sec else "normal"
        im.alpha_composite(spr(MR,"menu_%02d_%s_%s"%(i,a,dur)),(1034-1018,(298+86*i)-166))
    im.alpha_composite(spr(MR,"options_krom"),(0,0))
    im.alpha_composite(spr(MR,"btn_kapat"),(1775-1018,169-166))
    return im

def tabaka(basliklar_ve_resimler, dosya, sc=1.0, sutun=None):
    P=[(t,i) for t,i in basliklar_ve_resimler]
    n=len(P); sutun=sutun or n
    satir=(n+sutun-1)//sutun
    cw=max(int(i.width*sc) for _,i in P); chh=max(int(i.height*sc) for _,i in P)
    gap,head=14,28
    cv=Image.new("RGB",(cw*sutun+gap*(sutun+1), (chh+head)*satir+gap*(satir+1)),(20,20,20))
    d=ImageDraw.Draw(cv); f=F(16)
    for k,(t,i) in enumerate(P):
        r,c = divmod(k,sutun)
        x=gap+c*(cw+gap); y=gap+r*(chh+head+gap)
        d.text((x+2,y),t,font=f,fill=(255,205,110))
        cv.paste(i.convert("RGB").resize((int(i.width*sc),int(i.height*sc)),Image.LANCZOS),(x,y+head))
    cv.save(dosya); print(dosya, cv.size)

# Kullanim ornegi:
#   python3 -c "import sys;sys.path.insert(0,'arayuz/araclar');from paket_onizleme import *; \
#     tabaka([('CHAR INFO',character(0)),('CLAN',character(2)),('FRIENDS',character(3)), \
#             ('Ana menu',ana_menu())],'cikti.png',sc=0.72)"
# Paketleri once klasor agacina acmak gerekir (pathname/asset eslemesi).
