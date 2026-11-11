// OLYMPOS-KO · 1298 envanter yuvasi davranisi
// Kendi envanter pencerenizdeki her yuvaya eklenir:
//   dokunma  -> esya eylem penceresi acilir (Use Self / Use Target / Equip / Close)
//   surukleme -> ikonun kopyasi parmagi izler, kaynak yuva bos gorunur; hizli slota birakilinca atanir
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Envanter Yuvasi")]
    public class OlymposEnvanterYuvasi : MonoBehaviour,
        IPointerClickHandler, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        public OlymposOyunIciYonetici yonetici;
        public string esyaId;
        public Image ikon;
        public Text adetText;
        [Tooltip("Suruklenen kopyanin kenari (px). Olculen: 89")]
        public float hayaletBoyu = 89f;

        RectTransform hayalet;
        bool surukleniyor;

        public void Goster(OlymposEsya e)
        {
            esyaId = e != null ? e.id : null;
            bool var = e != null && e.adet > 0;
            if (ikon != null) { ikon.sprite = var ? e.ikon : null; ikon.enabled = var && e.ikon != null; }
            if (adetText != null)
            {
                adetText.gameObject.SetActive(var);
                if (var) adetText.text = e.adet.ToString();
            }
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (surukleniyor || yonetici == null || string.IsNullOrEmpty(esyaId)) return;
            yonetici.EsyaPenceresiniAc(esyaId, (RectTransform)transform);
        }

        public void OnBeginDrag(PointerEventData eventData)
        {
            if (string.IsNullOrEmpty(esyaId) || ikon == null || ikon.sprite == null) return;
            var canvas = GetComponentInParent<Canvas>();
            if (canvas == null) return;
            surukleniyor = true;
            var go = new GameObject("SuruklenenEsya", typeof(RectTransform));
            hayalet = (RectTransform)go.transform;
            hayalet.SetParent(canvas.transform, false);
            hayalet.SetAsLastSibling();
            hayalet.sizeDelta = new Vector2(hayaletBoyu, hayaletBoyu);
            var img = go.AddComponent<Image>();
            img.sprite = ikon.sprite;
            img.raycastTarget = false;          // altindaki yuva birakmayi alabilsin
            ikon.enabled = false;               // oyunda kaynak yuva surukleme boyunca bos gorunur
            if (adetText != null) adetText.gameObject.SetActive(false);
            Tasi(eventData);
        }

        public void OnDrag(PointerEventData eventData) { Tasi(eventData); }

        void Tasi(PointerEventData eventData)
        {
            if (hayalet == null || eventData == null) return;
            hayalet.position = new Vector3(eventData.position.x, eventData.position.y, 0f);
        }

        public void OnEndDrag(PointerEventData eventData)
        {
            if (hayalet != null) Destroy(hayalet.gameObject);
            hayalet = null;
            surukleniyor = false;
            if (yonetici != null) Goster(yonetici.EsyaBul(esyaId));   // esya envanterde kalir
        }
    }
}
