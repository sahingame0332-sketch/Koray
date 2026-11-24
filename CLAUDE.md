# OLYMPOS-KO · 1298 Mobil Arayüz — Claude Code proje bağlamı

Bu depo, claude.ai'daki "OLYMPOS arayüz" sohbetinin devamıdır. Arayüz çalışmasının tamamı `arayuz/` altındadır;
sohbetin adım adım kaydı: `arayuz/00-sohbet-ozeti.md`. Kullanıcıyla **Türkçe** konuş.

Deponun geri kalanı aynı oyunun altyapı tarafıdır (veri modeli, içerik üretimi, APK analizi) — bkz. `README.md` ve `docs/`.
Arayüz işi ile altyapı işi aynı oyunun iki yüzü: `docs/03-icerik-uretim-rehberi.md` içindeki UI ekran envanteri bu pencerelerle eşleşir.

## Proje
- Oyun: **OLYMPOS-KO**, Knight Online **1298** istemcisi tarzında bir **mobil** oyun, **Unity** ile geliştiriliyor.
- Görev: kullanıcının gönderdiği oyun arayüzü ekran görüntülerini **birebir** Unity'ye aktarılabilir pencerelere çevirmek.
- Kullanıcının referans arşivi (`ara_yüz_görselleri.rar`, kendi bilgisayarında): `01_Onizlemeler`, `02_Unity_Gorselleri`,
  `03_Hazir_Paketler` (`1298_Mobil_Arayuz_Unity_Hazir`, NPC pencereleri, Moradon referansı), `04_1298_Font_Referanslari`
  (UIF font kayıtları CSV: 3.698 kayıt; çoğunluk Arial, sonra Gulim). Proje tercihi başlık/etiket fontu: **Roboto Slab Bold**.

## Kullanıcının çalışma tarzı ve kuralları (önemli)
1. **Birebir.** Yazılar, fontlar, renkler, çerçeveler, buton zeminleri **orijinal görselden alınır**; yeniden çizilmez/tasarlanmaz.
   Yöntem: ilgili parçayı orijinalden kes → üstündeki yazıyı sil (aynı satırdaki gerçek dokudan örnekleyerek doldur) → yazısız sprite.
   Küçük, oyun içi boyuttaki görsellerde yazılar da orijinal piksellerden korunur.
2. **Önce görsel.** Dosya/doküman/paket yapmadan önce sonucu **görsel olarak** göster (orijinal ↔ yeni yan yana).
   Kullanıcı onaylayınca ("Süpersin… Unity editöre aktarabileceğim şekilde dosya haline getir") Unity paketine geç.
3. **Saydamlık.** Pencere iç zemini **düz siyah** (kahverengi doku YOK) ve **yarı saydam**;
   oyun dünyası arkadan hafifçe görünür. Unity'de ayrı bir siyah Image + Inspector'da `backgroundAlpha` ile ayarlanır.
   Pencere dışında kalan oyun sahnesi parçaları **tamamen saydam**. Kutular/butonlar **opak**.
   Alfa değerleri **orijinal ekran görüntülerinden ölçüldü** (bkz. `arayuz/04-saydamlik.md`), varsayılmadı:
   Character **0.92** · Ana menü **0.92** · Stat butonları **0.92** · OPTIONS dış alan **0.95**.
   İSTİSNA: **Save Stat Preset** **mat** (ölçüm: alfa 0.99) ve **OPTIONS içerik paneli** opak (kendi siyah zemini var).
   Yeni pencerede alfa tahmin edilmez: `araclar/saydamlik_olcumu/saydamlik.py` ile ölçülür.
4. Kullanıcı "Dur" derse hemen dur, durumu kısaca söyle, bekle.

## Teslim edilenler
| Paket | Pencere | Boyut (px) | Zemin |
|---|---|---|---|
| `arayuz/unity_paketleri/OlymposCharacter1298.unitypackage` | Character › CHAR INFO sekmesi | 654 × 1030 | yarı saydam siyah **0.92** |
| `arayuz/unity_paketleri/OlymposStatWindows1298.unitypackage` | SAVE STAT PRESET | 293 × 454 | mat |
| (aynı paket) | Stat butonları STR/HP/DEX/INT/MP | 197 × 243 | yarı saydam siyah **0.92** |
| `arayuz/unity_paketleri/OlymposCharacter1298.unitypackage` | Character › CLAN ve FRIENDS sekmeleri | 654 × 1030 | yarı saydam **0.92** |
| `arayuz/unity_paketleri/OlymposMenuOptions1298.unitypackage` | Ana menü paneli | 321 × 989 | yarı saydam **0.92** |
| (aynı paket) | OPTIONS (11 sayfa) | 854 × 1171 | dış **0.95**, içerik paneli opak |
| `arayuz/unity_paketleri/OlymposNpcShop1298.unitypackage` | NPC dükkânı + diyalog + ipucu | 750 × 1156 | yarı saydam (bkz. `arayuz/05-npc-dukkan.md`) |
| `arayuz/unity_paketleri/OlymposOyunIci1298.unitypackage` | Oyun içi: eşya penceresi, buff çubuğu + Remove, hızlı slotlar, Save Skill Slot, hedef + Show Drops + Drop List, hedef iptal X | 2712 × 1220 ekran (kendi Canvas'ı) | 0.92 / 0.89 / 0.93 / 0.95, slot içi 0.88 (bkz. `arayuz/06-oyun-ici.md`) |
| `arayuz/unity_paketleri/OlymposZemin1298.unitypackage` | Zemin: 5 döşenebilir doku, kontrol + renk haritası örnekleri, `Olympos/Zemin1298` shader, ortam rengi | 256² / 128² | — (bkz. `arayuz/08-zemin.md`) |
| `arayuz/unity_paketleri/OlymposMerchant1298.unitypackage` | Komut menüsü, Create a Merchant + fiyat diyaloğu, tezgâh çubuğu, "<ad> Merchant", Slave Merchant, adet girişi (toplu eşya), süre çubuklu satın alma onayı, eşya bilgi penceresi (Equip / UnEquip / Remove / Buy Price / Purchase Price) | 2712 × 1220 ekran (OyunIci ile ortak Canvas) | 0.94 / 0.95 / 0.97 / 0.89 / 0.95 / 0.93, tezgâh yuvası 0.87 (bkz. `arayuz/09-merchant.md`) |
| `arayuz/unity_paketleri/OlymposAdetPenceresi1298.unitypackage` | Adet girişi penceresi — tek başına (Merchant paketindekinin bağımsız kopyası; sınıf `OlymposAdetPenceresi`) | 711 × 522 | yarı saydam **0.94** |
| `arayuz/unity_paketleri/OlymposSatinAlmaOnayi1298.unitypackage` | Süre çubuklu satın alma onayı — tek başına (sınıf `OlymposSatinAlmaPenceresi`) | 554 × 509 | mat (0.99) |
| `arayuz/unity_paketleri/OlymposMerchantAlici1298.unitypackage` | Merchant alıcı görünümü — tek başına: satıcı adlı tezgâh çubuğu (mor çerçeveli yuvalar) + "<ad> Merchant" penceresi (sınıflar `OlymposSatici*`) | 404 × 168 / 785 × 987 | yuva 0.87 / **0.89** |
| `arayuz/unity_paketleri/OlymposEfekt1298.unitypackage` | Skill/hasar efektleri — tek başına: Pillar of Fire ateş sütunu, karaktere vuruş ışıması (kare dizisi, eklemeli shader), cast çubuğu, hasar mesajı renkleri | 500 × 710 / 450 × 420 | eklemeli (Blend One One) (bkz. `arayuz/10-efekt.md`) |
| `arayuz/unity_paketleri/OlymposSkillEfekt1298.unitypackage` | Skill efektleri — tek başına: Fire Burst (moba), Fire Blade (moba), karaktere vuruş (tam); sınıf `OlymposSkillEfektOynatici`, shader `Olympos/Skill Efekt Eklemeli` | 900 × 760 / 560 × 820 / 470 × 430 | eklemeli, 36 kare/sn (bkz. `arayuz/10-efekt.md` ek 2) |
| `arayuz/unity_paketleri/OlymposGenie1298.unitypackage` | Knight Genie — tek başına: panel (Başlat/Durdur/Ayarlar, Time Left, sunucu, CR, kanal), AUTO ATTACK SETTINGS (24 slot + iksir, 4 kaydırıcı, 4 onay), aktif durum (GENIE rozeti, skill kilidi); sınıflar `OlymposGenie*` | 356 × 246 / 636 × 1162 / 300² | panel opak, pencere **0.93** (bkz. `arayuz/11-genie.md`) |
| `arayuz/unity_paketleri/OlymposGorevNpc1298.unitypackage` | Görev NPC'si — tek başına: "?" rozeti (ön-çarpımlı, shader `Olympos/UI On Carpimli`), QuestList, görev detayı (Objectives, 8 ödül, Accepted/Close); sınıflar `OlymposGorev*`, font Liberation Sans Bold | 350² / 642 × 470 / 596 × 840 | liste **0.91**, detay **0.93** (bkz. `arayuz/12-gorev-npc.md`) |
| `arayuz/unity_paketleri/OlymposRespawn1298.unitypackage` | Respawn penceresi (karakter ölünce) — tek başına; yazılar sprite'ta (orijinal piksel), Confirm → `onOnay`; referans `.jpg` pakette (`Referans/`) | 700 × 386 | yarı saydam **0.92** (bkz. `arayuz/13-respawn.md`) |
| `arayuz/unity_paketleri/OlymposRuneEfekt1298.unitypackage` | Alevli run halkası — tek başına: karakterin altında dönen rün dairesi + kenardan yükselen alev duvarı (shader'lar `Olympos/Rune Ates Halkasi`, `Olympos/Rune Alev Duvari`; namespace `Olympos.RuneEfekt`). **Özgün tasarım** — kullanıcının gönderdiği stok görsel (dreamstime, lisanssız) kopyalanmadı | 1024² doku, çap 1.6 × karakter boyu, alev 0.12 × çap | eklemeli (bkz. `arayuz/14-rune-efekt.md`) |
| `arayuz/unity_paketleri/OlymposRuneNeon1298.unitypackage` | Neon run halkası — tek başına: aynı efekt, mor/mavi/yeşil neon, Futhark rünleri (namespace `Olympos.RuneNeon`, shader'lar `Olympos/Rune Neon Halkasi` / `Duvari`). **Özgün tasarım** (stok görsel kopyalanmadı) | çap 1.6 × karakter boyu, alev 0.12 × çap, yoğunluk 0.5 | eklemeli (bkz. `arayuz/14-rune-efekt.md` ek) |
| `arayuz/unity_paketleri/OlymposAtesHavuzu1298.unitypackage` | Karakter altı ateş havuzu — tek başına: kayıttan 39 kare (30 kare/sn, 1.3 sn), eklemeli (sınıf `OlymposAtesHavuzuOynatici`, shader `Olympos/Ates Havuzu Eklemeli`) | 560 × 420, 3.73 × karakter boyu | eklemeli (bkz. `arayuz/10-efekt.md` ek 3) |
| `arayuz/unity_paketleri/OlymposAlimSatim1298.unitypackage` | NPC alım-satım penceresi — tek başına: Buy/Sell Item Count (sayı kutusu) → Need/Earn Money → Confirm/Cancel; harf aralıklı yazı efekti `OlymposAlimSatimHarfAraligi`; 4 referans `.jpg` pakette | 616 × 252 | yarı saydam **0.97** (bkz. `arayuz/15-npc-alimsatim.md`) |
| `arayuz/unity_paketleri/OlymposManesOfFire1298.unitypackage` | Manes Of Fire (moba uygulanan skill) — tek başına: gökten ışın + kırmızı prizma + ateş + yerde sarı rün halkaları, kayıttan 49 kare (30 kare/sn); sınıf `OlymposManesOfFireOynatici`, shader `Olympos/Manes Of Fire Eklemeli` | 520 × 940, 3.71 × boy | eklemeli (bkz. `arayuz/10-efekt.md` ek 4) |
| `arayuz/unity_paketleri/OlymposTezgah1298.unitypackage` | Yerdeki Merchant tezgâhı — tek başına: **3B mesh** `OlymposTezgah3B` (sandık + öne eğik tahta, fotoğraflardan düzeltilmiş dokular, shader `Olympos/Tezgah 3B`) + eski 2B sprite sürümü (`OlymposTezgah`); referans `.jpg` pakette | 0.78 × 0.42 × 0.59/0.99 m (karakter 1.8) | opak, dışı saydam (bkz. `arayuz/16-tezgah.md`) |
| `arayuz/unity_paketleri/OlymposKendiSkill1298.unitypackage` | Kendi skill efektleri — tek başına, 12 efekt: döküm yıldızları, Hide, Light Feet, Cat's/Lupine Eyes, Evade, Safety, Cure Disease/Curse, Magic Shield, Sprint, Swift, Strength Of Wolf, Minor Healing; kayıtlardan 30 kare/sn; `OlymposKendiSkillEfekti` + `OlymposKendiSkillKutuphanesi` (skill adına göre), shader `Olympos/Kendi Skill Eklemeli`; referans `.jpg`'ler pakette | 720 × 860, 2.717 × karakter boyu | eklemeli (bkz. `arayuz/10-efekt.md` ek 5) |
| `arayuz/unity_paketleri/OlymposOk1298.unitypackage` | Shadow Hunter oku — tek başına: ok görseli (opak üç + ışık izi), düz çizgide sabit süreli uçuş (0.483 sn, hedefi izler, eksenel billboard), vuruş (beyaz patlama + turuncu ışın, ön-çarpımlı 23 kare); `OlymposOkAtisi.At(okcu, hedef)` | ok 160 × 19 (0.533 × karakter boyu), vuruş 520 × 260 | alfa / ön-çarpımlı (bkz. `arayuz/17-ok.md`) |

| `arayuz/unity_paketleri/OlymposYakinSkill1298.unitypackage` | Yakın dövüş skill efektleri — tek başına: Stroke, Stab, Stab2; her skill **karakter** (kesik yayları, kıvılcımlar) + **hedef** (gökten ışın, vuruş patlaması) katmanı; `OlymposYakinSkillEfekti.Oyna(karakter, hedef)`, kütüphane skill adına göre, shader `Olympos/Yakin Skill Eklemeli`; referans `.jpg`'ler pakette | karakter 243 px ölçeğinde (bkz. `yakin_skill_olculer.json`) | eklemeli (bkz. `arayuz/10-efekt.md` ek 6) |
| `arayuz/unity_paketleri/OlymposSecim1298.unitypackage` | Seçim efektleri — tek başına: mobun altında **seçim halkası** (sarı halka + beyaz-mor iç çizgi + 3 üçgen işaret) ve karakterin ayağında hedefe dönen **yeşil yön oku**; yer decalı, ön-çarpımlı (shader `Olympos/Secim Zemin`), `OlymposSecimYoneticisi.Sec(karakter, hedef)` | halka 512², yarıçap 0.399 × boy; ok 156 × 232, 0.328 × 0.488 boy | kenar 0.85 / dolgu 0.47, halka çekirdek 0.95 (bkz. `arayuz/18-secim.md`) |
| `arayuz/unity_paketleri/OlymposSandik1298.unitypackage` | Mob ölünce düşen sandık — tek başına: **3B** `OlymposSandik` (gövde + kubbe kapak, kapalı/açık, `Dus/Ac/Kapat`; açık: altınlar + kapak içi, kapak 115.5°) + 2B sprite'lar (`OlymposSandik2B`); dokular 5 ekran görüntüsünden uydurulan kameralarla geri izdüşüm; referans `.jpg`'ler pakette | L × 0.848 × (0.389 + 0.414 kubbe), L = 0.24 × karakter boyu (tahmin) | opak ışıksız (bkz. `arayuz/19-sandik.md`) |
| `arayuz/unity_paketleri/OlymposEfekt7_1298.unitypackage` | Efekt 7 — tek başına: kesik + pembe aura (20 kare) ve yıldız vuruşu (10 kare), her biri arka (mobun arkası) + ön katman, 30 kare/sn; mobun hasar kırmızısı (ek malzeme, ölçülen eğri); `OlymposEfekt7Kutuphanesi.Uygula(ad, mob)` | mob boyuna göre (kayıtta 582 px) | eklemeli + hasar rengi (bkz. `arayuz/10-efekt.md` ek 7) |
| `arayuz/unity_paketleri/OlymposMobHasar1298.unitypackage` | Mob hasar rengi — tek başına (Efekt 7'den ayrıldı): vurulan mob kısa süre kırmızı; ek malzeme (shader `Olympos/Mob Hasar Kirmizi`, kanal başına c·renk + b), güç eğrileri "kesik"/"yildiz"; `OlymposMobHasarRengi.Oyna(mob, egri)` | — | mobun rengi (bkz. `arayuz/10-efekt.md` ek 7) |
| `arayuz/unity_paketleri/OlymposEfekt7Skill1298.unitypackage` | Efekt 7 skill ışıkları — tek başına (hasar rengi yok): kesik + aura, yıldız; arka + ön katman (namespace `Olympos.Efekt7Skill`, shader `Olympos/Efekt7 Skill Eklemeli`) | mob boyuna göre | eklemeli (bkz. ek 7) |
| `arayuz/unity_paketleri/OlymposEfekt7Karakter1298.unitypackage` | Efekt 7 karakter efekti — tek başına: kılıcın sarı kesik yayı (12 kare), karaktere bağlı, hedef tarafına otomatik ayna (`Olympos.Efekt7Karakter`) | 1.166 × karakter boyu (oyuncu boyu tahmin) | eklemeli (bkz. ek 7) |
| `arayuz/unity_paketleri/OlymposEfekt7Hasar1298.unitypackage` | Efekt 7 hasar efekti — tek başına: mobdaki vuruş (aura, kıvılcımlar, yıldız; kesik yayı çıkarıldı), arka + ön katman (`Olympos.Efekt7Hasar`); mob kırmızısıyla birlikte kullanılır | mob boyuna göre | eklemeli (bkz. ek 7) |
| `arayuz/unity_paketleri/OlymposEfekt8_1298.unitypackage` | Efekt 8 — tek başına, YALNIZ skill efekti (tablet kaydı 19-16-21, gerçek hız): kesikler + altın yapraklar → pembe aura → yatay parlama → yıldız; 26 kare, arka + ön katman (`Olympos.Efekt8`, shader `Olympos/Efekt8 Eklemeli`); mob kırmızısı yok (ayrı paket) | 3.18 × mob boyu (kayıtta 422 px) | eklemeli (bkz. `arayuz/10-efekt.md` ek 8) |
| `arayuz/unity_paketleri/OlymposEfekt9Vurus1298.unitypackage` | Efekt 9 vuruş — tek başına (kayıt 20-27-52): mobda pembe patlama, gökten ışın, yerde pembe halka + yatay parlama, yıldız, altın yapraklar; 26 kare (`Olympos.Efekt9Vurus`) | 4.50 × karakter boyu (270 px) | eklemeli (bkz. `arayuz/10-efekt.md` ek 9) |
| `arayuz/unity_paketleri/OlymposEfekt9Kesik1298.unitypackage` | Efekt 9 karakter kılıç kesiği — tek başına; 11 kare, karaktere bağlı, hedef tarafına otomatik ayna (`Olympos.Efekt9Kesik`) | 2.65 × karakter boyu | eklemeli (bkz. ek 9) |
| `arayuz/unity_paketleri/OlymposEfekt9Altin1298.unitypackage` | Efekt 9 altın patlama (karakterde) — tek başına; 10 kare (`Olympos.Efekt9Altin`) | 2.23 × karakter boyu | eklemeli (bkz. ek 9) |
| `arayuz/unity_paketleri/OlymposItemRemove1298.unitypackage` | Item Remove (eşya silme onayı) — tek başına: "Item Remove" / soru / eşya adı / "Count:N" + OK/Cancel; `pencere.Ac(ad, adet)`, `onOnay(ad, adet)`, harf aralıklı Text `OlymposItemRemoveHarfAraligi`; referans `.jpg` pakette | 696 × 382 | yarı saydam **0.92** (bkz. `arayuz/22-item-remove.md`) |
| `arayuz/unity_paketleri/OlymposSelectUpgrade1298.unitypackage` | Select Upgrade menüsü — tek başına: Item / Fast / Accessory Upgrade + Close (olaylar) | 420 × 497 (tablet 2266×1488, Canvas'ta ×0.82) | yarı saydam **0.93** (bkz. `arayuz/23-upgrade.md`) |
| `arayuz/unity_paketleri/OlymposItemUpgrade1298.unitypackage` | ITEM UPGRADE — tek başına: 3×3 + 2 büyük yuva, Need Coins / Upgrade Rate, Upgrade/Cancel/Preview, para, 7×4 envanter (`SetEnvanter`, `SetUpgradeYuvasi`) | 857 × 1235 | gövde **0.895**, panel 0.967, yuva 0.993 |
| `arayuz/unity_paketleri/OlymposAccessoryUpgrade1298.unitypackage` | ACCESSORY UPGRADE — tek başına: 3 büyük + 3 küçük yuva, 3 alt panel | 852 × 1235 | gövde **0.895**, paneller opak / 0.959 / 0.995 |
| `arayuz/unity_paketleri/OlymposFastUpgrade1298.unitypackage` | FAST UPGRADE +1…+5 — tek başına: 5×3 yuva, Need Coins çubuğu, Upgrade/Cancel | 862 × 1245 | gövde **0.895**, yuva 0.94 |
Kaynaklar `arayuz/unity_kaynak/Assets/...` (meta dosyalarıyla). Unity menüsü:
`OLYMPOS > 1298 > Character Penceresi Oluştur` (CHAR INFO + CLAN + FRIENDS sekmeleriyle birlikte),
`… > Save Stat Preset Penceresi Oluştur`, `… > Stat Butonları Penceresi Oluştur`,
`… > Ana Menü Paneli Oluştur`, `… > OPTIONS Penceresi Oluştur`.
`… > NPC Dükkân Penceresi Oluştur`, `… > Oyun İçi (Scroll · Skill Slot · Drops · Hedef) Oluştur`
(sonuncusu 2712×1220 referanslı ayrı bir Canvas kurar; diğerleri 1920×1080).
`… > Zemin Malzemeleri Oluştur` (arayüz değil: malzemeler + deneme zemini; namespace `Olympos.Zemin`).
`… > Merchant (Tezgâh · Slave · Equip · Eşya Bilgisi) Oluştur` (OyunIci'nin 2712×1220 Canvas'ını paylaşır).
`… > Adet Penceresi Oluştur`, `… > Satın Alma Onayı Penceresi Oluştur`, `… > Merchant Alıcı Görünümü Oluştur` (tek başına paketler; aynı Canvas).
`… > Efektler (Ateş Sütunu · Vuruş · Cast) Oluştur` (namespace `Olympos.Efekt`; efektler dünya uzayında).
`… > Skill Efektleri (Fire Burst · Fire Blade · Vuruş) Oluştur` (namespace `Olympos.SkillEfekt`).
`… > Genie (Panel · Auto Attack Settings · Rozet) Oluştur` (aynı 2712×1220 Canvas).
`… > Görev NPC (QuestList · Görev Detayı · ? Rozeti) Oluştur` (aynı Canvas). `… > Respawn Penceresi Oluştur` (aynı Canvas). `… > Alevli Run Halkası Oluştur`, `… > Neon Run Halkası Oluştur`, `… > Ateş Havuzu (Karakter Altı) Oluştur` (dünya uzayı). `… > NPC Alım-Satım Penceresi Oluştur` (2712×1220 Canvas). `… > Item Remove Penceresi Oluştur` (aynı Canvas). `… > Select Upgrade Menüsü / Item Upgrade / Accessory Upgrade / Fast Upgrade Penceresi Oluştur` (aynı Canvas, ×0.82, sağa yaslı). `… > Manes Of Fire (Moba) Oluştur`, `… > Merchant Tezgahı (Yer) Oluştur`, `… > Merchant Tezgahı 3B Oluştur`, `… > Kendi Skill Efektleri (…) Oluştur`, `… > Ok (Shadow Hunter) Oluştur`, `… > Yakın Skill Efektleri (Stroke · Stab · Stab2) Oluştur`, `… > Seçim Halkası + Yön Oku Oluştur`, `… > Sandık (Açık · Kapalı) Oluştur`, `… > Efekt 7 (Kesik + Aura · Yıldız Vuruşu) Oluştur`, ayrık: `… > Mob Hasar Rengi (Kırmızı) Oluştur`, `… > Efekt 7 Skill Işıkları (Kesik + Aura · Yıldız) Oluştur`, `… > Efekt 7 Karakter (Kılıç Kesiği) Oluştur`, `… > Efekt 7 Hasar (Mobda Vuruş: Aura · Yıldız) Oluştur`, `… > Efekt 8 (Skill Efekti) Oluştur`, `… > Efekt 9 Vuruş (…) Oluştur`, `… > Efekt 9 Karakter (Kılıç Kesiği) Oluştur`, `… > Efekt 9 Altın Patlama (Karakterde) Oluştur` (dünya uzayı).
Kurucular: doku import ayarları (Sprite, sıkıştırmasız, mipmap yok, 9-slice kenarlar) → hiyerarşiyi **sol-üst piksel
koordinatlarıyla** kurar → `Prefabs/` altına prefab → sahnedeki Canvas'a ekler (yoksa 1920×1080, match=1 Canvas + EventSystem).
UI sistemi: **uGUI + legacy `UnityEngine.UI.Text`** (TMP kullanılmadı). Namespace `Olympos.UI` / `Olympos.UI.EditorTools`.

**Doğrulama durumu:** Yerleşim Python/Chrome ile simüle edilip orijinalle karşılaştırıldı.
Claude Code'a devirden sonra Mono (`mcs`) kurulup betikler **derlendi: 0 hata, 0 uyarı**; paketlerin arşiv yapısı,
GUID'leri ve dosya içerikleri `unity_kaynak/` ile birebir eşleşiyor. Font kalibrasyonundan sonra ölçülen
31 yazı bölgesinde orijinale örtüşme 0.478 → **0.627** (31/31 iyileşti). **Unity'de import hâlâ denenmedi** (ortamda Unity yok).
Ayrıntı: `arayuz/01-dogrulama.md` (derleme/paket) ve `arayuz/02-font-kalibrasyonu.md` (font/punto).
Kontroller: `arayuz/araclar/derleme_kontrolu/derle.sh`, `arayuz/araclar/font_kalibrasyonu/olc.py`.

## Char Info (654×1030) ölçüleri
Renkler: etiket beyaz `#F4F4F4`, isim `#F2E79C`, turuncu etiket (Exp/NP/Attack/Defence) `#E2B47C`, değer tan `#DCB98A`,
stat puanı yeşil `#A6DC3C`, Stat Reset turuncu `#D98A34`, kutu kenarı tan `#DFC5AE`.
Sprite'lar (`arayuz/unity_kaynak/Assets/OlymposCharacter1298/Resources/OlymposCharacter1298/`): `window_frame` (bronz çerçeve 9px, içi saydam), `tabs_strip` (637×92 @ 9,8;
orijinal doku, CHAR INFO altın alt çizgisi dahil), `label_button` (9-slice L18 B8 R8 T8), `value_box` (9-slice 6),
`btn_preset`/`btn_reset` (145×45), `race_human` (57×57 @ 64,116, dairesel alfa).
Sekmeler: CHAR INFO (15,10,200,82) · QUESTS (224,10,128,82) · CLAN (365,10,156,82) · FRIENDS (525,10,120,82).
Diğer tüm koordinatlar `OlymposCharacterWindowBuilder.cs` içinde.
Font: **Roboto Slab Bold v2.002** artık pakette (`Fonts/RobotoSlab-Bold.ttf`, her iki pakette de).
Puntolar bu fonta göre ölçülerek kalibre edildi — sekme 21, etiket 21, HUMAN 20, isim 25, Magician 22,
stat adı 21, stat değeri 25, direnç adı 19, direnç değeri 23, buton 22. Değiştirmeden önce
`arayuz/02-font-kalibrasyonu.md` oku; puntolar fonta bağlı, font değişirse yeniden ölçülmeli.

## Stat pencereleri ölçüleri
- Save Stat Preset: orijinal 299×479'dan (3,8)-(296,462) kesildi. Slot aralığı **103 px**; slot 2–4 temiz **slot 1**'den üretildi
  (orijinalde 2. ve 3. slotta arkadaki stat penceresinin hayalet izleri vardı), numara rozetleri her slotun kendisinden.
  Tıklama alanları (sprite koordinatı): Kapat (246,3,28,28); slot k için Save (49,107+103k,95,25), Activate (148,107+103k,95,25);
  "- Empty -" örtüsü/metni (74,80+103k,146,16) → `SetSlotStatus(slot, text)`.
- Stat butonları: orijinal 202×251'den (2,0)-(198,242). Çerçeve 3 px. Butonlar x=21, w=163, h=38, y = 22/65/108/151/194.
  `stat_buttons_frame.png` = çerçeve + butonlar, içi saydam; siyah zemin ayrı Image.
- Butonlar: görünmez Image + ColorTint (normal α0, hover α0.12, basılı α0.35, disabled α0.45 siyah).

## Araçlar (`arayuz/araclar/`)
- `rar5list.py` / `rar5stored.py`: RAR5 başlık okuyucu; arşivdeki sıkıştırılmamış (stored) ZIP'i çıkarır (ortamda unrar yoktu).
- `mkunitypkg.py <klasör> <çıktı.unitypackage> <çıktı.zip>`: `Assets/` altındakilere yoldan türetilen sabit GUID'li minimal
  `.meta` yazar, `.unitypackage` (tar.gz: guid/asset, asset.meta, pathname) ve zip üretir.
- `build_windows2.py`: Save Stat Preset + stat butonları sprite'larını orijinallerden üretir (`preset_orig.png`, `stats_orig.png` bekler).
- `derleme_kontrolu/derle.sh`: Unity olmadan tüm `.cs` dosyalarını Mono ile derler (Unity API taslakları yanında).
- `font_kalibrasyonu/`: `font_kimligi.py` (orijinaldeki yazı hangi fonta ait — adayları ölçüp sıralar),
  `olc.py` (önizleme ↔ orijinal bölge bölge örtüşme), `bolgeler.json` (Char Info'daki 31 yazı bölgesi).
  Yeni pencere birebir yapılırken punto bunlarla seçilir, gözle değil.
- `oyun_ici/`: `medyan.py` (video karelerinin medyanı), `cikar.py` (pencereli/penceresiz kare farkıyla krom ayırma),
  `punto.py` (font + punto), `kur.py` (kurucunun benzetimi → `onizlemeler/oyun_ici_*.png`). `hud/`: yarım HUD işinin araçları.
- `merchant/`: `cikar.py` (krom + maske + yuva şablonu), `maske.py`, `punto.py`, `kur.py` (benzetim → `onizlemeler/merchant_*.png`).
  `cikar2.py` / `kur2.py`: tablet görüntülerinden adet ve satın alma onayı pencereleri (ölçek 1.0405).
  `cikar3.py` / `kur3.py`: alıcı görünümü (mor çerçeveler, satıcı adı).
- `efekt/`: `cikar.py VIDEO` (eklemeli efekt kareleri: orijinal − zemin), `kur.py VIDEO` (zemin + efekt ↔ orijinal).
  `cikar6.py VIDEO` / `kur6.py VIDEO` / `paket6.py VIDEO`: Stroke/Stab/Stab2 (karakter + hedef katmanı, iki zeminli min, seçim halkası maskesi, ışın için ayrışık I(y)·P(u) modeli).
  `cikar5.py KLASOR` / `kur5.py KLASOR`: 9 kayıttan kendi skill efektleri (renk imzası kapısı + gövde elipsi + etiket bandı dikey dolgu; geçici kareleri siler).
  `cikar4.py VIDEO` / `kur4.py VIDEO`: Manes Of Fire (moba; tablet 60 kare/sn).
  `cikar3.py VIDEO` / `kur3.py VIDEO`: karakter altı ateş havuzu (doyan merkezde ışığın kendi rengi).
  `cikar2.py A B` / `kur2.py A B`: telefon kayıtlarından Fire Burst, Fire Blade, tam vuruş (etiket bandı dikey dolgu, kararan piksel dolgusu).
  Kullanıcı kayıtlarında yüz kamerası olabilir: tam kareleri depoya koyma.
- `efekt7/`: galeride yavaş sarılan kayıt için süre kutusu OCR (`ocr.py`, `zaman.py`), `cikar7.py` (arka/ön katman + hasar kırmızısı), `kur7.py`, `genis.py`; uzak kayıt eki `uzak*.py`, `temiz.py`.
- `efekt8/`: `cikar8.py KLASOR` (tablet kaydı, yalnız skill ışığı: mob içinde kırmızı boyanmış zemin çıkarılır, sıkı mob maskesi), `kur8.py` (önizleme), `katman8.py` (arka/ön).
- `efekt9/`: `cikar9.py KLASOR` (iki efekt; gri/renksiz artış = hareket eden gövde, ad etiketleri dolgu), `kur9.py`, `ayir9.py` (vuruş / kesik / altın), `paket_onizle9.py`, `denetle9.py` (kare kare hata), `fullhd9.py` (1920×1080 önizleme).
- `genie/`: `cikar_pencere.py` (doğrusal olmayan zemin modeliyle krom), `cikar_panel.py` (3 sahnede değişmeyen piksel = opak),
  `cikar_aktif.py` (skill kilidi: 8 ikondan en küçük kareler; GENIE rozeti), `punto.py`, `kur.py` → `onizlemeler/genie_onizleme.png`.
- `gorev/`: `cikar_rozet.py` ("?" rozeti: basamak şeridi kontrastından geçirgenlik → ön-çarpımlı), `cikar_krom.py`,
  `cikar_pencere.py` (taban + tekrar eden parçalar), `punto.py` (Liberation Sans adayları), `kur.py` → `onizlemeler/gorev_onizleme.png`.
- `respawn/`: `cikar.py` (pencereSIZ kare yok: alfa iç/dış çim oranından; krom yerel karanlık tabana göre), `punto.py`, `kur.py`.
- `rune/`: `ciz.py` / `ciz2.py` (özgün rün daireleri: alevli / neon + gürültü), `kur.py` / `kur2.py` (shader benzetimi), `kur_video.py` (kayıttaki karaktere bindirme).
- `upgrade/`: `ortak.py` (kirli maske, tasarım gruplu katman çözümü, kutu bulma, hizalı boş yuva), `pencere2.py ad`, `secim.py`, `olc.py`, `punto.py`, `onizle.py`, `paket.py` (4 paketin Unity kaynakları).
- `item_remove/`: `punto.py` (font + punto + harf aralığı, satır satır ve ortak), `cikar.py` (çerçeve + OK/Cancel sprite), `kur.py` (benzetim + fark).
- `npc_alimsatim/`: `cikar.py` (krom + alfa: dışarı taşan dükkân öğelerinden), `punto.py`, `aralik.py` (punto + harf aralığı birlikte IoU), `kur.py`.
- `tezgah/`: `cikar.py` (çim dışı maske → dış bükey zarf → yumuşak kenar), `kur.py`; `cikar3b.py` (yüzleri homografiyle dokuya açar), `kur3b.py` (3B mesh'in yazılım çizimi).
- `ok/`: `izle.py` (ok ucu kare kare), `cikar.py` (ok görseli + uçuş ölçüsü), `cikar_vurus.py` (iki zeminli ayıklama, ön-çarpımlı), `kur.py`.
- `secim/`: kamera-zemin modeli (`rectfit2.py`, `zemin.py`, `kamera_zemin.npy`: yh −353, s 1621), halka (`acik.py`, `model2.py`, `halka_doku.py`: radyal a/P regresyonu + işaret),
  ok (`ok4`–`ok12.py`: 5 örnek hizalama + ayna + ölçülen kenar doğruları), `yansit.py` (geri yansıtma → `onizlemeler/secim_onizleme.png`). Ara dosyalar scratch'te üretilir.
- `sandik/`: ortografik kamera + şekil ortak uydurma (siluet + köşe), açık kapak açısı, yüzlerin geri izdüşümle dokusu, yazılım çizici (`ciz.py`, `onizle.py`).
- `zemin/`: `duzelt.py` (zemin düzlemini yukarıdan görünüşe çevirir), `zemin.py` (karo + renk ölçümü),
  `haritalar.py` (kontrol/renk haritası örnekleri), `onizle.py` (aynı kamerayla yeniden çizim → `onizlemeler/zemin_onizleme.png`).
- Char Info sprite çıkarımı (OpenCV inpaint + aynı satırdan doku örnekleme) sohbet içinde satır içi yapıldı; sonuçlar
  `arayuz/kaynak/char_info/sprites/`. HTML önizleme: `arayuz/kaynak/char_info/unity_preview.html` (sprite'larla, Moradon arka planı üzerinde).

## Sıradaki olası işler
- **Yarım iş:** oyun içi HUD (durum plakası, sohbet, alt bar, beceri çarkı…). Tablet ölçümleri `arayuz/07-hud-taslak.md` içinde;
  karar: HUD **telefon karelerinden (2712×1220)** kurulacak ki OyunIci/Merchant ile aynı Canvas'a otursun. Başlangıç:
  `araclar/hud_telefon/ortak.py` (çim taşması maskesi `cim_disi` — tamamı çim olan `m_once` karesinde bütün HUD öğelerini ayırıyor).
  Önizleme/paket yok.
- Lisanssız stok görsel (filigranlı) gelirse kopyalanmaz; aynı türde özgün tasarım yapılır ve kullanıcıya söylenir.
- Harf aralıklı yazılar (Roboto Slab Bold, +2 px) değişken metinse `OlymposAlimSatimHarfAraligi` deseni kullanılabilir.
- Kullanıcı referans görseli pakete `.jpg` olarak koymayı istedi (Respawn): yeni paketlerde `Referans/` klasörü.
- Kullanıcı son isteklerde her görseli **ayrı paket** olarak istedi ("ayrı paket olarak hazırla"): yeni pencereler tek başına,
  çakışmayan sınıf adlarıyla paketlenmeli. Merchant paketindeki "+N" puntosu üst yuvalarda 38; ölçülen 25 (bkz. 09 eki) — düzeltilebilir.
- Merchant paketi teslim edildi (`arayuz/09-merchant.md`, adet + satın alma onayı eki dâhil). Hâlâ varsayım: onayın nasıl
  açıldığı, bekleme süresi, satılmış eşyanın Slave Merchant'taki durumu — kayıt gelirse gerçek davranışla değiştirilmeli.
- Zemin paketi teslim edildi (`arayuz/08-zemin.md`); kullanıcı Unity'de deneyince shader derleme çıktısı ve
  karo ölçeği/en-boy rötuşu gerekebilir (görüş açısı 60° varsayıldı).
- Kullanıcının Unity'de ilk import sonucunu almak, Console çıktısındaki hataları düzeltmek.
  (Beklenen tek uyarı: Unity 2023.1+ için eskimiş `FindObjectOfType` — hata değil.)
  Aynı denemede puntoların Unity'de de tutup tutmadığına bakılmalı (±1 rötuş gerekebilir).
- Üç pencerenin ölçeklerini birbirine oranlamak (Char Info daha büyük bir ekran görüntüsünden geldi).
- OPTIONS sayfalarındaki onay kutuları ve kaydırıcıları etkileşimli hâle getirmek
  (şu an sayfa görselinin parçası; her iki durum da kaynak ekranlarda mevcut).
- QUESTS sekmesi — ekran görüntüsü gelince, aynı yöntemle.
- Kullanıcının göndereceği yeni pencereler.
