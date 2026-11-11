// OLYMPOS-KO · 1298 oyun ici yonetici: parcalari birbirine baglar.
//   envanter yuvasi -> esya penceresi -> Use Self -> adet-1, "Using - ..." bilgisi, buff ikonu
//   hizli slot      -> ayni basma yolu
//   buff ikonu      -> Remove -> etki silinir (oyun statlari geri alir)
//   hedef cubugu    -> Show Drops -> drop listesi ;  X -> hedef birakilir
// Oyunun kendi sistemleri olaylara abone olur; bu betik yalnizca arayuz akisini tasir.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    [Serializable] public class OlymposBilgiOlayi : UnityEvent<string> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Yonetici")]
    public class OlymposOyunIciYonetici : MonoBehaviour
    {
        [Header("Parcalar")]
        public OlymposEsyaPenceresi esyaPenceresi;
        public OlymposBuffCubugu buffCubugu;
        public OlymposHizliSlotCubugu slotCubugu;
        public OlymposHedefCubugu hedefCubugu;
        public OlymposDropListesi dropListesi;
        public OlymposSaveSkillSlot saveSkillSlot;

        [Header("Envanter")]
        public List<OlymposEsya> envanter = new List<OlymposEsya>();
        [Tooltip("Adetleri tazelenecek envanter yuvalari (istege bagli).")]
        public OlymposEnvanterYuvasi[] envanterYuvalari = new OlymposEnvanterYuvasi[0];

        [Header("Save Skill Slot")]
        [Tooltip("SKILL PAGE'deki \"Save skill slot\" dugmesi (ya da deneme dugmesi): pencereyi acar.")]
        public UnityEngine.UI.Button saveSkillSlotAcDugmesi;

        [Header("Bilgi satiri")]
        [Tooltip("Oyundaki bicim: \"Using - Hp Scroll 500(L)\"")]
        public string kullanimOnEki = "Using - ";

        [Header("Deneme")]
        [Tooltip("Isaretliyse Start'ta ornek bir hedef secilir (Show Drops ve X'i denemek icin).")]
        public bool denemeHedefi = true;
        public string denemeHedefAdi = "Kecoon fighter";
        public int denemeHedefSeviyesi = 12;

        [Header("Olaylar")]
        [Tooltip("Information paneline yazilacak satir.")]
        public OlymposBilgiOlayi onBilgi = new OlymposBilgiOlayi();
        [Tooltip("Esya kendine basildi: etkisini (HP +500 vb.) oyun uygular.")]
        public OlymposEsyaOlayi onKendineKullanildi = new OlymposEsyaOlayi();
        [Tooltip("Esya secili hedefe basildi.")]
        public OlymposEsyaOlayi onHedefeKullanildi = new OlymposEsyaOlayi();
        public OlymposEsyaOlayi onKusanildi = new OlymposEsyaOlayi();
        [Tooltip("Etki Remove ile silindi ya da suresi doldu (esya kimligi): oyun etkiyi geri alir.")]
        public OlymposBuffOlayi onEtkiBitti = new OlymposBuffOlayi();

        void Awake()
        {
            if (slotCubugu != null)
            {
                slotCubugu.yonetici = this;
                slotCubugu.onBasildi.AddListener(SlotBasildi);
            }
            if (esyaPenceresi != null)
            {
                esyaPenceresi.onUseSelf.AddListener(delegate (OlymposEsya e) { Kullan(e, false); });
                esyaPenceresi.onUseTarget.AddListener(delegate (OlymposEsya e) { Kullan(e, true); });
                esyaPenceresi.onEquip.AddListener(delegate (OlymposEsya e) { onKusanildi.Invoke(e); });
                esyaPenceresi.gameObject.SetActive(false);
            }
            if (buffCubugu != null)
            {
                buffCubugu.onRemoved.AddListener(delegate (string id) { onEtkiBitti.Invoke(id); });
                buffCubugu.onExpired.AddListener(delegate (string id) { onEtkiBitti.Invoke(id); });
            }
            if (hedefCubugu != null && dropListesi != null)
                hedefCubugu.onShowDrops.AddListener(dropListesi.Ac);
            if (dropListesi != null) dropListesi.gameObject.SetActive(false);
            if (saveSkillSlot != null && saveSkillSlot.slotCubugu == null) saveSkillSlot.slotCubugu = slotCubugu;
            if (saveSkillSlotAcDugmesi != null) saveSkillSlotAcDugmesi.onClick.AddListener(SaveSkillSlotAc);
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].yonetici = this;
        }

        void Start()
        {
            Tazele();
            if (denemeHedefi && hedefCubugu != null) hedefCubugu.HedefSec(denemeHedefAdi, denemeHedefSeviyesi, 1f);
        }

        public OlymposEsya EsyaBul(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            for (int i = 0; i < envanter.Count; i++)
                if (envanter[i] != null && envanter[i].id == id) return envanter[i];
            return null;
        }

        public void EsyaPenceresiniAc(string esyaId, RectTransform yuva)
        {
            var e = EsyaBul(esyaId);
            if (e != null && e.adet > 0 && esyaPenceresi != null) esyaPenceresi.Goster(e, yuva);
        }

        void SlotBasildi(int sira, string esyaId) { Kullan(EsyaBul(esyaId), false); }

        /// <summary>Esyayi basar. Basarili olursa adet 1 azalir, bilgi satiri yazilir, etki ikonu eklenir.</summary>
        public bool Kullan(OlymposEsya e, bool hedefe)
        {
            if (e == null || e.adet <= 0) return false;
            if (hedefe && (hedefCubugu == null || !hedefCubugu.HedefVar)) return false;   // hedef yokken Use Target islemez
            e.adet--;
            onBilgi.Invoke(kullanimOnEki + (string.IsNullOrEmpty(e.kullanimAdi) ? e.ad : e.kullanimAdi));
            if (hedefe) onHedefeKullanildi.Invoke(e);
            else
            {
                if (e.buffSuresi > 0f && buffCubugu != null) buffCubugu.Ekle(e.id, e.ikon, e.buffSuresi);
                onKendineKullanildi.Invoke(e);
            }
            Tazele();
            return true;
        }

        /// <summary>Envanter disaridan degistiginde (satin alma, drop...) adetleri gunceller.</summary>
        public void Tazele()
        {
            if (slotCubugu != null) slotCubugu.Yenile();
            for (int i = 0; i < envanterYuvalari.Length; i++)
            {
                var y = envanterYuvalari[i];
                if (y != null) y.Goster(EsyaBul(y.esyaId));
            }
        }

        public void SaveSkillSlotAc() { if (saveSkillSlot != null) saveSkillSlot.Ac(); }
    }
}
