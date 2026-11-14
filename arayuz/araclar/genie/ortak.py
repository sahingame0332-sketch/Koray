"""Genie: ortak yardimcilar. Referanslar referans_gorseller/genie/ (2712x1220 telefon ekran goruntuleri):
  g_once    : genie paneli, pencere kapali (sahne)
  g_pencere : ayni sahne, AUTO ATTACK SETTINGS + SKILL PAGE acik
  g_aktif   : genie calisirken (GENIE rozeti, skill kilitleri), baska sahne"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B_,"..","..","referans_gorseller","genie")
OUT=os.path.join(B_,"..","..","kaynak","genie","sprites")
os.makedirs(OUT,exist_ok=True)
_c={}
def Y(ad):
    if ad not in _c: _c[ad]=np.asarray(Image.open(os.path.join(REF,ad+".jpg")).convert("RGB")).astype(float)
    return _c[ad]
def yaz(ad,rgba):
    Image.fromarray(np.clip(rgba,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png"))
def oku(ad): return np.asarray(Image.open(os.path.join(OUT,ad+".png"))).astype(float)
# Pencere zemini: olculen arka plan katkisi g_pencere ~= 45.6*(g_once/255)^1.8 (dogrusal degil; bkz. 11-genie.md)
def zemin_katkisi(B): return 45.6*(np.clip(B,0,255)/255.0)**1.8
ALFA_PENCERE=0.93     # sahnenin orta tonlarinda (60-110) olculen oran 0.057-0.078 -> 1-a ~ 0.07
