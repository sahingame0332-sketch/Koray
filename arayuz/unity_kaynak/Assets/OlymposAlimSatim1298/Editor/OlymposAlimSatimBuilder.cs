// OLYMPOS-KO · 1298 NPC alim-satim penceresi — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > NPC Alım-Satım Penceresi Oluştur.  Olculer: arayuz/15-npc-alimsatim.md (ekran pikseli, sol-ust).
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposAlimSatimBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposAlimSatim1298";
        const string BuilderAdi = "OlymposAlimSatimBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;

        [MenuItem("OLYMPOS/1298/NPC Alım-Satım Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            Tex("alimsatim_pencere"); Tex("alimsatim_giris");
            AssetDatabase.Refresh();
            var slab = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Bold.ttf");

            // sprite (1662,539) 622 x 258 ; siyah zemin = ic (1669,546) 607 x 244
            const float X = 1662, Y = 539;
            var go = Bos(null, "NpcAlimSatim_1298", X, Y, 622, 258);
            var p = go.AddComponent<OlymposAlimSatimPenceresi>();
            var bg = Img(go, "Background", null, 1669 - X, 546 - Y, 607, 244);
            bg.raycastTarget = true; p.background = bg; bg.color = new Color(0f, 0f, 0f, p.backgroundAlpha);
            Img(go, "Krom", "alimsatim_pencere", 0, 0, 622, 258);
            // esya adi: merkez (1982, 574) ; ikinci satir: merkez (1985, 607.5) — Roboto Slab Bold 25, +2 px, #EBEBEB
            p.esyaText = Yazi(go, "EsyaAdi", "Holy water", 1982 - 290 - X, 574 - 18 - Y, 580, 36, slab);
            p.satirText = Yazi(go, "Satir", "Buy Item Count:", 1985 - 290 - X, 607.5f - 18 - Y, 580, 36, slab);
            // sayi kutusu (1752,637) 404 x 42 ; sayi Roboto Slab Bold 26 #F0DCDC, sol 1768
            var kutu = Bos(go, "GirisKutusu", 1752 - X, 637 - Y, 404, 42);
            var ki = Img(kutu, "Cerceve", "alimsatim_giris", 0, 0, 404, 42); ki.raycastTarget = true;
            var inp = kutu.AddComponent<InputField>();
            inp.targetGraphic = ki;
            var t = Txt(kutu, "Text", "1", 1768 - 1752, 0, 370, 40, slab, 26, Hex("#F0DCDC"), TextAnchor.MiddleLeft);
            inp.textComponent = t; inp.contentType = InputField.ContentType.IntegerNumber; inp.keyboardType = TouchScreenKeyboardType.NumberPad;
            inp.lineType = InputField.LineType.SingleLine; inp.characterLimit = 5; inp.text = "1";
            p.girisKutusu = kutu; p.adetField = inp;
            p.confirmButton = Hit(go, "Btn_Confirm", 1765 - X, 693 - Y, 186, 50);
            p.cancelButton = Hit(go, "Btn_Cancel", 1971 - X, 693 - Y, 188, 50);
            SaveAndPlace(go, "NpcAlimSatim_1298");
        }

        static GameObject Bos(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            if (parent != null) { Place(go, parent, x, y, w, h); return go; }
            var rt = (RectTransform)go.transform;                      // kok: ekran konumu (2712x1220, sol-ust)
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f); rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = new Vector2(x + w * 0.5f - EW * 0.5f, EH * 0.5f - (y + h * 0.5f));
            return go;
        }

        static Text Yazi(GameObject parent, string ad, string metin, float x, float y, float w, float h, Font f)
        {
            var t = Txt(parent, ad, metin, x, y, w, h, f, 25, Hex("#EBEBEB"), TextAnchor.MiddleCenter);
            t.gameObject.AddComponent<OlymposAlimSatimHarfAraligi>().aralik = 2f;
            return t;
        }

        // ---------------------------------------------------------------- yardimcilar
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
