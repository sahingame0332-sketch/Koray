// OLYMPOS-KO · 1298 karakter alti ates havuzu — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Ateş Havuzu (Karakter Altı) Oluştur.  Olculer: arayuz/10-efekt.md (ek 3).
using System.IO;
using System.Linq;
using Olympos.AtesHavuzu;
using UnityEditor;
using UnityEngine;

namespace Olympos.AtesHavuzu.EditorTools
{
    public static class OlymposAtesHavuzuBuilder
    {
        const string Klasor = "OlymposAtesHavuzu1298";
        static string Root;

        [MenuItem("OLYMPOS/1298/Ateş Havuzu (Karakter Altı) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            string dir = Root + "/Textures/AtesHavuzu";
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

            var shader = Shader.Find("Olympos/Ates Havuzu Eklemeli");
            if (shader == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Ates Havuzu Eklemeli"); return; }
            string md = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(Root, "Materials");
            var mat = AssetDatabase.LoadAssetAtPath<Material>(md + "/AtesHavuzu.mat");
            if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, md + "/AtesHavuzu.mat"); }

            var go = new GameObject("AtesHavuzu (karakter alti)", typeof(MeshFilter), typeof(MeshRenderer));
            var mr = go.GetComponent<MeshRenderer>();
            mr.sharedMaterial = mat; mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var o = go.AddComponent<OlymposAtesHavuzuOynatici>();
            o.kareler = kareler; o.fps = 30f; o.genislikKarakter = 3.73f; o.enBoy = 0.75f; o.pivot = new Vector2(0.464f, 0.40f);
            o.bitinceGizle = false; o.dongu = true;          // denemede surekli; oyunda dongu kapali, Hedefte(...) ile
            string pd = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(Root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/AtesHavuzu.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(go, "Ates havuzu");
            Selection.activeGameObject = go;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Ateş havuzu oluşturuldu (" + kareler.Length + " kare).");
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposAtesHavuzuBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
