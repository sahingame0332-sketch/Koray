// OLYMPOS-KO · 1298 ItemUpgrade — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Item Upgrade Penceresi Oluştur.  Olculer: arayuz/23-upgrade.md (kaynak goruntu pikseli, sol-ust).
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposItemUpgradeBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposItemUpgrade1298";
        const string BuilderAdi = "OlymposItemUpgradeBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;

        // Kaynak goruntu 2266x1488 (tablet); ortak 2712x1220 Canvas'a yukseklige gore olcek 0.8199, sag kenara yasli.
        const float SX = 2266f, SY = 1488f, OLCEK = 0.819892f;

        [MenuItem("OLYMPOS/1298/Item Upgrade Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            Tex("itemupgrade_pencere");
            AssetDatabase.Refresh();
            var slab = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Bold.ttf");
            var slabR = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Regular.otf");
            const float X = 1165, Y = 150;
            var go = Kok("ItemUpgrade_1298", X, Y, 857, 1235);
            var p = go.AddComponent<OlymposItemUpgradePenceresi>();
            var bg = Img(go, "Background", null, 24, 102, 812, 1072); bg.raycastTarget = true; p.background = bg; bg.color = new Color(0f, 0f, 0f, p.backgroundAlpha);
            Img(go, "Krom", "itemupgrade_pencere", 0, 0, 857, 1235);
            var yuv = new System.Collections.Generic.List<Image>();
            yuv.Add(Ikon(go, "Yuva_0", 113, 260, 100, 95));
            yuv.Add(Ikon(go, "Yuva_1", 660, 258, 101, 97));
            yuv.Add(Ikon(go, "Yuva_2", 292, 176, 82, 83));
            yuv.Add(Ikon(go, "Yuva_3", 395, 176, 82, 83));
            yuv.Add(Ikon(go, "Yuva_4", 498, 176, 82, 83));
            yuv.Add(Ikon(go, "Yuva_5", 292, 286, 82, 83));
            yuv.Add(Ikon(go, "Yuva_6", 395, 286, 82, 83));
            yuv.Add(Ikon(go, "Yuva_7", 498, 286, 82, 83));
            yuv.Add(Ikon(go, "Yuva_8", 292, 396, 82, 83));
            yuv.Add(Ikon(go, "Yuva_9", 395, 396, 82, 83));
            yuv.Add(Ikon(go, "Yuva_10", 498, 396, 82, 83));
            p.upgradeYuvalari = yuv.ToArray();
            int[] ex = { 64, 173, 283, 393, 502, 611, 720 }, ey = { 764, 871, 978, 1085 };
            var env = new Image[ex.Length * ey.Length]; var adt = new Text[env.Length];
            for (int r = 0; r < ey.Length; r++) for (int k = 0; k < ex.Length; k++) { int i = r * ex.Length + k; env[i] = Ikon(go, "Envanter_" + i, ex[k] + 2, ey[r] + 2, 84, 86);
                adt[i] = Txt(go, "Adet_" + i, "", ex[k], ey[r] + 60, 85, 28, slab, 18, Color.white, TextAnchor.LowerRight); }
            p.envanterYuvalari = env; p.envanterAdetleri = adt;
            p.needCoinsText = Yazi(go, "NeedCoins", "-", 164.5f, 447f, slabR, 27, 0f, Hex("#F0F2F5"));
            p.upgradeRateText = Yazi(go, "UpgradeRate", "-", 711f, 447f, slabR, 39, 1.5f, Hex("#E1E1E3"));
            p.paraText = Yazi(go, "Para", "5,042,580", 695f, 702.5f, slab, 34, 1f, Hex("#FFFFFF"));
            p.upgradeButton = Hit(go, "Btn_Upgrade", 117, 558, 188, 64);
            p.cancelButton = Hit(go, "Btn_Cancel", 345, 558, 190, 64);
            p.previewButton = Hit(go, "Btn_Preview", 571, 557, 190, 64);
            p.closeButton = Hit(go, "Btn_Close", 744, 19, 64, 64);
            SaveAndPlace(go, "ItemUpgrade_1298");
        }

        /// <summary>Kok: kaynak goruntudeki sol-ust (x,y), boyut (w,h) piksel; sag-orta capali, OLCEK ile kucultulmus.</summary>
        static GameObject Kok(string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(1f, 0.5f); rt.pivot = new Vector2(0f, 1f);
            rt.sizeDelta = new Vector2(w, h); rt.localScale = new Vector3(OLCEK, OLCEK, 1f);
            rt.anchoredPosition = new Vector2(-(SX - x) * OLCEK, (SY * 0.5f - y) * OLCEK);
            return go;
        }

        /// <summary>Ortali tek satir yazi; (cx, cy) murekkep merkezi, pencere ici piksel.</summary>
        static Text Yazi(GameObject parent, string ad, string metin, float cx, float cy, Font f, int punto, float aralik, Color renk)
        {
            var t = Txt(parent, ad, metin, cx - 200f, cy - 30f, 400f, 60f, f, punto, renk, TextAnchor.MiddleCenter);
            if (aralik != 0f) t.gameObject.AddComponent<OlymposItemUpgradeHarfAraligi>().aralik = aralik;
            return t;
        }

        static Image Ikon(GameObject parent, string ad, float x, float y, float w, float h)
        {
            var img = Img(parent, ad, null, x, y, w, h); img.preserveAspect = true; img.enabled = false; return img;
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

        // OyunIci / Merchant / Alim-Satim paketleriyle ortak Canvas (2712 x 1220, yukseklige gore olcek). Yoksa olusturulur.
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
