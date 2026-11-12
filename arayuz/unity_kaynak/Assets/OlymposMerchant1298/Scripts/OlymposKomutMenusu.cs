// OLYMPOS-KO · 1298 komut menusu (alt bardaki "Commands"): POWER-UP-STORE, OPEN MERCHANT, SLAVE MERCHANT,
// SEEKING PARTY, OPTIONS, FORUM, DISCORD, INSTAGRAM. Zemin siyah, alfa 0.94.
// Bir komuta basinca menu kapanir ve olay gonderilir.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposKomut { PowerUpStore, OpenMerchant, SlaveMerchant, SeekingParty, Options, Forum, Discord, Instagram }

    [Serializable] public class OlymposKomutOlayi : UnityEvent<int> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Komut Menusu")]
    public class OlymposKomutMenusu : MonoBehaviour
    {
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.94f;
        [Tooltip("OlymposKomut sirasiyla 8 dugme.")]
        public Button[] dugmeler = new Button[8];
        public Button closeButton;

        [Tooltip("Basilan komutun sirasi (OlymposKomut).")]
        public OlymposKomutOlayi onKomut = new OlymposKomutOlayi();
        public UnityEvent onOpenMerchant = new UnityEvent();
        public UnityEvent onSlaveMerchant = new UnityEvent();

        void Awake()
        {
            for (int i = 0; i < dugmeler.Length; i++)
            {
                int k = i;
                if (dugmeler[i] != null) dugmeler[i].onClick.AddListener(delegate { Bas(k); });
            }
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void OnValidate() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Kapat() { gameObject.SetActive(false); }
        public void AcKapat() { if (gameObject.activeSelf) Kapat(); else Ac(); }

        void Bas(int k)
        {
            Kapat();
            onKomut.Invoke(k);
            if (k == (int)OlymposKomut.OpenMerchant) onOpenMerchant.Invoke();
            else if (k == (int)OlymposKomut.SlaveMerchant) onSlaveMerchant.Invoke();
        }
    }
}
