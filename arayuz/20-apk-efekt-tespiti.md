# APK içindeki vuruş / skill efektleri — tespit (18 Kasım 2026)

İncelenen: `MykoMobileOnline1.1.apk` (resmî adres, MD5 `492d138e2fa646c25c1a1937a1799db5`), `assets/bin/Data` UnityPy ile okundu.
Çıkarılan dokular depoya **konmadı** (yalnız küçük önizleme tablosu: `onizlemeler/apk_efekt_dokulari.jpg`).

## Sayımlar
ParticleSystem 583 · Texture2D 956 · Material 128 · Shader 110 · AnimationClip 232 · Mesh 46.

## Vuruş efekti prefab'ları (ParticleSystem kökleri, alt sistem sayısıyla)
- `Power_Impact_{Fire,Ice,Water,Air,Earth,Lightning,Light,Dark,Arcane,Poison,Nature}_01/02` (6–8 alt sistem)
- `GrPower_Impact_*_01/02` — aynı elementlerin yerde (ground) sürümü (8–10)
- `GrMedium_Impact_01 … 11` (6)
- `Hit_bow_low` (ok vuruşu, 6), `Sparks`, `Flare`, `Glow`, `Genie FX`, `QuestFx_Avaiable`, `QuestFx_Complate 1`, `create_fx`, `clanaddon_fx`
Adlandırma ticari bir Unity Asset Store efekt paketinin düzenine benziyor; betiklerde de hazır paket izleri var
(`HS_ParticleCollisionInstance`, `EGA_EffectSound`, `AllIn1Vfx*`, `MagicaCloth`, `TCP2` = Toony Colors Pro 2).

## Efekt dokuları
`fx2_00066 … 00102` (37 karelik patlama dizisi: turuncu çekirdek → mavi enerji → söner), `fx1_00066`,
`Glow`, `Glow4`, `Glow7`, `0_glow_001751`, `Flare23`, `RingGlow`, `MagicCircle62`, `Skill-Glow`, `polySpriteGlow`, `buff_hit_rdc`.

## Karakter skill animasyonları (beden hareketi, efekt değil)
`skill_sword01_A/B`, `skill_sword02_B`, `skill_twoH_sword_B`, `skill_axe01_B`, `skill_axe02_A`, `skill_dual_A`, `skill_spear_A`,
`magic_attack`, `magic_call`, `magic_heal`, `magic_ability`, `magic_spec_attack`, `magic_anim1-5`.
Skill akışını yöneten betikler: `SkillController`, `AreaSkillController`, `CastingFXBehaviour`, `WeaponFXBehaviour`, `MonsterFxBehaviour`.

## Bulunamayanlar
Kayıtlardaki skill efektleri (Efekt 7–10 pembe patlama, sarı yıldız, kesikler, Manes Of Fire…) APK'da **yok**.
Oyun içeriği AssetBundle olarak oyun açılınca indiriliyor (`NewBundleLoader`, geliştirici yolu `D:\ko1patches\effects`).
İndirme adresi çalışma anında kuruluyor; tahmin edilen yollar 404. Bu paketler telefondaki oyun klasöründen
(`Android/data/<paket>/…`) alınırsa aynı yöntemle okunabilir.
