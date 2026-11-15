// OLYMPOS-KO · 1298 kendi skill efektleri — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Kendi Skill Efektleri (Hide · Light Feet · Eyes · Evade · Safety · Cure · Magic Shield) Oluştur
// (+ Sprint, Swift, Strength Of Wolf, Minor Healing — ikinci kayit seti)
// Olculer: arayuz/10-efekt.md (ek 5).
using System.IO;
using System.Linq;
using Olympos.KendiSkill;
using UnityEditor;
using UnityEngine;

namespace Olympos.KendiSkill.EditorTools
{
    public static class OlymposKendiSkillBuilder
    {
        const string Klasor = "OlymposKendiSkill1298";
        // klasor, gorunen ad, skill adlari (Information panelindeki gibi)
        static readonly string[][] EFEKTLER = {
            new[] { "dokum_yildizlari", "Dokum Yildizlari", "" },
            new[] { "hide", "Hide", "Hide" },
            new[] { "light_feet", "Light Feet", "Light Feet" },
            new[] { "kedi_gozu", "Cat's / Lupine Eyes", "Cat's Eyes|Lupine Eyes" },
            new[] { "evade", "Evade", "Evade" },
            new[] { "safety", "Safety", "Safety" },
            new[] { "cure", "Cure Disease / Curse", "Cure Disease|Cure Curse" },
            new[] { "magic_shield", "Magic Shield", "Magic Shield" },
            new[] { "sprint", "Sprint", "Sprint" },
            new[] { "swift", "Swift", "Swift" },
            new[] { "strength_of_wolf", "Strength Of Wolf", "Strength Of Wolf" },
            new[] { "minor_healing", "Minor Healing", "Minor Healing" } };

        [MenuItem("OLYMPOS/1298/Kendi Skill Efektleri (Hide · Light Feet · Eyes · Evade · Safety · Cure · Magic Shield) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Kendi Skill Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Kendi Skill Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var mat = AssetDatabase.LoadAssetAtPath<Material>(md + "/KendiSkill_Eklemeli.mat");
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, md + "/KendiSkill_Eklemeli.mat"); }

            var kok = new GameObject("OlymposKendiSkillEfektleri");
            var kut = kok.AddComponent<OlymposKendiSkillKutuphanesi>();
            float x = -6f;
            foreach (var e in EFEKTLER)
            {
                var go = new GameObject(e[1], typeof(MeshFilter), typeof(MeshRenderer));
                go.transform.SetParent(kok.transform, false); go.transform.localPosition = new Vector3(x, 0, 0); x += 1.8f;
                var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
                mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
                var o = go.AddComponent<OlymposKendiSkillEfekti>();
                o.skillAdi = e[1]; o.kareler = Kareler(root + "/Textures/" + e[0]);
                o.dongu = true; o.baslangictaOyna = true; o.bitinceGizle = false;      // denemede surekli; oyunda Oyna(...)
                if (e[2] == "") kut.dokumYildizlari = o;
                else foreach (var ad in e[2].Split('|')) kut.skiller.Add(new OlymposKendiSkillKutuphanesi.Kayit { skill = ad, efekt = o });
            }
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposKendiSkillEfektleri.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Kendi skill efektleri");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Kendi skill efektleri oluşturuldu (" + EFEKTLER.Length + " efekt).");
        }

        static Texture2D[] Kareler(string dir)
        {
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar)
            {
                var ti = AssetImporter.GetAtPath(p) as TextureImporter; if (ti == null) continue;
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = false; ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            AssetDatabase.Refresh();
            return yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposKendiSkillBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
