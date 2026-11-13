// OLYMPOS-KO · 1298 Merchant — alici gorunumu · kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Merchant Alıcı Görünümü Oluştur
// Baska oyuncunun tezgah cubugu (satici adi + mor cerceveli yuvalar + OPEN / WHISPER) ve "<ad> Merchant" penceresi.
// Olculer 2712 x 1220 ekran goruntulerinden — arayuz/09-merchant.md ("Alici gorunumu" eki)
using System.Collections.Generic;
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposMerchantAliciBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposMerchantAlici1298";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";

        static readonly Color Beyaz = Color.white, Pembe = Hex("#FFE7E9"), Etiket = Hex("#CA89E2"), Altin = Hex("#DDA96A");
        static string Root;
        static Font Roboto, SlabInce, DejaVu;

        [MenuItem("OLYMPOS/1298/Merchant Alıcı Görünümü Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            foreach (var d in new[] { "tezgah_krom", "mpencere_krom", "yuva_dolu_tezgah", "yuva_dolu_mp_ust", "yuva_dolu_mp_env",
                                      "yuva_mor_tezgah", "yuva_mor_mp_ust", "ikon_yay", "ikon_balta", "ikon_parsomen_sureli_3" }) Tex(d);
            AssetDatabase.Refresh();
            Roboto = LoadFont("Roboto-Bold.ttf");
            SlabInce = LoadFont("RobotoSlab-Regular.otf") ?? Roboto;
            DejaVu = LoadFont("DejaVuSans-Bold.ttf") ?? Roboto;

            var root = new GameObject("MerchantAlici_1298", typeof(RectTransform));
            var rrt = (RectTransform)root.transform;
            rrt.anchorMin = Vector2.zero; rrt.anchorMax = Vector2.one;
            rrt.offsetMin = Vector2.zero; rrt.offsetMax = Vector2.zero;

            var cubuk = BuildCubuk(root);
            var pencere = BuildPencere(root);
            cubuk.pencere = pencere;

            // ekran goruntulerindeki ornek: Itccc'nin tezgahi (6 yay + 4 balta + 2 yay, hepsi +1 ve mor cerceveli),
            // alicinin parasi 9,322 ve envanterinde sureli bir parsomen (adet rakami "3" ikonun pikselinde)
            cubuk.saticiAdi = "Itccc";
            var yay = Spr("ikon_yay"); var balta = Spr("ikon_balta");
            for (int i = 0; i < 12; i++)
            {
                bool b = i >= 6 && i < 10;
                cubuk.tezgah.Add(new OlymposSaticiEsyasi { ad = b ? "Ornek balta(+1)" : "Ornek yay(+1)", ikon = b ? balta : yay, yukseltme = 1, morCerceve = true });
            }
            pencere.para = 9322;
            for (int i = 0; i < 5; i++) pencere.envanter.Add(new OlymposSaticiEsyasi());
            pencere.envanter.Add(new OlymposSaticiEsyasi { ad = "Ornek sureli parsomen", ikon = Spr("ikon_parsomen_sureli_3"), adet = 1 });

            SaveAndPlace(root, "MerchantAlici_1298");
        }

        // =====================================================================
        // Tezgah cubugu — sprite 404 x 168 ; ekran goruntusunde (955, 241)
        static OlymposSaticiCubugu BuildCubuk(GameObject parent)
        {
            var go = Kutu(parent, "TezgahCubugu", 955, 241, 404, 168);
            var c = go.AddComponent<OlymposSaticiCubugu>();
            for (int i = 0; i < 4; i++)
            {
                var z = Img(go, "YuvaZemini_" + i, null, 35 + 86f * i, 17, 70, 72);
                z.color = new Color(0f, 0f, 0f, c.yuvaAlpha);
                c.yuvaZeminleri[i] = z;
            }
            Img(go, "Krom", "tezgah_krom", 0, 0, 404, 168);          // cerceve + OPEN / WHISPER orijinal piksellerden
            // yuva 86 x 88 ; ikon: gumus cercevede (8,8) 70 x 72, mor cercevede (16,12) 62 x 66 ; "+N": punto 31, sag kenar 78, ust 13
            for (int i = 0; i < 4; i++)
                c.yuvalar[i] = Yuva(go, "Yuva_" + i, 27 + 86f * i, 9, 86, 88, "yuva_dolu_tezgah", "yuva_mor_tezgah",
                                    new Vector4(8, 8, 70, 72), new Vector4(16, 12, 62, 66), 31, 78, 13);
            c.openButton = Hit(go, "Btn_Open", 23, 104, 179, 60);
            c.whisperButton = Hit(go, "Btn_Whisper", 202, 104, 178, 60);

            // satici adi: DejaVu Sans Bold 30, beyaz, 2 px siyah dis hat ; merkez x = 197.5, murek ust kenari cubugun 35 px ustu
            var ad = Txt(go, "SellerName", "Itccc", 197.5f - 300f, -45, 600, 40, DejaVu, 30, Beyaz, TextAnchor.MiddleCenter);
            var o = ad.gameObject.AddComponent<Outline>();
            o.effectColor = new Color(0f, 0f, 0f, 0.95f); o.effectDistance = new Vector2(2f, -2f);
            c.adText = ad;
            return c;
        }

        // =====================================================================
        // "<ad> Merchant" — sprite (945, 113) 785 x 987 ; zemin alfa 0.89
        static OlymposSaticiPenceresi BuildPencere(GameObject parent)
        {
            var go = Kutu(parent, "MerchantPenceresi", 945, 113, 785, 987);
            var p = go.AddComponent<OlymposSaticiPenceresi>();
            p.titleBackground = Zemin(go, "TitleBackground", 13, 9, 762, 48, p.backgroundAlpha);
            p.background = Zemin(go, "Background", 7, 59, 770, 905, p.backgroundAlpha);
            Img(go, "Krom", "mpencere_krom", 0, 0, 785, 987);        // cerceve, bos yuvalar, para ikonu, OK / Cancel orijinal piksellerden
            // baslik: Roboto Slab Regular 33, #DDA96A, ortali ; para: Roboto Bold 36, beyaz, sag kenar x = 673
            p.titleText = Txt(go, "Title", "Itccc Merchant", 0, 5, 781, 50, SlabInce, 33, Altin, TextAnchor.MiddleCenter);
            p.goldText = Txt(go, "Gold", "9,322", 373, 413, 300, 50, Roboto, 36, Beyaz, TextAnchor.MiddleRight);
            // tezgah 6 x 2 : yuva 117 x 114 ; ikon gumuste (8,8) 101 x 98, morda (12,12) 93 x 90 ; "+N": punto 25, sag kenar 110, ust 11
            for (int r = 0; r < 2; r++)
                for (int k = 0; k < 6; k++)
                    p.tezgahYuvalari[r * 6 + k] = Yuva(go, "Tezgah_" + (r * 6 + k), 29.7f + 120.31f * k, 115.8f + 121.17f * r, 117, 114,
                                                      "yuva_dolu_mp_ust", "yuva_mor_mp_ust", new Vector4(8, 8, 101, 98), new Vector4(12, 12, 93, 90), 25, 110, 11);
            // envanter 7 x 4 : yuva 104 x 102 ; ikon (8,8) 88 x 86 (mor cerceve bu izgarada gorulmedi)
            for (int r = 0; r < 4; r++)
                for (int k = 0; k < 7; k++)
                    p.envanterYuvalari[r * 7 + k] = Yuva(go, "Envanter_" + (r * 7 + k), 22.8f + 103.64f * k, 475.9f + 104.4f * r, 104, 102,
                                                        "yuva_dolu_mp_env", null, new Vector4(8, 8, 88, 86), new Vector4(8, 8, 88, 86), 28, 94, 11);
            p.okButton = Hit(go, "Btn_OK", 210, 920, 163, 56);
            p.cancelButton = Hit(go, "Btn_Cancel", 407, 920, 157, 56);
            go.SetActive(false);
            return p;
        }

        // =====================================================================
        // yardimcilar
        static OlymposSaticiYuvasi Yuva(GameObject parent, string name, float x, float y, float w, float h, string dolu, string mor,
                                        Vector4 normalKutu, Vector4 morKutu, int etiketPunto, float etiketSag, float etiketUst)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, Mathf.Round(x), Mathf.Round(y), w, h);
            var tik = go.AddComponent<Image>(); tik.color = new Color(0f, 0f, 0f, 0f); tik.raycastTarget = true;
            var yv = go.AddComponent<OlymposSaticiYuvasi>();
            yv.dugme = go.AddComponent<Button>(); yv.dugme.targetGraphic = tik; yv.dugme.transition = Selectable.Transition.None;
            yv.normalIkonKutusu = normalKutu; yv.morIkonKutusu = morKutu;
            yv.ikon = Img(go, "Icon", null, normalKutu.x, normalKutu.y, normalKutu.z, normalKutu.w);
            yv.ikon.enabled = false;
            yv.doluCerceve = Img(go, "FilledFrame", dolu, 0, 0, w, h);
            yv.doluCerceve.enabled = false;
            if (!string.IsNullOrEmpty(mor))
            {
                yv.morCerceve = Img(go, "PurpleFrame", mor, 0, 0, w, h);
                yv.morCerceve.enabled = false;
            }
            // "+N": mor #CA89E2, Roboto Bold ; orijinalde biraz daha kalin -> ayni renkte ince dis hat
            yv.yukseltmeText = Txt(go, "Upgrade", "", etiketSag - 120, etiketUst - etiketPunto * 0.14f, 120, etiketPunto + 6, Roboto, etiketPunto, Etiket, TextAnchor.UpperRight);
            var eo = yv.yukseltmeText.gameObject.AddComponent<Outline>();
            eo.effectColor = Etiket; eo.effectDistance = new Vector2(0.5f, -0.5f);
            int p2 = Mathf.RoundToInt(h * 0.27f);
            yv.adetText = Txt(go, "Count", "", 0, h - 8 - (p2 + 6), w - 11, p2 + 6, Roboto, p2, Pembe, TextAnchor.LowerRight);
            var ao = yv.adetText.gameObject.AddComponent<Outline>();
            ao.effectColor = new Color(0f, 0f, 0f, 0.95f); ao.effectDistance = new Vector2(1f, -1f);
            yv.yukseltmeText.gameObject.SetActive(false); yv.adetText.gameObject.SetActive(false);
            return yv;
        }

        static Image Zemin(GameObject parent, string name, float x, float y, float w, float h, float alfa)
        {
            var img = Img(parent, name, null, x, y, w, h);
            img.color = new Color(0f, 0f, 0f, alfa);
            img.raycastTarget = true;
            return img;
        }

        /// <summary>Ekran pikseli (sol-ust kose) ile yerlesim; ekranin ortasina capalanir.</summary>
        static GameObject Kutu(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent.transform, false);
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = new Vector2(x + w * 0.5f - EW * 0.5f, EH * 0.5f - (y + h * 0.5f));
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
            var rt = (RectTransform)inst.transform;
            rt.anchorMin = Vector2.zero; rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero; rt.offsetMax = Vector2.zero;
            Undo.RegisterCreatedObjectUndo(inst, "Create " + prefabName);
            Selection.activeGameObject = inst;
            Debug.Log("[OLYMPOS] Oluşturuldu: " + path);
        }

        static string FindRoot()
        {
            var guids = AssetDatabase.FindAssets("OlymposMerchantAliciBuilder t:MonoScript");
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
