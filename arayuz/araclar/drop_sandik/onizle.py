"""Orijinal <-> model: her goruntu icin uydurulan kamerayla modeli fotografin uzerine cizer (yazilim cizici, ortografik).
Ust satir orijinal kirpinti, alt satir model + ayni zemin. -> onizleme.png"""
import numpy as np, json, sys
from PIL import Image, ImageDraw
from scipy import ndimage
from mesh import sandik; from ciz import ciz
U=json.load(open('uydu.json')); D,HB,HL,h1,c=U['sekil']; K=json.load(open('kirp.json'))
DOK={k:np.asarray(Image.open('t_%s.png'%k).convert('RGBA'),dtype=np.float32) for k in ['on','arka','uc','kapak','ust_acik','kapak_ic','kapak_taban']}
def ciz_alfa(S,P,boyut,zemin):
    """ciz() alfa>0.5 testli; kapak_taban icin once ic, sonra taban (ayri gecis) -> basit sira yeterli"""
    return ciz(S,DOK,P,boyut,zemin)
sira=sys.argv[2].split(',') if len(sys.argv)>2 else ['g','a','b','f','d','c']; ust=[]; alt=[]
for k in sira:
    i,(x0,y0,x1,y1)=K[k]; im=np.asarray(Image.open('d%d.png'%i).convert('RGB'),dtype=np.float32)[y0:y1,x0:x1]
    m=np.load('m_%s.npy'%k)
    # zemin: sandik pikselleri cevreden doldurulur (temiz cim/toprak)
    _,(iy,ix)=ndimage.distance_transform_edt(ndimage.binary_dilation(m,np.ones((9,9))),return_indices=True); bg=im[iy,ix]
    bg=ndimage.uniform_filter(bg,(9,9,1))
    P=kaydir(U['kam'][k],x0,y0)
    S=sandik(1.0,D,HB,HL,(h1,c),k=='c',U.get('aci',0))
    S=[s for s in S if s[0]!='kapak_taban']+[s for s in S if s[0]=='kapak_taban']
    r=ciz_alfa(S,P,(im.shape[1],im.shape[0]),bg)[...,:3]
    h=int(sys.argv[3]) if len(sys.argv)>3 else 300; f=lambda A:Image.fromarray(A.clip(0,255).astype(np.uint8)).resize((int(A.shape[1]*h/A.shape[0]),h),Image.LANCZOS)
    ust.append(f(im)); alt.append(f(r))
W=sum(o.width for o in ust)+10*(len(ust)-1); C=Image.new('RGB',(W,640),(20,20,20)); x=0
for o,r in zip(ust,alt): C.paste(o,(x,0)); C.paste(r,(x,340)); x+=o.width+10
d=ImageDraw.Draw(C); d.text((6,304),'ORIJINAL (ustte)  /  MODEL (altta, ayni kamera)',fill=(255,255,255))
C.save(sys.argv[1] if len(sys.argv)>1 else 'onizleme.png')
