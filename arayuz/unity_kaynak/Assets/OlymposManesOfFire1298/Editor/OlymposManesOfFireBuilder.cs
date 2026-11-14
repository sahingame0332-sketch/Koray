// OLYMPOS-KO · 1298 Manes Of Fire (moba) — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Manes Of Fire (Moba) Oluştur.  Olculer: arayuz/10-efekt.md (ek 4).
using System.IO;
using System.Linq;
using Olympos.ManesOfFire;
using UnityEditor;
using UnityEngine;

namespace Olympos.ManesOfFire.EditorTools
{
    public static class OlymposManesOfFireBuilder
    {
        const string Klasor = "OlymposManesOfFire1298";
        static string Root;

        [MenuItem("OLYMPOS/1298/Manes Of Fire (Moba) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            string dir = Root + "/Textures/ManesOfFire";
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar)
            {
                var ti = AssetImporter.GetAtPath(p) as TextureImporter;
                if (ti == null) continue;
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = false; ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            AssetDatabase.Refresh();
            var kareler = yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();

            var shader = Shader.Find("Olympos/Manes Of Fire Eklemeli");
            if (shader == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Manes Of Fire Eklemeli"); return; }
            string md = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(Root, "Materials");
            var mat = AssetDatabase.LoadAssetAtPath<Material>(md + "/ManesOfFire.mat");
            if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, md + "/ManesOfFire.mat"); }

            var go = new GameObject("ManesOfFire (moba)", typeof(MeshFilter), typeof(MeshRenderer));
            var mr = go.GetComponent<MeshRenderer>();
            mr.sharedMaterial = mat; mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var o = go.AddComponent<OlymposManesOfFireOynatici>();
            o.kareler = kareler; o.fps = 30f; o.genislikKarakter = 3.71f; o.enBoy = 1.808f; o.pivot = new Vector2(0.365f, 0.126f);
            o.bitinceGizle = false; o.dongu = true;          // denemede surekli; oyunda dongu kapali, Hedefte(...) ile
            string pd = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(Root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/ManesOfFire.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(go, "Manes of Fire");
            Selection.activeGameObject = go;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Manes Of Fire oluşturuldu (" + kareler.Length + " kare).");
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposManesOfFireBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
