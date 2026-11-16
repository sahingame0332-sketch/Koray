// OLYMPOS-KO · 1298 efekt 7 karakter kesigi — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Efekt 7 Karakter (Kılıç Kesiği) Oluştur
using System.IO;
using System.Linq;
using Olympos.Efekt7Karakter;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt7Karakter.EditorTools
{
    public static class OlymposEfekt7KarakterBuilder
    {
        const string Klasor = "OlymposEfekt7Karakter1298";

        [MenuItem("OLYMPOS/1298/Efekt 7 Karakter (Kılıç Kesiği) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt7 Karakter Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt7 Karakter Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string mp = md + "/Efekt7Karakter_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfekt7Karakter");
            var kar = new GameObject("Karakter (deneme)"); kar.transform.SetParent(kok.transform, false);
            var hed = new GameObject("Hedef (deneme)"); hed.transform.SetParent(kok.transform, false); hed.transform.localPosition = new Vector3(-1.5f, 0, 0);
            var go = new GameObject("Kilic Kesigi", typeof(MeshFilter), typeof(MeshRenderer)); go.transform.SetParent(kok.transform, false);
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var k = go.AddComponent<OlymposEfekt7KarakterKesik>();
            k.kareler = Kareler(root + "/Textures/karakter_kesik");
            k.karakter = kar.transform; k.hedef = hed.transform; k.denemeDongusu = true;

            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt7Karakter.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Efekt 7 karakter");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Efekt 7 karakter kesiği oluşturuldu.");
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
            var g = AssetDatabase.FindAssets("OlymposEfekt7KarakterBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
