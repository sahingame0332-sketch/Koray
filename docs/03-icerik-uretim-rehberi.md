# İçerik Üretim Hattı — Karakter, Item, Skill, Mob, Harita, Arayüz

> Tarih: 7 Kasım 2026

## 0. Bu dosya neden böyle

APK'dan içerik ve kaynak kodu çıkarmayı istedin. Onu yapmadım: başka bir
stüdyonun kodu ve sanat varlıkları, kullanıldığında telif ihlali olur
(ayrıntı: `02-apk-analizi.md` Bölüm 7.3).

Ama istediğin şeyin arkasındaki ihtiyaç tamamen meşru ve burada karşılanıyor:
**veri modeli, içerik formatı, dengeleme yöntemi ve dolu bir başlangıç içeriği.**
Oyun mekanikleri ve veri yapıları telif korumasında değildir — bu dosyadaki
bütün isimler, sayılar ve dengeleme bu proje için üretildi, **eseri senin.**

İki olgusal not, planını etkilediği için:

1. **Veritabanı ve sunucu kodu APK'da yok.** APK sadece istemcidir. Veritabanı
   `loginapi.mykomobile.com`'un arkasındaki sunucularda. Ne kadar uğraşılsa
   çıkmaz.
2. **İstemci kodu da çıkarılamaz.** IL2CPP, C#'ı native koda derler. Elde
   edilebilecek şey okunabilir C# değil, sembolleri kısmen kurtarılmış
   makine kodudur — üzerine inşa edilemez.

---

## 1. Ne üretildi

| Dosya | İçerik |
|---|---|
| `tools/generate_content.py` | İçerik üreteci — tek doğruluk kaynağı |
| `content/items.json` | **181** eşya |
| `content/skills.json` | **40** beceri (4 sınıf × 10, ağaç bağlantılı) |
| `content/npcs.json` | **44** NPC: 31 mob + 7 boss + 6 şehir NPC'si |
| `content/loot.json` | **242** loot satırı |
| `content/spawns.json` | **100** doğma noktası (419 eşzamanlı mob) |
| `content/zones.json` | **10** bölge |
| `content/balance_report.txt` | Otomatik dengeleme raporu |
| `docs/schema/02_content_seed.sql` | Yüklenebilir SQL (~210 KB) |

Kurulum:

```bash
python3 tools/generate_content.py          # içeriği üret
createdb oyun
psql -d oyun -f docs/schema/01_core_schema.sql
psql -d oyun -f docs/schema/02_content_seed.sql
```

**Doğrulandı:** PostgreSQL 16.15'te `ON_ERROR_STOP=1` ile yüklendi; ikinci kez
yüklendiğinde `ON CONFLICT` sayesinde kayıt sayısı değişmedi (idempotent).

---

## 2. Neden betik, neden elle yazılmış JSON değil

Bu, dosyanın en önemli fikri.

Bir MMORPG'nin içeriği yüzlerce kayıttır ve hepsi birbirine bağlıdır. Çelik
kademesinin hasarını %10 artırırsan, o kademeyi düşüren moblarının HP'si de
artmalı — yoksa oyun aniden kolaylaşır. Elle yazılan veride bu bağlar kopar ve
dengeleme bir daha asla toparlanmaz.

Burada içerik, betiğin en üstündeki **tasarım parametrelerinden formüllerle**
üretilir:

```python
TIERS = [
    ("baslangic", "Başlangıç",  1,  1.00,    1),
    ("demir",     "Demir",     10,  1.80,    6),
    ("celik",     "Çelik",     20,  3.20,   28),
    ...   # kod, ad, min_seviye, güç_çarpanı, fiyat_çarpanı
]

TARGET_TTK_SEC = 9.0    # normal mob kaç saniyede ölmeli
TARGET_TTD_SEC = 26.0   # tek mob, iyileşmeyen oyuncuyu kaç saniyede öldürmeli
```

Tek bir sayıyı değiştirip betiği yeniden çalıştırırsın; 181 eşya, 31 mob ve 242
loot satırı tutarlı şekilde yeniden üretilir. Bu, gerçek stüdyoların çalışma
biçimidir ve bir kişilik ekip için şart.

### Çıktının iki formatı neden var

- **JSON** — insan okur, `git diff` anlamlı olur, tasarım tartışması bunun üzerinden yapılır.
- **SQL** — veritabanına yüklenir, `ON CONFLICT ... DO UPDATE` ile tekrar yüklenebilir.

Sunucun içeriği veritabanından okur; JSON sadece yazarlık ve inceleme formatı.

---

## 3. Dengeleme yöntemi — asıl know-how burada

Mob istatistiklerini bağımsız bir formülle **yazmıyorum**. Beklenen oyuncu
gücünden **türetiyorum**:

```
beklenen_oyuncu_dps(seviye)  = o seviyedeki silah DPS'i (kademeler arası
                               doğrusal geçişle) × beceri katkısı (1.35)

mob_hp    = beklenen_oyuncu_dps × TARGET_TTK_SEC × arketip_çarpanı
mob_hasar = (beklenen_oyuncu_ehp / TARGET_TTD_SEC) × arketip_çarpanı
```

Kademeler arasında **doğrusal geçiş** kritik: aksi halde oyuncu seviye 20'de
Çelik silaha geçtiğinde gücü zıplar, moblar onunla zıplamadığı için oyun
birden kolaylaşır. İnterpolasyon bunu önler.

### Üretecin yakaladığı iki gerçek hata

Bu yöntem lafta kalmadı — rapor ilk çalıştırmada iki sorun yakaladı:

| Sorun | Sebep | Çözüm |
|---|---|---|
| Seviye 1 mob 2.1 saniyede ölüyordu | HP bağımsız karesel formülle hesaplanıyordu | HP, beklenen oyuncu DPS'inden türetildi |
| Seviye 40 golem 44 saniye sürüyordu | Arketip HP çarpanı 2.2 çok yüksekti | 1.55'e indirildi |

Düzeltme sonrası tablo:

```
  sv   mob                      HP      TTK     TTD   durum
    1  Yeşil Kurt                 240    7.7s   25.4s   ok
   20  Kuru Haydut                904    9.0s   26.1s   ok
   40  Gölge Golem               3020   14.0s   20.0s   ok
   75  Buz Golem                 7423   13.9s   20.0s   ok
   95  Ejder Haydut              5874    9.0s   26.0s   ok

  Sorunlu mob sayısı: 0
```

TTK 6.7–14 sn, TTD 20–26 sn bandında. Boss'lar 5 kişilik partiyle ~25 sn,
tek başına ~126 sn — yani parti gerektiriyor, tasarım niyeti bu.

**Bunu her içerik değişikliğinden sonra çalıştır.** `content/balance_report.txt`
sorunlu mob listesi veriyorsa yayına çıkarmadan düzelt.

---

## 4. İçerik türleri

### 4.1 Karakterler (sınıf ve ırk)

`01_core_schema.sql`'de 4 sınıf var: Savaşçı, Suikastçı, Büyücü, Şifacı.
Her sınıfın taban HP/MP'si ve seviye başına artışı `character_class`
tablosunda — dengelemeyi oradan yaparsın.

**Irk isimlendirmesi konusunda somut tavsiye:** `02-apk-analizi.md`'de
gördüğümüz gibi, Nowa Games ırkları **Orc/Human** gibi jenerik adlarla
kurup App Store'a girdi; MykoMobile aynı kodun üzerine `KARUS_*`/`ELMORAD_*`
ekleyip mağaza dışında kaldı. **Jenerik veya kendi uydurduğun isimleri kullan.**
Şemada uluslar `north`/`south` (Kuzey Krallığı / Güney İmparatorluğu) — bunları
istediğin gibi değiştir, ama Knight Online'ın isimlerine dokunma.

### 4.2 Eşyalar — 181 kayıt

| Kategori | Sayı | Nasıl üretildi |
|---|---|---|
| Zırh | 90 | 3 aile (Plaka/Deri/Kumaş) × 5 slot × 6 kademe |
| Aksesuar | 40 | 2 tip × 4 stat × 5 kademe |
| Silah | 36 | 6 arketip (Kılıç/Balta/Topuz/Hançer/Yay/Asa) × 6 kademe |
| Tüketilebilir | 8 | Şifa/mana iksirleri, şehir taşı, tamir kiti |
| Malzeme | 7 | Upgrade ve üretim için |

Zırh koruması slot paylarıyla dağıtılır (göğüs %34, pantolon %24, başlık %16,
bot %14, eldiven %12 — toplamı 1.0). Yani bir setin toplam koruması ailenin
taban değerine eşit; slot dağılımı tasarım kararı.

Silahlarda `dps` alanı hesaplanıp saklanır — dengeleme kontrolü bunun üzerinden
yapılır. Kademe içinde silahlar arası fark **%60** (hızlı/düşük hasar ↔
yavaş/yüksek hasar), kademeler arası sıçrama **~1.8×**.

#### Çok sınıflı eşya — şemada düzelttiğim gerçek bir hata

İlk testte seviye 20 savaşçı **kumaş zırhı** da gördü. Sebep: `req_class_id`
tek sınıf tutuyor; asa gibi "büyücü **veya** şifacı" eşyalarında `NULL` kalıp
eşya herkese açılıyordu.

Çözüm, `01_core_schema.sql`'e eklenen `item_template_class` bağlantı tablosu ve
`item_allowed_for_class` görünümü. Bağlantı satırı olmayan eşya (iksir,
malzeme, aksesuar) her sınıfa açık kalır. Doğrulandı:

```
   sınıf   | asa | kumaş | plaka
-----------+-----+-------+-------
 Savaşçı   |   0 |     0 |    30
 Suikastçı |   0 |     0 |     0
 Büyücü    |   6 |    30 |     0
 Şifacı    |   6 |    30 |     0
```

Mağaza ve kuşanma sorgularını `item_allowed_for_class` üzerinden yaz, ham
`req_class_id` üzerinden değil.

### 4.3 Beceriler — 40 kayıt

Sınıf başına 10 beceri, seviye 2'den 82'ye. `req_skill_id` ile zincir
oluşturuyor — yani beceri ağacı. Savaşçı örneği:

```
 sv | beceri        | önkoşul       | MP  | bekleme
----+---------------+---------------+-----+---------
  2 | Sert Vuruş    |               |  12 |   4 sn
  8 | Kalkan Duvarı | Sert Vuruş    |  20 |  30 sn
 14 | Yarma         | Kalkan Duvarı |  28 |  10 sn
 ...
 82 | Savaş Tanrısı | İnfaz         | 100 | 300 sn
```

Etkiler `effects` jsonb alanında **sıralı liste** olarak tutulur. Böylece tek
bir beceri hem hasar hem debuff verebilir, ve yeni etki tipi eklemek şema
değişikliği gerektirmez:

```json
[{"kind": "damage", "school": "physical", "base": 214, "weapon_scale": 1.35},
 {"kind": "debuff", "attribute": "armor", "magnitude_pct": -15, "duration_ms": 10000}]
```

> Knight Online bunu `MAGIC` + `MAGIC_TYPE1..TYPE9` olmak üzere **10 ayrı
> tabloyla** yapıyordu ve her yeni beceri tipi yeni tablo gerektiriyordu
> (bkz. `01-mykomobile-altyapi-analizi.md` Bölüm 3.3). Tek tablo + jsonb
> çok daha esnek.

Desteklenen etki tipleri: `damage`, `damage_over_time`, `heal`, `buff`,
`debuff`, `control`, `threat`, `movement`, `stealth`, `cleanse`, `revive`.
Sunucu tarafında bunları yorumlayan bir etki motoru yazacaksın — becerinin
mantığı kodda değil, veride olur. Yeni beceri eklemek kod değişikliği
gerektirmez.

### 4.4 Moblar ve loot — 44 NPC, 242 loot satırı

6 arketip (Kurt, Örümcek, Haydut, Golem, Hortlak, Harpi), her biri HP/hasar
çarpanı, hız ve davranış ailesiyle. `ai_profile` alanı YZ davranışını taşır:

```json
{"family": "element", "move_speed": 2.1, "aggro_radius_m": 0,
 "chase_radius_m": 25, "leash_radius_m": 35, "wander": true}
```

`aggro_radius_m: 0` = saldırgan değil (golem). `leash_radius_m` = mobun doğma
noktasından en fazla ne kadar uzaklaşacağı — bu olmadan oyuncular mobları
şehre çeker.

**Loot grupları** önemli bir detay: `loot_group 0` bağımsız düşer (malzeme %32,
iksir %15), `loot_group 1`'den **en fazla bir eşya** düşer (ekipman, %0.4–0.9).
Bu, "aynı mobdan aynı anda 4 silah düşmesi" sorununu baştan engeller.

Boss'lar ayrı: HP normal mobun 14 katı, `enrage_below_hp_pct` ve faz tanımları
var, 1 saat respawn, ekipman düşme oranı %14.

### 4.5 Haritalar — 10 bölge

| Bölge | Tip | Seviye | Mob çeşidi | Eşzamanlı mob |
|---|---|---|---|---|
| Kuzey Şehri | safe | — | 0 | — |
| Güney Şehri | safe | — | 0 | — |
| Yeşil Ovalar | field | 1–20 | 6 | 61 |
| Kuru Geçit | field | 10–30 | 6 | 61 |
| Savaş Bölgesi | pvp | 20+ | 5 | 49 |
| Gölge Ormanı | field | 25–45 | 6 | 61 |
| Yanık Tepeler | field | 40–65 | 6 | 61 |
| Buz Mağarası | dungeon | 55–85 | 5 | 49 |
| Ejder Yuvası | dungeon | 75+ | 4 | 37 |
| Arena | arena | 20+ | 0 | — |

Seviye bantları **kasıtlı olarak örtüşüyor** (1-20, 10-30, 25-45...): oyuncu
her zaman iki seçeneğe sahip olur, tek koridora sıkışmaz.

Doğma noktaları betikte dairesel dağılımla üretiliyor — bu bir **yer tutucu.**
Gerçek koordinatları Unity'de haritanı yaptıktan sonra bir editör aracıyla
alıp `content/spawns.json`'a yazacaksın. Üreteci o noktada
"koordinat üret" modundan "koordinatları JSON'dan oku" moduna çevirmek 20
satırlık bir değişiklik.

Şehir NPC'leri hazır: her güvenli bölgede Tüccar, Kasadar, Eğitmen.

---

## 5. Görsel arayüzler

Burada net olmam gerek: **sana hazır UI grafiği veremem** — ne APK'dan
çıkarabilirim (telif), ne de görsel üretebilirim. Ama verebileceğim iki şey
gerçekten işe yarar: **ekran envanteri** ve **veri sözleşmeleri.**

### 5.1 Ekran envanteri (mobil MMORPG için asgari set)

| # | Ekran | İçerik | Veri kaynağı |
|---|---|---|---|
| 1 | Giriş | kullanıcı adı, şifre, kayıt, şifremi unuttum | `POST /auth/login` |
| 2 | Sunucu seçimi | dünya listesi, doluluk, ping | `GET /worlds` |
| 3 | Karakter seçimi | 3 slot, önizleme, sil/oluştur | `account_char`, `game_character` |
| 4 | Karakter oluşturma | ulus, sınıf, görünüm, isim kontrolü | `faction`, `character_class` |
| 5 | **HUD** | HP/MP barı, beceri çubuğu, mini harita, sohbet, hedef çerçevesi | canlı paketler |
| 6 | Envanter | ızgara + kuşanma slotları + ağırlık + altın | `character_item` |
| 7 | Karakter paneli | statlar, dağıtılmamış puan, toplam hasar/koruma | `game_character` |
| 8 | Beceri paneli | ağaç görünümü, önkoşul oku, puan dağıtma | `skill_template`, `character_skill` |
| 9 | NPC mağazası | satılık liste, satın al/sat, onay | `item_allowed_for_class` |
| 10 | Kasa | hesap bazlı depo, altın transferi | `account_warehouse` |
| 11 | Parti | üye listesi, HP barları, davet | canlı |
| 12 | Klan | üye, rütbe, hazine, duyuru | `clan`, `character.clan_id` |
| 13 | Sohbet | sekmeler: genel/parti/klan/özel | canlı |
| 14 | Takas | iki taraflı onay, kilit | canlı + `item_ledger` |
| 15 | Sıralamalar | NP, seviye, klan | Redis sorted set |
| 16 | Mağaza (IAP) | paketler, satın alma, makbuz | `store_product`, `store_purchase` |
| 17 | Ayarlar | grafik kalitesi, ses, kontrol, dil | yerel |
| 18 | Yama/indirme | AssetBundle indirme ilerlemesi | CDN |

18 ekran. Bir kişi için 2–3 ay iş; bu yüzden Faz 1'de sadece **1, 3, 4, 5, 6**
yap, gerisi sonra.

### 5.2 Dokunmatik HUD için somut kurallar

MykoMobile'ın sistem gereksinimleri (Android 7.0, 4 GB RAM) ve dikey/yatay
desteği, hedef cihaz sınıfını gösteriyor. Mobil MMORPG HUD'u için:

- **Dokunma hedefi en az 44×44 dp.** Beceri butonları daha küçükse oyuncu
  savaşta ıskalar.
- **Sol alt: hareket joystick'i. Sağ alt: beceri çubuğu.** Başparmakların
  doğal konumu. Önemli bilgiyi (HP barı) parmakların kapattığı alt köşelere koyma.
- **Çentik (notch) güvenli alanı.** MykoMobile manifest'inde
  `android.notch_support` ve `notch.config` var — sen de `Screen.safeArea`
  kullan, yoksa UI çentiğin altında kalır.
- **Beceri çubuğu 2 satır × 5 slot** yeter; 40 becerinin hepsi aynı anda
  gerekmiyor.
- **Hedef çerçevesi üstte ortada**, kendi HP'n sol üstte.
- **Her şey ölçeklenebilir olsun:** Canvas Scaler → Scale With Screen Size,
  referans 1080×1920 (veya yatay için 1920×1080), Match Width Or Height 0.5.

### 5.3 Sanat varlıkları nereden gelir

Sana model/doku/ikon üretemem. Meşru kaynaklar:

| Kaynak | Ne için | Not |
|---|---|---|
| **Unity Asset Store** | karakter, çevre, UI kit, VFX | Lisansı oku: bazıları tek projeye özel |
| **Mixamo** (Adobe) | karakter animasyonu | Ücretsiz, ticari kullanıma açık |
| **Quaternius, Kenney** | düşük poligonlu modeller | CC0 — koşulsuz ticari kullanım |
| **Sketchfab / ArtStation** | tek tek varlıklar | Lisansı mutlaka kontrol et |
| **Freelance 3D sanatçı** | özgün karakter/set | 5.000–30.000 USD bandı (bkz. `01` Bölüm 8) |

MykoMobile'ın kullandığı eklentiler (`02-apk-analizi.md` Bölüm 2) iyi bir
alışveriş listesi: Odin Inspector, DOTween Pro, Cinemachine, TextMeshPro,
MagicaCloth, Toony Colors Pro, All In 1 VFX. Hepsi Asset Store'dan lisanslı
alınabilir — onların yaptığı gibi.

**Uyarı:** Bir "KO asset pack" veya "hazır MMO içerik paketi" satıcısı
çıkarsa, kaynağını sor. Knight Online'dan çıkarılmış varlıklar piyasada
dolaşıyor ve bunları kullanmak seni `02` Bölüm 7.3'teki riske sokar.

---

## 6. Üretece nasıl içerik eklersin

Yeni silah arketipi:

```python
WEAPONS = [
    ...
    ("mizrak", "Mızrak", "main_hand", 40, 1.60, 3.2, "strength", ["warrior"]),
]
```

Yeni kademe:

```python
TIERS = [
    ...
    ("mitril", "Mitril", 85, 24.00, 9000),
]
```

Yeni bölge:

```python
ZONES = [
    ...
    (11, "lav_cukuru", "Lav Çukuru", "dungeon", 85, 999, 4),
]
```

Her değişiklikten sonra:

```bash
python3 tools/generate_content.py          # içerik + denge raporu
cat content/balance_report.txt             # "Sorunlu mob sayısı: 0" olmalı
psql -d oyun -f docs/schema/02_content_seed.sql
```

Betik mevcut ID'leri korur (`ON CONFLICT DO UPDATE`), yani üretimdeki
oyuncuların eşyaları kaybolmaz — sadece tanımlar güncellenir.

---

## 7. Eksikler ve sıradaki adım

Bu hat şunları **henüz** üretmiyor:

- **Görevler (quest)** — şema da yok; `01` Bölüm 6.3'ün "sonraki adımlar" listesinde
- **Üretim/zanaat tarifleri** — malzemeler hazır, tarifler yok
- **Upgrade başarı oranları** — `kutsama_tasi` malzemesi var, oran tablosu yok
- **Klan kuşatma takvimi**
- **Gerçek harita koordinatları** — doğma noktaları yer tutucu
- **Yerelleştirme** — isimler şimdilik Türkçe gömülü; `locale` tablosuna taşınmalı

Sıradaki en mantıklı iş: **Faz 1 iskeleti** — Gateway + World Server + Unity
istemcisi, bu içeriği gerçekten okuyup iki oyuncunun birbirini görüp
vurabildiği çalışan bir dikey dilim. İçerik hazır olduğu için sunucu yazarken
"ne veri okuyacağım" sorusu kalmadı.
