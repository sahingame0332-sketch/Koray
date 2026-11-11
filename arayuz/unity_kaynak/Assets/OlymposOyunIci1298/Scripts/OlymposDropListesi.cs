// OLYMPOS-KO · 1298 "DROP LIST SEARCH" penceresi (698 x 1116)
// Hedef cubugundaki "Show Drops" ile acilir: secili yaratigin droplari 5 x 3 kutuda listelenir.
// GROUP kutusuna basinca icindeki esyalar gelir; esyaya basinca "Drop Rate" ipucu acilir.
// Ustteki arama: Monster / Item Name kipinde ada gore arar, sonuclar 5 satirlik listede cikar.
// Zemin siyah, alfa 0.89 (pencereli/penceresiz kare farkindan olculdu).
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Drop Listesi")]
    public class OlymposDropListesi : MonoBehaviour
    {
        public const int Sutun = 5, Satir = 3, KutuSayisi = Sutun * Satir, SonucSatiri = 5;

        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.89f;
        public Button closeButton;

        [Header("Arama")]
        public Button monsterToggle;
        public Button itemToggle;
        public Image monsterCheck;
        public Image itemCheck;
        public InputField searchField;
        public Button[] resultButtons = new Button[SonucSatiri];
        public Text[] resultTexts = new Text[SonucSatiri];
        public Button resultPrev, resultNext;
        public Text resultPageText;

        [Header("Kutular")]
        public Button[] slotButtons = new Button[KutuSayisi];
        public Image[] slotIcons = new Image[KutuSayisi];
        public Image[] slotFrames = new Image[KutuSayisi];
        public Text[] slotLabels = new Text[KutuSayisi];
        public RectTransform[] slotLabelBgs = new RectTransform[KutuSayisi];
        public Button gridPrev, gridNext;
        public Text gridPageText;

        [Header("Ipucu")]
        public OlymposDropIpucu tooltip;

        [Header("Veri")]
        public OlymposCanavarDrop[] veritabani = new OlymposCanavarDrop[0];

        [Header("Oran renkleri (olculen: Middle beyaz, Low sari)")]
        public Color varsayilanOranRengi = Color.white;
        public string[] ozelOranlar = { "Low" };
        public Color[] ozelOranRenkleri = { new Color32(0xFA, 0xE8, 0x00, 0xFF) };

        [Header("Olaylar")]
        public UnityEvent onClosed = new UnityEvent();

        class Sonuc { public string metin; public OlymposCanavarDrop canavar; public OlymposDropGirdisi grup; }

        bool esyaKipi;
        readonly List<Sonuc> sonuclar = new List<Sonuc>();
        int sonucSayfa, kutuSayfa;
        OlymposDropGirdisi[] liste = new OlymposDropGirdisi[0];
        readonly Stack<OlymposDropGirdisi[]> gecmis = new Stack<OlymposDropGirdisi[]>();

        void Awake()
        {
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (monsterToggle != null) monsterToggle.onClick.AddListener(delegate { KipSec(false); });
            if (itemToggle != null) itemToggle.onClick.AddListener(delegate { KipSec(true); });
            if (searchField != null) searchField.onValueChanged.AddListener(Ara);
            if (resultPrev != null) resultPrev.onClick.AddListener(delegate { SonucSayfasi(-1); });
            if (resultNext != null) resultNext.onClick.AddListener(delegate { SonucSayfasi(+1); });
            if (gridPrev != null) gridPrev.onClick.AddListener(delegate { KutuSayfasi(-1); });
            if (gridNext != null) gridNext.onClick.AddListener(delegate { KutuSayfasi(+1); });
            for (int i = 0; i < SonucSatiri; i++)
            {
                int k = i;
                if (i < resultButtons.Length && resultButtons[i] != null) resultButtons[i].onClick.AddListener(delegate { SonucSec(k); });
            }
            for (int i = 0; i < KutuSayisi; i++)
            {
                int k = i;
                if (i < slotButtons.Length && slotButtons[i] != null) slotButtons[i].onClick.AddListener(delegate { KutuyaBas(k); });
            }
            ZeminiUygula();
            KipSec(false);
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        // ------------------------------------------------------------ acma / kapama
        /// <summary>"Show Drops": yaratigin drop listesini acar. Her acilista kok listeden baslar.</summary>
        public void Ac(string canavarAdi)
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (tooltip != null) tooltip.Kapat();
            if (searchField != null) searchField.text = "";
            KipSec(false);
            var c = CanavarBul(canavarAdi);
            gecmis.Clear();
            ListeGoster(c != null ? c.droplar : new OlymposDropGirdisi[0]);
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            if (tooltip != null) tooltip.Kapat();
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        OlymposCanavarDrop CanavarBul(string ad)
        {
            if (string.IsNullOrEmpty(ad)) return null;
            for (int i = 0; i < veritabani.Length; i++)
                if (veritabani[i] != null && string.Equals(veritabani[i].canavarAdi, ad, StringComparison.OrdinalIgnoreCase))
                    return veritabani[i];
            return null;
        }

        // ------------------------------------------------------------ kutular
        public void ListeGoster(OlymposDropGirdisi[] girdiler)
        {
            liste = girdiler ?? new OlymposDropGirdisi[0];
            kutuSayfa = 0;
            KutulariCiz();
        }

        int KutuSayfaSayisi { get { return Mathf.Max(1, (liste.Length + KutuSayisi - 1) / KutuSayisi); } }

        void KutuSayfasi(int yon)
        {
            int yeni = Mathf.Clamp(kutuSayfa + yon, 0, KutuSayfaSayisi - 1);
            if (yeni == kutuSayfa) return;
            kutuSayfa = yeni;
            if (tooltip != null) tooltip.Kapat();
            KutulariCiz();
        }

        Color OranRengi(string oran)
        {
            for (int i = 0; i < ozelOranlar.Length && i < ozelOranRenkleri.Length; i++)
                if (string.Equals(ozelOranlar[i], oran, StringComparison.OrdinalIgnoreCase)) return ozelOranRenkleri[i];
            return varsayilanOranRengi;
        }

        void KutulariCiz()
        {
            for (int i = 0; i < KutuSayisi; i++)
            {
                int g = kutuSayfa * KutuSayisi + i;
                var d = g < liste.Length ? liste[g] : null;
                bool dolu = d != null;
                if (i < slotIcons.Length && slotIcons[i] != null) { slotIcons[i].sprite = dolu ? d.ikon : null; slotIcons[i].enabled = dolu && d.ikon != null; }
                if (i < slotFrames.Length && slotFrames[i] != null) slotFrames[i].enabled = dolu;
                if (i < slotLabels.Length && slotLabels[i] != null)
                {
                    var t = slotLabels[i];
                    t.gameObject.SetActive(dolu);
                    if (dolu)
                    {
                        t.text = d.oran; t.color = OranRengi(d.oran);
                        // etiketin siyah zemini yazinin genisligine oturur (olculen: yazi + 5 px)
                        if (i < slotLabelBgs.Length && slotLabelBgs[i] != null)
                            slotLabelBgs[i].sizeDelta = new Vector2(t.preferredWidth + 5f, slotLabelBgs[i].sizeDelta.y);
                    }
                }
                if (i < slotLabelBgs.Length && slotLabelBgs[i] != null) slotLabelBgs[i].gameObject.SetActive(dolu);
                if (i < slotButtons.Length && slotButtons[i] != null) slotButtons[i].interactable = dolu;
            }
            if (gridPageText != null) gridPageText.text = (kutuSayfa + 1) + "/" + KutuSayfaSayisi;
        }

        void KutuyaBas(int i)
        {
            int g = kutuSayfa * KutuSayisi + i;
            if (g < 0 || g >= liste.Length || liste[g] == null) return;
            var d = liste[g];
            if (d.grup)
            {
                gecmis.Push(liste);
                if (tooltip != null) tooltip.Kapat();
                ListeGoster(d.grupIcerigi);
                return;
            }
            if (tooltip == null) return;
            // Ipucu kutunun sag ustune acilir, ekrana sigacak sekilde kaydirilir.
            // (Videodaki konum kurali tek orneklerden tam cozulemedi: yaklasik.)
            var kutu = (RectTransform)slotButtons[i].transform;
            var ust = tooltip.transform.parent as RectTransform;
            Vector3 dunya = kutu.TransformPoint(new Vector3(kutu.rect.xMax, kutu.rect.yMax, 0f));
            Vector3 yerel = ust != null ? ust.InverseTransformPoint(dunya) : dunya;
            float x = ust != null ? yerel.x - ust.rect.xMin : yerel.x;
            float y = ust != null ? ust.rect.yMax - yerel.y : -yerel.y;
            tooltip.Goster(d, new Vector2(x + 8f, y - 300f));
        }

        /// <summary>Grup icindeyken bir ust listeye doner. (Oyunda geri dugmesi yok; pencere yeniden acilinca koke doner.)</summary>
        public void Geri()
        {
            if (gecmis.Count == 0) return;
            if (tooltip != null) tooltip.Kapat();
            ListeGoster(gecmis.Pop());
        }

        // ------------------------------------------------------------ arama
        void KipSec(bool esya)
        {
            esyaKipi = esya;
            if (monsterCheck != null) monsterCheck.enabled = !esya;
            if (itemCheck != null) itemCheck.enabled = esya;
            Ara(searchField != null ? searchField.text : "");
        }

        // Arama sonuclari videoda gorunmuyor (liste hep bos, "0/0"); buradaki davranis varsayimdir:
        // Monster kipi -> adi eslesen yaratiklar; Item Name kipi -> adi eslesen esyalar ("Esya (Yaratik)").
        void Ara(string sorgu)
        {
            sonuclar.Clear();
            sonucSayfa = 0;
            string q = sorgu != null ? sorgu.Trim() : "";
            if (q.Length > 0)
            {
                for (int i = 0; i < veritabani.Length; i++)
                {
                    var c = veritabani[i];
                    if (c == null) continue;
                    if (!esyaKipi)
                    {
                        if (Icerir(c.canavarAdi, q)) sonuclar.Add(new Sonuc { metin = c.canavarAdi, canavar = c });
                    }
                    else EsyaAra(c, c.droplar, null, q);
                }
            }
            SonuclariCiz();
        }

        void EsyaAra(OlymposCanavarDrop c, OlymposDropGirdisi[] girdiler, OlymposDropGirdisi grup, string q)
        {
            if (girdiler == null) return;
            for (int i = 0; i < girdiler.Length; i++)
            {
                var d = girdiler[i];
                if (d == null) continue;
                if (d.grup) { EsyaAra(c, d.grupIcerigi, d, q); continue; }
                if (Icerir(d.ad, q)) sonuclar.Add(new Sonuc { metin = d.ad + " (" + c.canavarAdi + ")", canavar = c, grup = grup });
            }
        }

        static bool Icerir(string metin, string q)
        {
            return !string.IsNullOrEmpty(metin) && metin.IndexOf(q, StringComparison.OrdinalIgnoreCase) >= 0;
        }

        int SonucSayfaSayisi { get { return (sonuclar.Count + SonucSatiri - 1) / SonucSatiri; } }

        void SonucSayfasi(int yon)
        {
            int n = SonucSayfaSayisi;
            if (n == 0) return;
            sonucSayfa = Mathf.Clamp(sonucSayfa + yon, 0, n - 1);
            SonuclariCiz();
        }

        void SonuclariCiz()
        {
            for (int i = 0; i < SonucSatiri; i++)
            {
                int g = sonucSayfa * SonucSatiri + i;
                bool dolu = g < sonuclar.Count;
                if (i < resultTexts.Length && resultTexts[i] != null) resultTexts[i].text = dolu ? sonuclar[g].metin : "";
                if (i < resultButtons.Length && resultButtons[i] != null) resultButtons[i].interactable = dolu;
            }
            int n = SonucSayfaSayisi;
            if (resultPageText != null) resultPageText.text = (n == 0 ? 0 : sonucSayfa + 1) + "/" + n;   // bosken "0/0"
        }

        void SonucSec(int i)
        {
            int g = sonucSayfa * SonucSatiri + i;
            if (g < 0 || g >= sonuclar.Count) return;
            var s = sonuclar[g];
            gecmis.Clear();
            if (tooltip != null) tooltip.Kapat();
            if (s.grup != null) { gecmis.Push(s.canavar.droplar); ListeGoster(s.grup.grupIcerigi); }
            else ListeGoster(s.canavar.droplar);
        }
    }
}
