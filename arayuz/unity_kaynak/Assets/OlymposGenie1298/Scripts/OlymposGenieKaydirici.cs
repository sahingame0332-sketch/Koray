// OLYMPOS-KO · 1298 Auto Attack Settings kaydiricisi: iz pencere gorselinin parcasi, topuz ve deger yazisi ayri.
// Topuz merkezi = izBasi + oran * izBoyu (olculen: 363.5 + p * 405, telefon pikseli). Iz uzerine dokunup surukleyince deger degisir.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposGenieDegerOlayi : UnityEvent<int> { }

    [AddComponentMenu("OLYMPOS/1298/Genie/Genie Kaydirici")]
    public class OlymposGenieKaydirici : MonoBehaviour, IPointerDownHandler, IDragHandler
    {
        public RectTransform topuz;
        public Text degerText;
        [Tooltip("Deger yazisi bicimi: \"{0}\" (Attack Range) veya \"%{0}\".")]
        public string bicim = "%{0}";
        public int enAz = 0;
        public int enCok = 100;
        public int deger = 50;
        [Tooltip("Topuz merkezinin en az / en cok degerdeki x konumu (bu nesnenin yerel koordinatinda).")]
        public float izBasi = 0f;
        public float izBoyu = 405f;
        public OlymposGenieDegerOlayi onDegisti = new OlymposGenieDegerOlayi();

        void OnEnable() { Uygula(); }
        void OnValidate() { deger = Mathf.Clamp(deger, enAz, enCok); Uygula(); }

        public void Ayarla(int v, bool olay = true)
        {
            v = Mathf.Clamp(v, enAz, enCok);
            bool degisti = v != deger; deger = v; Uygula();
            if (degisti && olay) onDegisti.Invoke(deger);
        }

        void Uygula()
        {
            float p = enCok > enAz ? (deger - enAz) / (float)(enCok - enAz) : 0f;
            if (topuz != null) { var a = topuz.anchoredPosition; a.x = izBasi + p * izBoyu; topuz.anchoredPosition = a; }
            if (degerText != null) degerText.text = string.Format(bicim, deger);
        }

        public void OnPointerDown(PointerEventData e) { Surukle(e); }
        public void OnDrag(PointerEventData e) { Surukle(e); }

        void Surukle(PointerEventData e)
        {
            Vector2 yerel;
            var rt = (RectTransform)transform;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(rt, e.position, e.pressEventCamera, out yerel)) return;
            // yerel: pivot (0,1) sol-ust -> x dogrudan
            float p = Mathf.Clamp01((yerel.x - izBasi) / izBoyu);
            Ayarla(Mathf.RoundToInt(enAz + p * (enCok - enAz)));
        }
    }
}
