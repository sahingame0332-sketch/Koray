# 12 · Görev NPC'si — "?" rozeti, QuestList, görev detayı

Kaynak: 4 telefon ekran görüntüsü (2712 × 1220) `referans_gorseller/gorev/`: `q_once` (NPC uzakta, "?" rozeti), `q_open` (Open düğmesi),
`q_liste` (QuestList; q_open ile aynı sahne), `q_detay` (Starter Weapon&Armor).
Paket: `unity_paketleri/OlymposGorevNpc1298.unitypackage` (sınıflar `OlymposGorev*`). Önizleme `onizlemeler/gorev_onizleme.png`.
Araçlar `araclar/gorev/`: `cikar_rozet.py`, `cikar_krom.py`, `cikar_pencere.py`, `punto.py`, `kur.py`.

## "?" rozeti
- Rozet merdivenin önünde; basamak şeritlerinin kontrastı rozet içinde azalıyor ama kaybolmuyor → **geçirgenlik ölçüldü**
  t(r) = std_iç / std_dış: merkez 0.37–0.55, hale 0.30, r ≥ 175 → 1. Renk merkezde 255'e dayanıyor → ışık ekleniyor.
  İkisini birden taşıyan **ön-çarpımlı** karışım: `O = t·Bg + C`. Unity: `Olympos/UI On Carpimli` (Blend One OneMinusSrcAlpha).
- "?" harfi opak (sarı gövde), çevresinde koyu kahve (#2D160C) yumuşak gölge — gövdeden uzaklığa göre ölçülen profil.
- Sınır: orijinalde rozet dünyada (sağ altı duvarın arkasında kalıyor); paket ekran katmanında.

## Pencereler
Krom ayırma genie yöntemiyle (arkadan geçen ışık `k·(B/255)^1.8`): QuestList k=56 → zemin alfası **0.91**, detay k=42 → **0.93**.
Opak parçalar (başlık taşı, düğmeler, çerçeve) renkleri doğrudan orijinalden (çıkarma arkadaki ad etiketlerinin hayaletini bırakıyordu).
Yarı saydam gri açıklama kutuları ölçülen medyan renk/alfa ile düzlendi (arkadaki karakter/ad izleri silindi).

| Yazı | Font | Punto | Renk |
|---|---|---|---|
| QuestList başlığı | orijinal piksel | — | — |
| Test NPC Description. | Liberation Sans Bold | 16 | `#DD9344` |
| Görev satırı adı | Liberation Sans Bold + dış hat | 22 | `#F6E1E1` |
| Detay başlığı | Liberation Sans Bold + dış hat | 19 | `#EEDADA` |
| Kill: 20x Orc Watcher | Liberation Sans Bold | 16 | `#E09869` |
| Hunt: Shilan / Shilan öldür. | Liberation Sans Bold + dış hat | 16 | `#EAD8D8` |
| Ödül adları | Liberation Sans Bold + dış hat | 16 | `#E9D6D6` |
| Accepted | Liberation Sans Bold + dış hat | 21 | `#F0DDDE` |
| Objectives / Rewards / Close | orijinal piksel | — | — |

Ölçüler (ekran, sol-üst): QuestList sprite (1040,372) 642×470, zemin (1056,388) 566×441, portre merkez (1181,567) r 63,
görev satırı (1122,694) 468×82 · detay sprite (1052,172) 596×840, zemin (1070,187) 559×811, portre (1181,358),
hedef satırı (1117,496) 475×78, ikon (1132,512) 46², ödül hücresi (1128,638) 228×74, adım 229/76, ikon +(13,15) 47×45, ad +(67,19),
Accepted (1153,958) 203×37, Close (1362,958) 150×37.
Font seçimi: IoU + mürekkep genişliği (Liberation Sans = Arial metrikleri; UIF kayıtlarında çoğunluk Arial).
Unity'de denenmedi.
