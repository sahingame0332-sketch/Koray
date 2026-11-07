# Koray — Mobil MMORPG Projesi

Bu depo, MykoMobile (Knight Online kimliğiyle pazarlanan Unity tabanlı mobil MMORPG)
altyapısının teknik incelemesi ve buradan yola çıkarak **kendi oyununu** yapmak için hazırlanan yol
haritasıyla başlıyor. İkinci hat, oyunun arayüzü: `arayuz/` altında **OLYMPOS-KO** adıyla,
Knight Online 1298 istemcisinin pencereleri birebir Unity'ye aktarılıyor.

Proje bağlamı ve çalışma kuralları: [`CLAUDE.md`](CLAUDE.md).

## Dokümanlar

| Dosya | İçerik |
|---|---|
| [`docs/01-mykomobile-altyapi-analizi.md`](docs/01-mykomobile-altyapi-analizi.md) | Ana doküman: MykoMobile'ın ne olduğu, "altyapı"nın teknik anatomisi (77 tablo, 70 saklı yordam, 289 opcode), tasarım kusurları, hukuki durum, üç yol karşılaştırması, önerilen mimari ve 0→1 yol haritası |
| [`docs/02-apk-analizi.md`](docs/02-apk-analizi.md) | MykoMobile APK'sının (145 MB, resmî indirme) statik analizi: motor, SDK yığını, imza, izinler, arka uç adresleri — ve kod tabanının kökenine dair bulgular |
| [`docs/03-icerik-uretim-rehberi.md`](docs/03-icerik-uretim-rehberi.md) | İçerik üretim hattı: karakter, item, skill, mob, harita ve arayüz için veri modeli, dengeleme yöntemi, UI ekran envanteri ve sanat varlığı kaynakları |
| [`docs/schema/01_core_schema.sql`](docs/schema/01_core_schema.sql) | Normalize PostgreSQL çekirdek şeması (27 tablo + 2 görünüm). KO'nun yedi temel kusuru baştan çözülmüş. PostgreSQL 16.15'te test edildi. |
| [`docs/schema/02_content_seed.sql`](docs/schema/02_content_seed.sql) | Üretilmiş başlangıç içeriği: 181 eşya, 40 beceri, 44 NPC, 242 loot satırı, 100 doğma noktası, 10 bölge (otomatik üretildi — elle düzenlemeyin) |
| [`tools/generate_content.py`](tools/generate_content.py) | İçerik üreteci. Tasarım parametrelerini değiştir, çalıştır, içerik + dengeleme raporu yeniden üretilir |
| `content/*.json` | Üretilen içeriğin okunabilir hâli + `balance_report.txt` |

### Arayüz (`arayuz/`)

| Dosya | İçerik |
|---|---|
| [`arayuz/00-sohbet-ozeti.md`](arayuz/00-sohbet-ozeti.md) | claude.ai'daki arayüz sohbetinin adım adım kaydı — hangi pencere hangi istek üzerine, nasıl üretildi |
| [`arayuz/01-dogrulama.md`](arayuz/01-dogrulama.md) | Devir paketinin doğrulama raporu: derleme sonucu, paket/GUID tutarlılığı, iyileştirme adayları, açık kalanlar |
| [`arayuz/02-font-kalibrasyonu.md`](arayuz/02-font-kalibrasyonu.md) | Roboto Slab Bold'un temini ve puntoların orijinale göre ölçülerek kalibre edilmesi: yöntem, aday font sıralaması, punto tablosu, sonuçlar |
| `arayuz/unity_paketleri/*.unitypackage` | Unity'ye doğrudan import edilebilir iki paket: Character (Char Info) ve Save Stat Preset + Stat butonları |
| `arayuz/unity_kaynak/Assets/` | Paketlerin kaynağı (`.meta` dosyalarıyla): sprite'lar, fontlar, çalışma zamanı betikleri, editör kurucuları |
| `arayuz/kaynak/` | Sprite çıkarımının ara ürünleri ve HTML önizleme (`kaynak/char_info/unity_preview.html`) |
| `arayuz/referans_gorseller/`, `arayuz/onizlemeler/` | Orijinal oyun ekran görüntüleri ve orijinal ↔ yeni karşılaştırma görselleri |
| `arayuz/araclar/` | RAR5 okuyucu, `.unitypackage` üreteci, sprite üreteci, `derleme_kontrolu/` (Unity'siz C# derlemesi) ve `font_kalibrasyonu/` (font/punto ölçümü) |

## Hızlı başlangıç

```bash
python3 tools/generate_content.py              # içeriği üret + denge raporu
createdb oyun
psql -d oyun -f docs/schema/01_core_schema.sql  # şema
psql -d oyun -f docs/schema/02_content_seed.sql # içerik
cat content/balance_report.txt                  # "Sorunlu mob sayısı: 0" olmalı

arayuz/araclar/derleme_kontrolu/derle.sh        # arayüz betiklerini Unity'siz derle (mono-devel gerekir)
```

## Durum

Veri modeli ve başlangıç içeriği hazır ve PostgreSQL'de doğrulandı. Sunucu kodu henüz yok —
sıradaki iş `01` Bölüm 7'deki **Faz 1 dikey dilimi**.

Arayüz tarafında üç pencere (Char Info, Save Stat Preset, Stat butonları) Unity paketi hâlinde
hazır; betikler bu ortamda **derlendi (0 hata)** ve paketler yapı/GUID/içerik olarak doğrulandı.
Char Info'nun fontu gerçek **Roboto Slab Bold** ile kuruldu ve puntolar orijinale göre ölçülerek
kalibre edildi: 31 yazı bölgesinde örtüşme 0.478 → **0.627**, 31/31 iyileşti.
Unity'de ilk import henüz denenmedi — `arayuz/01-dogrulama.md` ve `arayuz/02-font-kalibrasyonu.md`.

## Önemli notlar

- **Okuma sırası:** `01` genel resmi ve yol haritasını verir, `02` ise APK analizinin
  somut bulgularını. `01`'in başında, `02`'nin çürüttüğü bir varsayım için düzeltme
  kutusu var — onu atlamayın.
- **Hukuk:** `01` Bölüm 4 ve `02` Bölüm 7.3, Knight Online türevi bir ürün yapmanın
  Türkiye'deki hukuki durumunu özetliyor (Mgame Corporation'ın Ocak 2025'te açtırdığı
  dava dahil). Teknik karar vermeden önce ikisini de oku. Hukuki tavsiye değildir.
