// OLYMPOS-KO · 1298 "Save Skill Slot Stat" penceresi (526 x 1056, 4 kayit)
// Save     : o anki skill bar dizilimi + skill puanlari kayda yazilir
// Activate : kayittaki dizilim skill bara geri yuklenir, puanlar olayla oyuna bildirilir
// Zemin siyah, alfa 0.95 (pencerenin arkasindan gorunen oyuncu adinin parlakligindan olculdu).
using System;
using System.Text;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposSkillKayitOlayi : UnityEvent<int> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Save Skill Slot")]
    public class OlymposSaveSkillSlot : MonoBehaviour
    {
        public const int KayitSayisi = 4;

        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.95f;

        [Header("Satirlar")]
        public Text[] statusTexts = new Text[KayitSayisi];
        public Button[] saveButtons = new Button[KayitSayisi];
        public Button[] activateButtons = new Button[KayitSayisi];
        public Button closeButton;

        [Header("Kaynaklar")]
        public OlymposHizliSlotCubugu slotCubugu;
        [Tooltip("Skill dallarinin adlari. Buyucu icin: Fire, Ice, Lightning, Master")]
        public string[] dalAdlari = { "Fire", "Ice", "Lightning", "Master" };
        [Tooltip("Dallara verilmis puanlar. Oyun bunu guncel tutar; Save bu degerleri kaydeder.")]
        public int[] dalPuanlari = { 0, 0, 0, 0 };

        [Header("Kayit")]
        public string bosMetni = "- Empty -";
        [Tooltip("PlayerPrefs anahtari on eki. Bos birakilirsa diske yazilmaz (sunucu tarafli kayit icin).")]
        public string playerPrefsOnEki = "olympos.skillslot.";

        [Header("Olaylar")]
        public OlymposSkillKayitOlayi onKaydedildi = new OlymposSkillKayitOlayi();
        [Tooltip("Activate sonrasi: Kayit(i).dalPuanlari oyunun skill puanlarina uygulanmali.")]
        public OlymposSkillKayitOlayi onEtkinlestirildi = new OlymposSkillKayitOlayi();
        public UnityEvent onClosed = new UnityEvent();

        readonly OlymposSkillKaydi[] kayitlar = new OlymposSkillKaydi[KayitSayisi];

        void Awake()
        {
            for (int i = 0; i < KayitSayisi; i++)
            {
                int k = i;
                if (kayitlar[i] == null) kayitlar[i] = Oku(i);      // KayitAta ile onceden verilmis kaydi ezme
                if (i < saveButtons.Length && saveButtons[i] != null) saveButtons[i].onClick.AddListener(delegate { Kaydet(k); });
                if (i < activateButtons.Length && activateButtons[i] != null) activateButtons[i].onClick.AddListener(delegate { Etkinlestir(k); });
            }
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
            Yenile();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        public OlymposSkillKaydi Kayit(int i) { return i >= 0 && i < KayitSayisi ? kayitlar[i] : null; }

        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); Yenile(); }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        public void Kaydet(int i)
        {
            if (i < 0 || i >= KayitSayisi) return;
            var k = new OlymposSkillKaydi();
            k.dolu = true;
            k.slotEsyaIdleri = slotCubugu != null ? slotCubugu.Kaydet() : new string[0];
            k.dalAdlari = (string[])dalAdlari.Clone();
            k.dalPuanlari = (int[])dalPuanlari.Clone();
            kayitlar[i] = k;
            Yaz(i, k);
            Yenile();
            onKaydedildi.Invoke(i);
        }

        public void Etkinlestir(int i)
        {
            if (i < 0 || i >= KayitSayisi) return;
            var k = kayitlar[i];
            if (k == null || !k.dolu) return;               // bos kayit etkinlestirilemez
            if (slotCubugu != null) slotCubugu.Yukle(k.slotEsyaIdleri);
            if (k.dalPuanlari != null) dalPuanlari = (int[])k.dalPuanlari.Clone();
            onEtkinlestirildi.Invoke(i);
        }

        public void Sil(int i)
        {
            if (i < 0 || i >= KayitSayisi) return;
            kayitlar[i] = new OlymposSkillKaydi();
            if (!string.IsNullOrEmpty(playerPrefsOnEki)) PlayerPrefs.DeleteKey(playerPrefsOnEki + i);
            Yenile();
        }

        void Yenile()
        {
            for (int i = 0; i < KayitSayisi && i < statusTexts.Length; i++)
                if (statusTexts[i] != null) statusTexts[i].text = DurumMetni(kayitlar[i]);
        }

        // Olculen bicim:  "Fire:41 - Ice:23" / "Lightning:0 - Master:0"  (satir basina iki dal)
        string DurumMetni(OlymposSkillKaydi k)
        {
            if (k == null || !k.dolu || k.dalAdlari == null || k.dalPuanlari == null) return bosMetni;
            var sb = new StringBuilder();
            int n = Mathf.Min(k.dalAdlari.Length, k.dalPuanlari.Length);
            for (int j = 0; j < n; j++)
            {
                if (j > 0) sb.Append(j % 2 == 0 ? "\n" : " - ");
                sb.Append(k.dalAdlari[j]).Append(':').Append(k.dalPuanlari[j]);
            }
            return n == 0 ? bosMetni : sb.ToString();
        }

        OlymposSkillKaydi Oku(int i)
        {
            if (!string.IsNullOrEmpty(playerPrefsOnEki))
            {
                string json = PlayerPrefs.GetString(playerPrefsOnEki + i, "");
                if (!string.IsNullOrEmpty(json))
                {
                    var k = JsonUtility.FromJson<OlymposSkillKaydi>(json);
                    if (k != null) return k;
                }
            }
            return new OlymposSkillKaydi();
        }

        void Yaz(int i, OlymposSkillKaydi k)
        {
            if (string.IsNullOrEmpty(playerPrefsOnEki)) return;
            PlayerPrefs.SetString(playerPrefsOnEki + i, JsonUtility.ToJson(k));
            PlayerPrefs.Save();
        }

        /// <summary>Sunucudan gelen kaydi yerlestirir (diske yazmaz).</summary>
        public void KayitAta(int i, OlymposSkillKaydi k)
        {
            if (i < 0 || i >= KayitSayisi) return;
            kayitlar[i] = k ?? new OlymposSkillKaydi();
            Yenile();
        }
    }
}
