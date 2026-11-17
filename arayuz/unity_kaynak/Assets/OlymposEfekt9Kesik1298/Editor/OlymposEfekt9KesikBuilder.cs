// OLYMPOS-KO · 1298 efekt 9 kesik — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 9 Karakter (Kılıç Kesiği) Oluştur
using System.IO;
using System.Linq;
using Olympos.Efekt9Kesik;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt9Kesik.EditorTools
{
    public static class OlymposEfekt9KesikBuilder
    {
        const string Klasor = "OlymposEfekt9Kesik1298";

        [MenuItem("OLYMPOS/1298/Efekt 9 Karakter (Kılıç Kesiği) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt9 Kesik Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt9 Kesik Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/OlymposEfekt9Kesik_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt9Kesik");
            var ef = kok.AddComponent<OlymposEfekt9Kesik>();
            var nk = new GameObject("Nokta (deneme: karakter buraya)"); nk.transform.SetParent(kok.transform, false);
            ef.denemeNokta = nk.transform; ef.denemeDongusu = true;
            var go = new GameObject("Katman", typeof(MeshFilter), typeof(MeshRenderer)); go.transform.SetParent(kok.transform, false);
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var k = go.AddComponent<OlymposEfekt9KesikKatman>();
            k.kareler = Kareler(root + "/Textures/kesik");
            k.genislikHedef = 2.6481f; k.enBoy = 0.6322f; k.pivot = new Vector2(0.414f, -0.1305f); k.derinlik = -0.3f; k.MeshKur();
            ef.katman = k;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt9Kesik.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "OlymposEfekt9Kesik");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] OlymposEfekt9Kesik oluşturuldu.");
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
            var g = AssetDatabase.FindAssets("OlymposEfekt9KesikBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
