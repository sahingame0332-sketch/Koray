// OLYMPOS-KO · 1298 skill efektleri — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Skill Efektleri (Fire Burst · Fire Blade · Vuruş) Oluştur
// Kayit: telefon 2712 x 1220, ~72 kare/sn (2 karede bir -> 36 kare/sn). Olculer depoda arayuz/10-efekt.md (ek 2).
// Karakter boyu kayitta ~180 px; genislikler bu boya gore.
using System.IO;
using System.Linq;
using Olympos.SkillEfekt;
using UnityEditor;
using UnityEngine;

namespace Olympos.SkillEfekt.EditorTools
{
    public static class OlymposSkillEfektBuilder
    {
        const string Klasor = "OlymposSkillEfekt1298";
        static string Root;

        [MenuItem("OLYMPOS/1298/Skill Efektleri (Fire Burst · Fire Blade · Vuruş) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            var burst = Kareler("FireBurst");
            var blade = Kareler("FireBlade");
            var vurus = Kareler("VurusTam");

            var shader = Shader.Find("Olympos/Skill Efekt Eklemeli");
            if (shader == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Skill Efekt Eklemeli"); return; }
            string md = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(Root, "Materials");
            string mp = md + "/SkillEfekt_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposSkillEfektDeneme");
            Undo.RegisterCreatedObjectUndo(kok, "Skill efekt denemesi");
            // Fire Burst: kare 900 x 760; mobun ayagi (secim halkasi merkezi) (430, 575) -> pivot (0.478, 0.243); genislik 5.0 karakter boyu
            var a = Oynatici(kok, "FireBurst (mob)", mat, burst, 5.0f, 0.844f, new Vector2(0.478f, 0.243f), new Vector3(-3f, 0f, 0f));
            // Fire Blade: kare 560 x 820; isinin yere degdigi halka (160, 685) -> pivot (0.286, 0.165); genislik 3.11 karakter boyu
            var b = Oynatici(kok, "FireBlade (mob)", mat, blade, 3.11f, 1.464f, new Vector2(0.286f, 0.165f), new Vector3(0f, 0f, 0f));
            // Karaktere vurus (tam): kare 470 x 430; karakterin ayagi (235, 335) -> pivot (0.50, 0.221); genislik 2.61 karakter boyu
            var v = Oynatici(kok, "Vurus (karaktere, tam)", mat, vurus, 2.61f, 0.915f, new Vector2(0.50f, 0.221f), new Vector3(3f, 0f, 0f));
            a.dongu = b.dongu = v.dongu = true;      // denemede surekli oynasin; oyunda dongu kapali, Hedefte(...) ile tetikleyin

            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Skill efektleri oluşturuldu (Fire Burst " + burst.Length + ", Fire Blade " + blade.Length + ", Vuruş " + vurus.Length + " kare).");
        }

        static OlymposSkillEfektOynatici Oynatici(GameObject kok, string ad, Material mat, Texture2D[] k, float gen, float enBoy, Vector2 pivot, Vector3 konum)
        {
            var go = new GameObject(ad, typeof(MeshFilter), typeof(MeshRenderer));
            go.transform.SetParent(kok.transform, false);
            go.transform.position = konum;
            var mr = go.GetComponent<MeshRenderer>();
            mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            mr.receiveShadows = false;
            var o = go.AddComponent<OlymposSkillEfektOynatici>();
            o.kareler = k; o.genislikKarakter = gen; o.enBoy = enBoy; o.pivot = pivot; o.fps = 36f;
            o.bitinceGizle = false;
            string pd = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(Root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(go, pd + "/" + ad.Split(' ')[0] + ".prefab", InteractionMode.AutomatedAction);
            return o;
        }

        static Texture2D[] Kareler(string alt)
        {
            string dir = Root + "/Textures/" + alt;
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar)
            {
                var ti = AssetImporter.GetAtPath(p) as TextureImporter;
                if (ti == null) { Debug.LogError("[OLYMPOS] Doku bulunamadı: " + p); continue; }
                ti.textureType = TextureImporterType.Default;
                ti.alphaIsTransparency = false;
                ti.mipmapEnabled = false;
                ti.wrapMode = TextureWrapMode.Clamp;
                ti.filterMode = FilterMode.Bilinear;
                ti.textureCompression = TextureImporterCompression.Uncompressed;
                ti.maxTextureSize = 1024;
                ti.SaveAndReimport();
            }
            AssetDatabase.Refresh();
            return yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposSkillEfektBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
