# Skill Sistemi — Unity'ye Yüklenebilir Veri ve Yükleyici

> Tarih: 7 Kasım 2026

## 0. MykoMobile'ın skill'leri neden verilmedi

İki ayrı sebep var ve ikisi de tek başına yeterli.

**Hukuki.** MykoMobile'ın skill tablosunu çıkarıp senin oyununa koymak, başka
bir stüdyonun içeriğini kullanmak olur. Gerekçe `docs/02` Bölüm 7.3'te:
kod tabanı NOWA Games'e ait görünüyor ve içinde Knight Online'ın tescilli
isimleri var. Mgame'in Ocak 2025 davası tam bu olgu örüntüsüne dayandı.

**Olgusal.** APK'da "bütün skiller" diye bir şey yok. Oyun içeriği çalışma
anında `development.mykomobile.com`'dan AssetBundle olarak iniyor (APK 145 MB,
site 2 GB depolama istiyor — fark buradan) ve yetkili skill tablosu sunucu
tarafında. Yani çıkarmaya çalışsam da elde edilecek şey eksik olurdu.

Onun yerine **senin skill sistemini Unity'ye yüklenebilir hale getirdim.**
40 skill zaten `docs/03` ile üretilmişti ama Unity tarafında yükleyici yoktu;
asıl eksik olan buydu.

---

## 1. Ne eklendi

| Dosya | İşlev |
|---|---|
| `unity/Assets/Resources/GameData/skills.json` | **40 skill, 200 rank** — oyunun okuduğu veri (130 KB) |
| `unity/Assets/Scripts/Model/SkillData.cs` | Veri sınıfları: `SkillData`, `SkillRankData`, `SkillEffectData` |
| `unity/Assets/Scripts/Model/SkillDatabase.cs` | Çalışma zamanı yükleyici + arama + doğrulama |
| `unity/Assets/Scripts/Model/SkillDefinition.cs` | ScriptableObject (ikon/VFX bağlamak için, opsiyonel) |
| `unity/Assets/Scripts/Editor/SkillImporter.cs` | JSON → ScriptableObject asset üretimi |
| `docs/schema/01_core_schema.sql` | Yeni `skill_rank` tablosu |
| `tools/generate_content.py` | Rank üretimi + Unity ihracı |

### Kullanım — tek satır

```csharp
SkillDatabase.Load();                                   // açılışta bir kez
SkillData s = SkillDatabase.GetByCode("warrior_sert_vurus");
SkillRankData r = s.GetHighestRankForLevel(myLevel);
Debug.Log(r.effects[0].Describe());                     // "119 hasar (silah x2.3)"
```

**Hiçbir editör adımı gerekmiyor.** `Resources` altındaki JSON'dan okur, Play'e
basınca çalışır.

---

## 2. Rank sistemi

Her becerinin 5 rank'ı var; oyuncu beceri puanı harcayarak yükseltir.

```
 rank  seviye   MP  bekleme  hasar  silah x
    1       2   12    4.00s     70   1.350
    2      26   15    3.84s     94   1.823
    3      50   18    3.68s    119   2.295
    4      74   21    3.52s    144   2.768
    5      98   24    3.36s    168   3.240
```

Rank aralığı beceriye göre hesaplanır: son rank seviye 98'i geçmez. Seviye 2'de
öğrenilen beceri geniş aralıkla gelişir (2→26→50→74→98), seviye 82'de
öğrenilen sık aralıkla.

Bekleme süresi rank ile **hafif düşer** (%4/rank). Tamamen sabit kalsa yüksek
rank sadece "daha pahalı aynı şey" olurdu.

### Neden `skill_rank` ayrı tablo

Knight Online'da her beceri rank'ı `MAGIC` tablosunda **ayrı satır** tutuluyordu
— 1522 satırın sebebi bu. İsim, açıklama ve hedef tipi her rank için tekrar
ediyordu; bir ismi değiştirmek 5 satır güncellemek demekti.

Burada tanım (`skill_template`) tek, rank'a göre değişen sayılar
(`skill_rank`) ayrı. 40 tanım + 200 rank = 240 satır, isim tekrarı yok.

`character_skill` bileşik yabancı anahtarla `(skill_id, skill_rank)` →
`skill_rank(skill_id, rank)` bağlı. Yani **oyuncu tanımlı olmayan bir rank'a
sahip olamaz** — veritabanı seviyesinde engelli. Doğrulandı: rank 99 eklemek
denendiğinde FK reddediyor.

---

## 3. Etki (effect) modeli

11 etki tipi destekliyor. Hepsi `effects` dizisinde, **sıralı liste** olarak:

| kind | Örnek |
|---|---|
| `damage` | Ateş Oku: 75 hasar (silah x1.45) |
| `damage_over_time` | Zehirli Bıçak: 12 sn boyunca 46 hasar/2 sn |
| `heal` | Kutsal Işık: 92 iyileştirme |
| `buff` | Mana Kalkanı: all_stats +%14, 15 sn |
| `debuff` | Zaman Yarığı: armor %-27, 10 sn |
| `control` | Buz Zinciri: root, 3.2 sn |
| `threat` | Meydan Okuma: tehdit x4, 6 sn |
| `movement` | Işınlanma: dash, 8 m |
| `stealth` | Gizlenme: 20 sn |
| `cleanse` | Arındırma: 2 etki temizle |
| `revive` | Diriliş: dirilt (%30 HP, %20 MP) |

Bir beceri birden fazla etki taşıyabilir — örneğin hem hasar hem zırh kırma.
Yeni etki tipi eklemek şema değişikliği gerektirmez.

### Neden düz şema (bütün alanlar her kayıtta var)

Unity'nin `JsonUtility`'si **polimorfik tip okuyamaz**: `kind` alanına bakıp
farklı sınıfa deserialize etme yeteneği yok. Alternatif Newtonsoft.Json ile
özel converter yazmaktı ama bu ek paket bağımlılığı demek.

Çözüm: bütün etki alanları tek sınıfta (`SkillEffectData`), kullanılmayanlar
`0` / `""`. `kind` hangi alanların anlamlı olduğunu söyler. Birkaç yüz bayt
israf eder, karşılığında sıfır bağımlılık ve hızlı okuma verir.

Bu yüzden `content/skills.json` (veritabanı için, değişken anahtarlı) ile
`unity/Assets/Resources/GameData/skills.json` (Unity için, düz) **ayrı
dosyalar**. İkisi de aynı üreteçten çıkıyor, yani ayrılamazlar.

**Koruma:** `SkillEffectData`'ya alan eklersen `generate_content.py` içindeki
`UNITY_EFFECT_FIELDS` sözlüğüne de ekle. Üreteç, şemada tanımsız bir alan
görürse **hata verir** — sessizce yutmaz. Bu, "JSON'da var ama C# okumuyor,
bütün değerler 0" sınıfı hatayı baştan engeller.

---

## 4. ScriptableObject yolu — opsiyonel

Oyun JSON ile çalışır, yani bu adım **zorunlu değil.** Asset'lere yalnızca
beceriye **Unity varlığı** bağlamak gerektiğinde ihtiyaç duyarsın: ikon, ses,
VFX prefab'ı, animasyon klibi. Bunlar JSON'da tutulamaz çünkü Unity referansı
gerektirir.

```
Tools > Koray > Skill Asset'lerini Üret
```

`Assets/GameData/Skills/<sınıf>/<kod>.asset` dosyalarını üretir.

**Yeniden üretim sanat bağlantılarını silmez.** Importer yalnızca sayısal
veriyi (`SkillData`) günceller; elle bağladığın `Icon`, `CastVfx`,
`ImpactVfx`, `CastSound`, `AnimationStateName` alanlarına dokunmaz. Yani
içeriği yeniden üretmek güvenli.

İkinci menü komutu `Tools > Koray > Skill Verisini Doğrula` asset üretmeden
sadece veri tutarlılığını kontrol eder.

---

## 5. Sunucu mu istemci mi — önemli ayrım

Bu veri istemcide **arayüz, önizleme, ikon ve VFX seçimi** içindir.

Hasarın **gerçek hesabı sunucuda** yapılır (`docs/01` Bölüm 6.2). İstemci
"bu beceri 119 hasar verir" diye gösterir; sunucu ne verdiğini kendisi
belirler. İkisi ayrılırsa gösterilen sayı yanlış olur **ama oyun
hilelenemez** — doğru ödünleşme budur.

Bu yüzden `SkillDatabase` bir hasar hesaplama motoru içermiyor. İçermesi
gerekse de o motor sunucuyla **paylaşılan bir derleme hedefinden** gelmeli,
yoksa iki kopya zamanla ayrılır.

---

## 6. Doğrulama

Unity kurulu olmadığı için `JsonUtility`'nin çalışan bir taklidini yazdım
(gerçek bir JSON ayrıştırıcı + yansıma ile alan bağlama) ve **gerçek C#
sınıflarını gerçek veriyle** çalıştırdım:

```bash
bash tools/unity-compile-check/check.sh --run
```

Bu, bu işin en büyük riskini kapatıyor: JSON'da `baseValue` yazarken C#'ta
`base_value` olsa Unity sessizce `0` okur ve **bütün hasar değerleri sıfır
olur.** Koşum tam olarak onu yakalar.

| Kontrol | Sonuç |
|---|---|
| Derleme (uyarılar hata sayılarak) | temiz |
| `Resources`'tan yükleme | 40 beceri, şema v1 |
| Alan bağlama (14 somut değer kontrolü) | hepsi dolu ve doğru tipte |
| Türkçe karakterler | `Sert Vuruş`, `Kutsal Işık` doğru |
| Rank ölçeklemesi artan mı | evet (70→168 hasar) |
| 11 etki tipinin hepsi okunuyor mu | evet |
| Sınıf dağılımı ve seviye sırası | 4×10, sıralı |
| Beceri ağacı (önkoşul, döngü, rank sırası) | sorun yok |
| `GetHighestRankForLevel` | sv 1 öğrenilemez, sv 100 rank 5 |
| SQL: 01 + 02 yükleme | temiz, 40 skill / 200 rank |
| SQL: canlı öğrenilmiş beceri varken yeniden seed | FK ihlali yok |
| SQL: olmayan rank (99) | bileşik FK reddediyor |

### Yakalanan iki hata

**1. Seed, canlı veritabanında patlıyordu.** İlk sürüm `DELETE FROM skill_rank`
yapıyordu. `character_skill` buraya FK ile bağlı olduğu için tek bir oyuncu
beceri öğrenmişse DELETE FK ihlaliyle patlar ve **bütün seed başarısız olur.**
`ON CONFLICT DO UPDATE` ile yerinde güncellemeye çevrildi; test edildi.

**2. Test kendi hatasıyla düştü.** İlk FK testinde kullanıcı adı `'t'` idi;
şemadaki `CHECK (length(username) BETWEEN 3 AND 32)` reddetti ve test anlamsız
"OK" verdi. Kısıt doğru çalışıyordu, test yanlıştı — düzeltilip gerçek senaryo
koşuldu.

### Neyi kapsamıyor

`JsonUtility` taklidim gerçek Unity değil. Gerçek `JsonUtility`'nin
davranışını (yalnızca public alanları doldurma, eksik alanları varsayılan
bırakma, fazlasını yok sayma) taklit ediyor ama birebir aynı olduğu garanti
değil. Ayrıca ScriptableObject serileştirmesi, Inspector görünümü, asset
üretimi ve `Resources.Load` gerçek davranışı Unity'de test edilmedi —
`SkillImporter` yalnızca derlendi, çalıştırılmadı.

Projeyi Unity'de bir kez açıp `Tools > Koray > Skill Verisini Doğrula`
komutunu çalıştırman yeterli; Console'da aynı sonucu görmelisin.

---

## 7. Genişletme

Yeni beceri eklemek: `tools/generate_content.py` içindeki `SKILLS` sözlüğüne
satır ekle.

```python
"warrior": [
    ...
    ("kalkan_hucumu", "Kalkan Hücumu", "damage", "single_enemy", 1.60, 35, 12000, 3.0, 40),
    #  kod            ad               tür       hedef           güç   MP  bekleme menzil seviye
]
```

Sonra:

```bash
python3 tools/generate_content.py                 # JSON + SQL + Unity ihracı
bash tools/unity-compile-check/check.sh --run     # doğrula
psql -d oyun -f docs/schema/02_content_seed.sql   # veritabanına yükle
```

Rank sayısını değiştirmek: `SKILL_RANKS = 5`. Ölçekleme: `RANK_POWER_STEP`,
`RANK_COST_STEP`.

### Henüz yok

- **Etki çalıştırma motoru** — veri hazır, uygulama sunucuda yazılacak
- **Beceri çubuğu UI'ı** — `character_skill_bar` tablosu var, Unity tarafı yok
- **Beceri ağacı ekranı** — `reqSkillId` zinciri hazır, görselleştirme yok
- **İkon ve VFX** — `SkillDefinition` alanları hazır, varlıklar yok
  (meşru kaynaklar: `docs/03` Bölüm 5.3)
- **Yerelleştirme** — isimler şimdilik Türkçe gömülü
