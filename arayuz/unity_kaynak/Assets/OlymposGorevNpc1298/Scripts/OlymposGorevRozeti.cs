// OLYMPOS-KO · 1298 NPC basinin ustundeki "?" gorev rozeti — 350 x 350 (telefon pikseli, kayitta merkez (985,175)).
// Karisim olculdu: merkezde isik zemine EKLENIYOR, kenarda ortuyor -> on-carpimli (premultiplied) sprite,
// malzeme "Olympos/UI On Carpimli" (Blend One OneMinusSrcAlpha). Ad etiketi gibi ekranda sabit boyutta, NPC'yi izler.
// Not: orijinalde rozet dunyadadir (sag alti duvarin arkasinda kaliyor); bu surum ekran katmaninda, duvar ortmesi yok.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Gorev/Gorev Rozeti (?)")]
    public class OlymposGorevRozeti : MonoBehaviour
    {
        public Transform npc;
        [Tooltip("NPC pivotundan yukari dunya birimi (bas ustu).")]
        public float yukseklik = 2.6f;
        public Vector2 ekranKaydirma = Vector2.zero;
        public Camera kamera;
        public Image gorsel;
        [Tooltip("Gorev verilebiliyorsa goster. Oyuncu tum gorevleri aldiysa kapatin.")]
        public bool gorevVar = true;

        Canvas canvas;

        void Awake() { canvas = GetComponentInParent<Canvas>(); }

        void LateUpdate()
        {
            if (gorsel == null) return;
            if (!gorevVar || npc == null || canvas == null) { gorsel.enabled = gorevVar && npc == null; return; }
            var k = kamera != null ? kamera : Camera.main; if (k == null) return;
            Vector3 s = k.WorldToScreenPoint(npc.position + Vector3.up * yukseklik);
            gorsel.enabled = s.z > 0f; if (s.z <= 0f) return;
            var cr = (RectTransform)canvas.transform; Vector2 yerel;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(cr, s, canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera, out yerel);
            transform.position = cr.TransformPoint(yerel + ekranKaydirma);
        }
    }
}
