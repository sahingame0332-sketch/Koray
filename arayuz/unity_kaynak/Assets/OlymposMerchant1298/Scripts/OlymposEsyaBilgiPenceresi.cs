// OLYMPOS-KO · 1298 esya bilgi penceresi (envanter / ekipman / NPC dukkani / Merchant)
// Tek pencere, dort kullanim (hepsi ayni yerlesim; fark: fiyat satiri ve dugmeler):
//   envanter esyasi      : fiyat yok          · Equip  + Close
//   kusanilmis esya      : fiyat yok          · UnEquip + Close
//   NPC dukkani          : "Buy Price : 3,188" (sari)        · Close
//   Create a Merchant    : "Purchase Price : 99,999" (mor)   · Remove + Close
//   Merchant penceresi   : "Purchase Price : ..."            · Close
//   tezgah cubugu yuvasi : fiyat yok          · Close
// Zemin siyah, alfa 0.93. Yerlesim icerikle buyur; butun araliklar ekran goruntulerinden olculdu.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposBilgiDugmesi { Yok, Equip, UnEquip, Remove }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Esya Bilgi Penceresi")]
    public class OlymposEsyaBilgiPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;

        [Header("Icerik")]
        public Image iconImage;
        public Text nameText;
        public Text typeText;
        public Text priceText;
        public Text[] statTexts = new Text[0];
        public Text[] centerTexts = new Text[0];
        public RectTransform[] separators = new RectTransform[3];

        [Header("Dugmeler")]
        public Button equipButton;
        public Button unEquipButton;
        public Button removeButton;
        public Button closeButton;

        [Header("Renkler (olculen)")]
        public Color beyaz = new Color32(0xFF, 0xE7, 0xE9, 0xFF);
        public Color bonus = new Color32(0x98, 0xBF, 0x2A, 0xFF);
        public Color zehir = new Color32(0x81, 0xC2, 0x67, 0xFF);
        public Color kirmizi = new Color32(0xFE, 0x00, 0x01, 0xFF);
        public Color derece = new Color32(0x88, 0xC2, 0x73, 0xFF);
        public Color buyPriceRengi = new Color32(0xFB, 0xD2, 0x0C, 0xFF);
        public Color purchasePriceRengi = new Color32(0xB4, 0x2A, 0x99, 0xFF);

        [Header("Yerlesim (olculen, px)")]
        public float enAzGenislik = 346f;
        [Tooltip("Ilk ayirici: fiyat satiri yokken / varken")]
        public float ayirici1Fiyatsiz = 147f, ayirici1Fiyatli = 194f;
        public float statIlk = 36f, statAdim = 38.7f, statSonrasi = 48f;
        public float ortaIlk = 35f, ortaAdim = 31.5f, ortaSonrasi = 59f;
        public float dugmeBoslugu = 13f, dugmeAdimi = 161f;
        [Tooltip("Pencerenin sag-ust kosesinin, dokunulan yuvanin merkezine gore konumu (olculen: -34, +17).")]
        public Vector2 yuvaOfseti = new Vector2(-34f, 17f);
        [Tooltip("Pencerenin alt kenari ekranin altindan en az bu kadar yukarida kalir (olculen: 100).")]
        public float altBosluk = 100f;

        [Header("Olaylar")]
        public OlymposTicariEsyaOlayi onEquip = new OlymposTicariEsyaOlayi();
        public OlymposTicariEsyaOlayi onUnEquip = new OlymposTicariEsyaOlayi();
        public OlymposTicariEsyaOlayi onRemove = new OlymposTicariEsyaOlayi();
        public UnityEvent onClosed = new UnityEvent();

        public OlymposTicariEsya Esya { get; private set; }
        Action<OlymposTicariEsya> tekSeferlik;     // bu acilisa ozel dugme islemi

        void Awake()
        {
            if (equipButton != null) equipButton.onClick.AddListener(delegate { Sec(onEquip); });
            if (unEquipButton != null) unEquipButton.onClick.AddListener(delegate { Sec(onUnEquip); });
            if (removeButton != null) removeButton.onClick.AddListener(delegate { Sec(onRemove); });
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Sec(OlymposTicariEsyaOlayi olay)
        {
            var e = Esya; var ozel = tekSeferlik;
            Kapat();
            if (e == null) return;
            if (ozel != null) ozel(e); else olay.Invoke(e);
        }

        public void Kapat()
        {
            tekSeferlik = null;
            if (!gameObject.activeSelf) return;
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        Color Renk(OlymposBilgiRengi r)
        {
            switch (r)
            {
                case OlymposBilgiRengi.Bonus: return bonus;
                case OlymposBilgiRengi.Zehir: return zehir;
                case OlymposBilgiRengi.Kirmizi: return kirmizi;
                default: return beyaz;
            }
        }

        // ---- kisa yollar
        public void GosterEnvanter(OlymposTicariEsya e, RectTransform yuva) { Goster(e, null, 0, beyaz, e != null && e.kusanilir ? OlymposBilgiDugmesi.Equip : OlymposBilgiDugmesi.Yok, yuva, null); }
        public void GosterKusanilmis(OlymposTicariEsya e, RectTransform yuva) { Goster(e, null, 0, beyaz, OlymposBilgiDugmesi.UnEquip, yuva, null); }
        public void GosterNpc(OlymposTicariEsya e, RectTransform yuva) { if (e != null) Goster(e, "Buy Price : ", e.npcFiyati, buyPriceRengi, OlymposBilgiDugmesi.Yok, yuva, null); }
        public void GosterTezgahKurulum(OlymposTicariEsya e, RectTransform yuva, Action<OlymposTicariEsya> kaldir) { if (e != null) Goster(e, "Purchase Price : ", e.tezgahFiyati, purchasePriceRengi, OlymposBilgiDugmesi.Remove, yuva, kaldir); }
        public void GosterTezgah(OlymposTicariEsya e, RectTransform yuva) { if (e != null) Goster(e, "Purchase Price : ", e.tezgahFiyati, purchasePriceRengi, OlymposBilgiDugmesi.Yok, yuva, null); }
        public void GosterFiyatsiz(OlymposTicariEsya e, RectTransform yuva) { Goster(e, null, 0, beyaz, OlymposBilgiDugmesi.Yok, yuva, null); }

        /// <summary>fiyatEtiketi null ise fiyat satiri yazilmaz. dugmeIslemi verilirse sol dugme olay yerine onu cagirir.</summary>
        public void Goster(OlymposTicariEsya e, string fiyatEtiketi, long fiyat, Color fiyatRengi,
                           OlymposBilgiDugmesi solDugme, RectTransform yuva, Action<OlymposTicariEsya> dugmeIslemi)
        {
            if (e == null) return;
            Esya = e; tekSeferlik = dugmeIslemi;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();

            if (iconImage != null) { iconImage.sprite = e.ikon; iconImage.enabled = e.ikon != null; }
            nameText.text = e.ad; nameText.color = e.adRengi;
            typeText.text = string.IsNullOrEmpty(e.turSatiri) ? "-" : e.turSatiri; typeText.color = e.adRengi;
            float sag = nameText.rectTransform.anchoredPosition.x + Mathf.Max(nameText.preferredWidth, typeText.preferredWidth);

            bool fiyatli = fiyatEtiketi != null;
            priceText.gameObject.SetActive(fiyatli);
            if (fiyatli)
            {
                priceText.text = fiyatEtiketi + OlymposTicariBicim.Para(fiyat);
                priceText.color = fiyatRengi;
                sag = Mathf.Max(sag, priceText.rectTransform.anchoredPosition.x + priceText.preferredWidth);
            }

            float s1 = fiyatli ? ayirici1Fiyatli : ayirici1Fiyatsiz;
            int n = e.statlar != null ? Mathf.Min(e.statlar.Length, statTexts.Length) : 0;
            for (int i = 0; i < statTexts.Length; i++)
            {
                var t = statTexts[i];
                bool acik = i < n;
                t.gameObject.SetActive(acik);
                if (!acik) continue;
                t.text = e.statlar[i].metin; t.color = Renk(e.statlar[i].renk);
                UstY(t, s1 + statIlk + statAdim * i);
                sag = Mathf.Max(sag, t.rectTransform.anchoredPosition.x + t.preferredWidth);
            }
            float genislik = Mathf.Max(enAzGenislik, Mathf.Ceil(sag + 33f));
            float s2 = n > 0 ? s1 + statIlk + statAdim * (n - 1) + statSonrasi : s1 + 30f;

            // ortali blok: [sinif] · [bos satir + cins] · derece · aciklama satirlari
            int k = 0;
            if (!string.IsNullOrEmpty(e.sinifSatiri)) Orta(k++, e.sinifSatiri, e.sinifUygun ? beyaz : kirmizi, s2, genislik);
            if (!string.IsNullOrEmpty(e.cinsSatiri)) { Orta(k++, "", beyaz, s2, genislik); Orta(k++, e.cinsSatiri, beyaz, s2, genislik); }
            if (!string.IsNullOrEmpty(e.dereceSatiri)) Orta(k++, e.dereceSatiri, derece, s2, genislik);
            if (!string.IsNullOrEmpty(e.aciklama))
            {
                string[] satirlar = e.aciklama.Split('\n');
                for (int i = 0; i < satirlar.Length; i++) Orta(k++, satirlar[i], beyaz, s2, genislik);
            }
            for (int i = k; i < centerTexts.Length; i++) centerTexts[i].gameObject.SetActive(false);
            float s3 = s2 + ortaIlk + ortaAdim * Mathf.Max(0, k - 1) + ortaSonrasi;
            float dugmeY = s3 + dugmeBoslugu;

            float[] ay = { s1, s2, s3 };
            for (int i = 0; i < separators.Length && i < 3; i++)
            {
                if (separators[i] == null) continue;
                separators[i].anchoredPosition = new Vector2(12f, -ay[i]);
                separators[i].sizeDelta = new Vector2(genislik - 26f, separators[i].sizeDelta.y);
            }

            Button sol = solDugme == OlymposBilgiDugmesi.Equip ? equipButton
                       : solDugme == OlymposBilgiDugmesi.UnEquip ? unEquipButton
                       : solDugme == OlymposBilgiDugmesi.Remove ? removeButton : null;
            Button[] hepsi = { equipButton, unEquipButton, removeButton };
            for (int i = 0; i < hepsi.Length; i++) if (hepsi[i] != null) hepsi[i].gameObject.SetActive(hepsi[i] == sol);
            float x = 12f;
            if (sol != null) { ((RectTransform)sol.transform).anchoredPosition = new Vector2(x, -dugmeY); x += dugmeAdimi; }
            if (closeButton != null) ((RectTransform)closeButton.transform).anchoredPosition = new Vector2(x, -dugmeY);

            var kendi = (RectTransform)transform;
            kendi.sizeDelta = new Vector2(genislik, Mathf.Round(dugmeY + 65f));
            Yerlestir(kendi, yuva);
        }

        void Orta(int i, string metin, Color renk, float s2, float genislik)
        {
            if (i >= centerTexts.Length) return;
            var t = centerTexts[i];
            t.gameObject.SetActive(true);
            t.text = metin; t.color = renk;
            var rt = t.rectTransform;
            rt.sizeDelta = new Vector2(genislik, rt.sizeDelta.y);
            rt.anchoredPosition = new Vector2(0f, rt.anchoredPosition.y);
            UstY(t, s2 + ortaIlk + ortaAdim * i);
        }

        // Yazinin ust kenari (buyuk harf / cikinti tepesi) "y" olsun: kutu, punto ile orantili bir payla yukari alinir.
        static void UstY(Text t, float y)
        {
            var rt = t.rectTransform;
            float pay = (rt.sizeDelta.y - t.fontSize * 0.72f) * 0.5f;
            rt.anchoredPosition = new Vector2(rt.anchoredPosition.x, -(y - pay));
        }

        // Olculen kural: pencerenin sag-ust kosesi = yuva merkezi + (-34, +17 asagi); alt kenar ekran altindan 100 px yukarida kalir.
        void Yerlestir(RectTransform kendi, RectTransform yuva)
        {
            var ust = kendi.parent as RectTransform;
            if (ust == null) return;
            Rect r = ust.rect;
            float w = kendi.sizeDelta.x, h = kendi.sizeDelta.y;
            float solX, ustY;      // ust nesnenin sol-ust kosesine gore, y asagi
            if (yuva != null)
            {
                Vector3 dunya = yuva.TransformPoint(new Vector3((0.5f - yuva.pivot.x) * yuva.rect.width, (0.5f - yuva.pivot.y) * yuva.rect.height, 0f));
                Vector3 yerel = ust.InverseTransformPoint(dunya);
                solX = (yerel.x - r.xMin) + yuvaOfseti.x - w;
                ustY = (r.yMax - yerel.y) - yuvaOfseti.y;
            }
            else { solX = (r.width - w) * 0.5f; ustY = (r.height - h) * 0.5f; }
            if (ustY + h > r.height - altBosluk) ustY = r.height - altBosluk - h;
            if (ustY < 0f) ustY = 0f;
            if (solX < 0f) solX = 0f;
            if (solX + w > r.width) solX = r.width - w;
            kendi.anchorMin = kendi.anchorMax = new Vector2(0f, 1f);
            kendi.pivot = new Vector2(0f, 1f);
            kendi.anchoredPosition = new Vector2(solX, -ustY);
        }
    }
}
