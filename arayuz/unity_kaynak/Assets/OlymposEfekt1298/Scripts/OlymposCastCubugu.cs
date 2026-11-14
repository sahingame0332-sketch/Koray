// OLYMPOS-KO · 1298 skill hazirlama (cast) cubugu: skill adi + yesil dolum + kalan sure ("0,2 sec")
// Olculer tablet kaydindan (2266 x 1488): cerceve 205 x 12 siyah, dolum 8 px yesil (dikey ton), ad Roboto Bold 15 #FDE1E2,
// sure Roboto Bold 17 #E3DF73. Kurucu telefon duzenine (2712 x 1220) 1/1.0405 ile cevirir.
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.Efekt
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Efekt/Cast Cubugu")]
    public class OlymposCastCubugu : MonoBehaviour
    {
        public Text adText;
        [Tooltip("Image.Type = Filled, yatay, soldan.")]
        public Image dolgu;
        public Text sureText;
        [Tooltip("Sure bicimi. Olculen: \"0,2 sec\" (ondalik ayirici virgul).")]
        public string sureBicimi = "{0:0.0} sec";
        public UnityEvent onBitti = new UnityEvent();

        float toplam, gecen;
        bool aktif;

        void Awake() { gameObject.SetActive(false); }

        /// <summary>Hazirlamayi baslatir. Ornek: Baslat("Pillar Of Fire", 1.5f)</summary>
        public void Baslat(string skillAdi, float saniye)
        {
            toplam = Mathf.Max(0.01f, saniye); gecen = 0f; aktif = true;
            if (adText != null) adText.text = skillAdi;
            gameObject.SetActive(true);
            Yaz();
        }

        public void Iptal() { aktif = false; gameObject.SetActive(false); }

        void Update()
        {
            if (!aktif) return;
            gecen += Time.deltaTime;
            if (gecen >= toplam) { aktif = false; gameObject.SetActive(false); onBitti.Invoke(); return; }
            Yaz();
        }

        void Yaz()
        {
            if (dolgu != null) dolgu.fillAmount = Mathf.Clamp01(gecen / toplam);
            if (sureText != null)
                sureText.text = string.Format(sureBicimi, Mathf.Max(0f, toplam - gecen)).Replace('.', ',');
        }
    }
}
