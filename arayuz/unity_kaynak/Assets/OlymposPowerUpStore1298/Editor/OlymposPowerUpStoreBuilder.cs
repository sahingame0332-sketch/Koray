// OLYMPOS-KO · 1298 Power Up Store — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Power Up Store Oluştur.  Olculer: arayuz/24-powerup-store.md (telefon 2712x1220 ekran pikseli, sol-ust).
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposPowerUpStoreBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposPowerUpStore1298";
        const string BuilderAdi = "OlymposPowerUpStoreBuilder";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";
        static string Root;

        const float MX = 272f;                       // magaza sol kenari (ekran pikseli)

        [MenuItem("OLYMPOS/1298/Power Up Store Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            string[] sek = { "MainPage", "PowerUP", "Premiums", "Scrolls", "Special", "Package" };
            Tex("magaza_zemin"); Tex("kart_kategori"); Tex("kart_ana"); Tex("dugme_kategori_uygun"); Tex("para_ikonu");
            Tex("ayrinti"); Tex("paket_icerik"); Tex("basari"); Tex("cashcode");
            Tex("kaydirma"); Sinir("kaydirma", new Vector4(0f, 10f, 0f, 10f));
            foreach (var s in sek) { Tex("sekme_" + s); Tex("sekme_" + s + "_secili"); }
            AssetDatabase.Refresh();
            var lb = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/LiberationSans-Bold.ttf");
            var rb = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/Roboto-Bold.ttf");

            // ---------------- magaza
            var go = Bos(null, "PowerUpStore_1298", MX, 0, 2137, 1220);
            var p = go.AddComponent<OlymposPowerUpStore>();
            var zem = Img(go, "Zemin", "magaza_zemin", 0, 0, 2137, 1220); zem.raycastTarget = true;
            int[] sy = { 253, 348, 446, 543, 640, 738 };
            for (int i = 0; i < 6; i++)
            {
                p.sekmeler[i] = Img(go, "Sekme_" + sek[i], "sekme_" + sek[i], 50, sy[i], 290, 86);
                p.sekmeNormal[i] = Spr("sekme_" + sek[i]); p.sekmeSecili[i] = Spr("sekme_" + sek[i] + "_secili");
                p.sekmeButonlari[i] = Hit(go, "Btn_" + sek[i], 59, sy[i] + 6, 274, 72);
            }
            p.closeButton = Hit(go, "Btn_Close", 2160 - MX, 25, 238, 57);
            p.refundButton = Hit(go, "Btn_Refund", 1523 - MX, 100, 250, 63);
            p.buyCashButton = Hit(go, "Btn_BuyCash", 1789 - MX, 100, 275, 63);
            p.cashText = Yazi(go, "Cash", "0", 2294 - MX, 131.5f, lb, 37, 0f, Hex("#BEAAAB"));
            // arama: yer tutucu sprite'ta; yazilinca kutu ici siyah ortulur
            var ortu = Img(go, "AramaOrtusu", null, 309 - MX, 124, 346, 42); ortu.color = Color.black; ortu.gameObject.SetActive(false); p.aramaOrtusu = ortu.gameObject;
            var ara = Bos(go, "Arama", 309 - MX, 124, 346, 42);
            var araImg = ara.AddComponent<Image>(); araImg.color = new Color(0f, 0f, 0f, 0f); araImg.raycastTarget = true;
            var araT = Txt(ara, "Text", "", 8, 0, 330, 42, lb, 24, Hex("#E6E6E6"), TextAnchor.MiddleLeft); araT.fontStyle = FontStyle.Italic;
            var inp = ara.AddComponent<InputField>(); inp.textComponent = araT; inp.targetGraphic = araImg; inp.lineType = InputField.LineType.SingleLine; inp.characterLimit = 40;
            p.arama = inp;
            // liste: gorunum (640,270) 1700 x 840, kaydirma cubugu x 2347
            var vp = Bos(go, "Liste", 640 - MX, 270, 1700, 840); vp.AddComponent<RectMask2D>();
            var vimg = vp.AddComponent<Image>(); vimg.color = new Color(0f, 0f, 0f, 0f); vimg.raycastTarget = true;
            var icerik = Bos(vp, "Icerik", 0, 0, 1700, 840);
            var sr = vp.AddComponent<ScrollRect>(); sr.viewport = (RectTransform)vp.transform; sr.content = (RectTransform)icerik.transform;
            sr.horizontal = false; sr.vertical = true; sr.movementType = ScrollRect.MovementType.Clamped; sr.scrollSensitivity = 40f;
            var sbGo = Bos(go, "Kaydirma", 2347 - MX, 266, 15, 846);
            var sbImg = sbGo.AddComponent<Image>(); sbImg.color = new Color(0f, 0f, 0f, 0f); sbImg.raycastTarget = true;
            var sb = sbGo.AddComponent<Scrollbar>(); sb.direction = Scrollbar.Direction.BottomToTop;
            var hArea = Bos(sbGo, "Alan", 0, 0, 15, 846);
            var tut = Img(hArea, "Tutamak", "kaydirma", 0, 0, 15, 404); tut.type = Image.Type.Sliced; tut.raycastTarget = true;
            var trt = tut.rectTransform; trt.anchorMin = new Vector2(0f, 0f); trt.anchorMax = new Vector2(1f, 1f); trt.offsetMin = trt.offsetMax = Vector2.zero;
            sb.handleRect = trt; sb.targetGraphic = tut;
            sr.verticalScrollbar = sb; sr.verticalScrollbarVisibility = ScrollRect.ScrollbarVisibility.AutoHide;
            p.liste = sr; p.icerik = (RectTransform)icerik.transform;
            p.kartSablonu = Kart(icerik, "KartSablonu_Kategori", false, lb, rb);
            p.anaKartSablonu = Kart(icerik, "KartSablonu_MainPage", true, lb, rb);
            p.urunler.Add(Ornek("Scroll of Health 2000 Up", 30, 150, OlymposPowerUpKategori.Scrolls, true));
            p.urunler.Add(Ornek("Teleport Scroll", 50, 0, OlymposPowerUpKategori.Scrolls, false));
            p.urunler.Add(Ornek("Switch Premium", 1, 2800, OlymposPowerUpKategori.Premiums, false));
            var pk = Ornek("Full Package Bundle [NO TRADE]", 1, 5000, OlymposPowerUpKategori.Package, false); pk.paket = true; p.urunler.Add(pk);

            // ---------------- satin alma ayrintisi (1026,256) 666 x 740
            var ay = Bos(go, "SatinAlmaAyrintisi", 1026 - MX, 256, 666, 740);
            var a = ay.AddComponent<OlymposPowerUpAyrinti>();
            Img(ay, "Pencere", "ayrinti", 0, 0, 666, 740).raycastTarget = true;
            a.baslikText = Yazi(ay, "Baslik", "Teleport Scroll", 329f, 37.5f, lb, 29, 0.5f, Hex("#BFADAD"));
            a.ikon = Ikon(ay, "Ikon", 279, 69, 84, 84);
            a.adetText = Yazi(ay, "Adet", "(1)", 325f, 185.5f, lb, 36, 1.5f, Hex("#BFADAD"));
            a.aciklamaText = Txt(ay, "Aciklama", "Teleport Scroll.", 26, 211, 612, 330, rb, 33, Hex("#FCE7E6"), TextAnchor.UpperLeft);
            a.aciklamaText.horizontalOverflow = HorizontalWrapMode.Wrap;
            a.fiyatText = Yazi(ay, "Fiyat", "0", 325.5f, 595f, lb, 37, 0f, Hex("#FDDE24"));
            a.eksiButton = Hit(ay, "Btn_Eksi", 189, 89, 62, 58); a.artiButton = Hit(ay, "Btn_Arti", 414, 89, 62, 58);
            a.purchaseButton = Hit(ay, "Btn_Puchase", 184, 658, 254, 79); a.closeButton = Hit(ay, "Btn_X", 594, 6, 68, 66);
            p.ayrinti = a;

            // ---------------- paket icerigi (912,158) 918 x 880
            var pi = Bos(go, "PaketIcerigi", 912 - MX, 158, 918, 880);
            var pic = pi.AddComponent<OlymposPowerUpPaketIcerik>();
            Img(pi, "Pencere", "paket_icerik", 0, 0, 918, 880).raycastTarget = true;
            pic.icerikAlani = (RectTransform)Bos(pi, "IcerikAlani", 16, 40, 870, 820).transform;
            pic.closeButton = Hit(pi, "Btn_X", 838, 2, 70, 70);
            p.paketIcerik = pic;

            // ---------------- Cash Code sayfasi (oyun alaninin tamami, opak)
            var cc = Bos(go, "CashCode", 0, 0, 2137, 1220);
            var ccs = cc.AddComponent<OlymposPowerUpCashCode>();
            Img(cc, "Sayfa", "cashcode", 0, 0, 2137, 1220).raycastTarget = true;
            var kod = Bos(cc, "KodAlani", 780 - MX, 583, 904, 98);
            var kImg = kod.AddComponent<Image>(); kImg.color = new Color(0f, 0f, 0f, 0f); kImg.raycastTarget = true;
            var yt = Yazi(kod, "YerTutucu", "Enter Your Epin or Gift Code", 1232.5f - 780f, 53f, lb, 29, 0.5f, Hex("#FDE6E6"));
            var kt = Txt(kod, "Text", "", 30, 0, 844, 98, lb, 29, Color.white, TextAnchor.MiddleCenter);
            var kin = kod.AddComponent<InputField>(); kin.textComponent = kt; kin.placeholder = yt; kin.targetGraphic = kImg;
            kin.lineType = InputField.LineType.SingleLine; kin.characterLimit = 64;
            ccs.kodAlani = kin;
            ccs.useButton = Hit(cc, "Btn_Use", 1093 - MX, 682, 257, 101);
            ccs.closeButton = Hit(cc, "Btn_X", 2305 - MX, 254, 64, 64);
            ccs.logo = Img(cc, "Logo", null, 480 - MX, 890, 300, 145); ccs.logo.preserveAspect = true;
            p.cashCode = ccs;

            // ---------------- basari bildirimi: tam ekran gri ortu + pencere (1024,575) 664 x 229
            var bs = Bos(go, "BasariBildirimi", -MX, 0, 2712, 1220);
            var bsc = bs.AddComponent<OlymposPowerUpBasari>();
            bsc.ortu = Img(bs, "Ortu", null, 0, 0, 2712, 1220); bsc.ortu.raycastTarget = true; bsc.ortu.color = OlymposPowerUpRenk.GriOrtu();
            var dl = Bos(bs, "Pencere", 1024, 575, 664, 229);
            Img(dl, "Krom", "basari", 0, 0, 664, 229).raycastTarget = true;
            bsc.mesajText = Yazi(dl, "Mesaj", "Purchase Succcessfully", 327f, 87.5f, lb, 30, 0f, Hex("#FCE7E6"));
            bsc.okButton = Hit(dl, "Btn_OK", 212, 146, 253, 71);
            p.basari = bsc;

            SaveAndPlace(go, "PowerUpStore_1298");
        }

        static OlymposPowerUpUrun Ornek(string ad, int adet, int fiyat, OlymposPowerUpKategori k, bool ana)
        {
            var u = new OlymposPowerUpUrun(); u.ad = ad; u.adet = adet; u.fiyat = fiyat; u.kategori = k; u.anaSayfada = ana; return u;
        }

        /// <summary>Kart sablonu: sprite kokeni = cerceve - (2,2) (kategori) / (1,1) (Main Page).</summary>
        static OlymposPowerUpKart Kart(GameObject parent, string ad, bool ana, Font lb, Font rb)
        {
            float w = ana ? 294 : 292, h = 315;
            var go = Bos(parent, ad, 0, 0, w, h);
            var k = go.AddComponent<OlymposPowerUpKart>();
            k.icGecirgenlikLineer = ana ? 0.185f : 0.30f;
            k.ic = ana ? Img(go, "Ic", null, 4, 4, 286, 285) : Img(go, "Ic", null, 5, 5, 282, 283);
            k.ic.color = new Color(0f, 0f, 0f, OlymposPowerUpRenk.SiyahAlfa(k.icGecirgenlikLineer));
            Img(go, "Kart", ana ? "kart_ana" : "kart_kategori", 0, 0, w, h);
            float fx = ana ? 1 : 2, fy = ana ? 1 : 2;                                         // cerceve sol-ust
            Vector2 ik = ana ? new Vector2(103, 47) : new Vector2(102, 39);
            k.ikon = Ikon(go, "Ikon", fx + ik.x, fy + ik.y, 84, 84);
            k.rozet = Txt(go, "Rozet", "30", fx + ik.x, fy + ik.y + 50, 81, 34, lb, 24, Hex("#FEE5E4"), TextAnchor.LowerRight);
            var ol = k.rozet.gameObject.AddComponent<Outline>(); ol.effectColor = new Color(0f, 0f, 0f, 0.8f); ol.effectDistance = new Vector2(1f, -1f);
            float adY = ana ? 149.5f : 143.5f;
            k.adText = Txt(go, "Ad", "Scroll of Health 2000 Up", fx + 144 - (ana ? 107.5f : 113.5f), fy + adY - 14f, ana ? 215 : 227, 60, rb, 22, Hex("#CBBBB9"), TextAnchor.UpperCenter);
            k.adText.horizontalOverflow = HorizontalWrapMode.Wrap; k.adText.lineSpacing = 1f;
            Vector2 pa = ana ? new Vector2(87, 188) : new Vector2(85, 187);
            Img(go, "Para", "para_ikonu", fx + pa.x, fy + pa.y, 41, 43);
            float fyY = ana ? 206 : 205;
            k.fiyatText = Txt(go, "Fiyat", "150", fx + 127, fy + fyY - 20, 160, 40, lb, 31, Hex("#F94922"), TextAnchor.MiddleLeft);
            k.fiyatText.gameObject.AddComponent<OlymposPowerUpHarfAraligi>().aralik = 1.5f;
            var fo = k.fiyatText.gameObject.AddComponent<Outline>(); fo.effectColor = new Color(45f / 255f, 14f / 255f, 6f / 255f, 1f); fo.effectDistance = new Vector2(1f, -1f);
            if (ana) k.purchaseButton = Hit(go, "Btn_Purchase", 25, 256, 244, 59);
            else
            {
                k.uygunDugme = Img(go, "UygunDugme", "dugme_kategori_uygun", 74, 250, 146, 66); k.uygunDugme.enabled = false;
                k.purchaseButton = Hit(go, "Btn_Purchase", 74, 250, 146, 66);
            }
            return k;
        }

        static GameObject Bos(GameObject parent, string name, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            if (parent != null) { Place(go, parent, x, y, w, h); return go; }
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f); rt.sizeDelta = new Vector2(w, h);
            rt.anchoredPosition = new Vector2(x + w * 0.5f - EW * 0.5f, EH * 0.5f - (y + h * 0.5f));
            return go;
        }

        /// <summary>Ortali tek satir; (cx, cy) murekkep merkezi (ebeveyn ici piksel).</summary>
        static Text Yazi(GameObject parent, string ad, string metin, float cx, float cy, Font f, int punto, float aralik, Color renk)
        {
            var t = Txt(parent, ad, metin, cx - 300f, cy - 30f, 600f, 60f, f, punto, renk, TextAnchor.MiddleCenter);
            if (aralik != 0f) t.gameObject.AddComponent<OlymposPowerUpHarfAraligi>().aralik = aralik;
            return t;
        }

        static Image Ikon(GameObject parent, string ad, float x, float y, float w, float h)
        {
            var img = Img(parent, ad, null, x, y, w, h); img.preserveAspect = true; img.enabled = false; return img;
        }

        static void Sinir(string name, Vector4 b)
        {
            var ti = AssetImporter.GetAtPath(TexDir + "/" + name + ".png") as TextureImporter;
            if (ti == null) return; ti.spriteBorder = b; ti.SaveAndReimport();
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
