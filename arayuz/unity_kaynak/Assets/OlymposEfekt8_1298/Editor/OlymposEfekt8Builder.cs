// OLYMPOS-KO · 1298 efekt 8 (yalniz skill efekti) — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 8 (Skill Efekti) Oluştur
// Olculer: kayitta mob 422 px; kare 1343 x 948 -> genislik 3.1825 x mob boyu, yuk./gen. 0.7059, pivot (mobun zemini) (0.6016, 0.1909).
using System.IO;
using System.Linq;
using Olympos.Efekt8;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt8.EditorTools
{
    public static class OlymposEfekt8Builder
    {
        const string Klasor = "OlymposEfekt8_1298";

        [MenuItem("OLYMPOS/1298/Efekt 8 (Skill Efekti) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt8 Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt8 Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/Efekt8_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt8");
            var ef = kok.AddComponent<OlymposEfekt8>();
            var hd = new GameObject("Mob (deneme: mobu buraya koyun)"); hd.transform.SetParent(kok.transform, false);
            ef.hedefDeneme = hd.transform; ef.denemeDongusu = true;
            foreach (var tur in new[] { "arka", "on" })
            {
                var go = new GameObject(tur == "arka" ? "Arka Katman (mobun arkasi)" : "On Katman (mobun onu)", typeof(MeshFilter), typeof(MeshRenderer));
                go.transform.SetParent(kok.transform, false);
                var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
                mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
                var k = go.AddComponent<OlymposEfekt8Katman>();
                k.kareler = Kareler(root + "/Textures/skill_" + tur);
                k.genislikHedef = 3.1825f; k.enBoy = 0.7059f; k.pivot = new Vector2(0.6016f, 0.1909f);
                k.derinlik = tur == "arka" ? 0.6f : -0.6f; k.MeshKur();
                if (tur == "arka") ef.arka = k; else ef.on = k;
            }
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt8.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Efekt 8");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Efekt 8 oluşturuldu.");
        }

        static Texture2D[] Kareler(string dir)
        {
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar)
            {
                var ti = AssetImporter.GetAtPath(p) as TextureImporter; if (ti == null) continue;
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = false; ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Bilinear; ti.npotScale = TextureImporterNPOTScale.None;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 2048; ti.SaveAndReimport();
            }
            AssetDatabase.Refresh();
            return yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposEfekt8Builder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
