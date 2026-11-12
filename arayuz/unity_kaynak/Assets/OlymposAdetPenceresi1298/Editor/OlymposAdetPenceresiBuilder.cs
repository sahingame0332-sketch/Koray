// OLYMPOS-KO · 1298 adet girisi penceresi — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Adet Penceresi Oluştur
// Olculer: arayuz/09-merchant.md (ek bolum) — tablet goruntusu 2266 x 1488, pencere (1170,325) 740 x 543
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposAdetPenceresiBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposAdetPenceresi1298";
        const string BuilderAdi = "OlymposAdetPenceresiBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;

        [MenuItem("OLYMPOS/1298/Adet Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            Tex("adet_krom");
            AssetDatabase.Refresh();
            var roboto = LoadFont("Roboto-Regular.ttf");

            // telefon duzeninde ekran konumu (1605, 208): Create a Merchant icinde, fiyat diyaloguyla ayni yer
            var go = Kok("AdetPenceresi_1298", 1605, 208, T(740), T(543));
            var a = go.AddComponent<OlymposAdetPenceresi>();
            var bg = Img(go, "Background", null, T(6), T(6), T(728), T(531));
            bg.color = new Color(0f, 0f, 0f, a.backgroundAlpha); bg.raycastTarget = true;
            a.background = bg;
            // baslik + iki dildeki uyari + alan cercevesi + OK / CANCEL orijinal piksellerden
            Img(go, "Krom", "adet_krom", 0, 0, T(740), T(543));

            // sayi alani: yuvarlak uclu cerceve (137,358) 462 x 72 ; sayi egik, #D6D6D6, tablet punto 46, murek solu x=219
            var alan = new GameObject("CountField", typeof(RectTransform));
            Place(alan, go, T(150), T(362), T(440), T(64));
            var ai = alan.AddComponent<Image>(); ai.color = new Color(0f, 0f, 0f, 0f); ai.raycastTarget = true;
            var inp = alan.AddComponent<InputField>();
            inp.targetGraphic = ai;
            var t = Txt(alan, "Text", "20", T(69), 0, T(360), T(64), roboto, Mathf.RoundToInt(T(46)), Hex("#D6D6D6"), TextAnchor.MiddleLeft);
            t.fontStyle = FontStyle.Italic;
            inp.textComponent = t;
            inp.contentType = InputField.ContentType.IntegerNumber;
            inp.keyboardType = TouchScreenKeyboardType.NumberPad;
            inp.lineType = InputField.LineType.SingleLine;
            inp.characterLimit = 5;
            inp.text = "20";
            a.countField = inp;

            a.okButton = Hit(go, "Btn_OK", T(154), T(457), T(204), T(65));
            a.cancelButton = Hit(go, "Btn_Cancel", T(380), T(457), T(207), T(65));

            SaveAndPlace(go, "AdetPenceresi_1298");
        }

        // ------------------------------------------------------------------ yardimcilar
        // Olculer TABLET goruntusunden (2266 x 1488) alindi; o duzen telefon duzeninin (2712 x 1220) 1.0405 kati.
        // Tablet pikseli olarak yazilir, T() telefon birimine cevirir. Sprite'lar tablet cozunurlugunde.
        const float Tablet = 1.0405f;
        static float T(float v) { return v / Tablet; }

        static GameObject Kok(string name, float ekranX, float ekranY, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = new Vector2(ekranX + w * 0.5f - EW * 0.5f, EH * 0.5f - (ekranY + h * 0.5f));
            return go;
        }

        static RectTransform Place(GameObject go, GameObject parent, float x, float y, float w, float h)
        {
            var rt = go.GetComponent<RectTransform>();
            if (rt == null) rt = go.AddComponent<RectTransform>();
            rt.SetParent(parent.transform, false);
            rt.anchorMin = rt.anchorMax = new Vector2(0f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.anchoredPosition = new Vector2(x, -y);
            rt.sizeDelta = new Vector2(w, h);
            return rt;
        }

        static Image Img(GameObject parent, string name, string sprite, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var img = go.AddComponent<Image>();
            if (!string.IsNullOrEmpty(sprite)) img.sprite = Spr(sprite);
            img.raycastTarget = false;
            return img;
        }

        static Text Txt(GameObject parent, string name, string text, float x, float y, float w, float h,
                        Font font, int size, Color color, TextAnchor anchor)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var t = go.AddComponent<Text>();
            t.font = font; t.fontSize = size; t.color = color; t.alignment = anchor; t.text = text;
            t.supportRichText = false;
            t.horizontalOverflow = HorizontalWrapMode.Overflow;
            t.verticalOverflow = VerticalWrapMode.Overflow;
            t.raycastTarget = false;
            return t;
        }

        /// <summary>Kromun ustundeki gorunmez tiklama alani (basinca hafif kararir).</summary>
        static Button Hit(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var img = go.AddComponent<Image>();
            img.color = Color.black; img.raycastTarget = true;
            var b = go.AddComponent<Button>();
            b.targetGraphic = img;
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor = new Color(1f, 1f, 1f, 0f); cb.highlightedColor = new Color(1f, 1f, 1f, 0f);
            cb.pressedColor = new Color(1f, 1f, 1f, 0.35f);
            cb.selectedColor = new Color(1f, 1f, 1f, 0f); cb.disabledColor = new Color(1f, 1f, 1f, 0f);
            cb.colorMultiplier = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
            return b;
        }

        static void SaveAndPlace(GameObject root, string prefabName)
        {
            string dir = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(dir)) AssetDatabase.CreateFolder(Root, "Prefabs");
            string path = dir + "/" + prefabName + ".prefab";
            var prefab = PrefabUtility.SaveAsPrefabAsset(root, path);
            Object.DestroyImmediate(root);
            var canvas = EnsureCanvas();
            var inst = (GameObject)PrefabUtility.InstantiatePrefab(prefab, canvas.transform);
            Undo.RegisterCreatedObjectUndo(inst, "Create " + prefabName);
            Selection.activeGameObject = inst;
            Debug.Log("[OLYMPOS] Oluşturuldu: " + path);
        }

        static string FindRoot()
        {
            var guids = AssetDatabase.FindAssets(BuilderAdi + " t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string ed = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(ed).Replace('\\', '/');
            }
            return "Assets/" + Klasor;
        }

        static string TexDir { get { return Root + "/Resources/" + Klasor; } }

        static Sprite Spr(string name)
        {
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(TexDir + "/" + name + ".png");
            if (s == null) Debug.LogError("[OLYMPOS] Sprite bulunamadı: " + TexDir + "/" + name + ".png");
            return s;
        }

        static Font LoadFont(string file) { return AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/" + file); }

        static void Tex(string name)
        {
            string path = TexDir + "/" + name + ".png";
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti == null) { Debug.LogError("[OLYMPOS] Doku bulunamadı: " + path); return; }
            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Single;
            ti.spritePixelsPerUnit = 100f;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.filterMode = FilterMode.Bilinear;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.maxTextureSize = 2048;
            ti.SaveAndReimport();
        }

        // OyunIci / Merchant paketleriyle ortak Canvas (2712 x 1220, yukseklige gore olcek). Yoksa olusturulur.
        static Canvas EnsureCanvas()
        {
            Canvas canvas = null;
            var hepsi = Object.FindObjectsOfType<Canvas>();
            for (int i = 0; i < hepsi.Length; i++) if (hepsi[i].name == CanvasAdi) canvas = hepsi[i];
            if (canvas == null)
            {
                var go = new GameObject(CanvasAdi, typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
                canvas = go.GetComponent<Canvas>();
                canvas.renderMode = RenderMode.ScreenSpaceOverlay;
                canvas.sortingOrder = 10;
                var sc = go.GetComponent<CanvasScaler>();
                sc.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
                sc.referenceResolution = new Vector2(EW, EH);
                sc.matchWidthOrHeight = 1f;
                Undo.RegisterCreatedObjectUndo(go, "Create Canvas");
            }
            if (Object.FindObjectOfType<EventSystem>() == null)
            {
                var es = new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
                Undo.RegisterCreatedObjectUndo(es, "Create EventSystem");
            }
            return canvas;
        }

        static Color Hex(string h) { Color c; ColorUtility.TryParseHtmlString(h, out c); return c; }
    }
}
