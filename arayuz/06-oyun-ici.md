# 06 · Oyun içi öğeler — scroll basma/silme, Save Skill Slot, Show Drops, hedef iptal

Kaynak: kullanıcının gönderdiği **2 video** (2712 × 1220, H.265; 20,8 s ve 10,6 s) ve **2 ekran görüntüsü**.
Paket: `unity_paketleri/OlymposOyunIci1298.unitypackage` · kaynak: `unity_kaynak/Assets/OlymposOyunIci1298/`
Önizleme: `onizlemeler/oyun_ici_onizleme.png` (orijinal ↔ yeni, 7 panel).

## Yöntem

| Adım | Araç | Not |
|---|---|---|
| Kare çıkarma | `araclar/oyun_ici/medyan.py` | Sabit anların 15–24 karesinin piksel medyanı → H.265 gürültüsü bastırıldı. Referanslar `referans_gorseller/oyun_ici/` (JPEG q90, 4:4:4). |
| Krom ayırma | `araclar/oyun_ici/cikar.py` | Aynı sahnenin pencereli (O) ve penceresiz (B) karesi var: `R = O − (1−a)·B`. `R≈0` saf zemin; krom siyaha karşı çözülür (`alfa = max(R)/T`, `RGB = R/alfa`) → siyah zemin Image'ının üstünde orijinali verir. |
| Font / punto | `araclar/oyun_ici/punto.py` | Aday fontlar 10–63 punto taranır; mürekkep genişliği + IoU. |
| Doğrulama | `araclar/oyun_ici/kur.py` | Kurucunun Python benzetimi: aynı sprite + koordinat + punto ile yeniden kurar, orijinalle yan yana koyar. |

## Saydamlıklar (ölçüldü)

| Öğe | Alfa | Nasıl ölçüldü |
|---|---|---|
| Eşya penceresi zemini | **0.92** | pencereli/penceresiz kare oranı (0.908–0.934) |
| Drop List zemini | **0.89** | aynı (0.871–0.93; düşük uç kromda hayalet bırakmıyor) |
| Drop ipucu zemini | **0.93** | aynı (0.916–0.942) |
| Save Skill Slot zemini | **0.95** | arkadan görünen oyuncu adının parlaklığı (≈0.955) — tek fotoğraf var |
| Boş hızlı slotun iç diski | **0.88** | iç/dış çim oranı, 3 kare × 5 slot (0.86–0.89) |
| Düğmeler, ikonlar, hedef çubuğu, X | opak | — |

## Fontlar

| Yazı | Font | Punto | Renk |
|---|---|---|---|
| Eşya adı / türü / açıklaması | Roboto Bold | 36 / 27 / 27 | `#FFE7E9` (hafif pembe beyaz) / `#FCD100` / `#FFE7E9` |
| Buff süresi ("59m") | Roboto Bold + dış hat | 27 | `#FFE7E9` |
| Slot adedi | Roboto Bold + dış hat | 31 | beyaz |
| Hedef adı / seviye | **DejaVu Sans Bold** (IoU 0.56; Roboto 0.37) | 30 / 16 | `#FE5356` / `#8EE13A` |
| Drop kutu etiketi | Roboto Slab Bold | 19 | Middle beyaz · Low `#FAE800` |
| Sayfa yazıları ("0/0", "1/2") | Roboto Slab Regular | 32 | `#E3B170` |
| İpucu adı / tür / Drop Rate / stat / orta blok | Roboto Bold | 36 / 27 / 32 / 29 / 27 | mor `#CA89E7`, kırmızı `#FE0001`, yeşil `#96C019` / `#80C366` |
| Save Skill Slot durum yazısı | Roboto Slab Bold + dış hat | 29 (satır adımı 42 px) | beyaz |

Sabit etiketler (pencere başlıkları, "Monster", "Item Name", Save/Activate, Use Self…, Remove/Close, Show Drops,
"You can save your skill bar + skill point.") **orijinal piksellerden** korunur; yalnız değişen yazılar Text'tir.

## Ölçüler (ekran pikseli, 2712 × 1220; sol-üst köşe)

**Eşya penceresi** 663 × 313 — ikon çerçevesi (2,2) 103², ikon (9,9) 89²; ad x=113; ayırıcı y=236, x=11 → *ad sağı + 20*;
açıklama bu genişlikte ortalı (3 pencerede doğrulandı: 485/407/490); düğmeler y=248: x=11/173/334/496, 155 × 62.
Pencerenin sağ-üst köşesi dokunulan yuvanın merkezinin ≈32 px solunda, 14 px üstünde açılır.

**Buff çubuğu** ikon 64², adım 66, sağ kenar x=2309, üst y=56 (sağa yaslı; yeni etki sağa eklenir).
Menü: ok (2262,120) 30×18 · Remove (2180,136) 194×66 · Close (2180,206) 194×64 — dokunulan ikonun altında ortalı.

**Hızlı slotlar** halka 164, iç disk 144; ikon dairesel maskeyle 146. 14 merkez:
(2193,452) · (1840,595) (2030,595) (1657,634) (2235,634) (2431,638) · (1893,770) (2085,781) (1541,799) (1722,799) ·
(1547,961) (1715,961) (1889,968) (2084,971). Adet yazısı merkezin 51 px altında.

**Hedef** ad merkezi (1370,75) · çubuk (1178,96) 404×41 · Lv x=1190, y=117 · Show Drops (1298,134) 152×54 ·
iptal X (2503,784) 140².

**Drop List Search** (176,82) 698 × 1116 — zemin (6,8) 683×1107 · onay kutuları (36,88)/(36,164) 55² ·
arama (31,243) 648×65 · sonuç listesi (34,314) 642×323, 5 satır · üst sayfa okları (237,645)/(408,646), yazı merkezi (350,669) ·
kutular x=64+115c, y=703+111r, 103² (5×3) · alt oklar (213,1032)/(417,1031), yazı merkezi (352,1073).
İpucu örneği 484 × 621: ayırıcılar y=194/355/543 (x=12, genişlik = kutu − 26), stat merkezleri 241 + 38.5k,
orta blok adımı 31, Close (12,556).

**Save Skill Slot Stat** (1196,110) 526 × 1056 — satır başı y=85+245k · Save (26, +169) 236×64 · Activate (269, +169) ·
durum yazısı merkezi +118 · kapat (462,2) 64².

## Çalışma mantığı (videodan gözlenen)

1. **Envanterden basma:** eşyaya dokun → pencere → *Use Self* → pencere kapanır, adet −1 (5→4), HP 419→919,
   sağ üstte ikon + "59m". Speed-Up Potion ve Scroll of Armor için aynı.
2. **Basılanı silme:** etki ikonuna dokun → *Remove / Close*. Remove sonrası ikon kalkar (3→2), HP 919→419.
3. **Skill bardan basma:** eşya envanterden yuvaya sürüklenir (sürüklerken kaynak yuva boş görünür, bırakınca eşya
   envanterde kalır). Yuvada dairesel ikon + **kalan adet** (zırh 4→3, iksir 3→2 basınca düştü). Yuvaya dokununca
   bilgi satırına `Using - Scroll Of Armor 150(L)` / `Using - Speed Potion` yazılır.
4. **Save Skill Slot:** 4 kayıt; dolu kayıt `Fire:41 - Ice:23` / `Lightning:0 - Master:0`, boş kayıt `- Empty -`.
5. **Show Drops:** hedef çubuğunun altında; pencere *Monster* işaretli açılır, kutularda 2 GROUP + 1 eşya (1/1).
   GROUP → 15'erli eşya sayfaları (1/2). Eşya → ipucu (*Drop Rate : Middle*). Pencere kapatılıp açılınca köke döner.
6. **Hedef iptal:** kırmızı X yalnız hedef seçiliyken görünür.

## Varsayımlar (videoda yok — açıkça işaretli)

- Arama sonuç listesi hep boştu ("0/0"); arama davranışı (ada göre süzme, sonuca basınca drop'ları gösterme) varsayım.
- 1 dakikanın altındaki süre yazısı ("45s"), adedi biten eşyanın yuvadan kalkması.
- İpucunun kutuya göre konumu tek tek örneklerden çözülemedi; kutunun sağ üstüne açılıp ekrana sığdırılıyor.
- Hedef can çubuğunun boş hâli görülmedi; oluk aynı sprite koyulaştırılarak yapıldı.
- Videoda skill bardan *Hp Scroll* iki kez basıldı, bilgi satırı yazdı ama adet düşmedi ve etki eklenmedi
  (sebep görünmüyor); pakette her başarılı basış adedi düşürür.
- 2. kaydın numara rozeti diğerlerinden farklı (pembe-mor); anlamı bilinmiyor, piksel olarak korundu.

## Doğrulama

- Mono `mcs` ile tüm paketler birlikte derlendi: **0 hata, 0 uyarı** (`araclar/derleme_kontrolu/derle.sh`).
- Paket ↔ `unity_kaynak` : 57 girdi, 51 dosya, GUID + SHA-256 eşleşmesi **0 sorun**; kurucudaki 20 sprite kutusu sprite
  boyutlarıyla eşleşiyor.
- **Unity'de import denenmedi** (ortamda Unity yok).
