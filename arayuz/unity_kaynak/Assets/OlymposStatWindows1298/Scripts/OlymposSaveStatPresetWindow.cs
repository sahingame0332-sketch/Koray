// OLYMPOS-KO · 1298 "SAVE STAT PRESET" penceresi
// Görsel, orijinal ekran görüntüsünden birebir alınmıştır (mat zemin).
// Save / Activate / Kapat butonları görselin üzerindeki görünmez tıklama alanlarıdır.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposSaveStatPresetWindow : MonoBehaviour
    {
        public const int SlotCount = 4;

        [Header("Butonlar")]
        public Button closeButton;
        public Button[] saveButtons = new Button[SlotCount];
        public Button[] activateButtons = new Button[SlotCount];

        [Header("Slot durum yazısı")]
        [Tooltip("Görseldeki '- Empty -' yazısını örten siyah kutular.")]
        public Image[] emptyCovers = new Image[SlotCount];
        [Tooltip("Slot doluyken '- Empty -' yerine yazılacak metinler.")]
        public Text[] statusTexts = new Text[SlotCount];

        [Header("Davranış")]
        [Tooltip("X'e basılınca pencere kapansın mı?")]
        public bool closeHidesWindow = true;

        [Serializable] public class SlotEvent : UnityEvent<int> { }
        /// <summary>Slot indeksi: 0..3 (görselde 1..4)</summary>
        public SlotEvent onSave = new SlotEvent();
        public SlotEvent onActivate = new SlotEvent();
        public UnityEvent onClose = new UnityEvent();

        void Awake()
        {
            for (int i = 0; i < SlotCount; i++)
            {
                int slot = i;
                if (saveButtons != null && i < saveButtons.Length && saveButtons[i] != null)
                    saveButtons[i].onClick.AddListener(() => onSave.Invoke(slot));
                if (activateButtons != null && i < activateButtons.Length && activateButtons[i] != null)
                    activateButtons[i].onClick.AddListener(() => onActivate.Invoke(slot));
            }
            if (closeButton != null)
                closeButton.onClick.AddListener(() =>
                {
                    onClose.Invoke();
                    if (closeHidesWindow) gameObject.SetActive(false);
                });
        }

        /// <summary>
        /// Slotun durum satırını değiştirir. null veya boş verilirse görseldeki
        /// orijinal "- Empty -" yazısı görünür. Örn: SetSlotStatus(0, "STR 50 · DEX 70 · INT 112")
        /// </summary>
        public void SetSlotStatus(int slot, string text)
        {
            if (slot < 0 || slot >= SlotCount) return;
            bool custom = !string.IsNullOrEmpty(text);
            if (emptyCovers != null && slot < emptyCovers.Length && emptyCovers[slot] != null)
                emptyCovers[slot].gameObject.SetActive(custom);
            if (statusTexts != null && slot < statusTexts.Length && statusTexts[slot] != null)
            {
                statusTexts[slot].gameObject.SetActive(custom);
                if (custom) statusTexts[slot].text = text;
            }
        }
    }
}
