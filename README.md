# Koray — Mobil MMORPG Projesi

Bu depo, MykoMobile (Knight Online kimliğiyle pazarlanan Unity tabanlı mobil MMORPG)
altyapısının teknik incelemesi ve buradan yola çıkarak **kendi oyununu** yapmak için hazırlanan yol
haritasıyla başlıyor.

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

## Hızlı başlangıç

```bash
python3 tools/generate_content.py              # içeriği üret + denge raporu
createdb oyun
psql -d oyun -f docs/schema/01_core_schema.sql  # şema
psql -d oyun -f docs/schema/02_content_seed.sql # içerik
cat content/balance_report.txt                  # "Sorunlu mob sayısı: 0" olmalı
```

## Durum

Veri modeli ve başlangıç içeriği hazır ve PostgreSQL'de doğrulandı. Oyun kodu
(sunucu + Unity istemcisi) henüz yok — sıradaki iş `01` Bölüm 7'deki **Faz 1
dikey dilimi**.

## Önemli notlar

- **Okuma sırası:** `01` genel resmi ve yol haritasını verir, `02` ise APK analizinin
  somut bulgularını. `01`'in başında, `02`'nin çürüttüğü bir varsayım için düzeltme
  kutusu var — onu atlamayın.
- **Hukuk:** `01` Bölüm 4 ve `02` Bölüm 7.3, Knight Online türevi bir ürün yapmanın
  Türkiye'deki hukuki durumunu özetliyor (Mgame Corporation'ın Ocak 2025'te açtırdığı
  dava dahil). Teknik karar vermeden önce ikisini de oku. Hukuki tavsiye değildir.
