// OLYMPOS-KO · 1298 Respawn penceresi (karakter olunce) — TEK BASINA paket
// 700 x 386 (telefon pikseli; ekranda (1985,645), 2712 x 1220 duzeni). Zemin duz siyah, alfa 0.92 (olculdu).
// "Respawn" (sari #EDF522), mesaj (beyaz) ve Confirm dugmesi orijinal piksellerden (yazilarin harf araligi Unity
// legacy Text ile verilemedigi icin yazi da sprite'ta). Ayni mesaj farkli dilde istenirse: yaziSprite yerine
// bosSprite + kendi Text'leriniz (olculen: Roboto Slab Bold, buyuk harf yuksekligi 20 px ~28 punto, harf araligi +1.8 px).
// Kullanim: pencere.Goster();  pencere.onOnay -> karakteri yeniden dogma noktasina isinla.
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Respawn Penceresi")]
    public class OlymposRespawnPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.92f;

        [Header("Parcalar")]
        public Image krom;
        public Button confirmButton;
        [Tooltip("Pencere acikken arkadaki HUD'a dokunmayi engelle.")]
        public bool arkayiKilitle = true;
        public Image engelleyici;

        [Header("Deneme")]
        public bool acilistaGoster = true;

        [Header("Olaylar")]
        [Tooltip("Confirm: yeniden dogma noktasina isinla.")]
        public UnityEvent onOnay = new UnityEvent();

        void Awake()
        {
            if (confirmButton != null) confirmButton.onClick.AddListener(Onayla);
            ZeminiUygula();
        }

        void Start() { if (!acilistaGoster) gameObject.SetActive(false); }
        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
            if (engelleyici != null) engelleyici.raycastTarget = arkayiKilitle;
        }

        public void Goster() { gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Gizle() { gameObject.SetActive(false); }

        public void Onayla()
        {
            Gizle();
            onOnay.Invoke();
        }
    }
}
