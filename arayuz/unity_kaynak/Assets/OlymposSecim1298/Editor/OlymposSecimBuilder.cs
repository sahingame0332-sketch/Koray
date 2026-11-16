// OLYMPOS-KO · 1298 secim efektleri — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Seçim Halkası + Yön Oku Oluştur
using System.IO;
using Olympos.Secim;
using UnityEditor;
using UnityEngine;

namespace Olympos.Secim.EditorTools
{
    public static class OlymposSecimBuilder
    {
        const string Klasor = "OlymposSecim1298";

        [MenuItem("OLYMPOS/1298/Seçim Halkası + Yön Oku Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Secim Zemin");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Secim Zemin"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var mHalka = Malzeme(md + "/SecimHalkasi.mat", sh, Doku(root + "/Textures/secim_halkasi.png"));
            var mOk = Malzeme(md + "/YonOku.mat", sh, Doku(root + "/Textures/yon_oku.png"));

            var kok = new GameObject("OlymposSecim");
            var yon = kok.AddComponent<OlymposSecimYoneticisi>();
            // deneme: karakter (kapsul) ve hedef (kure) yer tutuculari
            var kar = new GameObject("Karakter (deneme)"); kar.transform.SetParent(kok.transform, false);
            var hed = new GameObject("Hedef (deneme)"); hed.transform.SetParent(kok.transform, false); hed.transform.localPosition = new Vector3(-0.6f, 0, -1.4f);

            var h = new GameObject("Secim Halkasi", typeof(MeshFilter), typeof(MeshRenderer)); h.transform.SetParent(kok.transform, false);
            Ayarla(h, mHalka); yon.halka = h.AddComponent<OlymposSecimHalkasi>();
            var o = new GameObject("Yon Oku", typeof(MeshFilter), typeof(MeshRenderer)); o.transform.SetParent(kok.transform, false);
            Ayarla(o, mOk); yon.ok = o.AddComponent<OlymposYonOku>();
            yon.denemeKarakter = kar.transform; yon.denemeHedef = hed.transform;

            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposSecim.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Secim efektleri");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Seçim halkası + yön oku oluşturuldu.");
        }

        static void Ayarla(GameObject g, Material m)
        {
            var r = g.GetComponent<MeshRenderer>(); r.sharedMaterial = m;
            r.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; r.receiveShadows = false;
        }

        static Material Malzeme(string p, Shader sh, Texture2D t)
        {
            var mat = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, p); }
            mat.mainTexture = t; EditorUtility.SetDirty(mat);
            return mat;
        }

        static Texture2D Doku(string p)
        {
            var ti = AssetImporter.GetAtPath(p) as TextureImporter;
            if (ti != null)
            {
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = false;   // on-carpimli: renk tasmasi yapma
                ti.mipmapEnabled = true; ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Trilinear;
                ti.npotScale = TextureImporterNPOTScale.None; ti.sRGBTexture = true;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(p);
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposSecimBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
