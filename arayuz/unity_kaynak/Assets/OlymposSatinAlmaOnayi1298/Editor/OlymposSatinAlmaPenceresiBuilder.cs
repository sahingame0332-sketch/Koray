// OLYMPOS-KO · 1298 sure cubuklu satin alma onayi — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Satın Alma Onayı Penceresi Oluştur
// Olculer: arayuz/09-merchant.md (ek bolum) — tablet goruntusu 2266 x 1488, pencere (864,416) 577 x 530
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposSatinAlmaPenceresiBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposSatinAlmaOnayi1298";
        const string BuilderAdi = "OlymposSatinAlmaPenceresiBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;

        [MenuItem("OLYMPOS/1298/Satın Alma Onayı Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            foreach (var d in new[] { "onay_krom", "btn_onay_zemin", "yazi_ok", "yazi_cancel", "onay_ikon_cerceve", "sure_oluk", "sure_dolgu", "ikon_short_bow" }) Tex(d);
            AssetDatabase.Refresh();
            var roboto = LoadFont("Roboto-Bold.ttf");

            // telefon duzeninde ekran konumu (1098, 292): "<ad> Merchant" penceresinin ortasi
            var go = Kok("SatinAlmaOnayi_1298", 1098, 292, T(577), T(530));
            var o = go.AddComponent<OlymposSatinAlmaPenceresi>();
            var bg = Img(go, "Background", null, T(5), T(5), T(567), T(520));
            bg.color = new Color(0f, 0f, 0f, o.backgroundAlpha); bg.raycastTarget = true;
            o.background = bg;
            // cerceve + sari uyari satirlari + pembe baslik orijinal piksellerden
            Img(go, "Krom", "onay_krom", 0, 0, T(577), T(530));

            // esya: cerceve (238,23) 98 x 96 ; ikon (245,30) 84 x 82 ; "+N" mor #CA89E2, tablet punto 29
            o.iconImage = Img(go, "Icon", "ikon_short_bow", T(245), T(30), T(84), T(82));
            Img(go, "IconFrame", "onay_ikon_cerceve", T(238), T(23), T(98), T(96));
            o.upgradeText = Txt(go, "Upgrade", "+5", T(231), T(22), T(100), T(40), roboto, Mathf.RoundToInt(T(29)), Hex("#CA89E2"), TextAnchor.UpperRight);
            o.denemeIkonu = Spr("ikon_short_bow");

            // sure cubugu: oluk (58,144) 460 x 24 ; dolgu (60,147) 455 x 17, turuncu
            Img(go, "TimerTrough", "sure_oluk", T(58), T(144), T(460), T(24));
            var dol = Img(go, "TimerFill", "sure_dolgu", T(60), T(147), T(455), T(17));
            dol.type = Image.Type.Filled; dol.fillMethod = Image.FillMethod.Horizontal; dol.fillOrigin = 0; dol.fillAmount = 0.49f;
            o.fillImage = dol;
            o.dolguGenisligi = T(455);
            // sayac: dolgunun ucunda ; #FFE6E6, dis hatli, tablet punto 19
            var say = new GameObject("Countdown", typeof(RectTransform));
            var srt = (RectTransform)say.transform;
            srt.SetParent(go.transform, false);
            srt.anchorMin = srt.anchorMax = new Vector2(0f, 1f); srt.pivot = new Vector2(0.5f, 1f);
            srt.anchoredPosition = new Vector2(T(60) + T(455) * 0.49f, -T(143)); srt.sizeDelta = new Vector2(T(60), T(26));
            var st = say.AddComponent<Text>();
            st.font = roboto; st.fontSize = Mathf.RoundToInt(T(19)); st.color = Hex("#FFE6E6"); st.alignment = TextAnchor.MiddleCenter; st.text = "2";
            st.horizontalOverflow = HorizontalWrapMode.Overflow; st.verticalOverflow = VerticalWrapMode.Overflow; st.raycastTarget = false;
            var so = say.AddComponent<Outline>(); so.effectColor = new Color(0f, 0f, 0f, 0.95f); so.effectDistance = new Vector2(1f, -1f);
            o.countdownText = st;

            // fiyat satirlari: ortali (merkez x=295.5), 470 genislikte sarar, satir adimi 31, tablet punto 27, #D9C3C3 ; fiyat #FFD300
            var m = Txt(go, "Message", "[Price: <color=#FFD300>99,999,999</color> ] Will you buy this item?\nPlease double check the price",
                        T(60.5f), T(281), T(470), T(110), roboto, Mathf.RoundToInt(T(27)), Hex("#D9C3C3"), TextAnchor.UpperCenter);
            m.supportRichText = true;
            m.horizontalOverflow = HorizontalWrapMode.Wrap;
            m.lineSpacing = 0.98f;
            o.messageText = m;

            // dugmeler (115,437) ve (332,437), 156 x 64 ; yazilar orijinal piksellerden ayri sprite
            o.okButton = Dugme(go, "Btn_OK", "yazi_ok", T(115), T(437), T(47), T(19), T(66), T(28));
            o.cancelButton = Dugme(go, "Btn_Cancel", "yazi_cancel", T(332), T(437), T(14), T(19), T(130), T(28));

            SaveAndPlace(go, "SatinAlmaOnayi_1298");
        }

        /// <summary>Zemin (renklenir) + yazi (renklenmez): kapaliyken yalniz zemin 0.56'ya duser — orijinaldeki soluk OK ile ayni.</summary>
        static Button Dugme(GameObject parent, string name, string yazi, float x, float y, float yx, float yy, float yw, float yh)
        {
            var img = Img(parent, name, "btn_onay_zemin", x, y, T(156), T(64));
            img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>();
            b.targetGraphic = img;
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white; cb.highlightedColor = Color.white; cb.selectedColor = Color.white;
            cb.pressedColor = new Color(0.72f, 0.72f, 0.72f, 1f);
            cb.disabledColor = new Color(0.56f, 0.56f, 0.56f, 1f);
            cb.colorMultiplier = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
            Img(img.gameObject, "Label", yazi, yx, yy, yw, yh);
            return b;
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
