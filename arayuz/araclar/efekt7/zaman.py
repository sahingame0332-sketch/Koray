"""Benzersiz oyun kareleri + oyun zamani (sure kutusundan okunan; okunamayanlar komsulardan dogrusal)."""
import numpy as np, json
from ortak import *
import ocr
def zamanlar():
    T=ocr.sablon(); t=[];s=[]
    for i in range(len(fs)): a,b=ocr.oku(i,T); t.append(a); s.append(b)
    t=np.array(t); ok=np.array(s)<=0.12; i=np.arange(len(t))
    t=np.interp(i,i[ok],t[ok]); return t
def benzersiz(aralik,esik=0.6):
    out=[aralik[0]]; p=Y(aralik[0])[240:1060,300:1700:2]
    for i in aralik[1:]:
        q=Y(i)[240:1060,300:1700:2]
        if np.abs(q-p).mean()>esik: out.append(i); p=q
    return out
if __name__=="__main__":
    t=zamanlar(); json.dump(list(map(float,t)),open("zaman.json","w"))
    r={}
    for ad,(E,o,s) in OLAY.items():
        u=benzersiz(list(E)); r[ad]=[(i,round(float(t[i]),3)) for i in u]; print(ad,len(u),r[ad][:3],'...',r[ad][-2:])
    json.dump(r,open("benzersiz.json","w"))
