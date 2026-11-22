"""Oyun fotograflarindan cikan dokulari ItemBox bicimine uyarlar (cikti: ib/t_*.png, ib/olcu.json).
 - Govde on/arka/uc (govde kismi): ust kenar + tahtalar + alt cerceve; tahta bolgesi 4 esit tahtaya (on: kilitli iki tahta
   + arkadan iki tahta), cerceveler olceklenmez.
 - Uc kemeri: eski (koseli) kemer -> yeni super-elips kemer, ayni aci + ayni goreli yaricap ile esleme; kemer disi saydam.
 - Kapak, kapak agzi, altin, kapak ici: bicimden bagimsiz, aynen."""
import numpy as np, json, os, shutil
from PIL import Image
from scipy import ndimage
from mesh import kesit
PX=256
E0=json.load(open('olcu.json')); IB=json.load(open('itembox.json'))['sekil']
D0,HB0,HL0=E0['D'],E0['HB'],E0['HL']; n0=(E0['h1'],E0['c'])
D1,HB1,HL1,US,O=IB; a0=D0/2; aL1=D1*(1+O)/2
os.makedirs('ib',exist_ok=True)
yuk=lambda p:np.asarray(Image.open(p).convert('RGBA'),np.float32)
def kaydet(ad,T): Image.fromarray(T.clip(0,255).astype(np.uint8),'RGBA').save('ib/t_%s.png'%ad)
def boy(A,h):            # satir sayisini h'ye getir (dikey yeniden ornekleme)
    y=(np.arange(h)+0.5)*A.shape[0]/h-0.5
    return np.stack([ndimage.map_coordinates(A[...,c],[np.repeat(y[:,None],A.shape[1],1),np.tile(np.arange(A.shape[1]),(h,1))],order=1,mode='nearest') for c in range(4)],-1)
def tahta_sinir(A):
    """ust kenar bitisi, tahtalar arasi karanlik cizgi, alt cerceve baslangici (satir)"""
    r=A[:,int(A.shape[1]*0.12):int(A.shape[1]*0.3),:3]; sat=(r.max(-1)-r.min(-1)).mean(1)
    tah=np.nonzero(sat>12)[0]; ust,alt=tah[0],tah[-1]+1
    lum=r.mean((1,2)); orta=ust+np.argmin(lum[ust+8:alt-8])+8
    return ust,orta,alt
def kilit_sil(R):
    """kilit plakasi bolgesi (sutun 0.36-0.66 W): sol yarisi soldaki, sag yarisi sagdaki tahta blogundan kopyalanir
    (tahta damari yatay; satirlar ayni kalir), birlesim 4 px yumusak"""
    R=R.copy(); W=R.shape[1]; x0,x1=int(0.36*W),int(0.66*W); xm=(x0+x1)//2; w=x1-x0
    sol=R[:,x0-(xm-x0):x0].copy(); sag=R[:,x1:x1+(x1-xm)].copy()
    R[:,x0:xm]=sol; R[:,xm:x1]=sag
    for xs in (x0,xm,x1):
        for d in range(-2,3):
            if 0<xs+d<W-1: R[:,xs+d]=0.5*R[:,xs+d]+0.25*(R[:,xs+d-1]+R[:,xs+d+1])
    return R
def govde_yuz(A,B=None,kilitsiz=False):
    """ust kenar + 4 esit tahta + alt cerceve; tahtalar ayni dokudan (ikinci kopyada kilit silinmis)"""
    u,o,a=tahta_sinir(A); u+=2; a-=2           # sinir satirlarindaki kenar grisi tahtalar arasina tasinmasin
    H1=int(round(A.shape[0]*HB1/HB0)); bolge=H1-u-(A.shape[0]-a)
    ikinci=A[u:a] if kilitsiz else kilit_sil(A[u:a])
    tah=boy(np.concatenate([A[u:a],ikinci],0),bolge)
    return np.concatenate([A[:u],tah,A[a:]],0)
on,arka=yuk('t_on.png'),yuk('t_arka.png')
kaydet('on',govde_yuz(on,arka)); kaydet('arka',govde_yuz(arka,arka))
# uc
U0=yuk('t_uc.png'); H0=U0.shape[0]; W0=U0.shape[1]; vb0=HB0/(HB0+HL0)
govde0=U0[int(round(H0*(1-vb0))):]                       # alt kisim = govde ucu
gov1=govde_yuz(govde0,kilitsiz=True)
H1=int(round(PX*(HB1+HL1))); W1=W0
gov1=boy(gov1,int(round(H1*HB1/(HB1+HL1))))
hk=H1-gov1.shape[0]
# kemer eslemesi
v,u=np.mgrid[0:hk,0:W1]+0.5; y=(1-v/hk)*HL1; z=aL1-u/W1*(2*aL1)
zn,yn=z/aL1,y/HL1; r=(np.abs(zn)**US+np.abs(yn)**US)**(1/US); th=np.arctan2(yn,zn)
ph=np.linspace(0,np.pi,2000); bz,by=kesit(ph,a0,HL0,n0); bth=np.arctan2(by/HL0,bz/a0); brn=np.hypot(bz/a0,by/HL0)
o=np.argsort(bth); rb=np.interp(th,bth[o],brn[o])
# kenar bandi (cerceve): ayni aci + ayni goreli yaricap; ic (tahtalar): dogrusal olcek -> tahtalar duz kalir
# cerceve bandi her yerde ayni kalinlikta: eski kemerin temiz yan kesiminden (30 derece) radyal profil alinir
TB=0.16; thr=np.where(zn>=0,np.radians(30),np.radians(150)); rbr=np.interp(thr,bth[o],brn[o])
zr=r*rbr*np.cos(thr)*a0; yr=r*rbr*np.sin(thr)*HL0
zl=zn*a0*0.55; yl=yn*HL0*0.80
w=np.clip((r-(1-TB))/0.03,0,1)
zo=zl*(1-w)+zr*w; yo=(yl*(1-w)+yr*w)+HB0
uo=(a0-zo)/D0*W0-0.5; vo=(1-yo/(HB0+HL0))*H0-0.5
kem=np.stack([ndimage.map_coordinates(U0[...,c],[vo,uo],order=1,mode='nearest') for c in range(4)],-1)
kem[...,3]=255*np.clip((1-r)*hk/1.2+0.5,0,1)
kem[:,W1//2:]=kem[:,:W1-W1//2][:,::-1]        # kemer simetrik (on yarisi aynalanir; tepe dikis cizgisi olmaz)
yeni=np.concatenate([kem,np.dstack([gov1[...,:3],np.full(gov1.shape[:2],255.)])],0)
kaydet('uc',yeni)
for k in ['kapak','kapak_taban','ust_acik','kapak_ic']: shutil.copy('t_%s.png'%k,'ib/t_%s.png'%k)
json.dump({'L':1.0,'D':D1,'HB':HB1,'HL':HL1,'us':US,'tasma':O,'aci_derece':E0.get('aci_derece')},open('ib/olcu.json','w'))
print('on',Image.open('ib/t_on.png').size,'uc',yeni.shape)
