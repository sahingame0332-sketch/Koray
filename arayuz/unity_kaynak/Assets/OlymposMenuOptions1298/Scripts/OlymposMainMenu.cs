// OLYMPOS-KO · 1298 Ana menü paneli
// Çerçeve ve sekiz düğme orijinal ekran görüntüsünden birebir alınmıştır; düğmeler
// görselin üzerindeki görünmez tıklama alanlarıdır.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposMenuOgesi
    {
        PowerUpStore = 0, OpenMerchant = 1, SlaveMerchant = 2, SeekingParty = 3,
        Options = 4, Forum = 5, Discord = 6, Instagram = 7
    }

    [DisallowMultipleComponent]
    public class OlymposMainMenu : MonoBehaviour
    {
        public const int OgeSayisi = 8;

        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("1 = tamamen siyah, 0 = tamamen saydam. Varsayılan 0.92: orijinalden ölçüldü " +
                 "(geçirgenlik t≈0.08). Ayrıntı: arayuz/04-saydamlik.md")]
        public float backgroundAlpha = 0.92f;

        [Header("Düğmeler (yukarıdan aşağı)")]
        public Button[] buttons = new Button[OgeSayisi];
        public Button closeButton;

        [Header("Davranış")]
        [Tooltip("X'e basılınca panel gizlensin mi?")]
        public bool closeHidesWindow = true;

        [Serializable] public class MenuEvent : UnityEvent<OlymposMenuOgesi> { }
        public MenuEvent onMenuSelected = new MenuEvent();
        public UnityEvent onClose = new UnityEvent();

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background == null) return;
            background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            for (int i = 0; i < OgeSayisi; i++)
            {
                var oge = (OlymposMenuOgesi)i;
                if (buttons != null && i < buttons.Length && buttons[i] != null)
                    buttons[i].onClick.AddListener(() => onMenuSelected.Invoke(oge));
            }
            if (closeButton != null)
                closeButton.onClick.AddListener(() =>
                {
                    onClose.Invoke();
                    if (closeHidesWindow) gameObject.SetActive(false);
                });
        }

        public void SetInteractable(OlymposMenuOgesi oge, bool value)
        {
            int i = (int)oge;
            if (buttons != null && i < buttons.Length && buttons[i] != null)
                buttons[i].interactable = value;
        }
    }
}
