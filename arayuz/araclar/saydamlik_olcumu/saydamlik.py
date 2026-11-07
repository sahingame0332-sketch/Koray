#!/usr/bin/env python3
"""Bir pencerenin zemin saydamlığını ekran görüntüsünden ölçer.

Yöntem: pencere kenarının hemen dışındaki oyun dünyası (b) ile hemen içindeki
boş zemin (o) karşılaştırılır. Zemin saf siyah ve alfa a ise  o = (1-a)·b,
yani geçirgenlik t = o/b  ve  alfa = 1-t.

Kenarın iki yanında arka planın yerel olarak düz olduğu varsayılır; bu yüzden
yalnızca dış şeridin düz ve yeterince parlak olduğu satırlar sayılır ve iç
şeritte arayüz öğelerini dışlamak için 10. yüzdelik kullanılır.

Kullanım:
  python3 saydamlik.py EKRAN.png  DIS_X0 DIS_X1  IC_X0 IC_X1  Y0 Y1
  python3 saydamlik.py EKRAN.png --profil X0 X1 Y0 Y1      # ham kesit yazdırır
"""
import sys
import numpy as np
from PIL import Image

def profil(path, x0, x1, y0, y1):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    p = a[y0:y1, x0:x1].mean(axis=(0, 2))
    for i, v in enumerate(p):
        print("  x=%5d %7.1f %s" % (x0 + i, v, "#" * int(v / 4)))

def olc(path, dis, ic, y0, y1, min_parlaklik=35, duzluk=10):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    ts = []
    for y in range(y0, y1):
        d = a[y, dis[0]:dis[1]].mean(axis=1)
        i = a[y, ic[0]:ic[1]].mean(axis=1)
        if d.max() > 248 or d.std() > duzluk:      # doygun ya da düz değil
            continue
        dm = float(np.median(d))
        if dm < min_parlaklik:                     # arka plan çok karanlık
            continue
        ts.append(float(np.percentile(i, 10)) / dm)
    if not ts:
        return None
    t = np.array(ts)
    return len(t), float(np.median(t)), float(np.percentile(t, 25)), float(np.percentile(t, 75))

def main(argv):
    if len(argv) < 3:
        print(__doc__); return 1
    if argv[2] == "--profil":
        profil(argv[1], *map(int, argv[3:7])); return 0
    v = list(map(int, argv[2:8]))
    r = olc(argv[1], (v[0], v[1]), (v[2], v[3]), v[4], v[5])
    if r is None:
        print("Ölçülemedi: uygun satır yok (arka plan çok karanlık ya da düz değil)."); return 1
    n, m, q1, q3 = r
    print("örnek satır : %d" % n)
    print("geçirgenlik : t = %.4f   (çeyrekler %.4f – %.4f)" % (m, q1, q3))
    print("ZEMİN ALFASI: %.3f" % (1 - m))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
