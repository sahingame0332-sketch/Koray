// OLYMPOS-KO · 1298 Character penceresi · CLAN sekmesi
// Tablo çerçevesi, başlık satırı ve düğmeler orijinal görselden; üye satırları,
// klan adı, derece ve sayaçlar koddan doldurulur.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable]
    public struct OlymposClanUye
    {
        public string role;
        public string name;
        public int level;
        public string job;
    }

    [DisallowMultipleComponent]
    public class OlymposClanTab : MonoBehaviour
    {
        public const int SatirSayisi = 12;

        [Header("Klan kimliği")]
        public Image flagImage;
        public Text clanNameText;
        public Text gradeText;
        public Button upgradeButton;

        [Header("Üye tablosu")]
        public Text[] roleTexts  = new Text[SatirSayisi];
        public Text[] nameTexts  = new Text[SatirSayisi];
        public Text[] levelTexts = new Text[SatirSayisi];
        public Text[] jobTexts   = new Text[SatirSayisi];
        public Button[] rowButtons = new Button[SatirSayisi];

        [Header("Sayfa ve sayaçlar")]
        public Button prevPageButton;
        public Button nextPageButton;
        public Text pageText;
        public Text onlineCountText;
        public Text memberCountText;

        [Header("Düğmeler")]
        public Button donatedListButton;
        public Button refreshButton;
        public Button joinClanButton;
        public Button joinPartyButton;
        public Button appointButton;
        public Button leaveButton;
        public Button privateButton;

        [Serializable] public class SatirEvent : UnityEvent<int> { }
        public SatirEvent onRowSelected = new SatirEvent();
        public UnityEvent onPrevPage = new UnityEvent();
        public UnityEvent onNextPage = new UnityEvent();

        // Orijinalden ölçülen üye satırı yeşili
        static readonly Color UyeYesil = new Color32(0x3C, 0xE6, 0x3C, 0xFF);

        void Awake()
        {
            for (int i = 0; i < SatirSayisi; i++)
            {
                int k = i;
                if (rowButtons != null && i < rowButtons.Length && rowButtons[i] != null)
                    rowButtons[i].onClick.AddListener(() => onRowSelected.Invoke(k));
            }
            if (prevPageButton != null) prevPageButton.onClick.AddListener(() => onPrevPage.Invoke());
            if (nextPageButton != null) nextPageButton.onClick.AddListener(() => onNextPage.Invoke());
        }

        public void SetClan(string ad, string derece, Sprite bayrak)
        {
            if (clanNameText != null && ad != null) clanNameText.text = ad;
            if (gradeText != null && derece != null) gradeText.text = "Grade: " + derece;
            if (flagImage != null && bayrak != null) flagImage.sprite = bayrak;
        }

        public void SetCounts(int cevrimici, int uye, int kapasite)
        {
            if (onlineCountText != null) onlineCountText.text = cevrimici.ToString();
            if (memberCountText != null) memberCountText.text = uye + "/" + kapasite;
        }

        public void SetPage(int sayfa)
        {
            if (pageText != null) pageText.text = sayfa.ToString();
        }

        /// <summary>Tek bir satırı doldurur.</summary>
        public void SetMember(int satir, OlymposClanUye uye)
        {
            if (satir < 0 || satir >= SatirSayisi) return;
            Yaz(roleTexts,  satir, uye.role);
            Yaz(nameTexts,  satir, uye.name);
            Yaz(levelTexts, satir, uye.level > 0 ? uye.level.ToString() : "");
            Yaz(jobTexts,   satir, uye.job);
        }

        /// <summary>Listeyi baştan doldurur; eksik satırlar boşaltılır.</summary>
        public void SetMembers(OlymposClanUye[] uyeler)
        {
            for (int i = 0; i < SatirSayisi; i++)
            {
                if (uyeler != null && i < uyeler.Length) SetMember(i, uyeler[i]);
                else SetMember(i, new OlymposClanUye());
            }
        }

        static void Yaz(Text[] dizi, int i, string v)
        {
            if (dizi == null || i >= dizi.Length || dizi[i] == null) return;
            dizi[i].text = v ?? "";
            dizi[i].color = UyeYesil;
        }
    }
}
