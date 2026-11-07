# MykoMobile APK — Statik Analiz Raporu

> Tarih: 7 Kasım 2026
> İncelenen dosya: `MykoMobileOnline1.1.apk`, resmî dağıtım adresinden indirildi
> (`development.mykomobile.com`)
> Boyut: 152.561.458 bayt (~145 MB) · MD5 `492d138e2fa646c25c1a1937a1799db5`
> Dosya tarihi: 12 Kasım 2025
>
> Yöntem: yalnızca **statik** analiz — arşiv listesi, binary manifest çözümü,
> imza sertifikası, IL2CPP metadata ve Unity varlık dosyalarında dizge taraması.
> Oyun çalıştırılmadı, trafiği dinlenmedi, hiçbir varlık çıkarılıp yeniden
> kullanılmadı.

---

## 0. En önemli üç bulgu

**1. Bu bir Knight Online sunucu dosyası (Ebenezer) istemcisi DEĞİL.**
APK içinde Knight Online protokolünün hiçbir izi yok — `WIZ_` ile başlayan 289
opcode'dan **sıfırı** bulundu. Bunun yerine `NNetwork.dll` adlı kendi ağ
katmanı ve kendi opcode kümeleri (`MagicOpCodes`, `BuffOpcodes`,
`ChatNormalOpcodes`) var. Yani **sunucu tarafı da özgün yazılmış**, sızdırılmış
Mgame sunucu dosyaları değil.

> ⚠️ Bu bulgu, `docs/01-mykomobile-altyapi-analizi.md` dokümanında yaptığım bir
> varsayımı çürütüyor. Orada MykoMobile'ı klasik bir KO özel sunucusu (Ebenezer +
> MSSQL `KN_online`) varsaymıştım. **Yanlıştı.** Düzeltme o dokümanın başına
> eklendi.

**2. İstemci, başka bir oyunun kod tabanından geliyor: Nowa Online World.**
Manifest'teki derin bağlantı şeması hâlâ `com.NOWAGames.NOWAOnlineWorldA`.
Derlenmiş kodda `SetNOWALogin` metodu ve `NOWAOnlineWorld3` dizgesi, oyun
varlıklarının içinde ise `www.nowaonlineworld.com` ve `nowa-logo` duruyor.
Nowa Online World, **NOWA GAMES TEKNOLOJİ A.Ş.** adlı Türk stüdyonun yaklaşık 4
yıllık geliştirme sonrası Aralık 2024'te çıkardığı mobil MMORPG'si.

**3. Nowa'nın kaçındığı hukuki riski MykoMobile geri eklemiş.**
Nowa Online World, App Store'da ırkları **"Orc" ve "Human"** gibi jenerik
adlarla sunuyor. MykoMobile'ın derlemesinde her iki isimlendirme **birlikte**
duruyor: Nowa'nın `ORCNation`/`HUMANNation`'ı yanında Knight Online'ın
`KARUS_WARRIOR`, `ELMORAD_MAGE_FEMALE`, `KarusClassToRaces` sabitleri. Varlıklar
içinde KO'nun harita adları da var: `Moradon`, `eslantzone`.
Yani jenerik isimli özgün bir oyun, **Knight Online kimliğine geri boyanmış.**

---

## 1. Kimlik ve imza

| Alan | Değer |
|---|---|
| Paket adı | `com.mykomobileonline` |
| `versionCode` / `versionName` | 41 / "1" |
| Derin bağlantı şeması | **`com.NOWAGames.NOWAOnlineWorldA`** ← orijinal proje kimliği |
| İmza sahibi | `O=KNGames` (kendinden imzalı) |
| Sertifika geçerlilik | 27 Kas 2023 → 21 Eki **2173** (150 yıl) |
| İmza algoritması | **SHA1withRSA** — zayıf, keytool uyarı veriyor |
| Anahtar | 2048-bit RSA |
| SHA-256 parmak izi | `03:61:B7:30:D1:AC:B4:3F:23:89:8F:20:52:FC:00:94:05:8F:6F:FA:25:A3:DD:A7:80:B2:02:AD:98:B4:0F:9D` |

**Notlar:**
- Sertifikanın Kasım 2023'te üretilmiş olması, projenin en az 2 yıllık olduğunu gösteriyor.
- `O=KNGames` — site, marka ve bayiler "MykoMobile" derken imza "KNGames" diyor; ortada tüzel kişilik beyanı yok.
- SHA1withRSA 2026'da kullanılmaması gereken bir imza algoritması. Google Play bu imzayla yükleme kabul etmez — mağaza dışı dağıtımın bir başka sebebi.

---

## 2. Motor ve teknoloji yığını (kesin)

| Katman | Tespit | Kanıt |
|---|---|---|
| Motor | **Unity 2021.3.45f2** (2021 LTS — Unity desteği sona ermiş) | `libunity.so` ve `data.unity3d` başlığındaki sürüm dizgesi |
| Betik arka ucu | **IL2CPP** (C# → C++ → native) | `libil2cpp.so` 72.9 MB (arm64) + `global-metadata.dat` 12.96 MB |
| Render hattı | **URP** (Universal Render Pipeline) | `Unity.RenderPipelines.Universal.Runtime.dll` |
| Derleyici optimizasyonu | **Burst** + Jobs | `lib_burst_generated.so`, `Unity.Burst.dll`, `Unity.Collections.dll` |
| Sesli sohbet | **Vivox** (Unity Gaming Services) | `libvivox-sdk.so` 12.1 MB, `libVivoxNative.so`, `Unity.Services.Vivox.dll` |
| Ağ | **Elle yazılmış TCP** + kendi opcode sistemi | `NNetwork.dll`, `TcpClient`, `NetworkStream`, `MagicOpCodes`, `BuffOpcodes` |
| Serileştirme | Newtonsoft.Json + Odin Serializer | `Newtonsoft.Json.dll`, `Sirenix.Serialization.dll` |
| İçerik dağıtımı | **AssetBundle**, uzaktan indirme | `AssetBundle*` API'leri, `development.mykomobile.com` |
| Desteklenen ABI | `arm64-v8a`, `armeabi-v7a` — **x86 yok** | `lib/` dizini |
| Grafik gereksinimi | OpenGL ES 3.0 **zorunlu**, Vulkan opsiyonel | manifest `uses-feature` |

### Kullanılan üçüncü taraf eklentileri (Asset Store)

Metadata'dan çıkan assembly listesi, ekibin hazır eklentilere yoğun şekilde dayandığını gösteriyor:

| Eklenti | İşlev |
|---|---|
| **Odin Inspector / Serializer** (Sirenix) | Editör arayüzü ve serileştirme |
| **DOTween Pro** | Animasyon/tween |
| **Cinemachine** | Kamera |
| **TextMeshPro** | Metin render |
| **MagicaCloth V2** | Pelerin/kumaş fiziği |
| **Toony Colors Pro 2** | Stilize karakter shader'ı |
| **All In 1 VFX Toolkit** | Görsel efektler |
| **Damage Numbers Pro** | Hasar sayıları |
| **MeshCombineStudio** | Mesh birleştirme (mobil performans) |
| **Advanced Culling System** | Görünürlük optimizasyonu |
| **Bakery** | Lightmap pişirme |
| **Stylized Water 2** | Su yüzeyi |
| **Kino Bloom**, Postprocessing | Post-efekt |
| **SRDebugger** (StompyRobot) | Cihaz üstü hata ayıklama paneli |
| **AFPSCounter** (CodeStage) | FPS göstergesi |
| **AppleAuth** | Apple ile giriş |
| Unity Services: Analytics, Authentication, RemoteConfig, Vivox | Bulut servisleri |

**Bu liste senin için iyi haber:** Bu ölçekte bir mobil MMORPG istemcisinin
büyük kısmı hazır eklentilerle kuruluyor. Sıfırdan shader, kumaş fiziği veya
kamera sistemi yazmak zorunda değilsin.

---

## 3. Arka uç (sunucu) yüzeyi

Kodda gömülü adresler:

| Adres | İşlev |
|---|---|
| `https://loginapi.mykomobile.com/api` | **Giriş / kimlik doğrulama API'si** |
| `www.mykomobile.com/api.php` | **PHP** tabanlı web API |
| `development.mykomobile.com/` | Yama ve AssetBundle indirme ana makinesi |
| `https://forum.mykomobile.com/index.php` | Forum (XenForo tipi) |
| `https://mykomobile.com/register`, `/forgot-password`, `/privacy-policy` | Web akışları |

**Çıkarımlar:**
- Kimlik doğrulama HTTPS REST üzerinden (`loginapi...`), oyun akışı ayrı TCP bağlantısıyla. Bu, Bölüm 6.2'de önerdiğim Gateway + World Server ayrımının aynısı — mantıklı bir tasarım.
- Web tarafı **PHP** (`api.php`). Oyun sunucusunun dili buradan anlaşılmıyor; istemci C#, sunucu muhtemelen C# veya C++ ama APK bunu kanıtlamıyor.
- Oyun içeriği AssetBundle olarak çalışma anında indiriliyor: APK 145 MB ama sitede **2 GB depolama** isteniyor. Fark buradan geliyor.

---

## 4. İzinler ve gizlilik

```
INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
RECORD_AUDIO, MODIFY_AUDIO_SETTINGS          ← Vivox sesli sohbet
BLUETOOTH (≤30), BLUETOOTH_CONNECT (≥31)     ← ses cihazı yönlendirme
READ_PHONE_STATE                             ← cihaz kimliği
READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
uses-feature android.hardware.microphone required="true"   ← ZORUNLU
```

Dikkat çeken üç nokta:

1. **Mikrofon `required="true"`.** Yani mikrofonu olmayan cihaz oyunu kuramaz. Sesli sohbet opsiyonel bir özellik olmalıyken donanım şartı yapılmış — büyük olasılıkla dikkatsizlik, ama kurulabilir cihaz havuzunu daraltıyor.
2. **`READ_PHONE_STATE`.** Cihaz tanımlama için; Android 10+ sonrası zaten IMEI vermiyor. Genelde ban kaçışını tespit için konur. KVKK açısından açık rıza ve aydınlatma gerektirir.
3. **Faturalandırma izni YOK.** `com.android.vending.BILLING` yok → uygulama içi satın alma yok. Ödeme tamamen oyun dışında (site + bayiler) yürüyor. Bu, mağaza komisyonundan kaçınma değil zorunluluk: mağaza dışı dağıtımın doğal sonucu.

**`extractNativeLibs="true"`** — native kütüphaneler kuruluma açılıyor; 202 MB'lık `lib/` dizini diskte iki kez yer kaplıyor. Modern pratik `false`'tur.

---

## 5. Minimum sürüm tutarsızlığı

| Kaynak | Android minimum |
|---|---|
| Resmî site (sistem gereksinimleri) | **Android 7.0** |
| APK manifest (`minSdkVersion=22`) | **Android 5.1** |

APK teknik olarak Android 5.1'e kurulur ama site 7.0 diyor. İkisinden biri
güncellenmemiş. `targetSdkVersion=34` (Android 14) güncel — yani ekip
hedef SDK'yı takip ediyor, minimumu ise unutmuş.

---

## 6. İçerik ölçeği

| Bileşen | Boyut |
|---|---|
| `libil2cpp.so` (arm64) | 72.9 MB |
| `libil2cpp.so` (armv7) | 65.2 MB |
| `data.unity3d` (oyun varlıkları) | 57.1 MB |
| `libunity.so` (arm64 + armv7) | 32.8 MB |
| `global-metadata.dat` | 13.0 MB |
| Vivox kütüphaneleri | 29.7 MB |
| `sharedassets0.resource` | 11.4 MB |
| `classes.dex` (Java katmanı) | **0.2 MB** |

`classes.dex`'in sadece 200 KB olması, Java tarafında neredeyse hiç kod
olmadığını, her şeyin C# → IL2CPP içinde olduğunu gösteriyor. Standart Unity
yapısı.

**Dil desteği:** Türkçe, İngilizce, Rusça, Arapça.

---

## 7. Bu analizin senin projen için anlamı

### 7.1 İyi haber: hedef sandığından erişilebilir

MykoMobile, dev bir stüdyo ürünü değil. Yığını şu: **Unity LTS + IL2CPP + URP +
bir tutam Asset Store eklentisi + elle yazılmış TCP protokolü + PHP web
arka ucu.** Bunların hepsi öğrenilebilir, çoğu satın alınabilir. Teknoloji
duvarı yok.

Ayrıca mimari tercihleri, `docs/01` dokümanında önerdiğim mimariyle büyük
ölçüde örtüşüyor: HTTPS üzerinden ayrı giriş API'si, ayrı TCP oyun bağlantısı,
AssetBundle ile uzaktan içerik. Yani o yol haritası gerçeklikle uyumlu.

### 7.2 Doğrulanmış teknik dersler

| Onların yaptığı | Senin yapman gereken |
|---|---|
| Unity 2021 LTS (desteği bitmiş) | **Unity 6 LTS** ile başla; 2021 bugün yeni proje için yanlış seçim |
| SHA1withRSA imza | SHA-256; ayrıca Play App Signing kullan |
| `minSdkVersion=22` ile site 7.0 çelişkisi | Tek doğru kaynak tut; manifest ile sitenin yazdığı aynı olsun |
| Mikrofon `required="true"` | Sesli sohbet **opsiyonel** olsun; donanım şartı koyma |
| `extractNativeLibs="true"` | `false` — kurulum boyutu yarıya iner |
| x86 ABI yok | Emülatör/Chromebook istiyorsan x86_64 ekle |
| Mağaza dışı dağıtım, faturalandırma izni yok | **Play Billing + StoreKit 2** ile mağaza içi kal |
| Kendi TCP protokolü, kendi opcode'ları | Aynı yaklaşım doğru — ama sunucu yetkili doğrulamayı baştan kur |
| İçerik AssetBundle ile uzaktan | Aynısını yap; APK'yı küçük tut, içeriği indir |

### 7.3 Kötü haber: hukuki durum daha kötü, daha karmaşık

`docs/01` Bölüm 4'te Mgame'in Ocak 2025'teki davasını anlatmıştım. APK analizi
tabloyu **iki kat riskli** hale getiriyor, çünkü artık iki ayrı hak sahibi var:

**Risk 1 — Mgame (Knight Online).**
Kodda `KARUS_*` ve `ELMORAD_*` sabitleri, varlıklarda `Moradon` ve
`eslantzone` duruyor. Pazarlama doğrudan "Knight Online Mobile" diyor. Mgame'in
Ocak 2025'te açtırdığı dava tam olarak bu olgu örüntüsüne dayanıyordu ve
bilirkişi "KNIGHT ibaresinin tescilli markanın ayırt edici unsuru olarak
kullanıldığını" tespit etmişti.

**Risk 2 — Nowa Games.**
İstemcinin kod tabanı Nowa Online World'den geliyor; derin bağlantı şeması,
`SetNOWALogin` metodu ve varlıklardaki `nowa-logo` / `www.nowaonlineworld.com`
bunu gösteriyor. Bunun iki açıklaması olabilir:

- **(a) Lisanslı kullanım.** MykoMobile, Nowa Games'ten kod tabanını satın almış veya lisanslamış olabilir. Bu durumda kalıntı dizgeler sadece temizlenmemiş iz olur.
- **(b) İzinsiz kullanım.** Kod tabanı izinsiz alınmış olabilir.

**Hangisi olduğunu APK'dan anlamak mümkün değil** ve bir iddiada bulunmuyorum.
Ama senin açından sonuç ikisinde de aynı: **"MykoMobile altyapısı" diye sana
satılan şey, satıcının sahibi olmadığı bir kod tabanı olabilir.** (a) ise
lisans Nowa ile MykoMobile arasındadır, sana devredilemez. (b) ise zaten
baştan sorunlu.

### 7.4 Değişen tavsiye — ve değişmeyen

**Değişen:** Önceki dokümanda "B yolu (hazır altyapı satın alma)" için temel
itirazım, devralacağın kodun 2004'ten kalma sızdırılmış C++ olması ve düz metin
şifre gibi kusurlar taşımasıydı. **Bu itiraz MykoMobile için geçerli değil** —
kod modern (Unity 2021, C#, kendi protokolü). Teknik kalite sandığımdan iyi.

**Değişmeyen, hatta güçlenen:** İtirazın ağırlık merkezi artık tamamen
sahiplik ve hukukta. Satın alacağın şey:
- Sahibinin kim olduğu belirsiz bir kod tabanı (Nowa Games izi),
- İçine Knight Online'ın tescilli isimleri gömülmüş (Mgame riski),
- Google Play ve App Store'a giremeyen bir imza ve dağıtım modeli,
- Dolayısıyla meşru ödeme altyapısı kuramayan bir ürün.

Yani: **teknik gerekçe zayıfladı, hukuki gerekçe güçlendi. Tavsiyem aynı kalıyor —
C yolu: kendi oyununu kendi kodunla ve kendi isimlerinle yap.**

Üstelik APK bunun yapılabilir olduğunu kanıtlıyor: Nowa Games tam olarak bunu
yaptı. KO benzeri bir mobil MMORPG'yi **jenerik isimlerle** (Orc/Human) kurup
App Store'a soktu. Sen de aynı yolu izleyebilirsin — ve `KARUS_*` sabitlerini
eklemediğin sürece Risk 1'den tamamen uzak kalırsın.

---

## 8. Analizin sınırları

Dürüst olmak gerekirse bu analizin cevaplamadığı şeyler:

- **Sunucu tarafının dili ve mimarisi bilinmiyor.** APK sadece istemciyi içerir. `api.php` web tarafının PHP olduğunu gösteriyor, oyun sunucusu için kanıt yok.
- **Ağ protokolünün ayrıntıları çıkarılmadı.** Opcode sınıflarının varlığını gördüm; gerçek paket düzenini çıkarmak IL2CPP'yi tersine çevirmeyi gerektirir. Bunu yapmadım, senin projen için gereği de yok — kendi protokolünü yazacaksın.
- **Varlıkların sanatsal kökeni belirlenmedi.** Model ve doku dosyalarının KO'dan mı alındığı, Nowa'nın özgün üretimi mi olduğu ayrı bir inceleme konusu. Varlıkları çıkarıp incelemedim; bu, kullanmak niyetinde olmadığın içeriği kopyalamaya yaklaşmak olur.
- **Nowa Games ile MykoMobile arasındaki ilişki bilinmiyor.** Lisans var mı yok mu, dışarıdan görünmüyor.
- **iOS derlemesi incelenmedi.** Yalnızca Android APK.

Merak ettiğin belirli bir nokta varsa söyle; bu dosya üzerinden daha derin
bakabilirim.

---

## 9. Kaynaklar

- APK: `https://development.mykomobile.com/MykoMobileOnline1.1.apk` (resmî indirme bağlantısı, `mykomobile.com/en/download-game` sayfasından)
- [AA — Nowa Games'in yeni mobil MMORPG oyunu kullanıcılarla buluşuyor](https://www.aa.com.tr/tr/isdunyasi/teknoloji/nowa-gamesin-yeni-mobil-mmorpg-oyunu-kullanicilarla-bulusuyor/692029)
- [Donanım Haber — Nowa Online World, 4 yıllık geliştirme sürecinin ardından](https://www.donanimhaber.com/nowa-online-world-4-yillik-gelistirme-sureci--185097)
- [Nowa Online World — App Store](https://apps.apple.com/tr/app/nowa-online-world/id6698880492) (sağlayıcı: NOWA GAMES TEKNOLOJI ANONIM SIRKETI)
- [Sabah — Mgame davası, Ocak 2025](https://www.sabah.com.tr/teknoloji/2025/01/07/yuz-binlerin-oynadigi-online-oyun-davalik-oldu-oyunu-kopyalayip-markayi-ihlal-edenler-icin-5-yil-hapis-istendi)
