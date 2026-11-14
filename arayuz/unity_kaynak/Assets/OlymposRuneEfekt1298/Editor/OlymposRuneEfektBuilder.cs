// OLYMPOS-KO · alevli run halkasi — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Alevli Run Halkası Oluştur
using System.IO;
using Olympos.RuneEfekt;
using UnityEditor;
using UnityEngine;

namespace Olympos.RuneEfekt.EditorTools
{
    public static class OlymposRuneEfektBuilder
    {
        const string Klasor = "OlymposRuneEfekt1298";
        static string Root;

        [MenuItem("OLYMPOS/1298/Alevli Run Halkası Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            var cizgi = Tex("rune_cizgi", TextureWrapMode.Clamp);
            var gur = Tex("rune_gurultu", TextureWrapMode.Repeat);
            string md = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(Root, "Materials");
            var hm = Mat(md + "/RuneAtesHalkasi.mat", "Olympos/Rune Ates Halkasi"); if (hm == null) return;
            var dm = Mat(md + "/RuneAlevDuvari.mat", "Olympos/Rune Alev Duvari"); if (dm == null) return;
            hm.SetTexture("_Cizgi", cizgi); hm.SetTexture("_Gurultu", gur); dm.SetTexture("_Gurultu", gur);
            EditorUtility.SetDirty(hm); EditorUtility.SetDirty(dm);

            var go = new GameObject("AlevliRunHalkasi");
            var e = go.AddComponent<OlymposRuneEfekti>();
            e.halkaMalzemesi = hm; e.duvarMalzemesi = dm; e.dongu = true;      // denemede surekli; oyunda Oyna(...) ile
            string pd = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(Root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/AlevliRunHalkasi.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(go, "Alevli run halkasi");
            Selection.activeGameObject = go;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Alevli run halkası oluşturuldu.");
        }

        static Material Mat(string yol, string shaderAdi)
        {
            var sh = Shader.Find(shaderAdi);
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: " + shaderAdi); return null; }
            var m = AssetDatabase.LoadAssetAtPath<Material>(yol);
            if (m == null) { m = new Material(sh); AssetDatabase.CreateAsset(m, yol); }
            return m;
        }

        static Texture2D Tex(string ad, TextureWrapMode wrap)
        {
            string p = Root + "/Textures/" + ad + ".png";
            var ti = AssetImporter.GetAtPath(p) as TextureImporter;
            if (ti != null)
            {
                ti.textureType = TextureImporterType.Default; ti.sRGBTexture = false; ti.alphaIsTransparency = false;
                ti.mipmapEnabled = true; ti.wrapMode = wrap; ti.filterMode = FilterMode.Trilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            else Debug.LogError("[OLYMPOS] Doku bulunamadı: " + p);
            return AssetDatabase.LoadAssetAtPath<Texture2D>(p);
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposRuneEfektBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
