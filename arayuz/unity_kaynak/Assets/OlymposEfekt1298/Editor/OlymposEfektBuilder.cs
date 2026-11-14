// OLYMPOS-KO · 1298 efektler — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Efektler (Ateş Sütunu · Vuruş · Cast) Oluştur
// Kayit: 2266 x 1488, 60 kare/sn; olculer depoda arayuz/10-efekt.md
using System.IO;
using System.Linq;
using Olympos.Efekt;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.Efekt.EditorTools
{
    public static class OlymposEfektBuilder
    {
        const string Klasor = "OlymposEfekt1298";
        const float EW = 2712f, EH = 1220f, Tablet = 1.0405f;
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;
        static float T(float v) { return v / Tablet; }

        [MenuItem("OLYMPOS/1298/Efektler (Ateş Sütunu · Vuruş · Cast) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            var ates = Kareler("AtesSutunu");
            var vurus = Kareler("Vurus");
            Tex("Cast/cast_oluk", false); Tex("Cast/cast_dolgu", false);
            AssetDatabase.Refresh();

            var shader = Shader.Find("Olympos/Efekt Eklemeli");
            if (shader == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Efekt Eklemeli"); return; }
            string md = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(Root, "Materials");
            string mp = md + "/Efekt_Eklemeli.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp);
            if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, mp); }

            var kok = new GameObject("OlymposEfektDeneme");
            Undo.RegisterCreatedObjectUndo(kok, "Efekt denemesi");
            // Pillar of Fire: kare 500 x 710 px; mobun ayagi (200, 600) -> pivot (0.40, 0.155); karakter ~110 px -> genislik 4.5 karakter boyu
            var a = Oynatici(kok, "AtesSutunu (Pillar of Fire)", mat, ates, 4.5f, 1.42f, new Vector2(0.40f, 0.155f), new Vector3(-2f, 0f, 0f));
            // karaktere vurus: kare 450 x 420 px; karakterin govdesi (258, 230) -> pivot (0.573, 0.452); genislik 4.1 karakter boyu
            var v = Oynatici(kok, "Vurus (karaktere)", mat, vurus, 4.1f, 0.933f, new Vector2(0.573f, 0.452f), new Vector3(2f, 0.9f, 0f));
            v.dongu = true; a.dongu = true;          // denemede surekli oynasin; oyunda dongu kapali, Hedefte(...) ile tetikleyin

            BuildCast();
            Selection.activeGameObject = kok;
            AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Efektler oluşturuldu.");
        }

        static OlymposEfektOynatici Oynatici(GameObject kok, string ad, Material mat, Texture2D[] k, float gen, float enBoy, Vector2 pivot, Vector3 konum)
        {
            var go = new GameObject(ad, typeof(MeshFilter), typeof(MeshRenderer));
            go.transform.SetParent(kok.transform, false);
            go.transform.position = konum;
            var mr = go.GetComponent<MeshRenderer>();
            mr.sharedMaterial = mat;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            mr.receiveShadows = false;
            var o = go.AddComponent<OlymposEfektOynatici>();
            o.kareler = k; o.genislikKarakter = gen; o.enBoy = enBoy; o.pivot = pivot; o.fps = 30f;
            o.bitinceGizle = false;
            return o;
        }

        // Cast cubugu: tablet (1032, 1002) 205 x 12 ; ad merkezi x=1124, murek ust 986 ; sure murek sol 1107, ust 1017
        static void BuildCast()
        {
            var canvas = EnsureCanvas();
            var go = new GameObject("CastCubugu_1298", typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.SetParent(canvas.transform, false);
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            // ekran ortasina gore konum (tablet kaydinda ortanin 1.5 px sagi, 266 px alti) -> telefon birimi
            rt.sizeDelta = new Vector2(T(205), T(52));
            rt.anchoredPosition = new Vector2(T(1134.5f - 2266f * 0.5f), T(1488f * 0.5f - 1010f));
            var c = go.AddComponent<OlymposCastCubugu>();
            var roboto = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/Roboto-Bold.ttf");
            Img(go, "Trough", Spr("Cast/cast_oluk"), 0, T(18), T(205), T(12));
            var d = Img(go, "Fill", Spr("Cast/cast_dolgu"), T(2), T(19), T(201), T(8));
            d.type = Image.Type.Filled; d.fillMethod = Image.FillMethod.Horizontal; d.fillOrigin = 0; d.fillAmount = 0.85f;
            c.dolgu = d;
            c.adText = Txt(go, "SkillName", "Pillar Of Fire", 0, 0, T(205), T(18), roboto, Mathf.RoundToInt(T(15)), Hex("#FDE1E2"), TextAnchor.MiddleCenter);
            c.sureText = Txt(go, "Remaining", "0,2 sec", 0, T(31), T(205), T(20), roboto, Mathf.RoundToInt(T(17)), Hex("#E3DF73"), TextAnchor.MiddleCenter);
            foreach (var t in new[] { c.adText, c.sureText })
            {
                var o = t.gameObject.AddComponent<Outline>(); o.effectColor = new Color(0f, 0f, 0f, 0.9f); o.effectDistance = new Vector2(1f, -1f);
            }
            Undo.RegisterCreatedObjectUndo(go, "Cast cubugu");
        }

        static Texture2D[] Kareler(string alt)
        {
            string dir = Root + "/Textures/" + alt;
            var yollar = Directory.GetFiles(dir, "*.png").Select(p => p.Replace('\\', '/')).OrderBy(p => p).ToArray();
            foreach (var p in yollar) Tex(alt + "/" + Path.GetFileNameWithoutExtension(p), true);
            AssetDatabase.Refresh();
            return yollar.Select(p => AssetDatabase.LoadAssetAtPath<Texture2D>(p)).ToArray();
        }

        static void Tex(string ad, bool efekt)
        {
            string path = Root + "/Textures/" + ad + ".png";
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti == null) { Debug.LogError("[OLYMPOS] Doku bulunamadı: " + path); return; }
            ti.textureType = efekt ? TextureImporterType.Default : TextureImporterType.Sprite;
            if (!efekt) ti.spriteImportMode = SpriteImportMode.Single;
            ti.alphaIsTransparency = false;
            ti.mipmapEnabled = false;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.filterMode = FilterMode.Bilinear;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.maxTextureSize = 1024;
            ti.SaveAndReimport();
        }

        static Sprite Spr(string ad) { return AssetDatabase.LoadAssetAtPath<Sprite>(Root + "/Textures/" + ad + ".png"); }

        static Image Img(GameObject parent, string name, Sprite s, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var img = go.AddComponent<Image>(); img.sprite = s; img.raycastTarget = false;
            return img;
        }

        static Text Txt(GameObject parent, string name, string text, float x, float y, float w, float h, Font font, int size, Color color, TextAnchor anchor)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var t = go.AddComponent<Text>();
            t.font = font; t.fontSize = size; t.color = color; t.alignment = anchor; t.text = text;
            t.horizontalOverflow = HorizontalWrapMode.Overflow; t.verticalOverflow = VerticalWrapMode.Overflow; t.raycastTarget = false;
            return t;
        }

        static void Place(GameObject go, GameObject parent, float x, float y, float w, float h)
        {
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent.transform, false);
            rt.anchorMin = rt.anchorMax = new Vector2(0f, 1f); rt.pivot = new Vector2(0f, 1f);
            rt.anchoredPosition = new Vector2(x, -y); rt.sizeDelta = new Vector2(w, h);
        }

        static Canvas EnsureCanvas()
        {
            Canvas canvas = null;
            foreach (var c in Object.FindObjectsOfType<Canvas>()) if (c.name == CanvasAdi) canvas = c;
            if (canvas == null)
            {
                var go = new GameObject(CanvasAdi, typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
                canvas = go.GetComponent<Canvas>(); canvas.renderMode = RenderMode.ScreenSpaceOverlay; canvas.sortingOrder = 10;
                var sc = go.GetComponent<CanvasScaler>();
                sc.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize; sc.referenceResolution = new Vector2(EW, EH); sc.matchWidthOrHeight = 1f;
                Undo.RegisterCreatedObjectUndo(go, "Create Canvas");
            }
            if (Object.FindObjectOfType<EventSystem>() == null)
                Undo.RegisterCreatedObjectUndo(new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule)), "Create EventSystem");
            return canvas;
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposEfektBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }

        static Color Hex(string h) { Color c; ColorUtility.TryParseHtmlString(h, out c); return c; }
    }
}
