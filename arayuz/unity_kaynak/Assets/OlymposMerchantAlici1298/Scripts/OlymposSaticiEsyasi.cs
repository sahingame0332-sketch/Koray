// OLYMPOS-KO · 1298 Merchant — alici gorunumu · veri tipleri (TEK BASINA paket)
// Olculer: depoda arayuz/09-merchant.md ("Alici gorunumu" eki)
using System;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    /// <summary>Tezgahta ya da alicinin envanterinde duran bir esya.</summary>
    [Serializable]
    public class OlymposSaticiEsyasi
    {
        public string ad;
        public Sprite ikon;
        [Tooltip("Yigin adedi. 2 ve uzeri yuvanin sag altinda yazar.")]
        public int adet = 1;
        [Tooltip("Yukseltme seviyesi. 0'dan buyukse yuvanin sag ustunde mor \"+N\" yazar.")]
        public int yukseltme;
        [Tooltip("Yuva mor cerceveyle cizilir. Ekran goruntulerinde +1 silahlarda mor, baska bir +5 yayda gumus: kural bilinmiyor, esya basina secilir.")]
        public bool morCerceve;
        [Tooltip("Tezgahtaki fiyat (tek esya).")]
        public long fiyat;

        public bool Bos { get { return ikon == null && string.IsNullOrEmpty(ad); } }
    }

    [Serializable] public class OlymposSaticiSiraOlayi : UnityEvent<int> { }
    [Serializable] public class OlymposSaticiAdOlayi : UnityEvent<string> { }
}
