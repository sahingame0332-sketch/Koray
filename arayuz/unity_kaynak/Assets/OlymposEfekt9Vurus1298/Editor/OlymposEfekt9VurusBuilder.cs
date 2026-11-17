// OLYMPOS-KO · 1298 efekt 9 vurus — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 9 Vuruş (Mobda: Patlama · Işın · Halka · Yıldız) Oluştur
using System.IO;
using System.Linq;
using Olympos.Efekt9Vurus;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt9Vurus.EditorTools
{
    public static class OlymposEfekt9VurusBuilder
    {
        const string Klasor = "OlymposEfekt9Vurus1298";

        [MenuItem("OLYMPOS/1298/Efekt 9 Vuruş (Mobda: Patlama · Işın · Halka · Yıldız) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt9 Vurus Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt9 Vurus Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/OlymposEfekt9Vurus_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt9Vurus");
            var ef = kok.AddComponent<OlymposEfekt9Vurus>();
            var nk = new GameObject("Nokta (deneme: mob buraya)"); nk.transform.SetParent(kok.transform, false);
            ef.denemeNokta = nk.transform; ef.denemeDongusu = true;
            var go = new GameObject("Katman", typeof(MeshFilter), typeof(MeshRenderer)); go.transform.SetParent(kok.transform, false);
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var k = go.AddComponent<OlymposEfekt9VurusKatman>();
            k.kareler = Kareler(root + "/Textures/vurus");
            k.genislikHedef = 4.5037f; k.enBoy = 0.6686f; k.pivot = new Vector2(0.4293f, 0.1734f); k.derinlik = 0.0f; k.MeshKur();
            ef.katman = k;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt9Vurus.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "OlymposEfekt9Vurus");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] OlymposEfekt9Vurus oluşturuldu.");
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
            var g = AssetDatabase.FindAssets("OlymposEfekt9VurusBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
