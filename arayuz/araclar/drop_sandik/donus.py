"""Yeni acilar: kapali + acik sandik, oyun kamerasi egimi (35 derece), 6 yon; notr zemin -> donus.png"""
import numpy as np, json, sys
from PIL import Image
from mesh import sandik; from ciz import ciz
U=json.load(open('uydu.json')); D,HB,HL,h1,c=U['sekil']
DOK={k:np.asarray(Image.open('t_%s.png'%k).convert('RGBA'),dtype=np.float32) for k in ['on','arka','uc','kapak','ust_acik','kapak_ic','kapak_taban']}
Z=np.zeros((260,300,3))+np.array([74,82,52.]); out=[]
for acik in (False,True):
    sat=[]
    for yaw in (0,35,90,145,180,-60):
        S=sandik(1.0,D,HB,HL,(h1,c),acik,U.get('aci',0)); S=[s for s in S if s[0]!='kapak_taban']+[s for s in S if s[0]=='kapak_taban']
        P=[np.radians(yaw),np.radians(35),0,150,150,175]
        q=np.array([[x-0.5,y,z] for _,T in S for t,_ in T for x,y,z in t])
        P0=[P[0],P[1],0,150,150,175]
        r=ciz([(n,[([(x-0.5,y,z) for x,y,z in t],uv) for t,uv in T]) for n,T in S],DOK,P0,(300,260),Z.copy())
        sat.append(Image.fromarray(r[...,:3].clip(0,255).astype(np.uint8)))
    out.append(sat)
C=Image.new('RGB',(6*300+50,2*260+10),(20,20,20))
for j,sat in enumerate(out):
    for i,im in enumerate(sat): C.paste(im,(i*310,j*270))
C.save(sys.argv[1] if len(sys.argv)>1 else 'donus.png')
