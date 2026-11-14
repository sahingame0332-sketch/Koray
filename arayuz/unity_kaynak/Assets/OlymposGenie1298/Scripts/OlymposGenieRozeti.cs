// OLYMPOS-KO · 1298 "GENIE" rozeti — genie calisirken karakterin ad etiketinin ustunde duran pembe isik halkasi + sari GENIE yazisi.
// Sprite 300 x 300 (telefon pikseli, normal alfa karisimi; harfler ve parilti yildizlari opak). Ekrana sabit boyutta cizilir
// (ad etiketleri gibi); konumu hedefin dunya konumundan + yukseklik ile hesaplanir. Kayitta rozet merkezi ad etiketi ustunun ~95 px ustunde.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Genie/Genie Rozeti")]
    public class OlymposGenieRozeti : MonoBehaviour
    {
        [Tooltip("Rozetin uzerinde duracagi karakter. Bos ise yerinde kalir.")]
        public Transform hedef;
        [Tooltip("Hedefin pivotundan yukari dunya birimi (bas ustu).")]
        public float yukseklik = 2.4f;
        [Tooltip("Ekran pikseli (2712x1220 duzeni) ek kaydirma.")]
        public Vector2 ekranKaydirma = Vector2.zero;
        public Camera kamera;
        public Image gorsel;

        RectTransform rt; Canvas canvas;

        void Awake() { rt = (RectTransform)transform; canvas = GetComponentInParent<Canvas>(); }

        public void Goster(bool goster) { gameObject.SetActive(goster); if (goster) LateUpdate(); }

        void LateUpdate()
        {
            if (hedef == null || canvas == null) return;
            var k = kamera != null ? kamera : Camera.main; if (k == null) return;
            Vector3 s = k.WorldToScreenPoint(hedef.position + Vector3.up * yukseklik);
            if (s.z < 0f) { if (gorsel != null) gorsel.enabled = false; return; }
            if (gorsel != null) gorsel.enabled = true;
            var cr = (RectTransform)canvas.transform; Vector2 yerel;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(cr, s, canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera, out yerel);
            rt.position = cr.TransformPoint(yerel + ekranKaydirma);
        }
    }
}
