# MykoMobile APK — kullanılan hazır Unity paketlerinin tespiti (19 Kasım 2026)

Kaynak: APK içindeki `assets/bin/Data` (şifresiz) — MonoScript ad alanları, assembly adları, prefab adları.
İndirilen oyun içi paketler (`files/*.n`) şifreli olduğu için açılmadı (koruma aşılmadı).

## Görsel efekt (VFX) paketleri
| Kanıt (APK'da) | Paket | Yayıncı | Kesinlik |
|---|---|---|---|
| Ad alanı `PolygonArsenal`: PolygonEffectCycler, PolygonBeamScript, PolygonProjectileScript, PolygonSoundSpawn… | **Polygon Arsenal** (~1300 prefab; kılıç, büyü, kristal, RPG dövüş, mermi) | Archanor VFX | Yüksek |
| `HS_ParticleCollisionInstance`, `HS_TargetProjectile`, `HS_FrontSpawner`, `Hovl_DemoLasers`, `Hovl_LaserDemo` | **Hovl Studio** paketleri (mermi/vuruş + lazer; tam paket adı belirsiz — "Epic Lasers" ve projectile paketleri adaylar) | Hovl Studio | Yayıncı yüksek, paket orta |
| Assembly `AllIn1VfxAssmebly`, ad alanı `AllIn1VfxToolkit` | **All In 1 Vfx Toolkit** (shader/efekt aracı) | Seaside Studios | Yüksek |
| Ad alanı `MasterFX`: MEffectExample, MMagicExample, LaserShooter, BulletShooter, ParticleMappingController | Büyük olasılıkla **Master Magic FX** ailesi | (aynı adlı yayıncı) | Orta — doğrulanmadı |
| Prefab: `Power_Impact_{Fire,Ice,Water,Air,Earth,Lightning,Light,Dark,Arcane,Poison,Nature}_01/02`, `GrPower_Impact_*`, `GrMedium_Impact_01–11` | 11 elementli vuruş paketi | **Bulunamadı** | — |
| `EGA_EffectSound` | Bilinmiyor | **Bulunamadı** | — |
| `fx2_00066–00102` (37 karelik patlama dizisi), `MagicCircle62`, `Flare23` | Bilinmiyor | — | — |

## Diğer hazır paketler (efekt dışı)
Magica Cloth 2 (kumaş), Damage Numbers Pro (hasar sayıları), Toony Colors Pro 2 (toon shader), Stylized Water 2,
Lux URP Essentials (çim/rüzgâr), Mesh Combine Studio, Advanced Culling System, Bakery, DOTween Pro, Odin (Sirenix),
SRDebugger, Advanced FPS Counter, FIMSpace (FSpine), Amazing Assets TerrainToMesh, UModeler, Beebyte Obfuscator.

## Not
Kayıtlardaki skill efektlerinin (Efekt 7–10 vb.) hangi paketten geldiği APK'dan kesinleştirilemedi; bu efektler şifreli oyun
paketlerinde. Polygon Arsenal / Hovl Studio / Master Magic FX demo videolarıyla gözle karşılaştırma bir sonraki adım olabilir.
