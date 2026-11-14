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
