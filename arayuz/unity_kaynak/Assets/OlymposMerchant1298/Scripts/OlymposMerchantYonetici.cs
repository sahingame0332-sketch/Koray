// OLYMPOS-KO · 1298 Merchant yoneticisi: parcalari birbirine baglar.
//   Commands -> komut menusu -> OPEN MERCHANT  -> Create a Merchant -> OK -> tezgah cubugu (+ slave suresi baslar)
//                             -> SLAVE MERCHANT -> Slave Merchant penceresi (tezgah acikken)
//   tezgah cubugu OPEN -> "<ad> Merchant" penceresi ; Close Slave Merchant -> tezgah kapanir, esyalar doner
// Oyunun kendi sistemleri olaylara abone olur.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Yonetici")]
    public class OlymposMerchantYonetici : MonoBehaviour
    {
        [Header("Parcalar")]
        public OlymposKomutMenusu komutMenusu;
        public OlymposMerchantOlustur olustur;
        public OlymposTezgahCubugu tezgahCubugu;
        public OlymposMerchantPenceresi merchantPenceresi;
        public OlymposSlaveMerchant slaveMerchant;
        public OlymposEsyaBilgiPenceresi bilgi;
        [Tooltip("Alt bardaki \"Commands\" dugmesi (ya da deneme dugmesi): komut menusunu acar/kapatir.")]
        public Button commandsDugmesi;

        [Header("Oyuncu")]
        public string oyuncuAdi = "xMegaTon";
        public long para = 523455;
        [Tooltip("Envanter, yuva sirasiyla (7 x 4 = 28). Bos yuva: null/bos kayit.")]
        public List<OlymposTicariEsya> envanter = new List<OlymposTicariEsya>();

        [Header("Olaylar")]
        [Tooltip("Information paneline yazilacak satir (\"Slave Expire Time : ...\", \"Merchant Items Received\").")]
        public OlymposMetinOlayi onBilgi = new OlymposMetinOlayi();
        public OlymposMetinOlayi onWhisper = new OlymposMetinOlayi();

        public bool TezgahAcik { get; private set; }

        void Awake()
        {
            // Inspector'dan girilen bos kayitlar (id'siz) bos yuva sayilir
            for (int i = 0; i < envanter.Count; i++)
                if (envanter[i] != null && string.IsNullOrEmpty(envanter[i].id) && envanter[i].ikon == null) envanter[i] = null;

            if (commandsDugmesi != null && komutMenusu != null) commandsDugmesi.onClick.AddListener(komutMenusu.AcKapat);
            if (komutMenusu != null)
            {
                komutMenusu.onOpenMerchant.AddListener(MerchantOlustur);
                komutMenusu.onSlaveMerchant.AddListener(SlaveAc);
                komutMenusu.gameObject.SetActive(false);
            }
            if (olustur != null)
            {
                olustur.onTezgahAcildi.AddListener(TezgahAcildi);
                olustur.gameObject.SetActive(false);
                if (olustur.fiyatDiyalogu != null) olustur.fiyatDiyalogu.gameObject.SetActive(false);
                if (olustur.adetDiyalogu != null) olustur.adetDiyalogu.gameObject.SetActive(false);
            }
            if (tezgahCubugu != null)
            {
                tezgahCubugu.onOpen.AddListener(TezgahiGoster);
                tezgahCubugu.onWhisper.AddListener(delegate { onWhisper.Invoke(oyuncuAdi); });
                tezgahCubugu.gameObject.SetActive(false);
            }
            if (merchantPenceresi != null)
            {
                merchantPenceresi.onOdendi.AddListener(delegate (long p) { para -= p; });
                if (merchantPenceresi.satinAlmaOnayi != null) merchantPenceresi.satinAlmaOnayi.gameObject.SetActive(false);
                merchantPenceresi.gameObject.SetActive(false);
            }
            if (slaveMerchant != null)
            {
                slaveMerchant.onBilgi.AddListener(delegate (string s) { onBilgi.Invoke(s); });
                slaveMerchant.onSlaveKapatildi.AddListener(TezgahiKapat);
                slaveMerchant.onParaAlindi.AddListener(delegate (long p) { para += p; });
                slaveMerchant.gameObject.SetActive(false);
            }
            if (bilgi != null) bilgi.gameObject.SetActive(false);
        }

        /// <summary>OPEN MERCHANT: tezgah zaten aciksa bir sey yapmaz (varsayim).</summary>
        public void MerchantOlustur()
        {
            if (olustur == null || TezgahAcik) return;
            while (envanter.Count < OlymposMerchantOlustur.EnvanterYuvasi) envanter.Add(null);
            olustur.Ac(envanter);
        }

        void TezgahAcildi()
        {
            TezgahAcik = true;
            if (tezgahCubugu != null) tezgahCubugu.Goster(olustur.tezgah);
            if (slaveMerchant != null) slaveMerchant.Baslat(olustur.tezgah);
        }

        void TezgahiGoster()
        {
            if (merchantPenceresi != null && olustur != null)
                merchantPenceresi.Ac(oyuncuAdi, olustur.tezgah, envanter, para);
        }

        public void SlaveAc() { if (slaveMerchant != null && TezgahAcik) slaveMerchant.Ac(); }

        /// <summary>Tezgahi kapatir: satilmayan esyalar envantere doner, cubuk gizlenir.</summary>
        public void TezgahiKapat()
        {
            if (!TezgahAcik) return;
            TezgahAcik = false;
            if (merchantPenceresi != null) merchantPenceresi.Kapat();
            if (olustur != null) olustur.HepsiniGeriAl();
            if (tezgahCubugu != null) tezgahCubugu.Gizle();
            if (slaveMerchant != null) slaveMerchant.Sifirla();
        }
    }
}
