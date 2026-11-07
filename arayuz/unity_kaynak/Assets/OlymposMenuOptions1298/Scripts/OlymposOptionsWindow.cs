// OLYMPOS-KO · 1298 OPTIONS penceresi
// Sol menüde 11 sayfa; her düğmenin normal ve seçili görseli orijinalden alınmıştır.
// Sayfa içerikleri de orijinal görsellerdir; ilgili sayfanın Image'ı etkinleştirilir.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposOptionSayfa
    {
        Looting = 0, Cospre = 1, VFX = 2, GameOption1 = 3, GameOption2 = 4,
        GameOption3 = 5, BlockOptions = 6, BattleOptions = 7, PMBlock = 8,
        HideOption = 9, SoundOption = 10
    }

    [DisallowMultipleComponent]
    public class OlymposOptionsWindow : MonoBehaviour
    {
        public const int SayfaSayisi = 11;

        [Header("Zemin")]
        [Tooltip("Pencerenin dış alanının siyah zemini. İçerik panelinin kendi opak zemini vardır.")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("1 = tamamen siyah, 0 = tamamen saydam. Varsayılan 0.95: orijinalden ölçüldü " +
                 "(geçirgenlik t≈0.045). Ayrıntı: arayuz/04-saydamlik.md")]
        public float backgroundAlpha = 0.95f;

        [Header("Sol menü")]
        public Button[] menuButtons   = new Button[SayfaSayisi];
        public Image[]  menuImages    = new Image[SayfaSayisi];
        public Sprite[] menuNormal    = new Sprite[SayfaSayisi];
        public Sprite[] menuSelected  = new Sprite[SayfaSayisi];

        [Header("İçerik sayfaları")]
        public GameObject[] pages = new GameObject[SayfaSayisi];

        [Header("Düğmeler")]
        public Button closeButton;
        public Button resetButton;

        [Header("Davranış")]
        public bool closeHidesWindow = true;
        [Tooltip("Açılışta gösterilecek sayfa.")]
        public OlymposOptionSayfa startPage = OlymposOptionSayfa.Looting;

        [Serializable] public class SayfaEvent : UnityEvent<OlymposOptionSayfa> { }
        public SayfaEvent onPageChanged = new SayfaEvent();
        public UnityEvent onReset = new UnityEvent();
        public UnityEvent onClose = new UnityEvent();

        OlymposOptionSayfa aktif;
        public OlymposOptionSayfa AktifSayfa { get { return aktif; } }

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background == null) return;
            background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            for (int i = 0; i < SayfaSayisi; i++)
            {
                var s = (OlymposOptionSayfa)i;
                if (menuButtons != null && i < menuButtons.Length && menuButtons[i] != null)
                    menuButtons[i].onClick.AddListener(() => ShowPage(s));
            }
            if (closeButton != null)
                closeButton.onClick.AddListener(() =>
                {
                    onClose.Invoke();
                    if (closeHidesWindow) gameObject.SetActive(false);
                });
            if (resetButton != null) resetButton.onClick.AddListener(() => onReset.Invoke());
            ShowPage(startPage, false);
        }

        public void ShowPage(OlymposOptionSayfa sayfa) { ShowPage(sayfa, true); }

        public void ShowPage(OlymposOptionSayfa sayfa, bool olayGonder)
        {
            int sec = (int)sayfa;
            if (sec < 0 || sec >= SayfaSayisi) return;
            aktif = sayfa;
            for (int i = 0; i < SayfaSayisi; i++)
            {
                if (pages != null && i < pages.Length && pages[i] != null)
                    pages[i].SetActive(i == sec);
                if (menuImages != null && i < menuImages.Length && menuImages[i] != null)
                {
                    var spr = (i == sec)
                        ? (menuSelected != null && i < menuSelected.Length ? menuSelected[i] : null)
                        : (menuNormal   != null && i < menuNormal.Length   ? menuNormal[i]   : null);
                    if (spr != null) menuImages[i].sprite = spr;
                }
            }
            if (olayGonder) onPageChanged.Invoke(sayfa);
        }
    }
}
