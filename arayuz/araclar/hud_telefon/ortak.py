"""Telefon HUD'i (2712x1220) icin ortak yardimcilar. Kareler oyun_ici/ ve merchant/ referanslarindan."""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B,"..","..","referans_gorseller")
OUT=os.path.join(B,"..","..","kaynak","hud_telefon","sprites")
YOL={"m_once":"merchant/m_once","m_tezgah":"merchant/m_tezgah","m_tezgah_hedef":"merchant/m_tezgah_hedef","s_once":"merchant/s_once","s_sonra":"merchant/s_sonra",
     "f_equip":"merchant/f_equip","f_unequip":"merchant/f_unequip","f_npc":"merchant/f_npc","m_menu":"merchant/m_menu","s_menu":"merchant/s_menu",
     "v1_buffsiz":"oyun_ici/v1_buffsiz","v1_slotlar":"oyun_ici/v1_slotlar","v1_buff3":"oyun_ici/v1_buff3","v1_once":"oyun_ici/v1_once",
     "v2_hedef":"oyun_ici/v2_hedef","v2_drop_bos":"oyun_ici/v2_drop_bos","saveslot":"oyun_ici/foto_saveslot"}
_c={}
def Y(ad):
    if ad not in _c: _c[ad]=np.asarray(Image.open(os.path.join(REF,YOL[ad]+".jpg")).convert("RGB")).astype(np.float32)
    return _c[ad]
def statik(kareler,kutu,e0=16.0,e1=44.0,bulanik=1.0):
    """Farkli arka planli karelerde degismeyen pikseller HUD'dir.
    Donus: (medyan RGB, alfa 0..1). alfa = 1 - clip((aralik-e0)/(e1-e0))."""
    x,y,w,h=kutu; st=np.stack([ndimage.gaussian_filter(Y(k)[y:y+h,x:x+w],[bulanik,bulanik,0]) for k in kareler])
    ar=(st.max(0)-st.min(0)).max(2)
    al=1-np.clip((ar-e0)/(e1-e0),0,1)
    ham=np.stack([Y(k)[y:y+h,x:x+w] for k in kareler])
    return np.median(ham,axis=0),al
def temizle(al,minalan=400,kapat=5,doldur=True):
    """kucuk adaciklari at, delikleri doldur, en buyuk parcayi tut"""
    m=al>0.5
    m=ndimage.binary_closing(m,np.ones((kapat,kapat)))
    lab,n=ndimage.label(m)
    if n>1:
        s=ndimage.sum(m,lab,range(1,n+1)); tut=np.zeros(n+1,bool); tut[1:]=s>=minalan; m=tut[lab]
    if doldur: m=ndimage.binary_fill_holes(m)
    return np.where(m,np.maximum(al,ndimage.gaussian_filter(m.astype(float),0.7)),al*0)
def rgba(rgb,al): return np.dstack([rgb,np.clip(al,0,1)*255])
def opak(kare,kutu):
    x,y,w,h=kutu; O=Y(kare)[y:y+h,x:x+w]; return np.dstack([O,np.full(O.shape[:2],255.0)])
def daire(kare,cx,cy,d,yumusat=1.5):
    r=d/2.0; n=int(round(d)); x0=int(round(cx-r)); y0=int(round(cy-r)); O=Y(kare)[y0:y0+n,x0:x0+n]
    yy,xx=np.mgrid[0:n,0:n]; dist=np.sqrt((xx-(n-1)/2.0)**2+(yy-(n-1)/2.0)**2)
    return np.dstack([O,np.clip((r-dist)/yumusat+0.5,0,1)*255]),(x0,y0)
def kaydet(ad,a): Image.fromarray(np.clip(a,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png"))
def dama(a,k=12):
    a=np.asarray(a,float); H,W=a.shape[:2]; ch=(np.indices((H,W)).sum(0)//k)%2
    bg=np.where(ch[...,None]==0,np.array([200,60,200]),np.array([120,30,120])).astype(float); al=a[:,:,3:4]/255
    return Image.fromarray((a[:,:,:3]*al+bg*(1-al)).astype(np.uint8))
def satir_doldur(a,kutu,serit=14):
    """kutu=(x0,y0,x1,y1) icini, her satirda sol ve sag komsu seritlerin medyanlari arasinda dogrusal gecisle doldurur."""
    x0,y0,x1,y1=kutu; n=x1-x0; t=((np.arange(n)+0.5)/n)[:,None]
    for y in range(y0,y1):
        L=np.median(a[y,max(0,x0-serit):x0,:3],axis=0); R=np.median(a[y,x1:x1+serit,:3],axis=0)
        a[y,x0:x1,:3]=L*(1-t)+R*t
    a[y0:y1,x0:x1,3]=255
def cim_disi(kare,kutu,ac=5):
    """Kutu kenarindan baslayip cim benzeri (yesil baskin) piksellerden gecerek disariyi bulur; kalan = HUD ogesi."""
    x,y,w,h=kutu; a=Y(kare)[y:y+h,x:x+w]; R,G,Bl=a[:,:,0],a[:,:,1],a[:,:,2]
    cim=(G>Bl*1.6)&(G>R*0.9)&(a.max(2)>20)
    cim=ndimage.binary_dilation(cim,np.ones((3,3)))
    lab,n=ndimage.label(cim)
    kenar=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])); kenar=kenar[kenar>0]
    ic=~np.isin(lab,kenar)
    ic=ndimage.binary_opening(ic,np.ones((ac,ac)))
    ic=ndimage.binary_fill_holes(ic)
    return ic
