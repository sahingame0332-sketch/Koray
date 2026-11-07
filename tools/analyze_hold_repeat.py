#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stat dagitim butonu icin basili-tutma tekrarlama egrisi analizi.

PROBLEM
-------
Oyuncu "+" butonuna basili tuttugunda puanlar tekrar tekrar eklenir. Bu hiz
yanlis ayarlanirsa iki ayri sikayet dogar:

  - cok yavas  -> seviye 100'de ~297 puani dagitmak dakikalar surer
  - cok hizli  -> oyuncu tek puan eklemek isterken 5 puan ekler, geri alamaz

Dogru hiz bir tercih degil, HESAPLANABILIR bir seydir: oyuncunun elindeki
puan sayisi dagilimini biliyoruz (level_curve: seviye basina 3 puan), hedef
sureleri de tanimlayabiliriz. Bu betik egriyi simule eder ve hedeflere
uyup uymadigini soyler.

MODEL
-----
  t = 0      : parmak degdi -> ANINDA 1 puan eklenir (tek dokunus hassasiyeti)
  t < INITIAL_DELAY        : tekrar YOK (yanlislikla tekrar baslamasin)
  t >= INITIAL_DELAY       : her tick'te STEP kadar puan eklenir
                             tick hizi  : TICK_RATE_START -> TICK_RATE_MAX
                             adim boyu  : STEP_THRESHOLDS esiklerine gore buyur

Adim boyunun buyumesi kritik: tick hizini 60/sn'ye cikarmak yerine adimi
buyutmek hem kare hizindan bagimsiz olur hem de sayac okunabilir kalir.

KULLANIM
--------
  python3 tools/analyze_hold_repeat.py
"""

import math

# =============================================================================
#  AYARLAR  --  Unity tarafindaki StatRepeatTuning varsayilanlariyla AYNI olmali
# =============================================================================

INITIAL_DELAY = 0.35        # sn: basili tutmanin tekrarı baslatmasi icin gereken sure
TICK_RATE_START = 8.0       # tick/sn: tekrar basladigindaki hiz
TICK_RATE_MAX = 20.0        # tick/sn: ulasilabilecek en yuksek hiz
RATE_RAMP_TIME = 1.20       # sn: start -> max hizlanma suresi
RATE_RAMP_EXP = 1.60        # hizlanma egrisi (1 = dogrusal, >1 = basta yavas)

# (basili tutma suresi esigi, o esikten sonraki adim boyu)
STEP_THRESHOLDS = [
    (0.00, 1),
    (1.20, 2),
    (2.20, 5),
    (3.40, 10),
    (5.00, 25),
]

# Hedefler: (puan_sayisi, en_fazla_saniye, aciklama)
TARGETS = [
    (1,   0.00, "tek dokunus: aninda, tekrar beklemeden"),
    (3,   0.80, "bir seviye atlama (3 puan): hizli ama kontrollu"),
    (15,  2.20, "5 seviye birikmis"),
    (30,  3.20, "10 seviye birikmis"),
    (60,  4.60, "20 seviye birikmis"),
    (150, 6.50, "50 seviye birikmis"),
    (297, 8.00, "seviye 1->100 hic dagitilmamis (en kotu durum)"),
]

SIM_DT = 0.001              # sn: simulasyon adimi


# =============================================================================
#  SIMULASYON
# =============================================================================

def tick_rate(hold_time):
    """Basili tutma suresine gore o anki tick hizi (tick/sn)."""
    t = hold_time - INITIAL_DELAY
    if t <= 0:
        return TICK_RATE_START
    f = min(1.0, t / RATE_RAMP_TIME) ** RATE_RAMP_EXP
    return TICK_RATE_START + (TICK_RATE_MAX - TICK_RATE_START) * f


def step_size(hold_time):
    """Basili tutma suresine gore tick basina eklenecek puan."""
    step = STEP_THRESHOLDS[0][1]
    for threshold, s in STEP_THRESHOLDS:
        if hold_time >= threshold:
            step = s
    return step


def simulate(points, max_seconds=40.0):
    """points kadar puanin tamaminin dagitilmasi kac saniye surer?

    Unity tarafindaki mantigin birebir aynisi: ilk puan dokunusta,
    sonrakiler INITIAL_DELAY sonrasi tick'lerle.

    Dondurur: (sure, tick_sayisi, tick_kayitlari)
    """
    if points <= 0:
        return 0.0, 0, []

    remaining = points - 1          # ilk puan dokunus aninda verildi
    if remaining == 0:
        return 0.0, 1, [(0.0, 1, points - 1)]

    t = 0.0
    next_tick = INITIAL_DELAY
    ticks = 1
    log = [(0.0, 1, remaining)]
    last_fire = 0.0

    while remaining > 0 and t < max_seconds:
        t += SIM_DT
        if t >= next_tick:
            # Adim ve hiz, tick'in PLANLANAN anina gore hesaplanir (next_tick),
            # gerceklesen anina (t) gore degil. Unity tarafindaki
            # HoldRepeatButton.Update ile birebir ayni model -- boylece bu
            # analizin sonuclari oyunda da gecerli olur ve kare hizindan
            # bagimsiz kalir.
            step = min(step_size(next_tick), remaining)
            remaining -= step
            ticks += 1
            log.append((next_tick, step, remaining))
            next_tick += 1.0 / tick_rate(next_tick)

    # Sure, SON TICK'in planlanan ani olarak raporlanir (simulasyon adiminin
    # yuvarlama hatasini tasimasin) -- Unity kosumu da ayni seyi olcer.
    return (log[-1][0] if log else 0.0), ticks, log


# =============================================================================
#  RAPOR
# =============================================================================

def main():
    print("BASILI-TUTMA TEKRARLAMA EGRISI ANALIZI")
    print("=" * 72)
    print()
    print("Ayarlar:")
    print(f"  ilk gecikme        : {INITIAL_DELAY:.2f} sn")
    print(f"  tick hizi          : {TICK_RATE_START:.0f} -> {TICK_RATE_MAX:.0f} tick/sn "
          f"({RATE_RAMP_TIME:.2f} sn'de, egri exp {RATE_RAMP_EXP})")
    print(f"  adim esikleri      : " + ", ".join(
        f"{th:.2f}sn->{s}" for th, s in STEP_THRESHOLDS))
    print()

    # --- Hiz egrisi ---
    print("Zaman icinde etkin hiz (puan/sn):")
    print("  sure(sn)  tick/sn  adim  puan/sn")
    for t in [0.35, 0.60, 1.00, 1.20, 1.60, 2.20, 2.60, 3.40, 4.00, 5.00, 6.00]:
        r = tick_rate(t)
        s = step_size(t)
        print(f"  {t:>7.2f}  {r:>7.1f}  {s:>4}  {r*s:>7.1f}")
    print()

    # --- Hedef kontrolu ---
    print("Hedef kontrolu:")
    print("  puan    sure     hedef   tick   durum   aciklama")
    all_ok = True
    for points, limit, note in TARGETS:
        dur, ticks, _ = simulate(points)
        ok = dur <= limit + 1e-9
        all_ok = all_ok and ok
        print(f"  {points:>4}  {dur:>6.2f}sn  {limit:>5.2f}sn  {ticks:>5}   "
              f"{'ok   ' if ok else 'SORUN'}   {note}")
    print()
    print(f"  SONUC: {'butun hedefler saglandi' if all_ok else 'HEDEF IHLALI VAR'}")
    print()

    # --- En kotu durum ayrintisi ---
    print("En kotu durum (297 puan) tick dokumu -- ilk 12 ve son 3 tick:")
    _, _, log = simulate(297)
    for i, (t, step, rem) in enumerate(log):
        if i < 12 or i >= len(log) - 3:
            print(f"  t={t:>5.2f}sn  +{step:>3}  kalan {rem:>4}")
        elif i == 12:
            print(f"  ... ({len(log) - 15} tick atlandi) ...")
    print()

    # --- Yanlislikla fazla ekleme riski ---
    # --- Olu ayar kontrolu: hangi adim esiklerine gercekten ulasiliyor? ---
    worst_points = max(p for p, _, _ in TARGETS)
    worst_dur, _, _ = simulate(worst_points)
    print("Adim esigi ulasilabilirlik kontrolu:")
    print(f"  En kotu durum ({worst_points} puan) {worst_dur:.2f} sn'de bitiyor.")
    for threshold, step in STEP_THRESHOLDS:
        if threshold == 0.0:
            print(f"  {threshold:>5.2f} sn -> adim {step:<3} ulasiliyor (baslangic)")
        elif threshold < worst_dur:
            print(f"  {threshold:>5.2f} sn -> adim {step:<3} ulasiliyor")
        else:
            print(f"  {threshold:>5.2f} sn -> adim {step:<3} ULASILMIYOR -- olu ayar,")
            print(f"           yalnizca puan sayisi ileride artarsa devreye girer")
    print()

    print("Hassasiyet kontrolu (oyuncu tek puan isterken ne eklenir?):")
    for hold in [0.05, 0.15, 0.30, 0.34, 0.40, 0.50]:
        # hold suresince basili tutulursa kac puan eklenir
        added = 1
        t = 0.0
        next_tick = INITIAL_DELAY
        while t < hold:
            t += SIM_DT
            if t >= next_tick:
                added += step_size(next_tick)
                next_tick += 1.0 / tick_rate(next_tick)
        flag = "" if added <= 2 else "  <-- fazla"
        print(f"  {hold*1000:>4.0f} ms basili tutma -> {added} puan{flag}")
    print()
    print("Not: INITIAL_DELAY 0.35 sn, insan ortalama dokunus suresinin")
    print("(~100-150 ms) belirgin ustunde; kazara tekrar baslamaz.")


if __name__ == "__main__":
    main()
