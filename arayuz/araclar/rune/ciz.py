#!/usr/bin/env python3
"""Ozgun run dairesi (stok gorsel KOPYALANMADI; ayni turde kendi tasarim). 1024x1024 dokular:
  rune_cizgi.png : R = dis katman (halkalar, cetvel bandi, run bandi)  G = ic katman (heksagram, semboller, ic run halkasi)
                   B = dis katmanin isiltisi (bulanik)              A = ic katmanin isiltisi
  rune_gurultu.png : dosenebilir fbm gurultu (alev titremesi/dili icin), 256x256
Cizgiler 4x buyuk cizilip kucultulur (yumusak kenar)."""
import os, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFilter
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","rune")
N=1024; S=4; M=N*S; C=M/2
random.seed(1298)
def yeni(): return Image.new("L",(M,M),0)
def daire(d,r,w): d.ellipse((C-r,C-r,C+r,C+r),outline=255,width=int(w))
def cizgi(d,p,q,w): d.line([p,q],fill=255,width=int(w)); 
def kutup(r,a): return (C+r*math.cos(a),C+r*math.sin(a))
# ---- uydurma run alfabesi: 3x5 izgarada govde + dallar ----
NOKTA=[(x,y) for y in range(5) for x in range(3)]
def run_uret():
    v=[]
    v.append(((1,0),(1,4)))                                  # govde
    for _ in range(random.randint(1,3)):
        y=random.randint(0,3); s=random.choice([-1,1])
        v.append(((1,y),(1+s,y+random.choice([1,0,1]))))
    if random.random()<0.35: v.append(((0,random.randint(0,2)),(2,random.randint(2,4))))
    return v
ALFABE=[run_uret() for _ in range(28)]
def run_yaz(d,merkez,aci,boy,w,glif):
    sx=boy/4*0.8; sy=boy/4
    ca,sa=math.cos(aci),math.sin(aci)
    def t(p):
        x=(p[0]-1)*sx; y=(p[1]-2)*sy
        return (merkez[0]+x*ca-y*sa, merkez[1]+x*sa+y*ca)
    for a,b in glif: d.line([t(a),t(b)],fill=255,width=int(w))
def run_bandi(d,r,boy,w,adim,ofset=0):
    n=int(2*math.pi*r/adim)
    for i in range(n):
        a=2*math.pi*i/n+ofset
        run_yaz(d,kutup(r,a),a+math.pi/2,boy,w,random.choice(ALFABE))
W=S*3.2
# ================= DIS KATMAN =================
dis=yeni(); d=ImageDraw.Draw(dis)
R0=M*0.485
daire(d,R0,W*1.3); daire(d,R0-S*14,W*0.8)
run_bandi(d,R0-S*30,S*20,W*0.9,S*17)                  # en dis ince run yazisi
daire(d,R0-S*46,W*0.9); daire(d,R0-S*72,W*0.9)
n=72
for i in range(n):                                     # cetvel bandi
    a=2*math.pi*i/n; cizgi(d,kutup(R0-S*46,a),kutup(R0-S*72,a),W*0.8)
daire(d,R0-S*84,W*1.1)
run_bandi(d,R0-S*112,S*44,W*1.5,S*36,0.03)             # kalin run bandi
daire(d,R0-S*140,W*1.1)
# ================= IC KATMAN =================
ic=yeni(); d=ImageDraw.Draw(ic)
R1=R0-S*152
for k in range(2):                                      # heksagram (iki ucgen)
    p=[kutup(R1,-math.pi/2+k*math.pi/3+i*2*math.pi/3) for i in range(3)]
    d.polygon(p,outline=255,width=int(W)); 
daire(d,R1*0.578,W*0.9)                                  # heksagram ic cemberi
# alti kucuk sembol dairesi (yildiz uclarinda)
SR=S*46
for i in range(6):
    a=-math.pi/2+i*math.pi/3; c=kutup(R1,a)
    d.ellipse((c[0]-SR,c[1]-SR,c[0]+SR,c[1]+SR),fill=0,outline=255,width=int(W))
    t=i%3
    if t==0:                                              # gunes
        d.ellipse((c[0]-SR*0.35,c[1]-SR*0.35,c[0]+SR*0.35,c[1]+SR*0.35),outline=255,width=int(W*0.8))
        for j in range(8):
            b=j*math.pi/4; d.line([(c[0]+SR*0.5*math.cos(b),c[1]+SR*0.5*math.sin(b)),(c[0]+SR*0.8*math.cos(b),c[1]+SR*0.8*math.sin(b))],fill=255,width=int(W*0.7))
    elif t==1:                                            # hilal
        d.ellipse((c[0]-SR*0.6,c[1]-SR*0.6,c[0]+SR*0.6,c[1]+SR*0.6),fill=255)
        d.ellipse((c[0]-SR*0.35,c[1]-SR*0.7,c[0]+SR*0.75,c[1]+SR*0.5),fill=0)
    else:                                                 # alev damlasi
        pts=[(c[0],c[1]-SR*0.7),(c[0]+SR*0.4,c[1]),(c[0],c[1]+SR*0.55),(c[0]-SR*0.4,c[1])]
        d.polygon(pts,outline=255,width=int(W*0.8)); d.line([(c[0],c[1]-SR*0.2),(c[0],c[1]+SR*0.3)],fill=255,width=int(W*0.7))
run_bandi(d,R1*0.578-S*18,S*20,W*0.9,S*17)               # ic run halkasi
daire(d,R1*0.578-S*34,W*0.8)
R2=R1*0.578-S*34                                          # merkez: 8 kollu yildiz
for i in range(8):
    a=i*math.pi/4; b=a+math.pi/8; cizgi(d,kutup(R2*0.85,a),kutup(R2*0.32,a+math.pi/8),W*0.7); cizgi(d,kutup(R2*0.85,a),kutup(R2*0.32,a-math.pi/8),W*0.7)
    cizgi(d,(C,C),kutup(R2*0.85,a),W*0.4)
daire(d,R2*0.18,W*0.8)
def kucult(im): return im.resize((N,N),Image.LANCZOS)
D=kucult(dis); I=kucult(ic)
def isilti(im):
    a=np.asarray(im.filter(ImageFilter.GaussianBlur(6))).astype(float)*0.6+np.asarray(im.filter(ImageFilter.GaussianBlur(18))).astype(float)*1.4
    return Image.fromarray(np.clip(a*1.6,0,255).astype(np.uint8))
Image.merge("RGBA",(D,I,isilti(D),isilti(I))).save(os.path.join(OUT,"rune_cizgi.png"))
# ---- dosenebilir fbm gurultu ----
def fbm(n=256,okt=5,seed=7):
    rng=np.random.default_rng(seed); t=np.zeros((n,n))
    for o in range(okt):
        f=4*2**o; g=rng.random((f,f))
        u=np.linspace(0,f,n,endpoint=False); i0=np.floor(u).astype(int); fr=u-i0; fr=fr*fr*(3-2*fr)
        a=g[i0][:,i0]; b=g[i0][:,(i0+1)%f]; c=g[(i0+1)%f][:,i0]; e=g[(i0+1)%f][:,(i0+1)%f]
        x=fr[None,:]; y=fr[:,None]
        t+=((a*(1-x)+b*x)*(1-y)+(c*(1-x)+e*x)*y)*0.5**o
    t=(t-t.min())/(t.max()-t.min()); return t
Image.fromarray((fbm()*255).astype(np.uint8)).save(os.path.join(OUT,"rune_gurultu.png"))
print("tamam")
