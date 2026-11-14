"""Gorev NPC'si: ortak. Referanslar referans_gorseller/gorev/ (2712x1220 telefon):
  q_once  : NPC uzakta, basinin ustunde "?" rozeti      q_open  : NPC yakin, Open dugmesi
  q_liste : QuestList penceresi (q_open ile ayni sahne) q_detay : gorev detayi "Starter Weapon&Armor"
"""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B_,"..","..","referans_gorseller","gorev")
OUT=os.path.join(B_,"..","..","kaynak","gorev","sprites"); os.makedirs(OUT,exist_ok=True)
_c={}
def Y(ad):
    if ad not in _c: _c[ad]=np.asarray(Image.open(os.path.join(REF,ad+".jpg")).convert("RGB")).astype(float)
    return _c[ad]
def yaz(ad,rgba): Image.fromarray(np.clip(rgba,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png"))
def oku(ad): return np.asarray(Image.open(os.path.join(OUT,ad+".png"))).astype(float)
