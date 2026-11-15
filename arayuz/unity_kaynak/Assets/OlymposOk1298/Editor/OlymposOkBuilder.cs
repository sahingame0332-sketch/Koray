// OLYMPOS-KO · 1298 Shadow Hunter oku — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Ok (Shadow Hunter) Oluştur
// Sahneye: "OlymposOk_ShadowHunter" (OlymposOkAtisi) + vurus sablonu (pasif) + prefab.
using System.IO;
using System.Linq;
using Olympos.Ok;
using UnityEditor;
using UnityEngine;

namespace Olympos.Ok.EditorTools
{
    public static class OlymposOkBuilder
    {
        const string Klasor = "OlymposOk1298";

        [MenuItem("OLYMPOS/1298/Ok (Shadow Hunter) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var okDoku = Doku(root + "/Textures/ok.png", true);
            var dir = root + "/Textures/Vurus";
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            var kareler = yollar.Select(p => Doku(p, false)).ToArray();
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var okMat = Mat(md + "/Ok.mat", "Olympos/Ok"); var vMat = Mat(md + "/OkVurus.mat", "Olympos/Ok Vurus");
            if (okMat == null || vMat == null) return;
            okMat.SetTexture("_MainTex", okDoku); EditorUtility.SetDirty(okMat);

            var kok = new GameObject("OlymposOk_ShadowHunter");
            var vgo = new GameObject("VurusSablonu", typeof(MeshFilter), typeof(MeshRenderer));
            vgo.transform.SetParent(kok.transform, false);
            var vmr = vgo.GetComponent<MeshRenderer>(); vmr.sharedMaterial = vMat;
            vmr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; vmr.receiveShadows = false;
            var vur = vgo.AddComponent<OlymposOkVurusu>(); vur.kareler = kareler;
            vgo.SetActive(false);
            var atis = kok.AddComponent<OlymposOkAtisi>(); atis.okMalzemesi = okMat; atis.vurusSablonu = vur;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposOk_ShadowHunter.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Ok");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Ok (Shadow Hunter) oluşturuldu: atis.At(okcu, hedef) ile kullanin.");
        }

        static Material Mat(string yol, string sh)
        {
            var s = Shader.Find(sh); if (s == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: " + sh); return null; }
            var m = AssetDatabase.LoadAssetAtPath<Material>(yol); if (m == null) { m = new Material(s); AssetDatabase.CreateAsset(m, yol); }
            return m;
        }

        static Texture2D Doku(string p, bool alfa)
        {
            var ti = AssetImporter.GetAtPath(p) as TextureImporter;
            if (ti != null)
            {
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = alfa; ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(p);
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposOkBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
