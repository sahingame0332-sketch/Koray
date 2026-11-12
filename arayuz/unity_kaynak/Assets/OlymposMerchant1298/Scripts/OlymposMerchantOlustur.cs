// OLYMPOS-KO · 1298 "Create a Merchant" penceresi (756 x 851, zemin alfa 0.95)
// Ustte 6 x 2 tezgah yuvasi, altta 7 x 4 envanter.
//   envanter esyasina dokun -> [yiginliysa adet diyalogu ->] fiyat diyalogu -> OK -> esya ilk bos tezgah yuvasina gecer
//   (toplu esya: girilen adet kadari tezgaha gecer, kalani envanterde kalir; fiyat TEK esya icindir —
//    diyalogdaki "If there are more than one item, enter the price for each one" uyarisi)
//   tezgahtaki esyaya dokun -> bilgi penceresi ("Purchase Price", Remove / Close); Remove esyayi envantere geri koyar
//   OK -> tezgah acilir (en az bir esya varsa) ; CANCEL -> esyalar envantere doner, pencere kapanir
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Create a Merchant")]
    public class OlymposMerchantOlustur : MonoBehaviour
    {
        public const int TezgahYuvasi = 12, EnvanterYuvasi = 28;

        public Image background;
        public Image titleBackground;
        [Range(0f, 1f)] public float backgroundAlpha = 0.95f;
        public OlymposTicariYuva[] tezgahYuvalari = new OlymposTicariYuva[TezgahYuvasi];
        public OlymposTicariYuva[] envanterYuvalari = new OlymposTicariYuva[EnvanterYuvasi];
        public Button okButton;
        public Button cancelButton;
        public OlymposFiyatDiyalogu fiyatDiyalogu;
        [Tooltip("Yiginli esyada fiyattan once acilir. Bos birakilirsa yiginin tamami konur.")]
        public OlymposAdetDiyalogu adetDiyalogu;
        public OlymposEsyaBilgiPenceresi bilgi;

        [Tooltip("Tezgah acildi: satisa konan esyalar tezgahFiyati dolu olarak gelir.")]
        public UnityEvent onTezgahAcildi = new UnityEvent();
        public UnityEvent onIptal = new UnityEvent();

        /// <summary>Envanter (yuva sirasiyla; bos yuva null). Yonetici verir.</summary>
        public List<OlymposTicariEsya> envanter;
        public readonly OlymposTicariEsya[] tezgah = new OlymposTicariEsya[TezgahYuvasi];
        int bekleyen = -1;     // fiyati sorulan envanter yuvasi
        int bekleyenAdet = 1;  // tezgaha konacak adet

        void Awake()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) { tezgahYuvalari[i].sira = i; tezgahYuvalari[i].onTiklandi.AddListener(TezgahaDokun); }
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) { envanterYuvalari[i].sira = i; envanterYuvalari[i].onTiklandi.AddListener(EnvantereDokun); }
            if (okButton != null) okButton.onClick.AddListener(Tamam);
            if (cancelButton != null) cancelButton.onClick.AddListener(Vazgec);
            if (fiyatDiyalogu != null)
            {
                fiyatDiyalogu.onOnay.AddListener(FiyatVerildi);
                fiyatDiyalogu.onIptal.AddListener(delegate { bekleyen = -1; });
            }
            if (adetDiyalogu != null)
            {
                adetDiyalogu.onOnay.AddListener(AdetVerildi);
                adetDiyalogu.onIptal.AddListener(delegate { bekleyen = -1; });
            }
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            var c = new Color(0f, 0f, 0f, backgroundAlpha);
            if (background != null) background.color = c;
            if (titleBackground != null) titleBackground.color = c;
        }

        public void Ac(List<OlymposTicariEsya> env)
        {
            envanter = env;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            Ciz();
        }

        public int TezgahtakiAdet
        {
            get { int n = 0; for (int i = 0; i < tezgah.Length; i++) if (tezgah[i] != null) n++; return n; }
        }

        void Ciz()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) tezgahYuvalari[i].Goster(tezgah[i]);
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].Goster(envanter != null && i < envanter.Count ? envanter[i] : null);
        }

        void EnvantereDokun(int i)
        {
            if (envanter == null || i >= envanter.Count || envanter[i] == null || fiyatDiyalogu == null) return;
            if (TezgahtakiAdet >= TezgahYuvasi) return;
            if (bilgi != null) bilgi.Kapat();
            bekleyen = i;
            bekleyenAdet = envanter[i].adet;
            if (envanter[i].adet > 1 && adetDiyalogu != null) adetDiyalogu.Ac(envanter[i].adet);
            else fiyatDiyalogu.Ac();
        }

        void AdetVerildi(long adet)
        {
            if (envanter == null || bekleyen < 0 || bekleyen >= envanter.Count || envanter[bekleyen] == null) { bekleyen = -1; return; }
            bekleyenAdet = (int)Mathf.Clamp(adet, 1, envanter[bekleyen].adet);
            fiyatDiyalogu.Ac();
        }

        void FiyatVerildi(long fiyat)
        {
            int i = bekleyen; bekleyen = -1;
            if (envanter == null || i < 0 || i >= envanter.Count || envanter[i] == null) return;
            if (fiyat <= 0) return;                    // 0 fiyatla esya konmaz (varsayim: videoda denenmedi)
            for (int k = 0; k < tezgah.Length; k++)
                if (tezgah[k] == null)
                {
                    var e = envanter[i];
                    if (bekleyenAdet < e.adet) { var parca = e.Kopya(bekleyenAdet); e.adet -= bekleyenAdet; e = parca; }   // yigin bolunur
                    else envanter[i] = null;
                    e.tezgahFiyati = fiyat;
                    tezgah[k] = e;
                    break;
                }
            Ciz();
        }

        void TezgahaDokun(int k)
        {
            if (k < 0 || k >= tezgah.Length || tezgah[k] == null || bilgi == null) return;
            bilgi.GosterTezgahKurulum(tezgah[k], (RectTransform)tezgahYuvalari[k].transform, Kaldir);
        }

        void Kaldir(OlymposTicariEsya e)
        {
            for (int k = 0; k < tezgah.Length; k++)
                if (tezgah[k] == e) { tezgah[k] = null; EnvantereKoy(e); break; }
            Ciz();
        }

        void EnvantereKoy(OlymposTicariEsya e)
        {
            if (envanter == null) return;
            e.tezgahFiyati = 0;
            // envanterde ayni esyanin yigini varsa ona eklenir (bolunmus yigin geri birlesir)
            if (!string.IsNullOrEmpty(e.id))
                for (int i = 0; i < envanter.Count; i++)
                    if (envanter[i] != null && envanter[i] != e && envanter[i].id == e.id) { envanter[i].adet += e.adet; return; }
            for (int i = 0; i < envanter.Count; i++) if (envanter[i] == null) { envanter[i] = e; return; }
            envanter.Add(e);
        }

        /// <summary>Tezgahtaki butun esyalari envantere geri koyar (CANCEL, tezgahi kapatma, Close Slave Merchant).</summary>
        public void HepsiniGeriAl()
        {
            for (int k = 0; k < tezgah.Length; k++)
                if (tezgah[k] != null) { EnvantereKoy(tezgah[k]); tezgah[k] = null; }
            if (gameObject.activeSelf) Ciz();
        }

        void Kapat()
        {
            if (bilgi != null) bilgi.Kapat();
            if (fiyatDiyalogu != null) fiyatDiyalogu.gameObject.SetActive(false);
            if (adetDiyalogu != null) adetDiyalogu.gameObject.SetActive(false);
            gameObject.SetActive(false);
        }

        void Tamam()
        {
            if (TezgahtakiAdet == 0) { Vazgec(); return; }     // bos tezgah acilmaz (varsayim)
            Kapat();
            onTezgahAcildi.Invoke();
        }

        void Vazgec()
        {
            HepsiniGeriAl();
            Kapat();
            onIptal.Invoke();
        }
    }
}
