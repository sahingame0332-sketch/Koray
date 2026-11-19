// OLYMPOS-KO · 1298 efekt 10 pembe patlama — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 10 Pembe Patlama (Çekirdek · Yıldız) Oluştur
using System.IO;
using System.Linq;
using Olympos.Efekt10Patlama;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt10Patlama.EditorTools
{
    public static class OlymposEfekt10PatlamaBuilder
    {
        const string Klasor = "OlymposEfekt10Patlama1298";

        [MenuItem("OLYMPOS/1298/Efekt 10 Pembe Patlama (Çekirdek · Yıldız) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt10 Patlama Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt10 Patlama Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/OlymposEfekt10Patlama_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt10Patlama");
            var ef = kok.AddComponent<OlymposEfekt10Patlama>();
            var nk = new GameObject("Nokta (deneme: mobun merkezi)"); nk.transform.SetParent(kok.transform, false);
            ef.denemeNokta = nk.transform; ef.denemeDongusu = true;
            var go = new GameObject("Katman", typeof(MeshFilter), typeof(MeshRenderer)); go.transform.SetParent(kok.transform, false);
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var k = go.AddComponent<OlymposEfekt10PatlamaKatman>();
            k.kareler = Kareler(root + "/Textures/patlama");
            k.fps = 60f; k.genislikHedef = 7.0f; k.enBoy = 0.56f; k.pivot = new Vector2(0.5f, 0.5f); k.derinlik = -0.3f; k.MeshKur();
            ef.katman = k;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt10Patlama.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "OlymposEfekt10Patlama");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] OlymposEfekt10Patlama oluşturuldu.");
        }

        static Texture2D[] Kareler(string dir)
        {
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar)
            {
                var ti = AssetImporter.GetAtPath(p) as TextureImporter; if (ti == null) continue;
                ti.textureType = TextureImporterType.Default; ti.alphaIsTransparency = false; ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp; ti.filterMode = FilterMode.Bilinear; ti.npotScale = TextureImporterNPOTScale.None;
                ti.textureCompression = TextureImporterCompression.Uncompressed; ti.maxTextureSize = 1024; ti.SaveAndReimport();
            }
            AssetDatabase.Refresh();
            return yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposEfekt10PatlamaBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
