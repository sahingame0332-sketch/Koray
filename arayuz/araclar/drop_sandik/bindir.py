"""Uydurulan modeli her kirpintiya tel kafes olarak bindirir -> bindir.jpg"""
import numpy as np, json, sys
from PIL import Image, ImageDraw
from mesh import sandik; from geo import proj
K=json.load(open('kirp.json')); U=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'uydu.json'))
sh=U['sekil']; out=[]
for k,P in U['kam'].items():
    i,(x0,y0,x1,y1)=K[k]; im=Image.open('d%d.png'%i).convert('RGB').crop((x0,y0,x1,y1)); sc=3
    im=im.resize((im.width*sc,im.height*sc)); d=ImageDraw.Draw(im)
    acik=k=='c'
    for ad,T in sandik(1.0,sh[0],sh[1],sh[2],(sh[3],sh[4]),acik=acik,aci=U.get('aci',0)):
        col={'on':(255,0,0),'arka':(0,120,255),'uc':(255,255,0),'kapak':(0,255,0)}.get(ad,(255,0,255))
        for tri,_ in T:
            q=proj(np.array(tri),P)
            d.line([(float(x)*sc,float(y)*sc) for x,y,_ in q]+[(float(q[0,0])*sc,float(q[0,1])*sc)],fill=col,width=1)
    # kilit: on yuz merkezi
    c=proj(np.array([[0.5,sh[1]*0.45,sh[0]/2]]),P)[0]; d.ellipse([c[0]*sc-6,c[1]*sc-6,c[0]*sc+6,c[1]*sc+6],outline=(255,0,255),width=3)
    im=im.resize((im.width*450//im.height,450)); out.append(im)
W=sum(o.width for o in out); c=Image.new('RGB',(W,450)); x=0
for o in out: c.paste(o,(x,0)); x+=o.width
c.save('bindir.jpg',quality=85)
