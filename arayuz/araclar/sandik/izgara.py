import sys
from PIL import Image, ImageDraw
i=int(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); Z=int(sys.argv[6]) if len(sys.argv)>6 else 5
im=Image.open('s%d.jpg'%i).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS); d=ImageDraw.Draw(im)
for x in range(x0 - x0%10 + 10, x1, 10):
    c=(255,0,0) if x%50==0 else (90,90,90); d.line(((x-x0)*Z,0,(x-x0)*Z,im.height),fill=c,width=1)
    if x%50==0: d.text(((x-x0)*Z+2,2),str(x),fill=(255,255,0))
for y in range(y0 - y0%10 + 10, y1, 10):
    c=(255,0,0) if y%50==0 else (90,90,90); d.line((0,(y-y0)*Z,im.width,(y-y0)*Z),fill=c,width=1)
    if y%50==0: d.text((2,(y-y0)*Z+2),str(y),fill=(255,255,0))
im.save('g%d.png'%i)
