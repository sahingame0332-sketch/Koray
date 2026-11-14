#!/usr/bin/env python3
"""NPC alim-satim adet/para penceresi: yazilarin fontu + puntosu (oyun_ici/punto.py IoU yontemi)."""
import os, sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","oyun_ici"))
import punto as P
P.REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","referans_gorseller","npc_alimsatim")
LS="/usr/share/fonts/truetype/liberation/"; P.ADAY.update({"LiberationSans-Bold":LS+"LiberationSans-Bold.ttf"})
W=(235,235,235)
for ad,t,k,kutu,r in (("baslik","Holy water","al_adet",(1900,556,2065,592),W),("buy","Buy Item Count:","al_adet",(1870,592,2100,624),W),
                      ("need","Need Money : 70","al_para",(1868,590,2102,624),W),("sell","Sell Item Count:","sat_adet",(1868,590,2096,622),W),
                      ("earn","Earn Money : 33","sat_para",(1866,592,2096,624),W),("sayi","1","al_adet",(1762,642,1788,672),(240,220,220)),
                      ("sayi3","3","sat_adet",(1762,642,1788,672),(240,220,220))):
    P.olc(ad,t,k,kutu,r,tol=70)
