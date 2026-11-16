"""Kayit 14-01-51: galeride yavas ileri sarilan oyun videosunun ekran kaydi (2712x1220). Oyun goruntusu ayni olcekte, ustunde
galeri katmanlari var (ust beyaz serit, sag panel, ipucu kutusu, sure kutusu, kaydirici). Oyun zamani sure kutusundan okunur (ocr.py).
Kareler: G/k_%04d.png (30 kare/sn kayit; depoya konmaz)."""
import os, numpy as np, glob, json
from PIL import Image
from scipy import ndimage
GK=os.environ.get("EFEKT7_KARELER","G")
fs=sorted(glob.glob(os.path.join(GK,"k_*.png")))
def Y(i): return np.asarray(Image.open(fs[i]).convert('RGB'),dtype=np.float32)
def med(L): return np.median(np.stack([Y(i) for i in L]),0)
UST=226; SAG=2570
OVR=[(1030,295,1712,408),(1155,895,1556,1005),(455,1060,2250,1135)]
def ovr_maske():
    m=np.zeros((1220,2712),bool); m[:UST]=True; m[:,SAG:]=True
    for a,b,c,d in OVR: m[b:d,a:c]=True
    return m
#  olay: (efekt kareleri, once zemin, sonra zemin)
TEMIZ=range(292,339)        # hicbir efektin olmadigi kareler (oyun zamani 1.9-2.3 sn): zemin
OLAY={"A":(range(160,248),range(150,159),TEMIZ),
      "B":(range(249,280),TEMIZ,range(640,690)),
      "C":(range(402,573),TEMIZ,range(640,690)),
      "D":(range(584,630),TEMIZ,range(640,690))}
KARAKTER=(1180,480,1700,1060)   # oyuncu karakteri bolgesi (efekt yok; hareketi siziyordu)
# hasar rengi (hedefin kirmiziya donmesi), tam gucte: L = zemin parlakligi (RGB ortalamasi)
#   R = 0.60 L + 162,  G = 0.95 L + 5,  B = 0.75 L     (4 karede olculdu, bkz. 10-efekt.md ek 7)
def kirmizi(L): return np.stack([0.60*L+162, 0.95*L+5, 0.75*L],-1)
