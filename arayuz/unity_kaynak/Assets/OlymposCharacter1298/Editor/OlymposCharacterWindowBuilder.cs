// OLYMPOS-KO · 1298 Character penceresi kurucu (sadece Editör)
// Menü: OLYMPOS > 1298 > Character Penceresi Oluştur
// - Doku import ayarlarını yapar (Sprite, sıkıştırmasız, 9-slice kenarlar)
// - Pencereyi referans görseldeki piksel koordinatlarıyla kurar (654 x 1030)
// - Prefabs/CharacterWindow_1298.prefab olarak kaydeder ve sahnedeki Canvas'a ekler
//
// PUNTOLAR: Roboto Slab Bold icin olculerek kalibre edildi (orijinal ekran goruntusundeki
// yazi pikselleriyle ortusme en yuksek olan punto secildi). Font yoksa Roboto Bold'a dusulur
// ve bu puntolar hafif sapar. Ayrinti: arayuz/02-font-kalibrasyonu.md
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposCharacterWindowBuilder
    {
        const float W = 654f, H = 1030f;

        // Renkler (referans görselden ölçüldü)
        static readonly Color White     = Hex("#F4F4F4");
        static readonly Color NameYellow= Hex("#F2E79C");
        static readonly Color LabelOrng = Hex("#E2B47C");
        static readonly Color ValueTan  = Hex("#DCB98A");
        static readonly Color StatGreen = Hex("#A6DC3C");
        static readonly Color ResetOrng = Hex("#D98A34");

        static string Root;
        static Font Slab, Sans;

        [MenuItem("OLYMPOS/1298/Character Penceresi Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            ConfigureTextures();

            Slab = LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf");
            Sans = LoadFont("Roboto-Bold.ttf");
            if (LoadFont("RobotoSlab-Bold.ttf") == null)
                Debug.LogWarning("[OLYMPOS] Fonts klasöründe RobotoSlab-Bold.ttf bulunamadı. Etiketler geçici olarak Roboto-Bold ile yazıldı. " +
                                 "RobotoSlab-Bold.ttf dosyasını " + Root + "/Fonts/ içine koyup menüyü tekrar çalıştırın.");

            var go = BuildWindow();

            string prefabDir = Root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(prefabDir)) AssetDatabase.CreateFolder(Root, "Prefabs");
            string prefabPath = prefabDir + "/CharacterWindow_1298.prefab";
            var prefab = PrefabUtility.SaveAsPrefabAsset(go, prefabPath);
            Object.DestroyImmediate(go);

            var canvas = EnsureCanvas();
            var inst = (GameObject)PrefabUtility.InstantiatePrefab(prefab, canvas.transform);
            Undo.RegisterCreatedObjectUndo(inst, "Create OLYMPOS Character Window");
            Selection.activeGameObject = inst;
            Debug.Log("[OLYMPOS] Character penceresi oluşturuldu: " + prefabPath);
        }

        [MenuItem("OLYMPOS/1298/Sadece Doku Ayarlarını Uygula")]
        public static void ConfigureTexturesMenu()
        {
            Root = FindRoot();
            ConfigureTextures();
        }

        // ------------------------------------------------------------------
        static GameObject BuildWindow()
        {
            var root = new GameObject("CharacterWindow_1298", typeof(RectTransform));
            var rt = (RectTransform)root.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(W, H);
            rt.anchoredPosition = Vector2.zero;

            var win = root.AddComponent<OlymposCharacterWindow>();

            // Zemin: düz siyah, yarı saydam. Alfa orijinalden ölçüldü (0.92) — bkz. arayuz/04-saydamlik.md
            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true; // arkadaki dünyaya tıklamayı engeller
            win.background = bg;

            // Bronz çerçeve (içi tamamen saydam)
            Img(root, "Frame", "window_frame", 0, 0, W, H, false);

            // ---- Sekmeler ----
            Img(root, "TabsStrip", "tabs_strip", 9, 8, 637, 92, false);
            win.tabCharInfo = Tab(root, "Tab_CharInfo", "CHAR INFO", 15, 10, 200, 82);
            win.tabQuests   = Tab(root, "Tab_Quests",   "QUESTS",   224, 10, 128, 82);
            win.tabClan     = Tab(root, "Tab_Clan",     "CLAN",     365, 10, 156, 82);
            win.tabFriends  = Tab(root, "Tab_Friends",  "FRIENDS",  525, 10, 120, 82);

            // ---- Irk & isim ----
            win.raceIcon = Img(root, "RaceIcon", "race_human", 64, 116, 57, 57, false);
            win.raceText = Txt(root, "RaceText", "HUMAN", 40, 172, 104, 26, Slab, 20, White, TextAnchor.MiddleCenter);
            win.nameText = Txt(root, "NameText", "xDarKPasT", 174, 126, 320, 34, Slab, 25, NameYellow, TextAnchor.MiddleLeft);

            // ---- Level / Job / HP / MP ----
            Label(root, "Lbl_Level", "Level", 38, 235, 81, White);
            win.levelText = Box(root, "Box_Level", "72", 128, 224, 93, 51, Sans, 21, White);
            Label(root, "Lbl_HP", "HP Point", 228, 235, 121, White);
            win.hpText = Box(root, "Box_HP", "1.673 / 1.673", 363, 224, 240, 48, Sans, 22, White);

            Label(root, "Lbl_Job", "Job", 38, 291, 81, White);
            win.jobText = Box(root, "Box_Job", "Magician", 122, 280, 99, 51, Slab, 22, White);
            Label(root, "Lbl_MP", "MP Point", 228, 291, 121, White);
            win.mpText = Box(root, "Box_MP", "3.417 / 3.417", 363, 281, 240, 48, Sans, 22, White);

            // ---- Exp / NP ----
            Label(root, "Lbl_Exp", "Exp Points", 47, 371, 152, LabelOrng);
            win.expText = Box(root, "Box_Exp", "0 / 7.049.084.376", 216, 358, 392, 53, Sans, 22, ValueTan);
            Label(root, "Lbl_NP", "NP Points", 47, 434, 152, LabelOrng);
            win.npText = Box(root, "Box_NP", "2.077.085 / 935.170", 216, 422, 392, 52, Sans, 22, ValueTan);

            // ---- Attack / Defence ----
            Label(root, "Lbl_Attack", "Attack", 47, 525, 122, LabelOrng);
            win.attackText = Box(root, "Box_Attack", "5", 178, 513, 149, 52, Sans, 21, White);
            Label(root, "Lbl_Defence", "Defence", 345, 525, 122, LabelOrng);
            win.defenceText = Box(root, "Box_Defence", "182", 484, 513, 124, 52, Sans, 21, White);

            // ---- Stat puanları ----
            var sp = Label(root, "Lbl_StatPoints", "Your Stat Points", 48, 584, 239, White);
            win.statPointsText = Txt(sp, "Value", "0", 205, 0, 30, 30, Slab, 21, StatGreen, TextAnchor.MiddleLeft);

            win.strText   = Stat(root, "Stat_STR", "STR", "50",  49, 619, 18, 137);
            win.dexText   = Stat(root, "Stat_DEX", "DEX", "70",  49, 678, 16, 137);
            win.intText   = Stat(root, "Stat_INT", "INT", "112", 49, 735, 20, 132);
            win.hpStatText= Stat(root, "Stat_HP",  "HP",  "52",  372, 619, 26, 144);
            win.mpStatText= Stat(root, "Stat_MP",  "MP",  "255", 372, 678, 24, 138);

            win.statPresetButton = Btn(root, "Btn_StatPreset", "btn_preset", "Stat  Preset", 456, 742, White);

            // ---- Dirençler ----
            Label(root, "Lbl_Resistance", "Resistance", 50, 858, 138, White);
            win.statResetButton = Btn(root, "Btn_StatReset", "btn_reset", "Stat Reset", 456, 849, ResetOrng);

            win.flameText     = Resist(root, "Res_Flame",     "Flame Resist.",     46,  903, 272, 48, 226);
            win.poisonText    = Resist(root, "Res_Poison",    "Poison Resist.",    340, 903, 270, 46, 228);
            win.glacierText   = Resist(root, "Res_Glacier",   "Glacier Resist.",   46,  960, 272, 44, 226);
            win.lightningText = Resist(root, "Res_Lightning", "Lightning Resist.", 340, 960, 270, 46, 228);

            return root;
        }

        // ------------------------------------------------------------------
        // Yardımcılar: tüm koordinatlar referans görseldeki gibi SOL-ÜST köşeden piksel
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

        static Image Img(GameObject parent, string name, string sprite, float x, float y, float w, float h, bool sliced)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var img = go.AddComponent<Image>();
            img.sprite = Spr(sprite);
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.raycastTarget = false;
            return img;
        }

        static Text Txt(GameObject parent, string name, string text, float x, float y, float w, float h,
                        Font font, int size, Color color, TextAnchor anchor)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var t = go.AddComponent<Text>();
            t.font = font;
            t.fontSize = size;
            t.fontStyle = FontStyle.Normal;
            t.color = color;
            t.alignment = anchor;
            t.text = text;
            t.supportRichText = false;
            t.horizontalOverflow = HorizontalWrapMode.Overflow;
            t.verticalOverflow = VerticalWrapMode.Overflow;
            t.raycastTarget = false;
            var sh = go.AddComponent<Shadow>();
            sh.effectColor = new Color(0f, 0f, 0f, 0.9f);
            sh.effectDistance = new Vector2(1f, -1f);
            return t;
        }

        static Button Tab(GameObject parent, string name, string text, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var hit = go.AddComponent<Image>();
            hit.color = new Color(1f, 1f, 1f, 0f); // görünmez tıklama alanı; zemin TabsStrip'te
            var b = go.AddComponent<Button>();
            b.targetGraphic = hit;
            b.transition = Selectable.Transition.None;
            Txt(go, "Text", text, 0, 0, w, h, Slab, 21, White, TextAnchor.MiddleCenter);
            return b;
        }

        static GameObject Label(GameObject parent, string name, string text, float x, float y, float w, Color color)
        {
            var img = Img(parent, name, "label_button", x, y, w, 30, true);
            Txt(img.gameObject, "Text", text, 17, 0, w - 17, 30, Slab, 21, color, TextAnchor.MiddleLeft);
            return img.gameObject;
        }

        static Text Box(GameObject parent, string name, string value, float x, float y, float w, float h,
                        Font font, int size, Color color)
        {
            var img = Img(parent, name, "value_box", x, y, w, h, true);
            return Txt(img.gameObject, "Value", value, 0, 0, w, h, font, size, color, TextAnchor.MiddleCenter);
        }

        static Text Stat(GameObject parent, string name, string key, string value, float x, float y, float keyX, float valX)
        {
            var img = Img(parent, name, "value_box", x, y, 238, 51, true);
            Txt(img.gameObject, "Key", key, keyX, 0, 80, 51, Slab, 21, White, TextAnchor.MiddleLeft);
            return Txt(img.gameObject, "Value", value, valX, 0, 80, 51, Slab, 25, ValueTan, TextAnchor.MiddleLeft);
        }

        static Text Resist(GameObject parent, string name, string key, float x, float y, float w, float keyX, float valX)
        {
            var img = Img(parent, name, "value_box", x, y, w, 53, true);
            Txt(img.gameObject, "Key", key, keyX, 0, 180, 53, Slab, 19, White, TextAnchor.MiddleLeft);
            return Txt(img.gameObject, "Value", "0", valX, 0, 40, 53, Slab, 23, ValueTan, TextAnchor.MiddleLeft);
        }

        static Button Btn(GameObject parent, string name, string sprite, string text, float x, float y, Color color)
        {
            var img = Img(parent, name, sprite, x, y, 145, 45, false);
            img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>();
            b.targetGraphic = img;
            Txt(img.gameObject, "Text", text, 0, 0, 145, 45, Slab, 22, color, TextAnchor.MiddleCenter);
            return b;
        }

        // ------------------------------------------------------------------
        static string FindRoot()
        {
            var guids = AssetDatabase.FindAssets("OlymposCharacterWindowBuilder t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string editorDir = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(editorDir).Replace('\\', '/');
            }
            return "Assets/OlymposCharacter1298";
        }

        static string TexDir { get { return Root + "/Resources/OlymposCharacter1298"; } }

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

        static void ConfigureTextures()
        {
            // 9-slice kenarları: (sol, alt, sağ, üst)
            Tex("window_frame", Vector4.zero);
            Tex("tabs_strip",   Vector4.zero);
            Tex("race_human",   Vector4.zero);
            Tex("label_button", new Vector4(18, 8, 8, 8));
            Tex("value_box",    new Vector4(6, 6, 6, 6));
            Tex("btn_preset",   new Vector4(6, 6, 6, 6));
            Tex("btn_reset",    new Vector4(6, 6, 6, 6));
            AssetDatabase.Refresh();
        }

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

        static Color Hex(string h)
        {
            Color c;
            ColorUtility.TryParseHtmlString(h, out c);
            return c;
        }
    }
}
