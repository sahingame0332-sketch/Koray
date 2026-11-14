#!/usr/bin/env python3
"""Gorev pencereleri yazilari: font + punto (oyun_ici/punto.py IoU yontemi; adaylara Liberation Sans eklendi — Arial metrikli)."""
import os, sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","oyun_ici"))
import punto as P
from ortak import REF
LS="/usr/share/fonts/truetype/liberation/"
P.ADAY.update({"LiberationSans-Bold":LS+"LiberationSans-Bold.ttf","LiberationSans-Regular":LS+"LiberationSans-Regular.ttf"})
P.REF=REF
F=["LiberationSans-Bold","LiberationSans-Regular","Roboto-Bold","Roboto-Regular"]
OLC=[("liste_aciklama","Test NPC Description.","q_liste",(1265,510,1445,537),(0xDD,0x93,0x44)),
     ("liste_giris","Starter Weapon&Armor","q_liste",(1230,722,1482,752),(0xF6,0xE1,0xE1)),
     ("liste_baslik","QuestList","q_liste",(1258,405,1398,444),(0xF9,0xE5,0xE4)),
     ("detay_baslik","Starter Weapon&Armor","q_detay",(1222,203,1446,232),(0xEE,0xDA,0xDA)),
     ("detay_aciklama","Kill: 20x Orc Watcher","q_detay",(1254,300,1422,322),(0xE0,0x98,0x69)),
     ("hedef1","Hunt: Shilan","q_detay",(1180,509,1282,531),(0xEA,0xD8,0xD8)),
     ("hedef2","Shilan öldür.","q_detay",(1180,538,1282,562),(0xEA,0xD7,0xD7)),
     ("odul4","Silan Pauldron","q_detay",(1418,727,1537,750),(0xE7,0xD5,0xD4)),
     ("odul1","Rapt Bow(+2)","q_detay",(1190,651,1302,677),(0xE9,0xD6,0xD6)),
     ("accepted","Accepted","q_detay",(1222,964,1328,996),(0xF0,0xDD,0xDE)),
     ("close","Close","q_detay",(1400,964,1470,991),(0xEB,0xD9,0xDA)),
     ("objectives","Objectives","q_detay",(1118,455,1211,481),(0xEE,0xDA,0xDA)),
     ("sayi","25","q_detay",(1152,536,1181,561),(0xEE,0xD8,0xD4))]
for ad,t,k,kutu,r in OLC: P.olc(ad,t,k,kutu,r,tol=60,fontlar=F)
