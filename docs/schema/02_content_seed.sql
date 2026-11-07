-- =============================================================================
--  02_content_seed.sql  --  OTOMATIK URETILDI, ELLE DUZENLEMEYIN
--  Kaynak: tools/generate_content.py   (yeniden uretmek icin o betigi calistirin)
--  Onkosul: 01_core_schema.sql yuklenmis olmali
-- =============================================================================

BEGIN;

-- ---------- BOLGELER ----------
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (1, 'north_town', 'Kuzey Şehri', 'safe', 1, 999)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (2, 'south_town', 'Güney Şehri', 'safe', 1, 999)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (3, 'green_field', 'Yeşil Ovalar', 'field', 1, 20)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (4, 'warzone', 'Savaş Bölgesi', 'pvp', 20, 999)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (5, 'kuru_gecit', 'Kuru Geçit', 'field', 10, 30)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (6, 'golge_orman', 'Gölge Ormanı', 'field', 25, 45)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (7, 'yanik_tepe', 'Yanık Tepeler', 'field', 40, 65)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (8, 'buz_magara', 'Buz Mağarası', 'dungeon', 55, 85)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (9, 'ejder_yuva', 'Ejder Yuvası', 'dungeon', 75, 999)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;
INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES (10, 'arena', 'Arena', 'arena', 20, 999)
  ON CONFLICT (id) DO UPDATE SET code=EXCLUDED.code, display_name=EXCLUDED.display_name,
    zone_type=EXCLUDED.zone_type, level_min=EXCLUDED.level_min, level_max=EXCLUDED.level_max;

-- ---------- ESYA SABLONLARI (181 kayit) ----------
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1001, 'kilic_baslangic', 'Başlangıç Kılıç', 'weapon', 'main_hand',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  40, 10, 37, true, '{"damage": 34, "attack_delay": 1.3, "range_m": 2.0, "dps": 26.2, "scale_stat": "strength", "bonus": {"strength": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1002, 'kilic_demir', 'Demir Kılıç', 'weapon', 'main_hand',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  240, 60, 37, true, '{"damage": 61, "attack_delay": 1.3, "range_m": 2.0, "dps": 46.9, "scale_stat": "strength", "bonus": {"strength": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1003, 'kilic_celik', 'Çelik Kılıç', 'weapon', 'main_hand',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  1120, 280, 37, true, '{"damage": 109, "attack_delay": 1.3, "range_m": 2.0, "dps": 83.8, "scale_stat": "strength", "bonus": {"strength": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1004, 'kilic_gumus', 'Gümüş Kılıç', 'weapon', 'main_hand',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  4800, 1200, 37, true, '{"damage": 190, "attack_delay": 1.3, "range_m": 2.0, "dps": 146.2, "scale_stat": "strength", "bonus": {"strength": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1005, 'kilic_obsidyen', 'Obsidyen Kılıç', 'weapon', 'main_hand',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  20800, 5200, 37, true, '{"damage": 323, "attack_delay": 1.3, "range_m": 2.0, "dps": 248.5, "scale_stat": "strength", "bonus": {"strength": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1006, 'kilic_ejder', 'Ejder Kılıç', 'weapon', 'main_hand',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  96000, 24000, 37, true, '{"damage": 544, "attack_delay": 1.3, "range_m": 2.0, "dps": 418.5, "scale_stat": "strength", "bonus": {"strength": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1007, 'balta_baslangic', 'Başlangıç Balta', 'weapon', 'main_hand',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  40, 10, 42, true, '{"damage": 44, "attack_delay": 1.75, "range_m": 2.0, "dps": 25.1, "scale_stat": "strength", "bonus": {"strength": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1008, 'balta_demir', 'Demir Balta', 'weapon', 'main_hand',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  240, 60, 42, true, '{"damage": 79, "attack_delay": 1.75, "range_m": 2.0, "dps": 45.1, "scale_stat": "strength", "bonus": {"strength": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1009, 'balta_celik', 'Çelik Balta', 'weapon', 'main_hand',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  1120, 280, 42, true, '{"damage": 141, "attack_delay": 1.75, "range_m": 2.0, "dps": 80.6, "scale_stat": "strength", "bonus": {"strength": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1010, 'balta_gumus', 'Gümüş Balta', 'weapon', 'main_hand',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  4800, 1200, 42, true, '{"damage": 246, "attack_delay": 1.75, "range_m": 2.0, "dps": 140.6, "scale_stat": "strength", "bonus": {"strength": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1011, 'balta_obsidyen', 'Obsidyen Balta', 'weapon', 'main_hand',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  20800, 5200, 42, true, '{"damage": 418, "attack_delay": 1.75, "range_m": 2.0, "dps": 238.9, "scale_stat": "strength", "bonus": {"strength": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1012, 'balta_ejder', 'Ejder Balta', 'weapon', 'main_hand',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  96000, 24000, 42, true, '{"damage": 704, "attack_delay": 1.75, "range_m": 2.0, "dps": 402.3, "scale_stat": "strength", "bonus": {"strength": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1013, 'topuz_baslangic', 'Başlangıç Topuz', 'weapon', 'main_hand',
  1, 102, 1, NULL,
  40, 10, 39, true, '{"damage": 38, "attack_delay": 1.5, "range_m": 2.0, "dps": 25.3, "scale_stat": "strength", "bonus": {"strength": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1014, 'topuz_demir', 'Demir Topuz', 'weapon', 'main_hand',
  1, 120, 10, NULL,
  240, 60, 39, true, '{"damage": 68, "attack_delay": 1.5, "range_m": 2.0, "dps": 45.3, "scale_stat": "strength", "bonus": {"strength": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1015, 'topuz_celik', 'Çelik Topuz', 'weapon', 'main_hand',
  1, 140, 20, NULL,
  1120, 280, 39, true, '{"damage": 122, "attack_delay": 1.5, "range_m": 2.0, "dps": 81.3, "scale_stat": "strength", "bonus": {"strength": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1016, 'topuz_gumus', 'Gümüş Topuz', 'weapon', 'main_hand',
  1, 170, 35, NULL,
  4800, 1200, 39, true, '{"damage": 213, "attack_delay": 1.5, "range_m": 2.0, "dps": 142.0, "scale_stat": "strength", "bonus": {"strength": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1017, 'topuz_obsidyen', 'Obsidyen Topuz', 'weapon', 'main_hand',
  1, 200, 50, NULL,
  20800, 5200, 39, true, '{"damage": 361, "attack_delay": 1.5, "range_m": 2.0, "dps": 240.7, "scale_stat": "strength", "bonus": {"strength": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1018, 'topuz_ejder', 'Ejder Topuz', 'weapon', 'main_hand',
  1, 240, 70, NULL,
  96000, 24000, 39, true, '{"damage": 608, "attack_delay": 1.5, "range_m": 2.0, "dps": 405.3, "scale_stat": "strength", "bonus": {"strength": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1019, 'hancer_baslangic', 'Başlangıç Hançer', 'weapon', 'main_hand',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  40, 10, 31, true, '{"damage": 22, "attack_delay": 0.85, "range_m": 1.6, "dps": 25.9, "scale_stat": "dexterity", "bonus": {"dexterity": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1020, 'hancer_demir', 'Demir Hançer', 'weapon', 'main_hand',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  240, 60, 31, true, '{"damage": 40, "attack_delay": 0.85, "range_m": 1.6, "dps": 47.1, "scale_stat": "dexterity", "bonus": {"dexterity": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1021, 'hancer_celik', 'Çelik Hançer', 'weapon', 'main_hand',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  1120, 280, 31, true, '{"damage": 70, "attack_delay": 0.85, "range_m": 1.6, "dps": 82.4, "scale_stat": "dexterity", "bonus": {"dexterity": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1022, 'hancer_gumus', 'Gümüş Hançer', 'weapon', 'main_hand',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  4800, 1200, 31, true, '{"damage": 123, "attack_delay": 0.85, "range_m": 1.6, "dps": 144.7, "scale_stat": "dexterity", "bonus": {"dexterity": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1023, 'hancer_obsidyen', 'Obsidyen Hançer', 'weapon', 'main_hand',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  20800, 5200, 31, true, '{"damage": 209, "attack_delay": 0.85, "range_m": 1.6, "dps": 245.9, "scale_stat": "dexterity", "bonus": {"dexterity": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1024, 'hancer_ejder', 'Ejder Hançer', 'weapon', 'main_hand',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  96000, 24000, 31, true, '{"damage": 352, "attack_delay": 0.85, "range_m": 1.6, "dps": 414.1, "scale_stat": "dexterity", "bonus": {"dexterity": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1025, 'yay_baslangic', 'Başlangıç Yay', 'weapon', 'main_hand',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  40, 10, 35, true, '{"damage": 30, "attack_delay": 1.45, "range_m": 14.0, "dps": 20.7, "scale_stat": "dexterity", "bonus": {"dexterity": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1026, 'yay_demir', 'Demir Yay', 'weapon', 'main_hand',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  240, 60, 35, true, '{"damage": 54, "attack_delay": 1.45, "range_m": 14.0, "dps": 37.2, "scale_stat": "dexterity", "bonus": {"dexterity": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1027, 'yay_celik', 'Çelik Yay', 'weapon', 'main_hand',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  1120, 280, 35, true, '{"damage": 96, "attack_delay": 1.45, "range_m": 14.0, "dps": 66.2, "scale_stat": "dexterity", "bonus": {"dexterity": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1028, 'yay_gumus', 'Gümüş Yay', 'weapon', 'main_hand',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  4800, 1200, 35, true, '{"damage": 168, "attack_delay": 1.45, "range_m": 14.0, "dps": 115.9, "scale_stat": "dexterity", "bonus": {"dexterity": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1029, 'yay_obsidyen', 'Obsidyen Yay', 'weapon', 'main_hand',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  20800, 5200, 35, true, '{"damage": 285, "attack_delay": 1.45, "range_m": 14.0, "dps": 196.6, "scale_stat": "dexterity", "bonus": {"dexterity": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1030, 'yay_ejder', 'Ejder Yay', 'weapon', 'main_hand',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  96000, 24000, 35, true, '{"damage": 480, "attack_delay": 1.45, "range_m": 14.0, "dps": 331.0, "scale_stat": "dexterity", "bonus": {"dexterity": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1031, 'asa_baslangic', 'Başlangıç Asa', 'weapon', 'main_hand',
  1, 102, 1, NULL,
  40, 10, 33, true, '{"damage": 26, "attack_delay": 1.6, "range_m": 3.0, "dps": 16.2, "scale_stat": "intellect", "bonus": {"intellect": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1032, 'asa_demir', 'Demir Asa', 'weapon', 'main_hand',
  1, 120, 10, NULL,
  240, 60, 33, true, '{"damage": 47, "attack_delay": 1.6, "range_m": 3.0, "dps": 29.4, "scale_stat": "intellect", "bonus": {"intellect": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1033, 'asa_celik', 'Çelik Asa', 'weapon', 'main_hand',
  1, 140, 20, NULL,
  1120, 280, 33, true, '{"damage": 83, "attack_delay": 1.6, "range_m": 3.0, "dps": 51.9, "scale_stat": "intellect", "bonus": {"intellect": 3}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1034, 'asa_gumus', 'Gümüş Asa', 'weapon', 'main_hand',
  1, 170, 35, NULL,
  4800, 1200, 33, true, '{"damage": 146, "attack_delay": 1.6, "range_m": 3.0, "dps": 91.2, "scale_stat": "intellect", "bonus": {"intellect": 6}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1035, 'asa_obsidyen', 'Obsidyen Asa', 'weapon', 'main_hand',
  1, 200, 50, NULL,
  20800, 5200, 33, true, '{"damage": 247, "attack_delay": 1.6, "range_m": 3.0, "dps": 154.4, "scale_stat": "intellect", "bonus": {"intellect": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1036, 'asa_ejder', 'Ejder Asa', 'weapon', 'main_hand',
  1, 240, 70, NULL,
  96000, 24000, 33, true, '{"damage": 416, "attack_delay": 1.6, "range_m": 3.0, "dps": 260.0, "scale_stat": "intellect", "bonus": {"intellect": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1037, 'plaka_baslik_baslangic', 'Başlangıç Plaka Başlık', 'armor', 'head',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  21, 6, 6, true, '{"armor": 16, "bonus": {"stamina": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1038, 'plaka_baslik_demir', 'Demir Plaka Başlık', 'armor', 'head',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  125, 34, 6, true, '{"armor": 29, "bonus": {"stamina": 1, "max_hp": 10}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1039, 'plaka_baslik_celik', 'Çelik Plaka Başlık', 'armor', 'head',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  582, 157, 6, true, '{"armor": 51, "bonus": {"stamina": 2, "max_hp": 19}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1040, 'plaka_baslik_gumus', 'Gümüş Plaka Başlık', 'armor', 'head',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  2496, 672, 6, true, '{"armor": 90, "bonus": {"stamina": 4, "max_hp": 34}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1041, 'plaka_baslik_obsidyen', 'Obsidyen Plaka Başlık', 'armor', 'head',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  10816, 2912, 6, true, '{"armor": 152, "bonus": {"stamina": 6, "max_hp": 48}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1042, 'plaka_baslik_ejder', 'Ejder Plaka Başlık', 'armor', 'head',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  49920, 13440, 6, true, '{"armor": 256, "bonus": {"stamina": 9, "max_hp": 67}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1043, 'plaka_zirh_baslangic', 'Başlangıç Plaka Zırh', 'armor', 'chest',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  44, 12, 10, true, '{"armor": 34, "bonus": {"stamina": 1, "max_hp": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1044, 'plaka_zirh_demir', 'Demir Plaka Zırh', 'armor', 'chest',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  265, 71, 10, true, '{"armor": 61, "bonus": {"stamina": 1, "max_hp": 20}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1045, 'plaka_zirh_celik', 'Çelik Plaka Zırh', 'armor', 'chest',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  1238, 333, 10, true, '{"armor": 109, "bonus": {"stamina": 2, "max_hp": 41}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1046, 'plaka_zirh_gumus', 'Gümüş Plaka Zırh', 'armor', 'chest',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  5304, 1428, 10, true, '{"armor": 190, "bonus": {"stamina": 4, "max_hp": 71}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1047, 'plaka_zirh_obsidyen', 'Obsidyen Plaka Zırh', 'armor', 'chest',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  22984, 6188, 10, true, '{"armor": 323, "bonus": {"stamina": 6, "max_hp": 102}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1048, 'plaka_zirh_ejder', 'Ejder Plaka Zırh', 'armor', 'chest',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  106080, 28560, 10, true, '{"armor": 544, "bonus": {"stamina": 9, "max_hp": 143}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1049, 'plaka_pantolon_baslangic', 'Başlangıç Plaka Pantolon', 'armor', 'legs',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  31, 8, 8, true, '{"armor": 24, "bonus": {"stamina": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1050, 'plaka_pantolon_demir', 'Demir Plaka Pantolon', 'armor', 'legs',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  187, 50, 8, true, '{"armor": 43, "bonus": {"stamina": 1, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1051, 'plaka_pantolon_celik', 'Çelik Plaka Pantolon', 'armor', 'legs',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  874, 235, 8, true, '{"armor": 77, "bonus": {"stamina": 2, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1052, 'plaka_pantolon_gumus', 'Gümüş Plaka Pantolon', 'armor', 'legs',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  3744, 1008, 8, true, '{"armor": 134, "bonus": {"stamina": 4, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1053, 'plaka_pantolon_obsidyen', 'Obsidyen Plaka Pantolon', 'armor', 'legs',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  16224, 4368, 8, true, '{"armor": 228, "bonus": {"stamina": 6, "max_hp": 72}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1054, 'plaka_pantolon_ejder', 'Ejder Plaka Pantolon', 'armor', 'legs',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  74880, 20160, 8, true, '{"armor": 384, "bonus": {"stamina": 9, "max_hp": 101}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1055, 'plaka_eldiven_baslangic', 'Başlangıç Plaka Eldiven', 'armor', 'hands',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  16, 4, 5, true, '{"armor": 12, "bonus": {"stamina": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1056, 'plaka_eldiven_demir', 'Demir Plaka Eldiven', 'armor', 'hands',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  94, 25, 5, true, '{"armor": 22, "bonus": {"stamina": 1, "max_hp": 7}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1057, 'plaka_eldiven_celik', 'Çelik Plaka Eldiven', 'armor', 'hands',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  437, 118, 5, true, '{"armor": 38, "bonus": {"stamina": 2, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1058, 'plaka_eldiven_gumus', 'Gümüş Plaka Eldiven', 'armor', 'hands',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  1872, 504, 5, true, '{"armor": 67, "bonus": {"stamina": 4, "max_hp": 25}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1059, 'plaka_eldiven_obsidyen', 'Obsidyen Plaka Eldiven', 'armor', 'hands',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  8112, 2184, 5, true, '{"armor": 114, "bonus": {"stamina": 6, "max_hp": 36}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1060, 'plaka_eldiven_ejder', 'Ejder Plaka Eldiven', 'armor', 'hands',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  37440, 10080, 5, true, '{"armor": 192, "bonus": {"stamina": 9, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1061, 'plaka_bot_baslangic', 'Başlangıç Plaka Bot', 'armor', 'feet',
  1, 102, 1, (SELECT id FROM character_class WHERE code='warrior'),
  18, 5, 6, true, '{"armor": 14, "bonus": {"stamina": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1062, 'plaka_bot_demir', 'Demir Plaka Bot', 'armor', 'feet',
  1, 120, 10, (SELECT id FROM character_class WHERE code='warrior'),
  109, 29, 6, true, '{"armor": 25, "bonus": {"stamina": 1, "max_hp": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1063, 'plaka_bot_celik', 'Çelik Plaka Bot', 'armor', 'feet',
  1, 140, 20, (SELECT id FROM character_class WHERE code='warrior'),
  510, 137, 6, true, '{"armor": 45, "bonus": {"stamina": 2, "max_hp": 17}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1064, 'plaka_bot_gumus', 'Gümüş Plaka Bot', 'armor', 'feet',
  1, 170, 35, (SELECT id FROM character_class WHERE code='warrior'),
  2184, 588, 6, true, '{"armor": 78, "bonus": {"stamina": 4, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1065, 'plaka_bot_obsidyen', 'Obsidyen Plaka Bot', 'armor', 'feet',
  1, 200, 50, (SELECT id FROM character_class WHERE code='warrior'),
  9464, 2548, 6, true, '{"armor": 133, "bonus": {"stamina": 6, "max_hp": 42}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1066, 'plaka_bot_ejder', 'Ejder Plaka Bot', 'armor', 'feet',
  1, 240, 70, (SELECT id FROM character_class WHERE code='warrior'),
  43680, 11760, 6, true, '{"armor": 224, "bonus": {"stamina": 9, "max_hp": 59}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1067, 'deri_baslik_baslangic', 'Başlangıç Deri Başlık', 'armor', 'head',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  21, 6, 4, true, '{"armor": 10, "bonus": {"dexterity": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1068, 'deri_baslik_demir', 'Demir Deri Başlık', 'armor', 'head',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  125, 34, 4, true, '{"armor": 18, "bonus": {"dexterity": 1, "max_hp": 10}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1069, 'deri_baslik_celik', 'Çelik Deri Başlık', 'armor', 'head',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  582, 157, 4, true, '{"armor": 32, "bonus": {"dexterity": 2, "max_hp": 19}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1070, 'deri_baslik_gumus', 'Gümüş Deri Başlık', 'armor', 'head',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  2496, 672, 4, true, '{"armor": 56, "bonus": {"dexterity": 4, "max_hp": 34}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1071, 'deri_baslik_obsidyen', 'Obsidyen Deri Başlık', 'armor', 'head',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  10816, 2912, 4, true, '{"armor": 94, "bonus": {"dexterity": 6, "max_hp": 48}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1072, 'deri_baslik_ejder', 'Ejder Deri Başlık', 'armor', 'head',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  49920, 13440, 4, true, '{"armor": 159, "bonus": {"dexterity": 9, "max_hp": 67}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1073, 'deri_zirh_baslangic', 'Başlangıç Deri Zırh', 'armor', 'chest',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  44, 12, 7, true, '{"armor": 21, "bonus": {"dexterity": 1, "max_hp": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1074, 'deri_zirh_demir', 'Demir Deri Zırh', 'armor', 'chest',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  265, 71, 7, true, '{"armor": 38, "bonus": {"dexterity": 1, "max_hp": 20}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1075, 'deri_zirh_celik', 'Çelik Deri Zırh', 'armor', 'chest',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  1238, 333, 7, true, '{"armor": 67, "bonus": {"dexterity": 2, "max_hp": 41}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1076, 'deri_zirh_gumus', 'Gümüş Deri Zırh', 'armor', 'chest',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  5304, 1428, 7, true, '{"armor": 118, "bonus": {"dexterity": 4, "max_hp": 71}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1077, 'deri_zirh_obsidyen', 'Obsidyen Deri Zırh', 'armor', 'chest',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  22984, 6188, 7, true, '{"armor": 200, "bonus": {"dexterity": 6, "max_hp": 102}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1078, 'deri_zirh_ejder', 'Ejder Deri Zırh', 'armor', 'chest',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  106080, 28560, 7, true, '{"armor": 337, "bonus": {"dexterity": 9, "max_hp": 143}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1079, 'deri_pantolon_baslangic', 'Başlangıç Deri Pantolon', 'armor', 'legs',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  31, 8, 6, true, '{"armor": 15, "bonus": {"dexterity": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1080, 'deri_pantolon_demir', 'Demir Deri Pantolon', 'armor', 'legs',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  187, 50, 6, true, '{"armor": 27, "bonus": {"dexterity": 1, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1081, 'deri_pantolon_celik', 'Çelik Deri Pantolon', 'armor', 'legs',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  874, 235, 6, true, '{"armor": 48, "bonus": {"dexterity": 2, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1082, 'deri_pantolon_gumus', 'Gümüş Deri Pantolon', 'armor', 'legs',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  3744, 1008, 6, true, '{"armor": 83, "bonus": {"dexterity": 4, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1083, 'deri_pantolon_obsidyen', 'Obsidyen Deri Pantolon', 'armor', 'legs',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  16224, 4368, 6, true, '{"armor": 141, "bonus": {"dexterity": 6, "max_hp": 72}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1084, 'deri_pantolon_ejder', 'Ejder Deri Pantolon', 'armor', 'legs',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  74880, 20160, 6, true, '{"armor": 238, "bonus": {"dexterity": 9, "max_hp": 101}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1085, 'deri_eldiven_baslangic', 'Başlangıç Deri Eldiven', 'armor', 'hands',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  16, 4, 4, true, '{"armor": 7, "bonus": {"dexterity": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1086, 'deri_eldiven_demir', 'Demir Deri Eldiven', 'armor', 'hands',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  94, 25, 4, true, '{"armor": 13, "bonus": {"dexterity": 1, "max_hp": 7}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1087, 'deri_eldiven_celik', 'Çelik Deri Eldiven', 'armor', 'hands',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  437, 118, 4, true, '{"armor": 24, "bonus": {"dexterity": 2, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1088, 'deri_eldiven_gumus', 'Gümüş Deri Eldiven', 'armor', 'hands',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  1872, 504, 4, true, '{"armor": 42, "bonus": {"dexterity": 4, "max_hp": 25}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1089, 'deri_eldiven_obsidyen', 'Obsidyen Deri Eldiven', 'armor', 'hands',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  8112, 2184, 4, true, '{"armor": 71, "bonus": {"dexterity": 6, "max_hp": 36}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1090, 'deri_eldiven_ejder', 'Ejder Deri Eldiven', 'armor', 'hands',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  37440, 10080, 4, true, '{"armor": 119, "bonus": {"dexterity": 9, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1091, 'deri_bot_baslangic', 'Başlangıç Deri Bot', 'armor', 'feet',
  1, 102, 1, (SELECT id FROM character_class WHERE code='rogue'),
  18, 5, 4, true, '{"armor": 9, "bonus": {"dexterity": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1092, 'deri_bot_demir', 'Demir Deri Bot', 'armor', 'feet',
  1, 120, 10, (SELECT id FROM character_class WHERE code='rogue'),
  109, 29, 4, true, '{"armor": 16, "bonus": {"dexterity": 1, "max_hp": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1093, 'deri_bot_celik', 'Çelik Deri Bot', 'armor', 'feet',
  1, 140, 20, (SELECT id FROM character_class WHERE code='rogue'),
  510, 137, 4, true, '{"armor": 28, "bonus": {"dexterity": 2, "max_hp": 17}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1094, 'deri_bot_gumus', 'Gümüş Deri Bot', 'armor', 'feet',
  1, 170, 35, (SELECT id FROM character_class WHERE code='rogue'),
  2184, 588, 4, true, '{"armor": 49, "bonus": {"dexterity": 4, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1095, 'deri_bot_obsidyen', 'Obsidyen Deri Bot', 'armor', 'feet',
  1, 200, 50, (SELECT id FROM character_class WHERE code='rogue'),
  9464, 2548, 4, true, '{"armor": 82, "bonus": {"dexterity": 6, "max_hp": 42}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1096, 'deri_bot_ejder', 'Ejder Deri Bot', 'armor', 'feet',
  1, 240, 70, (SELECT id FROM character_class WHERE code='rogue'),
  43680, 11760, 4, true, '{"armor": 139, "bonus": {"dexterity": 9, "max_hp": 59}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1097, 'kumas_baslik_baslangic', 'Başlangıç Kumaş Başlık', 'armor', 'head',
  1, 102, 1, NULL,
  21, 6, 4, true, '{"armor": 6, "bonus": {"intellect": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1098, 'kumas_baslik_demir', 'Demir Kumaş Başlık', 'armor', 'head',
  1, 120, 10, NULL,
  125, 34, 4, true, '{"armor": 12, "bonus": {"intellect": 1, "max_hp": 10}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1099, 'kumas_baslik_celik', 'Çelik Kumaş Başlık', 'armor', 'head',
  1, 140, 20, NULL,
  582, 157, 4, true, '{"armor": 20, "bonus": {"intellect": 2, "max_hp": 19}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1100, 'kumas_baslik_gumus', 'Gümüş Kumaş Başlık', 'armor', 'head',
  1, 170, 35, NULL,
  2496, 672, 4, true, '{"armor": 36, "bonus": {"intellect": 4, "max_hp": 34}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1101, 'kumas_baslik_obsidyen', 'Obsidyen Kumaş Başlık', 'armor', 'head',
  1, 200, 50, NULL,
  10816, 2912, 4, true, '{"armor": 61, "bonus": {"intellect": 6, "max_hp": 48}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1102, 'kumas_baslik_ejder', 'Ejder Kumaş Başlık', 'armor', 'head',
  1, 240, 70, NULL,
  49920, 13440, 4, true, '{"armor": 102, "bonus": {"intellect": 9, "max_hp": 67}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1103, 'kumas_zirh_baslangic', 'Başlangıç Kumaş Zırh', 'armor', 'chest',
  1, 102, 1, NULL,
  44, 12, 5, true, '{"armor": 14, "bonus": {"intellect": 1, "max_hp": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1104, 'kumas_zirh_demir', 'Demir Kumaş Zırh', 'armor', 'chest',
  1, 120, 10, NULL,
  265, 71, 5, true, '{"armor": 24, "bonus": {"intellect": 1, "max_hp": 20}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1105, 'kumas_zirh_celik', 'Çelik Kumaş Zırh', 'armor', 'chest',
  1, 140, 20, NULL,
  1238, 333, 5, true, '{"armor": 44, "bonus": {"intellect": 2, "max_hp": 41}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1106, 'kumas_zirh_gumus', 'Gümüş Kumaş Zırh', 'armor', 'chest',
  1, 170, 35, NULL,
  5304, 1428, 5, true, '{"armor": 76, "bonus": {"intellect": 4, "max_hp": 71}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1107, 'kumas_zirh_obsidyen', 'Obsidyen Kumaş Zırh', 'armor', 'chest',
  1, 200, 50, NULL,
  22984, 6188, 5, true, '{"armor": 129, "bonus": {"intellect": 6, "max_hp": 102}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1108, 'kumas_zirh_ejder', 'Ejder Kumaş Zırh', 'armor', 'chest',
  1, 240, 70, NULL,
  106080, 28560, 5, true, '{"armor": 218, "bonus": {"intellect": 9, "max_hp": 143}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1109, 'kumas_pantolon_baslangic', 'Başlangıç Kumaş Pantolon', 'armor', 'legs',
  1, 102, 1, NULL,
  31, 8, 4, true, '{"armor": 10, "bonus": {"intellect": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1110, 'kumas_pantolon_demir', 'Demir Kumaş Pantolon', 'armor', 'legs',
  1, 120, 10, NULL,
  187, 50, 4, true, '{"armor": 17, "bonus": {"intellect": 1, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1111, 'kumas_pantolon_celik', 'Çelik Kumaş Pantolon', 'armor', 'legs',
  1, 140, 20, NULL,
  874, 235, 4, true, '{"armor": 31, "bonus": {"intellect": 2, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1112, 'kumas_pantolon_gumus', 'Gümüş Kumaş Pantolon', 'armor', 'legs',
  1, 170, 35, NULL,
  3744, 1008, 4, true, '{"armor": 54, "bonus": {"intellect": 4, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1113, 'kumas_pantolon_obsidyen', 'Obsidyen Kumaş Pantolon', 'armor', 'legs',
  1, 200, 50, NULL,
  16224, 4368, 4, true, '{"armor": 91, "bonus": {"intellect": 6, "max_hp": 72}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1114, 'kumas_pantolon_ejder', 'Ejder Kumaş Pantolon', 'armor', 'legs',
  1, 240, 70, NULL,
  74880, 20160, 4, true, '{"armor": 154, "bonus": {"intellect": 9, "max_hp": 101}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1115, 'kumas_eldiven_baslangic', 'Başlangıç Kumaş Eldiven', 'armor', 'hands',
  1, 102, 1, NULL,
  16, 4, 3, true, '{"armor": 5, "bonus": {"intellect": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1116, 'kumas_eldiven_demir', 'Demir Kumaş Eldiven', 'armor', 'hands',
  1, 120, 10, NULL,
  94, 25, 3, true, '{"armor": 9, "bonus": {"intellect": 1, "max_hp": 7}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1117, 'kumas_eldiven_celik', 'Çelik Kumaş Eldiven', 'armor', 'hands',
  1, 140, 20, NULL,
  437, 118, 3, true, '{"armor": 15, "bonus": {"intellect": 2, "max_hp": 14}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1118, 'kumas_eldiven_gumus', 'Gümüş Kumaş Eldiven', 'armor', 'hands',
  1, 170, 35, NULL,
  1872, 504, 3, true, '{"armor": 27, "bonus": {"intellect": 4, "max_hp": 25}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1119, 'kumas_eldiven_obsidyen', 'Obsidyen Kumaş Eldiven', 'armor', 'hands',
  1, 200, 50, NULL,
  8112, 2184, 3, true, '{"armor": 46, "bonus": {"intellect": 6, "max_hp": 36}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1120, 'kumas_eldiven_ejder', 'Ejder Kumaş Eldiven', 'armor', 'hands',
  1, 240, 70, NULL,
  37440, 10080, 3, true, '{"armor": 77, "bonus": {"intellect": 9, "max_hp": 50}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1121, 'kumas_bot_baslangic', 'Başlangıç Kumaş Bot', 'armor', 'feet',
  1, 102, 1, NULL,
  18, 5, 3, true, '{"armor": 6, "bonus": {"intellect": 1, "max_hp": 1}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1122, 'kumas_bot_demir', 'Demir Kumaş Bot', 'armor', 'feet',
  1, 120, 10, NULL,
  109, 29, 3, true, '{"armor": 10, "bonus": {"intellect": 1, "max_hp": 8}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1123, 'kumas_bot_celik', 'Çelik Kumaş Bot', 'armor', 'feet',
  1, 140, 20, NULL,
  510, 137, 3, true, '{"armor": 18, "bonus": {"intellect": 2, "max_hp": 17}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1124, 'kumas_bot_gumus', 'Gümüş Kumaş Bot', 'armor', 'feet',
  1, 170, 35, NULL,
  2184, 588, 3, true, '{"armor": 31, "bonus": {"intellect": 4, "max_hp": 29}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1125, 'kumas_bot_obsidyen', 'Obsidyen Kumaş Bot', 'armor', 'feet',
  1, 200, 50, NULL,
  9464, 2548, 3, true, '{"armor": 53, "bonus": {"intellect": 6, "max_hp": 42}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1126, 'kumas_bot_ejder', 'Ejder Kumaş Bot', 'armor', 'feet',
  1, 240, 70, NULL,
  43680, 11760, 3, true, '{"armor": 90, "bonus": {"intellect": 9, "max_hp": 59}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1127, 'yuzuk_strength_demir', 'Demir Güç Yüzük', 'accessory', 'ring',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"strength": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1128, 'yuzuk_strength_celik', 'Çelik Güç Yüzük', 'accessory', 'ring',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"strength": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1129, 'yuzuk_strength_gumus', 'Gümüş Güç Yüzük', 'accessory', 'ring',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"strength": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1130, 'yuzuk_strength_obsidyen', 'Obsidyen Güç Yüzük', 'accessory', 'ring',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"strength": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1131, 'yuzuk_strength_ejder', 'Ejder Güç Yüzük', 'accessory', 'ring',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"strength": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1132, 'yuzuk_dexterity_demir', 'Demir Çeviklik Yüzük', 'accessory', 'ring',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"dexterity": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1133, 'yuzuk_dexterity_celik', 'Çelik Çeviklik Yüzük', 'accessory', 'ring',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"dexterity": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1134, 'yuzuk_dexterity_gumus', 'Gümüş Çeviklik Yüzük', 'accessory', 'ring',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"dexterity": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1135, 'yuzuk_dexterity_obsidyen', 'Obsidyen Çeviklik Yüzük', 'accessory', 'ring',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"dexterity": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1136, 'yuzuk_dexterity_ejder', 'Ejder Çeviklik Yüzük', 'accessory', 'ring',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"dexterity": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1137, 'yuzuk_intellect_demir', 'Demir Zekâ Yüzük', 'accessory', 'ring',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"intellect": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1138, 'yuzuk_intellect_celik', 'Çelik Zekâ Yüzük', 'accessory', 'ring',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"intellect": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1139, 'yuzuk_intellect_gumus', 'Gümüş Zekâ Yüzük', 'accessory', 'ring',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"intellect": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1140, 'yuzuk_intellect_obsidyen', 'Obsidyen Zekâ Yüzük', 'accessory', 'ring',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"intellect": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1141, 'yuzuk_intellect_ejder', 'Ejder Zekâ Yüzük', 'accessory', 'ring',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"intellect": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1142, 'yuzuk_stamina_demir', 'Demir Dayanıklılık Yüzük', 'accessory', 'ring',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"stamina": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1143, 'yuzuk_stamina_celik', 'Çelik Dayanıklılık Yüzük', 'accessory', 'ring',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"stamina": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1144, 'yuzuk_stamina_gumus', 'Gümüş Dayanıklılık Yüzük', 'accessory', 'ring',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"stamina": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1145, 'yuzuk_stamina_obsidyen', 'Obsidyen Dayanıklılık Yüzük', 'accessory', 'ring',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"stamina": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1146, 'yuzuk_stamina_ejder', 'Ejder Dayanıklılık Yüzük', 'accessory', 'ring',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"stamina": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1147, 'kolye_strength_demir', 'Demir Güç Kolye', 'accessory', 'necklace',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"strength": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1148, 'kolye_strength_celik', 'Çelik Güç Kolye', 'accessory', 'necklace',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"strength": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1149, 'kolye_strength_gumus', 'Gümüş Güç Kolye', 'accessory', 'necklace',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"strength": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1150, 'kolye_strength_obsidyen', 'Obsidyen Güç Kolye', 'accessory', 'necklace',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"strength": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1151, 'kolye_strength_ejder', 'Ejder Güç Kolye', 'accessory', 'necklace',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"strength": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1152, 'kolye_dexterity_demir', 'Demir Çeviklik Kolye', 'accessory', 'necklace',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"dexterity": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1153, 'kolye_dexterity_celik', 'Çelik Çeviklik Kolye', 'accessory', 'necklace',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"dexterity": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1154, 'kolye_dexterity_gumus', 'Gümüş Çeviklik Kolye', 'accessory', 'necklace',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"dexterity": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1155, 'kolye_dexterity_obsidyen', 'Obsidyen Çeviklik Kolye', 'accessory', 'necklace',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"dexterity": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1156, 'kolye_dexterity_ejder', 'Ejder Çeviklik Kolye', 'accessory', 'necklace',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"dexterity": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1157, 'kolye_intellect_demir', 'Demir Zekâ Kolye', 'accessory', 'necklace',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"intellect": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1158, 'kolye_intellect_celik', 'Çelik Zekâ Kolye', 'accessory', 'necklace',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"intellect": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1159, 'kolye_intellect_gumus', 'Gümüş Zekâ Kolye', 'accessory', 'necklace',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"intellect": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1160, 'kolye_intellect_obsidyen', 'Obsidyen Zekâ Kolye', 'accessory', 'necklace',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"intellect": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1161, 'kolye_intellect_ejder', 'Ejder Zekâ Kolye', 'accessory', 'necklace',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"intellect": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1162, 'kolye_stamina_demir', 'Demir Dayanıklılık Kolye', 'accessory', 'necklace',
  1, 0, 10, NULL,
  540, 132, 1, true, '{"bonus": {"stamina": 2}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1163, 'kolye_stamina_celik', 'Çelik Dayanıklılık Kolye', 'accessory', 'necklace',
  1, 0, 20, NULL,
  2520, 616, 1, true, '{"bonus": {"stamina": 5}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1164, 'kolye_stamina_gumus', 'Gümüş Dayanıklılık Kolye', 'accessory', 'necklace',
  1, 0, 35, NULL,
  10800, 2640, 1, true, '{"bonus": {"stamina": 9}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1165, 'kolye_stamina_obsidyen', 'Obsidyen Dayanıklılık Kolye', 'accessory', 'necklace',
  1, 0, 50, NULL,
  46800, 11440, 1, true, '{"bonus": {"stamina": 12}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1166, 'kolye_stamina_ejder', 'Ejder Dayanıklılık Kolye', 'accessory', 'necklace',
  1, 0, 70, NULL,
  216000, 52800, 1, true, '{"bonus": {"stamina": 18}}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1167, 'sifa_kucuk', 'Küçük Şifa İksiri', 'consumable', NULL,
  200, 0, 1, NULL,
  15, 3, 1, false, '{"effect": "heal_hp", "potency": 120}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1168, 'sifa_orta', 'Orta Şifa İksiri', 'consumable', NULL,
  200, 0, 20, NULL,
  70, 17, 1, false, '{"effect": "heal_hp", "potency": 400}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1169, 'sifa_buyuk', 'Büyük Şifa İksiri', 'consumable', NULL,
  200, 0, 45, NULL,
  260, 65, 1, false, '{"effect": "heal_hp", "potency": 1200}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1170, 'mana_kucuk', 'Küçük Mana İksiri', 'consumable', NULL,
  200, 0, 1, NULL,
  18, 4, 1, false, '{"effect": "heal_mp", "potency": 100}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1171, 'mana_orta', 'Orta Mana İksiri', 'consumable', NULL,
  200, 0, 20, NULL,
  80, 20, 1, false, '{"effect": "heal_mp", "potency": 340}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1172, 'mana_buyuk', 'Büyük Mana İksiri', 'consumable', NULL,
  200, 0, 45, NULL,
  300, 75, 1, false, '{"effect": "heal_mp", "potency": 1000}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1173, 'sehir_tasi', 'Şehir Taşı', 'consumable', NULL,
  200, 0, 5, NULL,
  50, 12, 1, false, '{"effect": "teleport", "potency": 0}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1174, 'tamir_kiti', 'Tamir Kiti', 'consumable', NULL,
  200, 0, 10, NULL,
  120, 30, 1, false, '{"effect": "repair", "potency": 50}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1175, 'kaba_deri', 'Kaba Deri', 'material', NULL,
  999, 0, 1, NULL,
  6, 1, 1, false, '{"material_tier": 1}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1176, 'demir_cubuk', 'Demir Çubuk', 'material', NULL,
  999, 0, 1, NULL,
  20, 4, 1, false, '{"material_tier": 10}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1177, 'celik_cubuk', 'Çelik Çubuk', 'material', NULL,
  999, 0, 1, NULL,
  85, 17, 1, false, '{"material_tier": 20}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1178, 'gumus_toz', 'Gümüş Tozu', 'material', NULL,
  999, 0, 1, NULL,
  340, 68, 1, false, '{"material_tier": 35}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1179, 'obsidyen_parca', 'Obsidyen Parçası', 'material', NULL,
  999, 0, 1, NULL,
  1400, 280, 1, false, '{"material_tier": 50}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1180, 'ejder_pulu', 'Ejder Pulu', 'material', NULL,
  999, 0, 1, NULL,
  6000, 1200, 1, false, '{"material_tier": 70}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;
INSERT INTO item_template (id, code, display_name, category, equip_slot, max_stack,
    max_durability, req_level, req_class_id, buy_price, sell_price, weight,
    is_upgradeable, stats) VALUES (
  1181, 'kutsama_tasi', 'Kutsama Taşı', 'material', NULL,
  999, 0, 1, NULL,
  500, 100, 1, false, '{"material_tier": 15}'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, stats=EXCLUDED.stats,
    buy_price=EXCLUDED.buy_price, sell_price=EXCLUDED.sell_price;

-- ---------- ESYA / SINIF BAGLANTILARI (168 kayit) ----------
-- Baglanti satiri OLMAYAN esya (iksir, malzeme, aksesuar) her sinifa aciktir.
DELETE FROM item_template_class;
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1001, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1002, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1003, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1004, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1005, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1006, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1007, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1008, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1009, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1010, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1011, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1012, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1013, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1013, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1014, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1014, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1015, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1015, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1016, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1016, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1017, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1017, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1018, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1018, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1019, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1020, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1021, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1022, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1023, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1024, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1025, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1026, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1027, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1028, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1029, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1030, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1031, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1031, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1032, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1032, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1033, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1033, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1034, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1034, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1035, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1035, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1036, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1036, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1037, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1038, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1039, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1040, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1041, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1042, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1043, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1044, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1045, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1046, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1047, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1048, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1049, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1050, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1051, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1052, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1053, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1054, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1055, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1056, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1057, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1058, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1059, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1060, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1061, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1062, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1063, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1064, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1065, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1066, (SELECT id FROM character_class WHERE code='warrior'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1067, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1068, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1069, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1070, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1071, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1072, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1073, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1074, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1075, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1076, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1077, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1078, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1079, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1080, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1081, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1082, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1083, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1084, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1085, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1086, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1087, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1088, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1089, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1090, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1091, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1092, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1093, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1094, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1095, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1096, (SELECT id FROM character_class WHERE code='rogue'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1097, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1097, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1098, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1098, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1099, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1099, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1100, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1100, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1101, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1101, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1102, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1102, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1103, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1103, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1104, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1104, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1105, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1105, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1106, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1106, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1107, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1107, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1108, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1108, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1109, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1109, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1110, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1110, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1111, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1111, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1112, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1112, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1113, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1113, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1114, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1114, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1115, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1115, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1116, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1116, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1117, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1117, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1118, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1118, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1119, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1119, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1120, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1120, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1121, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1121, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1122, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1122, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1123, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1123, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1124, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1124, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1125, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1125, (SELECT id FROM character_class WHERE code='priest'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1126, (SELECT id FROM character_class WHERE code='mage'));
INSERT INTO item_template_class (item_template_id, class_id) VALUES (1126, (SELECT id FROM character_class WHERE code='priest'));

-- ---------- BECERI SABLONLARI (40 kayit) ----------
-- Not: req_skill_id onceki beceriye isaret eder (beceri agaci), bu yuzden sirali eklenir.
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  101, 'warrior_sert_vurus', 'Sert Vuruş', 'Sert Vuruş — warrior becerisi (seviye 2).', (SELECT id FROM character_class WHERE code='warrior'), 2,
  NULL, 'single_enemy', 12, 0,
  400, 4000, 2.0, 0.0, '[{"kind": "damage", "school": "physical", "base": 70, "weapon_scale": 1.35}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  102, 'warrior_kalkan_duvari', 'Kalkan Duvarı', 'Kalkan Duvarı — warrior becerisi (seviye 8).', (SELECT id FROM character_class WHERE code='warrior'), 8,
  101, 'self', 20, 0,
  400, 30000, 0.0, 0.0, '[{"kind": "buff", "attribute": "armor", "magnitude_pct": 11, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  103, 'warrior_yarma', 'Yarma', 'Yarma — warrior becerisi (seviye 14).', (SELECT id FROM character_class WHERE code='warrior'), 14,
  102, 'area_enemy', 28, 0,
  400, 10000, 3.5, 6.0, '[{"kind": "damage", "school": "physical", "base": 136, "weapon_scale": 1.1}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  104, 'warrior_meydan_okuma', 'Meydan Okuma', 'Meydan Okuma — warrior becerisi (seviye 20).', (SELECT id FROM character_class WHERE code='warrior'), 20,
  103, 'single_enemy', 15, 0,
  400, 8000, 8.0, 0.0, '[{"kind": "threat", "multiplier": 4.0, "duration_ms": 6000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  105, 'warrior_kan_cigligi', 'Kan Çığlığı', 'Kan Çığlığı — warrior becerisi (seviye 28).', (SELECT id FROM character_class WHERE code='warrior'), 28,
  104, 'party', 35, 0,
  400, 60000, 0.0, 0.0, '[{"kind": "buff", "attribute": "armor", "magnitude_pct": 15, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  106, 'warrior_zirh_kirici', 'Zırh Kırıcı', 'Zırh Kırıcı — warrior becerisi (seviye 36).', (SELECT id FROM character_class WHERE code='warrior'), 36,
  105, 'single_enemy', 30, 0,
  400, 15000, 2.0, 0.0, '[{"kind": "debuff", "attribute": "armor", "magnitude_pct": -19, "duration_ms": 10000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  107, 'warrior_son_duran', 'Son Duran', 'Son Duran — warrior becerisi (seviye 45).', (SELECT id FROM character_class WHERE code='warrior'), 45,
  106, 'self', 50, 0,
  400, 120000, 0.0, 0.0, '[{"kind": "buff", "attribute": "armor", "magnitude_pct": 19, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  108, 'warrior_girdap', 'Girdap', 'Girdap — warrior becerisi (seviye 55).', (SELECT id FROM character_class WHERE code='warrior'), 55,
  107, 'area_enemy', 55, 0,
  400, 18000, 4.0, 6.0, '[{"kind": "damage", "school": "physical", "base": 574, "weapon_scale": 1.55}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  109, 'warrior_infaz', 'İnfaz', 'İnfaz — warrior becerisi (seviye 68).', (SELECT id FROM character_class WHERE code='warrior'), 68,
  108, 'single_enemy', 60, 0,
  400, 25000, 2.0, 0.0, '[{"kind": "damage", "school": "physical", "base": 1254, "weapon_scale": 2.8, "bonus_below_hp_pct": 25, "bonus_multiplier": 2.0}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  110, 'warrior_savas_tanrisi', 'Savaş Tanrısı', 'Savaş Tanrısı — warrior becerisi (seviye 82).', (SELECT id FROM character_class WHERE code='warrior'), 82,
  109, 'self', 100, 0,
  400, 300000, 0.0, 0.0, '[{"kind": "buff", "attribute": "armor", "magnitude_pct": 26, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  111, 'rogue_hizli_kesik', 'Hızlı Kesik', 'Hızlı Kesik — rogue becerisi (seviye 2).', (SELECT id FROM character_class WHERE code='rogue'), 2,
  NULL, 'single_enemy', 10, 0,
  400, 3000, 1.6, 0.0, '[{"kind": "damage", "school": "physical", "base": 62, "weapon_scale": 1.2}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  112, 'rogue_golge_adim', 'Gölge Adım', 'Gölge Adım — rogue becerisi (seviye 8).', (SELECT id FROM character_class WHERE code='rogue'), 8,
  111, 'self', 18, 0,
  0, 12000, 0.0, 0.0, '[{"kind": "movement", "effect": "dash", "distance_m": 8}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  113, 'rogue_zehirli_bicak', 'Zehirli Bıçak', 'Zehirli Bıçak — rogue becerisi (seviye 14).', (SELECT id FROM character_class WHERE code='rogue'), 14,
  112, 'single_enemy', 22, 0,
  400, 9000, 1.6, 0.0, '[{"kind": "damage_over_time", "school": "poison", "tick_damage": 46, "tick_interval_ms": 2000, "duration_ms": 12000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  114, 'rogue_sirt_hancer', 'Sırttan Hançer', 'Sırttan Hançer — rogue becerisi (seviye 20).', (SELECT id FROM character_class WHERE code='rogue'), 20,
  113, 'single_enemy', 30, 0,
  400, 14000, 1.6, 0.0, '[{"kind": "damage", "school": "physical", "base": 336, "weapon_scale": 2.1}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  115, 'rogue_tuzak', 'Tuzak', 'Tuzak — rogue becerisi (seviye 28).', (SELECT id FROM character_class WHERE code='rogue'), 28,
  114, 'area_enemy', 26, 0,
  400, 20000, 6.0, 6.0, '[{"kind": "control", "effect": "root", "duration_ms": 3560}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  116, 'rogue_ok_yagmuru', 'Ok Yağmuru', 'Ok Yağmuru — rogue becerisi (seviye 36).', (SELECT id FROM character_class WHERE code='rogue'), 36,
  115, 'area_enemy', 40, 0,
  400, 16000, 16.0, 6.0, '[{"kind": "damage", "school": "physical", "base": 333, "weapon_scale": 1.3}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  117, 'rogue_gizlenme', 'Gizlenme', 'Gizlenme — rogue becerisi (seviye 45).', (SELECT id FROM character_class WHERE code='rogue'), 45,
  116, 'self', 45, 0,
  0, 45000, 0.0, 0.0, '[{"kind": "stealth", "duration_ms": 20000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  118, 'rogue_olumcul_isabet', 'Ölümcül İsabet', 'Ölümcül İsabet — rogue becerisi (seviye 55).', (SELECT id FROM character_class WHERE code='rogue'), 55,
  117, 'single_enemy', 50, 0,
  400, 22000, 14.0, 0.0, '[{"kind": "damage", "school": "physical", "base": 962, "weapon_scale": 2.6}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  119, 'rogue_bicak_firtinasi', 'Bıçak Fırtınası', 'Bıçak Fırtınası — rogue becerisi (seviye 68).', (SELECT id FROM character_class WHERE code='rogue'), 68,
  118, 'area_enemy', 60, 0,
  400, 24000, 3.0, 6.0, '[{"kind": "damage", "school": "physical", "base": 806, "weapon_scale": 1.8}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  120, 'rogue_suikast', 'Suikast', 'Suikast — rogue becerisi (seviye 82).', (SELECT id FROM character_class WHERE code='rogue'), 82,
  119, 'single_enemy', 90, 0,
  400, 180000, 1.6, 0.0, '[{"kind": "damage", "school": "physical", "base": 1809, "weapon_scale": 3.4, "bonus_below_hp_pct": 25, "bonus_multiplier": 2.0}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  121, 'mage_ates_oku', 'Ateş Oku', 'Ateş Oku — mage becerisi (seviye 2).', (SELECT id FROM character_class WHERE code='mage'), 2,
  NULL, 'single_enemy', 14, 0,
  1200, 2500, 18.0, 0.0, '[{"kind": "damage", "school": "magic", "base": 75, "weapon_scale": 1.45}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  122, 'mage_buz_zinciri', 'Buz Zinciri', 'Buz Zinciri — mage becerisi (seviye 8).', (SELECT id FROM character_class WHERE code='mage'), 8,
  121, 'single_enemy', 20, 0,
  1200, 14000, 16.0, 0.0, '[{"kind": "control", "effect": "root", "duration_ms": 3160}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  123, 'mage_alev_halkasi', 'Alev Halkası', 'Alev Halkası — mage becerisi (seviye 14).', (SELECT id FROM character_class WHERE code='mage'), 14,
  122, 'area_enemy', 34, 0,
  1200, 11000, 14.0, 6.0, '[{"kind": "damage", "school": "magic", "base": 155, "weapon_scale": 1.25}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  124, 'mage_mana_kalkani', 'Mana Kalkanı', 'Mana Kalkanı — mage becerisi (seviye 20).', (SELECT id FROM character_class WHERE code='mage'), 20,
  123, 'self', 28, 0,
  1200, 35000, 0.0, 0.0, '[{"kind": "buff", "attribute": "all_stats", "magnitude_pct": 14, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  125, 'mage_yildirim', 'Yıldırım', 'Yıldırım — mage becerisi (seviye 28).', (SELECT id FROM character_class WHERE code='mage'), 28,
  124, 'single_enemy', 42, 0,
  1200, 9000, 20.0, 0.0, '[{"kind": "damage", "school": "magic", "base": 416, "weapon_scale": 2.0}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  126, 'mage_donma', 'Donma', 'Donma — mage becerisi (seviye 36).', (SELECT id FROM character_class WHERE code='mage'), 36,
  125, 'area_enemy', 48, 0,
  1200, 25000, 14.0, 6.0, '[{"kind": "control", "effect": "root", "duration_ms": 3720}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  127, 'mage_isinlanma', 'Işınlanma', 'Işınlanma — mage becerisi (seviye 45).', (SELECT id FROM character_class WHERE code='mage'), 45,
  126, 'self', 40, 0,
  0, 30000, 0.0, 0.0, '[{"kind": "movement", "effect": "dash", "distance_m": 8}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  128, 'mage_meteor', 'Meteor', 'Meteor — mage becerisi (seviye 55).', (SELECT id FROM character_class WHERE code='mage'), 55,
  127, 'area_enemy', 70, 0,
  1200, 28000, 22.0, 6.0, '[{"kind": "damage", "school": "magic", "base": 888, "weapon_scale": 2.4}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  129, 'mage_zaman_yarigi', 'Zaman Yarığı', 'Zaman Yarığı — mage becerisi (seviye 68).', (SELECT id FROM character_class WHERE code='mage'), 68,
  128, 'area_enemy', 65, 0,
  1200, 40000, 18.0, 6.0, '[{"kind": "debuff", "attribute": "armor", "magnitude_pct": -27, "duration_ms": 10000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  130, 'mage_kiyamet', 'Kıyamet', 'Kıyamet — mage becerisi (seviye 82).', (SELECT id FROM character_class WHERE code='mage'), 82,
  129, 'area_enemy', 130, 0,
  1200, 240000, 24.0, 6.0, '[{"kind": "damage", "school": "magic", "base": 1915, "weapon_scale": 3.6}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  131, 'priest_kutsal_isik', 'Kutsal Işık', 'Kutsal Işık — priest becerisi (seviye 2).', (SELECT id FROM character_class WHERE code='priest'), 2,
  NULL, 'single_ally', 16, 0,
  1200, 2000, 16.0, 0.0, '[{"kind": "heal", "base": 92}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  132, 'priest_koruma', 'Koruma', 'Koruma — priest becerisi (seviye 8).', (SELECT id FROM character_class WHERE code='priest'), 8,
  131, 'single_ally', 22, 0,
  1200, 25000, 16.0, 0.0, '[{"kind": "buff", "attribute": "all_stats", "magnitude_pct": 11, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  133, 'priest_arindirma', 'Arındırma', 'Arındırma — priest becerisi (seviye 14).', (SELECT id FROM character_class WHERE code='priest'), 14,
  132, 'single_ally', 18, 0,
  1200, 8000, 16.0, 0.0, '[{"kind": "cleanse", "max_effects": 2}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  134, 'priest_ceza', 'Ceza', 'Ceza — priest becerisi (seviye 20).', (SELECT id FROM character_class WHERE code='priest'), 20,
  133, 'single_enemy', 24, 0,
  1200, 6000, 14.0, 0.0, '[{"kind": "damage", "school": "magic", "base": 184, "weapon_scale": 1.15}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  135, 'priest_toplu_sifa', 'Toplu Şifa', 'Toplu Şifa — priest becerisi (seviye 28).', (SELECT id FROM character_class WHERE code='priest'), 28,
  134, 'party', 55, 0,
  1200, 15000, 12.0, 0.0, '[{"kind": "heal", "base": 274}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  136, 'priest_lanet', 'Lanet', 'Lanet — priest becerisi (seviye 36).', (SELECT id FROM character_class WHERE code='priest'), 36,
  135, 'single_enemy', 30, 0,
  1200, 18000, 14.0, 0.0, '[{"kind": "debuff", "attribute": "armor", "magnitude_pct": -19, "duration_ms": 10000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  137, 'priest_dirilis', 'Diriliş', 'Diriliş — priest becerisi (seviye 45).', (SELECT id FROM character_class WHERE code='priest'), 45,
  136, 'single_ally', 80, 0,
  1200, 300000, 8.0, 0.0, '[{"kind": "revive", "hp_pct": 30, "mp_pct": 20}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  138, 'priest_kutsal_alan', 'Kutsal Alan', 'Kutsal Alan — priest becerisi (seviye 55).', (SELECT id FROM character_class WHERE code='priest'), 55,
  137, 'area_ally', 75, 0,
  1200, 30000, 10.0, 6.0, '[{"kind": "heal", "base": 784}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  139, 'priest_ilahi_kalkan', 'İlahi Kalkan', 'İlahi Kalkan — priest becerisi (seviye 68).', (SELECT id FROM character_class WHERE code='priest'), 68,
  138, 'party', 90, 0,
  1200, 90000, 12.0, 0.0, '[{"kind": "buff", "attribute": "all_stats", "magnitude_pct": 23, "duration_ms": 15000}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;
INSERT INTO skill_template (id, code, display_name, description, class_id, req_level,
    req_skill_id, target_type, mp_cost, hp_cost, cast_time_ms, cooldown_ms,
    range_m, area_radius_m, effects) VALUES (
  140, 'priest_yeniden_dogus', 'Yeniden Doğuş', 'Yeniden Doğuş — priest becerisi (seviye 82).', (SELECT id FROM character_class WHERE code='priest'), 82,
  139, 'party', 150, 0,
  1200, 240000, 12.0, 0.0, '[{"kind": "heal", "base": 1977}]'::jsonb
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, effects=EXCLUDED.effects;

-- ---------- NPC / MOB SABLONLARI (44 kayit) ----------
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2001, 'green_field_kurt_1', 'Yeşil Kurt', 'monster', 1,
  240, 0, '{"attack": 12, "armor": 2, "attack_delay_ms": 1100, "hit_rate": 70, "evade_rate": 10, "resist": {"fire": 0, "ice": 0, "poison": 0}}'::jsonb, 13, 0,
  5, 12, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2002, 'green_field_orumcek_6', 'Yeşil Örümcek', 'monster', 6,
  306, 0, '{"attack": 14, "armor": 11, "attack_delay_ms": 1100, "hit_rate": 72, "evade_rate": 11, "resist": {"fire": 1, "ice": 1, "poison": 2}}'::jsonb, 35, 0,
  12, 28, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2003, 'green_field_haydut_11', 'Yeşil Haydut', 'monster', 11,
  548, 0, '{"attack": 29, "armor": 20, "attack_delay_ms": 1600, "hit_rate": 73, "evade_rate": 12, "resist": {"fire": 2, "ice": 2, "poison": 3}}'::jsonb, 78, 0,
  19, 43, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2004, 'green_field_golem_15', 'Yeşil Golem', 'monster', 15,
  1094, 0, '{"attack": 60, "armor": 27, "attack_delay_ms": 2400, "hit_rate": 75, "evade_rate": 13, "resist": {"fire": 3, "ice": 3, "poison": 5}}'::jsonb, 126, 0,
  25, 56, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2005, 'green_field_hortlak_20', 'Yeşil Hortlak', 'monster', 20,
  1039, 0, '{"attack": 53, "armor": 36, "attack_delay_ms": 1600, "hit_rate": 76, "evade_rate": 14, "resist": {"fire": 5, "ice": 5, "poison": 6}}'::jsonb, 201, 0,
  32, 71, '{"family": "olumsuz", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2006, 'green_field_boss', 'Yeşil Ovalar Hükümdarı', 'boss', 22,
  13914, 500, '{"attack": 116, "armor": 70, "attack_delay_ms": 1800, "hit_rate": 90, "evade_rate": 8, "resist": {"fire": 11, "ice": 11, "poison": 11}, "enrage_below_hp_pct": 30}'::jsonb, 4710, 50,
  870, 1930, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2007, 'warzone_kurt_20', 'Savaş Kurt', 'monster', 20,
  768, 0, '{"attack": 32, "armor": 36, "attack_delay_ms": 1100, "hit_rate": 76, "evade_rate": 14, "resist": {"fire": 5, "ice": 5, "poison": 6}}'::jsonb, 201, 0,
  32, 71, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2008, 'warzone_orumcek_27', 'Savaş Örümcek', 'monster', 27,
  915, 0, '{"attack": 39, "armor": 49, "attack_delay_ms": 1100, "hit_rate": 79, "evade_rate": 15, "resist": {"fire": 6, "ice": 6, "poison": 9}}'::jsonb, 332, 0,
  42, 93, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2009, 'warzone_haydut_33', 'Savaş Haydut', 'monster', 33,
  1490, 0, '{"attack": 53, "armor": 59, "attack_delay_ms": 1600, "hit_rate": 81, "evade_rate": 16, "resist": {"fire": 8, "ice": 8, "poison": 11}}'::jsonb, 466, 0,
  50, 111, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2010, 'warzone_golem_40', 'Savaş Golem', 'monster', 40,
  3020, 0, '{"attack": 149, "armor": 72, "attack_delay_ms": 2400, "hit_rate": 83, "evade_rate": 18, "resist": {"fire": 10, "ice": 10, "poison": 13}}'::jsonb, 648, 0,
  60, 133, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2011, 'warzone_boss', 'Savaş Bölgesi Hükümdarı', 'boss', 42,
  29332, 500, '{"attack": 191, "armor": 134, "attack_delay_ms": 1800, "hit_rate": 95, "evade_rate": 8, "resist": {"fire": 21, "ice": 21, "poison": 21}, "enrage_below_hp_pct": 30}'::jsonb, 14099, 50,
  1570, 3480, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2012, 'kuru_gecit_kurt_10', 'Kuru Kurt', 'monster', 10,
  432, 0, '{"attack": 20, "armor": 18, "attack_delay_ms": 1100, "hit_rate": 73, "evade_rate": 12, "resist": {"fire": 2, "ice": 2, "poison": 3}}'::jsonb, 68, 0,
  18, 40, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2013, 'kuru_gecit_orumcek_15', 'Kuru Örümcek', 'monster', 15,
  529, 0, '{"attack": 24, "armor": 27, "attack_delay_ms": 1100, "hit_rate": 75, "evade_rate": 13, "resist": {"fire": 3, "ice": 3, "poison": 5}}'::jsonb, 126, 0,
  25, 56, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2014, 'kuru_gecit_haydut_20', 'Kuru Haydut', 'monster', 20,
  904, 0, '{"attack": 46, "armor": 36, "attack_delay_ms": 1600, "hit_rate": 76, "evade_rate": 14, "resist": {"fire": 5, "ice": 5, "poison": 6}}'::jsonb, 201, 0,
  32, 71, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2015, 'kuru_gecit_golem_25', 'Kuru Golem', 'monster', 25,
  1750, 0, '{"attack": 94, "armor": 45, "attack_delay_ms": 2400, "hit_rate": 78, "evade_rate": 15, "resist": {"fire": 6, "ice": 6, "poison": 8}}'::jsonb, 292, 0,
  39, 86, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2016, 'kuru_gecit_hortlak_30', 'Kuru Hortlak', 'monster', 30,
  1558, 0, '{"attack": 59, "armor": 54, "attack_delay_ms": 1600, "hit_rate": 80, "evade_rate": 16, "resist": {"fire": 7, "ice": 7, "poison": 10}}'::jsonb, 397, 0,
  46, 102, '{"family": "olumsuz", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2017, 'kuru_gecit_boss', 'Kuru Geçit Hükümdarı', 'boss', 32,
  20234, 500, '{"attack": 129, "armor": 102, "attack_delay_ms": 1800, "hit_rate": 93, "evade_rate": 8, "resist": {"fire": 16, "ice": 16, "poison": 16}, "enrage_below_hp_pct": 30}'::jsonb, 8851, 50,
  1220, 2705, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2018, 'golge_orman_kurt_25', 'Gölge Kurt', 'monster', 25,
  960, 0, '{"attack": 33, "armor": 45, "attack_delay_ms": 1100, "hit_rate": 78, "evade_rate": 15, "resist": {"fire": 6, "ice": 6, "poison": 8}}'::jsonb, 292, 0,
  39, 86, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2019, 'golge_orman_orumcek_30', 'Gölge Örümcek', 'monster', 30,
  1016, 0, '{"attack": 40, "armor": 54, "attack_delay_ms": 1100, "hit_rate": 80, "evade_rate": 16, "resist": {"fire": 7, "ice": 7, "poison": 10}}'::jsonb, 397, 0,
  46, 102, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2020, 'golge_orman_haydut_35', 'Gölge Haydut', 'monster', 35,
  1581, 0, '{"attack": 74, "armor": 63, "attack_delay_ms": 1600, "hit_rate": 81, "evade_rate": 17, "resist": {"fire": 8, "ice": 8, "poison": 11}}'::jsonb, 516, 0,
  53, 118, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2021, 'golge_orman_golem_40', 'Gölge Golem', 'monster', 40,
  3020, 0, '{"attack": 149, "armor": 72, "attack_delay_ms": 2400, "hit_rate": 83, "evade_rate": 18, "resist": {"fire": 10, "ice": 10, "poison": 13}}'::jsonb, 648, 0,
  60, 133, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2022, 'golge_orman_hortlak_45', 'Gölge Hortlak', 'monster', 45,
  2663, 0, '{"attack": 91, "armor": 81, "attack_delay_ms": 1600, "hit_rate": 85, "evade_rate": 19, "resist": {"fire": 11, "ice": 11, "poison": 15}}'::jsonb, 794, 0,
  67, 148, '{"family": "olumsuz", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2023, 'golge_orman_boss', 'Gölge Ormanı Hükümdarı', 'boss', 47,
  34477, 500, '{"attack": 197, "armor": 150, "attack_delay_ms": 1800, "hit_rate": 96, "evade_rate": 8, "resist": {"fire": 23, "ice": 23, "poison": 23}, "enrage_below_hp_pct": 30}'::jsonb, 17113, 50,
  1745, 3868, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2024, 'yanik_tepe_kurt_40', 'Yanık Kurt', 'monster', 40,
  1656, 0, '{"attack": 52, "armor": 72, "attack_delay_ms": 1100, "hit_rate": 83, "evade_rate": 18, "resist": {"fire": 10, "ice": 10, "poison": 13}}'::jsonb, 648, 0,
  60, 133, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2025, 'yanik_tepe_orumcek_45', 'Yanık Örümcek', 'monster', 45,
  1737, 0, '{"attack": 62, "armor": 81, "attack_delay_ms": 1100, "hit_rate": 85, "evade_rate": 19, "resist": {"fire": 11, "ice": 11, "poison": 15}}'::jsonb, 794, 0,
  67, 148, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2026, 'yanik_tepe_haydut_50', 'Yanık Haydut', 'monster', 50,
  2683, 0, '{"attack": 110, "armor": 90, "attack_delay_ms": 1600, "hit_rate": 86, "evade_rate": 20, "resist": {"fire": 12, "ice": 12, "poison": 16}}'::jsonb, 952, 0,
  74, 164, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2027, 'yanik_tepe_golem_55', 'Yanık Golem', 'monster', 55,
  4870, 0, '{"attack": 218, "armor": 99, "attack_delay_ms": 2400, "hit_rate": 88, "evade_rate": 21, "resist": {"fire": 13, "ice": 13, "poison": 18}}'::jsonb, 1123, 0,
  81, 180, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2028, 'yanik_tepe_hortlak_60', 'Yanık Hortlak', 'monster', 60,
  4141, 0, '{"attack": 131, "armor": 108, "attack_delay_ms": 1600, "hit_rate": 90, "evade_rate": 22, "resist": {"fire": 15, "ice": 15, "poison": 20}}'::jsonb, 1305, 0,
  88, 195, '{"family": "olumsuz", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2029, 'yanik_tepe_boss', 'Yanık Tepeler Hükümdarı', 'boss', 62,
  52978, 500, '{"attack": 285, "armor": 198, "attack_delay_ms": 1800, "hit_rate": 100, "evade_rate": 8, "resist": {"fire": 31, "ice": 31, "poison": 31}, "enrage_below_hp_pct": 30}'::jsonb, 27638, 50,
  2270, 5030, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2030, 'buz_magara_kurt_55', 'Buz Kurt', 'monster', 55,
  2671, 0, '{"attack": 77, "armor": 99, "attack_delay_ms": 1100, "hit_rate": 88, "evade_rate": 21, "resist": {"fire": 13, "ice": 13, "poison": 18}}'::jsonb, 1123, 0,
  81, 180, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2031, 'buz_magara_orumcek_62', 'Buz Örümcek', 'monster', 62,
  2838, 0, '{"attack": 91, "armor": 112, "attack_delay_ms": 1100, "hit_rate": 90, "evade_rate": 22, "resist": {"fire": 15, "ice": 15, "poison": 20}}'::jsonb, 1382, 0,
  91, 201, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2032, 'buz_magara_haydut_68', 'Buz Haydut', 'monster', 68,
  4335, 0, '{"attack": 118, "armor": 122, "attack_delay_ms": 1600, "hit_rate": 92, "evade_rate": 23, "resist": {"fire": 17, "ice": 17, "poison": 22}}'::jsonb, 1622, 0,
  99, 220, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2033, 'buz_magara_golem_75', 'Buz Golem', 'monster', 75,
  7423, 0, '{"attack": 323, "armor": 135, "attack_delay_ms": 2400, "hit_rate": 95, "evade_rate": 25, "resist": {"fire": 18, "ice": 18, "poison": 25}}'::jsonb, 1923, 0,
  109, 242, '{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, false, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2034, 'buz_magara_boss', 'Buz Mağarası Hükümdarı', 'boss', 77,
  68568, 500, '{"attack": 412, "armor": 246, "attack_delay_ms": 1800, "hit_rate": 104, "evade_rate": 8, "resist": {"fire": 38, "ice": 38, "poison": 38}, "enrage_below_hp_pct": 30}'::jsonb, 40270, 50,
  2795, 6192, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2035, 'ejder_yuva_kurt_75', 'Ejder Kurt', 'monster', 75,
  4071, 0, '{"attack": 114, "armor": 135, "attack_delay_ms": 1100, "hit_rate": 95, "evade_rate": 25, "resist": {"fire": 18, "ice": 18, "poison": 25}}'::jsonb, 1923, 0,
  109, 242, '{"family": "hayvan", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2036, 'ejder_yuva_orumcek_85', 'Ejder Örümcek', 'monster', 85,
  3999, 0, '{"attack": 134, "armor": 153, "attack_delay_ms": 1100, "hit_rate": 98, "evade_rate": 27, "resist": {"fire": 21, "ice": 21, "poison": 28}}'::jsonb, 2391, 0,
  123, 272, '{"family": "bocek", "move_speed": 4.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 25
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2037, 'ejder_yuva_haydut_95', 'Ejder Haydut', 'monster', 95,
  5874, 0, '{"attack": 174, "armor": 171, "attack_delay_ms": 1600, "hit_rate": 101, "evade_rate": 29, "resist": {"fire": 23, "ice": 23, "poison": 31}}'::jsonb, 2903, 0,
  137, 304, '{"family": "insan", "move_speed": 3.2, "aggro_radius_m": 12, "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}'::jsonb, true, 45
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2038, 'ejder_yuva_boss', 'Ejder Yuvası Hükümdarı', 'boss', 97,
  83749, 500, '{"attack": 433, "armor": 310, "attack_delay_ms": 1800, "hit_rate": 109, "evade_rate": 8, "resist": {"fire": 48, "ice": 48, "poison": 48}, "enrage_below_hp_pct": 30}'::jsonb, 60203, 50,
  3495, 7742, '{"family": "boss", "move_speed": 3.0, "aggro_radius_m": 20, "chase_radius_m": 50, "leash_radius_m": 70, "wander": false, "phases": [{"below_hp_pct": 60, "add_ability": "area_slam"}, {"below_hp_pct": 30, "add_ability": "summon_adds"}]}'::jsonb, true, 3600
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2039, 'north_town_merchant', 'Kuzey Tüccar', 'merchant', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2040, 'north_town_banker', 'Kuzey Kasadar', 'banker', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2041, 'north_town_trainer', 'Kuzey Eğitmen', 'trainer', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2042, 'south_town_merchant', 'Güney Tüccar', 'merchant', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2043, 'south_town_banker', 'Güney Kasadar', 'banker', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;
INSERT INTO npc_template (id, code, display_name, npc_kind, level, max_hp, max_mp,
    combat, exp_reward, faction_point_reward, gold_min, gold_max, ai_profile,
    is_aggressive, respawn_sec) VALUES (
  2044, 'south_town_trainer', 'Güney Eğitmen', 'trainer', 1,
  10000, 0, '{}'::jsonb, 0, 0,
  0, 0, '{"family": "npc", "wander": false, "aggro_radius_m": 0}'::jsonb, false, 0
) ON CONFLICT (id) DO UPDATE SET display_name=EXCLUDED.display_name, combat=EXCLUDED.combat,
    max_hp=EXCLUDED.max_hp, ai_profile=EXCLUDED.ai_profile;

-- ---------- LOOT TABLOLARI (242 kayit) ----------
DELETE FROM npc_loot_entry;
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1175, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1167, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1001, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1007, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1013, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2001, 1019, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1176, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1167, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1001, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1007, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1013, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2002, 1019, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1176, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1002, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1008, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1014, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2003, 1020, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1181, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1002, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1008, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1014, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2004, 1020, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2005, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1003, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1009, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1015, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1021, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1027, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1033, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1039, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2006, 1045, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2007, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2008, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2009, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2010, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1004, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1010, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1016, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1022, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1028, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1034, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1040, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2011, 1046, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1176, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1167, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1002, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1008, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1014, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2012, 1020, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1181, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1002, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1008, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1014, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2013, 1020, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2014, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2015, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2016, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1003, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1009, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1015, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1021, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1027, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1033, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1039, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2017, 1045, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1177, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2018, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1168, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1003, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1009, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1015, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2019, 1021, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2020, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2021, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2022, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1004, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1010, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1016, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1022, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1028, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1034, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1040, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2023, 1046, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1178, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2024, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1004, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1010, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1016, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2025, 1022, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2026, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2027, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2028, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1005, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1011, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1017, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1023, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1029, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1035, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1041, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2029, 1047, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1179, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2030, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2031, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1005, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1011, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1017, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2032, 1023, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1006, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1012, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1018, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2033, 1024, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1006, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1012, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1018, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1024, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1030, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1036, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1042, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2034, 1048, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1006, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1012, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1018, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2035, 1024, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1006, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1012, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1018, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2036, 1024, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1180, 320000, 1, 3, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1169, 150000, 1, 2, 0);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1006, 9000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1012, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1018, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2037, 1024, 4000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1006, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1012, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1018, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1024, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1030, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1036, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1042, 140000, 1, 1, 1);
INSERT INTO npc_loot_entry (npc_template_id, item_template_id, drop_rate_ppm, quantity_min, quantity_max, loot_group) VALUES (2038, 1048, 140000, 1, 1, 1);

-- ---------- DOGMA NOKTALARI (100 kayit) ----------
DELETE FROM npc_spawn;
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2001, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2001, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2001, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2002, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2002, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2002, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2003, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2003, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2003, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2004, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2004, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2004, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2005, -105.53, 0.0, 37.52, 160.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2005, 20.27, 0.0, -110.15, 280.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2005, 85.26, 0.0, 72.63, 40.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (3, 2006, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2007, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2007, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2007, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2008, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2008, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2008, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2009, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2009, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2009, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2010, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2010, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2010, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (4, 2011, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2012, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2012, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2012, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2013, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2013, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2013, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2014, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2014, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2014, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2015, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2015, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2015, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2016, -105.53, 0.0, 37.52, 160.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2016, 20.27, 0.0, -110.15, 280.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2016, 85.26, 0.0, 72.63, 40.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (5, 2017, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2018, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2018, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2018, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2019, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2019, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2019, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2020, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2020, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2020, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2021, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2021, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2021, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2022, -105.53, 0.0, 37.52, 160.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2022, 20.27, 0.0, -110.15, 280.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2022, 85.26, 0.0, 72.63, 40.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (6, 2023, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2024, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2024, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2024, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2025, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2025, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2025, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2026, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2026, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2026, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2027, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2027, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2027, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2028, -105.53, 0.0, 37.52, 160.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2028, 20.27, 0.0, -110.15, 280.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2028, 85.26, 0.0, 72.63, 40.4, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (7, 2029, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2030, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2030, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2030, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2031, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2031, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2031, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2032, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2032, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2032, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2033, -47.46, 0.0, 81.14, 120.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2033, -46.54, 0.0, -81.67, 240.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2033, 94.0, 0.0, 0.53, 0.3, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (8, 2034, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2035, 40.0, 0.0, 0.0, 0.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2035, -20.0, 0.0, 34.64, 120.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2035, -20.0, 0.0, -34.64, 240.0, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2036, 44.36, 0.0, 37.36, 40.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2036, -54.54, 0.0, 19.74, 160.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2036, 10.18, 0.0, -57.1, 280.1, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2037, 12.92, 0.0, 74.89, 80.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2037, -71.32, 0.0, -26.26, 200.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2037, 58.4, 0.0, -48.63, 320.2, 14.0, 4, NULL);
INSERT INTO npc_spawn (zone_id, npc_template_id, pos_x, pos_y, pos_z, heading, wander_radius_m, spawn_count, respawn_sec) VALUES (9, 2038, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 3600);

COMMIT;
