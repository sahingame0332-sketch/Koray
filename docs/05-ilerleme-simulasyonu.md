# İlerleme Simülasyonu — İçeriği Çalıştırıp Değer Üretmek

> Tarih: 7 Kasım 2026

## 0. "Oyunu çalıştır" neden böyle oldu

İki şey istenebilirdi, ikisini de netleştirelim.

### MykoMobile burada çalıştırılamaz

Dört bağımsız engel var, hepsi bu oturumda doğrulandı:

| Engel | Kanıt |
|---|---|
| Android aracı yok | `adb`, `emulator`, `sdkmanager`, `qemu` — hiçbiri kurulu değil |
| Donanım sanallaştırma yok | `/dev/kvm` yok, `/proc/cpuinfo`'da 0 sanallaştırma bayrağı |
| GPU yok | `/dev/dri` yok; APK ise OpenGL ES 3.0 **zorunlu** istiyor |
| Mimari uyuşmuyor | APK yalnızca `arm64-v8a` + `armeabi-v7a` içeriyor; **x86 yok** |

Son satır tek başına belirleyici: standart x86 Android emülatörü bu APK'yı ARM
çevirisi olmadan çalıştıramaz. Üstüne oyun canlı bir servis — hesap ve kendi
sunucularına bağlantı gerekiyor.

**Sen ölçebilirsin, ben ayara çeviririm:** telefonda ekran kaydını başlat,
karakter panelini aç, dağıtılmamış puan sayını not et, "+" butonunu bırakmadan
puanlar bitene kadar tut. Kaç puan / kaç saniye bilgisini ver; videodan ilk
saniyedeki artış hızını da söylersen eğriyi birebir çıkarırım.

### Kendi projende çalıştırılabilir oyun henüz yok

Sunucu kodu yazılmadı, Unity Editor burada yok. Ama **içeriği çalıştırmak**
mümkün — ve istemci olmadan yapılabilecek en değerli şey bu.

---

## 1. `tools/simulate_progression.py`

İçeriği kullanarak bir oyuncunun seviye 1'den 100'e yolculuğunu simüle eder:
her seviyede en verimli mobu seçer, öldürme süresini hesaplar, gereken öldürme
sayısını bulur, ölü zamanı ekler ve saate çevirir.

```bash
python3 tools/simulate_progression.py              # tam rapor
python3 tools/simulate_progression.py --calibrate   # eğriyi hedefe göre çöz
```

### Neden `balance_report.txt` yetmiyor

`content/balance_report.txt` **tek bir mobun** dengesini gösterir (TTK/TTD) ve
"sorunlu mob sayısı: 0" diyor. Ama oyunun gerçek sorunu **birikimde**:
tek tek moblar dengeliyken seviye eğrisi ile mob tecrübesi uyuşmazsa oyun
ilerleme tarafında çöker. Bunu ancak baştan sona simüle ederek görürsün.

Tam olarak bu oldu.

---

## 2. Bulunan ciddi hata: seviye eğrisi

İlk çalıştırmada:

```
TOPLAM 1 -> 100: 7.8 saat   (hedef bant 80-400 saat)  -> COK KISA

Tempo (seviye başına süre):
  sv   1-10   0.11 sa/sv
  sv  51-60   0.07 sa/sv
  sv  91-99   0.06 sa/sv     <-- seviyeler İLERLEDİKÇE HIZLANIYOR
```

Bir MMORPG 7.8 saatte bitmez; dahası tempo **ters** — geç seviyeler erken
seviyelerden hızlı. Bu, oyuncunun hiçbir başarı hissi yaşamaması demek.

### Sebep matematiksel, tahmin değil

```
mob tecrübesi    ~ 12 + level^1.75
seviye ihtiyacı  ~ coef × p × level^(p-1)        (toplam = coef × level^p)

seviye başına öldürme sayısı ~ level^(p-1) / level^1.75 = level^(p-2.75)
```

Yani **p > 2.75 olmalı** ki seviye başına çaba artsın. İlk şemada `p = 2.2`
yazmıştım → üs negatif → seviyeler hızlanıyor. Kaçınılmaz sonuç.

### Çözüm aracın kendisinden geldi

`--calibrate` modu, her üs için katsayıyı hedef süreye göre ölçekleyip iki
kriteri denetler: ilk 10 seviye yeterince hızlı mı, ve süre/seviye artıyor mu.

```
  exponent   katsayi    toplam   sv1-10   tempo        durum
       2.8     110.80    100.0sa   4.63sa  son/ilk x  3.0  DUSEN  -
       3.0      47.48    100.0sa   3.14sa  son/ilk x  5.1  DUSEN  -
       3.2      20.12    100.0sa   2.10sa  son/ilk x  8.5  ARTAN  -
       3.4       8.45    100.0sa   1.40sa  son/ilk x 14.2  ARTAN  ok
       3.6       3.52    100.0sa   0.93sa  son/ilk x 23.6  ARTAN  ok
       3.8       1.46    100.0sa   0.61sa  son/ilk x 39.1  ARTAN  ok
```

Tablo bir **takası** gösteriyor: üs büyüdükçe başlangıç hızlanır ama geç oyun
giderek daha acımasız olur. 3.8'de son bant ilk bandın 39 katı — oyuncu bırakır.

Seçilen: **`exp_required = 8.45 × level^3.4`**

`docs/schema/01_core_schema.sql` içindeki `level_curve` seed'i bununla
güncellendi ve gerekçesi oraya yorum olarak yazıldı.

---

## 3. Düzeltme sonrası değerler

```
  sv  gereken exp  mob (sv)                  TTK   öldürme   süre   toplam
    1           81  Yeşil Örümcek      ( 6)    9.8s        2   0.01sa     0.0sa
   10        8,123  Kuru Örümcek       (15)    9.4s       64   0.24sa     1.4sa
   20       40,428  Gölge Kurt         (25)    9.6s      138   0.53sa     5.7sa
   30      104,887  Gölge Örümcek      (30)    6.7s      264   0.71sa    11.6sa
   50      351,770  Yanık Örümcek      (45)    5.8s      443   1.02sa    29.5sa
   70      783,433  Ejder Kurt         (75)    8.1s      407   1.31sa    53.6sa
   90    1,426,592  Ejder Örümcek      (85)    6.4s      597   1.52sa    82.1sa
   99    1,791,089  Ejder Haydut       (95)    8.7s      617   2.13sa   100.0sa

TOPLAM 1 -> 100: 100.0 saat  -> ok
  toplam öldürülen mob : 33,407
  duvar yok. En uzun seviye: 99 (2.13 saat)
```

Tempo artık monoton artıyor:

```
  sv   1-10   0.14 sa/sv  #
  sv  21-30   0.59 sa/sv  #######
  sv  41-50   0.93 sa/sv  ###########
  sv  61-70   1.27 sa/sv  ###############
  sv  91-99   2.00 sa/sv  #######################
```

İlk 10 seviye 1.4 saat — yeni oyuncu hızlı ilerleyip oyunu tanıyor. Son
seviyeler 2 saat — başarı hissi veriyor ama duvar değil.

### Ekonomi

| | |
|---|---|
| Brüt altın geliri (1→100) | 5.044.279 |
| İksir masrafı | 2.751.030 (**%55**) |
| Net altın | 2.293.249 |
| Saatlik net | 22.924/sa |
| En pahalı ekipman | Ejder Güç Yüzük (216.000) |
| Onu almak için | 9.4 saat farm |

---

## 4. Simülasyonun işaret ettiği, henüz çözülmemiş iki şey

### 4.1 İksir masrafı gelirin %55'i — çok yüksek

Oyuncunun kazandığı altının yarısından fazlası tüketilebilire gidiyor. Bu, para
biriktirme hissini yok eder. Üç ayardan biri gerekli:

- mob altın düşürmesini artır (`gen_mobs_and_spawns` içinde `gold_min/gold_max`)
- iksir fiyatını düşür (`gen_items` tüketilebilir listesi)
- `POTION_PER_KILL = 0.35` varsayımını düşür — yani mobları daha az tehlikeli
  yap (bu `TARGET_TTD_SEC`'i etkiler)

Hangisi doğru, oyun hissine bağlı bir karar; o yüzden kendi başıma değiştirmedim.

### 4.2 Düşme oranları her yerde aynı: %2.10

```
  sv   mob                     oran     ortalama kaç mob
    1  Yeşil Kurt              % 2.10          48
   25  Kuru Golem              % 2.10          48
```

Üreteç her moba aynı loot desenini veriyor. Sonuç: seviye 1'de de seviye 90'da
da ekipman düşme heyecanı aynı. Gerçek oyunlarda nadir mob / boss daha iyi
oran verir. `gen_mobs_and_spawns` içindeki sabit `ppm` değerleri arketipe ve
seviyeye göre farklılaştırılmalı.

---

## 5. Simülasyonun sınırları — neyi kanıtlamıyor

Dürüst olmak gerekirse:

- **Sınıf karşılaştırması eksik.** Rapor sınıflar arası %57 fark gösteriyor ve
  "DENGESİZ" diye işaretliyor. Ama bu yalnızca **silah DPS'i**. Büyücü ve
  şifacı hasarının çoğu becerilerden ve zekâ ölçeklemesinden gelir; simülasyon
  beceri hasarını sınıf bazında modellemiyor. Yani bu işaret bir **model
  eksikliği**, kanıtlanmış bir dengesizlik değil. Doğru ölçüm için beceri
  rotasyonu simüle edilmeli.
- **Parti ve zindan yok.** Her şey tek oyuncu. Partide tecrübe bölünür ama
  öldürme hızlanır; net etki modellenmedi. Boss'lar hesaba hiç girmiyor.
- **PvP, görev, zanaat yok.** Gerçek oyunda tecrübenin bir kısmı görevlerden
  gelir; bu tamamen mob avı varsayıyor.
- **Oyuncu davranışı varsayım.** `%30 ölü zaman`, `mob başına 0.35 iksir`,
  `beceri katkısı ×1.35` — bunlar makul tahminler, ölçüm değil. Gerçek oyuncu
  verisi geldiğinde bu üç sayı güncellenmeli; rapor zaten varsayımları en
  üstte yazıyor.
- **Mob seçimi iyimser.** Simülasyon her seviyede tecrübe/saniye en yüksek
  mobu seçiyor. Gerçek oyuncu her zaman en verimli yerde avlanmaz, yani gerçek
  süre bundan uzun olur.

Bu yüzden 100 saat bir **alt sınır** sayılmalı, kesin bir rakam değil.

---

## 6. Varsayımları değiştirip yeniden çalıştırmak

Betiğin en üstündeki varsayımları değiştir, çalıştır:

```python
DOWNTIME_FRACTION = 0.30    # ölü zaman oranı
POTION_PER_KILL = 0.35      # mob başına iksir
SKILL_DPS_BONUS = 1.35      # becerilerin katkısı
WALL_HOURS = 3.0            # kaç saatten uzun seviye "duvar" sayılır
TOTAL_HOURS_TARGET = (80.0, 400.0)
```

Eğriyi farklı hedefe göre yeniden çözmek için:

```bash
python3 tools/simulate_progression.py --calibrate --hours 150 --early 2.0
```

Çıktı, SQL'e yazılacak satırı doğrudan veriyor. Değiştirirsen
`01_core_schema.sql` ile `EXP_COEF`/`EXP_EXPONENT`'i birlikte güncelle —
ikisi ayrılırsa simülasyon yalan söylemeye başlar.
