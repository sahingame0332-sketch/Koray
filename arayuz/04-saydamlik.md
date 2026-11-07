# Pencere saydamlıkları — ölçüm

Tarih: 7 Kasım 2026

Devirden bu yana her pencerede varsayılan olarak **alfa 0,85** kullanılıyordu. Bu değer
ölçülmüş değil, varsayılmıştı. Kullanıcı "saydamlıkları da birebir al" deyince orijinal
ekran görüntülerinden ölçüldü — ve 0,85'in fazla saydam olduğu çıktı.

## Yöntem

Pencere zemini saf siyah ve alfası `a` ise, ekranda görünen değer

```
görünen = (1 - a) · arka_plan
```

olur. Yani pencere kenarının **hemen dışındaki** oyun dünyası ile **hemen içindeki** boş
zeminin oranı doğrudan geçirgenliği (`t = 1 - a`) verir. Kenarın iki yanında arka planın
yerel olarak aynı kaldığı varsayılır; bu yüzden yalnızca dış şeridin düz ve yeterince
parlak olduğu satırlar sayılır, iç şeritte ise arayüz öğelerini dışlamak için 10. yüzdelik
alınır.

Araç: `araclar/saydamlik_olcumu/saydamlik.py` (ham kesit için `--profil`).

Kanal kanal bakıldığında geçirgenlik R, G ve B'de aynı çıkıyor — yani zemin **saf siyah**,
renk tonu yok. Bu da formülü doğruluyor.

## Ölçüm

| pencere | geçirgenlik t | **alfa** | kaynak |
|---|---:|---:|---|
| Character (dört sekme) | 0,071 – 0,079 | **0,92** | 01, 02, 15 — sol ve sağ kenar |
| Ana menü | 0,065 – 0,085 | **0,92** | 03 — sol ve sağ kenar |
| Stat butonları | 0,078 | **0,92** | 15 — sağ kenar |
| OPTIONS, dış alan | 0,037 – 0,055 | **0,95** | 04, 09 — sol ve sağ kenar |
| Save Stat Preset | 0,012 | **0,99 → mat** | 16 — sol kenar |
| OPTIONS içerik paneli | ~0 | **opak** | kendi siyah zemini var |

Örnek kesit (görsel 15, Character penceresinin sol kenarı, y 1250–1300):

```
x 270…300  oyun dünyası   54 → 61
x 302…305  bronz çerçeve  88 → 127
x 308…351  pencere içi     4,1 → 5,3        t = 4,5 / 57 = 0,079  →  alfa 0,92
```

Save Stat Preset'te aynı kesit (görsel 16): dışarısı 52, pencere içi **0,6** →
t = 0,012. Kullanıcının baştan söylediği "Save Stat Preset mat" kuralı ölçümle doğrulandı.

## Önce yanılmıştım

İlk incelemede OPTIONS'ı **opak** sanmıştım: 11 ekran görüntüsünde pencere içi pikseller
birebir aynıydı ve rgb(2,2,1) çıkıyordu. İki hata vardı:

1. On bir çekim de aynı kamera konumundan alınmış, yani pencerenin arkasındaki dünya zaten
   sabit — "değişmiyor" olması opaklık kanıtı değil.
2. Ölçtüğüm yer pencerenin dış alanı değil, **içerik panelinin** içiydi; o panelin kendi
   opak siyah zemini var. Pencerenin dış alanı (çerçeve ile panel arası, sol menünün
   bulunduğu bölge) gerçekte yarı saydam.

Kenar ölçümü ikisini ayırdı: OPTIONS'ın dış alanı alfa 0,95, içerik paneli opak.

## Belirsizlik

Ölçümün doğruluğu ±0,02 civarında. Kaynağı, kenarın iki yanında arka planın tam olarak
aynı olmaması (arada 6–11 px çerçeve var). Aynı pencerenin farklı kenarlarından ve farklı
ekran görüntülerinden alınan değerler 0,89 ile 0,96 arasında dağılıyor; tabloya medyan
yazıldı. Oyunun gerçekte 0,9 gibi yuvarlak tek bir değer kullanıyor olması da mümkün.

Bu yüzden her pencerede `backgroundAlpha` Inspector ayarı açık kalıyor; Unity'de yan yana
görülünce tek tıkla ayarlanabilir.

## Uygulanan değişiklikler

- `OlymposCharacterWindow.backgroundAlpha` 0,85 → **0,92**
- `OlymposStatButtonsWindow.backgroundAlpha` 0,85 → **0,92**
- `kaynak/char_info/unity_preview.html` zemini `rgba(0,0,0,.92)`
- Önizleme görselleri ve iki `BENIOKU.txt` yenilendi
- Yeni pencereler bu değerlerle kurulacak: Ana menü 0,92 · OPTIONS dış 0,95 (içerik paneli opak)
- Save Stat Preset mat kalıyor (değişiklik yok)
