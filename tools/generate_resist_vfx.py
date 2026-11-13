#!/usr/bin/env python3
"""Resist buff efektinin dokularini uretir (ozgun, prosedurel).

Cikti: unity/Assets/Resources/VFX/ResistBuff/*.png

Dokular GRI TONLAMALIDIR: parlaklik = yogunluk. Renk Unity tarafinda
(ResistBuffEffect.cs + KorayAdditive.shader) verilir; boylece ayni dort doku
ates / buz / simsek / zehir direnclerinin hepsinde kullanilir.

Gerekli: pip install pillow numpy
Kullanim: python3 tools/generate_resist_vfx.py
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "unity", "Assets", "Resources", "VFX", "ResistBuff")
SS = 4  # supersample carpani


def _glow(img, radii_weights):
    """Keskin cizime yumusak hale ekler (additive)."""
    base = np.asarray(img, dtype=np.float32)
    acc = base.copy()
    for radius, weight in radii_weights:
        acc += np.asarray(img.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32) * weight
    return acc


def _finish(arr, size, name, edge_fade=True):
    arr = np.clip(arr, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "L").resize((size, size), Image.LANCZOS)
    if edge_fade:
        # Kenarlarda tam siyah: clamp/tekrar dikisleri gorunmesin.
        a = np.asarray(img, dtype=np.float32)
        yy, xx = np.mgrid[0:size, 0:size]
        r = np.hypot(xx - (size - 1) / 2.0, yy - (size - 1) / 2.0) / (size / 2.0)
        a *= np.clip((1.0 - r) / 0.04, 0, 1)
        img = Image.fromarray(a.astype(np.uint8), "L")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, optimize=True)
    print("yazildi:", os.path.relpath(path, ROOT), img.size)


def _circle(d, c, r, width, fill=255):
    d.ellipse([c - r, c - r, c + r, c + r], outline=fill, width=width)


def _glyph(d, rng, cx, cy, s, angle, width):
    """3x3 izgarada rastgele cizgilerden olusan ozgun bir isaret."""
    pts = [(-1 + i, -1 + j) for i in range(3) for j in range(3)]
    ca, sa = math.cos(angle), math.sin(angle)

    def tr(p):
        x, y = p[0] * s * 0.5, p[1] * s * 0.72
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)

    p = rng.choice(pts)
    for _ in range(rng.randint(3, 5)):
        q = rng.choice([t for t in pts if t != p])
        d.line([tr(p), tr(q)], fill=255, width=width)
        p = q
    if rng.random() < 0.4:
        x, y = tr(rng.choice(pts))
        rr = s * 0.16
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=255, width=max(1, width - 1))


def rune_circle(size=512):
    n = size * SS
    c = n / 2.0
    R = n / 2.0 * 0.90
    img = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(img)
    rng = random.Random(41)
    w = SS * 2

    _circle(d, c, R, w * 2)
    _circle(d, c, R * 0.955, w)
    _circle(d, c, R * 0.76, w)
    _circle(d, c, R * 0.72, w * 2)
    _circle(d, c, R * 0.36, w)

    # rün bandi
    count = 26
    for i in range(count):
        a = 2 * math.pi * i / count
        rr = R * 0.857
        _glyph(d, rng, c + rr * math.cos(a), c + rr * math.sin(a), R * 0.085, a + math.pi / 2, w)

    # ic ice iki kare -> sekiz koseli yildiz
    for off in (0.0, math.pi / 4):
        pts = [(c + R * 0.72 * math.cos(off + k * math.pi / 2),
                c + R * 0.72 * math.sin(off + k * math.pi / 2)) for k in range(4)]
        d.line(pts + [pts[0]], fill=255, width=w)

    # yildiz koselerinde kucuk halkalar, merkezden cikan isinlar
    for k in range(8):
        a = k * math.pi / 4
        x, y = c + R * 0.72 * math.cos(a), c + R * 0.72 * math.sin(a)
        rr = R * 0.045
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=0, outline=255, width=w)
        a2 = a + math.pi / 8
        d.line([(c + R * 0.36 * math.cos(a2), c + R * 0.36 * math.sin(a2)),
                (c + R * 0.51 * math.cos(a2), c + R * 0.51 * math.sin(a2))], fill=255, width=w)

    # ic tik isaretleri
    for k in range(48):
        a = 2 * math.pi * k / 48
        r0, r1 = R * 0.36, R * (0.33 if k % 4 else 0.30)
        d.line([(c + r0 * math.cos(a), c + r0 * math.sin(a)),
                (c + r1 * math.cos(a), c + r1 * math.sin(a))], fill=255, width=SS)

    arr = _glow(img, [(SS * 2, 0.7), (SS * 7, 0.55), (SS * 18, 0.35)]) * 0.80
    _finish(arr, size, "rune_circle.png")


def hoop(size=256):
    """Ince halka; aci boyunca parlakligi degisir ki donus gorulsun."""
    n = size * SS
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    c = (n - 1) / 2.0
    dx, dy = xx - c, yy - c
    r = np.hypot(dx, dy) / (n / 2.0)
    ang = np.arctan2(dy, dx)
    d = np.abs(r - 0.86)
    core = np.exp(-(d / 0.012) ** 2)
    halo = np.exp(-(d / 0.055) ** 2) * 0.38
    streak = 0.45 + 0.55 * (0.5 + 0.5 * np.cos(ang * 2.0)) ** 2
    arr = (core + halo) * streak * 255.0
    _finish(arr, size, "hoop.png")


def glow(size=128):
    n = size
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    c = (n - 1) / 2.0
    r = np.hypot(xx - c, yy - c) / (n / 2.0)
    arr = np.clip(1.0 - r, 0, 1) ** 2.2 * 255.0
    _finish(arr, size, "glow.png", edge_fade=False)


def spark(size=64):
    n = size * SS
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    c = (n - 1) / 2.0
    x, y = (xx - c) / (n / 2.0), (yy - c) / (n / 2.0)
    r = np.hypot(x, y)
    dot = np.exp(-(r / 0.16) ** 2)
    rays = np.exp(-(np.abs(x) / 0.035) ** 2) * np.exp(-(np.abs(y) / 0.45) ** 2) \
         + np.exp(-(np.abs(y) / 0.035) ** 2) * np.exp(-(np.abs(x) / 0.45) ** 2)
    arr = (dot + rays * 0.7 + np.exp(-(r / 0.4) ** 2) * 0.18) * 255.0
    _finish(arr * np.clip((1.0 - r) / 0.2, 0, 1), size, "spark.png", edge_fade=False)


if __name__ == "__main__":
    rune_circle()
    hoop()
    glow()
    spark()
