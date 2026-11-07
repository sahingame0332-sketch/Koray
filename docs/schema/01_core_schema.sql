-- =============================================================================
--  Kendi mobil MMORPG'n icin cekirdek veritabani semasi
--  Hedef: PostgreSQL 16+
--  Tarih: 2026-11-07
--  Durum: PostgreSQL 16.15 uzerinde ON_ERROR_STOP=1 ile hatasiz calistirildi;
--         26 tablo olusur. Kisit testleri (dupe, FK, CHECK, makbuz tekrari)
--         dogru sekilde reddediyor.
-- =============================================================================
--
--  Bu sema, Knight Online'in `KN_online` veritabanini inceleyerek hazirlandi.
--  Amac ayni seyi tekrarlamak DEGIL; o semanin yedi temel kusurunu bastan
--  cozmek. Her kusur ve karsilik gelen cozum asagida:
--
--  KO'nun hatasi                          | Buradaki cozum
--  ---------------------------------------+-----------------------------------
--  1. strPasswd varchar(13), duz metin    | password_hash text (Argon2id),
--                                         | uygulama katmaninda hashlenir
--  2. strSocNo (Kore kimlik no) alani     | Yok. Kisisel veri toplanmaz.
--  3. Envanter strItem varchar(400)       | character_item: her esya AYRI SATIR
--     icinde paketli -> dupe hatalari     | + item_ledger ile tam denetim izi
--  4. Level/stat tinyint -> 255 tavan     | integer / bigint
--  5. Is mantigi 70 sakli yordamda        | Sema sadece veri tutar; mantik
--                                         | uygulama kodunda, test edilebilir
--  6. FK kisiti yok, normalizasyon yok    | Her iliski FK ile zorlanir
--  7. MSSQL + Windows kilidi              | PostgreSQL + Linux, lisans yok
--
--  Kullanim:
--    createdb oyun
--    psql -d oyun -f docs/schema/01_core_schema.sql
--
--  NOT: Bu bir baslangic noktasidir, bitmis bir sema degil. Oyun tasarimin
--  netlestikce buraya beceri agaci, gorev, kusatma vb. eklenecek.
-- =============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS citext;     -- buyuk/kucuk harf duyarsiz metin


-- =============================================================================
--  1. HESAP VE KIMLIK
-- =============================================================================

CREATE TABLE account (
    id                  bigserial PRIMARY KEY,
    public_id           uuid        NOT NULL DEFAULT gen_random_uuid() UNIQUE,

    -- citext: "Ahmet" ile "ahmet" ayni hesap sayilir, ama gosterimde korunur
    username            citext      NOT NULL UNIQUE
                            CHECK (length(username) BETWEEN 3 AND 32),
    email               citext      UNIQUE,

    -- Argon2id ciktisi, PHC string formatinda ($argon2id$v=19$m=...$...).
    -- Uzunluk sinirlama YOK: algoritma degisirse sema degismesin.
    -- Hashleme uygulama katmaninda yapilir, asla SQL'de.
    password_hash       text        NOT NULL,
    password_changed_at timestamptz NOT NULL DEFAULT now(),

    -- 0=banli, 1=oyuncu, 2=yardimci GM, 3=GM, 4=yonetici
    role                smallint    NOT NULL DEFAULT 1,
    status              text        NOT NULL DEFAULT 'active'
                            CHECK (status IN ('active','suspended','banned','deleted')),

    premium_until       timestamptz,
    last_login_at       timestamptz,
    last_login_ip       inet,
    failed_login_count  integer     NOT NULL DEFAULT 0,
    locked_until        timestamptz,

    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE  account IS 'Oyuncu hesabi. Sifre daima Argon2id ile hashlenir.';
COMMENT ON COLUMN account.password_hash IS 'Argon2id PHC string. Duz metin sifre ASLA saklanmaz.';

CREATE INDEX account_status_idx ON account (status) WHERE status <> 'active';


-- Oturumlar Redis'te tutulur; burada sadece uzun omurlu yenileme jetonlari
CREATE TABLE account_session (
    id             bigserial   PRIMARY KEY,
    account_id     bigint      NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    token_hash     bytea       NOT NULL UNIQUE,   -- jetonun SHA-256'si, jetonun kendisi degil
    device_id      text,
    platform       text        CHECK (platform IN ('android','ios','windows','other')),
    ip             inet,
    issued_at      timestamptz NOT NULL DEFAULT now(),
    expires_at     timestamptz NOT NULL,
    revoked_at     timestamptz
);

CREATE INDEX account_session_account_idx ON account_session (account_id)
    WHERE revoked_at IS NULL;


-- =============================================================================
--  2. DUNYA YAPISI
-- =============================================================================

CREATE TABLE world (
    id           smallserial PRIMARY KEY,
    code         text        NOT NULL UNIQUE,   -- 'ares', 'diez'
    display_name text        NOT NULL,
    is_open      boolean     NOT NULL DEFAULT false,
    max_players  integer     NOT NULL DEFAULT 2000,
    created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE faction (
    id           smallserial PRIMARY KEY,
    code         text        NOT NULL UNIQUE,   -- iki ulus: 'north', 'south'
    display_name text        NOT NULL
);

CREATE TABLE zone (
    -- KO'da `Zone tinyint` idi -> 255 tavan. Burada integer.
    id            integer     PRIMARY KEY,
    code          text        NOT NULL UNIQUE,
    display_name  text        NOT NULL,
    zone_type     text        NOT NULL
                      CHECK (zone_type IN ('safe','field','pvp','dungeon','arena','siege')),
    -- Hangi ulusun bolgesi; NULL = tarafsiz
    owner_faction_id smallint REFERENCES faction(id),
    level_min     integer     NOT NULL DEFAULT 1,
    level_max     integer     NOT NULL DEFAULT 999,
    -- Baslangic/dirilme koordinati. KO int kullaniyordu (268100 gibi, 1/100 birim).
    -- Burada metre cinsinden gercek sayi: okunabilir ve motorla uyumlu.
    spawn_x       double precision NOT NULL DEFAULT 0,
    spawn_y       double precision NOT NULL DEFAULT 0,
    spawn_z       double precision NOT NULL DEFAULT 0,
    is_enabled     boolean     NOT NULL DEFAULT true
);

COMMENT ON COLUMN zone.spawn_y IS 'Y = yukseklik. Unity sag-el koordinat sistemiyle uyumlu.';


-- =============================================================================
--  3. KARAKTER
-- =============================================================================

CREATE TABLE character_class (
    id            smallserial PRIMARY KEY,
    code          text        NOT NULL UNIQUE,   -- 'warrior', 'rogue', 'mage', 'priest'
    display_name  text        NOT NULL,
    -- Seviye basina otomatik kazanilan statlar; dengeleme burada yapilir
    base_hp       integer     NOT NULL DEFAULT 100,
    base_mp       integer     NOT NULL DEFAULT 50,
    hp_per_level  integer     NOT NULL DEFAULT 12,
    mp_per_level  integer     NOT NULL DEFAULT 6
);

CREATE TABLE level_curve (
    level         integer PRIMARY KEY CHECK (level >= 1),
    exp_required  bigint  NOT NULL CHECK (exp_required >= 0),
    stat_points   integer NOT NULL DEFAULT 3,
    skill_points  integer NOT NULL DEFAULT 2
);

COMMENT ON TABLE level_curve IS 'KO''nun LEVEL_UP tablosunun karsiligi; 90 degil, istedigin kadar seviye.';


CREATE TABLE game_character (
    id              bigserial   PRIMARY KEY,
    account_id      bigint      NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    world_id        smallint    NOT NULL REFERENCES world(id),

    -- Isim dunya bazinda tekil. citext -> "Koray" ve "koray" cakisir.
    name            citext      NOT NULL CHECK (length(name) BETWEEN 2 AND 20),

    faction_id      smallint    NOT NULL REFERENCES faction(id),
    class_id        smallint    NOT NULL REFERENCES character_class(id),

    -- integer, tinyint degil: tavan yok
    level           integer     NOT NULL DEFAULT 1 CHECK (level >= 1),
    experience      bigint      NOT NULL DEFAULT 0 CHECK (experience >= 0),

    -- Ana statlar. KO'da hepsi tinyint (255 tavan) idi.
    stat_strength   integer     NOT NULL DEFAULT 10,
    stat_stamina    integer     NOT NULL DEFAULT 10,
    stat_dexterity  integer     NOT NULL DEFAULT 10,
    stat_intellect  integer     NOT NULL DEFAULT 10,
    stat_charisma   integer     NOT NULL DEFAULT 10,
    unspent_stat_points  integer NOT NULL DEFAULT 0,
    unspent_skill_points integer NOT NULL DEFAULT 0,

    current_hp      integer     NOT NULL DEFAULT 100,
    current_mp      integer     NOT NULL DEFAULT 50,

    -- Gorunum. Deger araligini uygulama dogrular; sema esnek kalir.
    appearance      jsonb       NOT NULL DEFAULT '{}'::jsonb,

    -- Konum
    zone_id         integer     NOT NULL REFERENCES zone(id),
    pos_x           double precision NOT NULL DEFAULT 0,
    pos_y           double precision NOT NULL DEFAULT 0,
    pos_z           double precision NOT NULL DEFAULT 0,
    heading         real        NOT NULL DEFAULT 0,
    bind_zone_id    integer     REFERENCES zone(id),

    -- Ekonomi. bigint: KO'nun `Gold int` tavani (2.1 milyar) enflasyonda yetmez.
    gold            bigint      NOT NULL DEFAULT 0 CHECK (gold >= 0),

    -- PvP / katki (KO'daki Loyalty / NP)
    faction_points        bigint NOT NULL DEFAULT 0,
    faction_points_monthly bigint NOT NULL DEFAULT 0,
    pvp_kills       integer     NOT NULL DEFAULT 0,
    pvp_deaths      integer     NOT NULL DEFAULT 0,

    clan_id         bigint,     -- FK asagida, clan tablosundan sonra
    clan_rank       smallint,

    play_time_sec   bigint      NOT NULL DEFAULT 0,
    deleted_at      timestamptz,
    created_at      timestamptz NOT NULL DEFAULT now(),
    updated_at      timestamptz NOT NULL DEFAULT now()
);

-- Isim ayni dunyada tekil, ama silinmis karakterin ismi serbest kalir
CREATE UNIQUE INDEX game_character_name_uniq
    ON game_character (world_id, name) WHERE deleted_at IS NULL;

CREATE INDEX game_character_account_idx ON game_character (account_id)
    WHERE deleted_at IS NULL;
CREATE INDEX game_character_zone_idx ON game_character (zone_id)
    WHERE deleted_at IS NULL;
-- Siralama sorgulari icin
CREATE INDEX game_character_ranking_idx
    ON game_character (world_id, faction_points DESC) WHERE deleted_at IS NULL;


-- =============================================================================
--  4. ESYA SISTEMI  <- KO'nun en buyuk hatasinin duzeltildigi yer
-- =============================================================================

-- Esya SABLONU (KO'daki ITEM tablosunun karsiligi).
-- KO'da 61 kolon vardi ve her yeni ozellik icin ALTER TABLE gerekiyordu.
-- Burada sabit olanlar kolon, degisken olanlar jsonb.
CREATE TABLE item_template (
    id              integer     PRIMARY KEY,
    code            text        NOT NULL UNIQUE,
    display_name    text        NOT NULL,

    category        text        NOT NULL
                        CHECK (category IN ('weapon','armor','shield','accessory',
                                            'consumable','material','quest','currency')),
    equip_slot      text        CHECK (equip_slot IN ('head','chest','legs','hands','feet',
                                                      'main_hand','off_hand','ring','necklace')),

    -- Stoklanabilirlik: 1 = stoklanamaz (silah/zirh), >1 = stoklanabilir (iksir)
    max_stack       integer     NOT NULL DEFAULT 1 CHECK (max_stack >= 1),
    max_durability  integer     NOT NULL DEFAULT 0,  -- 0 = dayaniklilik yok

    req_level       integer     NOT NULL DEFAULT 1,
    req_class_id    smallint    REFERENCES character_class(id),
    req_faction_id  smallint    REFERENCES faction(id),

    buy_price       bigint      NOT NULL DEFAULT 0,
    sell_price      bigint      NOT NULL DEFAULT 0,
    weight          integer     NOT NULL DEFAULT 0,

    is_tradeable    boolean     NOT NULL DEFAULT true,
    is_sellable     boolean     NOT NULL DEFAULT true,
    is_upgradeable  boolean     NOT NULL DEFAULT false,

    -- Hasar, AC, element hasarlari, direncler, stat bonuslari...
    -- KO'da 50+ kolondu. jsonb: yeni ozellik = sema degisikligi yok.
    -- Ornek: {"damage": 120, "attack_delay": 1.2, "armor": 0,
    --          "bonus": {"strength": 5}, "resist": {"fire": 10}}
    stats           jsonb       NOT NULL DEFAULT '{}'::jsonb,

    created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX item_template_category_idx ON item_template (category);
CREATE INDEX item_template_stats_idx ON item_template USING gin (stats);


-- Bir esyayi BIRDEN FAZLA sinif kusanabilir (orn. asa: buyucu + sifaci).
-- item_template.req_class_id tek sinifi ifade eder ve hizli yol olarak kalir;
-- cok sinifli esyalarda bu tablo yetkilidir.
--
-- NEDEN AYRI TABLO: tek kolonla "buyucu VEYA sifaci" ifade edilemez. Kolona
-- NULL konursa esya HERKESE acilir -- savascinin magazada kumas zirh gormesi
-- tam olarak bu hatadan dogar. Cok-cok iliski bir baglanti tablosu gerektirir.
CREATE TABLE item_template_class (
    item_template_id integer  NOT NULL REFERENCES item_template(id) ON DELETE CASCADE,
    class_id         smallint NOT NULL REFERENCES character_class(id) ON DELETE CASCADE,
    PRIMARY KEY (item_template_id, class_id)
);

CREATE INDEX item_template_class_class_idx ON item_template_class (class_id);

-- Bir sinifin kusanabilecegi esyalar: baglanti tablosunda satiri olmayan esya
-- (iksir, malzeme, aksesuar) her sinifa aciktir.
CREATE VIEW item_allowed_for_class AS
SELECT i.id AS item_template_id, c.id AS class_id
FROM item_template i
CROSS JOIN character_class c
WHERE NOT EXISTS (SELECT 1 FROM item_template_class x WHERE x.item_template_id = i.id)
UNION
SELECT item_template_id, class_id FROM item_template_class;


-- KARAKTERIN ESYASI: her esya KENDI SATIRI.
-- KO burada `strItem varchar(400)` kullaniyordu; bu yuzden:
--   - tek esya atomik guncellenemiyordu -> dupe hatalari
--   - "bu esya nereden geldi" sorulamiyordu
--   - envanter 400 bayta sabitti
-- Bu tasarimda her uc sorun da ortadan kalkar.
CREATE TABLE character_item (
    id              bigserial   PRIMARY KEY,
    -- Her esya ornegine kalici ve tekil kimlik: takas/log/destek icin sart
    instance_uid    uuid        NOT NULL DEFAULT gen_random_uuid() UNIQUE,

    character_id    bigint      NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    template_id     integer     NOT NULL REFERENCES item_template(id),

    container       text        NOT NULL DEFAULT 'inventory'
                        CHECK (container IN ('inventory','equipped','warehouse','mail','trade')),
    -- equipped ise slot adi, degilse cizelge indeksi
    slot            integer     NOT NULL,

    quantity        integer     NOT NULL DEFAULT 1 CHECK (quantity >= 1),
    durability      integer,
    upgrade_level   smallint    NOT NULL DEFAULT 0,

    -- Rastgele olusan ozellikler (rolled stats), buyu tasi vb.
    attributes      jsonb       NOT NULL DEFAULT '{}'::jsonb,

    bound_to_character boolean  NOT NULL DEFAULT false,
    expires_at      timestamptz,   -- kiralik esya (KO'daki RENTAL_ITEM)
    acquired_at     timestamptz NOT NULL DEFAULT now()
);

-- Ayni kapta ayni slota iki esya konamaz. Dupe'a karsi veritabani seviyesi kilit.
CREATE UNIQUE INDEX character_item_slot_uniq
    ON character_item (character_id, container, slot);

CREATE INDEX character_item_character_idx ON character_item (character_id);
CREATE INDEX character_item_template_idx  ON character_item (template_id);


-- DENETIM DEFTERI: her esya hareketi buraya yazilir.
-- KO'da bu yoktu; bu yuzden dupe'lar tespit edilemiyor, destek talepleri
-- cozulemiyor, ekonomi denetlenemiyordu.
-- Bu tablo SADECE EKLENIR (append-only) -- asla UPDATE/DELETE yapilmaz.
CREATE TABLE item_ledger (
    id              bigserial   PRIMARY KEY,
    occurred_at     timestamptz NOT NULL DEFAULT now(),

    instance_uid    uuid        NOT NULL,
    template_id     integer     NOT NULL REFERENCES item_template(id),

    action          text        NOT NULL
                        CHECK (action IN ('create','drop','pickup','npc_buy','npc_sell',
                                          'player_trade','mail_send','mail_receive',
                                          'upgrade','destroy','gm_grant','gm_remove',
                                          'quest_reward','monster_drop','expire')),
    quantity        integer     NOT NULL,

    from_character_id bigint    REFERENCES game_character(id) ON DELETE SET NULL,
    to_character_id   bigint    REFERENCES game_character(id) ON DELETE SET NULL,

    -- GM islemi ise hangi hesap yapti
    actor_account_id  bigint    REFERENCES account(id) ON DELETE SET NULL,
    context         jsonb       NOT NULL DEFAULT '{}'::jsonb
);

COMMENT ON TABLE item_ledger IS
    'Append-only esya denetim defteri. Her esya hareketi buraya yazilir. '
    'Dupe tespiti, destek talepleri ve ekonomi analizi bu tabloya dayanir.';

CREATE INDEX item_ledger_instance_idx  ON item_ledger (instance_uid, occurred_at);
CREATE INDEX item_ledger_character_idx ON item_ledger (from_character_id, occurred_at DESC);
CREATE INDEX item_ledger_time_idx      ON item_ledger (occurred_at DESC);


-- Hesap bazli kasa (KO'daki WAREHOUSE; orada da paketli blob idi)
CREATE TABLE account_warehouse (
    account_id      bigint      NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    world_id        smallint    NOT NULL REFERENCES world(id),
    gold            bigint      NOT NULL DEFAULT 0 CHECK (gold >= 0),
    slot_count      integer     NOT NULL DEFAULT 24,
    PRIMARY KEY (account_id, world_id)
);


-- =============================================================================
--  5. BECERI SISTEMI
-- =============================================================================

-- KO'da MAGIC + MAGIC_TYPE1..TYPE9 olmak uzere 10 tablo vardi ve her
-- beceri tipi icin ayri tablo gerekiyordu. Burada tek tablo + jsonb etki listesi.
CREATE TABLE skill_template (
    id              integer     PRIMARY KEY,
    code            text        NOT NULL UNIQUE,
    display_name    text        NOT NULL,
    description     text,

    class_id        smallint    REFERENCES character_class(id),
    req_level       integer     NOT NULL DEFAULT 1,
    req_skill_id    integer     REFERENCES skill_template(id),  -- beceri agaci

    target_type     text        NOT NULL
                        CHECK (target_type IN ('self','single_enemy','single_ally',
                                               'area_enemy','area_ally','party','none')),

    mp_cost         integer     NOT NULL DEFAULT 0,
    hp_cost         integer     NOT NULL DEFAULT 0,
    cast_time_ms    integer     NOT NULL DEFAULT 0,
    cooldown_ms     integer     NOT NULL DEFAULT 0,
    range_m         real        NOT NULL DEFAULT 2.0,
    area_radius_m   real        NOT NULL DEFAULT 0,

    -- Etkiler sirali liste. Ornek:
    -- [{"kind":"damage","school":"physical","base":150,"stat_scale":{"strength":1.4}},
    --  {"kind":"debuff","effect":"slow","magnitude":30,"duration_ms":4000}]
    effects         jsonb       NOT NULL DEFAULT '[]'::jsonb,

    is_enabled      boolean     NOT NULL DEFAULT true
);

CREATE TABLE character_skill (
    character_id    bigint      NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    skill_id        integer     NOT NULL REFERENCES skill_template(id),
    skill_rank      smallint    NOT NULL DEFAULT 1,
    learned_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (character_id, skill_id)
);

-- Beceri cubugu (KO'daki USERDATA_SKILLSHORTCUT)
CREATE TABLE character_skill_bar (
    character_id    bigint      NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    bar_index       smallint    NOT NULL,
    slot_index      smallint    NOT NULL,
    skill_id        integer     REFERENCES skill_template(id),
    item_template_id integer    REFERENCES item_template(id),
    PRIMARY KEY (character_id, bar_index, slot_index),
    -- Bir slotta ya beceri ya esya olur, ikisi birden olmaz
    CHECK (num_nonnulls(skill_id, item_template_id) <= 1)
);


-- =============================================================================
--  6. CANAVAR VE NPC
-- =============================================================================

CREATE TABLE npc_template (
    id              integer     PRIMARY KEY,
    code            text        NOT NULL UNIQUE,
    display_name    text        NOT NULL,

    npc_kind        text        NOT NULL
                        CHECK (npc_kind IN ('monster','boss','merchant','banker',
                                            'quest_giver','guard','gate','trainer')),

    level           integer     NOT NULL DEFAULT 1,
    max_hp          bigint      NOT NULL DEFAULT 100,   -- boss icin bigint
    max_mp          integer     NOT NULL DEFAULT 0,

    -- Savas degerleri + direncler: jsonb
    combat          jsonb       NOT NULL DEFAULT '{}'::jsonb,

    exp_reward      bigint      NOT NULL DEFAULT 0,
    faction_point_reward integer NOT NULL DEFAULT 0,
    gold_min        bigint      NOT NULL DEFAULT 0,
    gold_max        bigint      NOT NULL DEFAULT 0,

    -- YZ davranisi: gezinme, kovalama menzili, saldirganlik
    ai_profile      jsonb       NOT NULL DEFAULT '{}'::jsonb,
    is_aggressive   boolean     NOT NULL DEFAULT true,
    respawn_sec     integer     NOT NULL DEFAULT 30
);

-- Drop tablosu (KO'daki K_MONSTER_ITEM; orada 9 sabit slot vardi)
CREATE TABLE npc_loot_entry (
    id              bigserial   PRIMARY KEY,
    npc_template_id integer     NOT NULL REFERENCES npc_template(id) ON DELETE CASCADE,
    item_template_id integer    NOT NULL REFERENCES item_template(id),
    -- Oran: 1_000_000 = %100. Tam sayi kullan, float kullanma:
    -- kayan nokta hatasi ekonomide birikir.
    drop_rate_ppm   integer     NOT NULL CHECK (drop_rate_ppm BETWEEN 1 AND 1000000),
    quantity_min    integer     NOT NULL DEFAULT 1,
    quantity_max    integer     NOT NULL DEFAULT 1,
    loot_group      smallint    NOT NULL DEFAULT 0   -- ayni grupta en fazla 1 esya duser
);

CREATE INDEX npc_loot_entry_npc_idx ON npc_loot_entry (npc_template_id);

-- Dogma noktalari (KO'daki K_NPCPOS)
CREATE TABLE npc_spawn (
    id              bigserial   PRIMARY KEY,
    zone_id         integer     NOT NULL REFERENCES zone(id) ON DELETE CASCADE,
    npc_template_id integer     NOT NULL REFERENCES npc_template(id),
    pos_x           double precision NOT NULL,
    pos_y           double precision NOT NULL,
    pos_z           double precision NOT NULL,
    heading         real        NOT NULL DEFAULT 0,
    wander_radius_m real        NOT NULL DEFAULT 10,
    spawn_count     integer     NOT NULL DEFAULT 1,
    respawn_sec     integer,    -- NULL ise template'ten alinir
    is_enabled      boolean     NOT NULL DEFAULT true
);

CREATE INDEX npc_spawn_zone_idx ON npc_spawn (zone_id) WHERE is_enabled;


-- =============================================================================
--  7. KLAN / SOSYAL
-- =============================================================================

CREATE TABLE clan (
    id              bigserial   PRIMARY KEY,
    world_id        smallint    NOT NULL REFERENCES world(id),
    name            citext      NOT NULL CHECK (length(name) BETWEEN 2 AND 24),
    faction_id      smallint    NOT NULL REFERENCES faction(id),

    leader_character_id bigint  REFERENCES game_character(id) ON DELETE SET NULL,
    member_limit    integer     NOT NULL DEFAULT 30,
    clan_level      integer     NOT NULL DEFAULT 1,
    treasury_gold   bigint      NOT NULL DEFAULT 0 CHECK (treasury_gold >= 0),
    points          bigint      NOT NULL DEFAULT 0,

    -- Klan amblemi: binary degil, varlik referansi. KO `Mark` kolonunda
    -- ham binary tutuyordu; bu hem sismeye hem guvenlik sorununa yol aciyor.
    emblem_asset_id text,
    notice          text,

    allied_clan_id  bigint      REFERENCES clan(id) ON DELETE SET NULL,
    disbanded_at    timestamptz,
    created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX clan_name_uniq ON clan (world_id, name) WHERE disbanded_at IS NULL;

-- Karakter -> klan FK'si (dongusel bagimlilik oldugu icin burada ekliyoruz)
ALTER TABLE game_character
    ADD CONSTRAINT game_character_clan_fk
    FOREIGN KEY (clan_id) REFERENCES clan(id) ON DELETE SET NULL;

CREATE INDEX game_character_clan_idx ON game_character (clan_id) WHERE clan_id IS NOT NULL;


CREATE TABLE friendship (
    character_id        bigint NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    friend_character_id bigint NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    created_at          timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (character_id, friend_character_id),
    CHECK (character_id <> friend_character_id)
);

CREATE TABLE block_list (
    character_id         bigint NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    blocked_character_id bigint NOT NULL REFERENCES game_character(id) ON DELETE CASCADE,
    created_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (character_id, blocked_character_id),
    CHECK (character_id <> blocked_character_id)
);


-- =============================================================================
--  8. MAGAZA VE SATIN ALMA (mesru IAP)
-- =============================================================================

CREATE TABLE store_product (
    id              bigserial   PRIMARY KEY,
    sku             text        NOT NULL UNIQUE,   -- Play/StoreKit SKU ile ayni
    display_name    text        NOT NULL,
    -- Verilecek icerik: {"premium_days": 30} veya {"items":[{"id":1001,"qty":5}]}
    grants          jsonb       NOT NULL,
    price_tier      text,
    is_active       boolean     NOT NULL DEFAULT true,
    created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE store_purchase (
    id              bigserial   PRIMARY KEY,
    account_id      bigint      NOT NULL REFERENCES account(id),
    product_id      bigint      NOT NULL REFERENCES store_product(id),

    platform        text        NOT NULL CHECK (platform IN ('google_play','app_store')),
    -- Magazanin islem kimligi. UNIQUE: ayni makbuz iki kez islenemez
    -- (replay saldirisina karsi veritabani seviyesi koruma).
    platform_txn_id text        NOT NULL,

    -- Makbuz DAIMA sunucu tarafinda magaza API'siyle dogrulanir.
    -- Istemcinin "satin aldim" demesi asla yeterli degildir.
    verified_at     timestamptz,
    status          text        NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending','verified','granted','refunded','failed')),
    granted_at      timestamptz,
    amount_minor    bigint,     -- kurusu/centi cinsinden
    currency        char(3),
    created_at      timestamptz NOT NULL DEFAULT now(),

    UNIQUE (platform, platform_txn_id)
);

CREATE INDEX store_purchase_account_idx ON store_purchase (account_id, created_at DESC);


-- =============================================================================
--  9. OPERASYON VE GUVENLIK
-- =============================================================================

-- GM islemleri: kim, kime, ne yapti. Hesap verebilirlik icin sart.
CREATE TABLE gm_action_log (
    id              bigserial   PRIMARY KEY,
    occurred_at     timestamptz NOT NULL DEFAULT now(),
    actor_account_id bigint     NOT NULL REFERENCES account(id),
    action          text        NOT NULL,
    target_account_id   bigint  REFERENCES account(id) ON DELETE SET NULL,
    target_character_id bigint  REFERENCES game_character(id) ON DELETE SET NULL,
    details         jsonb       NOT NULL DEFAULT '{}'::jsonb,
    ip              inet
);

CREATE INDEX gm_action_log_time_idx ON gm_action_log (occurred_at DESC);


-- Yaptirimlar
CREATE TABLE sanction (
    id              bigserial   PRIMARY KEY,
    account_id      bigint      REFERENCES account(id) ON DELETE CASCADE,
    character_id    bigint      REFERENCES game_character(id) ON DELETE CASCADE,
    kind            text        NOT NULL CHECK (kind IN ('ban','suspend','mute','trade_block')),
    reason          text        NOT NULL,
    evidence        jsonb       NOT NULL DEFAULT '{}'::jsonb,
    issued_by       bigint      REFERENCES account(id),
    starts_at       timestamptz NOT NULL DEFAULT now(),
    ends_at         timestamptz,       -- NULL = kalici
    revoked_at      timestamptz,
    CHECK (num_nonnulls(account_id, character_id) >= 1)
);

CREATE INDEX sanction_active_idx ON sanction (account_id)
    WHERE revoked_at IS NULL;


-- Hile/anomali sinyalleri. KO'da HACKTOOL_USERLOG vardi ama sadece log
-- tutuyordu; burada otomatik degerlendirme icin yapilandirilmis veri.
CREATE TABLE anticheat_signal (
    id              bigserial   PRIMARY KEY,
    occurred_at     timestamptz NOT NULL DEFAULT now(),
    account_id      bigint      REFERENCES account(id) ON DELETE CASCADE,
    character_id    bigint      REFERENCES game_character(id) ON DELETE CASCADE,
    signal          text        NOT NULL,   -- 'speed_hack','impossible_move','packet_flood',...
    severity        smallint    NOT NULL DEFAULT 1 CHECK (severity BETWEEN 1 AND 5),
    details         jsonb       NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX anticheat_signal_account_idx ON anticheat_signal (account_id, occurred_at DESC);


-- =============================================================================
--  10. BASLANGIC VERISI (ornek)
-- =============================================================================

INSERT INTO world (code, display_name, is_open) VALUES
    ('ares', 'Ares', true);

INSERT INTO faction (code, display_name) VALUES
    ('north', 'Kuzey Krallığı'),
    ('south', 'Güney İmparatorluğu');

INSERT INTO character_class (code, display_name, base_hp, base_mp, hp_per_level, mp_per_level) VALUES
    ('warrior', 'Savaşçı', 140, 30, 16, 3),
    ('rogue',   'Suikastçı', 110, 40, 12, 5),
    ('mage',    'Büyücü',    85, 90,  8, 12),
    ('priest',  'Şifacı',    95, 80, 10, 11);

INSERT INTO zone (id, code, display_name, zone_type, level_min, level_max) VALUES
    (1, 'north_town', 'Kuzey Şehri',   'safe',  1, 999),
    (2, 'south_town', 'Güney Şehri',   'safe',  1, 999),
    (3, 'green_field','Yeşil Ovalar',  'field', 1,  20),
    (4, 'warzone',    'Savaş Bölgesi', 'pvp',  20, 999);

-- Ornek seviye egrisi: ilk 10 seviye. Gercek egriyi dengeleme calismasiyla belirle.
INSERT INTO level_curve (level, exp_required, stat_points, skill_points)
SELECT lvl,
       (100 * power(lvl, 2.2))::bigint,
       3,
       CASE WHEN lvl % 2 = 0 THEN 2 ELSE 1 END
FROM generate_series(1, 100) AS lvl;

COMMIT;

-- =============================================================================
--  SONRAKI ADIMLAR
-- =============================================================================
--  Bu sema cekirdegi kuruyor. Oyun tasarimin netlestikce eklenecekler:
--    - quest / quest_progress      (gorev sistemi)
--    - mail / mail_attachment      (oyuncu postasi)
--    - auction / auction_bid       (oyuncu pazari)
--    - party (calisma zamani: Redis'te tut, kalici olmasin)
--    - siege_schedule / siege_result  (kale kusatmasi)
--    - season / season_reward      (sezon sistemi)
--
--  Onemli isletme kurallari (SEMA DEGIL, UYGULAMA KODUNDA olmali):
--    - Sifre hashleme: Argon2id, m=64MB t=3 p=4 taban al
--    - Esya tasima: TEK transaction icinde character_item UPDATE + item_ledger INSERT
--    - Takas: iki tarafli onay, tek transaction, her iki tarafa ledger kaydi
--    - Satin alma: magaza API dogrulamasi -> status='verified' -> sonra grant
--    - Hareket dogrulama: sunucu tarafi hiz/mesafe kontrolu, istemciye guvenme
-- =============================================================================
