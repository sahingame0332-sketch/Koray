#if UNITY_EDITOR
using System.Collections.Generic;
using System.IO;
using Koray.Model;
using UnityEditor;
using UnityEngine;

namespace Koray.EditorTools
{
    /// <summary>
    /// skills.json -> SkillDefinition asset'leri.
    ///
    /// NEDEN GEREKLI
    ///   Oyun JSON ile calisir (SkillDatabase), yani bu adim ZORUNLU DEGIL.
    ///   Asset'lere yalnizca beceriye ikon / VFX prefab'i / ses baglamak
    ///   istedigin an ihtiyac duyarsin -- bunlar Unity referansi gerektirir
    ///   ve JSON'da tutulamaz.
    ///
    /// KORUMA
    ///   Yeniden uretim yalnizca sayisal veriyi (SkillData) gunceller.
    ///   Elle bagladigin Icon / CastVfx / ImpactVfx / CastSound alanlarina
    ///   DOKUNMAZ. Yani iceriği yeniden uretmek sanat baglantilarini silmez.
    ///
    /// Menu: Tools > Koray > Skill Asset'lerini Uret
    /// </summary>
    public static class SkillImporter
    {
        private const string JsonPath   = "Assets/Resources/GameData/skills.json";
        private const string OutputDir  = "Assets/GameData/Skills";

        [MenuItem("Tools/Koray/Skill Asset'lerini Üret")]
        public static void GenerateAssets()
        {
            if (!File.Exists(JsonPath))
            {
                EditorUtility.DisplayDialog(
                    "Skill verisi bulunamadı",
                    JsonPath + " yok.\n\nÖnce üret:\n  python3 tools/generate_content.py",
                    "Tamam");
                return;
            }

            string json = File.ReadAllText(JsonPath);
            SkillCatalogJson catalog = JsonUtility.FromJson<SkillCatalogJson>(json);

            if (catalog == null || catalog.skills == null || catalog.skills.Length == 0)
            {
                EditorUtility.DisplayDialog("Hata",
                    "skills.json ayrıştırılamadı veya boş.", "Tamam");
                return;
            }

            if (!Directory.Exists(OutputDir))
                Directory.CreateDirectory(OutputDir);

            int created = 0, updated = 0;

            try
            {
                AssetDatabase.StartAssetEditing();

                for (int i = 0; i < catalog.skills.Length; i++)
                {
                    SkillData data = catalog.skills[i];
                    if (data == null || string.IsNullOrEmpty(data.code))
                        continue;

                    EditorUtility.DisplayProgressBar(
                        "Skill asset'leri üretiliyor",
                        data.displayName,
                        (float)i / catalog.skills.Length);

                    // Sinif basina alt klasor -- 40 asset tek klasorde karisir
                    string classDir = Path.Combine(OutputDir, data.className);
                    if (!Directory.Exists(classDir))
                        Directory.CreateDirectory(classDir);

                    string assetPath = Path.Combine(classDir, data.code + ".asset")
                        .Replace('\\', '/');

                    SkillDefinition def =
                        AssetDatabase.LoadAssetAtPath<SkillDefinition>(assetPath);

                    if (def == null)
                    {
                        def = ScriptableObject.CreateInstance<SkillDefinition>();
                        def.ApplyData(data);
                        AssetDatabase.CreateAsset(def, assetPath);
                        created++;
                    }
                    else
                    {
                        // Yalnizca veriyi guncelle; Icon/VFX/Sound korunur
                        def.ApplyData(data);
                        EditorUtility.SetDirty(def);
                        updated++;
                    }
                }
            }
            finally
            {
                AssetDatabase.StopAssetEditing();
                EditorUtility.ClearProgressBar();
                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();
            }

            // Veri tutarliligini da kontrol et
            SkillDatabase.LoadFromJson(json);
            List<string> problems = SkillDatabase.Validate();

            string message = string.Format(
                "{0} asset oluşturuldu, {1} asset güncellendi.\n" +
                "Toplam {2} beceri, {3} rank.\n\n{4}",
                created, updated, catalog.skillCount, catalog.rankCount,
                problems.Count == 0
                    ? "Doğrulama: sorun yok."
                    : "Doğrulama: " + problems.Count + " sorun (Console'a yazıldı).");

            foreach (string p in problems)
                Debug.LogWarning("Skill doğrulama: " + p);

            Debug.Log("SkillImporter: " + message.Replace("\n", " "));
            EditorUtility.DisplayDialog("Skill asset'leri", message, "Tamam");
        }

        [MenuItem("Tools/Koray/Skill Verisini Doğrula")]
        public static void ValidateOnly()
        {
            if (!File.Exists(JsonPath))
            {
                Debug.LogError("SkillImporter: " + JsonPath + " yok.");
                return;
            }

            SkillDatabase.LoadFromJson(File.ReadAllText(JsonPath));
            List<string> problems = SkillDatabase.Validate();

            if (problems.Count == 0)
            {
                Debug.Log(string.Format(
                    "Skill doğrulama: sorun yok. {0} beceri yüklendi (şema v{1}).",
                    SkillDatabase.Count, SkillDatabase.SchemaVersion));
                return;
            }

            foreach (string p in problems)
                Debug.LogWarning("Skill doğrulama: " + p);

            Debug.LogError("Skill doğrulama: " + problems.Count + " sorun bulundu.");
        }
    }
}
#endif
