// OLYMPOS-KO · 1298 efekt 9 altin — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 9 Altın Patlama (Karakterde) Oluştur
using System.IO;
using System.Linq;
using Olympos.Efekt9Altin;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt9Altin.EditorTools
{
    public static class OlymposEfekt9AltinBuilder
    {
        const string Klasor = "OlymposEfekt9Altin1298";

        [MenuItem("OLYMPOS/1298/Efekt 9 Altın Patlama (Karakterde) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt9 Altin Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt9 Altin Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/OlymposEfekt9Altin_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt9Altin");
            var ef = kok.AddComponent<OlymposEfekt9Altin>();
            var nk = new GameObject("Nokta (deneme: karakter buraya)"); nk.transform.SetParent(kok.transform, false);
            ef.denemeNokta = nk.transform; ef.denemeDongusu = true;
            var go = new GameObject("Katman", typeof(MeshFilter), typeof(MeshRenderer)); go.transform.SetParent(kok.transform, false);
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var k = go.AddComponent<OlymposEfekt9AltinKatman>();
            k.kareler = Kareler(root + "/Textures/altin");
            k.genislikHedef = 2.1222f; k.enBoy = 0.8115f; k.pivot = new Vector2(0.5148f, 0.0731f); k.derinlik = -0.3f; k.MeshKur();
            ef.katman = k;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt9Altin.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "OlymposEfekt9Altin");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] OlymposEfekt9Altin oluşturuldu.");
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
            var g = AssetDatabase.FindAssets("OlymposEfekt9AltinBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
