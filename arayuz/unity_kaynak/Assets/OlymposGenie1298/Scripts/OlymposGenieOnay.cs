// OLYMPOS-KO · 1298 Auto Attack Settings onay kutusu: kutu + etiket pencere gorselinde, onay isareti (beyaz tik) ayri Image.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposGenieOnayOlayi : UnityEvent<bool> { }

    [AddComponentMenu("OLYMPOS/1298/Genie/Genie Onay Kutusu")]
    public class OlymposGenieOnay : MonoBehaviour
    {
        public Button button;
        public Image isaret;
        public bool isaretli;
        public OlymposGenieOnayOlayi onDegisti = new OlymposGenieOnayOlayi();

        void Awake() { if (button != null) button.onClick.AddListener(Degistir); Uygula(); }
        void OnValidate() { Uygula(); }

        public void Degistir() { Ayarla(!isaretli); }
        public void Ayarla(bool v, bool olay = true)
        {
            bool d = v != isaretli; isaretli = v; Uygula();
            if (d && olay) onDegisti.Invoke(isaretli);
        }
        void Uygula() { if (isaret != null) isaret.enabled = isaretli; }
    }
}
