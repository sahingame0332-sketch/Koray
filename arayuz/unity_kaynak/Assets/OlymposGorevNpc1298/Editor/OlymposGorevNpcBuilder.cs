// OLYMPOS-KO · 1298 gorev NPC'si — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Görev NPC (QuestList · Görev Detayı · ? Rozeti) Oluştur
// Olculer telefon ekran goruntusunden (2712 x 1220): arayuz/12-gorev-npc.md. Koordinatlar ekran pikseli, sol-ust.
using System.Collections.Generic;
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposGorevNpcBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposGorevNpc1298";
        const string BuilderAdi = "OlymposGorevNpcBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;
        static Font lb;
        static readonly string[] Odul = { "Rapt Bow(+2)", "Stiletto(+2)", "Stiletto(+2)", "Silan Pauldron", "Silan Pad", "Silan Helmet", "Silan Gauntlet", "Silan Boots" };

        [MenuItem("OLYMPOS/1298/Görev NPC (QuestList · Görev Detayı · ? Rozeti) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            var tum = new List<string> { "liste_pencere", "detay_pencere", "portre", "gorev_satiri", "hedef_satiri", "odul_yuvasi", "soru_rozeti", "ikon_hedef" };
            for (int i = 1; i <= 8; i++) tum.Add("ikon_odul_" + i);
            foreach (var t in tum) Tex(t);
            AssetDatabase.Refresh();
            lb = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/LiberationSans-Bold.ttf");

            var kok = new GameObject("GorevNpc_1298", typeof(RectTransform));
            var krt = (RectTransform)kok.transform;
            krt.anchorMin = krt.anchorMax = krt.pivot = new Vector2(0.5f, 0.5f);
            krt.sizeDelta = new Vector2(EW, EH);

            Rozet(kok);
            var detay = Detay(kok);
            var liste = Liste(kok);
            liste.detay = detay;
            detay.gameObject.SetActive(false);
            SaveAndPlace(kok, "GorevNpc_1298");
        }

        // ---------------------------------------------------------------- "?" rozeti 350 x 350, kayitta merkez (985,175)
        static void Rozet(GameObject kok)
        {
            var go = Bos(kok, "SoruRozeti", 985 - 175, 0, 350, 350);
            var im = Img(go, "Gorsel", "soru_rozeti", 0, 0, 350, 350);
            string mp = Root + "/Materials";
            if (!AssetDatabase.IsValidFolder(mp)) AssetDatabase.CreateFolder(Root, "Materials");
            var mat = AssetDatabase.LoadAssetAtPath<Material>(mp + "/UI_OnCarpimli.mat");
            var sh = Shader.Find("Olympos/UI On Carpimli");
            if (mat == null && sh != null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, mp + "/UI_OnCarpimli.mat"); }
            if (sh == null) Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/UI On Carpimli");
            im.material = mat;
            var r = go.AddComponent<OlymposGorevRozeti>(); r.gorsel = im;
        }

        // ---------------------------------------------------------------- QuestList: sprite (1040,372) 642 x 470
        static OlymposGorevListesi Liste(GameObject kok)
        {
            const float X = 1040, Yy = 372;
            var go = Bos(kok, "QuestList", X, Yy, 642, 470);
            var l = go.AddComponent<OlymposGorevListesi>();
            var bg = Img(go, "Background", null, 1056 - X, 388 - Yy, 566, 441); bg.raycastTarget = true; l.background = bg;
            bg.color = new Color(0f, 0f, 0f, l.backgroundAlpha);
            Img(go, "Krom", "liste_pencere", 0, 0, 642, 470);
            l.portre = Img(go, "Portre", "portre", 1181 - 63 - X, 567 - 63 - Yy, 126, 126);
            l.aciklamaText = Txt(go, "Aciklama", "Test NPC Description.", 1272 - X, 512 - Yy, 300, 24, lb, 16, Hex("#DD9344"), TextAnchor.UpperLeft);
            var satir = Hit(go, "GorevSatiri", 1122 - X, 694 - Yy, 468, 82);
            Img(satir.gameObject, "Cerceve", "gorev_satiri", 0, 0, 468, 82);
            var st = Txt(satir.gameObject, "Ad", "Starter Weapon&Armor", 0, 0, 468, 88, lb, 22, Hex("#F6E1E1"), TextAnchor.MiddleCenter);
            Dis(st);
            l.satirSablonu = satir;
            l.kapatButton = Hit(go, "Btn_Kapat", 1580 - X, 390 - Yy, 62, 62);
            var g = OrnekGorev(); l.gorevler = new List<OlymposGorev> { g };
            return l;
        }

        // ---------------------------------------------------------------- detay: sprite (1052,172) 596 x 840
        static OlymposGorevDetayi Detay(GameObject kok)
        {
            const float X = 1052, Yy = 172;
            var go = Bos(kok, "GorevDetayi", X, Yy, 596, 840);
            var d = go.AddComponent<OlymposGorevDetayi>();
            var bg = Img(go, "Background", null, 1070 - X, 187 - Yy, 559, 811); bg.raycastTarget = true; d.background = bg;
            bg.color = new Color(0f, 0f, 0f, d.backgroundAlpha);
            Img(go, "Krom", "detay_pencere", 0, 0, 596, 840);
            d.portre = Img(go, "Portre", "portre", 1181 - 63 - X, 358 - 63 - Yy, 126, 126);
            d.baslikText = Txt(go, "Baslik", "Starter Weapon&Armor", 1334.5f - 200 - X, 218 - 16 - Yy, 400, 32, lb, 19, Hex("#EEDADA"), TextAnchor.MiddleCenter); Dis(d.baslikText);
            d.aciklamaText = Txt(go, "Aciklama", "Kill: 20x Orc Watcher", 1259 - X, 302 - Yy, 310, 24, lb, 16, Hex("#E09869"), TextAnchor.UpperLeft);
            Img(go, "HedefSatiri", "hedef_satiri", 1117 - X, 496 - Yy, 475, 78);
            d.hedefIkon = Img(go, "HedefIkon", "ikon_hedef", 1132 - X, 512 - Yy, 46, 46);
            d.hedefSayi = Txt(go, "HedefSayi", "25", 1132 - X, 536 - Yy, 46, 24, lb, 18, Hex("#EED8D4"), TextAnchor.LowerRight); Dis(d.hedefSayi);
            d.hedefBaslik = Txt(go, "HedefBaslik", "Hunt: Shilan", 1185 - X, 510 - Yy, 390, 22, lb, 16, Hex("#EAD8D8"), TextAnchor.UpperLeft); Dis(d.hedefBaslik);
            d.hedefAciklama = Txt(go, "HedefAciklama", "Shilan öldür.", 1185 - X, 541 - Yy, 390, 22, lb, 16, Hex("#EAD7D7"), TextAnchor.UpperLeft); Dis(d.hedefAciklama);
            for (int i = 0; i < 8; i++)
            {
                float ox = 1128 + 229 * (i % 2) - X, oy = 638 + 76 * (i / 2) - Yy;
                var h = Bos(go, "Odul_" + (i + 1), ox, oy, 228, 74);
                Img(h, "Yuva", "odul_yuvasi", 0, 0, 228, 74);
                d.odulHucreleri[i] = h;
                d.odulIkonlari[i] = Img(h, "Ikon", "ikon_odul_" + (i + 1), 13, 15, 47, 45);
                d.odulAdlari[i] = Txt(h, "Ad", Odul[i], 67, 15, 156, 22, lb, 16, Hex("#E9D6D6"), TextAnchor.UpperLeft); Dis(d.odulAdlari[i]);
            }
            d.kabulButton = Hit(go, "Btn_Accepted", 1153 - X, 958 - Yy, 203, 37);
            d.kabulText = Txt(d.kabulButton.gameObject, "Yazi", "Accepted", 0, 0, 203, 45, lb, 21, Hex("#F0DDDE"), TextAnchor.MiddleCenter); Dis(d.kabulText);
            d.kapatButton = Hit(go, "Btn_Close", 1362 - X, 958 - Yy, 150, 37);
            d.kapatXButton = Hit(go, "Btn_KapatX", 1582 - X, 183 - Yy, 62, 62);
            d.gorev = OrnekGorev();
            return d;
        }

        static OlymposGorev OrnekGorev()
        {
            var g = new OlymposGorev();
            g.hedefler.Add(new OlymposGorevHedefi { ikon = Spr("ikon_hedef"), baslik = "Hunt: Shilan", aciklama = "Shilan öldür.", sayi = 25 });
            for (int i = 0; i < 8; i++) g.oduller.Add(new OlymposGorevOdulu { ikon = Spr("ikon_odul_" + (i + 1)), ad = Odul[i] });
            return g;
        }

        /// <summary>Beyaz yazilarin koyu dis hatti (orijinalde 1 px).</summary>
        static void Dis(Text t)
        {
            var o = t.gameObject.AddComponent<Outline>(); o.effectColor = new Color(0f, 0f, 0f, 0.8f); o.effectDistance = new Vector2(1f, -1f);
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
            ti.alphaIsTransparency = name != "soru_rozeti";      // on-carpimli doku: kenar renkleri korunmali
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
