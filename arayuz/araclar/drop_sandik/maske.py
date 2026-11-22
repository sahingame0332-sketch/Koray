import numpy as np, json, cv2
from PIL import Image
from scipy import ndimage
K={'a':(1,(765,20,995,240)),'b':(1,(485,455,780,690)),'c':(3,(625,105,985,450)),'d':(3,(1525,340,1790,635)),
   'e':(4,(1588,590,1783,741)),'f':(4,(1525,721,1767,905)),'g':(5,(641,596,826,758))}
# a: Lv yazisi bolgesini disarida tut
json.dump(K,open('kirp.json','w'))
out=[]
for k,(i,(x0,y0,x1,y1)) in K.items():
    I=cv2.imread('d%d.png'%i)[y0:y1,x0:x1].copy()
    h,w=I.shape[:2]; m=np.zeros((h,w),np.uint8)
    bg=np.zeros((1,65)); fg=np.zeros((1,65))
    r=(8,8,w-16,h-16)
    if k=='a': r=(8,8,w-60,h-16)
    cv2.grabCut(I,m,r,bg,fg,8,cv2.GC_INIT_WITH_RECT)
    M=(m==1)|(m==3)
    l,n=ndimage.label(M); s=ndimage.sum(M,l,range(1,n+1)); M=l==(1+np.argmax(s))
    M=ndimage.binary_fill_holes(M)
    np.save('m_%s.npy'%k,M)
    v=I[...,::-1].astype(float); v[~M]=v[~M]*0.2+np.array([0,80,160])*0.5
    out.append(Image.fromarray(v.clip(0,255).astype(np.uint8)))
W=sum(o.width for o in out); c=Image.new('RGB',(W,max(o.height for o in out)))
x=0
for o in out: c.paste(o,(x,0)); x+=o.width
c.save('maske.jpg')
