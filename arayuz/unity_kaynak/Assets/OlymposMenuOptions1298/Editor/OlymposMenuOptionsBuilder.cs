// OLYMPOS-KO · 1298 Ana menü + OPTIONS pencere kurucu (sadece Editör)
// Menü: OLYMPOS > 1298 > Ana Menü Paneli Oluştur
//       OLYMPOS > 1298 > OPTIONS Penceresi Oluştur
// Ölçüler 2266x1488'lik ekran görüntülerinden alındı (arayuz/03-yeni-pencereler.md);
// pencereler orada göründükleri piksel boyutunda kurulur.
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposMenuOptionsBuilder
    {
        static string Root;

        static readonly string[] SayfaAdlari = {
            "looting", "cospre", "vfx", "game1", "game2", "game3",
            "block", "battle", "pmblock", "hide", "sound"
        };

        // ------------------------------------------------------------------
        [MenuItem("OLYMPOS/1298/Ana Menü Paneli Oluştur")]
        public static void BuildMainMenu()
        {
            Root = FindRoot();
            Tex("ana_menu_cerceve"); Tex("btn_kapat");
            AssetDatabase.Refresh();

            const float W = 321f, H = 989f;
            var root = NewRoot("AnaMenu_1298", W, H);
            var win = root.AddComponent<OlymposMainMenu>();

            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true;
            win.background = bg;

            var frame = new GameObject("Cerceve", typeof(RectTransform));
            Place(frame, root, 0, 0, W, H);
            var fi = frame.AddComponent<Image>();
            fi.sprite = Spr("ana_menu_cerceve");
            fi.raycastTarget = false;

            // 8 düğme: x 17, genişlik 292, yükseklik 72 — üst kenarlar ölçüldü
            float[] tops = { 51f, 170f, 291f, 412f, 534f, 653f, 775f, 896f };
            string[] adlar = { "PowerUpStore", "OpenMerchant", "SlaveMerchant", "SeekingParty",
                               "Options", "Forum", "Discord", "Instagram" };
            for (int i = 0; i < tops.Length; i++)
                win.buttons[i] = Hit(root, "Btn_" + adlar[i], 17, tops[i], 292, 72);

            // Kapat düğmesi: üst kenarın ortasında, çerçeveyi taşarak
            var kapat = new GameObject("Btn_Kapat", typeof(RectTransform));
            Place(kapat, root, W / 2f - 41f, -38f, 82, 84);
            var ki = kapat.AddComponent<Image>();
            ki.sprite = Spr("btn_kapat");
            ki.raycastTarget = true;
            var kb = kapat.AddComponent<Button>();
            kb.targetGraphic = ki;
            Renkler(kb, true);
            win.closeButton = kb;

            SaveAndPlace(root, "AnaMenu_1298");
        }

        // ------------------------------------------------------------------
        [MenuItem("OLYMPOS/1298/OPTIONS Penceresi Oluştur")]
        public static void BuildOptions()
        {
            Root = FindRoot();
            Tex("options_krom"); Tex("btn_kapat");
            for (int i = 0; i < SayfaAdlari.Length; i++)
            {
                Tex(string.Format("menu_{0:00}_{1}_normal", i, SayfaAdlari[i]));
                Tex(string.Format("menu_{0:00}_{1}_secili", i, SayfaAdlari[i]));
                Tex(string.Format("panel_{0:00}_{1}", i, SayfaAdlari[i]));
            }
            AssetDatabase.Refresh();

            const float W = 854f, H = 1171f;
            // Ekran koordinatında pencere kökü (1018,166); aşağıdaki değerler ona göre yerel.
            const float MX = 1034f - 1018f, MW = 278f, MH = 57f;   // sol menü düğmeleri
            const float PX = 1339f - 1018f, PY = 283f - 166f;      // içerik paneli iç alanı
            const float PW = 511f, PH = 909f;

            var root = NewRoot("OptionsWindow_1298", W, H);
            var win = root.AddComponent<OlymposOptionsWindow>();

            var bg = root.AddComponent<Image>();
            bg.sprite = null;
            bg.color = new Color(0f, 0f, 0f, win.backgroundAlpha);
            bg.raycastTarget = true;
            win.background = bg;

            // İçerik sayfaları (kromun altında kalmalı: önce oluşturulur)
            for (int i = 0; i < SayfaAdlari.Length; i++)
            {
                var sayfa = new GameObject("Sayfa_" + SayfaAdlari[i], typeof(RectTransform));
                Place(sayfa, root, PX, PY, PW, PH);
                var si = sayfa.AddComponent<Image>();
                si.sprite = Spr(string.Format("panel_{0:00}_{1}", i, SayfaAdlari[i]));
                si.raycastTarget = false;
                win.pages[i] = sayfa;
            }

            // Sol menü düğmeleri
            for (int i = 0; i < SayfaAdlari.Length; i++)
            {
                float top = (298f + 86f * i) - 166f;
                var go = new GameObject("Menu_" + SayfaAdlari[i], typeof(RectTransform));
                Place(go, root, MX, top, MW, MH);
                var mi = go.AddComponent<Image>();
                mi.sprite = Spr(string.Format("menu_{0:00}_{1}_normal", i, SayfaAdlari[i]));
                mi.raycastTarget = true;
                var mb = go.AddComponent<Button>();
                mb.targetGraphic = mi;
                Renkler(mb, false);
                win.menuButtons[i]  = mb;
                win.menuImages[i]   = mi;
                win.menuNormal[i]   = Spr(string.Format("menu_{0:00}_{1}_normal", i, SayfaAdlari[i]));
                win.menuSelected[i] = Spr(string.Format("menu_{0:00}_{1}_secili", i, SayfaAdlari[i]));
            }

            // Krom: çerçeve, başlık, panel kenarlığı, RESET SETTINGS — her şeyin üstünde
            var krom = new GameObject("Krom", typeof(RectTransform));
            Place(krom, root, 0, 0, W, H);
            var kri = krom.AddComponent<Image>();
            kri.sprite = Spr("options_krom");
            kri.raycastTarget = false;

            win.resetButton = Hit(root, "Btn_ResetSettings", 1457f - 1018f, 1214f - 166f, 322, 56);

            var kapat = new GameObject("Btn_Kapat", typeof(RectTransform));
            Place(kapat, root, 1775f - 1018f, 169f - 166f, 82, 84);
            var ki = kapat.AddComponent<Image>();
            ki.sprite = Spr("btn_kapat");
            ki.raycastTarget = true;
            var kb = kapat.AddComponent<Button>();
            kb.targetGraphic = ki;
            Renkler(kb, true);
            win.closeButton = kb;

            SaveAndPlace(root, "OptionsWindow_1298");
        }

        [MenuItem("OLYMPOS/1298/Menü ve OPTIONS · Doku Ayarlarını Uygula")]
        public static void ConfigureTexturesMenu()
        {
            Root = FindRoot();
            Tex("ana_menu_cerceve"); Tex("btn_kapat"); Tex("options_krom");
            for (int i = 0; i < SayfaAdlari.Length; i++)
            {
                Tex(string.Format("menu_{0:00}_{1}_normal", i, SayfaAdlari[i]));
                Tex(string.Format("menu_{0:00}_{1}_secili", i, SayfaAdlari[i]));
                Tex(string.Format("panel_{0:00}_{1}", i, SayfaAdlari[i]));
            }
            AssetDatabase.Refresh();
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

        // Koordinatlar sol-üst köşeden piksel
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

        static void Renkler(Button b, bool gorunur)
        {
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            if (gorunur)
            {
                cb.normalColor      = Color.white;
                cb.highlightedColor = new Color(1f, 1f, 1f, 0.85f);
                cb.pressedColor     = new Color(0.7f, 0.7f, 0.7f, 1f);
                cb.selectedColor    = Color.white;
                cb.disabledColor    = new Color(1f, 1f, 1f, 0.45f);
            }
            else
            {
                cb.normalColor      = Color.white;
                cb.highlightedColor = new Color(1.0f, 1.0f, 1.0f, 1f);
                cb.pressedColor     = new Color(0.75f, 0.75f, 0.75f, 1f);
                cb.selectedColor    = Color.white;
                cb.disabledColor    = new Color(1f, 1f, 1f, 0.45f);
            }
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
        }

        /// <summary>Görselin üzerinde görünmez tıklama alanı.</summary>
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
            var guids = AssetDatabase.FindAssets("OlymposMenuOptionsBuilder t:MonoScript");
            if (guids.Length > 0)
            {
                string p = AssetDatabase.GUIDToAssetPath(guids[0]).Replace('\\', '/');
                string editorDir = Path.GetDirectoryName(p).Replace('\\', '/');
                return Path.GetDirectoryName(editorDir).Replace('\\', '/');
            }
            return "Assets/OlymposMenuOptions1298";
        }

        static string TexDir { get { return Root + "/Resources/OlymposMenuOptions1298"; } }

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
