# Devir paketi doğrulama raporu

Tarih: 7 Kasım 2026 · Ortam: Claude Code (Linux konteyner, Unity yok)

> Font ve punto tarafı ayrı belgede: `02-font-kalibrasyonu.md`.

Devir notundaki açık nokta şuydu: *"Unity ve C# derleyicisi bulunmayan bir ortamda yazıldı →
derlenmedi, Unity'de denenmedi."* Bu ortamda **C# derleyicisi (Mono `mcs` 6.8) kuruldu** ve
derleme adımı kapatıldı. Unity'nin kendisi hâlâ yok, dolayısıyla import/çalışma zamanı denemesi
kullanıcıda duruyor.

## Yapılan doğrulamalar

| # | Kontrol | Sonuç |
|---|---|---|
| 1 | Beş C# dosyasının derlenmesi (Mono `mcs`, `-langversion:7.2`) | **0 hata, 0 uyarı** |
| 2 | `.unitypackage` arşiv yapısı (tar.gz; her giriş için `pathname` + `asset.meta`, dosyalarda ayrıca `asset`) | Doğru — Character 21 giriş (14 dosya + 7 klasör), StatWindows 19 giriş (12 dosya + 7 klasör) |
| 3 | Paketteki GUID'ler ↔ `unity_kaynak/` içindeki `.meta` GUID'leri | **Hepsi aynı** (0 uyuşmazlık) |
| 4 | Paketteki dosya içerikleri ↔ `unity_kaynak/` kaynakları (SHA-256) | **Hepsi aynı** (26 dosya, 0 fark) |
| 5 | Sprite piksel ölçüleri ↔ kurucudaki koordinatlar | Uyumlu (aşağıdaki not 1 hariç) |
| 6 | Font kalibrasyonu sonrası paketler yeniden üretildi; 2–4 tekrar koşuldu | **0 uyuşmazlık**, mevcut GUID'ler değişmedi |

3 ve 4 birlikte şunu garanti eder: paketi **Import Package** ile almak ile `Assets/` klasörünü
elle kopyalamak aynı sonucu verir; GUID'ler kaymaz, prefab/referanslar kopmaz.

### Derleme nasıl tekrar edilir

```bash
apt-get install -y mono-devel          # ortamda mcs yoksa
arayuz/araclar/derleme_kontrolu/derle.sh
```

Taslaklar ve ayrıntı: `arayuz/araclar/derleme_kontrolu/` (`UnityStubs.cs`, `EditorStubs.cs`, `BENIOKU.md`).

**Bu doğrulamanın sınırı:** taslaklar, Unity API'sinin bu depodaki betiklerin kullandığı
üyelerinden oluşuyor ve imzaları Unity belgelerine göre elle yazıldı. Temiz derleme, **C# kodunun
kendisinin sağlam olduğunu** gösterir (sözdizimi, isim çözümleme, tip akışı, jenerikler,
`Object` ad çakışması olmaması, `??` ve üçlü operatör kullanımları). Gerçek Unity imzalarının
birebir eşleştiğini **kanıtlamaz**. Kesin sonuç Unity'deki ilk import'ta alınacak.

## Notlar ve iyileştirme adayları

Hiçbiri derlemeyi veya import'u engellemiyor; bilinçli karar olabilecekleri için
koda dokunulmadı, kayda geçiriliyor.

1. **`race_human.png` 228×228, ekranda 57×57.** Dört kat küçültülerek çiziliyor ve doku
   ayarlarında mipmap kapalı (`mipmapEnabled = false`). Bilinear filtre 4× küçültmede
   komşu piksellerin yalnızca bir kısmını örneklediği için ikon kenarlarında tırtık olabilir.
   Seçenekler: dokuyu 57×57'ye (veya 114×114) indirmek, ya da yalnızca bu doku için mipmap açmak.
   Pencere sabit ölçekte durduğu sürece etki sınırlı.
2. **`value_box.png` alfa kanalı taşımıyor (RGB).** Diğer tüm sprite'lar RGBA. Bu, devir
   notundaki "kutular/butonlar **opak**" kuralıyla uyumlu — eksik değil, kasıtlı. İleride
   "alfa eksik" diye düzeltilmeye çalışılmasın.
3. **`btn_preset` / `btn_reset` için 9-slice kenarı boşa gidiyor.** `ConfigureTextures()`
   bu ikisine `spriteBorder = (6,6,6,6)` yazıyor, ama kurucu bunları `Image.Type.Simple`
   olarak çiziyor (`Btn` → `Img(..., sliced: false)`) ve butonlar tam 145×45, yani sprite'ın
   kendi ölçüsünde. Zararsız; ya kenar ayarı kaldırılabilir ya da ileride esnek genişlik
   gerekirse `Sliced`'a geçilebilir.
4. **`Object.FindObjectOfType<T>()` Unity 2023.1 / Unity 6'da eskimiş sayılıyor.**
   İki kurucunun `EnsureCanvas()` metodunda kullanılıyor. Konsolda **uyarı** üretir, hata
   değil — çalışmayı engellemez. Yeni karşılığı `FindFirstObjectByType<T>()`.
   Hangi Unity sürümünün kullanılacağı netleşince `#if UNITY_2023_1_OR_NEWER` ile ayrılabilir.
5. **`label_button.png` 138×32, etiketler 30 px yükseklikte çiziliyor.** 9-slice dikey
   kenarları 8+8 = 16 px olduğundan orta bant 16 px'den 14 px'e sıkışıyor. Gözle fark edilmez.

## Hâlâ açık

- **Unity'de ilk import ve derleme.** Kullanıcının `OLYMPOS > 1298 > …` menülerini çalıştırıp
  Console çıktısını getirmesi gerekiyor. Beklenen tek uyarı kaynağı: not 4.
  (`RobotoSlab-Bold.ttf` artık pakette olduğu için font uyarısı çıkmayacak.)
- Üç pencerenin ölçeklerinin birbirine oranlanması (Char Info daha büyük bir ekran
  görüntüsünden geldi — kök `RectTransform.Scale` ile ayarlanacak).
- Puntoların Unity'de de tuttuğunun doğrulanması (Chromium üzerinden ölçüldü; ±1 rötuş gerekebilir) — `02-font-kalibrasyonu.md`.
- QUESTS / CLAN / FRIENDS sekmeleri ve yeni pencereler.
