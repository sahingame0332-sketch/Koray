#!/usr/bin/env python3
"""Bir veya daha fazla onizlemeyi orijinal ekran goruntusuyle karsilastirir.

Olcut: her yazi bolgesinde, orijinalin acik renkli yazi pikselleri ile onizlemeninkiler
arasindaki ortusme orani (IoU). Bolge +-6 px kaydirilarak en iyi hizalama aranir, boylece
1-2 piksellik konum farki fontun sekil benzerligini maskelemez. 1.0 = birebir.

Kullanim:
  python3 olc.py ORIJINAL.jpg ONIZLEME1.png [ONIZLEME2.png ...]
"""
import json, sys, pathlib
import numpy as np
from PIL import Image

ESIK, KAYMA = 150, 6

def yukle(p):
    return np.asarray(Image.open(p).convert("L")).astype(np.int16)

def iou(orig, img, kutu):
    x0, y0, x1, y1 = kutu
    hedef = orig[y0:y1, x0:x1] > ESIK
    en_iyi = 0.0
    for dy in range(-KAYMA, KAYMA + 1):
        for dx in range(-KAYMA, KAYMA + 1):
            m = img[y0 + dy:y1 + dy, x0 + dx:x1 + dx] > ESIK
            if m.shape != hedef.shape:
                continue
            birlesim = np.logical_or(hedef, m).sum()
            if birlesim:
                en_iyi = max(en_iyi, np.logical_and(hedef, m).sum() / birlesim)
    return en_iyi

def main(argv):
    if len(argv) < 3:
        print(__doc__); return 1
    orig = yukle(argv[1])
    adlar = [pathlib.Path(p).name for p in argv[2:]]
    imgs = [yukle(p) for p in argv[2:]]
    bolgeler = json.loads((pathlib.Path(__file__).parent / "bolgeler.json").read_text())["bolgeler"]

    print("%-20s" % "bölge" + "".join("%12s" % a[:11] for a in adlar))
    print("-" * (20 + 12 * len(adlar)))
    toplam = [[] for _ in imgs]
    gruplar = {}
    for ad, b in bolgeler.items():
        satir = "%-20s" % ad[:20]
        for i, im in enumerate(imgs):
            v = iou(orig, im, b["kutu"])
            toplam[i].append(v)
            gruplar.setdefault(b["grup"], [[] for _ in imgs])[i].append(v)
            satir += "%12.3f" % v
        print(satir)
    print("-" * (20 + 12 * len(adlar)))
    print("%-20s" % "ORTALAMA" + "".join("%12.3f" % np.mean(t) for t in toplam))
    print("\nGrup ortalamalari:")
    for g, vs in sorted(gruplar.items()):
        print("  %-8s" % g + "".join("%12.3f" % np.mean(v) for v in vs))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
