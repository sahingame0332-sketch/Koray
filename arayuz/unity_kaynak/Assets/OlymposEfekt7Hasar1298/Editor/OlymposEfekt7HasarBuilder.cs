// OLYMPOS-KO · 1298 efekt 7 hasar (mobdaki vurus) efekti — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Efekt 7 Hasar (Mobda Vuruş: Aura · Yıldız) Oluştur
// Olculer: arayuz/10-efekt.md (ek 7). Kaynak: kayit 14-01-51 (yakin), 30 kare/sn; mob boyu kayitta 582 px.
using System.IO;
using System.Linq;
using Olympos.Efekt7Hasar;
using UnityEditor;
using UnityEngine;

namespace Olympos.Efekt7Hasar.EditorTools
{
    public static class OlymposEfekt7HasarBuilder
    {
        const string Klasor = "OlymposEfekt7Hasar1298";
        // Inspector'dan degistirilebilir: arka katmanda kayittaki cit cubugu izleri kalsin mi (onizlemeyle birebir) yoksa citsiz kopya mi
        public static bool CitsizArka = false;

        struct Katman
        {
            public string efekt, tur; public float genislik, enBoy, px, py;
            public Katman(string e, string t, float g, float b, float x, float y) { efekt = e; tur = t; genislik = g; enBoy = b; px = x; py = y; }
        }
        // efekt, katman, genislik (mob boyu), yukseklik/genislik, pivot x, pivot y (alttan) — mobun zemin noktasi
        static readonly Katman[] KATMANLAR = { // kesik_aura arka: karakterin kilic yayi cikarildi (ayri paket), olculer ayni
            new Katman("kesik_aura", "arka", 2.4227f, 0.5915f, 0.3582f, 0.2974f),
            new Katman("kesik_aura", "on", 0.9278f, 1.1870f, 0.6481f, 0.0858f),
            new Katman("yildiz", "arka", 1.6100f, 0.8239f, 0.5390f, 0.3212f),
            new Katman("yildiz", "on", 0.6546f, 1.6063f, 0.5459f, 0.0425f),
        };

        [MenuItem("OLYMPOS/1298/Efekt 7 Hasar (Mobda Vuruş: Aura · Yıldız) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Efekt7 Hasar Eklemeli");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt7 Hasar Eklemeli"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            var mat = Malzeme(md + "/Efekt7Hasar_Eklemeli.mat", sh);

            var kok = new GameObject("OlymposEfekt7Hasar");
            var kut = kok.AddComponent<OlymposEfekt7HasarKutuphanesi>();
            float x = -1.5f;
            foreach (var ad in new[] { "kesik_aura", "yildiz" })
            {
                var g = new GameObject(ad == "kesik_aura" ? "Kesik + Aura" : "Yildiz Vurusu");
                g.transform.SetParent(kok.transform, false); g.transform.localPosition = new Vector3(x, 0, 0); x += 3f;
                var ef = g.AddComponent<OlymposEfekt7Hasar>(); ef.skillAdi = ad;
                var hd = new GameObject("Hedef (deneme: buraya mobu koyun)"); hd.transform.SetParent(g.transform, false);
                ef.hedefDeneme = hd.transform; ef.denemeDongusu = true;
                foreach (var k in KATMANLAR.Where(k => k.efekt == ad))
                {
                    var go = new GameObject(k.tur == "arka" ? "Arka Katman (mobun arkasi)" : "On Katman (mobun onu)", typeof(MeshFilter), typeof(MeshRenderer));
                    go.transform.SetParent(g.transform, false);
                    var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = mat;
                    mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
                    var kt = go.AddComponent<OlymposEfekt7HasarKatman>();
                    string klasor = k.tur == "arka" && CitsizArka && AssetDatabase.IsValidFolder(root + "/Textures/" + ad + "_arka_temiz") ? ad + "_arka_temiz" : ad + "_" + k.tur;
                    kt.kareler = Kareler(root + "/Textures/" + klasor);
                    kt.genislikHedef = k.genislik; kt.enBoy = k.enBoy; kt.pivot = new Vector2(k.px, k.py);
                    kt.derinlik = k.tur == "arka" ? 0.6f : -0.6f;
                    kt.MeshKur();
                    if (k.tur == "arka") ef.arka = kt; else ef.on = kt;
                }
                kut.efektler.Add(ef);
            }
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposEfekt7Hasar.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Efekt 7 hasar");
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Efekt 7 oluşturuldu (kesik_aura, yildiz).");
        }

        static Material Malzeme(string p, Shader sh)
        {
            var m = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (m == null) { m = new Material(sh); AssetDatabase.CreateAsset(m, p); }
            return m;
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
            var g = AssetDatabase.FindAssets("OlymposEfekt7HasarBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
