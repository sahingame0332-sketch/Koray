// OLYMPOS-KO · 1298 stat butonları penceresi (STR / HP / DEX / INT / MP)
// Çerçeve ve butonlar orijinal görselden birebir alınmıştır.
// İç zemin: yarı saydam siyah, oyun dünyası arkadan hafifçe görünür.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposStat { STR = 0, HP = 1, DEX = 2, INT = 3, MP = 4 }

    [DisallowMultipleComponent]
    public class OlymposStatButtonsWindow : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("1 = tamamen siyah, 0 = tamamen saydam. Varsayılan 0.92: orijinal ekran görüntüsünden ölçüldü " +
                 "(geçirgenlik t≈0.078). Ayrıntı: arayuz/04-saydamlik.md")]
        public float backgroundAlpha = 0.92f;

        [Header("Butonlar (yukarıdan aşağı)")]
        public Button strButton;
        public Button hpButton;
        public Button dexButton;
        public Button intButton;
        public Button mpButton;

        [Serializable] public class StatEvent : UnityEvent<OlymposStat> { }
        /// <summary>Bir stat butonuna (+) basıldığında tetiklenir.</summary>
        public StatEvent onStatPlus = new StatEvent();

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background == null) return;
            background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            Hook(strButton, OlymposStat.STR);
            Hook(hpButton, OlymposStat.HP);
            Hook(dexButton, OlymposStat.DEX);
            Hook(intButton, OlymposStat.INT);
            Hook(mpButton, OlymposStat.MP);
        }

        void Hook(Button b, OlymposStat s)
        {
            if (b != null) b.onClick.AddListener(() => onStatPlus.Invoke(s));
        }

        /// <summary>Stat puanı kalmadığında butonları kilitlemek için.</summary>
        public void SetInteractable(bool value)
        {
            foreach (var b in new[] { strButton, hpButton, dexButton, intButton, mpButton })
                if (b != null) b.interactable = value;
        }
    }
}
