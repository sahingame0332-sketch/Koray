# 10 · Skill ve hasar efektleri (Pillar of Fire, karaktere vuruş, cast çubuğu, hasar mesajları)

Kaynak: kullanıcının 4 sn'lik kaydı (2266 × 1488, 60 kare/sn, HEVC). Kayıt sol üstte yüz kamerası içerdiği için
**depoya konmadı**; yalnız çıkarılan efekt kareleri (`kaynak/efekt/`) ve ölçümler var.
Paket: `unity_paketleri/OlymposEfekt1298.unitypackage` (tek başına) · önizleme: `onizlemeler/efekt_onizleme.png`.
Araçlar: `araclar/efekt/cikar.py VIDEO` (kareler), `kur.py VIDEO` (doğrulama görseli).

## Yöntem
- Kamera sabit: efektsiz karelerde zemin farkı < 0.3 / 255 (196. kareden sonra kayıt ekranı kararıyor).
- Efekt **eklemeli ışık**: efekt bölgesinde 148 971 piksel parlıyor, 4 606 kararıyor (kararanlar efektin önündeki karakter/mob).
  Bu yüzden kare = `clip(O − B, 0, 255)`, B = efekt öncesi karelerin medyanı. Unity'de `Blend One One` ile aynı zemine eklenince
  orijinal geri gelir: ortalama mutlak fark **3.7** (ateş sütunu) ve **4.2** (vuruş) / 255.
- UI etiketleri (ad, can çubuğu) ve efektin önündeki karakter bölgesi en yakın piksel + yumuşatma ile dolduruldu;
  ısınmayan sönük artıklar (mob animasyonu) silindi.

## Ölçümler
| Efekt | Kayıtta | Kare | Boyut (px) | Pivot (hedef noktası) | Genişlik |
|---|---|---|---|---|---|
| Pillar of Fire (moba) | kare 110–160 (1.83–2.67 sn) | 26 @ 30 fps | 500 × 710 | mobun ayağı (0.40, 0.155) | 4.5 karakter boyu |
| Karaktere vuruş | kare 178–194 (2.97–3.23 sn) | 9 @ 30 fps | 450 × 420 | karakter gövdesi (0.573, 0.452) | 4.1 karakter boyu |

- Karakter ekranda ~110 px (kurucu `karakterBoyu = 1.8` ile çarpar).
- Ateş sütunu: ilk 0.1 sn dışa saçılan ince kıvılcım çizgileri → 0.2–0.4 sn en geniş turuncu-sarı alev (genişlik ~470 px) →
  incelen kırmızı çekirdekli dikey sütun → 0.85 sn'de sönük kalıntı.
- Vuruş: ilk 2 kare sarı yuvarlak ışıma (yarıçap ~120 px) + zeminde dikdörtgen ışık lekesi (oyunun dinamik ışığı),
  sonra kırmızı-turuncu halka ve dışa sivri ışınlar (yarıçap ~90 px). Sonu kayıtta yok.
- **Cast çubuğu** (tablet koordinatı): siyah (1032,1002) 205 × 12; yeşil dolum 8 px, dikey ton
  `#437731 → #5CB938 → #3D8222`; skill adı Roboto Bold 15 `#FDE1E2` mürekkep üstü 986; kalan süre "0,2 sec"
  Roboto Bold 17 `#E3DF73`; ekran ortasının 266 px altında. Kurucu telefon düzenine 1/1.0405 ile çevirir.
- **Hasar:** ekranda uçan sayı yok. Information paneli (Roboto Slab Bold 31, satır ~30 px):
  kırmızı `#F80001` "… is inflicted with N HP damage." ve "N SP Used"; beyaz "… received N damage";
  sarı `#FCE600` "Using - Pillar Of Fire". Hedefin can çubuğu azalır (bkz. 06 hedef çubuğu).

## Sınırlar
Düz kare dizisi (parçacık sistemi değil) · karakter önündeki şerit tahmini · vuruşun sönüşü kayıtta yok ·
Unity'de ve URP'de denenmedi, shader burada derlenemedi.

---

## Ek 2 — Fire Burst · Fire Blade · karaktere vuruş (tam) — ayrı paket
Paket: `unity_paketleri/OlymposSkillEfekt1298.unitypackage` (tek başına; sınıf `OlymposSkillEfektOynatici`,
namespace `Olympos.SkillEfekt`, shader `Olympos/Skill Efekt Eklemeli`, menü
`OLYMPOS > 1298 > Skill Efektleri (Fire Burst · Fire Blade · Vuruş) Oluştur`). İlk efekt paketiyle çakışmaz.

Kaynak: iki telefon kaydı (2712 × 1220, ~72 kare/sn; 2 karede bir → **36 kare/sn**). Kayıtlar yüz kamerası
içerebileceği için depoya konmadı; yalnız çıkarılan efekt kareleri var (`kaynak/efekt/{fire_burst,fire_blade,vurus_tam}`).
Araçlar: `araclar/efekt/cikar2.py VIDEO_A VIDEO_B`, `kur2.py VIDEO_A VIDEO_B` → `onizlemeler/efekt2_onizleme.png`.

| Efekt | Kayıtta | Kare | Boyut (px) | Pivot | Genişlik |
|---|---|---|---|---|---|
| Fire Burst (moba) | b: 69–140 | 36 | 900 × 760 | mobun ayağı (0.478, 0.243) | 5.00 karakter boyu |
| Fire Blade (moba) | a: 228–265 | 19 | 560 × 820 | ışının yere değdiği halka (0.286, 0.165) | 3.11 |
| Karaktere vuruş (tam) | a: 160–195 | 18 | 470 × 430 | karakterin ayağı (0.50, 0.221) | 2.61 |

- Karakter boyu kayıtta ~180 px. Doğrulama (zemin + eklemeli kare ↔ orijinal): ortalama mutlak fark
  **7.6 / 6.2 / 8.4** (255 üzerinden); fark çoğunlukla karakter/yaratık hareketinden ve doldurulan bölgelerden.
- Fire Burst: 0–0.15 sn dışa açılan sivri turuncu ışınlar + sarı çekirdek, uçuşan kor parçaları → 0.2–0.5 sn
  yuvarlak turuncu-sarı alev bulutu → 1.0 sn'de söner. 0.47 sn'den sonra oyuncuya gelen vuruş ışıması aynı yere
  biniyordu: oyuncu çevresi (r 150 px, yumuşak kenar) bu karelerden silindi (o ışıma = VurusTam).
- Fire Blade: gökten inen ince turuncu ışın (beyaz-sarı çekirdek, pembe-turuncu hale) + yerde kırmızımsı halka;
  0.4 sn'de söner. Önündeki ad etiketleri / hedef çubuğu bandı sütun boyunca dikey ara değerle tamamlandı.
- Vuruş (tam): sarı çekirdekli yuvarlak ışıma + ince beyaz halka → kırmızı-turuncu sivri kenarlı patlama →
  0.22 sn beyazımsı tepe → 0.3 sn'de biter (ilk paketteki kırpık vuruşun tamamı).
- Temizlik: eklemeli ışık zemini karartamaz → kararan / yeşil-mavi değişen pikseller (yaratık, karakter, çim)
  komşu ışıktan dolduruldu; ışık içinde kalan karanlık delikler kapatıldı; G ≤ R (çim artığı kalmasın).
- Sınır: karakterin tam arkasında kalan ışık tahmini (komşudan dolgu); Fire Burst'ün yer düzlemi (alt düz kenar)
  kameraya dönük dörtgende perspektifiyle taşınır. Unity'de denenmedi.

---

## Ek 3 — Karakter altı ateş havuzu (ayrı paket)
Paket `unity_paketleri/OlymposAtesHavuzu1298.unitypackage` (namespace `Olympos.AtesHavuzu`, sınıf `OlymposAtesHavuzuOynatici`,
shader `Olympos/Ates Havuzu Eklemeli`, menü `OLYMPOS > 1298 > Ateş Havuzu (Karakter Altı) Oluştur`).
Kaynak: kayıt 19-30-28 (2712 × 1220, ~67 kare/sn, depoya konmadı) → 30 kare/sn. Araçlar `araclar/efekt/cikar3.py`, `kur3.py`;
önizleme `onizlemeler/efekt3_onizleme.png`.

- Kamera 30fps karesi 67'de durur; efekt ~0.2 sn önce başlamış → ilk anı alınamadı, oynatıcıda 0.15 sn açılış.
- Zemin = efekt sonrası 116–131 karelerinin medyanı (aynı kamera). 39 kare (67–105), 560 × 420 px, kutu (1100,460).
- Doyma: merkezde orijinal 255; `O − B` sarı zeminde mavimsi kalıyordu → parlaklığa göre (215–250) ışığın kendi rengiyle harmanlandı.
- Karakter ~150 px, ayak (1360,712) → pivot (0.464, 0.40), genişlik 3.73 karakter boyu, en/boy 0.75. Havuz ~440 × 220 px.
- Ad etiketi ve karakter silueti dolduruldu; siluet içi %35 zayıf (yumuşak elips). Doğrulama: zemin + efekt ↔ orijinal ort. fark **8.0** / 255.

---

## Ek 4 — Manes Of Fire (moba uygulanan skill, ayrı paket)
Paket `unity_paketleri/OlymposManesOfFire1298.unitypackage` (namespace `Olympos.ManesOfFire`, sınıf `OlymposManesOfFireOynatici`,
shader `Olympos/Manes Of Fire Eklemeli`, menü `OLYMPOS > 1298 > Manes Of Fire (Moba) Oluştur`).
Kaynak: tablet kaydı 21-40-04 (2266 × 1488, 60 kare/sn; depoya konmadı). Araçlar `araclar/efekt/cikar4.py`, `kur4.py`; önizleme `onizlemeler/efekt4_onizleme.png`.
- Kamera 100–235 arası sabit; zemin = 100–118 medyanı (mob + seçim halkası yerinde). Kareler 118–214, 2'de bir → 49 kare, 30 kare/sn.
- Kutu (1215,0) 520 × 940 (ışın ekranın tepesine kadar). Mob ~140 px, ayak (1405,822) → pivot (0.365, 0.126), genişlik 3.71 boy, en/boy 1.808.
- Maskeler: "Open" düğmesi (1215,686)–(1364,774), mob adı, karakter (sol kenar). Doğrulama: zemin + efekt ↔ orijinal ort. fark **5.8** / 255.
- Sınır: mob 1.0 sn'den sonra yürüyor; zemin mobu eski yerinde tutuyor (efekt karelerine etkisi yok, önizlemede görünür).
- İkinci açı (kayıt 21-48-55, alçak kamera, 2.4 sn, ~1.7 sn'de kontrol merkezi açılıyor): prizma ve ışın aynı biçimde → kameraya dönük (billboard)
  varsayımı doğrulandı. Kare çıkarılmadı (efekt küçük, adlar/HP çubukları önünde, sonu kesik). Yerdeki halkalar bu açıda görünmüyor;
  halkalar ilk kaydın perspektifinde kareye gömülü — çok farklı kamera açısında ayrı yer dekalı gerekebilir.


---

## Ek 5 — Kendi skill efektleri (9 kayıt, ayrı paket)
Paket `unity_paketleri/OlymposKendiSkill1298.unitypackage` (namespace `Olympos.KendiSkill`, sınıflar `OlymposKendiSkillEfekti`,
`OlymposKendiSkillKutuphanesi`, shader `Olympos/Kendi Skill Eklemeli`). Araçlar `araclar/efekt/cikar5.py KLASOR`, `kur5.py KLASOR`;
önizleme `onizlemeler/efekt5_onizleme.png` (+ efekt başına `efekt5_<ad>.png`). Kayıtlar depoya konmadı.
- Skill adları Information panelinden: Hide, Light Feet, Cat's Eyes, Lupine Eyes, Evade, Safety, Scaled Skin, Cure Disease, Cure Curse, Magic Shield.
  Cast süresi olan skill'lerde (Eyes, Cure) önce ortak "döküm yıldızları" oynuyor (cast çubuğu "Lupine Eyes 1,5 sec").
  Cat's Eyes ve Lupine Eyes aynı görsel; Cure Disease ve Cure Curse aynı görsel. Scaled Skin'in efekti kayıtların başından önce kalmış.
- Kesim kutusu (1000,150) 720 × 860 (30 kare/sn), karakter ~265 px, ayak (1370,835) → pivot (0.514, 0.203), genişlik 2.717 boy.
- Temizlik: (1) renk imzası kapısı — O−B artışının yönü efektin ölçülen rengine (altın / turuncu / kırmızı / pembe; Cure'da beyaz) yakın
  değilse atılır (karakterin gri zırhı, sarı-yeşil teni); (2) gövde elipsi (1370,700, 92×150) içinde cast hareketi zayıflatılır;
  (3) kararan / yeşil artan pikseller ve cast çubuğu komşu ışıktan doldurulur; (4) isim etiketi bandı dikey doldurulur; (5) uzak yaratık etiketleri silinir.
- Doğrulama (zemin + efekt ↔ orijinal, ort. mutlak fark /255): dokum_yildizlari 6.2, hide 5.9, light_feet 3.2, kedi_gozu 3.6, evade 5.1, safety 4.3, cure 3.6, magic_shield 3.8.
- Sınır: karakterin tam arkasında kalan ışık tahmini; döküm yıldızları ve Hide'da gövde üstündeki ışıma kısmen zayıflatıldı.
- Ek kayıt seti (4 kayıt): Sprint, Swift, Strength Of Wolf, Minor Healing — aynı pakete eklendi (toplam 12 efekt). Renk imzaları: mor
  (Sprint), altın-turuncu (Swift, Strength Of Wolf), mavi (Minor Healing). Fark: sprint 2.9, swift 3.2, strength_of_wolf 2.9, minor_healing 3.6.
  Swift ve Strength Of Wolf'ta cast (döküm yıldızları) önce oynar; kütüphanede dokumlu: true ile kullanılır.

---

## Ek 6 — Yakın dövüş skill'leri: Stroke · Stab · Stab2 (ayrı paket)
Paket `unity_paketleri/OlymposYakinSkill1298.unitypackage` (namespace `Olympos.YakinSkill`, sınıflar `OlymposYakinSkillKatmani`,
`OlymposYakinSkillEfekti`, `OlymposYakinSkillKutuphanesi`, shader `Olympos/Yakin Skill Eklemeli`,
menü `OLYMPOS > 1298 > Yakın Skill Efektleri (Stroke · Stab · Stab2) Oluştur`).
Kaynak: telefon kaydı 14-31-04 (2712 × 1220, 8.5 sn; depoya konmadı). Araçlar `araclar/efekt/cikar6.py VIDEO [skill ...]`,
`kur6.py VIDEO` (önizleme `onizlemeler/efekt6_onizleme.png`, `efekt6_animasyon.mp4/.gif`), `paket6.py VIDEO` (Unity klasörü + kurucu,
şablon `paket6_kurucu.cs.tmpl`).
- Skill'ler (Information paneli): Stroke kare 45–77 (33 kare), Stab 109–135 (27), Stab2 202–217 (16); 30 kare/sn. Kamera sabit.
- İki katman: **karakter** (kesik yayları, kıvılcımlar; ayak (1360,828), karakter 243 px) ve **hedef** (gökten ışın, vuruş patlaması,
  sarı yıldız; hedef zemini = seçim halkasının merkezi: Stroke (1307,983), Stab (1175,1119)). Katmanlar ışın çizgisi (±300 px) + hedef
  diski (r≈300) ağırlığıyla ayrıldı; toplamları orijinal efekttir.
- Derinlik: seçim halkası yarıçapları (138 / 164 px) zemin ufkunu y=261 verir → hedef katmanı 1.273 (Stroke) / 1.513 (Stab) kat ölçekte
  ölçüldü (Unity'de karakter boyuyla aynı birim).
- Temizlik: iki zemin (öncesi + sonrası) min(O−B) ile hareketli solucan / karakter; seçim halkası (halkalı-efektsiz karelerden maske, +6 px)
  ve kırmızı etiketler, yeşil hedef oku, UI (hedef çubuğu, skill düğmeleri) komşu ışıktan dolduruldu. Renk kapısı: kırmızı baskın ya da
  limon sarısı (R ≥ 0.8 G), mavi R'yi geçmez; gövdede yalnız sıcak artış.
- Işın: E(x,y) ≈ I(y)·P(x − çizgi(y)) ayrışık modeli (ağaç gövdesi, çim dokusu, doyan gök ışına karışmasın); modelin üstündeki güçlü
  ışık korunur; patlamaya son 180 satırda orijinale geçiş. Işının olmadığı karelerde model kurulmaz.
- Doğrulama (zemin + iki katman ↔ orijinal, ort. mutlak fark /255): stroke **6.5**, stab **6.4**, stab2 **4.5**.
- Sınırlar: Stab'da patlamanın alt çubuk (y ≥ 1140) altındaki kısmı kayıtta yok; ışının eğimi kayıttaki ekran konumuna ait
  (kameraya dönük dörtgen); ışın ekran tepesinde kesildiği için hedef katmanında `_UstSonum` 0.08.

---

## Ek 7 — Efekt 7: kesik + pembe aura · yıldız vuruşu + hasar kırmızısı (ayrı paket)
Paket `unity_paketleri/OlymposEfekt7_1298.unitypackage` (namespace `Olympos.Efekt7`; sınıflar `OlymposEfekt7`, `OlymposEfekt7Katman`,
`OlymposEfekt7HasarRengi`, `OlymposEfekt7Kutuphanesi`; shader'lar `Olympos/Efekt7 Eklemeli`, `Olympos/Efekt7 Hasar Kirmizi`;
menü `OLYMPOS > 1298 > Efekt 7 (Kesik + Aura · Yıldız Vuruşu) Oluştur`). Kareler `kaynak/efekt7/`, araçlar `araclar/efekt7/`.
- Kaynak: kayıt 14-01-51 — galeride yavaş ileri sarılan oyun videosunun ekran kaydı. Oyun zamanı ekrandaki süre kutusundan okundu
  (`ocr.py`, rakam şablonları), benzersiz kareler (`zaman.py`); 30 kare/sn'ye en yakın kareyle örneklendi.
- Ayıklama (`cikar7.py`): zemin = efektsiz kareler (oyun zamanı 1.9–2.3 sn) ve sonraki; hedef silueti kırmızı karelerden;
  hedef içinde kırmızı boyanmış zemin çıkarılır, kalan ışık eklemeli; ARKA = siluet dışı (siluet içi komşudan), ÖN = siluet içi.
- Hasar kırmızısı (4 karede, kanal başına doğrusal): R = 0.60 L + 162, G = 0.95 L + 5, B = 0.75 L (L = zemin parlaklığı).
- Doğrulama (`kur7.py`, önizleme `efekt7_onizleme.png`, `efekt7_animasyon.mp4`, geniş açı `efekt7_genis.*`): ort. fark kesik_aura 8.4, yildiz 2.6 /255.
- Ek (uzak kayıtlar 16-33-29 / 16-33-43, gerçek hız; efekt 7 kareleri değiştirilmeden): `uzak2.py` özellik + DTW ile gerçek zamanlama,
  `uzak3.py` altın yapraklar katmanı (`kaynak/efekt7/yapraklar`, `gercek_zamanlama.json`), `temiz.py` arka katmanın çitsiz kopyası;
  önizleme `efekt7_uzak_a.*`. Gerçek döngü ≈ 1.2 sn (kesik+aura ≈ 0.53 sn, ardından yıldız + 0.2 sn kırmızı). Pakette henüz yok.
- Ayrık paketler (kullanıcı isteği): `OlymposMobHasar1298` (yalnız mob hasar rengi, `Olympos.MobHasar`) ve `OlymposEfekt7Skill1298` (yalnız skill ışıkları, `Olympos.Efekt7Skill`); önizlemeler `efekt7_paket_hasar.*`, `efekt7_paket_skill.*` (`paket_onizle.py hasar|skill`). Efekt 7 paketi aynen duruyor.
