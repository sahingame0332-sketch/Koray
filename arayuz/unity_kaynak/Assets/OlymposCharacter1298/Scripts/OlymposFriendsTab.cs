// OLYMPOS-KO · 1298 Character penceresi · FRIENDS sekmesi
// Görsel orijinal ekran görüntüsünden birebir alınmıştır; satır zeminleri, düğmeler ve
// durum göstergeleri sprite'ın parçasıdır. İsimler ve sayfa numarası koddan yazılır.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    /// <summary>Bir arkadaşın çevrimiçi durumu. Renkler orijinal göstergelerden ölçüldü.</summary>
    public enum OlymposFriendDurum { Cevrimdisi = 0, Cevrimici = 1, Partide = 2 }

    [DisallowMultipleComponent]
    public class OlymposFriendsTab : MonoBehaviour
    {
        public const int SatirSayisi = 7;

        [Header("Satırlar")]
        public Button[] rowButtons = new Button[SatirSayisi];
        public Text[] rowNames = new Text[SatirSayisi];

        [Header("Sayfa")]
        public Button prevPageButton;
        public Button nextPageButton;
        public Text pageText;

        [Header("Düğmeler")]
        public Button registerButton;
        public Button deleteButton;
        public Button privateButton;
        public Button partyButton;
        public Button refreshButton;

        [Serializable] public class SatirEvent : UnityEvent<int> { }
        /// <summary>Bir arkadaş satırına basıldı (0..6).</summary>
        public SatirEvent onRowSelected = new SatirEvent();
        public UnityEvent onPrevPage = new UnityEvent();
        public UnityEvent onNextPage = new UnityEvent();

        // Orijinal göstergelerden ölçülen renkler
        static readonly Color Yesil   = new Color32(0x2E, 0xE6, 0x2E, 0xFF);  // Online
        static readonly Color Turuncu = new Color32(0xF2, 0x8C, 0x1E, 0xFF);  // In Party
        static readonly Color Kirmizi = new Color32(0xF0, 0x1E, 0x1E, 0xFF);  // Not Connected

        int secili = -1;
        /// <summary>Seçili satır; hiçbiri seçili değilse -1.</summary>
        public int SeciliSatir { get { return secili; } }

        void Awake()
        {
            for (int i = 0; i < SatirSayisi; i++)
            {
                int k = i;
                if (rowButtons != null && i < rowButtons.Length && rowButtons[i] != null)
                    rowButtons[i].onClick.AddListener(() => { secili = k; onRowSelected.Invoke(k); });
            }
            if (prevPageButton != null) prevPageButton.onClick.AddListener(() => onPrevPage.Invoke());
            if (nextPageButton != null) nextPageButton.onClick.AddListener(() => onNextPage.Invoke());
        }

        /// <summary>Bir satırı doldurur. Ad boş verilirse satır boşaltılır.</summary>
        public void SetFriend(int satir, string ad, OlymposFriendDurum durum)
        {
            if (satir < 0 || satir >= SatirSayisi) return;
            if (rowNames == null || satir >= rowNames.Length || rowNames[satir] == null) return;
            var t = rowNames[satir];
            t.text = ad ?? "";
            t.color = durum == OlymposFriendDurum.Cevrimici ? Yesil
                    : durum == OlymposFriendDurum.Partide   ? Turuncu
                    : Kirmizi;
        }

        /// <summary>Tüm satırları temizler.</summary>
        public void Clear()
        {
            for (int i = 0; i < SatirSayisi; i++) SetFriend(i, "", OlymposFriendDurum.Cevrimdisi);
            secili = -1;
        }

        public void SetPage(int sayfa)
        {
            if (pageText != null) pageText.text = sayfa.ToString();
        }
    }
}
