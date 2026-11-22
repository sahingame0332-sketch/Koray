"""ItemBox bicimi + oyun fotograflarinin dokulari: ItemBox 360 karelerinin kamerasiyla model <-> ItemBox, ayrica
oyun fotograflarinin acisindan (g, b, c). -> itembox_onizleme.png"""
import numpy as np, json, sys
from PIL import Image, ImageDraw
from mesh import sandik; from ciz import ciz; import itembox_uydur as I
J=json.load(open('itembox.json')); x=np.array(J['x']); D,HB,HL,US,O=J['sekil']
DOK={k:np.asarray(Image.open('ib/t_%s.png'%k).convert('RGBA'),dtype=np.float32) for k in ['on','arka','uc','kapak','ust_acik','kapak_ic','kapak_taban']}
ACI=np.radians(json.load(open('ib/olcu.json'))['aci_derece'] or 150)
def model(acik): 
    S=sandik(1.0,D,HB,HL,(US,0),acik,ACI,o=O); S=[s for s in S if s[0]!='kapak_taban']+[s for s in S if s[0]=='kapak_taban']
    return [(n,[([(p[0]-0.5,p[1],p[2]) for p in t],uv) for t,uv in T]) for n,T in S]
ust=[];alt=[]
for i in (43,1,7,13,19,31,37):
    im=np.asarray(Image.open('ib_%02d.png'%i).convert('RGB'),np.float32)[70:395,20:400]
    zem=np.zeros_like(im)+np.array([24,32,42.])
    P=I.kam(x,i); P=list(P); P[7]-=20; P[8]-=70
    r=ciz(model(False),DOK,P,(380,325),zem)[...,:3]
    ust.append(Image.fromarray(im.astype(np.uint8))); alt.append(Image.fromarray(r.clip(0,255).astype(np.uint8)))
# acik + yeni acilar
ek=[]
for yaw,acik in ((25,False),(150,False),(-35,True),(40,True)):
    P=[np.radians(yaw),np.radians(30),0,0,-0.45,(8.5 if not acik else 11.5),2000,190,(190 if not acik else 215)]
    ek.append(Image.fromarray(ciz(model(acik),DOK,P,(380,325),np.zeros((325,380,3))+np.array([74,82,52.]))[...,:3].clip(0,255).astype(np.uint8)))
W=380*7+60; C=Image.new('RGB',(W,325*3+120),(20,20,20)); d=ImageDraw.Draw(C)
d.text((6,4),'ITEMBOX (client 360) - ustte  /  ItemBox bicimi + oyun fotograflarinin dokulari - altta (ayni kamera)',fill=(255,255,0))
for k,(a,b) in enumerate(zip(ust,alt)): C.paste(a,(k*390,20)); C.paste(b,(k*390,20+335))
d.text((6,20+670),'yeni acilar: kapali / acik',fill=(255,255,0))
for k,e in enumerate(ek): C.paste(e,(k*390,20+690))
C.save(sys.argv[1] if len(sys.argv)>1 else 'itembox_onizleme.png')
