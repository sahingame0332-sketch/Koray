import sys
from PIL import Image, ImageDraw
i,x0,y0,x1,y1,sc=map(int,sys.argv[1:7])
im=Image.open(f'd{i}.png').convert('RGB').crop((x0,y0,x1,y1)); im=im.resize((im.width*sc,im.height*sc),Image.NEAREST)
d=ImageDraw.Draw(im)
for x in range((x0//10+1)*10,x1,10):
    c=(255,0,0) if x%50==0 else (255,255,0); X=(x-x0)*sc
    if x%50==0 or sc>=4: d.line([(X,0),(X,im.height)],fill=c,width=1)
    if x%50==0: d.text((X+2,2),str(x),fill=(255,0,0))
for y in range((y0//10+1)*10,y1,10):
    c=(255,0,0) if y%50==0 else (255,255,0); Y=(y-y0)*sc
    if y%50==0 or sc>=4: d.line([(0,Y),(im.width,Y)],fill=c,width=1)
    if y%50==0: d.text((2,Y+2),str(y),fill=(255,0,0))
im.save(sys.argv[7])
