// OLYMPOS-KO · 1298 hizli slot cubugu (bu cihazda 14 yuva; konumlar 2712x1220 kareden olculdu)
using System;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    [Serializable] public class OlymposSlotOlayi : UnityEvent<int, string> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Hizli Slot Cubugu")]
    public class OlymposHizliSlotCubugu : MonoBehaviour
    {
        public OlymposHizliSlot[] slotlar = new OlymposHizliSlot[0];
        [Tooltip("Esyayi kimlikten bulur. Bos birakilirsa yonetici baglar.")]
        public OlymposOyunIciYonetici yonetici;

        [Header("Olaylar")]
        [Tooltip("Yuvaya dokunuldu (sira, esya kimligi). Esyayi basmak yoneticinin isi.")]
        public OlymposSlotOlayi onBasildi = new OlymposSlotOlayi();
        [Tooltip("Yuvaya esya atandi ya da yuva bosaltildi (sira, esya kimligi ya da bos).")]
        public OlymposSlotOlayi onDegisti = new OlymposSlotOlayi();

        void Awake()
        {
            for (int i = 0; i < slotlar.Length; i++)
                if (slotlar[i] != null) { slotlar[i].cubuk = this; slotlar[i].sira = i; }
        }

        OlymposEsya Bul(string id) { return yonetici != null ? yonetici.EsyaBul(id) : null; }

        public void Ata(int sira, string esyaId)
        {
            if (sira < 0 || sira >= slotlar.Length || slotlar[sira] == null) return;
            var e = Bul(esyaId);
            if (e == null) return;
            // ayni esya baska yuvadaysa oradan kalkar: bir esya tek yuvada durur
            for (int i = 0; i < slotlar.Length; i++)
                if (i != sira && slotlar[i] != null && slotlar[i].esyaId == esyaId) slotlar[i].Goster(null);
            slotlar[sira].Goster(e);
            onDegisti.Invoke(sira, esyaId);
        }

        public void Temizle(int sira)
        {
            if (sira < 0 || sira >= slotlar.Length || slotlar[sira] == null) return;
            slotlar[sira].Goster(null);
            onDegisti.Invoke(sira, "");
        }

        public void Bas(int sira)
        {
            if (sira < 0 || sira >= slotlar.Length || slotlar[sira] == null || !slotlar[sira].Dolu) return;
            onBasildi.Invoke(sira, slotlar[sira].esyaId);
        }

        /// <summary>Adetleri tazeler; adedi biten esyanin yuvasi bosalir.</summary>
        public void Yenile()
        {
            for (int i = 0; i < slotlar.Length; i++)
            {
                var s = slotlar[i];
                if (s == null || !s.Dolu) continue;
                var e = Bul(s.esyaId);
                if (e == null || e.adet <= 0) s.Goster(null); else s.Goster(e);
            }
        }

        public string[] Kaydet()
        {
            var d = new string[slotlar.Length];
            for (int i = 0; i < slotlar.Length; i++) d[i] = slotlar[i] != null && slotlar[i].Dolu ? slotlar[i].esyaId : "";
            return d;
        }

        public void Yukle(string[] idler)
        {
            for (int i = 0; i < slotlar.Length; i++)
            {
                if (slotlar[i] == null) continue;
                string id = idler != null && i < idler.Length ? idler[i] : null;
                var e = string.IsNullOrEmpty(id) ? null : Bul(id);
                slotlar[i].Goster(e != null && e.adet > 0 ? e : null);
            }
        }
    }
}
