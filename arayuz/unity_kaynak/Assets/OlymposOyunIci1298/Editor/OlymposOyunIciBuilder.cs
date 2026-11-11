// OLYMPOS-KO · 1298 oyun ici ogeler — kurucu (sadece Editor)
// Menu: OLYMPOS > 1298 > Oyun İçi (Scroll · Skill Slot · Drops · Hedef) Oluştur
// Butun olculer 2712 x 1220 oyun kayitlarindan alindi — arayuz/06-oyun-ici.md
// Koordinatlar ekranin sol-ust kosesine gore pikseldir; her oge kendi kosesine capalanir.
using System.Collections.Generic;
using System.IO;
using Olympos.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI.EditorTools
{
    public static class OlymposOyunIciBuilder
    {
        const float EW = 2712f, EH = 1220f;                 // referans ekran
        const string Klasor = "OlymposOyunIci1298";
        const string CanvasAdi = "OlymposOyunIciCanvas (2712x1220)";

        static readonly Color Pembe  = Hex("#FFE7E9");      // esya/ipucu yazilarinin beyazi (hafif pembe, olculdu)
        static readonly Color Beyaz  = Color.white;
        static readonly Color Sari   = Hex("#FCD100");
        static readonly Color Altin  = Hex("#E3B170");
        static readonly Color Mor    = Hex("#CA89E7");

        static string Root;
        static Font Roboto, Slab, SlabInce, DejaVu;

        enum Capa { SolUst, SagUst, SagAlt, UstOrta, Orta }

        // hizli slot merkezleri (ekran pikseli) — okuma sirasiyla
        static readonly Vector2[] SlotMerkezleri = {
            new Vector2(2193, 452),
            new Vector2(1840, 595), new Vector2(2030, 595), new Vector2(1657, 634), new Vector2(2235, 634), new Vector2(2431, 638),
            new Vector2(1893, 770), new Vector2(2085, 781), new Vector2(1541, 799), new Vector2(1722, 799),
            new Vector2(1547, 961), new Vector2(1715, 961), new Vector2(1889, 968), new Vector2(2084, 971)
        };

        [MenuItem("OLYMPOS/1298/Oyun İçi (Scroll · Skill Slot · Drops · Hedef) Oluştur")]
        public static void Build()
        {
            Root = FindRoot();
            string[] dokular = {
                "btn_use_self", "btn_use_target", "btn_equip", "btn_close_kirmizi", "ikon_cerceve",
                "ikon_hp_scroll", "ikon_hiz_iksiri", "ikon_zirh_scroll", "buff_cerceve", "menu_ok", "btn_remove", "btn_menu_close",
                "slot_halka", "slot_maske", "btn_hedef_iptal", "hedef_cubuk", "btn_show_drops",
                "drop_krom", "onay_isareti", "drop_yer_tutucu", "drop_slot_dolu", "drop_grup", "drop_ornek_temiz", "saveslot_krom",
                "drop_ornek_0", "drop_ornek_1", "drop_ornek_2", "drop_ornek_3", "drop_ornek_4",
                "drop_ornek_5", "drop_ornek_6", "drop_ornek_7", "drop_ornek_8", "drop_ornek_9" };
            foreach (var d in dokular) Tex(d);
            AssetDatabase.Refresh();
            Roboto   = LoadFont("Roboto-Bold.ttf");
            Slab     = LoadFont("RobotoSlab-Bold.ttf");
            SlabInce = LoadFont("RobotoSlab-Regular.otf") ?? Slab;
            DejaVu   = LoadFont("DejaVuSans-Bold.ttf") ?? Roboto;

            var root = new GameObject("OyunIci_1298", typeof(RectTransform));
            var rrt = (RectTransform)root.transform;
            rrt.anchorMin = Vector2.zero; rrt.anchorMax = Vector2.one;
            rrt.offsetMin = Vector2.zero; rrt.offsetMax = Vector2.zero;      // Canvas'i tam kaplar
            var yon = root.AddComponent<OlymposOyunIciYonetici>();

            yon.slotCubugu   = BuildSlotlar(root);
            yon.hedefCubugu  = BuildHedef(root);
            yon.buffCubugu   = BuildBuff(root);
            var demoYuvalar  = BuildDemoEnvanter(root, yon);
            yon.saveSkillSlot = BuildSaveSlot(root);
            yon.dropListesi  = BuildDrop(root);
            yon.esyaPenceresi = BuildEsyaPenceresi(root);
            yon.envanterYuvalari = demoYuvalar;
            yon.saveSkillSlotAcDugmesi = DemoDugme(demoYuvalar[0].transform.parent.gameObject, "Btn_SaveSkillSlot (deneme)", "Save skill slot", 0, 136, 200, 40);
            yon.saveSkillSlot.slotCubugu = yon.slotCubugu;

            // gerilen kok icin dogru yerlesim: once kaydet, sonra Canvas altinda tam ekran
            SaveAndPlace(root, "OyunIci_1298");
        }

        // =====================================================================
        // 1) Esya eylem penceresi — 663 x 313, zemin alfa 0.92
        static OlymposEsyaPenceresi BuildEsyaPenceresi(GameObject parent)
        {
            var go = Kutu(parent, "EsyaPenceresi", Capa.SolUst, 1360, 740, 663, 313);
            var p = go.AddComponent<OlymposEsyaPenceresi>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, p.backgroundAlpha); bg.raycastTarget = true;
            p.background = bg;

            p.iconImage = Img(go, "Icon", null, 9, 9, 89, 89);
            Img(go, "IconFrame", "ikon_cerceve", 2, 2, 103, 103);
            p.nameText = Txt(go, "Name", "Scroll of 500HP Up(L)", 113, 2, 540, 45, Roboto, 36, Pembe, TextAnchor.MiddleLeft);
            p.typeText = Txt(go, "Type", "Store Item", 113, 44, 540, 32, Roboto, 27, Sari, TextAnchor.MiddleLeft);
            p.descriptionText = Txt(go, "Description", "Increases HP by 500.", 12, 171, 474, 32, Roboto, 27, Pembe, TextAnchor.MiddleCenter);
            var ay = Img(go, "Separator", null, 11, 236, 475, 1);
            ay.color = Hex("#41342E");
            p.separator = ay.rectTransform;

            p.useSelfButton   = SpriteBtn(go, "Btn_UseSelf",   "btn_use_self",      11, 248, 155, 62);
            p.useTargetButton = SpriteBtn(go, "Btn_UseTarget", "btn_use_target",    173, 248, 155, 62);
            p.equipButton     = SpriteBtn(go, "Btn_Equip",     "btn_equip",         334, 248, 156, 62);
            p.closeButton     = SpriteBtn(go, "Btn_Close",     "btn_close_kirmizi", 496, 248, 155, 62);
            return p;
        }

        // =====================================================================
        // 2) Buff cubugu — ikon 64, adim 66, sag kenar x=2309, ust y=56 ; menu ikonun altinda
        static OlymposBuffCubugu BuildBuff(GameObject parent)
        {
            const int N = 8;
            float w = N * 66f - 2f;
            var go = Kutu(parent, "BuffCubugu", Capa.SagUst, 2309 - w, 56, w, 64);
            var b = go.AddComponent<OlymposBuffCubugu>();
            b.hucreler = new OlymposBuffCubugu.Hucre[N];
            for (int i = 0; i < N; i++)
            {
                var h = new OlymposBuffCubugu.Hucre();
                var kok = new GameObject("Buff_" + i, typeof(RectTransform));
                Place(kok, go, i * 66f, 0, 64, 64);
                var tik = kok.AddComponent<Image>(); tik.color = new Color(0f, 0f, 0f, 0f); tik.raycastTarget = true;
                h.dugme = kok.AddComponent<Button>(); h.dugme.targetGraphic = tik; h.dugme.transition = Selectable.Transition.None;
                h.ikon = Img(kok, "Icon", null, 3, 3, 58, 58);
                Img(kok, "Frame", "buff_cerceve", 0, 0, 64, 64);
                h.sure = Txt(kok, "Time", "59m", -8, 36, 80, 30, Roboto, 27, Pembe, TextAnchor.MiddleCenter);
                Dishat(h.sure, 1f);
                h.kok = kok;
                kok.SetActive(false);
                b.hucreler[i] = h;
            }
            // menu: ok (30x18) + Remove (194x66) + Close (194x64); ikon sol kenarina gore x = -65
            var menu = new GameObject("Menu", typeof(RectTransform));
            Place(menu, go, 0, 64, 194, 150);
            Img(menu, "Arrow", "menu_ok", 82, 0, 30, 18);
            b.removeButton    = SpriteBtn(menu, "Btn_Remove", "btn_remove", 0, 16, 194, 66);
            b.menuCloseButton = SpriteBtn(menu, "Btn_Close", "btn_menu_close", 0, 86, 194, 64);
            b.menu = (RectTransform)menu.transform;
            menu.SetActive(false);
            return b;
        }

        // =====================================================================
        // 3) Hizli slotlar — halka 164, ic disk 144 (bosken siyah alfa 0.88), adet punto 31
        static OlymposHizliSlotCubugu BuildSlotlar(GameObject parent)
        {
            const float X0 = 1459, Y0 = 370, W = 1054, H = 683;      // slotlarin sinir kutusu
            var go = Kutu(parent, "HizliSlotCubugu", Capa.SagAlt, X0, Y0, W, H);
            var c = go.AddComponent<OlymposHizliSlotCubugu>();
            c.slotlar = new OlymposHizliSlot[SlotMerkezleri.Length];
            for (int i = 0; i < SlotMerkezleri.Length; i++)
            {
                float cx = SlotMerkezleri[i].x - X0, cy = SlotMerkezleri[i].y - Y0;
                var s = new GameObject("Slot_" + i, typeof(RectTransform));
                Place(s, go, cx - 82, cy - 82, 164, 164);
                var tik = s.AddComponent<Image>(); tik.color = new Color(0f, 0f, 0f, 0f); tik.raycastTarget = true;
                var hs = s.AddComponent<OlymposHizliSlot>();

                var bos = Img(s, "Empty", "slot_maske", 10, 10, 144, 144);
                bos.color = new Color(0f, 0f, 0f, 0.88f);
                hs.bosZemin = bos;

                var maske = Img(s, "IconMask", "slot_maske", 9, 9, 146, 146);
                var m = maske.gameObject.AddComponent<Mask>(); m.showMaskGraphic = false;
                hs.ikon = Img(maske.gameObject, "Icon", null, 0, 0, 146, 146);
                hs.ikonKoku = maske.gameObject;
                maske.gameObject.SetActive(false);

                Img(s, "Ring", "slot_halka", 0, 0, 164, 164);
                hs.adetText = Txt(s, "Count", "", 42, 114, 80, 38, Roboto, 31, Beyaz, TextAnchor.MiddleCenter);
                Dishat(hs.adetText, 1f);
                hs.adetText.gameObject.SetActive(false);
                hs.cubuk = c; hs.sira = i;
                c.slotlar[i] = hs;
            }
            return c;
        }

        // =====================================================================
        // 4) Hedef cubugu + Show Drops (ust orta) ve hedef iptal X (sag alt)
        static OlymposHedefCubugu BuildHedef(GameObject parent)
        {
            var kok = new GameObject("Hedef", typeof(RectTransform));
            var krt = (RectTransform)kok.transform;
            krt.SetParent(parent.transform, false);
            krt.anchorMin = Vector2.zero; krt.anchorMax = Vector2.one; krt.offsetMin = Vector2.zero; krt.offsetMax = Vector2.zero;
            var h = kok.AddComponent<OlymposHedefCubugu>();

            // cubuk kutusu: x 1178..1582, y 56..190
            var cub = Kutu(kok, "Cubuk", Capa.UstOrta, 1178, 56, 404, 134);
            h.cubukKoku = cub;
            // ad merkezi: ekran (1370, 75) -> kutu ici (192, 19); uzun adlar icin 600 px genis kutu
            h.adText = Txt(cub, "Name", "Kecoon fighter", 192 - 300, 0, 600, 38, DejaVu, 30, Hex("#FE5356"), TextAnchor.MiddleCenter);
            Dishat(h.adText, 2f, Hex("#460C0E"));
            // can cubugu: bos hali kareler arasinda gorulmedi -> ayni sprite koyulastirilarak oluk yapildi (varsayim)
            var oluk = Img(cub, "HpTrough", "hedef_cubuk", 0, 40, 404, 41);
            oluk.color = new Color(0.22f, 0.22f, 0.22f, 1f);
            var dolgu = Img(cub, "HpFill", "hedef_cubuk", 0, 40, 404, 41);
            dolgu.type = Image.Type.Filled; dolgu.fillMethod = Image.FillMethod.Horizontal;
            dolgu.fillOrigin = 0; dolgu.fillAmount = 1f;
            h.canDolgu = dolgu;
            h.seviyeText = Txt(cub, "Level", "Lv.12", 12, 50, 120, 22, DejaVu, 16, Hex("#8EE13A"), TextAnchor.MiddleLeft);
            Dishat(h.seviyeText, 1f, Hex("#14320A"));
            h.showDropsButton = SpriteBtn(cub, "Btn_ShowDrops", "btn_show_drops", 120, 78, 152, 54);

            // hedef iptal: 140 x 140, sol-ust (2503, 784)
            var x = Kutu(kok, "Btn_HedefIptal", Capa.SagAlt, 2503, 784, 140, 140);
            var xi = x.AddComponent<Image>(); xi.sprite = Spr("btn_hedef_iptal"); xi.raycastTarget = true;
            var xb = x.AddComponent<Button>(); xb.targetGraphic = xi; Renkler(xb);
            h.iptalButton = xb;
            return h;
        }

        // =====================================================================
        // 5) Drop List Search — 698 x 1116, sol-ust (176, 82), zemin alfa 0.89
        static OlymposDropListesi BuildDrop(GameObject parent)
        {
            var go = Kutu(parent, "DropListesi", Capa.SolUst, 176, 82, 698, 1116);
            var d = go.AddComponent<OlymposDropListesi>();
            var bg = Img(go, "Background", null, 6, 8, 683, 1107);
            bg.color = new Color(0f, 0f, 0f, d.backgroundAlpha); bg.raycastTarget = true;
            d.background = bg;
            Img(go, "Krom", "drop_krom", 0, 0, 698, 1116);

            d.closeButton = Hit(go, "Btn_Close", 620, 2, 62, 62);
            d.monsterToggle = Hit(go, "Toggle_Monster", 30, 82, 220, 64);
            d.itemToggle    = Hit(go, "Toggle_ItemName", 30, 158, 260, 64);
            d.monsterCheck = Img(go, "Check_Monster", "onay_isareti", 28, 74, 76, 78);
            d.itemCheck    = Img(go, "Check_ItemName", "onay_isareti", 28, 150, 76, 78);
            d.itemCheck.enabled = false;

            // arama alani (cerceve kromda): 31,243 648x65
            var alan = new GameObject("SearchField", typeof(RectTransform));
            Place(alan, go, 40, 250, 630, 51);
            var ai = alan.AddComponent<Image>(); ai.color = new Color(0f, 0f, 0f, 0f); ai.raycastTarget = true;
            var f = alan.AddComponent<InputField>();
            f.targetGraphic = ai;
            f.textComponent = Txt(alan, "Text", "", 10, 0, 610, 51, SlabInce, 26, Beyaz, TextAnchor.MiddleCenter);
            var yt = Img(alan, "Placeholder", "drop_yer_tutucu", 110, 6, 406, 36);   // orijinal piksel: "Enter Your Monster or Item Name...."
            f.placeholder = yt;
            f.characterLimit = 32;
            d.searchField = f;

            // sonuc listesi: 34,314 642x323 -> 5 satir, adim 64.6
            for (int i = 0; i < OlymposDropListesi.SonucSatiri; i++)
            {
                float y = 314 + 64.6f * i;
                d.resultButtons[i] = Hit(go, "Result_" + i, 36, y + 2, 638, 61);
                d.resultTexts[i] = Txt(go, "ResultText_" + i, "", 52, y + 2, 606, 61, SlabInce, 28, Beyaz, TextAnchor.MiddleLeft);
            }
            d.resultPrev = Hit(go, "Btn_ResultPrev", 237, 645, 56, 44);
            d.resultNext = Hit(go, "Btn_ResultNext", 408, 646, 56, 44);
            d.resultPageText = Txt(go, "ResultPage", "0/0", 300, 648, 101, 42, SlabInce, 32, Altin, TextAnchor.MiddleCenter);

            // kutular: x = 64 + 115c, y = 703 + 111r, 103 x 103 ; ikon ic 89 (7 px icerde)
            for (int r = 0; r < OlymposDropListesi.Satir; r++)
                for (int c = 0; c < OlymposDropListesi.Sutun; c++)
                {
                    int i = r * OlymposDropListesi.Sutun + c;
                    float x = 64 + 115f * c, y = 703 + 111f * r;
                    d.slotIcons[i] = Img(go, "SlotIcon_" + i, null, x + 7, y + 7, 89, 89);
                    d.slotIcons[i].enabled = false;
                    d.slotFrames[i] = Img(go, "SlotFrame_" + i, "drop_slot_dolu", x, y, 103, 103);
                    d.slotFrames[i].enabled = false;
                    // oran etiketi: sag alt, yazi sagi x+97 ; siyah zemin yaziya gore genisler
                    var eb = new GameObject("SlotLabelBg_" + i, typeof(RectTransform));
                    var ert = (RectTransform)eb.transform;
                    ert.SetParent(go.transform, false);
                    ert.anchorMin = ert.anchorMax = new Vector2(0f, 1f); ert.pivot = new Vector2(1f, 1f);
                    ert.anchoredPosition = new Vector2(x + 99f, -(y + 75f)); ert.sizeDelta = new Vector2(68f, 23f);
                    var ei = eb.AddComponent<Image>(); ei.color = Color.black; ei.raycastTarget = false;
                    d.slotLabelBgs[i] = ert;
                    d.slotLabels[i] = Txt(go, "SlotLabel_" + i, "Middle", x - 3, y + 74, 100, 25, Slab, 19, Beyaz, TextAnchor.MiddleRight);
                    eb.SetActive(false); d.slotLabels[i].gameObject.SetActive(false);
                    d.slotButtons[i] = Hit(go, "Slot_" + i, x, y, 103, 103);
                }
            d.gridPrev = Hit(go, "Btn_GridPrev", 213, 1032, 72, 67);
            d.gridNext = Hit(go, "Btn_GridNext", 417, 1031, 69, 68);
            d.gridPageText = Txt(go, "GridPage", "1/1", 292, 1050, 121, 46, SlabInce, 32, Altin, TextAnchor.MiddleCenter);

            d.tooltip = BuildIpucu(go);
            d.veritabani = OrnekDroplar();
            go.SetActive(false);
            return d;
        }

        // ipucu — ornek kutu 484 x 621 ; pencere icindeki yeri (415, 417)
        static OlymposDropIpucu BuildIpucu(GameObject parent)
        {
            var go = new GameObject("Ipucu", typeof(RectTransform));
            Place(go, parent, 415, 417, 484, 621);
            var t = go.AddComponent<OlymposDropIpucu>();
            var bg = go.AddComponent<Image>();
            bg.color = new Color(0f, 0f, 0f, t.backgroundAlpha); bg.raycastTarget = true;
            t.background = bg;
            t.iconImage = Img(go, "Icon", null, 12, 12, 89, 89);
            Img(go, "IconFrame", "ikon_cerceve", 5, 5, 103, 103);
            t.nameText = Txt(go, "Name", "", 115, 2, 600, 45, Roboto, 36, Mor, TextAnchor.MiddleLeft);
            t.typeText = Txt(go, "Type", "", 115, 44, 600, 32, Roboto, 27, Mor, TextAnchor.MiddleLeft);
            t.dropRateLabel = Txt(go, "DropRateLabel", "Drop Rate :", 13, 132, 300, 38, Roboto, 32, Hex("#FF1000"), TextAnchor.MiddleLeft);
            t.dropRateValue = Txt(go, "DropRateValue", "Middle", 183, 132, 300, 38, Roboto, 32, Pembe, TextAnchor.MiddleLeft);
            t.statTexts = new Text[6];
            for (int i = 0; i < 6; i++)
                t.statTexts[i] = Txt(go, "Stat_" + i, "", 12, 224 + 38.5f * i, 700, 34, Roboto, 29, Pembe, TextAnchor.MiddleLeft);
            t.classText = Txt(go, "ClassLine", "", 0, 385, 484, 32, Roboto, 27, Hex("#FE0001"), TextAnchor.MiddleCenter);
            t.gradeText = Txt(go, "GradeLine", "", 0, 416, 484, 32, Roboto, 27, Hex("#80C366"), TextAnchor.MiddleCenter);
            t.descriptionText = Txt(go, "Description", "", 12, 447, 458, 64, Roboto, 27, Pembe, TextAnchor.UpperCenter);
            t.descriptionText.horizontalOverflow = HorizontalWrapMode.Wrap;
            t.descriptionText.lineSpacing = 0.98f;       // olculen satir adimi 31 px
            for (int i = 0; i < 3; i++)
            {
                var a = Img(go, "Separator_" + i, null, 12, new float[] { 194, 355, 543 }[i], 458, 1);
                a.color = Hex("#403A37");
                t.separators[i] = a.rectTransform;
            }
            t.closeButton = SpriteBtn(go, "Btn_Close", "btn_close_kirmizi", 12, 556, 155, 62);
            go.SetActive(false);
            return t;
        }

        // =====================================================================
        // 6) Save Skill Slot Stat — 526 x 1056, sol-ust (1196, 110), zemin alfa 0.95
        static OlymposSaveSkillSlot BuildSaveSlot(GameObject parent)
        {
            var go = Kutu(parent, "SaveSkillSlot", Capa.Orta, 1196, 110, 526, 1056);
            var s = go.AddComponent<OlymposSaveSkillSlot>();
            var bg = Img(go, "Background", null, 12, 68, 498, 986);
            bg.color = new Color(0f, 0f, 0f, s.backgroundAlpha); bg.raycastTarget = true;
            s.background = bg;
            var bas = Img(go, "TitleBack", null, 4, 12, 518, 55);      // baslik cubugu opak
            bas.color = Color.black;
            Img(go, "Krom", "saveslot_krom", 0, 0, 526, 1056);
            s.closeButton = Hit(go, "Btn_Close", 462, 2, 64, 64);
            for (int k = 0; k < OlymposSaveSkillSlot.KayitSayisi; k++)
            {
                float y = 85 + 245f * k;
                // durum yazisi: iki satir, satir adimi 42 px, blok merkezi satir basindan 118 px
                var t = Txt(go, "Status_" + k, "- Empty -", 16, y + 76, 494, 84, Slab, 29, Beyaz, TextAnchor.MiddleCenter);
                t.lineSpacing = 1.1f;
                Dishat(t, 1f);
                s.statusTexts[k] = t;
                s.saveButtons[k]     = Hit(go, "Btn_Save_" + k, 26, y + 169, 236, 64);
                s.activateButtons[k] = Hit(go, "Btn_Activate_" + k, 269, y + 169, 236, 64);
            }
            go.SetActive(false);
            return s;
        }

        // =====================================================================
        // Deneme envanteri: mekanigi Unity'de hemen denemek icin 3 yuva (kendi envanterinizle degistirin)
        static OlymposEnvanterYuvasi[] BuildDemoEnvanter(GameObject parent, OlymposOyunIciYonetici yon)
        {
            string[] id   = { "hp_scroll_500", "armor_scroll_150", "speed_potion" };
            string[] ad   = { "Scroll of 500HP Up(L)", "Scroll of Armor 150(L)", "Speed-Up Potion" };
            string[] acik = { "Increases HP by 500.", "Increase Defense by 150", "Increases Speed by 150%." };
            string[] kul  = { "Hp Scroll 500(L)", "Scroll Of Armor 150(L)", "Speed Potion" };
            string[] ikon = { "ikon_hp_scroll", "ikon_zirh_scroll", "ikon_hiz_iksiri" };
            int[] adet    = { 5, 5, 4 };
            var go = Kutu(parent, "DemoEnvanter (kendi envanterinizle degistirin)", Capa.SolUst, 900, 880, 330, 180);
            var et = Txt(go, "Etiket", "DENEME ENVANTERİ — dokun: pencere · sürükle: skill bar", 0, 0, 330, 24, Roboto, 14, Sari, TextAnchor.MiddleLeft);
            et.horizontalOverflow = HorizontalWrapMode.Overflow;
            var yuvalar = new OlymposEnvanterYuvasi[id.Length];
            for (int i = 0; i < id.Length; i++)
            {
                yon.envanter.Add(new OlymposEsya { id = id[i], ad = ad[i], turSatiri = "Store Item", aciklama = acik[i],
                                                   kullanimAdi = kul[i], adet = adet[i], ikon = Spr(ikon[i]), buffSuresi = 3600f });
                var y = new GameObject("Yuva_" + i, typeof(RectTransform));
                Place(y, go, i * 110f, 28, 103, 103);
                var zemin = y.AddComponent<Image>(); zemin.color = new Color(0f, 0f, 0f, 0.6f); zemin.raycastTarget = true;
                var ey = y.AddComponent<OlymposEnvanterYuvasi>();
                ey.ikon = Img(y, "Icon", ikon[i], 7, 7, 89, 89);
                Img(y, "Frame", "ikon_cerceve", 0, 0, 103, 103);
                ey.adetText = Txt(y, "Count", adet[i].ToString(), 40, 70, 54, 28, Roboto, 22, Beyaz, TextAnchor.MiddleRight);
                Dishat(ey.adetText, 1f);
                ey.esyaId = id[i]; ey.yonetici = yon;
                yuvalar[i] = ey;
            }
            return yuvalar;
        }

        static Button DemoDugme(GameObject parent, string name, string yazi, float x, float y, float w, float h)
        {
            var img = Img(parent, name, null, x, y, w, h);
            img.color = new Color(0.12f, 0.14f, 0.2f, 0.95f); img.raycastTarget = true;
            var b = img.gameObject.AddComponent<Button>(); b.targetGraphic = img; Renkler(b);
            Txt(img.gameObject, "Text", yazi, 0, 0, w, h, Slab, 22, Beyaz, TextAnchor.MiddleCenter);
            return b;
        }

        // Videodaki "Kecoon fighter" droplari (ikonlar kareden kesildi; ipucu metni yalniz gorulen esya icin tam)
        static OlymposCanavarDrop[] OrnekDroplar()
        {
            var pauldron = new OlymposDropGirdisi {
                ad = "Quilted Pauldron(+3)", ikon = Spr("drop_ornek_temiz"), oran = "Middle", turSatiri = "Upgrade Item",
                statlar = new[] {
                    new OlymposDropSatiri { metin = "Defense Ability : 28", renk = OlymposSatirRengi.Beyaz },
                    new OlymposDropSatiri { metin = "Health Bonus : 4", renk = OlymposSatirRengi.Yesil },
                    new OlymposDropSatiri { metin = "Required Strenght : 66", renk = OlymposSatirRengi.Kirmizi } },
                sinifSatiri = "(Warrior Item)", dereceSatiri = "Item Grade : Low Class",
                aciklama = "The pauldron worn by\nnovice warriors." };
            var icerik = new List<OlymposDropGirdisi>();
            icerik.Add(pauldron);
            int[] sira = { 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 3, 8, 9 };
            for (int i = 0; i < sira.Length; i++)
                icerik.Add(new OlymposDropGirdisi { ad = "Ornek esya " + (i + 2), ikon = Spr("drop_ornek_" + sira[i]), oran = "Middle" });
            var grup1 = new OlymposDropGirdisi { ad = "GROUP", ikon = Spr("drop_grup"), oran = "Middle", grup = true, grupIcerigi = icerik.ToArray() };
            var grup2 = new OlymposDropGirdisi { ad = "GROUP", ikon = Spr("drop_grup"), oran = "Middle", grup = true, grupIcerigi = icerik.ToArray() };
            var tek = new OlymposDropGirdisi { ad = "Ornek esya 1", ikon = Spr("drop_ornek_0"), oran = "Low" };
            return new[] { new OlymposCanavarDrop { canavarAdi = "Kecoon fighter", droplar = new[] { grup1, grup2, tek } } };
        }

        // =====================================================================
        // yardimcilar
        /// <summary>Ekran pikseli (sol-ust kose) ile yerlesim; secilen ekran kosesine capalanir.</summary>
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
                case Capa.SagAlt:
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(1f, 0f);
                    rt.anchoredPosition = new Vector2(-(EW - (x + w)), EH - (y + h)); break;
                case Capa.UstOrta:
                    rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 1f);
                    rt.anchoredPosition = new Vector2(x + w * 0.5f - EW * 0.5f, -y); break;
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

        static void Dishat(Text t, float kalinlik) { Dishat(t, kalinlik, new Color(0f, 0f, 0f, 0.95f)); }

        static void Dishat(Text t, float kalinlik, Color renk)
        {
            var o = t.gameObject.AddComponent<Outline>();
            o.effectColor = renk;
            o.effectDistance = new Vector2(kalinlik, -kalinlik);
        }

        /// <summary>Yazisi orijinal piksellerden gelen gorunur dugme.</summary>
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
            cb.normalColor      = Color.white;
            cb.highlightedColor = Color.white;
            cb.pressedColor     = new Color(0.72f, 0.72f, 0.72f, 1f);
            cb.selectedColor    = Color.white;
            cb.disabledColor    = new Color(1f, 1f, 1f, 0.45f);
            cb.colorMultiplier  = 1f; cb.fadeDuration = 0.05f;
            b.colors = cb;
            var nav = b.navigation; nav.mode = Navigation.Mode.None; b.navigation = nav;
        }

        /// <summary>Kromun ustundeki gorunmez tiklama alani.</summary>
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
            cb.highlightedColor = new Color(1f, 1f, 1f, 0f);
            cb.pressedColor     = new Color(1f, 1f, 1f, 0.35f);
            cb.selectedColor    = new Color(1f, 1f, 1f, 0f);
            cb.disabledColor    = new Color(1f, 1f, 1f, 0f);
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
            var rt = (RectTransform)inst.transform;
            rt.anchorMin = Vector2.zero; rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero; rt.offsetMax = Vector2.zero;
            Undo.RegisterCreatedObjectUndo(inst, "Create " + prefabName);
            Selection.activeGameObject = inst;
            Debug.Log("[OLYMPOS] Oluşturuldu: " + path);
        }

        static string FindRoot()
        {
            var guids = AssetDatabase.FindAssets("OlymposOyunIciBuilder t:MonoScript");
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
            ti.SaveAndReimport();
        }

        // Bu ogeler 2712 x 1220 kayitlardan olculdu; diger OLYMPOS paketlerinin 1920 x 1080 Canvas'i ile
        // karismamasi icin kendi Canvas'inda dururlar (olcek yukseklige gore: match = 1).
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
