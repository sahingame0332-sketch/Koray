// OLYMPOS-KO · 1298 Knight Genie — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Genie (Panel · Auto Attack Settings · Rozet) Oluştur
// Olculer telefon ekran goruntusunden (2712 x 1220): arayuz/11-genie.md. Butun koordinatlar ekran pikseli, sol-ust.
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposGenieBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposGenie1298";
        const string BuilderAdi = "OlymposGenieBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;
        static Font slabB, slabR;

        [MenuItem("OLYMPOS/1298/Genie (Panel · Auto Attack Settings · Rozet) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            foreach (var t in new[] { "genie_panel", "aa_pencere", "aa_topuz", "aa_onay", "aa_etiketler", "genie_kilit", "genie_rozet" }) Tex(t);
            AssetDatabase.Refresh();
            slabB = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Bold.ttf");
            slabR = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Regular.otf");

            var kok = new GameObject("Genie_1298", typeof(RectTransform));
            var krt = (RectTransform)kok.transform;
            krt.anchorMin = krt.anchorMax = krt.pivot = new Vector2(0.5f, 0.5f);
            krt.sizeDelta = new Vector2(EW, EH);

            var rozet = Rozet(kok);
            var pencere = Pencere(kok);
            var panel = Panel(kok);
            panel.ayarPenceresi = pencere; panel.rozet = rozet; panel.kilitSprite = Spr("genie_kilit");
            pencere.gameObject.SetActive(false);
            rozet.gameObject.SetActive(false);
            SaveAndPlace(kok, "Genie_1298");
        }

        // ---------------------------------------------------------------- Knight Genie paneli (2308,50) 356 x 246
        static OlymposGeniePaneli Panel(GameObject kok)
        {
            var go = Bos(kok, "KnightGeniePaneli", 2308, 50, 356, 246);
            Img(go, "Krom", "genie_panel", 0, 0, 356, 246);
            var p = go.AddComponent<OlymposGeniePaneli>();
            const float X = 2308, Yy = 50;
            p.baslatButton = Hit(go, "Btn_Baslat", 2350 - X, 61 - Yy, 70, 66);
            p.durdurButton = Hit(go, "Btn_Durdur", 2425 - X, 61 - Yy, 70, 66);
            p.ayarButton = Hit(go, "Btn_Ayarlar", 2500 - X, 61 - Yy, 68, 66);
            // Time Left: Roboto Slab Regular 18, #FFFCEA, koyu dis hat; murek merkezi (2502, 137.5)
            p.sureText = Txt(go, "TimeLeft", "Time Left : 244 Minute(s)", 2502 - 160 - X, 137.5f - 14 - Yy, 320, 28, slabR, 18, Hex("#FFFCEA"), TextAnchor.MiddleCenter);
            var ol = p.sureText.gameObject.AddComponent<Outline>(); ol.effectColor = new Color(0.16f, 0.08f, 0f, 0.9f); ol.effectDistance = new Vector2(1f, -1f);
            // sunucu: Roboto Slab Bold 21 #AFEB9F, ortali (2500.5, 170)
            p.sunucuText = Txt(go, "Sunucu", "Ares - 1", 2500.5f - 150 - X, 170 - 18 - Yy, 300, 36, slabB, 21, Hex("#AFEB9F"), TextAnchor.MiddleCenter);
            // CR / kanal: Roboto Slab Bold 23, sola yasli x=2393
            p.crText = Txt(go, "CR", "CR : 01:18:08", 2393 - X, 214 - 18 - Yy, 255, 36, slabB, 23, Hex("#DCF19E"), TextAnchor.MiddleLeft);
            p.kanalText = Txt(go, "Kanal", "Channel 2", 2393 - X, 266.5f - 18 - Yy, 255, 36, slabB, 23, Hex("#EEF4EF"), TextAnchor.MiddleLeft);
            return p;
        }

        // ---------------------------------------------------------------- AUTO ATTACK SETTINGS: sprite (262,30) 636 x 1162
        static readonly float[] SlotX = { 322, 410, 497, 585, 672, 760 };
        static readonly float[] IzY = { 762, 840, 919, 997 };
        static readonly float[] TopuzUst = { 733, 811, 889, 967 };

        static OlymposGenieAyarPenceresi Pencere(GameObject kok)
        {
            const float X = 262, Yy = 30;
            var go = Bos(kok, "AutoAttackSettings", X, Yy, 636, 1162);
            var a = go.AddComponent<OlymposGenieAyarPenceresi>();
            var bg = Img(go, "Background", null, 273 - X, 44 - Yy, 604, 1108);
            bg.raycastTarget = true; a.background = bg; bg.color = new Color(0f, 0f, 0f, a.backgroundAlpha);
            Img(go, "Krom", "aa_pencere", 0, 0, 636, 1162);

            // slotlar 80 x 77, ikon alani icte 62 x 59
            a.saldiriSlotlari = Slotlar(go, "Saldiri", new float[] { 200, 288 }, X, Yy);
            a.destekSlotlari = Slotlar(go, "Destek", new float[] { 458, 547 }, X, Yy);
            a.iksirSlotlari = new Image[2];
            float[] ix = { 562, 649 };
            for (int i = 0; i < 2; i++)
            {
                var b = Hit(go, i == 0 ? "Iksir_HP" : "Iksir_MP", ix[i] - X, 655 - Yy, 67, 67);
                a.iksirSlotlari[i] = Ikon(b.gameObject, 5, 5, 57, 57);
            }

            // kaydiricilar: iz 357..760; topuz merkezi = 363.5 + p*405 ; deger yazisi Roboto Slab Bold 24 #D2A776, merkez x=818
            string[] ad = { "AttackRange", "SkillRecovery", "HpPotion", "MpPotion" };
            int[] enCok = { 45, 100, 100, 100 }; int[] dv = { 40, 70, 80, 50 };
            var k = new OlymposGenieKaydirici[4];
            for (int i = 0; i < 4; i++)
            {
                var hgo = new GameObject("Kaydirici_" + ad[i], typeof(RectTransform));
                Place(hgo, go, 330 - X, IzY[i] - 40 - Yy, 460, 80);
                var him = hgo.AddComponent<Image>(); him.color = new Color(0f, 0f, 0f, 0f); him.raycastTarget = true;
                var ks = hgo.AddComponent<OlymposGenieKaydirici>();
                var t = Img(hgo, "Topuz", "aa_topuz", 0, TopuzUst[i] - (IzY[i] - 40), 21, 73);
                t.rectTransform.pivot = new Vector2(0.5f, 1f);
                ks.topuz = t.rectTransform; ks.izBasi = 363.5f - 330f; ks.izBoyu = 405f;
                ks.degerText = Txt(go, "Deger_" + ad[i], "", 818 - 40 - X, IzY[i] + 7 - 18 - Yy, 80, 36, slabB, 24, Hex("#D2A776"), TextAnchor.MiddleCenter);
                ks.bicim = i == 0 ? "{0}" : "%{0}"; ks.enAz = 0; ks.enCok = enCok[i]; ks.deger = dv[i];
                k[i] = ks;
            }
            a.saldiriMenzili = k[0]; a.skillYenileme = k[1]; a.hpIksiri = k[2]; a.mpIksiri = k[3];
            // kaydirici etiketleri orijinalde topuzun USTUNDE: ayri katman
            Img(go, "KaydiriciEtiketleri", "aa_etiketler", 0, 0, 636, 1162);

            // onay kutulari: kutu (bx,by) 43 x 40 ; isaret sprite'i (604,1028) 60 x 54 (3. kutuya gore)
            float[,] kut = { { 328, 1036 }, { 328, 1090 }, { 612, 1036 }, { 612, 1090 } };
            string[] oad = { "BasicAttack", "FollowPartyLeader", "UseGenieSprit", "SkillUseInOrder" };
            var o = new OlymposGenieOnay[4];
            for (int i = 0; i < 4; i++)
            {
                var b = Hit(go, "Onay_" + oad[i], kut[i, 0] - X - 4, kut[i, 1] - Yy - 6, 252, 52);
                var on = b.gameObject.AddComponent<OlymposGenieOnay>();
                on.button = b;
                on.isaret = Img(go, "Isaret_" + oad[i], "aa_onay", 604 + kut[i, 0] - 612 - X, 1028 + kut[i, 1] - 1036 - Yy, 60, 54);
                on.isaretli = i == 2;                     // ekran goruntusu: yalniz "Use Genie Sprit" isaretli
                o[i] = on;
            }
            a.temelSaldiri = o[0]; a.partiLideri = o[1]; a.genieSpirit = o[2]; a.sirayla = o[3];
            a.kapatButton = Hit(go, "Btn_Kapat", 816 - X, 45 - Yy, 74, 74);
            return a;
        }

        static Image[] Slotlar(GameObject go, string ad, float[] satirY, float X, float Yy)
        {
            var d = new Image[12];
            for (int r = 0; r < 2; r++)
                for (int c = 0; c < 6; c++)
                {
                    var b = Hit(go, ad + "_" + (r * 6 + c + 1), SlotX[c] - X, satirY[r] - Yy, 80, 77);
                    d[r * 6 + c] = Ikon(b.gameObject, 9, 9, 62, 59);
                }
            return d;
        }

        static Image Ikon(GameObject parent, float x, float y, float w, float h)
        {
            var im = Img(parent, "Ikon", null, x, y, w, h);
            im.color = new Color(1f, 1f, 1f, 0f); im.preserveAspect = false;
            return im;
        }

        // ---------------------------------------------------------------- GENIE rozeti 300 x 300, kayitta merkez (1355,375)
        static OlymposGenieRozeti Rozet(GameObject kok)
        {
            var go = Bos(kok, "GenieRozeti", 1355 - 150, 375 - 150, 300, 300);
            var im = Img(go, "Gorsel", "genie_rozet", 0, 0, 300, 300);
            var r = go.AddComponent<OlymposGenieRozeti>(); r.gorsel = im;
            return r;
        }

        // ---------------------------------------------------------------- yardimcilar
        static GameObject Bos(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform)); Place(go, parent, x, y, w, h); return go;
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
