# 11 · Knight Genie — panel, AUTO ATTACK SETTINGS, aktif durum

Kaynak: kullanıcının 3 telefon ekran görüntüsü (2712 × 1220): `referans_gorseller/genie/`
`g_once` (panel, pencere kapalı) · `g_pencere` (aynı sahne, AUTO ATTACK SETTINGS + SKILL PAGE açık) · `g_aktif` (genie çalışırken, başka sahne).
Paket: `unity_paketleri/OlymposGenie1298.unitypackage` (tek başına; sınıflar `OlymposGenie*`, namespace `Olympos.UI`).
Önizleme: `onizlemeler/genie_onizleme.png`. Araçlar: `araclar/genie/` (`cikar_pencere.py`, `cikar_panel.py`, `cikar_aktif.py`, `punto.py`, `kur.py`).

## Yöntem
| Parça | Nasıl |
|---|---|
| AUTO ATTACK SETTINGS | Pencereli/penceresiz aynı sahne → krom ayırma. Arkadan geçen ışık **doğrusal değil**: `g_pencere ≈ 45.6·(g_once/255)^1.8` (çim 70→4, HUD yazısı 250→44). Bu modelle çıkarıldı; Unity'de siyah zemin **0.93** (sahnenin orta tonlarında ölçülen oran 0.057–0.078). Parlak HUD öğeleri orijinalde biraz daha görünür. |
| Hareketli parçalar | 4 topuz (21×73), onay işareti, değer yazıları ayrıldı; topuz altı iz satır ara değeriyle, işaretli kutu boş kutudan kopyayla tamamlandı. Kaydırıcı etiketleri orijinalde topuzun **üstünde** çizili (RECOVERY "AT") → ayrı katman `aa_etiketler`. |
| Knight Genie paneli | Opak; alfa = üç farklı sahnede (g_once, g_aktif, q_once) **değişmeyen** pikseller. Değişen yazılar aynı satırın temiz dokusundan aynalanarak silindi. |
| Skill kilidi | `O_aktif = (1−a)·O_önce + a·L`; 8 ikon üzerinden piksel başına en küçük kareler → kilit rengi ≈ #B6B2B3, alfa en çok 0.85. Yeniden bindirince ikon içi fark 4–9 / 255. |
| GENIE rozeti | Arka sahne çevreden yumuşak dolduruldu; `O = (1−a)·Bg + a·P` (P = pembe #F478D3); harfler ve parıltı yıldızları opak, orijinal renk. Ad etiketinin örttüğü alt kenar halkanın simetriğinden. |

## Ölçüler (ekran pikseli, sol-üst)
**Panel** (2308,50) 356 × 246 · düğmeler Başlat (2350,61) 70×66, Durdur (2425,61) 70×66, Ayarlar (2500,61) 68×66 ·
Time Left çubuğu y 129–150 · sunucu y 152–186 · CR y 198–232 · kanal y 247–284.

| Yazı | Font | Punto | Renk | Konum |
|---|---|---|---|---|
| Time Left : 244 Minute(s) | Roboto Slab Regular + koyu dış hat | 18 | `#FFFCEA` | merkez (2502, 137.5) |
| Ares - 1 | Roboto Slab Bold | 21 | `#AFEB9F` | merkez (2500.5, 170) |
| CR : 01:18:08 | Roboto Slab Bold | 23 | `#DCF19E` | sol 2393, merkez y 214 |
| Channel 2 | Roboto Slab Bold | 23 | `#EEF4EF` | sol 2393, merkez y 266.5 |
| Kaydırıcı değeri (40, %70…) | Roboto Slab Bold | 24 | `#D2A776` | merkez x 818, y = iz + 7 |

**AUTO ATTACK SETTINGS** sprite (262,30) 636 × 1162, siyah zemin (273,44) 604 × 1108 · kapat (816,45) 74² ·
slotlar 80 × 77, x = 322/410/497/585/672/760, y = 200/288 (ATTACK & DEBUFF), 458/547 (HEAL & BUFFS) · iksir (562,655)/(649,655) 67² ·
izler x 357–760, y = 762/840/919/997; topuz merkezi = 363.5 + p·405 · onay kutuları (328,1036)/(328,1090)/(612,1036)/(612,1090) 43×40.

**Aktif:** rozet 300², kayıtta merkez (1355,375) — ad etiketinin üstünün ~95 px üstü · kilit 96² ikon merkezine (ikon ≈118 px).

## Varsayımlar / sınırlar
- ATTACK RANGE aralığı 0–45 (40'ın topuz konumundan); MP topuzu %50 için beklenenden 8 px solda (değer 48–49 olabilir).
- CR sayacı geri sayar (görev kayıtlarında 01:20:05 → 01:19:45); neyin sayacı olduğu bilinmiyor.
- Time Left'in dakikada 1 azalması varsayım; rozet sabit (animasyonlu parıltı kaydı yok).
- Unity'de denenmedi.
