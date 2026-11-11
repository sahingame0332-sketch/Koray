// OLYMPOS-KO · 1298 hizli slot (skill bar yuvasi)
// Envanterden surukleyip birakilan esya burada dairesel ikon + adet olarak durur;
// dokununca esya basilir. Esya envanterden cikmaz: yuva yalnizca kisayoldur.
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Hizli Slot")]
    public class OlymposHizliSlot : MonoBehaviour, IDropHandler, IPointerClickHandler
    {
        public OlymposHizliSlotCubugu cubuk;
        public int sira;
        [Tooltip("Bos yuvanin koyu ic diski (alfa 0.88 olculdu).")]
        public Image bosZemin;
        [Tooltip("Dairesel maskenin icindeki esya ikonu.")]
        public Image ikon;
        public GameObject ikonKoku;
        public Text adetText;

        [HideInInspector] public string esyaId;

        public bool Dolu { get { return !string.IsNullOrEmpty(esyaId); } }

        public void Goster(OlymposEsya e)
        {
            bool dolu = e != null;
            esyaId = dolu ? e.id : null;
            if (ikonKoku != null) ikonKoku.SetActive(dolu);
            if (ikon != null) { ikon.sprite = dolu ? e.ikon : null; ikon.enabled = dolu && e.ikon != null; }
            if (bosZemin != null) bosZemin.enabled = !dolu;
            if (adetText != null)
            {
                adetText.gameObject.SetActive(dolu);
                if (dolu) adetText.text = e.adet.ToString();
            }
        }

        public void OnDrop(PointerEventData eventData)
        {
            if (cubuk == null || eventData == null || eventData.pointerDrag == null) return;
            var kaynak = eventData.pointerDrag.GetComponent<OlymposEnvanterYuvasi>();
            if (kaynak != null && !string.IsNullOrEmpty(kaynak.esyaId)) cubuk.Ata(sira, kaynak.esyaId);
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (cubuk != null && Dolu) cubuk.Bas(sira);
        }
    }
}
