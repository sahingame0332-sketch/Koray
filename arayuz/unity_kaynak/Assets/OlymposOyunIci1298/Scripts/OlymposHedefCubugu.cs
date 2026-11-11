// OLYMPOS-KO · 1298 hedef cubugu: secili yaratigin adi, seviyesi, can cubugu,
// altinda "Show Drops" dugmesi ve saldiri dugmelerinin yanindaki hedef iptal (X) dugmesi.
// Hedef yokken hicbiri gorunmez.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposHedefOlayi : UnityEvent<string> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Hedef Cubugu")]
    public class OlymposHedefCubugu : MonoBehaviour
    {
        [Header("Cubuk")]
        public GameObject cubukKoku;
        public Text adText;
        public Text seviyeText;
        [Tooltip("Can dolgusu (Image.Type = Filled, yatay, soldan).")]
        public Image canDolgu;
        public Button showDropsButton;

        [Header("Hedef iptal (X)")]
        public Button iptalButton;

        [Header("Olaylar")]
        public OlymposHedefOlayi onShowDrops = new OlymposHedefOlayi();
        [Tooltip("X'e basilip hedef birakildiginda (birakilan hedefin adi).")]
        public OlymposHedefOlayi onHedefBirakildi = new OlymposHedefOlayi();

        public string HedefAdi { get; private set; }
        public bool HedefVar { get { return !string.IsNullOrEmpty(HedefAdi); } }

        void Awake()
        {
            if (showDropsButton != null) showDropsButton.onClick.AddListener(delegate { if (HedefVar) onShowDrops.Invoke(HedefAdi); });
            if (iptalButton != null) iptalButton.onClick.AddListener(HedefiBirak);
            Gorunurluk();
        }

        /// <summary>Yaratik secildiginde cagrilir. canOrani 0..1.</summary>
        public void HedefSec(string ad, int seviye, float canOrani)
        {
            HedefAdi = ad;
            if (adText != null) adText.text = ad;
            if (seviyeText != null) seviyeText.text = "Lv." + seviye;
            CanGuncelle(canOrani);
            Gorunurluk();
        }

        public void CanGuncelle(float oran)
        {
            if (canDolgu != null) canDolgu.fillAmount = Mathf.Clamp01(oran);
        }

        /// <summary>X dugmesi: secimi kaldirir.</summary>
        public void HedefiBirak()
        {
            if (!HedefVar) return;
            string eski = HedefAdi;
            HedefAdi = null;
            Gorunurluk();
            onHedefBirakildi.Invoke(eski);
        }

        void Gorunurluk()
        {
            bool v = HedefVar;
            if (cubukKoku != null) cubukKoku.SetActive(v);
            if (iptalButton != null) iptalButton.gameObject.SetActive(v);
        }
    }
}
