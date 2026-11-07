# Stat Dağıtımı: Basılı-Tutma Tekrarlama Hızı Analizi ve Unity Kaynak Dosyaları

> Tarih: 7 Kasım 2026

## 0. Önce bir netleştirme

MykoMobile'ın kendi tekrarlama hızını **APK'dan ölçemem.** Bu sayı statik
analizle çıkmaz — oyunu cihazda çalıştırıp butonu tutarak ölçmek gerekir.
Elimde oyunun çalıştığı bir cihaz yok.

Onun yerine **doğru hızı türettim.** Bu aslında daha iyi bir sonuç: bir
sayıyı kopyalamak yerine, kendi oyununun kendi sayılarına göre hesaplanmış bir
eğri elde ediyorsun. Çünkü doğru hız, oyuncunun elinde biriken puan sayısına
bağlıdır ve o sayı senin `level_curve` tablonla belirlenir.

---

## 1. Problemi sayılarla kur

`docs/schema/01_core_schema.sql`'deki `level_curve` tablosu seviye başına **3
stat puanı** veriyor, azami seviye 100. Yani:

```
Seviye 1 → 100 arası kazanılan puan = 99 seviye × 3 = 297 puan
```

En kötü durum bu: bir oyuncu hiç dağıtmamış, 297 puanı var ve "+" butonunu
basılı tutuyor.

İki yanlış yön var, ikisi de gerçek şikâyet üretir:

| Hata | Sonuç |
|---|---|
| Çok yavaş | 297 puanı dağıtmak dakikalar sürer, oyuncu paneli kapatıp gider |
| Çok hızlı | Oyuncu tek puan eklemek isterken 5 puan ekler ve geri alamaz |

Yani hız bir zevk meselesi değil, **iki kısıt arasında çözülecek bir
problem.** Hedefleri şöyle tanımladım:

| Puan | Senaryo | Hedef süre |
|---|---|---|
| 1 | tek dokunuş | anında, beklemesiz |
| 3 | bir seviye atlandı | ≤ 0.80 sn |
| 15 | 5 seviye birikmiş | ≤ 2.20 sn |
| 30 | 10 seviye | ≤ 3.20 sn |
| 60 | 20 seviye | ≤ 4.60 sn |
| 150 | 50 seviye | ≤ 6.50 sn |
| 297 | en kötü durum | ≤ 8.00 sn |

---

## 2. Model

```
t = 0                    parmak değdi → ANINDA 1 puan (tek dokunuş hassasiyeti)
t < 0.35 sn              tekrar YOK (kazara tekrar başlamaz)
t ≥ 0.35 sn              her tick'te STEP kadar puan
                           tick hızı : 8 → 20 tick/sn (1.20 sn'de, eğri exp 1.6)
                           adım boyu : süre eşiklerine göre büyür
```

Adım eşikleri:

| Basılı tutma | Adım |
|---|---|
| 0.00 sn | 1 |
| 1.20 sn | 2 |
| 2.20 sn | 5 |
| 3.40 sn | 10 |
| 5.00 sn | 25 |

### İki tasarım kararı ve gerekçeleri

**1. Tick hızını 20/sn'de sınırla, adım boyunu büyüt.**
297 puanı makul sürede dağıtmak için tick hızını 60/sn'ye çıkarmak gerekirdi.
Bu iki sorun yaratır: 60 Hz ekranda kare başına birden fazla tick düşer (yani
kare hızına bağımlı hale gelirsin) ve sayaç okunamayacak kadar hızlı akar.
Bunun yerine adımı büyütmek her ikisini çözer. Oyuncu 300 puanı dağıtırken
10'luk adımlar görmekten rahatsız olmaz; 3 puanı dağıtırken 1'lik adım alır.

**2. İlk gecikme 0.35 sn.**
İnsanın normal bir dokunuşu ~100–150 ms sürer. 0.35 sn, bunun belirgin
üstünde — yani normal dokunuş asla tekrar başlatmaz. Ölçtüm: 340 ms basılı
tutma hâlâ tam 1 puan ekliyor.

---

## 3. Sonuçlar

`tools/analyze_hold_repeat.py` eğriyi simüle edip hedeflere göre denetliyor:

```
  puan    süre     hedef   tick   durum
     1    0.00sn   0.00sn      1   ok
     3    0.47sn   0.80sn      3   ok
    15    1.35sn   2.20sn     13   ok
    30    1.72sn   3.20sn     20   ok
    60    2.32sn   4.60sn     32   ok
   150    3.22sn   6.50sn     50   ok
   297    4.02sn   8.00sn     66   ok

  SONUÇ: bütün hedefler sağlandı
```

Zaman içinde etkin hız:

| Süre | tick/sn | adım | puan/sn |
|---|---|---|---|
| 0.35 sn | 8.0 | 1 | 8 |
| 1.00 sn | 12.5 | 1 | 12.5 |
| 1.20 sn | 14.9 | 2 | 30 |
| 1.60 sn | 20.0 | 2 | 40 |
| 2.20 sn | 20.0 | 5 | 100 |
| 3.40 sn | 20.0 | 10 | 200 |
| 5.00 sn | 20.0 | 25 | 500 |

### Betiğin yakaladığı ölü ayar

25'lik adım eşiği (5.00 sn) **mevcut sayılarla hiç devreye girmiyor** — en kötü
durum 4.02 sn'de bitiyor. Bilinçli olarak bıraktım: azami seviye yükselirse
veya seviye başına puan artarsa gerekecek. Betik bunu her çalıştırmada
raporluyor, böylece ölü ayar sessizce birikmiyor.

---

## 4. Düzelttiğim gerçek bir hata — tick planlaması

İlk yazdığım kodda sonraki tick, **gerçekleşen** ana göre planlanıyordu:

```csharp
_nextTickTime = _holdTime + Tuning.GetTickInterval(_holdTime);   // YANLIŞ
```

Sorun şu: kare süresi 16.7 ms, tick aralığı 50 ms. Tick her zaman biraz
**gecikerek** çalışır. Gecikmeyi bir sonraki planlamaya taşırsan sapma
66 tick boyunca birikir.

Doğrulama koşumu bunu yakaladı: C# 4.15 sn, Python 4.07 sn. Fark simülasyon
adımından geliyordu — yani 60 FPS'te dağıtım ~0.5 sn, 30 FPS'te ~1 sn uzardı.
"Kare hızından bağımsız" dediğim şey aslında değildi.

Düzeltme, planlamayı **ideal** ana taşımak:

```csharp
int step = Mathf.Min(Tuning.GetStepSize(_nextTickTime), capacity);   // DOĞRU
Emit(step);
_nextTickTime += Tuning.GetTickInterval(_nextTickTime);
```

Ölçülen sonuç:

```
Kare hızı bağımsızlığı (297 puan):
  FPS     süre    kare süresi
   30     4.03s    33.3 ms
   60     4.02s    16.7 ms
  120     4.02s     8.3 ms
  240     4.02s     4.2 ms
  yayılım 0.017s   ok (sapma birikmiyor)
```

17 ms yayılım = yarım kare. Bu ölçümün son kareye yuvarlanmasından geliyor,
sapma birikiminden değil.

---

## 5. Unity kaynak dosyaları

```
unity/Assets/Scripts/
├── Model/
│   └── StatKind.cs                    5 stat, DB kolonlarıyla eşleşen enum
├── UI/
│   ├── StatRepeatTuning.cs            Eğri ayarları (ScriptableObject)
│   ├── HoldRepeatButton.cs            Basılı-tutma tekrarlayan buton
│   └── StatAllocationPanel.cs         Panel: 5 stat, +/-, onayla/sıfırla
└── Net/
    ├── IStatAllocationService.cs      Sunucu arayüzü
    └── MockStatAllocationService.cs   Sunucu yoksa test için taklit servis
```

### 5.1 `StatRepeatTuning` — ScriptableObject

Eğriyi Inspector'dan ayarlanabilir yapar. Varsayılanlar yukarıdaki analizden
geliyor.

**Önemli:** Bu değerleri değiştirirsen `tools/analyze_hold_repeat.py`
içindeki sabitleri de aynı yap ve betiği çalıştır. Yoksa analiz ile oyun
birbirinden kopar ve analiz yalan söylemeye başlar. Koşum (`check.sh --run`)
tam bu kopmayı yakalamak için var.

Asset oluşturma: `Assets → Create → Koray → UI → Stat Repeat Tuning`

### 5.2 `HoldRepeatButton` — genel amaçlı

Stat paneli için yazıldı ama her yerde kullanılır: envanterde yığın bölme,
mağazada adet seçme, kasa transferi.

Üç tasarım detayı:

| Karar | Gerekçe |
|---|---|
| `Update()`, coroutine değil | Coroutine + `WaitForSeconds` kare hızına kilitlenir; 30 FPS'te tekrar hızı yarıya düşer |
| `Time.unscaledDeltaTime` | Panel açıkken oyun duraklatılmış olabilir (`timeScale = 0`); ölçeklenmiş zamanla buton hiç tekrar etmez |
| `pointerId` takibi | Çok dokunuşlu ekranda başka parmağın kalkması basmayı bitirmesin |

Ayrıca `IPointerExitHandler` ile parmak butonun dışına kayarsa tekrar durur —
yoksa oyuncu parmağını kaydırıp puanlarını farkında olmadan harcar.

`RemainingCapacity` delegesi önemli: buton her tick'te "daha kaç puan
ekleyebilirim?" diye sorar. 0 dönerse tekrar kendiliğinden durur, yani puan
bittiğinde buton boşa çalışmaz.

### 5.3 `StatAllocationPanel` — "beklemede" mantığı

Oyuncunun bastığı her puan **anında sunucuya gitmez.** Yerel bir beklemede
tablosunda toplanır, ekranda önizleme olarak gösterilir, oyuncu "Onayla"ya
bastığında **tek istek** gider.

Üç faydası var:

1. **Ağ.** 297 puan 66 tick üretir. Tick başına paket göndermek saniyede 20
   paket demektir; 1000 oyuncuda sunucuyu boşa döversin. Tek istek bunu
   66 kat azaltır.
2. **Geri alma.** Oyuncu yanlış dağıttıysa "Sıfırla" ile geri alır. Onaydan
   sonra geri alınamaz — bu da kasıtlı.
3. **Tutarlılık.** Sunucu reddederse istemci tutarsız kalmaz. Beklemede olan
   **korunur** (oyuncu bilgi kaybetmesin), hata mesajı gösterilir.

**Sunucu yetkilidir.** İstemci "gücüm artık 500" demez; "güce +120 vermek
istiyorum" der. Sunucu puanın gerçekten var olduğunu doğrular ve **nihai**
değerleri geri gönderir. Panel yalnızca o değerleri gösterir — kendi yerel
hesabını asla doğru kabul etmez. Bu, `docs/01` Bölüm 6.2'deki sunucu-yetkili
tasarımın bu ekrandaki karşılığı.

### 5.4 `MockStatAllocationService` — sunucudan önce test

Sunucu henüz yazılmadan paneli çalıştırabilmen için. Ağ gecikmesini taklit
eder ve `FailureRate` ile hata döndürebilir — böylece "istek başarısız olursa
arayüz ne yapıyor" yolunu da test edersin. Çoğu hata o yolda bulunur.

Gerçek sunucu hazır olduğunda bu bileşeni sahneden çıkarıp
`IStatAllocationService`'i uygulayan gerçek istemciyi takarsın. Panel kodu
değişmez.

---

## 6. Sahnede nasıl kurulur

1. **Tuning asset'i oluştur:** `Assets → Create → Koray → UI → Stat Repeat Tuning`
2. **Panel nesnesi:** boş GameObject'e `StatAllocationPanel` ekle.
3. **Her stat için bir satır:** `Rows` dizisini 5'e çıkar, her satıra:
   - `Stat` = ilgili `StatKind`
   - `PlusButton` / `MinusButton` = üzerinde `HoldRepeatButton` olan UI nesneleri
   - `ValueLabel`, `PendingLabel`, `NameLabel` (sonraki ikisi opsiyonel)
4. **Her butona** `HoldRepeatButton` ekle ve `Tuning` alanına asset'i ata.
   Butonun bir `Image` bileşeni olmalı (`Raycast Target` açık), yoksa dokunma
   algılanmaz.
5. **Genel alanlar:** `UnspentLabel`, `CommitButton`, `ResetButton`, `ErrorLabel`.
6. **Servis:** sahneye `MockStatAllocationService` ekle.
7. **Başlatma** — panel açılırken:

```csharp
var service = FindObjectOfType<MockStatAllocationService>();
panel.Initialize(service, service.Snapshot(), service.UnspentPoints);
```

Gerçek sunucuyla:

```csharp
panel.Initialize(myNetworkService, characterStats, character.UnspentStatPoints);
```

### TextMeshPro kullanacaksan

Kod `UnityEngine.UI.Text` kullanıyor (ek paket bağımlılığı olmasın diye).
TMP'ye geçmek için `StatAllocationPanel.cs` içindeki `Text` tiplerini
`TMP_Text` yap ve `using TMPro;` ekle — başka değişiklik gerekmiyor.
`docs/01` Bölüm 6.1'de TextMeshPro önerilmişti; yayına çıkarken geçmen iyi olur.

---

## 7. Doğrulama

Kodun gerçekten derlendiğini ve analizle aynı sonucu verdiğini iddia etmek
yerine ölçtüm. Unity kurulu olmadığı için `unity/Assets/Scripts` altındaki
kodu, minimal bir UnityEngine saplamasıyla Mono derleyicisinde derledim ve
çalıştırdım:

```bash
apt-get install -y mono-mcs                      # tek seferlik
bash tools/unity-compile-check/check.sh          # yalnız derleme
bash tools/unity-compile-check/check.sh --run    # derleme + doğrulama koşumu
```

Koşum şunları kontrol eder:

| Kontrol | Sonuç |
|---|---|
| Derleme (uyarılar hata sayılarak) | temiz |
| 7 puan senaryosunda C# ↔ Python | ≤ 3 ms fark |
| Kısa dokunuş (50–340 ms) tek puan ekliyor mu | evet |
| Puan bitince tekrar duruyor mu, taşma var mı | duruyor, taşma yok |
| Kare hızı bağımsızlığı (30/60/120/240 FPS) | yayılım 17 ms |

**Bunun kapsamadıkları:** çalışma zamanı davranışı Unity'de farklı olabilir;
serileştirme, Inspector bağlantıları, prefab kurulumu ve gerçek dokunma
girdisi doğrulanmadı. Saplama Unity'nin kendisi değil. Paneli Unity'de açıp
elinle test etmen gerekiyor — ama sözdizimi, tip ve zamanlama mantığı
doğrulanmış durumda.

---

## 8. Eklemediklerim

- **Titreşim/ses geri bildirimi.** `HoldRepeatButton.PressedChanged` ve
  `Repeated` olayları hazır; `Handheld.Vibrate()` veya bir tick sesi bağlamak
  sana kalıyor. Her tick'te titreştirme — 66 tick'te telefon titrer durur;
  adım eşiği değiştiğinde titreştir.
- **Stat sıfırlama (reset scroll).** Dağıtılmış puanları geri alma ekonomisi
  bir tasarım kararı; şema tarafında `item_ledger`'a kaydedilmesi gerekir.
- **Önizleme hesabı.** "Güce +120 verirsem hasarım ne olur?" göstermek için
  istemci tarafında stat→hasar formülünün bir kopyası gerekir. Sunucudaki
  formülle ikiye ayrılmaması için paylaşılan bir derleme hedefinden gelmeli.
- **Beceri puanı paneli.** `level_curve.skill_points` var; aynı bileşenler
  beceri puanı için de kullanılabilir, `HoldRepeatButton` bu yüzden genel
  amaçlı yazıldı.
