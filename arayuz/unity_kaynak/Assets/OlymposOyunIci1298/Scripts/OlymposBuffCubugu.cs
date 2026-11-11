// OLYMPOS-KO · 1298 etki (buff) cubugu + Remove / Close menusu
// Ikon 64 x 64, adim 66, saga yasli; yeni etki saga eklenir (basilma sirasi soldan saga).
// Ikona dokununca altinda menu acilir: Remove etkiyi siler, Close menuyu kapatir.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposBuffOlayi : UnityEvent<string> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Buff Cubugu")]
    public class OlymposBuffCubugu : MonoBehaviour
    {
        [Serializable]
        public class Hucre
        {
            public GameObject kok;
            public Image ikon;
            public Text sure;
            public Button dugme;
        }

        class Etki { public string id; public Sprite ikon; public float kalan; }

        [Header("Hucreler (kurucu doldurur)")]
        public Hucre[] hucreler = new Hucre[0];
        [Tooltip("Ikon genisligi + bosluk. Olculen: 66")]
        public float adim = 66f;

        [Header("Menu")]
        public RectTransform menu;
        public Button removeButton;
        public Button menuCloseButton;
        [Tooltip("Menunun, secilen ikonun sol kenarina gore x kaymasi. Olculen: -65 (menu ikonun altinda ortali)")]
        public float menuKaymasi = -65f;

        [Header("Olaylar")]
        [Tooltip("Remove ile silindiginde (etki kimligi).")]
        public OlymposBuffOlayi onRemoved = new OlymposBuffOlayi();
        [Tooltip("Suresi dolup kendiliginden bittiginde.")]
        public OlymposBuffOlayi onExpired = new OlymposBuffOlayi();

        readonly List<Etki> etkiler = new List<Etki>();
        int secili = -1;

        void Awake()
        {
            for (int i = 0; i < hucreler.Length; i++)
            {
                int k = i;
                if (hucreler[i] != null && hucreler[i].dugme != null)
                    hucreler[i].dugme.onClick.AddListener(delegate { MenuAc(k); });
            }
            if (removeButton != null) removeButton.onClick.AddListener(SeciliyiSil);
            if (menuCloseButton != null) menuCloseButton.onClick.AddListener(MenuKapat);
            MenuKapat();
            Yenile();
        }

        void Update()
        {
            bool degisti = false;
            for (int i = etkiler.Count - 1; i >= 0; i--)
            {
                etkiler[i].kalan -= Time.deltaTime;
                if (etkiler[i].kalan <= 0f)
                {
                    string id = etkiler[i].id;
                    etkiler.RemoveAt(i);
                    degisti = true;
                    onExpired.Invoke(id);
                }
            }
            if (degisti) { MenuKapat(); Yenile(); }
            else SureleriYaz();
        }

        public int Adet { get { return etkiler.Count; } }

        public bool Var(string id)
        {
            for (int i = 0; i < etkiler.Count; i++) if (etkiler[i].id == id) return true;
            return false;
        }

        /// <summary>Etki ekler. Ayni kimlik zaten varsa suresi yenilenir, yeri degismez.</summary>
        public void Ekle(string id, Sprite ikon, float saniye)
        {
            for (int i = 0; i < etkiler.Count; i++)
                if (etkiler[i].id == id) { etkiler[i].kalan = saniye; etkiler[i].ikon = ikon; Yenile(); return; }
            if (etkiler.Count >= hucreler.Length) return;
            etkiler.Add(new Etki { id = id, ikon = ikon, kalan = saniye });
            Yenile();
        }

        public void Kaldir(string id)
        {
            for (int i = 0; i < etkiler.Count; i++)
                if (etkiler[i].id == id) { etkiler.RemoveAt(i); break; }
            MenuKapat();
            Yenile();
        }

        public void HepsiniKaldir() { etkiler.Clear(); MenuKapat(); Yenile(); }

        // Saga yasli: son etki en sagdaki hucrede.
        void Yenile()
        {
            int n = etkiler.Count, m = hucreler.Length;
            for (int i = 0; i < m; i++)
            {
                var h = hucreler[i];
                if (h == null || h.kok == null) continue;
                int e = i - (m - n);              // hucre i -> etki e
                bool acik = e >= 0;
                if (h.kok.activeSelf != acik) h.kok.SetActive(acik);
                if (acik && h.ikon != null) { h.ikon.sprite = etkiler[e].ikon; h.ikon.enabled = etkiler[e].ikon != null; }
            }
            SureleriYaz();
        }

        void SureleriYaz()
        {
            int n = etkiler.Count, m = hucreler.Length;
            for (int i = m - n; i < m; i++)
            {
                if (i < 0) continue;
                var h = hucreler[i];
                if (h == null || h.sure == null) continue;
                h.sure.text = SureMetni(etkiler[i - (m - n)].kalan);
            }
        }

        /// <summary>Oyunda 60 dakikalik scroll basilir basilmaz "59m" yazar: kalan tam dakika.</summary>
        public static string SureMetni(float saniye)
        {
            if (saniye >= 60f) return Mathf.FloorToInt(saniye / 60f) + "m";
            return Mathf.Max(0, Mathf.CeilToInt(saniye)) + "s";   // 1 dakikanin alti videoda yok: varsayim
        }

        void MenuAc(int hucre)
        {
            int e = hucre - (hucreler.Length - etkiler.Count);
            if (e < 0 || menu == null) return;
            if (secili == e && menu.gameObject.activeSelf) { MenuKapat(); return; }
            secili = e;
            var hr = hucreler[hucre].kok.GetComponent<RectTransform>();
            menu.anchoredPosition = new Vector2(hr.anchoredPosition.x + menuKaymasi, menu.anchoredPosition.y);
            menu.gameObject.SetActive(true);
        }

        public void MenuKapat()
        {
            secili = -1;
            if (menu != null) menu.gameObject.SetActive(false);
        }

        void SeciliyiSil()
        {
            if (secili < 0 || secili >= etkiler.Count) { MenuKapat(); return; }
            string id = etkiler[secili].id;
            etkiler.RemoveAt(secili);
            MenuKapat();
            Yenile();
            onRemoved.Invoke(id);
        }
    }
}
