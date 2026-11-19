// OLYMPOS-KO — Efekt renk değiştirici (Unity editör aracı)
// Kullanım: Project penceresinde bir efekt prefab'ı seçin (ör. FX_Pink_Hit) →
//   menü: OLYMPOS > Efekt > Seçili Efektin Sarı Kopyasını Oluştur
// Yapılan: prefab'ın "_Sari" adlı bir KOPYASI ve kullandığı materyallerin kopyaları oluşturulur (orijinaller değişmez).
// Her ParticleSystem'de Start Color, Color over Lifetime ve materyal _TintColor/_Color renklerinin TONU (hue) hedef tona çevrilir;
// doygunluk (saturation), parlaklık (value) ve saydamlık (alpha) korunur → efekt aynı kalır, yalnız rengi sarı olur.
// Hedef tonu menüdeki "Ton Ayarı" penceresinden değiştirebilirsiniz (0.13 ≈ altın sarısı, 0.16 ≈ limon sarısı).
using System.IO;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace Olympos.FxRenk.EditorTools
{
    public class OlymposFxRenkDegistir : EditorWindow
    {
        static float hedefTon = 0.13f;          // 0-1 (0.13 ≈ 47°, altın sarısı)
        static float doygunlukCarpani = 1.0f;   // 1 = aynen; >1 daha canlı
        static string ek = "_Sari";

        [MenuItem("OLYMPOS/Efekt/Ton Ayarı (Renk Değiştirici)")]
        static void Ac() { GetWindow<OlymposFxRenkDegistir>("Efekt Rengi"); }

        void OnGUI()
        {
            hedefTon = EditorGUILayout.Slider("Hedef ton (0-1)", hedefTon, 0f, 1f);
            EditorGUILayout.ColorField("Önizleme", Color.HSVToRGB(hedefTon, 0.8f, 1f));
            doygunlukCarpani = EditorGUILayout.Slider("Doygunluk çarpanı", doygunlukCarpani, 0f, 2f);
            ek = EditorGUILayout.TextField("Kopya adı eki", ek);
            if (GUILayout.Button("Seçili efektin kopyasını oluştur")) KopyaOlustur();
        }

        [MenuItem("OLYMPOS/Efekt/Seçili Efektin Sarı Kopyasını Oluştur")]
        static void KopyaOlustur()
        {
            var kaynak = Selection.activeObject as GameObject;
            string yol = kaynak ? AssetDatabase.GetAssetPath(kaynak) : null;
            if (string.IsNullOrEmpty(yol) || !yol.EndsWith(".prefab"))
            {
                EditorUtility.DisplayDialog("Efekt Rengi", "Project penceresinde bir efekt prefab'ı seçin.", "Tamam");
                return;
            }
            string klasor = Path.GetDirectoryName(yol).Replace('\\', '/');
            string yeniYol = AssetDatabase.GenerateUniqueAssetPath(klasor + "/" + Path.GetFileNameWithoutExtension(yol) + ek + ".prefab");
            AssetDatabase.CopyAsset(yol, yeniYol);
            var kok = PrefabUtility.LoadPrefabContents(yeniYol);
            string matKlasor = klasor + "/" + Path.GetFileNameWithoutExtension(yeniYol) + "_Materyaller";
            if (!AssetDatabase.IsValidFolder(matKlasor)) AssetDatabase.CreateFolder(klasor, Path.GetFileName(matKlasor));
            var matKopya = new Dictionary<Material, Material>();

            foreach (var ps in kok.GetComponentsInChildren<ParticleSystem>(true))
            {
                var main = ps.main;
                main.startColor = Cevir(main.startColor);
                var col = ps.colorOverLifetime;
                if (col.enabled) col.color = Cevir(col.color);

                var r = ps.GetComponent<ParticleSystemRenderer>();
                if (r == null) continue;
                var mats = r.sharedMaterials;
                for (int i = 0; i < mats.Length; i++)
                {
                    var m = mats[i];
                    if (m == null) continue;
                    if (!matKopya.TryGetValue(m, out var k))
                    {
                        k = new Material(m) { name = m.name + ek };
                        foreach (var ad in new[] { "_TintColor", "_Color", "_BaseColor" })
                            if (k.HasProperty(ad)) k.SetColor(ad, RenkCevir(k.GetColor(ad)));
                        AssetDatabase.CreateAsset(k, AssetDatabase.GenerateUniqueAssetPath(matKlasor + "/" + k.name + ".mat"));
                        matKopya[m] = k;
                    }
                    mats[i] = k;
                }
                r.sharedMaterials = mats;
            }
            PrefabUtility.SaveAsPrefabAsset(kok, yeniYol);
            PrefabUtility.UnloadPrefabContents(kok);
            AssetDatabase.SaveAssets();
            Selection.activeObject = AssetDatabase.LoadAssetAtPath<GameObject>(yeniYol);
            Debug.Log("Efekt Rengi: oluşturuldu → " + yeniYol + " (" + matKopya.Count + " materyal kopyalandı)");
        }

        static Color RenkCevir(Color c)
        {
            Color.RGBToHSV(c, out float h, out float s, out float v);
            if (s < 0.04f) return c;                         // beyaz/gri: ton yok, aynen kalır
            float yuksek = Mathf.Max(c.r, Mathf.Max(c.g, c.b));  // HDR renk: parlaklığı koru
            var y = Color.HSVToRGB(hedefTon, Mathf.Clamp01(s * doygunlukCarpani), Mathf.Min(v, 1f), false);
            if (yuksek > 1f) y *= yuksek;
            y.a = c.a;
            return y;
        }

        static Gradient GradyanCevir(Gradient g)
        {
            if (g == null) return null;
            var ck = g.colorKeys;
            for (int i = 0; i < ck.Length; i++) ck[i].color = RenkCevir(ck[i].color);
            var y = new Gradient { mode = g.mode };
            y.SetKeys(ck, g.alphaKeys);
            return y;
        }

        static ParticleSystem.MinMaxGradient Cevir(ParticleSystem.MinMaxGradient m)
        {
            switch (m.mode)
            {
                case ParticleSystemGradientMode.Color: return new ParticleSystem.MinMaxGradient(RenkCevir(m.color));
                case ParticleSystemGradientMode.TwoColors: return new ParticleSystem.MinMaxGradient(RenkCevir(m.colorMin), RenkCevir(m.colorMax));
                case ParticleSystemGradientMode.Gradient: return new ParticleSystem.MinMaxGradient(GradyanCevir(m.gradient));
                case ParticleSystemGradientMode.TwoGradients: return new ParticleSystem.MinMaxGradient(GradyanCevir(m.gradientMin), GradyanCevir(m.gradientMax));
                case ParticleSystemGradientMode.RandomColor:
                    var r = new ParticleSystem.MinMaxGradient(GradyanCevir(m.gradient)); r.mode = ParticleSystemGradientMode.RandomColor; return r;
            }
            return m;
        }
    }
}
