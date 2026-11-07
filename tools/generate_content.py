#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oyun icerigi ureteci (characters / items / skills / mobs / zones / loot).

NEDEN BETIK, NEDEN ELLE YAZILMIS JSON DEGIL?
--------------------------------------------
Bir MMORPG'nin icerigi yuzlerce satirdir ve hepsi birbirine bagli: bir item
kademesinin hasari degisirse o kademeyi dusuren moblarin HP'si de degismeli.
Elle yazilan veride bu baglar kopar. Burada icerik, en ustteki TASARIM
PARAMETRELERINDEN formullerle uretilir -- tek bir sayiyi degistirip butun
dengeyi yeniden uretebilirsin.

CIKTILAR
--------
  content/*.json                  -> insan tarafindan okunabilir, git diff'i anlamli
  docs/schema/02_content_seed.sql -> 01_core_schema.sql uzerine yuklenecek SQL

KULLANIM
--------
  python3 tools/generate_content.py
  psql -d oyun -f docs/schema/01_core_schema.sql
  psql -d oyun -f docs/schema/02_content_seed.sql

TELIF NOTU
----------
Buradaki butun isimler, sayilar ve dengeleme bu proje icin ozgun uretildi.
Hicbir ticari oyundan kopyalanmadi. Uretilen icerik senin eserindir.
"""

import json
import math
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SCHEMA = ROOT / "docs" / "schema"

# =============================================================================
#  TASARIM PARAMETRELERI  --  dengelemeyi burada yap
# =============================================================================

MAX_LEVEL = 100

# Kademe (tier) tanimlari: her kademe bir oyun asamasi
TIERS = [
    # kod,        ad,            min_lvl, guc_carpani, fiyat_carpani
    ("baslangic", "Başlangıç",         1,  1.00,    1),
    ("demir",     "Demir",            10,  1.80,    6),
    ("celik",     "Çelik",            20,  3.20,   28),
    ("gumus",     "Gümüş",            35,  5.60,  120),
    ("obsidyen",  "Obsidyen",         50,  9.50,  520),
    ("ejder",     "Ejder",            70, 16.00, 2400),
]

# Silah arketipleri: taban hasar, vurus araligi (sn), menzil (m), hangi statla olcekler
WEAPONS = [
    # kod,    ad,          slot,        taban_hasar, gecikme, menzil, stat,        siniflar
    ("kilic",  "Kılıç",     "main_hand",  34, 1.30,  2.0, "strength", ["warrior"]),
    ("balta",  "Balta",     "main_hand",  44, 1.75,  2.0, "strength", ["warrior"]),
    ("topuz",  "Topuz",     "main_hand",  38, 1.50,  2.0, "strength", ["warrior", "priest"]),
    ("hancer", "Hançer",    "main_hand",  22, 0.85,  1.6, "dexterity", ["rogue"]),
    ("yay",    "Yay",       "main_hand",  30, 1.45, 14.0, "dexterity", ["rogue"]),
    ("asa",    "Asa",       "main_hand",  26, 1.60,  3.0, "intellect", ["mage", "priest"]),
]

# Zirh arketipleri: slot basina koruma payi (toplam = 1.0)
ARMOR_SLOTS = [
    ("baslik",  "Başlık",  "head",  0.16),
    ("zirh",    "Zırh",    "chest", 0.34),
    ("pantolon","Pantolon","legs",  0.24),
    ("eldiven", "Eldiven", "hands", 0.12),
    ("bot",     "Bot",     "feet",  0.14),
]

# Zirh aileleri: taban koruma, hangi sinif, hangi stat bonusu
ARMOR_FAMILIES = [
    ("plaka", "Plaka", 100, ["warrior"],           "stamina"),
    ("deri",  "Deri",   62, ["rogue"],             "dexterity"),
    ("kumas", "Kumaş",  40, ["mage", "priest"],    "intellect"),
]

# Sinif tanimlari (01_core_schema.sql'deki sira ile ayni olmali)
CLASSES = [
    (1, "warrior", "Savaşçı",   "strength"),
    (2, "rogue",   "Suikastçı", "dexterity"),
    (3, "mage",    "Büyücü",    "intellect"),
    (4, "priest",  "Şifacı",    "intellect"),
]
CLASS_BY_CODE = {c[1]: c[0] for c in CLASSES}

# Beceri sablonlari: her sinif icin (kod, ad, tur, hedef, taban_guc, mp, bekleme_ms, menzil, seviye)
SKILLS = {
    "warrior": [
        ("sert_vurus",   "Sert Vuruş",      "damage", "single_enemy", 1.35,  12,  4000,  2.0,  2),
        ("kalkan_duvari","Kalkan Duvarı",   "buff",   "self",         0.00,  20, 30000,  0.0,  8),
        ("yarma",        "Yarma",           "damage", "area_enemy",   1.10,  28, 10000,  3.5, 14),
        ("meydan_okuma", "Meydan Okuma",    "taunt",  "single_enemy", 0.00,  15,  8000,  8.0, 20),
        ("kan_cigligi",  "Kan Çığlığı",     "buff",   "party",        0.00,  35, 60000,  0.0, 28),
        ("zirh_kirici",  "Zırh Kırıcı",     "debuff", "single_enemy", 1.05,  30, 15000,  2.0, 36),
        ("son_duran",    "Son Duran",       "buff",   "self",         0.00,  50,120000,  0.0, 45),
        ("girdap",       "Girdap",          "damage", "area_enemy",   1.55,  55, 18000,  4.0, 55),
        ("infaz",        "İnfaz",           "execute","single_enemy", 2.80,  60, 25000,  2.0, 68),
        ("savas_tanrisi","Savaş Tanrısı",   "buff",   "self",         0.00, 100,300000,  0.0, 82),
    ],
    "rogue": [
        ("hizli_kesik",  "Hızlı Kesik",     "damage", "single_enemy", 1.20,  10,  3000,  1.6,  2),
        ("golge_adim",   "Gölge Adım",      "mobility","self",        0.00,  18, 12000,  0.0,  8),
        ("zehirli_bicak","Zehirli Bıçak",   "dot",    "single_enemy", 0.70,  22,  9000,  1.6, 14),
        ("sirt_hancer",  "Sırttan Hançer",  "damage", "single_enemy", 2.10,  30, 14000,  1.6, 20),
        ("tuzak",        "Tuzak",           "control","area_enemy",   0.40,  26, 20000,  6.0, 28),
        ("ok_yagmuru",   "Ok Yağmuru",      "damage", "area_enemy",   1.30,  40, 16000, 16.0, 36),
        ("gizlenme",     "Gizlenme",        "stealth","self",         0.00,  45, 45000,  0.0, 45),
        ("olumcul_isabet","Ölümcül İsabet", "damage", "single_enemy", 2.60,  50, 22000, 14.0, 55),
        ("bicak_firtinasi","Bıçak Fırtınası","damage","area_enemy",   1.80,  60, 24000,  3.0, 68),
        ("suikast",      "Suikast",         "execute","single_enemy", 3.40,  90,180000,  1.6, 82),
    ],
    "mage": [
        ("ates_oku",     "Ateş Oku",        "damage", "single_enemy", 1.45,  14,  2500, 18.0,  2),
        ("buz_zinciri",  "Buz Zinciri",     "control","single_enemy", 0.60,  20, 14000, 16.0,  8),
        ("alev_halkasi", "Alev Halkası",    "damage", "area_enemy",   1.25,  34, 11000, 14.0, 14),
        ("mana_kalkani", "Mana Kalkanı",    "buff",   "self",         0.00,  28, 35000,  0.0, 20),
        ("yildirim",     "Yıldırım",        "damage", "single_enemy", 2.00,  42,  9000, 20.0, 28),
        ("donma",        "Donma",           "control","area_enemy",   0.50,  48, 25000, 14.0, 36),
        ("isinlanma",    "Işınlanma",       "mobility","self",        0.00,  40, 30000,  0.0, 45),
        ("meteor",       "Meteor",          "damage", "area_enemy",   2.40,  70, 28000, 22.0, 55),
        ("zaman_yarigi", "Zaman Yarığı",    "debuff", "area_enemy",   0.80,  65, 40000, 18.0, 68),
        ("kiyamet",      "Kıyamet",         "damage", "area_enemy",   3.60, 130,240000, 24.0, 82),
    ],
    "priest": [
        ("kutsal_isik",  "Kutsal Işık",     "heal",   "single_ally",  1.40,  16,  2000, 16.0,  2),
        ("koruma",       "Koruma",          "buff",   "single_ally",  0.00,  22, 25000, 16.0,  8),
        ("arindirma",    "Arındırma",       "cleanse","single_ally",  0.00,  18,  8000, 16.0, 14),
        ("ceza",         "Ceza",            "damage", "single_enemy", 1.15,  24,  6000, 14.0, 20),
        ("toplu_sifa",   "Toplu Şifa",      "heal",   "party",        1.00,  55, 15000, 12.0, 28),
        ("lanet",        "Lanet",           "debuff", "single_enemy", 0.70,  30, 18000, 14.0, 36),
        ("dirilis",      "Diriliş",         "revive", "single_ally",  0.00,  80,300000,  8.0, 45),
        ("kutsal_alan",  "Kutsal Alan",     "heal",   "area_ally",    1.60,  75, 30000, 10.0, 55),
        ("ilahi_kalkan", "İlahi Kalkan",    "buff",   "party",        0.00,  90, 90000, 12.0, 68),
        ("yeniden_dogus","Yeniden Doğuş",   "heal",   "party",        2.80, 150,240000, 12.0, 82),
    ],
}

# Mob arketipleri: (kod, ad, ailesi, hp_carpani, hasar_carpani, saldirgan, hiz)
MOB_ARCHETYPES = [
    ("kurt",     "Kurt",        "hayvan",   0.85, 1.00, True,  "hizli"),
    ("orumcek",  "Örümcek",     "bocek",    0.75, 1.15, True,  "hizli"),
    ("haydut",   "Haydut",      "insan",    1.00, 1.00, True,  "normal"),
    ("golem",    "Golem",       "element",  1.55, 1.30, False, "yavas"),
    ("hortlak",  "Hortlak",     "olumsuz",  1.15, 1.15, True,  "normal"),
    ("harpi",    "Harpi",       "ucan",     0.90, 1.10, True,  "hizli"),
]

# --- Dengeleme hedefleri: mob istatistikleri BUNLARDAN turetilir ---
# Bir mobun HP'si bagimsiz bir formulle degil, o seviyedeki oyuncunun
# beklenen DPS'i x hedef oldurme suresi olarak hesaplanir. Boylece silah
# kademesi degistiginde mob HP'si otomatik uyum saglar.
TARGET_TTK_SEC = 9.0       # normal mob kac saniyede olmeli
TARGET_TTD_SEC = 26.0      # tek mob, iyilesmeyen oyuncuyu kac saniyede oldurmeli
BOSS_TTK_MULT  = 14.0      # boss, normal mobun kac kati dayanmali
SKILL_DPS_BONUS = 1.35     # beceriler duz vurusun uzerine ne kadar ekler

# Bolgeler: (id, kod, ad, tip, min_lvl, max_lvl, mob_sayisi)
ZONES = [
    (1, "north_town",  "Kuzey Şehri",     "safe",     1, 999, 0),
    (2, "south_town",  "Güney Şehri",     "safe",     1, 999, 0),
    (3, "green_field", "Yeşil Ovalar",    "field",    1,  20, 5),
    (4, "warzone",     "Savaş Bölgesi",   "pvp",     20, 999, 4),
    (5, "kuru_gecit",  "Kuru Geçit",      "field",   10,  30, 5),
    (6, "golge_orman", "Gölge Ormanı",    "field",   25,  45, 5),
    (7, "yanik_tepe",  "Yanık Tepeler",   "field",   40,  65, 5),
    (8, "buz_magara",  "Buz Mağarası",    "dungeon", 55,  85, 4),
    (9, "ejder_yuva",  "Ejder Yuvası",    "dungeon", 75, 999, 3),
    (10,"arena",       "Arena",           "arena",   20, 999, 0),
]

ID = {"item": 1000, "skill": 100, "npc": 2000}


def next_id(kind):
    ID[kind] += 1
    return ID[kind]


def expected_player_dps(level, items):
    """O seviyedeki oyuncunun beklenen saniye basina hasari.

    Kademeler arasinda dogrusal gecis yapilir: aksi halde kademe sinirinda
    oyuncu gucu ziplar, moblar da onunla ziplamadigi icin denge bozulur.
    """
    def tier_dps(tier_level):
        ws = [i for i in items if i["category"] == "weapon" and i["req_level"] == tier_level]
        return sum(w["stats"]["dps"] for w in ws) / len(ws)

    levels = [t[2] for t in TIERS]
    if level <= levels[0]:
        base = tier_dps(levels[0])
    elif level >= levels[-1]:
        # Son kademeden sonra seviyeyle hafif buyur
        base = tier_dps(levels[-1]) * (1 + (level - levels[-1]) * 0.012)
    else:
        for a, b in zip(levels, levels[1:]):
            if a <= level < b:
                f = (level - a) / (b - a)
                base = tier_dps(a) * (1 - f) + tier_dps(b) * f
                break
    return base * SKILL_DPS_BONUS


def expected_player_ehp(level, items):
    """O seviyedeki oyuncunun beklenen etkin can havuzu (HP + zirh indirimi)."""
    # Siniflarin ortalamasi (01_core_schema.sql'deki character_class degerleri)
    avg_base_hp = sum(h for h in (140, 110, 85, 95)) / 4
    avg_hp_per_level = sum(h for h in (16, 12, 8, 10)) / 4
    hp = avg_base_hp + avg_hp_per_level * level

    tier = tier_for_level(level)
    # 5 zirh parcasinin max_hp bonusu toplami (share toplami 1.0)
    hp += tier[2] * 6
    # Zirh, gelen hasari azaltir: basit dogrusal indirim modeli
    armor = sum(round(f[2] * s_[3] * tier[3]) for f in ARMOR_FAMILIES[:1] for s_ in ARMOR_SLOTS)
    reduction = min(0.55, armor / (armor + 60 + level * 22))
    return hp / max(0.45, 1 - reduction)


def tier_for_level(level):
    """Verilen seviyeye uygun en yuksek kademeyi dondurur."""
    chosen = TIERS[0]
    for t in TIERS:
        if t[2] <= level:
            chosen = t
    return chosen


# =============================================================================
#  URETICILER
# =============================================================================

def gen_items():
    items = []

    # --- Silahlar: her arketip x her kademe ---
    for wcode, wname, slot, base_dmg, delay, rng, scale_stat, classes in WEAPONS:
        for tcode, tname, tlevel, power, pricem in TIERS:
            dmg = round(base_dmg * power)
            # Saniye basina hasar: dengeleme kontrolu icin hesaplanip saklanir
            dps = round(dmg / delay, 1)
            items.append({
                "id": next_id("item"),
                "code": f"{wcode}_{tcode}",
                "display_name": f"{tname} {wname}",
                "category": "weapon",
                "equip_slot": slot,
                "max_stack": 1,
                "max_durability": 100 + tlevel * 2,
                "req_level": tlevel,
                "req_class": classes[0] if len(classes) == 1 else None,
                "buy_price": 40 * pricem,
                "sell_price": 10 * pricem,
                "weight": 20 + int(base_dmg / 2),
                "is_upgradeable": True,
                "stats": {
                    "damage": dmg,
                    "attack_delay": delay,
                    "range_m": rng,
                    "dps": dps,
                    "scale_stat": scale_stat,
                    "bonus": {scale_stat: max(1, round(tlevel / 6))},
                },
                "_classes": classes,
            })

    # --- Zirhlar: aile x slot x kademe ---
    for fcode, fname, base_ac, classes, bonus_stat in ARMOR_FAMILIES:
        for acode, aname, slot, share in ARMOR_SLOTS:
            for tcode, tname, tlevel, power, pricem in TIERS:
                ac = round(base_ac * share * power)
                items.append({
                    "id": next_id("item"),
                    "code": f"{fcode}_{acode}_{tcode}",
                    "display_name": f"{tname} {fname} {aname}",
                    "category": "armor",
                    "equip_slot": slot,
                    "max_stack": 1,
                    "max_durability": 100 + tlevel * 2,
                    "req_level": tlevel,
                    "req_class": classes[0] if len(classes) == 1 else None,
                    "buy_price": round(26 * pricem * share * 5),
                    "sell_price": round(7 * pricem * share * 5),
                    "weight": round(base_ac * share / 4) + 2,
                    "is_upgradeable": True,
                    "stats": {
                        "armor": ac,
                        "bonus": {
                            bonus_stat: max(1, round(tlevel / 8)),
                            "max_hp": round(tlevel * share * 6),
                        },
                    },
                    "_classes": classes,
                })

    # --- Aksesuarlar ---
    for acode, aname, slot in [("yuzuk", "Yüzük", "ring"), ("kolye", "Kolye", "necklace")]:
        for stat_code, stat_name in [("strength", "Güç"), ("dexterity", "Çeviklik"),
                                     ("intellect", "Zekâ"), ("stamina", "Dayanıklılık")]:
            for tcode, tname, tlevel, power, pricem in TIERS[1:]:
                items.append({
                    "id": next_id("item"),
                    "code": f"{acode}_{stat_code}_{tcode}",
                    "display_name": f"{tname} {stat_name} {aname}",
                    "category": "accessory",
                    "equip_slot": slot,
                    "max_stack": 1,
                    "max_durability": 0,
                    "req_level": tlevel,
                    "req_class": None,
                    "buy_price": 90 * pricem,
                    "sell_price": 22 * pricem,
                    "weight": 1,
                    "is_upgradeable": True,
                    "stats": {"bonus": {stat_code: max(2, round(tlevel / 4))}},
                    "_classes": [],
                })

    # --- Tuketilebilirler ---
    for ccode, cname, kind, potency, lvl, price in [
        ("sifa_kucuk",  "Küçük Şifa İksiri",  "heal_hp",  120,  1,   15),
        ("sifa_orta",   "Orta Şifa İksiri",   "heal_hp",  400, 20,   70),
        ("sifa_buyuk",  "Büyük Şifa İksiri",  "heal_hp", 1200, 45,  260),
        ("mana_kucuk",  "Küçük Mana İksiri",  "heal_mp",  100,  1,   18),
        ("mana_orta",   "Orta Mana İksiri",   "heal_mp",  340, 20,   80),
        ("mana_buyuk",  "Büyük Mana İksiri",  "heal_mp", 1000, 45,  300),
        ("sehir_tasi",  "Şehir Taşı",         "teleport",   0,  5,   50),
        ("tamir_kiti",  "Tamir Kiti",         "repair",    50, 10,  120),
    ]:
        items.append({
            "id": next_id("item"),
            "code": ccode,
            "display_name": cname,
            "category": "consumable",
            "equip_slot": None,
            "max_stack": 200,
            "max_durability": 0,
            "req_level": lvl,
            "req_class": None,
            "buy_price": price,
            "sell_price": max(1, price // 4),
            "weight": 1,
            "is_upgradeable": False,
            "stats": {"effect": kind, "potency": potency},
            "_classes": [],
        })

    # --- Malzemeler (upgrade ve uretim icin) ---
    for mcode, mname, lvl, price in [
        ("kaba_deri",    "Kaba Deri",        1,    6),
        ("demir_cubuk",  "Demir Çubuk",     10,   20),
        ("celik_cubuk",  "Çelik Çubuk",     20,   85),
        ("gumus_toz",    "Gümüş Tozu",      35,  340),
        ("obsidyen_parca","Obsidyen Parçası",50, 1400),
        ("ejder_pulu",   "Ejder Pulu",      70, 6000),
        ("kutsama_tasi", "Kutsama Taşı",    15,  500),
    ]:
        items.append({
            "id": next_id("item"),
            "code": mcode,
            "display_name": mname,
            "category": "material",
            "equip_slot": None,
            "max_stack": 999,
            "max_durability": 0,
            "req_level": 1,
            "req_class": None,
            "buy_price": price,
            "sell_price": max(1, price // 5),
            "weight": 1,
            "is_upgradeable": False,
            "stats": {"material_tier": lvl},
            "_classes": [],
        })

    return items


def gen_skills():
    skills = []
    for class_code, rows in SKILLS.items():
        prev_id = None
        for code, name, kind, target, power, mp, cd, rng, lvl in rows:
            sid = next_id("skill")
            # Etki listesi: kind'a gore uretilir
            if kind in ("damage", "execute"):
                effects = [{"kind": "damage", "school": "physical" if class_code in ("warrior", "rogue") else "magic",
                            "base": round(power * 40 + lvl * power * 6),
                            "weapon_scale": round(power, 2)}]
                if kind == "execute":
                    effects[0]["bonus_below_hp_pct"] = 25
                    effects[0]["bonus_multiplier"] = 2.0
            elif kind == "dot":
                effects = [{"kind": "damage_over_time", "school": "poison",
                            "tick_damage": round(power * 25 + lvl * 2),
                            "tick_interval_ms": 2000, "duration_ms": 12000}]
            elif kind == "heal":
                effects = [{"kind": "heal", "base": round(power * 50 + lvl * power * 8)}]
            elif kind == "buff":
                effects = [{"kind": "buff", "attribute": "armor" if class_code == "warrior" else "all_stats",
                            "magnitude_pct": 10 + lvl // 5, "duration_ms": 15000}]
            elif kind == "debuff":
                effects = [{"kind": "debuff", "attribute": "armor",
                            "magnitude_pct": -(10 + lvl // 4), "duration_ms": 10000}]
            elif kind == "control":
                effects = [{"kind": "control", "effect": "root",
                            "duration_ms": 3000 + lvl * 20}]
            elif kind == "taunt":
                effects = [{"kind": "threat", "multiplier": 4.0, "duration_ms": 6000}]
            elif kind == "mobility":
                effects = [{"kind": "movement", "effect": "dash", "distance_m": 8}]
            elif kind == "stealth":
                effects = [{"kind": "stealth", "duration_ms": 20000}]
            elif kind == "cleanse":
                effects = [{"kind": "cleanse", "max_effects": 2}]
            elif kind == "revive":
                effects = [{"kind": "revive", "hp_pct": 30, "mp_pct": 20}]
            else:
                effects = [{"kind": kind}]

            skills.append({
                "id": sid,
                "code": f"{class_code}_{code}",
                "display_name": name,
                "description": f"{name} — {class_code} becerisi (seviye {lvl}).",
                "class": class_code,
                "req_level": lvl,
                "req_skill_id": prev_id,
                "target_type": target,
                "mp_cost": mp,
                "hp_cost": 0,
                "cast_time_ms": 0 if kind in ("mobility", "stealth") else (400 if class_code in ("warrior", "rogue") else 1200),
                "cooldown_ms": cd,
                "range_m": rng,
                "area_radius_m": 6.0 if "area" in target else 0.0,
                "effects": effects,
                "_kind": kind,
            })
            prev_id = sid
    return skills


def gen_mobs_and_spawns(items):
    """Her bolge icin seviye bandina uygun moblar + loot tablolari + dogma noktalari."""
    mobs, loot, spawns = [], [], []

    # Loot icin kullanilabilir havuzlar
    mats = [i for i in items if i["category"] == "material"]
    potions = [i for i in items if i["category"] == "consumable" and i["stats"].get("effect", "").startswith("heal")]
    gear = [i for i in items if i["category"] in ("weapon", "armor", "accessory")]

    for zid, zcode, zname, ztype, lmin, lmax, mob_count in ZONES:
        if mob_count == 0:
            continue
        band_lo = lmin
        band_hi = min(lmax, lmin + 20) if lmax < 999 else lmin + 20

        for idx in range(mob_count):
            arch = MOB_ARCHETYPES[idx % len(MOB_ARCHETYPES)]
            acode, aname, family, hpm, dmgm, aggro, speed = arch
            # Seviye bant icinde kademeli dagitilir
            lvl = band_lo + round((band_hi - band_lo) * (idx / max(1, mob_count - 1))) if mob_count > 1 else band_lo
            lvl = max(1, lvl)

            # HP ve hasar, bagimsiz formulle degil, o seviyedeki beklenen oyuncu
            # gucunden TURETILIR -> kademe degisince denge kendiliginden korunur.
            pdps = expected_player_dps(lvl, items)
            pehp = expected_player_ehp(lvl, items)
            hp = max(40, round(pdps * TARGET_TTK_SEC * hpm))
            delay_ms = {"hizli": 1100, "normal": 1600, "yavas": 2400}[speed]
            # Mobun saniye basina hasari -> vurus basina hasara cevrilir
            mob_dps = (pehp / TARGET_TTD_SEC) * dmgm
            dmg = max(1, round(mob_dps * (delay_ms / 1000.0)))
            mid = next_id("npc")

            mobs.append({
                "id": mid,
                "code": f"{zcode}_{acode}_{lvl}",
                "display_name": f"{zname.split()[0]} {aname}",
                "npc_kind": "monster",
                "level": lvl,
                "max_hp": hp,
                "max_mp": 0,
                "combat": {
                    "attack": dmg,
                    "armor": round(lvl * 1.8),
                    "attack_delay_ms": delay_ms,
                    "hit_rate": 70 + lvl // 3,
                    "evade_rate": 10 + lvl // 5,
                    "resist": {"fire": lvl // 4, "ice": lvl // 4, "poison": lvl // 3},
                },
                "exp_reward": round(12 + lvl ** 1.75),
                "faction_point_reward": 0,
                "gold_min": round(4 + lvl * 1.4),
                "gold_max": round(9 + lvl * 3.1),
                "ai_profile": {
                    "family": family,
                    "move_speed": {"hizli": 4.2, "normal": 3.2, "yavas": 2.1}[speed],
                    "aggro_radius_m": 12 if aggro else 0,
                    "chase_radius_m": 25,
                    "leash_radius_m": 35,
                    "wander": True,
                },
                "is_aggressive": aggro,
                "respawn_sec": 25 if idx < mob_count - 1 else 45,
                "_zone": zid,
            })

            # --- Loot tablosu ---
            # grup 0: bagimsiz dusenler (malzeme, iksir)
            mat = min(mats, key=lambda m: abs(m["stats"]["material_tier"] - lvl))
            loot.append({"npc_id": mid, "item_id": mat["id"], "ppm": 320000,
                         "qmin": 1, "qmax": 3, "group": 0})
            pot = min(potions, key=lambda p: abs(p["req_level"] - lvl))
            loot.append({"npc_id": mid, "item_id": pot["id"], "ppm": 150000,
                         "qmin": 1, "qmax": 2, "group": 0})
            # grup 1: ekipman -- gruptan en fazla 1 tane duser
            tier = tier_for_level(lvl)
            candidates = [g for g in gear if g["req_level"] == tier[2]]
            for k, g in enumerate(candidates[:4]):
                loot.append({"npc_id": mid, "item_id": g["id"],
                             "ppm": 9000 if k == 0 else 4000,
                             "qmin": 1, "qmax": 1, "group": 1})

            # --- Dogma noktalari: bolge icinde dagitilmis izgara ---
            per_point = 4
            points = 3
            for p in range(points):
                ang = (2 * math.pi * p) / points + idx * 0.7
                r = 40 + idx * 18
                spawns.append({
                    "zone_id": zid,
                    "npc_id": mid,
                    "x": round(math.cos(ang) * r, 2),
                    "y": 0.0,
                    "z": round(math.sin(ang) * r, 2),
                    "heading": round((ang * 180 / math.pi) % 360, 1),
                    "wander_radius_m": 14.0,
                    "spawn_count": per_point,
                    "respawn_sec": None,
                })

        # --- Bolge boss'u ---
        boss_lvl = band_hi + 2
        bid = next_id("npc")
        bpdps = expected_player_dps(boss_lvl, items)
        bpehp = expected_player_ehp(boss_lvl, items)
        mobs.append({
            "id": bid,
            "code": f"{zcode}_boss",
            "display_name": f"{zname} Hükümdarı",
            "npc_kind": "boss",
            "level": boss_lvl,
            # Boss tek oyuncu icin degil, parti icin tasarlanir: HP normal mobun
            # BOSS_TTK_MULT kati, yani 5 kisilik partide ~25 sn surer.
            "max_hp": round(bpdps * TARGET_TTK_SEC * BOSS_TTK_MULT),
            "max_mp": 500,
            "combat": {
                "attack": round((bpehp / TARGET_TTD_SEC) * 2.2 * 1.8),
                "armor": round(boss_lvl * 3.2),
                "attack_delay_ms": 1800,
                "hit_rate": 85 + boss_lvl // 4,
                "evade_rate": 8,
                "resist": {"fire": boss_lvl // 2, "ice": boss_lvl // 2, "poison": boss_lvl // 2},
                "enrage_below_hp_pct": 30,
            },
            "exp_reward": round((12 + boss_lvl ** 1.75) * 20),
            "faction_point_reward": 50,
            "gold_min": round((4 + boss_lvl * 1.4) * 25),
            "gold_max": round((9 + boss_lvl * 3.1) * 25),
            "ai_profile": {
                "family": "boss",
                "move_speed": 3.0,
                "aggro_radius_m": 20,
                "chase_radius_m": 50,
                "leash_radius_m": 70,
                "wander": False,
                "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"},
                           {"below_hp_pct": 30, "add_ability": "summon_adds"}],
            },
            "is_aggressive": True,
            "respawn_sec": 3600,
            "_zone": zid,
        })
        btier = tier_for_level(boss_lvl)
        bgear = [g for g in gear if g["req_level"] == btier[2]]
        for k, g in enumerate(bgear[:8]):
            loot.append({"npc_id": bid, "item_id": g["id"], "ppm": 140000,
                         "qmin": 1, "qmax": 1, "group": 1})
        spawns.append({"zone_id": zid, "npc_id": bid, "x": 0.0, "y": 0.0, "z": 0.0,
                       "heading": 0.0, "wander_radius_m": 0.0, "spawn_count": 1,
                       "respawn_sec": 3600})

    return mobs, loot, spawns


def gen_merchants():
    """Her guvenli bolgeye satici ve kasadar."""
    npcs = []
    for zid, zcode, zname, ztype, lmin, lmax, _ in ZONES:
        if ztype not in ("safe",):
            continue
        for kind, label in [("merchant", "Tüccar"), ("banker", "Kasadar"), ("trainer", "Eğitmen")]:
            npcs.append({
                "id": next_id("npc"),
                "code": f"{zcode}_{kind}",
                "display_name": f"{zname.split()[0]} {label}",
                "npc_kind": kind,
                "level": 1,
                "max_hp": 10000,
                "max_mp": 0,
                "combat": {},
                "exp_reward": 0,
                "faction_point_reward": 0,
                "gold_min": 0,
                "gold_max": 0,
                "ai_profile": {"family": "npc", "wander": False, "aggro_radius_m": 0},
                "is_aggressive": False,
                "respawn_sec": 0,
                "_zone": zid,
            })
    return npcs


# =============================================================================
#  SQL YAZICI
# =============================================================================

def q(v):
    """Tek bir degeri guvenli SQL literaline cevirir."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (dict, list)):
        return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"


def write_sql(items, skills, mobs, loot, spawns, merchants):
    out = []
    w = out.append
    w("-- =============================================================================")
    w("--  02_content_seed.sql  --  OTOMATIK URETILDI, ELLE DUZENLEMEYIN")
    w("--  Kaynak: tools/generate_content.py   (yeniden uretmek icin o betigi calistirin)")
    w("--  Onkosul: 01_core_schema.sql yuklenmis olmali")
    w("-- =============================================================================")
    w("")
    w("BEGIN;")
    w("")

    # --- Zone: core semada 1-4 var, kalanlari ekle, hepsini guncelle ---
    w("-- ---------- BOLGELER ----------")
    for zid, zcode, zname, ztype, lmin, lmax, _ in ZONES:
        w(f"INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES "
          f"({zid}, {q(zcode)}, {q(zname)}, {q(ztype)}, {lmin}, {lmax})")
        w("  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,")
        w("    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;")
    w("")

    w(f"-- ---------- ESYA SABLONLARI ({len(items)} kayit) ----------")
    for i in items:
        cls = f"(SELECT id FROM character_class WHERE code={q(i['req_class'])})" if i["req_class"] else "NULL"
        w("INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,")
        w("    max_durability, req_level, req_class_id, buy_price, sell_price, weight,")
        w("    is_upgradeable, stats) VALUES (")
        w(f"  {i['id']}, {q(i['code'])}, {q(i['display_name'])}, {q(i['category'])}, {q(i['equip_slot'])},")
        w(f"  {i['max_stack']}, {i['max_durability']}, {i['req_level']}, {cls},")
        w(f"  {i['buy_price']}, {i['sell_price']}, {i['weight']}, {q(i['is_upgradeable'])}, {q(i['stats'])}")
        w(") ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,")
        w("    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;")
    w("")

    # Cok-sinifli esya -> sinif baglantilari
    links = [(i["id"], c) for i in items for c in i["_classes"]]
    w(f"-- ---------- ESYA / SINIF BAGLANTILARI ({len(links)} kayit) ----------")
    w("-- Baglanti satiri OLMAYAN esya (iksir, malzeme, aksesuar) her sinifa aciktir.")
    w("DELETE FROM item_template_class;")
    for item_id, class_code in links:
        w(f"INSERT INTO item_template_class (item_template_id, class_id) VALUES "
          f"({item_id}, (SELECT id FROM character_class WHERE code={q(class_code)}));")
    w("")

    w(f"-- ---------- BECERI SABLONLARI ({len(skills)} kayit) ----------")
    w("-- Not: req_skill_id onceki beceriye isaret eder (beceri agaci), bu yuzden sirali eklenir.")
    for s in skills:
        cls = f"(SELECT id FROM character_class WHERE code={q(s['class'])})"
        w("INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,")
        w("    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,")
        w("    range_m, area_radius_m, effects) VALUES (")
        w(f"  {s['id']}, {q(s['code'])}, {q(s['display_name'])}, {q(s['description'])}, {cls}, {s['req_level']},")
        w(f"  {q(s['req_skill_id'])}, {q(s['target_type'])}, {s['mp_cost']}, {s['hp_cost']},")
        w(f"  {s['cast_time_ms']}, {s['cooldown_ms']}, {s['range_m']}, {s['area_radius_m']}, {q(s['effects'])}")
        w(") ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;")
    w("")

    all_npcs = mobs + merchants
    w(f"-- ---------- NPC / MOB SABLONLARI ({len(all_npcs)} kayit) ----------")
    for m in all_npcs:
        w("INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,")
        w("    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,")
        w("    is_aggressive, respawn_sec) VALUES (")
        w(f"  {m['id']}, {q(m['code'])}, {q(m['display_name'])}, {q(m['npc_kind'])}, {m['level']},")
        w(f"  {m['max_hp']}, {m['max_mp']}, {q(m['combat'])}, {m['exp_reward']}, {m['faction_point_reward']},")
        w(f"  {m['gold_min']}, {m['gold_max']}, {q(m['ai_profile'])}, {q(m['is_aggressive'])}, {m['respawn_sec']}")
        w(") ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,")
        w("    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;")
    w("")

    w(f"-- ---------- LOOT TABLOLARI ({len(loot)} kayit) ----------")
    w("DELETE FROM npc_loot_entry;")
    for l in loot:
        w(f"INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, "
          f"quantity_min, quantity_max, loot_group) VALUES ({l['npc_id']}, {l['item_id']}, "
          f"{l['ppm']}, {l['qmin']}, {l['qmax']}, {l['group']});")
    w("")

    w(f"-- ---------- DOGMA NOKTALARI ({len(spawns)} kayit) ----------")
    w("DELETE FROM npc_spawn;")
    for s in spawns:
        w(f"INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, "
          f"wander_radius_m, spawn_count, respawn_sec) VALUES ({s['zone_id']}, {s['npc_id']}, "
          f"{s['x']}, {s['y']}, {s['z']}, {s['heading']}, {s['wander_radius_m']}, "
          f"{s['spawn_count']}, {q(s['respawn_sec'])});")
    w("")
    w("COMMIT;")
    w("")
    return "\n".join(out)


# =============================================================================
#  DENGELEME KONTROLLERI
# =============================================================================

def balance_report(items, skills, mobs):
    lines = []
    lines.append("DENGELEME RAPORU")
    lines.append("=" * 60)

    # Silah DPS egrisi
    lines.append("\nSilah DPS / kademe:")
    for tcode, tname, tlevel, _, _ in TIERS:
        ws = [i for i in items if i["category"] == "weapon" and i["req_level"] == tlevel]
        if ws:
            dps = [w["stats"]["dps"] for w in ws]
            lines.append(f"  sv {tlevel:>3} {tname:<10} DPS {min(dps):>6.1f} - {max(dps):>6.1f}  "
                         f"(fark %{(max(dps)/min(dps)-1)*100:.0f})")

    # Mob oldurme suresi (TTK) ve oyuncunun olme suresi (TTD)
    lines.append(f"\nMob dengesi (hedef: TTK ~{TARGET_TTK_SEC:.0f} sn, TTD ~{TARGET_TTD_SEC:.0f} sn):")
    lines.append("  sv   mob                      HP      TTK     TTD   durum")
    worst = []
    for m in sorted([m for m in mobs if m["npc_kind"] == "monster"], key=lambda x: x["level"]):
        pdps = expected_player_dps(m["level"], items)
        pehp = expected_player_ehp(m["level"], items)
        ttk = m["max_hp"] / pdps
        mob_dps = m["combat"]["attack"] / (m["combat"]["attack_delay_ms"] / 1000.0)
        ttd = pehp / mob_dps
        bad = ttk > TARGET_TTK_SEC * 2 or ttk < 3 or ttd < 8
        if bad:
            worst.append(m["code"])
        flag = "SORUN" if bad else "ok"
        lines.append(f"  {m['level']:>3}  {m['display_name']:<22} {m['max_hp']:>7} "
                     f"{ttk:>6.1f}s {ttd:>6.1f}s   {flag}")
    lines.append(f"\n  Sorunlu mob sayisi: {len(worst)}" + (f" -> {worst}" if worst else ""))

    lines.append("\nBoss dengesi (5 kisilik parti varsayimi):")
    for m in sorted([m for m in mobs if m["npc_kind"] == "boss"], key=lambda x: x["level"]):
        pdps = expected_player_dps(m["level"], items)
        ttk_solo = m["max_hp"] / pdps
        lines.append(f"  sv {m['level']:>3}  {m['display_name']:<24} HP {m['max_hp']:>8}  "
                     f"parti {ttk_solo/5:>5.1f}s   tek basina {ttk_solo:>6.1f}s")

    # Beceri sayisi
    lines.append("\nSinif basina beceri:")
    for _, code, name, _ in CLASSES:
        n = len([s for s in skills if s["class"] == code])
        lines.append(f"  {name:<12} {n} beceri")

    # Kategori dagilimi
    lines.append("\nEsya kategorileri:")
    cats = {}
    for i in items:
        cats[i["category"]] = cats.get(i["category"], 0) + 1
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        lines.append(f"  {c:<12} {n}")

    return "\n".join(lines)


def main():
    CONTENT.mkdir(exist_ok=True)
    SCHEMA.mkdir(parents=True, exist_ok=True)

    items = gen_items()
    skills = gen_skills()
    mobs, loot, spawns = gen_mobs_and_spawns(items)
    merchants = gen_merchants()

    # JSON ciktilari (insan okur, git diff'i anlamli)
    def dump(name, obj):
        path = CONTENT / f"{name}.json"
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    dump("items", items)
    dump("skills", skills)
    dump("npcs", mobs + merchants)
    dump("loot", loot)
    dump("spawns", spawns)
    dump("zones", [{"id": z[0], "code": z[1], "display_name": z[2], "zone_type": z[3],
                    "level_min": z[4], "level_max": z[5]} for z in ZONES])

    sql_path = SCHEMA / "02_content_seed.sql"
    sql_path.write_text(write_sql(items, skills, mobs, loot, spawns, merchants) , encoding="utf-8")

    report = balance_report(items, skills, mobs)
    (CONTENT / "balance_report.txt").write_text(report + "\n", encoding="utf-8")

    print(f"esya      : {len(items)}")
    print(f"beceri    : {len(skills)}")
    print(f"npc/mob   : {len(mobs) + len(merchants)}")
    print(f"loot satir: {len(loot)}")
    print(f"dogma nk. : {len(spawns)}")
    print(f"bolge     : {len(ZONES)}")
    print(f"\nSQL: {sql_path.relative_to(ROOT)}  ({sql_path.stat().st_size // 1024} KB)")
    print()
    print(report)


if __name__ == "__main__":
    main()
