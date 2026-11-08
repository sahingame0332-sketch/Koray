// OLYMPOS-KO · 1298 NPC dükkân penceresi kurucu (sadece Editör)
// Menü: OLYMPOS > 1298 > NPC Dükkân Penceresi Oluştur
// Ölçüler oynanış videolarından çıkarıldı (pencere 362 x 352) — arayuz/05-npc-dukkan.md
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposNpcShopBuilder
    {
        const float W = 362f, H = 352f;
        // Ekran koordinati -> pencere-yerel (pencere kokü 563,93)
        const float AX = 563f, AY = 93f;
        static float X(float ax) { return ax - AX; }
        static float Y(float ay) { return ay - AY; }

        // Izgara: 6 x 4, slot 42 px, adim 54.2 x 49
        const float SX0 = 589f, SPX = 54.2f, SY0 = 138f, SPY = 49f, SW = 42f;

        static readonly Color Altin  = Hex("#EBB96E");   // baslik
        static readonly Color Beyaz  = Hex("#F2F2F2");
        static readonly Color Deger  = Hex("#F8F8F8");

        static string Root;
        static Font Slab;

        [MenuItem("OLYMPOS/1298/NPC Dükkân Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            Tex("npc_dukkan_krom");
            AssetDatabase.Refresh();
            Slab = LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf");

            var root = NewRoot("NpcShopWindow_1298", W, H);
            var win = root.AddComponent<OlymposNpcShopWindow>();

            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true;
            win.background = bg;

            // Urun ikonlari ve secim cerceveleri kromun ALTINDA kalmali: once olusturulur.
            for (int r = 0; r < OlymposNpcShopWindow.Satir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.Sutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.Sutun + c;
                    float sx = X(SX0 + SPX * c), sy = Y(SY0 + SPY * r);
                    var ikon = Img(root, "Icon_" + i, null, sx + 2, sy + 2, SW - 4, SW - 4);
                    ikon.enabled = false;
                    win.slotIcons[i] = ikon;

                    var sec = Img(root, "Sel_" + i, null, sx, sy, SW, SW);
                    sec.color = new Color(1f, 0.85f, 0.35f, 0.30f);
                    sec.enabled = false;
                    win.slotSelection[i] = sec;
                }

            // Krom: cerceve, baslik cubugu, bos slotlar, oklar, onay kutusu, dugme, etiketler
            var krom = Img(root, "Krom", "npc_dukkan_krom", 0, 0, W, H);
            krom.raycastTarget = false;

            // Slot tiklama alanlari (kromun ustunde)
            for (int r = 0; r < OlymposNpcShopWindow.Satir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.Sutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.Sutun + c;
                    win.slotButtons[i] = Hit(root, "Slot_" + i,
                        X(SX0 + SPX * c), Y(SY0 + SPY * r), SW, SW);
                }

            win.titleText = Txt(root, "Title", "Caspy[Accessory]", X(563), Y(93), W, 42, 23, Altin, TextAnchor.MiddleCenter);
            win.closeButton = Hit(root, "Btn_Close", X(886), Y(96), 32, 34);

            win.prevPageButton = Hit(root, "Btn_PrevPage", X(672), Y(336), 32, 28);
            win.nextPageButton = Hit(root, "Btn_NextPage", X(786), Y(336), 32, 28);
            win.pageText = Txt(root, "PageText", "1/1", X(712), Y(334), 66, 32, 14, Beyaz, TextAnchor.MiddleCenter);

            win.multipleSellingButton = Hit(root, "Btn_MultipleSelling", X(577), Y(381), 150, 24);
            var check = Img(root, "MultipleSellingCheck", null, X(581), Y(385), 17, 16);
            check.color = new Color(0.95f, 0.95f, 0.95f, 0.95f);
            check.enabled = false;
            win.multipleSellingCheck = check;

            win.sellSelectedButton = Hit(root, "Btn_SellSelected", X(781), Y(378), 133, 27);
            win.totalAmountText = Txt(root, "TotalAmount", "0", X(812), Y(420), 98, 26, 11, Deger, TextAnchor.MiddleCenter);

            win.tooltip = BuildTooltip(root);
            win.dialog  = BuildDialog(root);

            SaveAndPlace(root, "NpcShopWindow_1298");
        }

        // ------------------------------------------------------------------
        static OlymposItemTooltip BuildTooltip(GameObject parent)
        {
            var go = new GameObject("Tooltip", typeof(RectTransform));
            Place(go, parent, 120, 60, 170, 120);
            var t = go.AddComponent<OlymposItemTooltip>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, t.backgroundAlpha);
            t.background = bg;

            t.iconImage       = Img(go, "Icon", null, 6, 6, 28, 28);
            t.nameText        = Txt(go, "Name", "", 40, 6, 124, 16, 12, Hex("#F2F2F2"), TextAnchor.MiddleLeft);
            t.gradeText       = Txt(go, "Grade", "", 40, 22, 124, 14, 10, Hex("#A8A8A8"), TextAnchor.MiddleLeft);
            t.priceText       = Txt(go, "Price", "", 6, 40, 158, 14, 11, Hex("#E03030"), TextAnchor.MiddleLeft);
            t.statsText       = Txt(go, "Stats", "", 6, 56, 158, 32, 10, Hex("#D8C090"), TextAnchor.UpperLeft);
            t.descriptionText = Txt(go, "Description", "", 6, 90, 158, 28, 10, Hex("#E6E6E6"), TextAnchor.UpperLeft);
            t.descriptionText.horizontalOverflow = HorizontalWrapMode.Wrap;
            t.statsText.horizontalOverflow = HorizontalWrapMode.Wrap;
            go.SetActive(false);
            return t;
        }

        static OlymposShopDialog BuildDialog(GameObject parent)
        {
            var go = new GameObject("Dialog", typeof(RectTransform));
            Place(go, parent, 90, 120, 180, 96);
            var d = go.AddComponent<OlymposShopDialog>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, d.backgroundAlpha);
            d.background = bg;

            d.titleText = Txt(go, "Title", "", 8, 6, 164, 16, 12, Hex("#F2F2F2"), TextAnchor.MiddleCenter);
            d.infoText  = Txt(go, "Info", "", 8, 26, 164, 14, 11, Hex("#D8C090"), TextAnchor.MiddleCenter);

            var alan = new GameObject("CountField", typeof(RectTransform));
            Place(alan, go, 50, 44, 80, 18);
            var ai = alan.AddComponent<Image>();
            ai.color = new Color(0.05f, 0.05f, 0.05f, 1f);
            var f = alan.AddComponent<InputField>();
            f.textComponent = Txt(alan, "Text", "1", 3, 0, 74, 18, 11, Hex("#F8F8F8"), TextAnchor.MiddleCenter);
            f.contentType = InputField.ContentType.IntegerNumber;
            f.characterLimit = 6;
            d.countField = f;

            d.confirmButton = Hit(go, "Btn_Confirm", 22, 70, 60, 20);
            d.cancelButton  = Hit(go, "Btn_Cancel", 100, 70, 60, 20);
            Txt(go, "ConfirmText", "Confirm", 22, 70, 60, 20, 10, Hex("#F2F2F2"), TextAnchor.MiddleCenter);
            Txt(go, "CancelText", "Cancel", 100, 70, 60, 20, 10, Hex("#F2F2F2"), TextAnchor.MiddleCenter);
            go.SetActive(false);
            return d;
        }

        // ------------------------------------------------------------------
        static GameObject NewRoot(string name, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = Vector2.zero;
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
                        int size, Color color, TextAnchor anchor)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var t = go.AddComponent<Text>();
            t.font = Slab; t.fontSize = size; t.color = color; t.alignment = anchor; t.text = text;
            t.supportRichText = false;
            t.horizontalOverflow = HorizontalWrapMode.Overflow;
            t.verticalOverflow = VerticalWrapMode.Overflow;
            t.raycastTarget = false;
            var sh = go.AddComponent<Shadow>();
            sh.effectColor = new Color(0f, 0f, 0f, 0.9f);
            sh.effectDistance = new Vector2(1f, -1f);
            return t;
        }

        static Button Hit(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var img = go.AddComponent<Image>();
            img.color = Color.black;
            img.raycastTarget = true;
            var b = go.AddComponent<Button>();
            b.targetGraphic = img;
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor      = new Color(1f, 1f, 1f, 0f);
            cb.highlightedColor = new Color(1f, 1f, 1f, 0.12f);
            cb.pressedColor     = new Color(1f, 1f, 1f, 0.35f);
            cb.selectedColor    = new Color(1f, 1f, 1f, 0f);
            cb.disabledColor    = new Color(1f, 1f, 1f, 0.45f);
            cb.colorMultiplier  = 1f; cb.fadeDuration = 0.05f;
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
            var guids = AssetDatabase.FindAssets("OlymposNpcShopBuilder t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string ed = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(ed).Replace('\\', '/');
            }
            return "Assets/OlymposNpcShop1298";
        }

        static string TexDir { get { return Root + "/Resources/OlymposNpcShop1298"; } }

        static Sprite Spr(string name)
        {
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(TexDir + "/" + name + ".png");
            if (s == null) Debug.LogError("[OLYMPOS] Sprite bulunamadı: " + TexDir + "/" + name + ".png");
            return s;
        }

        static Font LoadFont(string file)
        {
            return AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/" + file);
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
            ti.spriteBorder = Vector4.zero;
            ti.SaveAndReimport();
        }

        static Canvas EnsureCanvas()
        {
            var canvas = Object.FindObjectOfType<Canvas>();
            if (canvas == null)
            {
                var go = new GameObject("Canvas", typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
                canvas = go.GetComponent<Canvas>();
                canvas.renderMode = RenderMode.ScreenSpaceOverlay;
                var sc = go.GetComponent<CanvasScaler>();
                sc.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
                sc.referenceResolution = new Vector2(1920, 1080);
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
