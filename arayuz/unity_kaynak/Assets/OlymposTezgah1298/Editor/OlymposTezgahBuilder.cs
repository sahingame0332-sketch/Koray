// OLYMPOS-KO · 1298 Merchant tezgahi — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Merchant Tezgahı (Yer) Oluştur
using System.IO;
using Olympos.Tezgah;
using UnityEditor;
using UnityEngine;

namespace Olympos.Tezgah.EditorTools
{
    public static class OlymposTezgahBuilder
    {
        const string Klasor = "OlymposTezgah1298";

        [MenuItem("OLYMPOS/1298/Merchant Tezgahı (Yer) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var doku = Doku(root + "/Textures/tezgah.png"); var yan = Doku(root + "/Textures/tezgah_yan.png");
            if (doku == null) return;
            var sh = Shader.Find("Olympos/Tezgah Sprite");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Tezgah Sprite"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var mat = AssetDatabase.LoadAssetAtPath<Material>(md + "/Tezgah.mat");
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, md + "/Tezgah.mat"); }
            mat.SetTexture("_MainTex", doku); EditorUtility.SetDirty(mat);

            var go = new GameObject("MerchantTezgahi", typeof(MeshFilter), typeof(MeshRenderer));
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var t = go.AddComponent<OlymposTezgah>(); t.onDoku = doku; t.yanDoku = yan;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/MerchantTezgahi.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(go, "Merchant tezgahi");
            Selection.activeGameObject = go;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Merchant tezgâhı oluşturuldu.");
        }

        [MenuItem("OLYMPOS/1298/Merchant Tezgahı 3B Oluştur")]
        public static void Build3B()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Tezgah 3B");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Tezgah 3B"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var ust = Malzeme(md + "/Tezgah3B_Ust.mat", sh, Doku(root + "/Textures/3B/ust.png"));
            var on = Malzeme(md + "/Tezgah3B_On.mat", sh, Doku(root + "/Textures/3B/on.png"));
            var yan = Malzeme(md + "/Tezgah3B_Yan.mat", sh, Doku(root + "/Textures/3B/yan.png"));
            var go = new GameObject("MerchantTezgahi3B", typeof(MeshFilter), typeof(MeshRenderer));
            var t = go.AddComponent<OlymposTezgah3B>(); t.Kur();
            go.GetComponent<MeshRenderer>().sharedMaterials = new[] { ust, on, yan, yan, yan };   // ust, on, sol, sag, arka
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            // mesh kurulumda uretilir (Awake); prefab icin de asset olarak kaydet
            var mesh = go.GetComponent<MeshFilter>().sharedMesh; AssetDatabase.CreateAsset(Object.Instantiate(mesh), pd + "/Tezgah3B_Mesh.asset");
            go.GetComponent<MeshFilter>().sharedMesh = AssetDatabase.LoadAssetAtPath<Mesh>(pd + "/Tezgah3B_Mesh.asset");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/MerchantTezgahi3B.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(go, "Merchant tezgahi 3B");
            Selection.activeGameObject = go;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] 3B Merchant tezgâhı oluşturuldu.");
        }

        static Material Malzeme(string yol, Shader sh, Texture2D d)
        {
            var m = AssetDatabase.LoadAssetAtPath<Material>(yol);
            if (m == null) { m = new Material(sh); AssetDatabase.CreateAsset(m, yol); }
            m.SetTexture("_MainTex", d); EditorUtility.SetDirty(m); return m;
        }

        static Texture2D Doku(string p)
        {
            var ti = AssetImporter.GetAtPath(p) as TextureImporter;
            if (ti == null) { Debug.LogError("[OLYMPOS] Doku bulunamadı: " + p); return null; }
            ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = true; ti.mipmapEnabled = true;
            ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Trilinear;
            ti.textureCompression = TextureImporterCompression.Uncompressed; ti.SaveAndReimport();
            return AssetDatabase.LoadAssetAtPath<Texture2D>(p);
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposTezgahBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
