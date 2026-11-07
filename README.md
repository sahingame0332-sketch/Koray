# Koray — Mobil MMORPG Projesi

Bu depo, MykoMobile (Knight Online kimliğiyle pazarlanan Unity tabanlı mobil MMORPG)
altyapısının teknik incelemesi ve buradan yola çıkarak **kendi oyununu** yapmak için hazırlanan yol
haritasıyla başlıyor.

## Dokümanlar

| Dosya | İçerik |
|---|---|
| [`docs/01-mykomobile-altyapi-analizi.md`](docs/01-mykomobile-altyapi-analizi.md) | Ana doküman: MykoMobile'ın ne olduğu, "altyapı"nın teknik anatomisi (77 tablo, 70 saklı yordam, 289 opcode), tasarım kusurları, hukuki durum, üç yol karşılaştırması, önerilen mimari ve 0→1 yol haritası |
| [`docs/02-apk-analizi.md`](docs/02-apk-analizi.md) | MykoMobile APK'sının (145 MB, resmî indirme) statik analizi: motor, SDK yığını, imza, izinler, arka uç adresleri — ve kod tabanının kökenine dair bulgular |
| [`docs/schema/01_core_schema.sql`](docs/schema/01_core_schema.sql) | Kendi oyunun için normalize PostgreSQL başlangıç şeması (26 tablo). KO'nun yedi temel kusuru baştan çözülmüş. PostgreSQL 16.15'te test edildi. |

## Hızlı başlangıç

```bash
createdb oyun
psql -d oyun -f docs/schema/01_core_schema.sql
```

## Durum

Henüz kod yok — tasarım ve karar aşaması. Ana dokümanın **Bölüm 9**'u sıradaki üç
adımı anlatıyor.

## Önemli notlar

- **Okuma sırası:** `01` genel resmi ve yol haritasını verir, `02` ise APK analizinin
  somut bulgularını. `01`'in başında, `02`'nin çürüttüğü bir varsayım için düzeltme
  kutusu var — onu atlamayın.
- **Hukuk:** `01` Bölüm 4 ve `02` Bölüm 7.3, Knight Online türevi bir ürün yapmanın
  Türkiye'deki hukuki durumunu özetliyor (Mgame Corporation'ın Ocak 2025'te açtırdığı
  dava dahil). Teknik karar vermeden önce ikisini de oku. Hukuki tavsiye değildir.
