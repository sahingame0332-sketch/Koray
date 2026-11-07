# MykoMobile Altyapısı: Teknik Analiz ve Kendi Oyununu Yapma Yol Haritası

> Hazırlanma tarihi: 7 Kasım 2026
> Bu doküman, `sahingame0332-sketch/Koray` deposu için hazırlanan teknik inceleme ve yönlendirmedir.
> **Hukuki tavsiye değildir.** Hukuki bölüm, kamuya açık haber ve proje metinlerinden derlenmiştir.

---

> ### ⚠️ DÜZELTME — 7 Kasım 2026, APK analizinden sonra
>
> Bu doküman ilk yazıldığında MykoMobile'ı **klasik bir Knight Online özel sunucusu**
> (sızdırılmış Ebenezer sunucu dosyaları + MSSQL `KN_online`) varsaymıştım.
> APK'yı indirip inceledikten sonra **bu varsayım yanlış çıktı.**
>
> Gerçek durum: MykoMobile istemcisinde Knight Online protokolünün hiçbir izi yok
> (289 `WIZ_` opcode'undan sıfırı). Kendi `NNetwork.dll` ağ katmanı ve kendi
> opcode'ları var. Kod tabanı, Türk stüdyo **NOWA GAMES**'in *Nowa Online World*
> oyunundan geliyor. Yani ortada 2004 C++ kodu değil, modern Unity + C# kodu var.
>
> **Bu dokümanın hangi kısımları hâlâ geçerli:**
> - Bölüm 3 (Knight Online altyapısının anatomisi) — doğru, ama MykoMobile'ı değil
>   *klasik KO özel sunucularını* anlatıyor. Mimariyi öğrenmek için hâlâ değerli.
> - Bölüm 4 (hukuki durum) — geçerli ve APK bulgularıyla **daha da ağırlaştı**.
> - Bölüm 6-7 (önerilen mimari ve yol haritası) — geçerli; APK, bu mimarinin
>   gerçek ürünlerde kullanıldığını doğruladı.
>
> **Değişen:** Bölüm 5'teki "B yolu" itirazım artık teknik değil, tamamen
> sahiplik ve hukuk üzerine. Ayrıntısı: **[`02-apk-analizi.md`](02-apk-analizi.md)**
> Bölüm 7.4.

## 0. Özet (önce bunu oku)

Üç cümlede durum:

1. **MykoMobile bir Knight Online özel sunucusudur** (private server) ve PC istemcisi yerine kendi mobil istemcisiyle çalışır. Kendi sitesinin `<title>` etiketi bunu açıkça yazıyor: `MykoMobile | Knight Online Mobile`.
2. **"MykoMobile altyapısı" diye satın alabileceğin şey**, APK analizine göre 2004 kodu değil — Unity 2021 LTS + C# ile yazılmış, kendi ağ protokolü olan modern bir istemci. Ama kod tabanı başka bir stüdyoya (NOWA GAMES) ait görünüyor ve içine Knight Online'ın tescilli isimleri gömülmüş. Yani sorun teknik değil, **sahiplik.**
3. Mgame Corporation, Ocak 2025'te Türkiye'de tam olarak bu işi yapan iki kişi hakkında — "Knight Online Mobile Versiyon" adıyla kopya dağıtmak — **kişi başı 5 yıla kadar hapis istemiyle** dava açtırdı. Ticari gelir (cash/gold satışı) bu riski katlar.

**Tavsiyem:** Bu altyapıyı *okul* olarak kullan, *temel* olarak kullanma. Oyun mekanikleri telif korumasında değildir; kod, grafikler, isimler ve haritalar korumadadır. Yani "KO'nun hissini veren kendi mobil MMORPG'ni" yapmak meşrudur — KO'nun dosyalarını çalıştırmak değildir. Bölüm 5'te üç yolu karşılaştırdım, Bölüm 6-7'de önerdiğim yolun somut mimarisi ve takvimi var.

---

## 1. Deponun mevcut durumu

`sahingame0332-sketch/Koray` **tamamen boş** — hiç commit yok, hiç dosya yok. Yani incelenecek mevcut bir kod tabanı yoktu; bu doküman sıfırdan başlama noktası olarak hazırlandı.

---

## 2. MykoMobile nedir? (doğrulanmış bulgular)

Bunların hepsi `mykomobile.com` üzerinden, 7 Kasım 2026'da doğrudan okunarak teyit edildi.

| Konu | Bulgu |
|---|---|
| Kimlik | Site başlığı: `MykoMobile | Knight Online Mobile - Hemen Telefonuna İndir` |
| Sunucular | İki dünya: **ARES** ve **DIEZ** (DIEZ 11 Eylül'de açılmış) |
| Android dağıtım | Google Play **değil** — doğrudan APK: `development.mykomobile.com/MykoMobileOnline1.1.apk` |
| iOS dağıtım | App Store **değil** — **TestFlight** daveti (`testflight.apple.com/join/...`) |
| Oyuncu iddiası | İndirme sayfasında "10K+ Player" |
| Site yığını | PHP + Tailwind CSS + Lucide ikonlar + Google Analytics; forum ayrı subdomain (`forum.mykomobile.com`, XenForo tipi URL yapısı) |
| Ekonomi | Hesap paneli (`usercp`), sıralamalar, NP avcısı, level ödülleri; cash satışı üçüncü taraf bayilerden (Klasgame vb.) |

**Sistem gereksinimleri (siteden birebir):**

| | Android min | Android önerilen | iOS min | iOS önerilen |
|---|---|---|---|---|
| RAM | 4 GB | 6 GB | 4 GB | 6 GB |
| CPU | 8 çekirdek 1.6 GHz | 8 çekirdek 2.84 GHz | 4 çekirdek 2.37 GHz | 6 çekirdek 2.65 GHz |
| OS | Android 7.0 | Android 10+ | iOS 14.0 | iOS 17.2+ |
| Depolama | 2 GB | 4 GB | 2 GB | 4 GB |

### Bu tablodan okunan iki önemli şey

- **4 GB RAM / 2 GB depolama minimumu**, mobil için ağır bir istemci demektir. Bu, PC varlıklarının (asset) mobile taşındığı bir yapıya işaret eder — sıfırdan mobil için optimize edilmiş bir oyun 300-800 MB bandında olur.
- **Ne Google Play ne App Store.** APK + TestFlight dağıtımı tesadüf değil: mağazaların telif/marka denetiminden geçmeyen bir ürünün tek dağıtım yolu budur. Senin kendi oyunun için bu **kabul edilemez** bir kısıt — mağazasız bir mobil oyun büyüyemez, ödeme altyapısı kuramaz, güven kazanamaz.

> `mykoonline.com` ayrı ve benzer bir proje (yine Android APK + iOS TestFlight). Yani bu, tek bir oyun değil, bir **ekosistem/akım**. "MYKO" kısaltmasının resmî bir açılımını hiçbir birincil kaynakta bulamadım; Türk oyuncu dilinde Knight Online özel sunucularının genel adı olarak kullanılıyor.

---

## 3. Klasik KO "altyapısı" teknik olarak ne demek? (incelediğim kaynak kod ve veritabanı)

> **Kapsam notu:** Bu bölüm *klasik Knight Online özel sunucu altyapısını* anlatır —
> MykoMobile'ın kendisini değil. MykoMobile'ın bu yapıyı kullanmadığı APK analiziyle
> ortaya çıktı (bkz. [`02-apk-analizi.md`](02-apk-analizi.md)). Bölümü yine de
> bırakıyorum: bir MMORPG'nin hangi verileri ve hangi süreçleri tutmak zorunda
> olduğunu, hangi tasarım hatalarından kaçınman gerektiğini en net gösteren kaynak bu.

Bu bölüm için şu üç projeyi indirip doğrudan inceledim:

- **[Open-KO/KnightOnline](https://github.com/Open-KO/KnightOnline)** — C++ sunucu + istemci, sürüm 1.298 hedefli, MIT lisanslı
- **[Open-KO/OpenKO-db](https://github.com/Open-KO/OpenKO-db)** — veritabanı şeması ve varsayılan veri seti (20 MB)
- **[co3moz/knightonline-js](https://github.com/co3moz/knightonline-js)** — aynı protokolün TypeScript + MongoDB + Redis ile modern yeniden yazımı

### 3.1 Süreç mimarisi — 5 ayrı Windows servisi

```
         Mobil/PC İstemci
                │ TCP
    ┌───────────┴────────────┐
    │                        │
VersionManager          Ebenezer                 AIServer
(login + patch)         (oyun sunucusu)          (canavar YZ)
port 15100-15109        port 15001               │
    │                        │                   │
    └────────► MSSQL ◄───────┴──── Aujard ◄──────┘
               KN_online      (DB ajanı)
                  ▲
                  └── ItemManager (eşya/log işleri)
```

- **Ebenezer** — asıl oyun sunucusu. 52 kaynak dosya; `User.cpp`, `MagicProcess.cpp`, `KnightsSiegeWar.cpp`, `Map.cpp`, `Region.h`. Yapılandırma `gameserver.ini` + ODBC DSN üzerinden.
- **AIServer** — canavar yapay zekâsı ayrı süreç olarak koşar, Ebenezer'a TCP ile bağlanır (`AISocket.cpp`).
- **Aujard** — veritabanı ajanı; kalıcılık işlerini üstlenir, böylece oyun döngüsü SQL beklemez.
- **VersionManager** — launcher'ın sürüm/patch sorgusu ve hesap girişi.
- **ItemManager** — eşya ve log işlemleri.
- Süreçler arası iletişim kısmen **paylaşımlı hafıza kuyruğu** ile (`SharedMemoryQueue.cpp`) — yani aynı makinede koşmak zorundalar. Yatay ölçeklenemez.

### 3.2 Ağ protokolü

İncelediğim `src/shared/packets.h` dosyasında **289 opcode, 50 ayrı enum grubunda** tanımlı. Paket yapısı:

```
0xAA 0x55 | uzunluk (uint16 LE) | opcode (uint8) | gövde | 0x55 0xAA
```

- Şifreleme: `JvCryption` — basit, simetrik, XOR temelli bir akış şifresi (`JvEncryptionFast` ile `JvDecryptionFast` **aynı fonksiyon**). Yanında CRC32 bütünlük kontrolü ve LZF sıkıştırma var.
- Örnek opcode'lar: `WIZ_LOGIN=0x01`, `WIZ_MOVE=0x06`, `WIZ_ATTACK=0x08`, `WIZ_MAGIC_PROCESS=0x31`, `WIZ_ITEM_MOVE=0x1F`.

**Güvenlik değerlendirmesi:** Bu bir TLS değil, 2004 yılının obfuscation'ı. Simetrik ve anahtarı istemcide gömülü. Yani protokol **kriptografik olarak korumasız** sayılmalı — bu yüzden KO sahnesinde bot/hile endemiktir (veritabanında `HACKTOOL_USERLOG` ve `PROGRAMLIST_LOG` tabloları olması tesadüf değil; sorun kaynakta çözülmediği için log tutarak yönetilmeye çalışılmış).

### 3.3 Veritabanı: `KN_online`

Rakamlarla:

| Ölçü | Değer |
|---|---|
| Veritabanı | MSSQL `KN_online`, şema `knight` |
| Tablo sayısı | **77** |
| Saklı yordam (stored procedure) | **70** |
| Kurulum SQL dosyası | 211 |
| Hazır eşya kaydı | **~61.530** (14 MB tek dosya) |
| Canavar kaydı | 723 |
| Beceri/büyü kaydı | 1.522 |
| NPC doğma noktası | 1.730 |
| Bölge (zone) | 20 |
| Seviye tablosu | 90 seviye |

**Çekirdek tablolar:**

| Tablo | İşlev |
|---|---|
| `TB_USER` | Hesap: `strAccountID`, `strPasswd`, `strEmail`, `strAuthority`, `PremiumExpire` |
| `USERDATA` | Karakter: sınıf, ırk, seviye, exp, 5 ana stat, altın, konum (`PX/PY/PZ`), envanter |
| `ACCOUNT_CHAR` | Hesap ↔ karakter eşlemesi (3 slot) |
| `ITEM` | 61 kolonlu eşya tanımı: hasar, AC, element hasarları, 5 stat bonusu, 6 direnç, istek şartları |
| `MAGIC` + `MAGIC_TYPE1..9` | Beceri sistemi: `MAGIC` ana tanım, `TYPE1` vurma/kombo, `TYPE2` menzilli, `TYPE3` sürekli hasar, `TYPE4` buff, vb. |
| `K_MONSTER`, `K_MONSTER_ITEM`, `K_NPC`, `K_NPCPOS` | Canavar/NPC tanımları, drop tabloları, doğma noktaları |
| `ZONE_INFO` | 20 bölge: başlangıç koordinatı, tip, oda eventi |
| `KNIGHTS`, `KNIGHTS_USER`, `KNIGHTS_ALLIANCE`, `KNIGHTS_SIEGE_WARFARE` | Klan sistemi, ittifaklar, kale kuşatması |
| `KING_SYSTEM`, `KING_ELECTION_LIST`, `KING_BALLOT_BOX` | Kral seçim sistemi (aday, oy, azil, vergi) |
| `WEB_ITEMMALL`, `COUPON_SERIAL_LIST`, `WEB_ITEMMALL_LOG` | Cash mağazası ve kupon sistemi |
| `WAREHOUSE`, `RENTAL_ITEM`, `ITEM_UPGRADE`, `ITEMUP_PROBABILITY` | Kasa, kiralık eşya, upgrade ve başarı oranları |
| `HACKTOOL_USERLOG`, `PROGRAMLIST_LOG` | Hile tespit logları |

### 3.4 Bu veritabanının ciddi tasarım kusurları

Burası dokümanın en önemli kısmı. **Bu kusurlar düzeltilebilir değil**, çünkü istemci protokolü bunlara bağlı. Kendi oyununu yaparken bunların hiçbirini tekrarlamamalısın.

**1) Şifreler düz metin ve 13 karakter sınırlı.**
```sql
[strPasswd] varchar(13) NOT NULL
```
Hash yok, salt yok. Bir sızıntıda bütün oyuncu şifreleri açığa çıkar — ve insanlar şifre tekrar kullandığı için zarar oyununla sınırlı kalmaz. Ayrıca KVKK açısından ağır bir ihmal.

**2) `strSocNo varchar(20)` — Kore kimlik numarası alanı.**
Kullanılmayan ama şemada duran bir kişisel veri alanı. Hazır altyapı satın alırsan bu alan içinde gerçek veri bulabilirsin; devraldığın an sorumluluğu da devralırsın.

**3) Envanter tek bir metin bloğu içinde paketli.**
```sql
[strItem]   varchar(400),   -- bütün envanter
[strSerial] varchar(400),   -- eşya serileri
[strQuest]  varchar(400)    -- görev durumu
```
`WAREHOUSE.WarehouseData` da aynı şekilde. Sonuçları:
- Tek bir eşyayı atomik güncelleyemezsin → **duplicate (dupe) hataları** KO sahnesinin klasik belasıdır, sebebi budur.
- "Bu eşya nereden geldi?" sorusunu veritabanından cevaplayamazsın. Denetim imkânsız.
- Envanter boyutu 400 bayta sabit. Büyütmek istemciyi bozar.
- Hiçbir SQL sorgusu "şu eşyaya sahip oyuncular" diye sorulamaz.

**4) `tinyint` tavanları.**
`Level tinyint` → en fazla 255. Bütün statlar (`Strong`, `Sta`, `Dex`, `Intel`, `Cha`) `tinyint` → 255 tavan. `Zone tinyint` → 255 bölge. Oyununu büyütme yolun şemayla kapatılmış.

**5) 70 saklı yordamda gömülü iş mantığı.**
`account_login`, `create_new_char`, `update_user_data`, `king_impeachment_election`... Oyunun kuralları T-SQL içinde. Bu demek: birim testi yazamazsın, sürüm kontrolü anlamlı diff vermez, MSSQL'den çıkamazsın, ve mantığı değiştirmek için üretim veritabanına dokunmak gerekir.

**6) Yabancı anahtar (FK) kısıtı ve normalizasyon yok.**
`USERDATA.Knights` bir klan ID'si tutar ama FK yok. Klan silinince karakterler hayalet ID'ye bakar. Veri tutarlılığını veritabanı değil, C++ kodu garanti etmeye çalışır — ve çoğu zaman başaramaz.

**7) Windows'a ve MSSQL'e çivilenmiş.**
OpenKO Linux/macOS'ta sadece sunucu kısmını derleyebiliyor; istemci ve araçlar Windows + Visual Studio gerektiriyor. Üretimde Windows Server + MSSQL lisansı demek — bulut maliyetin Linux + PostgreSQL'e göre belirgin şekilde yüksek.

### 3.5 İstemci tarafı

- PC istemcisi **N3Base** adlı özel bir motor üzerine kurulu (162 kaynak dosya): `N3Chr`, `N3Camera`, `N3Mesh`, `N3Terrain`, `N3Sky`. DirectX 9'a güncellenmiş eski bir DirectX 8 motoru. `.smd` (harita), `.n3cplayer` (karakter), `.tbl` gibi özel dosya formatları var; depoda bunlar için editör araçları da geliyor (`N3ME` harita editörü 155 dosya, `TblEditor`, `UIE` arayüz editörü).
- **Bu motor mobile taşınamaz.** Mobil MykoMobile istemcisi bu yüzden sıfırdan yazılmış olmalı — sahnedeki yaygın yöntem **Unity 3D** ile protokolü tersine mühendislikle konuşan yeni bir istemci yazmaktır. (Benzer bir sunucu olan KO1, istemcilerini Unity 3D ile geliştirdiklerini açıkça yazıyor.)
- **Güncelleme:** APK indirilip incelendi ve motor kesin olarak doğrulandı: **Unity 2021.3.45f2 + IL2CPP + URP**. Ayrıca MykoMobile'ın bu protokolü *konuşmadığı* ortaya çıktı — kendi ağ katmanı var. Ayrıntılar: [`02-apk-analizi.md`](02-apk-analizi.md).

---

## 4. Hukuki gerçeklik

Bu bölümü atlama. Teknik kararından daha belirleyici.

### 4.1 Kodun kökeni temiz değil

OpenKO'nun kendi README'si şunu yazıyor:

> "Starting with the original leaked source, we have updated to DirectX 9..."

Yani proje **sızdırılmış Mgame kaynak kodundan** başlıyor. Üstüne MIT lisansı konulmuş olması bunu değiştirmez — kimse sahibi olmadığı kodu lisanslayamaz. Aynı README ayrıca:

> "This project is strictly for academic purposes only."
> "This project **cannot currently be used for a real server**."

Yani projenin kendi geliştiricileri bunu ürün temeli olarak önermiyor.

> Ek not: OpenKO'ya katkı yapmayı düşünürsen, projenin katkı kuralları **yapay zekâ kullanımını açıkça yasaklıyor**. Oraya PR atacaksan kodu kendin yazmalısın.

### 4.2 Türkiye'de açılmış dava — senin planına çok yakın

Ocak 2025'te Sabah ve diğer kaynaklarda çıkan habere göre:

- **Mgame Corporation** savcılığa suç duyurusunda bulundu.
- İddia: şüpheliler oyunu `knightempire.online` üzerinden **"Knight Online Mobile Versiyon"** adıyla izinsiz kopyalayıp dağıttı.
- Bilirkişi raporu: Knight Online **FSEK kapsamında "eser"**, umuma iletim hakkı ihlal edilmiş; şüpheli **"KNIGHT" ibaresini tescilli markanın ayırt edici unsuru olarak** kullanmış.
- Sonuç: iki şüpheliye ayrı ayrı **5 yıla kadar hapis** istemiyle dava.

Haklar: geliştirici **Noah System + Mgame**, yayıncı **NTTGame**; marka Türkiye'de tescilli.

Dikkat et: bu dava **tam olarak "Knight Online'ın mobil versiyonu"** tanımlı bir iş için açıldı. Senin "MykoMobile altyapısıyla kendi oyunumu yapmak istiyorum" planı, hukuken aynı olgu örüntüsüne oturuyor. Üstüne cash/gold satarsan ticari kazanç unsuru da eklenir.

*(Davanın sonucunu açık kaynaklarda bulamadım. Bu bir hukuki görüş değil; karar vermeden önce bir Türk fikrî mülkiyet avukatıyla konuş.)*

### 4.3 Neyi yapabilirsin, neyi yapamazsın

| Serbest | Korumalı |
|---|---|
| Oyun **mekanikleri**: iki ulus savaşı, klan kuşatması, upgrade sistemi, parti avı, NP ekonomisi | Kaynak **kodu** (Ebenezer, AIServer, N3Base dahil) |
| **Tür ve his**: hızlı tempolu, PvP odaklı, nostaljik MMORPG | **Grafikler**: modeller, dokular, haritalar, UI, müzik, ses |
| **Fikirler**: sınıf arketipleri, stat tasarımı, ekonomi dengesi | **İsimler ve marka**: "Knight Online", "KNIGHT", bölge/eşya/NPC isimleri |
| Kendi yazdığın, kendi çizdiğin her şey | **Veri setleri**: o 61.530 eşya kaydı, 723 canavar, 1.522 beceri — derlenmiş eser |
| Mimariden **öğrenmek** | Sızdırılmış dosyaları **çalıştırmak/dağıtmak** |

**Kritik ayrım:** "KO gibi oynanan kendi oyunum" meşrudur. "KO'nun dosyalarını mobile taşımış halim" değildir.

---

## 5. Üç yol — karşılaştırma

| | A) Sadece öğrenme laboratuvarı | B) Hazır altyapı satın alma | C) Kendi oyununu sıfırdan yazma |
|---|---|---|---|
| Ne yaparsın | OpenKO'yu kendi makinende Docker ile çalıştırır, mimariyi incelersin | Satıcıdan sunucu dosyaları + web + launcher paketi alırsın | KO'dan ilham alan, kendi kodun ve kendi varlıklarınla oyun | 
| Süre | 1-2 hafta | 1-2 ay | 12-24 ay |
| Maliyet | ~0 | 500-5.000 USD + aylık sunucu | Zaman + varlık üretimi |
| Hukuki risk | Çok düşük (kapalı, ticari değil) | **Çok yüksek** — 4.2'deki dava örüntüsü + belirsiz kod sahipliği | Düşük (kendi eserin) |
| Mağaza (Play/App Store) | — | **İmkânsız** | Mümkün |
| Teknik kalite | — | MykoMobile örneğinde modern (Unity + C#); klasik KO altyapısında 2004 kodu, düz metin şifre, dupe açıkları | Senin belirlediğin |
| Sahiplik | — | Yok — satıcı kodu, kapalı kutu, destek yok | Tam sahiplik |
| Gelir modeli | Yok | Gri; ödeme sağlayıcıları kapatır | Meşru IAP |
| Çıkış/satış değeri | — | 0 | Devredilebilir varlık |

### Neden B'yi önermiyorum

**Önce bir düzeltme:** İlk yazdığımda bu bölümdeki itirazım teknikti — "devraldığın şey 2004'ten kalma, düz metin şifre tutan, dupe açıklı bir kara kutu". APK analizi bunu çürüttü: MykoMobile'ın kodu modern (Unity 2021, C#, kendi protokolü). Yani **teknik itirazım MykoMobile için geçerli değil.**

İtiraz şimdi üç başka noktada duruyor ve bunlar daha ağır:

1. **Sahiplik belirsiz.** APK'daki izler kod tabanının NOWA GAMES'e ait olduğunu gösteriyor. Satıcı bunu lisansladıysa lisans sana geçmez; lisanslamadıysa zaten baştan sorunlu. Her iki halde de **sahibi olmadığın bir şeyin üzerine şirket kuruyorsun.**
2. **İçine gömülü marka riski.** Kodda `KARUS_*`/`ELMORAD_*`, varlıklarda `Moradon`/`eslantzone`. Mgame'in Ocak 2025 davası tam bu olgu örüntüsüne dayandı.
3. **Mağazaya giremez.** SHA1 imza, faturalandırma izni yok, APK + TestFlight dağıtımı. Yani meşru ödeme altyapısı kuramazsın, kullanıcı edinimi yapamazsın ve oyununu bir gün satamazsın.

Ayrıntılı gerekçe: [`02-apk-analizi.md`](02-apk-analizi.md) Bölüm 7.

### Önerim: **C**, A'yı ön hazırlık olarak kullanarak

Önce 1-2 hafta A'yı yap — KO mimarisini *gerçekten* anlamak, kendi tasarımını yaparken paha biçilmez. Sonra C'ye geç.

---

## 6. C yolu için önerdiğim mimari

Aşağıdaki seçimler, "KO benzeri PvP odaklı mobil MMORPG, küçük ekip, 2026" kısıtına göre yapıldı.

### 6.1 Yığın (stack)

| Katman | Öneri | Gerekçe |
|---|---|---|
| **İstemci** | **Unity 6 LTS** (C#) | Android + iOS tek kod tabanı; KO benzeri mobil sahnenin fiilî standardı; hazır varlık ekosistemi. Alternatif: Godot 4.4 (ücretsiz, hafif, 3D MMO için daha az olgun). |
| **Sunucu dili** | **C# / .NET 9** | İstemciyle **aynı dil** → paket DTO'larını tek bir paylaşılan projeden üretirsin, protokol hatası sınıfı tamamen kaybolur. Alternatif: Go (daha iyi eşzamanlılık, kod paylaşımı yok). |
| **Ağ** | Kendi **TCP** (giriş, envanter, ticaret) + **UDP/KCP** (hareket, savaş) | Mirror/FishNet gibi kütüphaneler "host-based" oyunlar içindir, MMO için uygun değildir. Sunucu yetkili (server-authoritative) olmak **zorunlu**. |
| **Veritabanı** | **PostgreSQL 16+** | Normalize şema, gerçek FK, JSONB esnekliği, ücretsiz, Linux. MSSQL lisans maliyetine gerek yok. |
| **Önbellek/oturum** | **Redis 7** | Oturum, sıralama tabloları, oran sınırlama, bölge arası mesajlaşma. |
| **Kimlik** | **Argon2id** şifre hash + kısa ömürlü erişim jetonu | KO'nun düz metin hatasının tam tersi. |
| **Taşıma güvenliği** | **TLS** (giriş/ödeme) + oturum anahtarlı şifreleme (oyun akışı) | `JvCryption` türü gömülü simetrik anahtar **kullanma**. |
| **Dağıtım** | Docker Compose → sonra Kubernetes | Bölge (zone) başına ayrı süreç, yatay ölçekleme. |
| **Gözlemlenebilirlik** | OpenTelemetry + Prometheus + Grafana | KO'nun olmayan şeyi: ne olduğunu görebilmek. |
| **Mağaza/ödeme** | Google Play Billing + Apple StoreKit 2 | Meşru yol; sunucu tarafı makbuz doğrulaması şart. |

### 6.2 Süreç mimarisi

```
   Mobil istemci (Unity)
          │ TLS
    ┌─────▼─────┐
    │  Gateway  │  kimlik doğrulama, oran sınırlama, yönlendirme
    └─────┬─────┘
          │
    ┌─────▼──────────────────────────────┐
    │  World Server (bölge başına süreç) │
    │  - oyun döngüsü (tick 10-20 Hz)    │
    │  - savaş, beceri, hareket doğrulama│
    │  - ilgi alanı (interest management)│
    └──┬──────────────┬──────────────────┘
       │              │
  ┌────▼────┐   ┌─────▼─────┐
  │ Redis   │   │ Persist   │  toplu yazma, event sourcing
  └─────────┘   │ Service   │
                └─────┬─────┘
                ┌─────▼─────┐
                │PostgreSQL │
                └───────────┘
```

**KO'dan en önemli ayrılma noktaları:**

1. **Her eşya ayrı satır, ayrı ID.** Paketli metin yok. Her hareket bir denetim kaydı (`item_ledger`) üretir → dupe mümkün değil, her eşyanın geçmişi sorgulanabilir.
2. **Oyun mantığı saklı yordamda değil, uygulama kodunda.** Birim test yazılabilir, diff okunabilir, veritabanı değiştirilebilir.
3. **Sunucu yetkili hareket ve savaş.** İstemci "10 hasar vurdum" demez; "şuna saldırmak istiyorum" der, hasarı sunucu hesaplar. KO'nun bot/hile sorununun kök sebebi burada çözülür.
4. **`int`/`bigint` kullan, `tinyint` tavanı koyma.**
5. **Şifreyi asla düz saklamama.**

### 6.3 Başlangıç veritabanı şeması

Somut bir başlangıç noktası olarak normalize bir PostgreSQL şeması hazırladım:
**[`docs/schema/01_core_schema.sql`](schema/01_core_schema.sql)** — 26 tablo, 678 satır.

KO'nun yaptığı hataların her birine karşılık ne yaptığını dosyanın başındaki yorumda açıkladım.

**Bu şema iddia değil, test edildi.** PostgreSQL 16.15 üzerinde `ON_ERROR_STOP=1` ile hatasız kuruldu ve şu beş kısıtın gerçekten çalıştığı doğrulandı:

| Test | Beklenen | Sonuç |
|---|---|---|
| Aynı envanter slotuna ikinci eşya | Reddedilmeli | ✅ `character_item_slot_uniq` reddetti |
| Negatif altın | Reddedilmeli | ✅ `CHECK (gold >= 0)` reddetti |
| Olmayan şablona eşya | Reddedilmeli | ✅ FK reddetti |
| Beceri çubuğunda hem beceri hem eşya | Reddedilmeli | ✅ `CHECK` reddetti |
| Aynı mağaza makbuzunun ikinci kez işlenmesi | Reddedilmeli | ✅ `UNIQUE(platform, txn_id)` reddetti |

Birinci satır kritik: **KO'nun dupe açığı veritabanı seviyesinde kapatılmış durumda.** Ayrıca eşya geçmişi (`item_ledger`) sorgulanabiliyor — KO'da imkânsız olan şey.

Kurulum:
```bash
createdb oyun
psql -d oyun -f docs/schema/01_core_schema.sql
```

---

## 7. 0 → 1 yol haritası

Dürüst tahminler (1-3 kişilik ekip, part-time değil tam zamanlı varsayımıyla).

### Faz 0 — Öğrenme laboratuvarı (1-2 hafta)
- OpenKO'yu Docker ile ayağa kaldır: `docker compose up` → MSSQL + `KN_online` otomatik yüklenir.
- `packets.h` içindeki 289 opcode'u oku. Hangi oyun olayının hangi pakete karşılık geldiğini çıkar.
- `USERDATA`, `ITEM`, `MAGIC` tablolarını incele: bir MMORPG'nin hangi verileri tutmak zorunda olduğunu gör.
- **Çıktı:** "Hangi sistemleri istiyorum, hangilerini istemiyorum" listesi. Yazıya dök.

### Faz 1 — Dikey dilim (2-3 ay)
Hedef: **tek bölge, iki oyuncu, birbirini görüp vurabiliyor.** Oyun değil, kanıt.
- Gateway + tek World Server + PostgreSQL + Redis, Docker Compose ile.
- Kayıt/giriş (Argon2id), karakter oluşturma, 1 sınıf, 1 harita.
- Sunucu yetkili hareket + tek bir saldırı becerisi + HP/ölüm/doğma.
- Unity istemcisi: giriş ekranı, karakter, dokunmatik kontrol, isabet geri bildirimi.
- **Bu fazı geçemezsen proje bitmez. Buradaki zorluk projenin tamamını temsil eder.**

### Faz 2 — Çekirdek döngü (3-4 ay)
- Envanter + eşya (ayrı satır + ledger), NPC satıcı, altın.
- Canavarlar: doğma noktaları, YZ (gez/kovala/saldır), drop tabloları.
- 3-4 sınıf, sınıf başına 8-12 beceri, seviye/exp eğrisi.
- Parti sistemi, sohbet kanalları.
- Temel yönetici araçları (GM komutları, oyuncu arama, eşya verme — **ledger'a kaydıyla**).

### Faz 3 — PvP ve sosyal yapı (3-4 ay)
- Klan sistemi, iki ulus çatışması, NP/katkı puanı.
- PvP bölgesi, kuşatma veya arena etkinliği.
- Sıralamalar (Redis sorted set), oyuncu profilleri.
- Web paneli: hesap yönetimi, sıralamalar, duyurular.

### Faz 4 — Mağaza ve kapalı beta (2-3 ay)
- IAP: Google Play Billing + StoreKit 2, **sunucu tarafı makbuz doğrulama**.
- Yük testi: 500 → 2.000 eşzamanlı bot oturumu. Darboğazları bul.
- Hile karşıtı: sunucu tarafı mantık doğrulaması, anomali tespiti, oran sınırlama.
- Gizlilik politikası + KVKK uyumu + kullanım şartları. Mağaza başvurusu.
- Kapalı beta → TestFlight/Play Internal Testing (bu kez **meşru** olarak).

### Faz 5 — Yayın ve sonrası (sürekli)
- Bölgesel sunucu, CDN, destek kanalı, sezon/içerik takvimi.

**Toplam: 12-18 ay** mutlu senaryoda. Varlık (3D model, animasyon, ses) üretimini dışarıdan alırsan bütçe, kendin yaparsan takvim şişer.

---

## 8. Maliyet ve ekip gerçeği

| Kalem | Tahmin |
|---|---|
| Geliştirme sunucusu (ilk 12 ay) | 20-50 USD/ay (tek VPS yeter) |
| Üretim (2.000 eşzamanlı) | 300-800 USD/ay |
| 3D varlıklar (karakter, canavar, çevre) | 5.000-30.000 USD (veya asset store + kendi emeğin) |
| Unity | Kişisel gelir < 200K USD ise ücretsiz |
| PostgreSQL / Redis / Linux | 0 USD |
| Mağaza hesapları | 25 USD (Google, tek sefer) + 99 USD/yıl (Apple) |
| Hukuki danışmanlık (şirket + sözleşmeler + IP kontrolü) | **Atlamayın.** |

**Ekip gerçeği:** Tek kişiyle mobil MMORPG çıkarmak, 2026'da da mümkün ama nadirdir. Minimum ekip: 1 sunucu geliştirici, 1 Unity geliştirici, 1 3D sanatçı. Sen hangisiysen diğer ikisini bulmayı planla.

---

## 9. Şimdi yapmanı önerdiğim üç şey

1. **Bu dokümanı oku ve Bölüm 5'teki yolu seç.** A mı, B mi, C mi? Karar netleşmeden kod yazmanın anlamı yok. B'yi seçeceksen önce 4.2'yi bir avukata göster.
2. **Faz 0'ı yap.** OpenKO'yu Docker ile çalıştır, `packets.h`'yi oku, `USERDATA`'yı incele. Bir hafta. Bundan sonra ne istediğini çok daha net bileceksin.
3. **Oyun tasarım dokümanını yaz** — kopya değil, kendi oyunun. Hangi 4 sınıf? Hangi 2 ulus? Progresyon neye benziyor? Para nereden geliyor? 10 sayfa yeter, ama yazılı olsun.

Hazır olduğunda Faz 1'in iskeletini (Gateway + World Server + Unity bağlantısı, çalışan Docker Compose ile) bu depoda kurabiliriz. Söyle, başlayalım.

---

## 10. Kaynaklar

**İncelediğim kod tabanları**
- [Open-KO/KnightOnline](https://github.com/Open-KO/KnightOnline) — C++ sunucu + istemci, v1.298, MIT (ama sızdırılmış kaynaktan türemiş)
- [Open-KO/OpenKO-db](https://github.com/Open-KO/OpenKO-db) — 77 tablo, 70 saklı yordam, 20 MB veri seti
- [co3moz/knightonline-js](https://github.com/co3moz/knightonline-js) — TypeScript + MongoDB + Redis yeniden yazım, protokol dokümantasyonu iyi
- [ko4life-net/ko](https://github.com/ko4life-net/ko) — tersine mühendislik projesi
- [knight-online GitHub konusu](https://github.com/topics/knight-online) — sahnedeki diğer projeler

**MykoMobile birincil kaynaklar**
- [mykomobile.com](https://mykomobile.com/en/) — ana sayfa, sunucular (ARES, DIEZ)
- [Sistem gereksinimleri](https://mykomobile.com/en/system-requirements)
- [mykoonline.com — MYKO nedir?](https://mykoonline.com/rehber/myko-nedir/) — benzer ayrı proje

**Hukuki**
- [Sabah: "Yüz binlerin oynadığı online oyun davalık oldu"](https://www.sabah.com.tr/teknoloji/2025/01/07/yuz-binlerin-oynadigi-online-oyun-davalik-oldu-oyunu-kopyalayip-markayi-ihlal-edenler-icin-5-yil-hapis-istendi) — Mgame davası, Ocak 2025
- [MedyaTV: dava ve Türkiye'deki etkisi](https://www.medyatv.com/foto-galeri/teknoloji/knight-onlineda-skandal-kopya-iddiasiyla-acilan-dava-turkiyedeki-oyunculari-nasil-etkileyecek/1185)
- [Knight Online — Steam](https://store.steampowered.com/app/389430/Knight_Online/?l=turkish) — geliştirici/yayıncı bilgisi
- [NTTGame son kullanıcı sözleşmesi](http://www.nttgameonline.com/knight/tr/corporate/agreement) — marka tescili beyanı
- [Knight Online — Wikipedia](https://en.wikipedia.org/wiki/Knight_Online)

**Teknik referans**
- [Knight Online sunucu kurulum rehberi (MSSQL)](https://whitebilisim.com/en/posts/knight-online-server-setup-guide)
- [KO1 — Unity 3D istemci kullandığını belirten özel sunucu](https://knightonline1.com/en/)
