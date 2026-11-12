// OLYMPOS-KO · 1298 Merchant / Slave Merchant / Equip-UnEquip / esya bilgi penceresi — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Merchant (Tezgâh · Slave · Equip · Eşya Bilgisi) Oluştur
// Butun olculer 2712 x 1220 oyun kayitlarindan alindi — arayuz/09-merchant.md
using System.Collections.Generic;
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposMerchantBuilder
    {
        const float EW = 2712f, EH = 1220f;
        const string Klasor = "OlymposMerchant1298";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";     // OyunIci paketiyle ortak

        static readonly Color Pembe = Hex("#FFE7E9"), Beyaz = Color.white, Mor = Hex("#CA89E7"), Etiket = Hex("#CA89E2");
        static readonly Color Altin = Hex("#DDA96A"), Sari = Hex("#FCD100"), Cizgi = Hex("#4A443C");

        static string Root;
        static Font Roboto, RobotoInce, Slab, SlabInce;
        enum Capa { SolUst, SagUst, Orta }

        [MenuItem("OLYMPOS/1298/Merchant (Tezgâh · Slave · Equip · Eşya Bilgisi) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            string[] dokular = {
                "menu_krom", "create_krom", "fiyat_krom", "tezgah_krom", "mpencere_krom", "slave_krom", "slave_satir", "slave_ikon_cerceve",
                "yuva_dolu_create_ust", "yuva_dolu_create_env", "yuva_dolu_mp_ust", "yuva_dolu_mp_env", "yuva_dolu_tezgah",
                "btn_equip", "btn_unequip", "btn_remove", "btn_close", "ikon_cerceve",
                "adet_krom", "onay_krom", "btn_onay_zemin", "yazi_ok", "yazi_cancel", "onay_ikon_cerceve", "sure_oluk", "sure_dolgu",
                "ikon_short_bow", "ikon_silan_boots", "ikon_knife", "ikon_hp_scroll", "ikon_zirh_scroll", "ikon_hiz_iksiri",
                "ikon_eldiven", "ikon_yuzuk", "ikon_asa", "ikon_zirh", "ikon_bilezik", "ikon_kupe", "ikon_pantolon", "ikon_sopa" };
            foreach (var d in dokular) Tex(d);
            AssetDatabase.Refresh();
            Roboto = LoadFont("Roboto-Bold.ttf");
            RobotoInce = LoadFont("Roboto-Regular.ttf") ?? Roboto;
            Slab = LoadFont("RobotoSlab-Bold.ttf");
            SlabInce = LoadFont("RobotoSlab-Regular.otf") ?? Slab;

            var root = new GameObject("Merchant_1298", typeof(RectTransform));
            var rrt = (RectTransform)root.transform;
            rrt.anchorMin = Vector2.zero; rrt.anchorMax = Vector2.one;
            rrt.offsetMin = Vector2.zero; rrt.offsetMax = Vector2.zero;
            var yon = root.AddComponent<OlymposMerchantYonetici>();

            // cizim sirasi: cubuk < pencereler < menu < bilgi penceresi
            yon.tezgahCubugu = BuildTezgah(root);
            var ekipman = BuildDeneme(root, yon);
            yon.merchantPenceresi = BuildMerchantPenceresi(root);
            yon.olustur = BuildOlustur(root);
            yon.slaveMerchant = BuildSlave(root);
            yon.komutMenusu = BuildMenu(root);
            var bilgi = BuildBilgi(root);
            yon.bilgi = bilgi;
            yon.tezgahCubugu.bilgi = bilgi;
            yon.merchantPenceresi.bilgi = bilgi;
            yon.olustur.bilgi = bilgi;
            ekipman.bilgi = bilgi;
            foreach (var n in root.GetComponentsInChildren<OlymposNpcEsyaBilgisi>(true)) n.bilgi = bilgi;
            yon.envanter = OrnekEnvanter();

            SaveAndPlace(root, "Merchant_1298");
        }

        // =====================================================================
        // Komut menusu — sprite (2322, 97) 314 x 1015 ; zemin alfa 0.94
        static OlymposKomutMenusu BuildMenu(GameObject parent)
        {
            var go = Kutu(parent, "KomutMenusu", Capa.SagUst, 2322, 97, 314, 1015);
            var m = go.AddComponent<OlymposKomutMenusu>();
            var bg = Img(go, "Background", null, 8, 69, 300, 940);
            bg.color = new Color(0f, 0f, 0f, m.backgroundAlpha); bg.raycastTarget = true;
            m.background = bg;
            Img(go, "Krom", "menu_krom", 0, 0, 314, 1015);
            string[] ad = { "PowerUpStore", "OpenMerchant", "SlaveMerchant", "SeekingParty", "Options", "Forum", "Discord", "Instagram" };
            for (int i = 0; i < 8; i++) m.dugmeler[i] = Hit(go, "Btn_" + ad[i], 14, 110 + 116f * i, 290, 62);
            m.closeButton = Hit(go, "Btn_Close", 129, 18, 76, 76);
            go.SetActive(false);
            return m;
        }

        // =====================================================================
        // Create a Merchant — sprite (1573, 51) 756 x 851 ; zemin alfa 0.95
        static OlymposMerchantOlustur BuildOlustur(GameObject parent)
        {
            var go = Kutu(parent, "CreateMerchant", Capa.Orta, 1573, 51, 756, 851);
            var c = go.AddComponent<OlymposMerchantOlustur>();
            c.titleBackground = Zemin(go, "TitleBackground", 5, 11, 754 - 4, 50, c.backgroundAlpha);
            c.background = Zemin(go, "Background", 15, 61, 740, 785, c.backgroundAlpha);
            Img(go, "Krom", "create_krom", 0, 0, 756, 851);
            for (int r = 0; r < 2; r++)
                for (int k = 0; k < 6; k++)
                    c.tezgahYuvalari[r * 6 + k] = Yuva(go, "Tezgah_" + (r * 6 + k), 64 + 111f * k, 112 + 110f * r, 102, 100, "yuva_dolu_create_ust");
            for (int r = 0; r < 4; r++)
                for (int k = 0; k < 7; k++)
                    c.envanterYuvalari[r * 7 + k] = Yuva(go, "Envanter_" + (r * 7 + k), 40.8f + 99.67f * k, 363 + 100.9f * r, 103, 101, "yuva_dolu_create_env");
            c.okButton = Hit(go, "Btn_OK", 219, 790, 157, 57);
            c.cancelButton = Hit(go, "Btn_Cancel", 408, 790, 160, 57);
            c.fiyatDiyalogu = BuildFiyat(go);
            c.adetDiyalogu = BuildAdet(go);
            go.SetActive(false);
            return c;
        }

        // Fiyat diyalogu — sprite (1605, 208) 711 x 522 -> Create penceresine gore (32, 157) ; zemin alfa 0.97
        static OlymposFiyatDiyalogu BuildFiyat(GameObject parent)
        {
            var go = new GameObject("FiyatDiyalogu", typeof(RectTransform));
            Place(go, parent, 32, 157, 711, 522);
            var f = go.AddComponent<OlymposFiyatDiyalogu>();
            var bg = Img(go, "Background", null, 6, 6, 699, 510);
            bg.color = new Color(0f, 0f, 0f, f.backgroundAlpha); bg.raycastTarget = true;
            f.background = bg;
            Img(go, "Krom", "fiyat_krom", 0, 0, 711, 522);      // iki dildeki uyari yazisi orijinal piksellerden

            var alan = new GameObject("PriceField", typeof(RectTransform));
            Place(alan, go, 205, 340, 365, 70);
            var ai = alan.AddComponent<Image>(); ai.color = new Color(0f, 0f, 0f, 0f); ai.raycastTarget = true;
            var inp = alan.AddComponent<InputField>();
            inp.targetGraphic = ai;
            // yazi: egik, #EBDFCD, punto 46 ; murek solu x=1819 (alan ici 9), ust 566
            var t = Txt(alan, "Text", "0", 9, 2, 350, 66, RobotoInce, 46, Hex("#EBDFCD"), TextAnchor.MiddleLeft);
            t.fontStyle = FontStyle.Italic;
            inp.textComponent = t;
            inp.contentType = InputField.ContentType.Standard;       // virgullu gosterim icin; rakam disi karakterler betikte atilir
            inp.keyboardType = TouchScreenKeyboardType.NumberPad;
            inp.lineType = InputField.LineType.SingleLine;
            inp.characterLimit = 14;
            inp.text = "0";
            f.priceField = inp;

            f.okButton = Hit(go, "Btn_OK", 146, 437, 200, 63);
            f.cancelButton = Hit(go, "Btn_Cancel", 362, 437, 202, 63);
            go.SetActive(false);
            return f;
        }

        // ---------------------------------------------------------------------
        // Asagidaki iki pencere TABLET goruntulerinden (2266 x 1488) olculdu; o duzen telefon duzeninin 1.0405 kati.
        // Olculer tablet pikseli olarak yazilir, T() telefon birimine cevirir. Sprite'lar tablet cozunurlugunde.
        const float Tablet = 1.0405f;
        static float T(float v) { return v / Tablet; }

        // Adet girisi — tablet 740 x 543 -> 711 x 522 ; fiyat diyaloguyla ayni yerde acilir ; zemin alfa 0.94
        static OlymposAdetDiyalogu BuildAdet(GameObject parent)
        {
            var go = new GameObject("AdetDiyalogu", typeof(RectTransform));
            Place(go, parent, 32, 157, T(740), T(543));
            var a = go.AddComponent<OlymposAdetDiyalogu>();
            var bg = Img(go, "Background", null, T(6), T(6), T(728), T(531));
            bg.color = new Color(0f, 0f, 0f, a.backgroundAlpha); bg.raycastTarget = true;
            a.background = bg;
            Img(go, "Krom", "adet_krom", 0, 0, T(740), T(543));     // baslik + iki dildeki uyari + alan cercevesi + dugmeler orijinal piksellerden

            var alan = new GameObject("CountField", typeof(RectTransform));
            Place(alan, go, T(150), T(362), T(440), T(64));
            var ai = alan.AddComponent<Image>(); ai.color = new Color(0f, 0f, 0f, 0f); ai.raycastTarget = true;
            var inp = alan.AddComponent<InputField>();
            inp.targetGraphic = ai;
            // sayi: egik, #D6D6D6, tablet punto 46 ; murek solu x=219, ust y=377
            var t = Txt(alan, "Text", "20", T(69), 0, T(360), T(64), RobotoInce, Mathf.RoundToInt(T(46)), Hex("#D6D6D6"), TextAnchor.MiddleLeft);
            t.fontStyle = FontStyle.Italic;
            inp.textComponent = t;
            inp.contentType = InputField.ContentType.IntegerNumber;
            inp.keyboardType = TouchScreenKeyboardType.NumberPad;
            inp.lineType = InputField.LineType.SingleLine;
            inp.characterLimit = 5;
            inp.text = "1";
            a.countField = inp;

            a.okButton = Hit(go, "Btn_OK", T(154), T(457), T(204), T(65));
            a.cancelButton = Hit(go, "Btn_Cancel", T(380), T(457), T(207), T(65));
            go.SetActive(false);
            return a;
        }

        // Satin alma onayi — tablet 577 x 530 -> 554 x 509 ; Merchant penceresine gore (153, 179) ; zemin mat (0.99)
        static OlymposSatinAlmaOnayi BuildOnay(GameObject parent)
        {
            var go = new GameObject("SatinAlmaOnayi", typeof(RectTransform));
            Place(go, parent, 153, 179, T(577), T(530));
            var o = go.AddComponent<OlymposSatinAlmaOnayi>();
            var bg = Img(go, "Background", null, T(5), T(5), T(567), T(520));
            bg.color = new Color(0f, 0f, 0f, o.backgroundAlpha); bg.raycastTarget = true;
            o.background = bg;
            Img(go, "Krom", "onay_krom", 0, 0, T(577), T(530));     // cerceve + sari uyari + pembe baslik orijinal piksellerden

            o.iconImage = Img(go, "Icon", null, T(245), T(30), T(84), T(82));
            Img(go, "IconFrame", "onay_ikon_cerceve", T(238), T(23), T(98), T(96));
            o.upgradeText = Txt(go, "Upgrade", "+5", T(231), T(22), T(100), T(40), Roboto, Mathf.RoundToInt(T(29)), Etiket, TextAnchor.UpperRight);

            Img(go, "TimerTrough", "sure_oluk", T(58), T(144), T(460), T(24));
            var dol = Img(go, "TimerFill", "sure_dolgu", T(60), T(147), T(455), T(17));
            dol.type = Image.Type.Filled; dol.fillMethod = Image.FillMethod.Horizontal; dol.fillOrigin = 0; dol.fillAmount = 0f;
            o.fillImage = dol;
            o.dolguGenisligi = T(455);
            // sayac: dolgunun ucunda, beyaz-pembe #FFE6E6, dis hatli, tablet punto 19
            var say = new GameObject("Countdown", typeof(RectTransform));
            var srt = (RectTransform)say.transform;
            srt.SetParent(go.transform, false);
            srt.anchorMin = srt.anchorMax = new Vector2(0f, 1f); srt.pivot = new Vector2(0.5f, 1f);
            srt.anchoredPosition = new Vector2(T(60), -T(143)); srt.sizeDelta = new Vector2(T(60), T(26));
            var st = say.AddComponent<Text>();
            st.font = Roboto; st.fontSize = Mathf.RoundToInt(T(19)); st.color = Hex("#FFE6E6"); st.alignment = TextAnchor.MiddleCenter; st.text = "4";
            st.horizontalOverflow = HorizontalWrapMode.Overflow; st.verticalOverflow = VerticalWrapMode.Overflow; st.raycastTarget = false;
            var so = say.AddComponent<Outline>(); so.effectColor = new Color(0f, 0f, 0f, 0.95f); so.effectDistance = new Vector2(1f, -1f);
            o.countdownText = st;

            // fiyat satirlari: ortali (merkez x=295.5), 470 genislikte sarar, satir adimi 31, tablet punto 27, #D9C3C3 ; fiyat #FFD300
            var m = Txt(go, "Message", "", T(60.5f), T(281), T(470), T(110), Roboto, Mathf.RoundToInt(T(27)), Hex("#D9C3C3"), TextAnchor.UpperCenter);
            m.supportRichText = true;
            m.horizontalOverflow = HorizontalWrapMode.Wrap;
            m.lineSpacing = 0.98f;
            o.messageText = m;

            o.okButton = OnayDugmesi(go, "Btn_OK", "yazi_ok", T(115), T(437), T(47), T(19), T(66), T(28));
            o.cancelButton = OnayDugmesi(go, "Btn_Cancel", "yazi_cancel", T(332), T(437), T(14), T(19), T(130), T(28));
            go.SetActive(false);
            return o;
        }

        /// <summary>Zemin (renklenir) + yazi (renklenmez): kapaliyken yalniz zemin 0.56'ya duser — orijinaldeki soluk OK ile ayni.</summary>
        static Button OnayDugmesi(GameObject parent, string name, string yazi, float x, float y, float yx, float yy, float yw, float yh)
        {
            var img = Img(parent, name, "btn_onay_zemin", x, y, T(156), T(64));
            img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>();
            b.targetGraphic = img;
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white; cb.highlightedColor = Color.white; cb.selectedColor = Color.white;
            cb.pressedColor = new Color(0.72f, 0.72f, 0.72f, 1f);
            cb.disabledColor = new Color(0.56f, 0.56f, 0.56f, 1f);
            cb.colorMultiplier = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
            Img(img.gameObject, "Label", yazi, yx, yy, yw, yh);
            return b;
        }

        // =====================================================================
        // Tezgah cubugu — sprite (1159, 551) 404 x 168 ; yuva zemini alfa 0.87
        static OlymposTezgahCubugu BuildTezgah(GameObject parent)
        {
            var go = Kutu(parent, "TezgahCubugu", Capa.Orta, 1159, 551, 404, 168);
            var t = go.AddComponent<OlymposTezgahCubugu>();
            for (int i = 0; i < 4; i++) t.yuvaZeminleri[i] = Zemin(go, "YuvaZemini_" + i, 35 + 86f * i, 17, 70, 72, t.yuvaAlpha);
            Img(go, "Krom", "tezgah_krom", 0, 0, 404, 168);
            for (int i = 0; i < 4; i++) t.yuvalar[i] = Yuva(go, "Yuva_" + i, 27 + 86f * i, 9, 86, 88, "yuva_dolu_tezgah");
            t.openButton = Hit(go, "Btn_Open", 23, 104, 179, 60);
            t.whisperButton = Hit(go, "Btn_Whisper", 202, 104, 178, 60);
            go.SetActive(false);
            return t;
        }

        // =====================================================================
        // "<ad> Merchant" — sprite (945, 113) 785 x 987 ; zemin alfa 0.89
        static OlymposMerchantPenceresi BuildMerchantPenceresi(GameObject parent)
        {
            var go = Kutu(parent, "MerchantPenceresi", Capa.Orta, 945, 113, 785, 987);
            var p = go.AddComponent<OlymposMerchantPenceresi>();
            p.titleBackground = Zemin(go, "TitleBackground", 13, 9, 762, 48, p.backgroundAlpha);
            p.background = Zemin(go, "Background", 7, 59, 770, 905, p.backgroundAlpha);
            Img(go, "Krom", "mpencere_krom", 0, 0, 785, 987);
            // baslik: Roboto Slab Regular 33, #DDA96A ; merkez x=390.5, ust kenar 18
            p.titleText = Txt(go, "Title", "xMegaTon Merchant", 0, 5, 781, 50, SlabInce, 33, Altin, TextAnchor.MiddleCenter);
            // para: Roboto Bold 36, beyaz ; sag kenar x=673, ust 425
            p.goldText = Txt(go, "Gold", "523,455", 373, 413, 300, 50, Roboto, 36, Beyaz, TextAnchor.MiddleRight);
            for (int r = 0; r < 2; r++)
                for (int k = 0; k < 6; k++)
                    p.tezgahYuvalari[r * 6 + k] = Yuva(go, "Tezgah_" + (r * 6 + k), 29.7f + 120.31f * k, 115.8f + 121.17f * r, 117, 114, "yuva_dolu_mp_ust");
            for (int r = 0; r < 4; r++)
                for (int k = 0; k < 7; k++)
                    p.envanterYuvalari[r * 7 + k] = Yuva(go, "Envanter_" + (r * 7 + k), 22.8f + 103.64f * k, 475.9f + 104.4f * r, 104, 102, "yuva_dolu_mp_env");
            p.okButton = Hit(go, "Btn_OK", 210, 920, 163, 56);
            p.cancelButton = Hit(go, "Btn_Cancel", 407, 920, 157, 56);
            p.satinAlmaOnayi = BuildOnay(go);
            go.SetActive(false);
            return p;
        }

        // =====================================================================
        // Slave Merchant — sprite (1444, 90) 1002 x 1027 ; zemin alfa 0.95 ; satir 946 x 96, adim 92
        static OlymposSlaveMerchant BuildSlave(GameObject parent)
        {
            const int N = 8;
            var go = Kutu(parent, "SlaveMerchant", Capa.Orta, 1444, 90, 1002, 1027);
            var s = go.AddComponent<OlymposSlaveMerchant>();
            var bg = Img(go, "Background", null, 8, 8, 952, 1010);
            bg.color = new Color(0f, 0f, 0f, s.backgroundAlpha); bg.raycastTarget = true;
            s.background = bg;
            Img(go, "Krom", "slave_krom", 0, 0, 1002, 1027);
            s.satirlar = new OlymposSlaveMerchant.Satir[N];
            for (int i = 0; i < N; i++)
            {
                var kok = new GameObject("Satir_" + i, typeof(RectTransform));
                Place(kok, go, 16, 204 + 92f * i, 946, 96);
                var st = new OlymposSlaveMerchant.Satir();
                Img(kok, "Cerceve", "slave_satir", 0, 0, 946, 96);
                st.ikon = Img(kok, "Icon", null, 57, 15, 70, 68);
                Img(kok, "IconFrame", "slave_ikon_cerceve", 52, 10, 80, 78);
                st.yukseltmeText = Txt(kok, "Upgrade", "+5", 46, 10, 80, 30, Roboto, 22, Etiket, TextAnchor.UpperRight);
                st.sayacText = Txt(kok, "Counter", "1/0", 169, 34, 160, 40, Slab, 26, Beyaz, TextAnchor.MiddleLeft);
                st.durumText = Txt(kok, "Status", "Not sold yet.", 165.5f, 34, 600, 40, Slab, 28, Beyaz, TextAnchor.MiddleCenter);
                st.kok = kok;
                kok.SetActive(false);
                s.satirlar[i] = st;
            }
            s.refreshButton = Hit(go, "Btn_Refresh", 784, 30, 72, 74);
            s.closeButton = Hit(go, "Btn_Close", 866, 28, 82, 82);
            s.claimCoinsButton = Hit(go, "Btn_ClaimCoins", 749, 166, 221, 62);
            s.closeSlaveButton = Hit(go, "Btn_CloseSlaveMerchant", 266, 948, 431, 70);
            go.SetActive(false);
            return s;
        }

        // =====================================================================
        // Esya bilgi penceresi — zemin alfa 0.93 ; boyut icerige gore betikte hesaplanir
        static OlymposEsyaBilgiPenceresi BuildBilgi(GameObject parent)
        {
            var go = Kutu(parent, "EsyaBilgiPenceresi", Capa.SolUst, 1727, 507, 400, 613);
            var b = go.AddComponent<OlymposEsyaBilgiPenceresi>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, b.backgroundAlpha); bg.raycastTarget = true;
            b.background = bg;
            b.iconImage = Img(go, "Icon", null, 12, 12, 89, 89);
            Img(go, "IconFrame", "ikon_cerceve", 5, 5, 103, 103);
            b.nameText = Txt(go, "Name", "", 115, 2, 900, 48, Roboto, 36, Pembe, TextAnchor.MiddleLeft);
            b.typeText = Txt(go, "Type", "", 115, 44, 900, 32, Roboto, 27, Pembe, TextAnchor.MiddleLeft);
            b.priceText = Txt(go, "Price", "", 12, 131, 900, 40, Roboto, 32, Sari, TextAnchor.MiddleLeft);
            b.statTexts = new Text[8];
            for (int i = 0; i < 8; i++) b.statTexts[i] = Txt(go, "Stat_" + i, "", 12, 176 + 38.7f * i, 900, 34, Roboto, 29, Pembe, TextAnchor.MiddleLeft);
            b.centerTexts = new Text[10];
            for (int i = 0; i < 10; i++) b.centerTexts[i] = Txt(go, "Center_" + i, "", 0, 376 + 31.5f * i, 400, 32, Roboto, 27, Pembe, TextAnchor.MiddleCenter);
            float[] ay = { 147, 347, 535 };
            for (int i = 0; i < 3; i++)
            {
                var a = Img(go, "Separator_" + i, null, 12, ay[i], 374, 1);
                a.color = Cizgi;
                b.separators[i] = a.rectTransform;
            }
            b.equipButton = SpriteBtn(go, "Btn_Equip", "btn_equip", 12, 548, 155, 62);
            b.unEquipButton = SpriteBtn(go, "Btn_UnEquip", "btn_unequip", 12, 548, 155, 62);
            b.removeButton = SpriteBtn(go, "Btn_Remove", "btn_remove", 12, 548, 155, 62);
            b.closeButton = SpriteBtn(go, "Btn_Close", "btn_close", 173, 548, 155, 62);
            go.SetActive(false);
            return b;
        }

        // =====================================================================
        // Deneme paneli: Commands dugmesi + Equip/UnEquip ornegi (Silan Boots) + NPC ornegi (Knife)
        // Kendi alt barinizla / envanter ve dukkan pencerelerinizle degistirin.
        static OlymposEkipman BuildDeneme(GameObject parent, OlymposMerchantYonetici yon)
        {
            var go = Kutu(parent, "Deneme (kendi pencerelerinizle degistirin)", Capa.SolUst, 60, 420, 520, 330);
            var bg = go.AddComponent<Image>(); bg.color = new Color(0f, 0f, 0f, 0.6f); bg.raycastTarget = true;
            Txt(go, "Baslik", "DENEME", 14, 6, 400, 26, Roboto, 18, Sari, TextAnchor.MiddleLeft);

            yon.commandsDugmesi = DemoDugme(go, "Btn_Commands", "Commands", 14, 40, 200, 50);

            Txt(go, "E1", "Envanter", 14, 104, 150, 22, Roboto, 16, Beyaz, TextAnchor.MiddleLeft);
            Txt(go, "E2", "Ekipman", 144, 104, 150, 22, Roboto, 16, Beyaz, TextAnchor.MiddleLeft);
            Txt(go, "E3", "NPC dükkânı", 334, 104, 180, 22, Roboto, 16, Beyaz, TextAnchor.MiddleLeft);
            var ek = go.AddComponent<OlymposEkipman>();
            var y1 = DemoYuva(go, "EnvanterYuvasi", 14, 130);
            var y2 = DemoYuva(go, "EkipmanYuvasi", 144, 130);
            ek.envanterYuvalari = new[] { y1 };
            ek.ekipmanYuvalari = new[] { y2 };
            ek.envanter = new List<OlymposTicariEsya> { SilanBoots() };
            ek.ekipman = new OlymposTicariEsya[1];
            Txt(go, "E4", "dokun: Equip / UnEquip", 14, 240, 300, 22, RobotoInce, 15, Pembe, TextAnchor.MiddleLeft);

            var y3 = DemoYuva(go, "NpcYuvasi", 334, 130);
            var npc = y3.gameObject.AddComponent<OlymposNpcEsyaBilgisi>();
            npc.yuva = y3; npc.esya = Knife();
            Txt(go, "E5", "dokun: Buy Price", 334, 240, 180, 22, RobotoInce, 15, Pembe, TextAnchor.MiddleLeft);
            Txt(go, "E6", "Commands > OPEN MERCHANT: eşyaya dokun, fiyat gir, OK", 14, 276, 500, 22, RobotoInce, 15, Pembe, TextAnchor.MiddleLeft);
            Txt(go, "E7", "Commands > SLAVE MERCHANT: tezgâh açıkken", 14, 298, 500, 22, RobotoInce, 15, Pembe, TextAnchor.MiddleLeft);
            return ek;
        }

        static OlymposTicariYuva DemoYuva(GameObject parent, string ad, float x, float y)
        {
            var z = Zemin(parent, ad + "_Zemin", x, y, 103, 103, 0.9f);
            z.raycastTarget = false;
            var yv = Yuva(parent, ad, x, y, 103, 103, "ikon_cerceve");
            return yv;
        }

        static Button DemoDugme(GameObject parent, string name, string yazi, float x, float y, float w, float h)
        {
            var img = Img(parent, name, null, x, y, w, h);
            img.color = new Color(0.12f, 0.14f, 0.2f, 0.95f); img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>(); b.targetGraphic = img; Renkler(b);
            Txt(img.gameObject, "Text", yazi, 0, 0, w, h, Slab, 24, Beyaz, TextAnchor.MiddleCenter);
            return b;
        }

        // ---------------------------------------------------------------- ornek veriler (ekran goruntulerinden)
        static OlymposBilgiSatiri S(string m, OlymposBilgiRengi r) { return new OlymposBilgiSatiri(m, r); }

        static OlymposTicariEsya ShortBow()
        {
            return new OlymposTicariEsya {
                id = "short_bow_5", ad = "Short Bow(+5)", adRengi = Mor, turSatiri = "Upgrade Item", ikon = Spr("ikon_short_bow"), yukseltme = 5,
                statlar = new[] { S("Attack Power : 31", OlymposBilgiRengi.Beyaz), S("Poison Damage : 50", OlymposBilgiRengi.Zehir), S("Required Dexterity : 80", OlymposBilgiRengi.Kirmizi) },
                sinifSatiri = "(Rogue Item)", sinifUygun = false, cinsSatiri = "(Bow)", dereceSatiri = "Item Grade : Low Class",
                aciklama = "A small bow that can\nshoot far due to its\nelasticity.", kusanilir = true };
        }

        static OlymposTicariEsya SilanBoots()
        {
            return new OlymposTicariEsya {
                id = "silan_boots", ad = "Silan Boots", adRengi = Pembe, turSatiri = "-", ikon = Spr("ikon_silan_boots"),
                statlar = new[] { S("Defense Ability : 15", OlymposBilgiRengi.Beyaz), S("Bonus HP : 15", OlymposBilgiRengi.Bonus),
                                  S("Bonus MP : 15", OlymposBilgiRengi.Bonus), S("Required Magic Power : 53", OlymposBilgiRengi.Beyaz) },
                sinifSatiri = "(Magician Item)", sinifUygun = true, dereceSatiri = "Item Grade : Middle Class",
                aciklama = "A pair of shoes that would\nlook good on a mage.", kusanilir = true, bonusHp = 15, bonusMp = 15 };
        }

        static OlymposTicariEsya Knife()
        {
            return new OlymposTicariEsya {
                id = "knife_1", ad = "Knife(+1)", adRengi = Mor, turSatiri = "Upgrade Item", ikon = Spr("ikon_knife"), yukseltme = 1, npcFiyati = 3188,
                statlar = new[] { S("Attack Power : 11", OlymposBilgiRengi.Beyaz), S("Required Dexterity : 80", OlymposBilgiRengi.Kirmizi) },
                cinsSatiri = "(Dagger)", dereceSatiri = "Item Grade : Low Class",
                aciklama = "This knife is more\npowerful than\na dagger, and is suited\nfor stabbing." };
        }

        static OlymposTicariEsya Basit(string id, string ad, string ikon, int adet, int yukseltme)
        {
            return new OlymposTicariEsya { id = id, ad = ad, ikon = Spr(ikon), adet = adet, yukseltme = yukseltme,
                                           adRengi = yukseltme > 0 ? Mor : Pembe, turSatiri = yukseltme > 0 ? "Upgrade Item" : "-" };
        }

        // Videodaki envanter dizilimi (7 x 4). Adi goruntulenmeyen esyalar "Ornek ..." adiyla; sayac rakami ikona
        // gomulu olan dort esya (kristal, kirmizi iksir, kask, ikinci HP scroll) alinmadi.
        static List<OlymposTicariEsya> OrnekEnvanter()
        {
            var e = new List<OlymposTicariEsya>();
            for (int i = 0; i < OlymposMerchantOlustur.EnvanterYuvasi; i++) e.Add(null);
            e[0] = Basit("hp_scroll_500", "Scroll of 500HP Up(L)", "ikon_hp_scroll", 4, 0);
            e[1] = Basit("armor_scroll_150", "Scroll of Armor 150(L)", "ikon_zirh_scroll", 3, 0);
            e[2] = Basit("speed_potion", "Speed-Up Potion", "ikon_hiz_iksiri", 2, 0);
            e[4] = ShortBow();
            e[5] = Basit("ornek_eldiven", "Ornek eldiven", "ikon_eldiven", 1, 0);
            e[6] = Basit("ornek_yuzuk", "Ornek yuzuk", "ikon_yuzuk", 1, 0);
            e[7] = Basit("ornek_asa", "Ornek asa", "ikon_asa", 1, 0);
            e[9] = Basit("ornek_zirh", "Ornek zirh", "ikon_zirh", 1, 0);
            e[10] = Basit("ornek_bilezik", "Ornek bilezik", "ikon_bilezik", 1, 0);
            e[11] = Basit("ornek_kupe_1", "Ornek kupe", "ikon_kupe", 1, 0);
            e[12] = Basit("ornek_kupe_2", "Ornek kupe", "ikon_kupe", 1, 0);
            e[13] = Basit("ornek_pantolon", "Ornek pantolon", "ikon_pantolon", 1, 0);
            e[15] = Basit("ornek_sopa", "Ornek sopa", "ikon_sopa", 1, 0);
            e[16] = Basit("ornek_sopa_8", "Ornek sopa(+8)", "ikon_sopa", 1, 8);
            return e;
        }

        // =====================================================================
        // yardimcilar
        /// <summary>Esya yuvasi: (x,y,w,h) yuvanin cerceve kutusu; ikon 8 px icerde.</summary>
        static OlymposTicariYuva Yuva(GameObject parent, string name, float x, float y, float w, float h, string doluSprite)
        {
            var go = new GameObject(name, typeof(RectTransform));
            Place(go, parent, Mathf.Round(x), Mathf.Round(y), w, h);
            var tik = go.AddComponent<Image>(); tik.color = new Color(0f, 0f, 0f, 0f); tik.raycastTarget = true;
            var yv = go.AddComponent<OlymposTicariYuva>();
            yv.dugme = go.AddComponent<Button>(); yv.dugme.targetGraphic = tik; yv.dugme.transition = Selectable.Transition.None;
            yv.ikon = Img(go, "Icon", null, 8, 8, w - 16, h - 16);
            yv.ikon.enabled = false;
            yv.doluCerceve = Img(go, "FilledFrame", doluSprite, 0, 0, w, h);
            yv.doluCerceve.enabled = false;
            int p1 = Mathf.RoundToInt(h * 0.33f), p2 = Mathf.RoundToInt(h * 0.27f);
            // "+N": sag ust, mor ; adet: sag alt, beyaz + dis hat
            yv.yukseltmeText = Txt(go, "Upgrade", "", 0, 11 - p1 * 0.14f, w - 10, p1 + 6, Roboto, p1, Etiket, TextAnchor.UpperRight);
            yv.adetText = Txt(go, "Count", "", 0, h - 8 - (p2 + 6), w - 11, p2 + 6, Roboto, p2, Pembe, TextAnchor.LowerRight);
            var o = yv.adetText.gameObject.AddComponent<Outline>();
            o.effectColor = new Color(0f, 0f, 0f, 0.95f); o.effectDistance = new Vector2(1f, -1f);
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

        static GameObject Kutu(GameObject parent, string name, Capa capa, float x, float y, float w, float h)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent.transform, false);
            rt.sizeDelta = new Vector2(w, h);
            switch (capa)
            {
                case Capa.SolUst:
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0f, 1f);
                    rt.anchoredPosition = new Vector2(x, -y); break;
                case Capa.SagUst:
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(1f, 1f);
                    rt.anchoredPosition = new Vector2(-(EW - (x + w)), -y); break;
                default:
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                    rt.anchoredPosition = new Vector2(x + w * 0.5f - EW * 0.5f, EH * 0.5f - (y + h * 0.5f)); break;
            }
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

        static Button SpriteBtn(GameObject parent, string name, string sprite, float x, float y, float w, float h)
        {
            var img = Img(parent, name, sprite, x, y, w, h);
            img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>();
            b.targetGraphic = img;
            Renkler(b);
            return b;
        }

        static void Renkler(Button b)
        {
            b.transition = Selectable.Transition.ColorTint;
            var cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white; cb.highlightedColor = Color.white;
            cb.pressedColor = new Color(0.72f, 0.72f, 0.72f, 1f);
            cb.selectedColor = Color.white; cb.disabledColor = new Color(1f, 1f, 1f, 0.45f);
            cb.colorMultiplier = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
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
            var guids = AssetDatabase.FindAssets("OlymposMerchantBuilder t:MonoScript");
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
