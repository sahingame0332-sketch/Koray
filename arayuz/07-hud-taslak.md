# 07 · Oyun içi HUD — taslak (yarım; paket YOK)

Kaynak: `referans_gorseller/hud_ekranlar/hud_01..04.png` (2266 × 1488, dört farklı sahne).
Durum: geometri + saydamlık ölçüldü, 45 sprite kesildi (`kaynak/hud/sprites/`), ilk yeniden kurulum denendi.
**Kullanıcıya önizleme gösterilmedi, Unity paketi yapılmadı** — araya oyun içi öğeler işi girdi (bkz. 06).
Araçlar: `araclar/hud/` (kareler arası varyans maskesi, sprite kesimi, yazı silme, benzetim).

## Ölçülenler
- Font: Roboto Slab Bold (yakın çekimde slab serif doğrulandı). Punto: alt bar 26 · sağ panel 25 · ad 27 · Exp 22 ·
  altın 33 · sohbet sekmesi 18 · sohbet satırı 31 · görev satırı 28. (HP/MP, Diez/CR, MykoMobile yazıları için kutular
  daraltılıp yeniden ölçülmeli.)
- Alt bar y=1407..1487, tam genişlik. Düğmeler y=1417, h=52: PM 82/115 · Character 216/180 · Map 418/129 · Skills 567/164 ·
  Sit 750/98 · Town 1410/91 · Commands 1518/174 · Inventory 1714/165 · Trade 1900/140 · Exit 2057/130 (x/genişlik).
  Orta plaka (x≈856..1405) yarı saydam siyah **≈0.75** (kenar yöntemi 0.758, std oranı 0.68); gerisi opak.
- Sohbet günlük panelleri x=7..810 ve 813..1366, y≈1028..1318: düz siyah **0.46** (iki pencere, dört sahne: 0.456 / 0.458).
- Bildirim çubuğu (7,922) 806×56: sıcak gri ≈`#8C7E70`, alfa ≈0.84. Sekmeler y=978, h=48: x=3/164/321/478/635.
- Sağ üst panel x=1942..2266 **opak**: düğme sırası 0..73 · Time Left 74..98 · Diez 99..143 · CR 144..190 ·
  Active Events 195..237 · Channel 244..291.
- Kamera düğmeleri (çap ≈88): (1981,346) (2069,348) (2160,346) (2068,435) (2161,436).
- Beceri çarkı (bu tablette 8 yuva, çap 134): (1875,859) (1745,974) (1909,1005) (2066,1009) (1634,1115) (1788,1124)
  (1631,1274) (1788,1277); oklar (2004,828) (2141,828); saldırı (1976,1180) çap 218.
- M/P/C düğmeleri 82²: M (459,3) · P (557,3) · C (459,96). Durum plakası (0,0) 452×240; HP (69,13) 353×36, MP (69,56) 353×34.

## Kalan
Yazıların silinip yeniden basıldığı tam önizleme → kullanıcı onayı → `OlymposHud1298` paketi.
Not: HUD 2266 × 1488 (tablet), oyun içi öğeler 2712 × 1220 (telefon) kayıtlarından; iki düzenin slot sayısı farklı (8 / 14).
