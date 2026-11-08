// OLYMPOS-KO · 1298 NPC etkileşim düğmesi ("Open")
// Oyuncu bir NPC'ye bastığında karakterin üstünde beliren düğme.
// Görsel orijinal ekran görüntülerinden birebir alındı: 281 x 84, yazı silinip
// Text bileşenine çevrildi (farklı NPC'lerde başka bir fiil gerekirse değişebilsin).
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposNpcOpenButton : MonoBehaviour
    {
        [Header("Parçalar")]
        public Button button;
        public Text label;

        [Header("İçerik")]
        [Tooltip("Düğme yazısı. Orijinalinde \"Open\".")]
        public string text = "Open";
        [Tooltip("Üstünde durduğu NPC'nin adı; yalnızca olayda geri verilir.")]
        public string npcName = "";

        [Serializable] public class AcEvent : UnityEvent<string> { }
        /// <summary>Düğmeye basıldı; parametre npcName.</summary>
        public AcEvent onOpen = new AcEvent();

        [Header("Davranış")]
        [Tooltip("Basınca düğme gizlensin mi? (oyunda dükkân açılınca kayboluyor)")]
        public bool hideOnClick = true;

        void OnValidate() { Uygula(); }

        void Awake()
        {
            Uygula();
            if (button != null)
                button.onClick.AddListener(() =>
                {
                    onOpen.Invoke(npcName);
                    if (hideOnClick) gameObject.SetActive(false);
                });
        }

        void Uygula()
        {
            if (label != null && !string.IsNullOrEmpty(text)) label.text = text;
        }

        /// <summary>Düğmeyi bir NPC için gösterir.</summary>
        public void Show(string npc, string yazi = "Open")
        {
            npcName = npc; text = yazi;
            Uygula();
            gameObject.SetActive(true);
        }

        public void Hide() { gameObject.SetActive(false); }
    }
}
