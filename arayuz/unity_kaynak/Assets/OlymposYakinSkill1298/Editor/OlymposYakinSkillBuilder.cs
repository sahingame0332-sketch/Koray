// OLYMPOS-KO · 1298 yakin dovus skill efektleri (Stroke · Stab · Stab2) — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Yakın Skill Efektleri (Stroke · Stab · Stab2) Oluştur
// Olculer: yakin_skill_olculer.json ve arayuz/10-efekt.md (ek 6). Bu dosya araclar/efekt/paket6.py ile uretildi.
using System.IO;
using System.Linq;
using Olympos.YakinSkill;
using UnityEditor;
using UnityEngine;

namespace Olympos.YakinSkill.EditorTools
{
    public static class OlymposYakinSkillBuilder
    {
        const string Klasor = "OlymposYakinSkill1298";

        struct Katman
        {
            public string skill, tur; public float genislik, enBoy, px, py, ustSonum;
            public Katman(string s, string t, float g, float e, float x, float y, float u) { skill = s; tur = t; genislik = g; enBoy = e; px = x; py = y; ustSonum = u; }
        }

        // skill, katman, genislik (karakter boyu), yukseklik/genislik, pivot x, pivot y, ust sonum — olculdu
        static readonly Katman[] KATMANLAR = {
            new Katman("stroke", "karakter", 6.5556f, 0.6773f, 0.5022f, 0.2892f, 0.00f),
            new Katman("stroke", "hedef", 2.0845f, 1.7674f, 0.5302f, 0.1377f, 0.08f),
            new Katman("stab", "karakter", 4.6091f, 1.0179f, 0.7089f, 0.2737f, 0.00f),
            new Katman("stab", "hedef", 2.0396f, 1.5200f, 0.6067f, 0.0184f, 0.08f),
            new Katman("stab2", "karakter", 4.9136f, 0.7504f, 0.6700f, 0.3482f, 0.00f),
        };
        static readonly string[][] SKILLER = { new[] { "stroke", "Stroke" }, new[] { "stab", "Stab" }, new[] { "stab2", "Stab2" } };

        [MenuItem("OLYMPOS/1298/Yakın Skill Efektleri (Stroke · Stab · Stab2) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Yakin Skill Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Yakin Skill Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");

            var kok = new GameObject("OlymposYakinSkillEfektleri");
            var kut = kok.AddComponent<OlymposYakinSkillKutuphanesi>();
            float x = -4f;
            foreach (var s in SKILLER)
            {
                var sgo = new GameObject(s[1]);
                sgo.transform.SetParent(kok.transform, false); sgo.transform.localPosition = new Vector3(x, 0, 0); x += 4f;
                var ef = sgo.AddComponent<OlymposYakinSkillEfekti>(); ef.skillAdi = s[1];
                var hd = new GameObject("Hedef (deneme)"); hd.transform.SetParent(sgo.transform, false); hd.transform.localPosition = new Vector3(-0.3f, 0, -1.2f);
                ef.hedefDeneme = hd.transform; ef.denemeDongusu = true;              // denemede surekli; oyunda Oyna(karakter, hedef)
                foreach (var k in KATMANLAR.Where(k => k.skill == s[0]))
                {
                    var mat = Malzeme(md, sh, k);
                    var go = new GameObject(k.tur == "karakter" ? "Karakter Katmani" : "Hedef Katmani", typeof(MeshFilter), typeof(MeshRenderer));
                    go.transform.SetParent(sgo.transform, false);
                    var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
                    mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
                    var kt = go.AddComponent<OlymposYakinSkillKatmani>();
                    kt.kareler = Kareler(root + "/Textures/" + k.skill + "_" + k.tur);
                    kt.genislikKarakter = k.genislik; kt.enBoy = k.enBoy; kt.pivot = new Vector2(k.px, k.py);
                    kt.MeshKur();
                    if (k.tur == "karakter") ef.karakterKatmani = kt; else ef.hedefKatmani = kt;
                }
                kut.efektler.Add(ef);
            }
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposYakinSkillEfektleri.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Yakin skill efektleri");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Yakın skill efektleri oluşturuldu (Stroke, Stab, Stab2).");
        }

        static Material Malzeme(string md, Shader sh, Katman k)
        {
            string p = md + "/YakinSkill_" + (k.ustSonum > 0f ? "Isin" : "Eklemeli") + ".mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (mat == null) { mat = new Material(sh); mat.SetFloat("_UstSonum", k.ustSonum); AssetDatabase.CreateAsset(mat, p); }
            return mat;
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
            var g = AssetDatabase.FindAssets("OlymposYakinSkillBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
