#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ilerleme simulasyonu: icerigi "oynayarak" gercek degerler uretir.

NE YAPAR
--------
Istemci veya sunucu olmadan, content/*.json icerigini kullanarak bir oyuncunun
seviye 1'den 100'e yolculugunu simule eder ve sorulari SAYIYLA cevaplar:

  - Seviye 1 -> 100 kac saat surer?
  - Hangi seviyeler "duvar" (asiri uzun)?
  - Saatte kac altin kazanilir, iksir masrafi ne kadar?
  - Bir ekipman dusurmek icin kac mob oldurmek gerekir?
  - Siniflar birbirine gore ne kadar hizli?

NEDEN GEREKLI
-------------
balance_report.txt tek bir mobun dengesini gosterir (TTK/TTD). Ama oyunun
GERCEK sorunu birikimdedir: tek tek moblar dengeli gorunurken seviye egrisi
ile mob tecrubesi uyusmazsa oyun seviye 60'ta durur. Bunu ancak bastan sona
simule ederek gorursun.

KULLANIM
--------
  python3 tools/generate_content.py      # once icerik uretilmis olmali
  python3 tools/simulate_progression.py
"""

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# =============================================================================
#  OYUNCU DAVRANIS VARSAYIMLARI  --  simulasyonun girdileri
# =============================================================================

SKILL_DPS_BONUS = 1.35      # beceriler duz vurusun uzerine ne ekler
DOWNTIME_FRACTION = 0.30    # yurume, bekleme, iksir icme, envanter -- olu zaman
POTION_PER_KILL = 0.35      # mob basina ortalama kac sifa iksiri icilir
PARTY_SIZE = 1              # tek oyuncu varsayimi (parti bonusu yok)
MAX_LEVEL = 100

# Hedefler: bir seviyenin kac saatten uzun surmesi "duvar" sayilir
WALL_HOURS = 3.0
# Toplam 1->100 icin makul bant (klasik MMORPG temposu)
TOTAL_HOURS_TARGET = (80.0, 400.0)

# =============================================================================
#  SEVIYE EGRISI
# =============================================================================
#  exp_required(level) = EXP_COEF * level ^ EXP_EXPONENT
#  (o seviyeye ulasmak icin gereken TOPLAM tecrube)
#
#  Bu iki sayi tahmin degil: --calibrate modu ile hedef sureye gore
#  cozuldu. 01_core_schema.sql'deki level_curve seed'i bunlarla AYNI olmali.
#
#  Neden exponent 2.2 yanlisti: mob tecrubesi 12 + level^1.75 ile buyuyor.
#  Toplam egri A*L^p ise seviye basina gereken tecrube ~ A*p*L^(p-1).
#  Seviye basina oldurme sayisinin ARTMASI icin (p-1) > 1.75, yani p > 2.75
#  olmali. p=2.2'de tam tersi olur: seviyeler ilerledikce HIZLANIR.
EXP_COEF = 8.45
EXP_EXPONENT = 3.4


def exp_threshold(level, coef=None, exponent=None):
    c = EXP_COEF if coef is None else coef
    e = EXP_EXPONENT if exponent is None else exponent
    return int(c * (level ** e))


# =============================================================================
#  ICERIK YUKLEME
# =============================================================================

def load(name):
    path = CONTENT / f"{name}.json"
    if not path.exists():
        print(f"HATA: {path.relative_to(ROOT)} bulunamadi.")
        print("Once calistir: python3 tools/generate_content.py")
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def build_player_dps_table(items):
    """Her kademe icin ortalama silah DPS'i, sinif bazinda."""
    weapons = [i for i in items if i["category"] == "weapon"]
    tiers = sorted({w["req_level"] for w in weapons})

    by_tier = {}
    for t in tiers:
        ws = [w for w in weapons if w["req_level"] == t]
        by_tier[t] = sum(w["stats"]["dps"] for w in ws) / len(ws)

    # Sinif bazinda: o sinifin kusanabildigi silahlarin ortalamasi
    by_class_tier = {}
    for w in weapons:
        for c in w.get("_classes", []):
            by_class_tier.setdefault(c, {}).setdefault(w["req_level"], []).append(
                w["stats"]["dps"])
    for c in by_class_tier:
        by_class_tier[c] = {t: sum(v) / len(v) for t, v in by_class_tier[c].items()}

    return tiers, by_tier, by_class_tier


def interp_dps(level, tiers, by_tier):
    """Kademeler arasi dogrusal gecisle o seviyedeki beklenen DPS."""
    if level <= tiers[0]:
        base = by_tier[tiers[0]]
    elif level >= tiers[-1]:
        base = by_tier[tiers[-1]] * (1 + (level - tiers[-1]) * 0.012)
    else:
        base = by_tier[tiers[0]]
        for a, b in zip(tiers, tiers[1:]):
            if a <= level < b:
                f = (level - a) / (b - a)
                base = by_tier[a] * (1 - f) + by_tier[b] * f
                break
    return base * SKILL_DPS_BONUS


def pick_mob(level, mobs):
    """O seviyede avlanacak en verimli mob: tecrube/saniye en yuksek olan."""
    # Oyuncu kendi seviyesine +-5 bandindaki moblari avlar
    candidates = [m for m in mobs
                  if m["npc_kind"] == "monster" and abs(m["level"] - level) <= 5]
    if not candidates:
        # Bant disindaysa en yakin seviyeli moba dus
        candidates = [m for m in mobs if m["npc_kind"] == "monster"]
        candidates.sort(key=lambda m: abs(m["level"] - level))
        candidates = candidates[:3]
    return candidates


# =============================================================================
#  SIMULASYON
# =============================================================================

def simulate(items, mobs, loot, coef=None, exponent=None):
    tiers, by_tier, by_class_tier = build_player_dps_table(items)

    # Iksir fiyati: seviyeye uygun sifa iksiri
    potions = [i for i in items if i["category"] == "consumable"
               and i["stats"].get("effect") == "heal_hp"]

    rows = []
    total_hours = 0.0
    total_gold = 0.0
    total_potion_cost = 0.0
    total_kills = 0

    for level in range(1, MAX_LEVEL):
        need = exp_threshold(level + 1, coef, exponent) - exp_threshold(level, coef, exponent)
        pdps = interp_dps(level, tiers, by_tier)

        candidates = pick_mob(level, mobs)
        # En verimli mobu sec: tecrube / oldurme suresi
        best = None
        for m in candidates:
            ttk = m["max_hp"] / pdps
            eps = m["exp_reward"] / ttk            # tecrube/saniye
            if best is None or eps > best[1]:
                best = (m, eps, ttk)
        mob, eps, ttk = best

        kills = need / mob["exp_reward"]
        combat_sec = kills * ttk
        wall_sec = combat_sec / (1 - DOWNTIME_FRACTION)
        hours = wall_sec / 3600.0

        gold = kills * (mob["gold_min"] + mob["gold_max"]) / 2.0
        pot = min(potions, key=lambda p: abs(p["req_level"] - level))
        pot_cost = kills * POTION_PER_KILL * pot["buy_price"]

        total_hours += hours
        total_gold += gold
        total_potion_cost += pot_cost
        total_kills += kills

        rows.append({
            "level": level,
            "need_exp": need,
            "mob": mob["display_name"],
            "mob_level": mob["level"],
            "mob_exp": mob["exp_reward"],
            "ttk": ttk,
            "kills": kills,
            "hours": hours,
            "cum_hours": total_hours,
            "gold": gold,
            "potion_cost": pot_cost,
            "net_gold": gold - pot_cost,
        })

    return rows, by_class_tier, tiers, by_tier, total_kills


def loot_expectation(mobs, loot, items):
    """Bir ekipman dusurmek icin kac mob gerekir?"""
    by_mob = {}
    for l in loot:
        by_mob.setdefault(l["npc_id"], []).append(l)

    out = []
    item_by_id = {i["id"]: i for i in items}
    for m in sorted([m for m in mobs if m["npc_kind"] == "monster"],
                    key=lambda x: x["level"]):
        entries = by_mob.get(m["id"], [])
        gear = [e for e in entries if e["group"] == 1]
        if not gear:
            continue
        # Grup 1'den en fazla 1 esya duser -> oranlar toplanir
        p = min(1.0, sum(e["ppm"] for e in gear) / 1_000_000)
        if p <= 0:
            continue
        out.append((m["level"], m["display_name"], p, 1.0 / p))
    return out


# =============================================================================
#  RAPOR
# =============================================================================

def main():
    items = load("items")
    mobs = load("npcs")
    loot = load("loot")

    rows, by_class_tier, tiers, by_tier, total_kills = simulate(items, mobs, loot)

    print("ILERLEME SIMULASYONU")
    print("=" * 78)
    print()
    print("Varsayimlar:")
    print(f"  beceri DPS katkisi   : x{SKILL_DPS_BONUS}")
    print(f"  olu zaman orani      : %{DOWNTIME_FRACTION*100:.0f} (yurume, bekleme, envanter)")
    print(f"  mob basina iksir     : {POTION_PER_KILL}")
    print(f"  parti buyuklugu      : {PARTY_SIZE} (tek oyuncu)")
    print()

    # --- Seviye tablosu (orneklenmis) ---
    print("Seviye tablosu (her 10 seviyede bir ornek):")
    print("  sv  gereken exp  mob (sv)                  TTK   oldurme   sure   toplam")
    for r in rows:
        if r["level"] % 10 == 0 or r["level"] in (1, 5, MAX_LEVEL - 1):
            print(f"  {r['level']:>3}  {r['need_exp']:>11,}  "
                  f"{r['mob'][:18]:<18} ({r['mob_level']:>2})  "
                  f"{r['ttk']:>5.1f}s  {r['kills']:>7.0f}  "
                  f"{r['hours']:>5.2f}sa  {r['cum_hours']:>6.1f}sa")
    print()

    total_hours = rows[-1]["cum_hours"]
    lo, hi = TOTAL_HOURS_TARGET
    verdict = "ok" if lo <= total_hours <= hi else ("COK KISA" if total_hours < lo else "COK UZUN")
    print(f"TOPLAM 1 -> {MAX_LEVEL}: {total_hours:.1f} saat  "
          f"(hedef bant {lo:.0f}-{hi:.0f} saat)  -> {verdict}")
    print(f"  toplam oldurulen mob : {total_kills:,.0f}")
    print()

    # --- Duvar tespiti ---
    walls = [r for r in rows if r["hours"] > WALL_HOURS]
    print(f"Duvar kontrolu (bir seviye > {WALL_HOURS} saat):")
    if not walls:
        en_uzun = max(rows, key=lambda r: r["hours"])
        print(f"  duvar yok. En uzun seviye: {en_uzun['level']} "
              f"({en_uzun['hours']:.2f} saat)")
    else:
        for r in walls[:12]:
            print(f"  sv {r['level']:>3}  {r['hours']:>6.2f} saat  "
                  f"{r['kills']:>7.0f} mob  ({r['mob']})")
        if len(walls) > 12:
            print(f"  ... ve {len(walls)-12} seviye daha")
        print(f"  TOPLAM {len(walls)} duvar seviyesi -> seviye egrisi veya mob "
              f"tecrubesi ayarlanmali")
    print()

    # --- Tempo tutarliligi: seviye basina sure artisi ---
    print("Tempo (seviye basina sure, 10'luk bantlarda ortalama):")
    for start in range(1, MAX_LEVEL, 10):
        band = [r for r in rows if start <= r["level"] < start + 10]
        if not band:
            continue
        avg = sum(r["hours"] for r in band) / len(band)
        bar = "#" * min(40, int(avg * 12))
        print(f"  sv {start:>3}-{min(start+9, MAX_LEVEL-1):<3} {avg:>5.2f} sa/sv  {bar}")
    print()

    # --- Ekonomi ---
    gross = sum(r["gold"] for r in rows)
    cost = sum(r["potion_cost"] for r in rows)
    print("Ekonomi (1 -> 100 boyunca):")
    print(f"  brut altin gelir     : {gross:>14,.0f}")
    print(f"  iksir masrafi        : {cost:>14,.0f}  (%{cost/gross*100:.0f})")
    print(f"  net altin            : {gross-cost:>14,.0f}")
    print(f"  saatlik net altin    : {(gross-cost)/total_hours:>14,.0f}/sa")
    print()
    # En pahali ekipman alinabilir mi?
    priciest = max((i for i in items if i["category"] in ("weapon", "armor", "accessory")),
                   key=lambda i: i["buy_price"])
    print(f"  en pahali ekipman    : {priciest['display_name']} "
          f"({priciest['buy_price']:,} altin)")
    hours_for_it = priciest["buy_price"] / ((gross - cost) / total_hours)
    print(f"  onu almak icin       : {hours_for_it:.1f} saat farm")
    print()

    # --- Loot beklentisi ---
    print("Ekipman dusme beklentisi (grup 1, en fazla 1 esya):")
    print("  sv   mob                     oran     ortalama kac mob")
    for level, name, p, n in loot_expectation(mobs, loot, items)[:10]:
        print(f"  {level:>3}  {name[:22]:<22}  %{p*100:>5.2f}  {n:>10.0f}")
    print()

    # --- Sinif karsilastirmasi ---
    print("Sinif silah DPS'i (kademe bazinda):")
    classes = sorted(by_class_tier.keys())
    header = "  kademe  " + "".join(f"{c[:9]:>11}" for c in classes)
    print(header)
    for t in tiers:
        line = f"  sv {t:>3}   "
        for c in classes:
            v = by_class_tier[c].get(t)
            line += f"{v:>11.1f}" if v else f"{'-':>11}"
        print(line)
    print()
    # En hizli / en yavas sinif farki
    for t in tiers:
        vals = [by_class_tier[c].get(t) for c in classes if by_class_tier[c].get(t)]
        if len(vals) > 1:
            spread = max(vals) / min(vals) - 1
            flag = "  <-- DENGESIZ" if spread > 0.60 else ""
            print(f"  sv {t:>3} siniflar arasi fark: %{spread*100:.0f}{flag}")


# =============================================================================
#  KALIBRASYON
# =============================================================================

def total_hours_for(items, mobs, loot, coef, exponent):
    rows, _, _, _, _ = simulate(items, mobs, loot, coef, exponent)
    return rows[-1]["cum_hours"], rows


def calibrate(items, mobs, loot,
              target_hours=150.0,
              early_hours_max=1.5,
              exponents=(2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0)):
    """Hedef sureye ve dogru tempoya uyan (coef, exponent) ciftini bulur.

    Her exponent icin katsayiyi hedef toplam sureye gore olcekler
    (sure katsayiyla dogrusal oldugu icin tek adimda cozulur), sonra
    iki kriteri kontrol eder:
      1. Ilk 10 seviye early_hours_max'tan kisa olmali (yeni oyuncu sikilmasin)
      2. Sure/seviye ARTAN olmali (gec seviyeler daha uzun sursun)
    """
    print("KALIBRASYON")
    print("=" * 78)
    print(f"Hedef: toplam {target_hours:.0f} saat, ilk 10 seviye < {early_hours_max} saat,")
    print("       sure/seviye artan olmali")
    print()
    print("  exponent   katsayi    toplam   sv1-10   tempo        durum")

    results = []
    for e in exponents:
        # Sure katsayiyla dogrusal: once 100 ile dene, sonra olcekle
        h0, _ = total_hours_for(items, mobs, loot, 100.0, e)
        if h0 <= 0:
            continue
        coef = 100.0 * (target_hours / h0)
        hours, rows = total_hours_for(items, mobs, loot, coef, e)

        early = sum(r["hours"] for r in rows if r["level"] <= 10)

        # Tempo: 10'luk bant ortalamalari artan mi?
        bands = []
        for start in range(1, MAX_LEVEL, 10):
            band = [r for r in rows if start <= r["level"] < start + 10]
            if band:
                bands.append(sum(r["hours"] for r in band) / len(band))
        rising = all(b2 >= b1 * 0.95 for b1, b2 in zip(bands, bands[1:]))
        ratio = bands[-1] / bands[0] if bands[0] > 0 else 0

        ok = early <= early_hours_max and rising
        results.append((e, coef, hours, early, ratio, rising, ok))
        print(f"  {e:>8.1f}  {coef:>9.2f}  {hours:>7.1f}sa  {early:>5.2f}sa  "
              f"son/ilk x{ratio:>5.1f}  {'ARTAN' if rising else 'DUSEN'}  "
              f"{'ok' if ok else '-'}")

    print()
    good = [r for r in results if r[6]]
    if not good:
        print("  Hicbir exponent iki kriteri birlikte saglamadi.")
        print("  Mob tecrube formulunu (generate_content.py) da ayarlamak gerekebilir.")
        return None

    # Kriterleri saglayanlardan tempoyu en dengeli olani sec (son/ilk orani
    # cok asiri olmasin -- gec seviyeler 20 kat uzun surerse oyuncu birakir)
    best = min(good, key=lambda r: abs(r[4] - 6.0))
    print(f"  SECILEN: exponent {best[0]:.1f}, katsayi {best[1]:.0f}")
    print(f"           toplam {best[2]:.1f} saat, ilk 10 seviye {best[3]:.2f} saat,")
    print(f"           son bant ilk bandin {best[4]:.1f} kati")
    print()
    print("  SQL'e yaz (01_core_schema.sql level_curve seed'i):")
    print(f"    ({best[1]:.2f} * power(lvl, {best[0]:.1f}))::bigint")
    print(f"  Ve bu dosyadaki EXP_COEF / EXP_EXPONENT degerlerini ayni yap.")
    return best


if __name__ == "__main__":
    if "--calibrate" in sys.argv:
        def arg(flag, default):
            return float(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default
        calibrate(load("items"), load("npcs"), load("loot"),
                  target_hours=arg("--hours", 150.0),
                  early_hours_max=arg("--early", 1.5))
    else:
        main()
