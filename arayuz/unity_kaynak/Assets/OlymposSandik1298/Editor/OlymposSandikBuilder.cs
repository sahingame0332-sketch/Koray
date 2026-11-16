// OLYMPOS-KO · 1298 sandik — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Sandık (Açık · Kapalı) Oluştur
using System.IO;
using Olympos.Sandik;
using UnityEditor;
using UnityEngine;

namespace Olympos.Sandik.EditorTools
{
    public static class OlymposSandikBuilder
    {
        const string Klasor = "OlymposSandik1298";

        [MenuItem("OLYMPOS/1298/Sandık (Açık · Kapalı) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Sandik 3B"); var sp = Shader.Find("Olympos/Sandik Sprite");
            if (sh == null || sp == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Sandik 3B / Sandik Sprite"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            System.Func<string, Material> M = ad => Malzeme(md + "/Sandik_" + ad + ".mat", sh, Doku(root + "/Textures/3B/" + ad + ".png", false));

            var kok = new GameObject("OlymposSandik");
            var kapali = new GameObject("Sandik (kapali)"); kapali.transform.SetParent(kok.transform, false); kapali.transform.localPosition = new Vector3(-0.5f, 0, 0);
            var acik = new GameObject("Sandik (acik)"); acik.transform.SetParent(kok.transform, false); acik.transform.localPosition = new Vector3(0.5f, 0, 0);
            foreach (var go in new[] { kapali, acik })
            {
                var s = go.AddComponent<OlymposSandik>();
                s.govdeMalzemeleri = new[] { M("on"), M("arka"), M("uc"), M("ust_acik") };
                s.kapakMalzemeleri = new[] { M("kapak"), M("kapak_ic"), M("uc") };
                s.baslangic = go == acik ? OlymposSandik.Durum.Acik : OlymposSandik.Durum.Kapali;
                s.Kur();
            }
            var iki = new GameObject("Sandik 2B", typeof(MeshFilter), typeof(MeshRenderer)); iki.transform.SetParent(kok.transform, false); iki.transform.localPosition = new Vector3(1.5f, 0, 0);
            var s2 = iki.AddComponent<OlymposSandik2B>();
            s2.kapali = Doku(root + "/Textures/2B/sandik_kapali.png", true); s2.acik = Doku(root + "/Textures/2B/sandik_acik.png", true);
            var r2 = iki.GetComponent<MeshRenderer>(); r2.sharedMaterial = Malzeme(md + "/Sandik_2B.mat", sp, s2.kapali);
            r2.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; r2.receiveShadows = false;

            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposSandik.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Sandik");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Sandık (kapalı + açık + 2B) oluşturuldu.");
        }

        static Material Malzeme(string p, Shader sh, Texture2D t)
        {
            var mat = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, p); }
            mat.mainTexture = t; EditorUtility.SetDirty(mat); return mat;
        }

        static Texture2D Doku(string p, bool alfa)
        {
            var ti = AssetImporter.GetAtPath(p) as TextureImporter;
            if (ti != null)
            {
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = alfa; ti.mipmapEnabled = true;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Trilinear; ti.npotScale = TextureImporterNPOTScale.None;
                ti.sRGBTexture = true; ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(p);
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposSandikBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
