// OLYMPOS-KO · 1298 Save Stat Preset + Stat Butonları pencere kurucu (sadece Editör)
// Menü: OLYMPOS > 1298 > Save Stat Preset Penceresi Oluştur
//       OLYMPOS > 1298 > Stat Butonları Penceresi Oluştur
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposStatWindowsBuilder
    {
        static string Root;

        // ------------------------------------------------------------------
        [MenuItem("OLYMPOS/1298/Save Stat Preset Penceresi Oluştur")]
        public static void BuildSaveStatPreset()
        {
            Prepare();
            const float W = 293f, H = 454f;

            var root = NewRoot("SaveStatPreset_1298", W, H);
            var win = root.AddComponent<OlymposSaveStatPresetWindow>();
            var img = root.AddComponent<Image>();
            img.sprite = Spr("save_stat_preset");   // mat zemin, görsel birebir
            img.raycastTarget = true;

            win.closeButton = Hit(root, "Btn_Close", 246, 3, 28, 28);

            Font font = LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf");
            for (int i = 0; i < OlymposSaveStatPresetWindow.SlotCount; i++)
            {
                float oy = 103f * i;
                var slot = new GameObject("Slot_" + (i + 1), typeof(RectTransform));
                Place(slot, root, 0, oy, W, 103);

                win.saveButtons[i]     = Hit(slot, "Btn_Save",     49,  107, 95, 25);
                win.activateButtons[i] = Hit(slot, "Btn_Activate", 148, 107, 95, 25);

                // Orijinal "- Empty -" yazısının üstünü kapatan kutu + yerine yazılacak metin (varsayılan kapalı)
                var cover = new GameObject("EmptyCover", typeof(RectTransform));
                Place(cover, slot, 74, 80, 146, 16);
                var ci = cover.AddComponent<Image>();
                ci.color = new Color(0.016f, 0.016f, 0.016f, 1f);
                ci.raycastTarget = false;
                cover.SetActive(false);
                win.emptyCovers[i] = ci;

                var t = Txt(slot, "StatusText", "- Empty -", 74, 80, 146, 16, font, 12, new Color(0.94f, 0.94f, 0.94f));
                t.gameObject.SetActive(false);
                win.statusTexts[i] = t;
            }

            SaveAndPlace(root, "SaveStatPreset_1298");
        }

        [MenuItem("OLYMPOS/1298/Stat Butonları Penceresi Oluştur")]
        public static void BuildStatButtons()
        {
            Prepare();
            const float W = 197f, H = 243f;

            var root = NewRoot("StatButtons_1298", W, H);
            var win = root.AddComponent<OlymposStatButtonsWindow>();

            // Yarı saydam siyah zemin
            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true;
            win.background = bg;

            // Çerçeve + butonlar (orijinal görsel, içi saydam)
            var frame = new GameObject("Frame", typeof(RectTransform));
            Place(frame, root, 0, 0, W, H);
            var fi = frame.AddComponent<Image>();
            fi.sprite = Spr("stat_buttons_frame");
            fi.raycastTarget = false;

            win.strButton = Hit(root, "Btn_STR", 21, 22,  163, 38);
            win.hpButton  = Hit(root, "Btn_HP",  21, 65,  163, 38);
            win.dexButton = Hit(root, "Btn_DEX", 21, 108, 163, 38);
            win.intButton = Hit(root, "Btn_INT", 21, 151, 163, 38);
            win.mpButton  = Hit(root, "Btn_MP",  21, 194, 163, 38);

            SaveAndPlace(root, "StatButtons_1298");
        }

        [MenuItem("OLYMPOS/1298/Stat Pencereleri · Doku Ayarlarını Uygula")]
        public static void ConfigureTexturesMenu()
        {
            Prepare();
        }

        // ------------------------------------------------------------------
        static void Prepare()
        {
            Root = FindRoot();
            Tex("save_stat_preset");
            Tex("stat_buttons_frame");
            AssetDatabase.Refresh();
        }

        static GameObject NewRoot(string name, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = Vector2.zero;
            return go;
        }

        // Koordinatlar görseldeki gibi SOL-ÜST köşeden piksel
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

        // Görselin üstünde görünmez tıklama alanı; üstüne gelince hafif, basınca belirgin kararır
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
            cb.colorMultiplier  = 1f;
            cb.fadeDuration     = 0.05f;
            b.colors = cb;
            var nav = b.navigation;
            nav.mode = Navigation.Mode.None;
            b.navigation = nav;
            return b;
        }

        static Text Txt(GameObject parent, string name, string text, float x, float y, float w, float h,
                        Font font, int size, Color color)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, x, y, w, h);
            var t = go.AddComponent<Text>();
            t.font = font;
            t.fontSize = size;
            t.color = color;
            t.alignment = TextAnchor.MiddleCenter;
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
            var guids = AssetDatabase.FindAssets("OlymposStatWindowsBuilder t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string editorDir = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(editorDir).Replace('\\', '/');
            }
            return "Assets/OlymposStatWindows1298";
        }

        static string TexDir { get { return Root + "/Resources/OlymposStatWindows1298"; } }

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
    }
}
