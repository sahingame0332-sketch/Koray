// OLYMPOS-KO · 1298 Select Upgrade menusu — TEK BASINA paket (OlymposSelectUpgrade1298). Olculer: arayuz/23-upgrade.md
// Govde duz siyah alfa 0.93 (sol kenardan olculdu); baslik + kenar + 4 dugme opak (orijinal piksel, yazilar sprite'ta).
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/SelectUpgrade/Select Upgrade Menusu")]
    public class OlymposSelectUpgradePenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;
        [Header("Dugmeler")]
        public Button itemUpgradeButton;
        public Button fastUpgradeButton;
        public Button accessoryUpgradeButton;
        public Button closeButton;
        [Header("Deneme")]
        public bool acilistaGoster = true;
        [Header("Olaylar (secimden sonra menu kapanir)")]
        public UnityEvent onItemUpgrade = new UnityEvent();
        public UnityEvent onFastUpgrade = new UnityEvent();
        public UnityEvent onAccessoryUpgrade = new UnityEvent();
        public UnityEvent onClose = new UnityEvent();

        void Awake()
        {
            if (itemUpgradeButton != null) itemUpgradeButton.onClick.AddListener(() => Sec(onItemUpgrade));
            if (fastUpgradeButton != null) fastUpgradeButton.onClick.AddListener(() => Sec(onFastUpgrade));
            if (accessoryUpgradeButton != null) accessoryUpgradeButton.onClick.AddListener(() => Sec(onAccessoryUpgrade));
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }
        void Start() { if (!acilistaGoster) gameObject.SetActive(false); }
        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }
        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Kapat() { gameObject.SetActive(false); onClose.Invoke(); }
        void Sec(UnityEvent e) { gameObject.SetActive(false); e.Invoke(); }
    }
}
