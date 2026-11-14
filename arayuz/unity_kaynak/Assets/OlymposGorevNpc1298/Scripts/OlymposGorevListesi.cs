// OLYMPOS-KO · 1298 QuestList penceresi — 642 x 470 sprite, siyah zemin 566 x 441, alfa 0.91 (olculdu).
// NPC portresi (dairesel), "Test NPC Description." (Liberation Sans Bold 16 #DD9344, yari saydam gri kutu ustunde),
// gorev satirlari (beyaz cerceveli dugme 468 x 82; yazi Liberation Sans Bold 22 #F6E1E1 ortali). Satira dokununca detay acilir.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposGorevOlayi : UnityEvent<OlymposGorev> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Gorev/QuestList")]
    public class OlymposGorevListesi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.91f;

        [Header("Parcalar")]
        public Image portre;
        public Text aciklamaText;
        public Button kapatButton;
        [Tooltip("Ilk gorev satiri (sablon). Digerleri bunun kopyasi olarak satirAdimi kadar asagiya dizilir.")]
        public Button satirSablonu;
        public float satirAdimi = 92f;
        public OlymposGorevDetayi detay;

        [Header("Veri")]
        public string npcAciklamasi = "Test NPC Description.";
        public List<OlymposGorev> gorevler = new List<OlymposGorev>();

        public OlymposGorevOlayi onGorevSecildi = new OlymposGorevOlayi();
        public UnityEvent onKapandi = new UnityEvent();

        readonly List<Button> satirlar = new List<Button>();

        void Awake()
        {
            if (kapatButton != null) kapatButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        /// <summary>NPC'ye "Open" ile girildiginde cagrilir.</summary>
        public void Ac(Sprite npcPortresi, string aciklama, List<OlymposGorev> liste)
        {
            if (npcPortresi != null && portre != null) portre.sprite = npcPortresi;
            if (aciklama != null) npcAciklamasi = aciklama;
            if (liste != null) gorevler = liste;
            gameObject.SetActive(true); transform.SetAsLastSibling();
            Yenile();
        }

        public void Kapat() { gameObject.SetActive(false); onKapandi.Invoke(); }

        public void Yenile()
        {
            if (aciklamaText != null) aciklamaText.text = npcAciklamasi;
            if (satirSablonu == null) return;
            for (int i = 1; i < satirlar.Count; i++) if (satirlar[i] != null) Destroy(satirlar[i].gameObject);
            satirlar.Clear(); satirlar.Add(satirSablonu);
            for (int i = 0; i < gorevler.Count; i++)
            {
                Button b = i == 0 ? satirSablonu : Instantiate(satirSablonu, satirSablonu.transform.parent);
                if (i > 0) { satirlar.Add(b); var rt = (RectTransform)b.transform; rt.anchoredPosition = ((RectTransform)satirSablonu.transform).anchoredPosition + new Vector2(0f, -satirAdimi * i); }
                var t = b.GetComponentInChildren<Text>(); if (t != null) t.text = gorevler[i].ad;
                var g = gorevler[i];
                b.onClick.RemoveAllListeners(); b.onClick.AddListener(() => Sec(g));
            }
            satirSablonu.gameObject.SetActive(gorevler.Count > 0);
        }

        void Sec(OlymposGorev g)
        {
            onGorevSecildi.Invoke(g);
            if (detay != null) { detay.Ac(g, portre != null ? portre.sprite : null); }
        }
    }
}
