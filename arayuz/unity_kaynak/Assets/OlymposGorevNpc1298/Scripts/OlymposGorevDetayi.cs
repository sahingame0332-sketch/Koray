// OLYMPOS-KO · 1298 gorev detayi ("Starter Weapon&Armor") — 596 x 840 sprite, siyah zemin 559 x 811, alfa 0.93 (olculdu).
// Baslik Liberation Sans Bold 19 #EEDADA; aciklama Bold 16 #E09869; Objectives satiri (ikon 46 + "25" Bold 18 + iki satir Bold 16);
// Rewards: 2 sutun x 4 satir hucre 228 x 74 (adim 229 / 76), ikon 47 x 45, ad Bold 16 #E9D6D6.
// Dugmeler: Accepted (Bold 21) -> kabul, Close -> kapat. Kabul edilmis gorevde Accepted pasif.
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Gorev/Gorev Detayi")]
    public class OlymposGorevDetayi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;

        [Header("Parcalar")]
        public Image portre;
        public Text baslikText;
        public Text aciklamaText;
        public Image hedefIkon;
        public Text hedefSayi;
        public Text hedefBaslik;
        public Text hedefAciklama;
        public GameObject[] odulHucreleri = new GameObject[8];
        public Image[] odulIkonlari = new Image[8];
        public Text[] odulAdlari = new Text[8];
        public Button kabulButton;
        public Text kabulText;
        public Button kapatButton;
        public Button kapatXButton;

        [Header("Veri")]
        public OlymposGorev gorev = new OlymposGorev();

        public OlymposGorevOlayi onKabul = new OlymposGorevOlayi();
        public UnityEvent onKapandi = new UnityEvent();

        void Awake()
        {
            if (kabulButton != null) kabulButton.onClick.AddListener(Kabul);
            if (kapatButton != null) kapatButton.onClick.AddListener(Kapat);
            if (kapatXButton != null) kapatXButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public void Ac(OlymposGorev g, Sprite npcPortresi)
        {
            if (g != null) gorev = g;
            if (npcPortresi != null && portre != null) portre.sprite = npcPortresi;
            gameObject.SetActive(true); transform.SetAsLastSibling();
            Yenile();
        }

        public void Kapat() { gameObject.SetActive(false); onKapandi.Invoke(); }

        public void Kabul()
        {
            if (gorev == null || gorev.kabulEdildi) return;
            gorev.kabulEdildi = true; Yenile();
            onKabul.Invoke(gorev);
        }

        public void Yenile()
        {
            if (gorev == null) return;
            if (baslikText != null) baslikText.text = gorev.ad;
            if (aciklamaText != null) aciklamaText.text = gorev.aciklama;
            var h = gorev.hedefler.Count > 0 ? gorev.hedefler[0] : null;
            if (hedefIkon != null) { hedefIkon.sprite = h != null ? h.ikon : null; hedefIkon.enabled = h != null && h.ikon != null; }
            if (hedefSayi != null) hedefSayi.text = h != null && h.sayi > 0 ? h.sayi.ToString() : "";
            if (hedefBaslik != null) hedefBaslik.text = h != null ? h.baslik : "";
            if (hedefAciklama != null) hedefAciklama.text = h != null ? h.aciklama : "";
            for (int i = 0; i < odulHucreleri.Length; i++)
            {
                bool var_ = i < gorev.oduller.Count;
                if (odulHucreleri[i] != null) odulHucreleri[i].SetActive(var_);
                if (!var_) continue;
                if (odulIkonlari[i] != null) { odulIkonlari[i].sprite = gorev.oduller[i].ikon; odulIkonlari[i].enabled = gorev.oduller[i].ikon != null; }
                if (odulAdlari[i] != null) odulAdlari[i].text = gorev.oduller[i].ad;
            }
            if (kabulButton != null) kabulButton.interactable = !gorev.kabulEdildi;
            if (kabulText != null) kabulText.color = gorev.kabulEdildi ? new Color(0.55f, 0.5f, 0.5f) : new Color(0.94f, 0.867f, 0.871f);
        }
    }
}
