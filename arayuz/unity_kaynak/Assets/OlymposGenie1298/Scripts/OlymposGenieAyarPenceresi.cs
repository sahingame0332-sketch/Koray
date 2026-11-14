// OLYMPOS-KO · 1298 AUTO ATTACK SETTINGS penceresi (genie ayarlari) — 636 x 1162 sprite, siyah zemin 604 x 1108.
// Zemin: duz siyah, alfa 0.93 (olculdu: sahnenin orta tonlarinda arkadan gecen isik ~%7; bkz. arayuz/11-genie.md).
// Basliklar, slot cerceveleri ve numaralari, POTION cubugu, HP/MP rozetleri, kaydirici izleri, onay kutulari ve etiketleri
// orijinal piksellerden. Hareketli: 4 kaydirici topuzu + deger, 4 onay isareti, slot ikonlari.
// Slotlar: ATTACK & DEBUFF 12 + HEAL & BUFFS (HP-AC) 12 + HP / MP iksiri. Ikon koymak: SlotAyarla(grup, sira, sprite).
// Ayarlar PlayerPrefs'e (anahtar oneki) kaydedilir.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposGenieSlotGrubu { SaldiriDebuff = 0, IyilestirmeBuff = 1, Iksir = 2 }
    [Serializable] public class OlymposGenieSlotOlayi : UnityEvent<OlymposGenieSlotGrubu, int> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Genie/Auto Attack Settings")]
    public class OlymposGenieAyarPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;
        public bool acilistaGoster = false;

        [Header("Slot ikonlari")]
        public Image[] saldiriSlotlari = new Image[12];
        public Image[] destekSlotlari = new Image[12];
        [Tooltip("0 = HP iksiri, 1 = MP iksiri")]
        public Image[] iksirSlotlari = new Image[2];

        [Header("Ayarlar")]
        public OlymposGenieKaydirici saldiriMenzili;      // ATTACK RANGE (40)
        public OlymposGenieKaydirici skillYenileme;       // USE SKILL RECOVERY AT (%70)
        public OlymposGenieKaydirici hpIksiri;            // AT % CONSUME HP POTION (%80)
        public OlymposGenieKaydirici mpIksiri;            // AT % CONSUME MP POTION (%50)
        public OlymposGenieOnay temelSaldiri;             // [R] Basic Attack
        public OlymposGenieOnay genieSpirit;              // Use Genie Sprit (orijinal yazim)
        public OlymposGenieOnay partiLideri;              // Follow Party Leader
        public OlymposGenieOnay sirayla;                  // Skill Use in Order

        public Button kapatButton;
        public string kayitOneki = "OlymposGenie.";

        [Header("Olaylar")]
        [Tooltip("Bir slota dokunuldu: oyun secili skill / iksiri SlotAyarla ile koyar.")]
        public OlymposGenieSlotOlayi onSlotTiklandi = new OlymposGenieSlotOlayi();
        public UnityEvent onKapandi = new UnityEvent();

        void Awake()
        {
            if (kapatButton != null) kapatButton.onClick.AddListener(Kapat);
            BagliSlotlar(saldiriSlotlari, OlymposGenieSlotGrubu.SaldiriDebuff);
            BagliSlotlar(destekSlotlari, OlymposGenieSlotGrubu.IyilestirmeBuff);
            BagliSlotlar(iksirSlotlari, OlymposGenieSlotGrubu.Iksir);
            ZeminiUygula();
            Yukle();
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        void BagliSlotlar(Image[] dizi, OlymposGenieSlotGrubu g)
        {
            for (int i = 0; i < dizi.Length; i++)
            {
                if (dizi[i] == null) continue;
                int sira = i; var b = dizi[i].GetComponentInParent<Button>();
                if (b != null) b.onClick.AddListener(() => onSlotTiklandi.Invoke(g, sira));
            }
        }

        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Kapat() { Kaydet(); gameObject.SetActive(false); onKapandi.Invoke(); }

        public void SlotAyarla(OlymposGenieSlotGrubu g, int sira, Sprite ikon)
        {
            var dizi = g == OlymposGenieSlotGrubu.SaldiriDebuff ? saldiriSlotlari : g == OlymposGenieSlotGrubu.IyilestirmeBuff ? destekSlotlari : iksirSlotlari;
            if (sira < 0 || sira >= dizi.Length || dizi[sira] == null) return;
            dizi[sira].sprite = ikon;
            dizi[sira].color = ikon != null ? Color.white : new Color(1f, 1f, 1f, 0f);
        }

        public void Kaydet()
        {
            K("menzil", saldiriMenzili); K("yenileme", skillYenileme); K("hp", hpIksiri); K("mp", mpIksiri);
            O("temel", temelSaldiri); O("spirit", genieSpirit); O("parti", partiLideri); O("sira", sirayla);
            PlayerPrefs.Save();
        }

        public void Yukle()
        {
            Y("menzil", saldiriMenzili); Y("yenileme", skillYenileme); Y("hp", hpIksiri); Y("mp", mpIksiri);
            Y("temel", temelSaldiri); Y("spirit", genieSpirit); Y("parti", partiLideri); Y("sira", sirayla);
        }

        void K(string a, OlymposGenieKaydirici k) { if (k != null) PlayerPrefs.SetInt(kayitOneki + a, k.deger); }
        void O(string a, OlymposGenieOnay o) { if (o != null) PlayerPrefs.SetInt(kayitOneki + a, o.isaretli ? 1 : 0); }
        void Y(string a, OlymposGenieKaydirici k) { if (k != null && PlayerPrefs.HasKey(kayitOneki + a)) k.Ayarla(PlayerPrefs.GetInt(kayitOneki + a), false); }
        void Y(string a, OlymposGenieOnay o) { if (o != null && PlayerPrefs.HasKey(kayitOneki + a)) o.Ayarla(PlayerPrefs.GetInt(kayitOneki + a) == 1, false); }
    }
}
