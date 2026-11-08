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
        // Olculer 2266x1488 ekran goruntulerinden alindi — arayuz/05-npc-dukkan.md
        const float W = 750f, H = 1156f;
        const float AX = 1167f, AY = 193f;               // pencerenin ekrandaki sol-ust kosesi
        static float X(float ax) { return ax - AX; }
        static float Y(float ay) { return ay - AY; }

        const float SX0 = 1223f, SPX = 112.2f, SY0 = 286f, SPY = 101f, SW = 86f, SH = 87f;   // dukkan 6x4
        const float IX0 = 1209f, IPX = 98.2f,  IY0 = 941f, IPY = 98f,  IW = 86f, IH = 90f;   // envanter 7x4

        static readonly Color Altin  = Hex("#EBB96E");   // baslik
        static readonly Color Beyaz  = Hex("#F2F2F2");
        static readonly Color Deger  = Hex("#F8F8F8");

        static string Root;
        static Font Slab;

        [MenuItem("OLYMPOS/1298/NPC \"Open\" Düğmesi Oluştur")]
        public static void BuildOpenButton()
        {
            Root = FindRoot();
            Tex("btn_open");
            AssetDatabase.Refresh();
            Slab = LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf");

            const float BW = 281f, BH = 84f;     // orijinalden olculdu
            var root = NewRoot("NpcOpenButton_1298", BW, BH);
            var ob = root.AddComponent<OlymposNpcOpenButton>();

            var img = root.AddComponent<Image>();
            img.sprite = Spr("btn_open");
            img.raycastTarget = true;

            var b = root.AddComponent<Button>();
            b.targetGraphic = img;
            Renkler(b, true);
            ob.button = b;

            // Yazi: orijinalde beyaz (240,240,240), Roboto Slab Bold punto 46
            ob.label = Txt(root, "Label", "Open", 0, 0, BW, BH, 46, Hex("#F0F0F0"), TextAnchor.MiddleCenter);

            SaveAndPlace(root, "NpcOpenButton_1298");
        }

        [MenuItem("OLYMPOS/1298/NPC Dükkân Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            Tex("npc_dukkan_krom"); Tex("diyalog_cerceve", new Vector4(20,20,20,20));
            Tex("btn_close"); Tex("btn_confirm"); Tex("btn_cancel");
            AssetDatabase.Refresh();
            Slab = LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf");

            var root = NewRoot("NpcShopWindow_1298", W, H);
            var win = root.AddComponent<OlymposNpcShopWindow>();

            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true;
            win.background = bg;

            // Krom: cerceve, baslik cubugu, bos slotlar, oklar, onay kutusu, dugme, etiketler
            var krom = Img(root, "Krom", "npc_dukkan_krom", 0, 0, W, H);
            krom.raycastTarget = false;

            // Ikonlar kromun USTUNDE olmali: slot zeminleri opak.
            // NOT: secim vurgusu OLUSTURULMUYOR. Oyunda coklu satista secili slotu
            // isaretleyen gorsel bir durum yok (kullanici dogruladi). Kendi geri
            // bildirimini eklemek isteyen slotSelection / invSelection dizilerini doldurur.
            for (int r = 0; r < OlymposNpcShopWindow.Satir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.Sutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.Sutun + c;
                    float sx = X(SX0 + SPX * c), sy = Y(SY0 + SPY * r);
                    var ikon = Img(root, "Icon_" + i, null, sx + 4, sy + 4, SW - 8, SH - 8);
                    ikon.enabled = false; win.slotIcons[i] = ikon;
                }
            for (int r = 0; r < OlymposNpcShopWindow.EnvSatir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.EnvSutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.EnvSutun + c;
                    float sx = X(IX0 + IPX * c), sy = Y(IY0 + IPY * r);
                    var ikon = Img(root, "InvIcon_" + i, null, sx + 4, sy + 4, IW - 8, IH - 8);
                    ikon.enabled = false; win.invIcons[i] = ikon;
                }

            // Tiklama alanlari ve yazilar kromun USTUNDE
            for (int r = 0; r < OlymposNpcShopWindow.Satir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.Sutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.Sutun + c;
                    win.slotButtons[i] = Hit(root, "Slot_" + i, X(SX0 + SPX * c), Y(SY0 + SPY * r), SW, SH);
                }
            for (int r = 0; r < OlymposNpcShopWindow.EnvSatir; r++)
                for (int c = 0; c < OlymposNpcShopWindow.EnvSutun; c++)
                {
                    int i = r * OlymposNpcShopWindow.EnvSutun + c;
                    float sx = X(IX0 + IPX * c), sy = Y(IY0 + IPY * r);
                    win.invButtons[i] = Hit(root, "InvSlot_" + i, sx, sy, IW, IH);
                    var say = Txt(root, "InvCount_" + i, "", sx + 4, sy + IH - 26, IW - 8, 22,
                                  16, Beyaz, TextAnchor.LowerRight);
                    say.gameObject.SetActive(false);
                    win.invCounts[i] = say;
                }

            win.titleText = Txt(root, "Title", "Caspy[Accessory]", 0, 0, W, 74, 47, Altin, TextAnchor.MiddleCenter);
            win.closeButton = Hit(root, "Btn_Close", X(1832), Y(195), 72, 72);

            win.prevPageButton = Hit(root, "Btn_PrevPage", X(1397), Y(692), 65, 50);
            win.nextPageButton = Hit(root, "Btn_NextPage", X(1634), Y(692), 65, 50);
            win.pageText = Txt(root, "PageText", "1/1", X(1490), Y(688), 100, 58, 34, Beyaz, TextAnchor.MiddleCenter);

            win.multipleSellingButton = Hit(root, "Btn_MultipleSelling", X(1199), Y(786), 310, 48);
            var check = Img(root, "MultipleSellingCheck", null, X(1207), Y(794), 29, 29);
            check.color = new Color(0.95f, 0.95f, 0.95f, 0.95f);
            check.enabled = false;
            win.multipleSellingCheck = check;

            win.sellSelectedButton = Hit(root, "Btn_SellSelected", X(1619), Y(784), 275, 50);
            win.totalAmountText = Txt(root, "TotalAmount", "0", X(1700), Y(870), 200, 52, 26, Deger, TextAnchor.MiddleCenter);

            win.tooltip = BuildTooltip(root);
            win.dialog  = BuildDialog(root);

            SaveAndPlace(root, "NpcShopWindow_1298");
        }

        // ------------------------------------------------------------------
        // ------------------------------------------------------------------
        // Ipucu kutusu: icerikle birlikte buyur (VerticalLayoutGroup + ContentSizeFitter).
        // Satir sirasi ekran goruntulerinden: ad · kalite · Buy Price · statlar ·
        // kirmizi statlar · sinif satiri · derece · aciklama · Close
        static OlymposItemTooltip BuildTooltip(GameObject parent)
        {
            var go = new GameObject("Tooltip", typeof(RectTransform));
            Place(go, parent, 120, 120, 420, 10);
            var t = go.AddComponent<OlymposItemTooltip>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, t.backgroundAlpha);
            t.background = bg;

            var vl = go.AddComponent<VerticalLayoutGroup>();
            vl.padding = new RectOffset(18, 18, 16, 16);
            vl.spacing = 6f;
            vl.childAlignment = TextAnchor.UpperCenter;
            vl.childForceExpandWidth = true;
            vl.childForceExpandHeight = false;
            var fit = go.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
            fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            // ust satir: ikon + ad/kalite
            var ust = new GameObject("Ust", typeof(RectTransform));
            Place(ust, go, 0, 0, 384, 74);
            var hl = ust.AddComponent<HorizontalLayoutGroup>();
            hl.spacing = 14f; hl.childForceExpandWidth = false; hl.childForceExpandHeight = false;
            Le(ust, 0, 74);
            var ikon = Img(ust, "Icon", null, 0, 0, 74, 74); Le(ikon.gameObject, 74, 74);
            t.iconImage = ikon;
            var sag = new GameObject("AdKutusu", typeof(RectTransform));
            Place(sag, ust, 0, 0, 290, 74);
            var vl2 = sag.AddComponent<VerticalLayoutGroup>(); vl2.spacing = 2f;
            vl2.childForceExpandWidth = true; vl2.childForceExpandHeight = false;
            Le(sag, 290, 74);
            t.nameText      = Satir(sag, "Name", 34, TextAnchor.LowerLeft, 40);
            t.gradeTypeText = Satir(sag, "GradeType", 24, TextAnchor.UpperLeft, 30);

            t.priceText     = Satir(go, "Price", 30, TextAnchor.MiddleLeft, 40);
            t.statsText     = Satir(go, "Stats", 26, TextAnchor.MiddleLeft, 32);
            t.statsRedText  = Satir(go, "StatsRed", 26, TextAnchor.MiddleLeft, 32);
            t.classText     = Satir(go, "ClassLine", 26, TextAnchor.MiddleCenter, 32);
            t.itemGradeText = Satir(go, "ItemGrade", 26, TextAnchor.MiddleCenter, 32);
            t.descriptionText = Satir(go, "Description", 26, TextAnchor.UpperCenter, 60);
            t.descriptionText.horizontalOverflow = HorizontalWrapMode.Wrap;
            t.statsText.horizontalOverflow = HorizontalWrapMode.Wrap;
            t.statsRedText.horizontalOverflow = HorizontalWrapMode.Wrap;

            var kapat = Img(go, "Btn_Close", "btn_close", 0, 0, 157, 58);
            kapat.raycastTarget = true;
            Le(kapat.gameObject, 157, 58);
            var kb = kapat.gameObject.AddComponent<Button>();
            kb.targetGraphic = kapat; Renkler(kb, true);
            t.closeButton = kb;

            go.SetActive(false);
            return t;
        }

        /// <summary>Ipucundaki tek satir: esnek yukseklikli Text.</summary>
        static Text Satir(GameObject parent, string ad, int punto, TextAnchor hiza, float yukseklik)
        {
            var t = Txt(parent, ad, "", 0, 0, 384, yukseklik, punto, Beyaz, hiza);
            Le(t.gameObject, 0, yukseklik);
            return t;
        }

        static void Le(GameObject go, float w, float h)
        {
            var le = go.AddComponent<LayoutElement>();
            if (w > 0) { le.preferredWidth = w; le.minWidth = w; }
            le.preferredHeight = h; le.minHeight = h;
        }

        // ------------------------------------------------------------------
        static OlymposShopDialog BuildDialog(GameObject parent)
        {
            var go = new GameObject("Dialog", typeof(RectTransform));
            Place(go, parent, X(1224), Y(672), 642, 254);
            var d = go.AddComponent<OlymposShopDialog>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, d.backgroundAlpha);
            bg.raycastTarget = true;
            d.background = bg;

            var cer = Img(go, "Cerceve", "diyalog_cerceve", 0, 0, 642, 254);
            cer.type = Image.Type.Sliced;
            d.frame = cer;

            d.titleText = Txt(go, "Title", "", 40, 18, 562, 46, 30, Beyaz, TextAnchor.MiddleCenter);
            d.infoText  = Txt(go, "Info",  "", 40, 64, 562, 42, 30, Beyaz, TextAnchor.MiddleCenter);

            var alan = new GameObject("CountField", typeof(RectTransform));
            Place(alan, go, 112, 112, 418, 44);
            var ai = alan.AddComponent<Image>();
            ai.color = new Color(0.04f, 0.04f, 0.04f, 1f);
            var f = alan.AddComponent<InputField>();
            f.textComponent = Txt(alan, "Text", "1", 10, 0, 398, 44, 26, Deger, TextAnchor.MiddleLeft);
            f.contentType = InputField.ContentType.IntegerNumber;
            f.characterLimit = 6;
            d.countField = f;
            alan.SetActive(false);

            var onay = Img(go, "Btn_Confirm", "btn_confirm", X(1339), Y(837), 195, 45);
            onay.raycastTarget = true;
            var ob = onay.gameObject.AddComponent<Button>(); ob.targetGraphic = onay; Renkler(ob, true);
            d.confirmButton = ob;

            var iptal = Img(go, "Btn_Cancel", "btn_cancel", X(1554), Y(837), 195, 45);
            iptal.raycastTarget = true;
            var ib = iptal.gameObject.AddComponent<Button>(); ib.targetGraphic = iptal; Renkler(ib, true);
            d.cancelButton = ib;

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

        /// <summary>Görünür düğme için renk geçişleri (sprite'ı karartarak).</summary>
        static void Renkler(Button b, bool gorunur)
        {
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor      = Color.white;
            cb.highlightedColor = new Color(1f, 1f, 1f, 0.85f);
            cb.pressedColor     = new Color(0.72f, 0.72f, 0.72f, 1f);
            cb.selectedColor    = Color.white;
            cb.disabledColor    = new Color(1f, 1f, 1f, 0.45f);
            cb.colorMultiplier  = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
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

        static void Tex(string name) { Tex(name, Vector4.zero); }

        static void Tex(string name, Vector4 border)
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
            ti.spriteBorder = border;
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
