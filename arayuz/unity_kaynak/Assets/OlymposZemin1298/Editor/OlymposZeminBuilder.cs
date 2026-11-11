// OLYMPOS-KO · 1298 zemin malzemeleri — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Zemin Malzemeleri Oluştur
// Dokular, renkler ve karo boylari ekran goruntulerinden olculdu — arayuz/08-zemin.md
using System.IO;
using Olympos.Zemin;
using UnityEditor;
using UnityEngine;

namespace Olympos.Zemin.EditorTools
{
    public static class OlymposZeminBuilder
    {
        /// <summary>Karakterinizin Unity birimindeki boyu. Karo boylari bununla carpilir (olcum "karakter boyu" cinsinden).</summary>
        public const float KarakterBoyu = 1.8f;
        const string Klasor = "OlymposZemin1298";
        static string Root;

        [MenuItem("OLYMPOS/1298/Zemin Malzemeleri Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            foreach (var d in new[] { "zemin_kum", "zemin_tas_doseme", "zemin_tas_tugla", "zemin_tas_arnavut", "zemin_cim" }) Doku(d, true, true);
            Doku("renk_haritasi_kum", false, true);
            Doku("kontrol_kum_cim", false, false);
            Doku("kontrol_moradon_yol", false, false);
            AssetDatabase.Refresh();

            var shader = Shader.Find("Olympos/Zemin1298");
            if (shader == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Zemin1298"); return; }
            string dir = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(dir)) AssetDatabase.CreateFolder(Root, "Materials");

            // tek katmanli malzemeler
            var kum     = Tek(shader, dir, "Zemin_Kum", OlymposZeminTuru.Kum);
            var doseme  = Tek(shader, dir, "Zemin_TasDoseme", OlymposZeminTuru.TasDoseme);
            var tugla   = Tek(shader, dir, "Zemin_TasTugla", OlymposZeminTuru.TasTugla);
            var arnavut = Tek(shader, dir, "Zemin_TasArnavut", OlymposZeminTuru.TasArnavut);
            var cim     = Tek(shader, dir, "Zemin_Cim", OlymposZeminTuru.Cim);

            // kum + cim: ornek kontrol haritasi 12.2 karakter boyu kenarli alandan cikarildi; renk haritasi kum icin
            float kumCimKenar = 12.2f * KarakterBoyu;
            var kumCim = Cok(shader, dir, "Zemin_KumCim",
                new[] { OlymposZeminTuru.Kum, OlymposZeminTuru.Cim }, "kontrol_kum_cim", "renk_haritasi_kum");
            // Moradon yolu: doseme | tugla (3.5 karakter boyu) | arnavut ; harita 32 karakter boyu genis
            float yolKenar = 32f * KarakterBoyu;
            var yol = Cok(shader, dir, "Zemin_MoradonYol",
                new[] { OlymposZeminTuru.TasDoseme, OlymposZeminTuru.TasTugla, OlymposZeminTuru.TasArnavut }, "kontrol_moradon_yol", null);
            AssetDatabase.SaveAssets();

            // deneme sahnesi: yan yana uc zemin
            var kok = new GameObject("OlymposZeminDeneme");
            Undo.RegisterCreatedObjectUndo(kok, "Zemin denemesi");
            Duzlem(kok, "Zemin_MoradonYol", yol, new Vector3(0f, 0f, 0f), yolKenar);
            Duzlem(kok, "Zemin_KumCim", kumCim, new Vector3(yolKenar * 0.5f + kumCimKenar * 0.5f + 2f, 0f, 0f), kumCimKenar);
            Duzlem(kok, "Zemin_Cim", cim, new Vector3(-(yolKenar * 0.5f + kumCimKenar * 0.5f + 2f), 0f, 0f), kumCimKenar);

            var ortam = new GameObject("OlymposOrtamRengi");
            ortam.transform.SetParent(kok.transform, false);
            var o = ortam.AddComponent<OlymposOrtamRengi>();
            o.zeminMalzemeleri = new[] { kum, doseme, tugla, arnavut, cim, kumCim, yol };
            o.OnAyarSec(OlymposOrtamOnAyari.Moradon);

            Selection.activeGameObject = kok;
            Debug.Log("[OLYMPOS] Zemin malzemeleri oluşturuldu: " + dir);
        }

        static Material Tek(Shader s, string dir, string ad, OlymposZeminTuru tur)
        {
            var o = OlymposZeminPaleti.Al(tur);
            var m = Mat(s, dir, ad);
            m.SetTexture("_Katman0", Tex(o.doku));
            float k = OlymposZeminPaleti.KaroBoyu(tur, KarakterBoyu);
            m.SetVector("_KaroBoyu", new Vector4(k, k, k, k));
            EditorUtility.SetDirty(m);
            return m;
        }

        static Material Cok(Shader s, string dir, string ad, OlymposZeminTuru[] katmanlar, string kontrol, string renkHaritasi)
        {
            var m = Mat(s, dir, ad);
            var boy = new Vector4(10f, 10f, 10f, 10f);
            for (int i = 0; i < katmanlar.Length && i < 4; i++)
            {
                m.SetTexture("_Katman" + i, Tex(OlymposZeminPaleti.Al(katmanlar[i]).doku));
                float k = OlymposZeminPaleti.KaroBoyu(katmanlar[i], KarakterBoyu);
                if (i == 0) boy.x = k; else if (i == 1) boy.y = k; else if (i == 2) boy.z = k; else boy.w = k;
            }
            m.SetVector("_KaroBoyu", boy);
            if (!string.IsNullOrEmpty(kontrol)) m.SetTexture("_Kontrol", Tex(kontrol));
            if (!string.IsNullOrEmpty(renkHaritasi)) m.SetTexture("_RenkHaritasi", Tex(renkHaritasi));
            EditorUtility.SetDirty(m);
            return m;
        }

        static Material Mat(Shader s, string dir, string ad)
        {
            string path = dir + "/" + ad + ".mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (m == null) { m = new Material(s); AssetDatabase.CreateAsset(m, path); }
            else m.shader = s;
            return m;
        }

        /// <summary>Kenari "kenar" olan yatay kare duzlem; malzemenin harita alani duzlemin kapladigi yere ayarlanir.</summary>
        static void Duzlem(GameObject kok, string ad, Material m, Vector3 merkez, float kenar)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Plane);        // 10 x 10 birim
            go.name = ad;
            go.transform.SetParent(kok.transform, false);
            go.transform.position = merkez;
            go.transform.localScale = new Vector3(kenar / 10f, 1f, kenar / 10f);
            go.GetComponent<MeshRenderer>().sharedMaterial = m;
            m.SetVector("_HaritaAlani", new Vector4(merkez.x - kenar * 0.5f, merkez.z - kenar * 0.5f, kenar, kenar));
            EditorUtility.SetDirty(m);
        }

        static Texture2D Tex(string ad)
        {
            var t = AssetDatabase.LoadAssetAtPath<Texture2D>(TexDir + "/" + ad + ".png");
            if (t == null) Debug.LogError("[OLYMPOS] Doku bulunamadı: " + TexDir + "/" + ad + ".png");
            return t;
        }

        // doser: zemin dokusu (Repeat, mipmap, anizotropik). Haritalar: Clamp. Kontrol haritasi renk degil veri -> sRGB kapali.
        static void Doku(string ad, bool doser, bool srgb)
        {
            string path = TexDir + "/" + ad + ".png";
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti == null) { Debug.LogError("[OLYMPOS] Doku bulunamadı: " + path); return; }
            ti.textureType = TextureImporterType.Default;
            ti.sRGBTexture = srgb;
            ti.mipmapEnabled = doser;
            ti.wrapMode = doser ? TextureWrapMode.Repeat : TextureWrapMode.Clamp;
            ti.filterMode = doser ? FilterMode.Trilinear : FilterMode.Bilinear;
            ti.anisoLevel = doser ? 8 : 1;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.maxTextureSize = 512;
            ti.SaveAndReimport();
        }

        static string TexDir { get { return Root + "/Textures"; } }

        static string FindRoot()
        {
            var guids = AssetDatabase.FindAssets("OlymposZeminBuilder t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string ed = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(ed).Replace('\\', '/');
            }
            return "Assets/" + Klasor;
        }
    }
}
