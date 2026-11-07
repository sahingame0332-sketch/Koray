# Yeni pencereler: FRIENDS · CLAN · Ana menü · OPTIONS

Tarih: 7 Kasım 2026 · Kaynak: `referans_gorseller/1298_ekranlar/` (16 ekran görüntüsü, 2266 × 1488)

Kullanıcının gönderdiği 16 ekran görüntüsünde dört yeni pencere var. Bu belge ölçümleri ve
çıkarılan sprite'ları kayda geçirir. **Unity paketleri henüz yapılmadı** — kural gereği önce
görsel onayı bekleniyor.

## Ekran görüntüsü envanteri

| # | dosya | içerik |
|---|---|---|
| 01 | `01_17854d3e.png` | Character › **FRIENDS** sekmesi |
| 02 | `02_23b1fccc.png` | Character › **CLAN** sekmesi |
| 03 | `03_1f503aa5.png` | **Ana menü paneli** (POWER-UP-STORE … INSTAGRAM) |
| 04–14 | 11 dosya | **OPTIONS** penceresi, 11 alt sayfasının her biri |
| 15 | `15_0b7e6da6.png` | Char Info + stat butonları (ölçek referansı) |
| 16 | `16_8b120c1e.png` | Char Info + Save Stat Preset (ölçek referansı) |

## Ölçülen pencere kutuları (ekran koordinatı)

| pencere | x | y | boyut | zemin |
|---|---|---|---|---|
| Character (dört sekme ortak) | 303–1063 | 143–1348 | 760 × 1205 | **yarı saydam 0,92** |
| OPTIONS | 1018–1872 | 166–1337 | 854 × 1171 | **yarı saydam 0,95** (içerik paneli opak) |
| Ana menü | 1864–2185 | 379–1368 | 321 × 989 | **yarı saydam 0,92** |
| Save Stat Preset | 1080–1652 | 404–1275 | 572 × 871 | **mat** (ölçüm: 0,99) |
| Kapat (X) düğmesi | — | — | 82 × 84 | daire, ortak parça |

**Saydamlık:** Dördü de yarı saydam. Alfa değerleri kenar ölçümüyle bulundu —
Character 0,92 · Ana menü 0,92 · OPTIONS dış alan 0,95; OPTIONS'ın içerik paneli ise
kendi opak siyah zeminine sahip. Yöntem ve sonuç tablosu: `04-saydamlik.md`.
(Bu belgenin ilk hâlinde OPTIONS yanlışlıkla "mat" yazılmıştı; düzeltildi.)

**Ölçek:** Mevcut Character paketi 654 × 1030; bu çekimde aynı pencere 760 × 1205
(oran 0,86). Kullanıcı kararı: **mevcut 654 ölçeği korunuyor**. Sprite'lar yine de 760'lık
tam çözünürlükte saklanıyor — Unity çizim anında küçültür, yüksek yoğunluklu ekranda
detay korunur. Yeni sekme içeriği 654 uzayındaki koordinatlara yerleşir
(mevcut sekme şeridiyle hizası ±3 px doğrulandı).

## FRIENDS (`kaynak/friends/friends_icerik.png`, 760 × 1205, RGBA)

Pencere-yerel değil, **ekran koordinatı**; pencere kökü (303,143).

| öğe | konum | boyut |
|---|---|---|
| "FRIENDS" başlığı | 567, 269 | 245 × 45 |
| Arkadaş satırları (7 adet) | 345, 361 + 70,86·k | 676 × 70 |
| Sayfa ◀ | 593, 931 | 56 × 56 |
| Sayfa numarası | 665, 937 | 30 × 47 |
| Sayfa ▶ | 717, 931 | 58 × 56 |
| Durum göstergesi şeridi | 400, 1119 | 580 × 37 |
| REGISTER | 475, 1196 | 196 × 46 |
| DELETE | 689, 1196 | 198 × 46 |
| PRIVATE / PARTY / REFRESH | 354 / 575 / 797, 1272 | ~204 × 47 |

Durum renkleri: Online yeşil, In Party turuncu, Not Connected kırmızı (göstergeler sprite'ta).
İsim satırlarındaki yazılar **silindi**: 4. satır (zaten boş) dokusu 1–3. satırların üzerine
birebir kopyalandı. İsimler Unity'de `Text` olarak yazılacak.

## CLAN (`kaynak/clan/clan_icerik.png` + `bayrak_tr.png`)

| öğe | konum | boyut |
|---|---|---|
| Upgrade düğmesi | 390, 280 | 142 × 36 |
| Klan bayrağı (ayrı sprite, klana göre değişir) | 367, 327 | 196 × 169 |
| Klan adı / Grade (dinamik `Text`) | 590, 366 / 416 | — |
| Sandık ikonu | 929, 262 | 73 × 67 |
| Üye tablosu (çerçeve + başlık) | 350, 571 | 679 × 500 |
| Tablo başlık ayracı | y 619 | — |
| Üye satırları (12 adet) | y 627 + 36,95·k | — |
| Sütun merkezleri | ROLE 411 · MEMBERS 643 · LVL 859 · JOB 976 | — |
| DONATED LIST | 341, 1100 | 164 × 37 |
| Sayfa ◀ / ▶ | 570 / 770, 1099 | 47 × 40 |
| REFRESH | 875, 1100 | 162 × 37 |
| Total Online Members: kutusu | 627, 1172 | 62 × 30 |
| Number of Members : kutusu | 615, 1217 | 74 × 32 |
| JOIN CLAN | 877, 1167 | 155 × 37 |
| JOIN PARTY / APPOINT / Leave / PRIVATE | 343 / 520 / 697 / 877, 1269 | 157 × 40 |

Üye satırlarındaki yeşil yazılar, satır aralarından alınan temiz zemin şeridiyle dolduruldu.
İki değer kutusunun içindeki rakamlar da temizlendi; ikisi de Unity'de `Text`.

## Ana menü (`kaynak/ana_menu/ana_menu_cerceve.png`, 321 × 989 + `btn_kapat.png`)

Çerçeve 4 px; 8 düğme, panel-yerel x = 17, genişlik 292, yükseklik ~72,
üst kenarlar y = 51 · 170 · 291 · 412 · 534 · 653 · 775 · 896 (adım ~121).
Sıra: POWER-UP-STORE, OPEN MERCHANT, SLAVE MERCHANT, SEEKING PARTY, OPTIONS, FORUM, DISCORD, INSTAGRAM.
Düğme yazıları orijinal piksellerden; düğmeler görünmez tıklama alanı + ColorTint olacak.

## OPTIONS (`kaynak/options/`)

| parça | adet | boyut |
|---|---|---|
| `options_krom.png` — çerçeve, başlık, panel kenarlığı, RESET SETTINGS | 1 | 854 × 1171 |
| `menu/NN_<ad>_normal.png` ve `_secili.png` | 11 × 2 | 278 × 57 |
| `paneller/NN_<ad>.png` — içerik sayfaları | 11 | 511 × 909 |

- Sol menü düğmeleri: x 1034, üst kenar y = 298 + 86·k, k = 0…10
- İçerik paneli iç alanı: x 1339, y 283, 511 × 909
- RESET SETTINGS: 1457, 1214 · 322 × 56
- Kapat (X): merkez ~1816, 211

Menü sırası: Looting · Cospre · VFX · Game Option 1 · Game Option 2 · Game Option 3 ·
Block Options · Battle Options · PM Block · Hide Option · Sound Option.

Her düğmenin **normal** hâli, o düğmenin seçili *olmadığı* bir ekran görüntüsünden alındı;
**seçili** hâli ise seçili olduğu ekrandan. Battle Options'ın seçili hâli mavi değil **yeşil** —
oyun iki ayrı vurgu durumu kullanıyor, ikisi de sprite olarak saklandı.

`options_krom.png` saydamlığı ölçümle belirlendi: 11 ekran görüntüsü üst üste konup
değişen pikseller saydam, sabit kalanlar opak işaretlendi.

**Doğrulama:** Parçalardan yeniden kurulan OPTIONS penceresi, kendi ekran görüntüsünün
arka planı üzerine konduğunda orijinalle **birebir aynı** çıkıyor (ortalama fark 0,000–0,005;
farklı piksel %0,00). Yani çıkarım kayıpsız.

## Unity paketleri (tamamlandı)

| paket | pencere | boyut | zemin |
|---|---|---|---|
| `OlymposCharacter1298` | Character › CHAR INFO · **CLAN** · **FRIENDS** sekmeleri | 654 × 1030 | yarı saydam 0,92 |
| `OlymposMenuOptions1298` | **Ana menü** | 321 × 989 | yarı saydam 0,92 |
| (aynı paket) | **OPTIONS** (11 sayfa) | 854 × 1171 | dış 0,95 · içerik paneli opak |

Unity menüsü: `OLYMPOS > 1298 > Ana Menü Paneli Oluştur`, `… > OPTIONS Penceresi Oluştur`.
FRIENDS ve CLAN, Character kurucusunun bir parçası olarak kuruluyor.

### Sekme yapısı

Character penceresi artık dört panelden oluşuyor (`Panel_CharInfo`, `Panel_Quests`,
`Panel_Clan`, `Panel_Friends`); `OlymposCharacterWindow.ShowTab(i)` birini açıp
diğerlerini kapatıyor. Aktif sekmenin altındaki altın çizgi artık şeride gömülü değil:
`tabs_strip_plain.png` + kayan `tab_underline.png` (9-slice) ile dört sekmede de doğru
yere gidiyor. Çizginin her sekmedeki x/genişliği orijinal ekran görüntülerinden ölçüldü
(Char Info 9/210 · Quests 224/128 · Clan 362/162 · Friends 526/120).

QUESTS sekmesinin içeriği yok — o sekmenin ekran görüntüsü gelmedi; panel boş duruyor.

### Punto kalibrasyonu

Yeni sekmelerdeki yazıların puntosu, orijinal yazının **mürekkep yüksekliğinden**
hesaplandı (Roboto Slab Bold'un harf oranları ölçülerek), 654 ölçeğine çevrildi:

| yazı | orijinal ink (760) | punto (654) |
|---|---:|---:|
| Arkadaş adı | 21 px | **25** |
| FRIENDS sayfa numarası | 47 px | **57** |
| Klan adı | 29 px | **34** |
| Klan derecesi | 33 px | **29** |
| Üye tablosu (4 sütun) | 17 px | **18** |
| CLAN sayfa numarası | 25 px | **30** |
| Sayaçlar (16 · 29/50) | 17 px | **19** |

### Bilinen sınır

OPTIONS sayfalarındaki onay kutuları ve kaydırıcılar şu an sayfa görselinin parçası:
görsel olarak birebir, ama henüz tıklanabilir değil. İşaretli/işaretsiz kutu ve kaydırıcı
durumlarının hepsi kaynak ekran görüntülerinde mevcut; bir sonraki adımda ayrı sprite'lara
çıkarılıp etkileşimli hâle getirilecek.

### Doğrulama

- Üç paket de yapı / GUID / içerik SHA-256 kontrolünden geçti, mevcut GUID'ler kaymadı.
- Tüm C# dosyaları derleniyor (0 hata).
- Kurucunun ürettiği yerleşim Python'da birebir simüle edilip orijinalle karşılaştırıldı:
  `onizlemeler/cmp_sekme_yerlesimi.png`.
