using System;
using System.Collections.Generic;
using Koray.Model;
using Koray.Net;
using UnityEngine;
using UnityEngine.UI;

namespace Koray.UI
{
    /// <summary>
    /// Stat dagitim paneli: 5 stat, "+"/"-" butonlari, onayla / sifirla.
    ///
    /// CALISMA MODELI -- "beklemede" (pending) mantigi
    ///   Oyuncunun bastigi her puan ANINDA sunucuya gitmez. Yerel bir
    ///   "beklemede" tablosunda toplanir ve ekranda onizleme olarak gosterilir.
    ///   Oyuncu "Onayla"ya bastiginda TEK istek gider.
    ///
    ///   Bunun uc faydasi var:
    ///     1. 297 puan icin 66 paket yerine 1 paket gider
    ///     2. Oyuncu yanlis dagittiysa "Sifirla" ile geri alabilir
    ///     3. Sunucu reddederse istemci tutarsiz kalmaz -- beklemede olan
    ///        atilir, sunucunun verdigi degerler gosterilir
    ///
    /// SUNUCU YETKILIDIR
    ///   Onaylanan degerler yalnizca sunucu yanitindan gelir. Istemci kendi
    ///   hesabini asla dogru kabul etmez.
    /// </summary>
    [AddComponentMenu("Koray/UI/Stat Allocation Panel")]
    public class StatAllocationPanel : MonoBehaviour
    {
        /// <summary>Bir stat satirinin sahne referanslari.</summary>
        [Serializable]
        public class StatRow
        {
            public StatKind Stat;

            [Tooltip("Puan ekleyen buton (basili tutmayi destekler)")]
            public HoldRepeatButton PlusButton;

            [Tooltip("Beklemede olan puani geri alan buton (basili tutmayi destekler)")]
            public HoldRepeatButton MinusButton;

            [Tooltip("Stat adi etiketi (bos birakilabilir)")]
            public Text NameLabel;

            [Tooltip("Deger etiketi. TextMeshPro kullanacaksan tipi TMP_Text yap.")]
            public Text ValueLabel;

            [Tooltip("Beklemede olan artisi gosteren etiket, orn. \"+12\" (bos birakilabilir)")]
            public Text PendingLabel;
        }

        [Header("Satirlar")]
        [SerializeField] private StatRow[] _rows = new StatRow[0];

        [Header("Genel arayuz")]
        [SerializeField] private Text _unspentLabel;
        [SerializeField] private Button _commitButton;
        [SerializeField] private Button _resetButton;
        [SerializeField] private Text _errorLabel;

        [Header("Kurallar")]
        [Tooltip("Tek bir statin alabilecegi en yuksek deger. Veritabaninda " +
                 "integer oldugu icin teknik sinir yok; bu bir TASARIM sinirı.")]
        [SerializeField, Min(1)] private int _maxStatValue = 999;

        /// <summary>Sunucunun onayladigi stat degerleri (yetkili).</summary>
        private readonly Dictionary<StatKind, int> _confirmed = new Dictionary<StatKind, int>();

        /// <summary>Henuz gonderilmemis artislar.</summary>
        private readonly Dictionary<StatKind, int> _pending = new Dictionary<StatKind, int>();

        private int _confirmedUnspent;
        private bool _requestInFlight;
        private IStatAllocationService _service;

        /// <summary>Beklemede olan toplam puan.</summary>
        public int PendingTotal
        {
            get
            {
                int sum = 0;
                foreach (KeyValuePair<StatKind, int> kv in _pending)
                    sum += kv.Value;
                return sum;
            }
        }

        /// <summary>Daha dagitilabilecek puan.</summary>
        public int RemainingPoints
        {
            get { return Mathf.Max(0, _confirmedUnspent - PendingTotal); }
        }

        // ------------------------------------------------------------------
        //  Kurulum
        // ------------------------------------------------------------------

        /// <summary>
        /// Paneli baslatir. Karakter paneli acilirken cagir.
        /// </summary>
        public void Initialize(IStatAllocationService service,
                               IReadOnlyDictionary<StatKind, int> stats,
                               int unspentPoints)
        {
            _service = service;
            _confirmed.Clear();

            if (stats != null)
            {
                foreach (KeyValuePair<StatKind, int> kv in stats)
                    _confirmed[kv.Key] = kv.Value;
            }

            _confirmedUnspent = Mathf.Max(0, unspentPoints);
            _pending.Clear();
            _requestInFlight = false;

            SetError(null);
            Refresh();
        }

        private void Awake()
        {
            // Butonlari bagla. Her satir kendi kapasitesini bildirir, boylece
            // puan bittiginde tekrar kendiliginden durur.
            for (int i = 0; i < _rows.Length; i++)
            {
                StatRow row = _rows[i];
                if (row == null)
                    continue;

                StatKind stat = row.Stat;

                if (row.NameLabel != null)
                    row.NameLabel.text = stat.ToDisplayName();

                if (row.PlusButton != null)
                {
                    row.PlusButton.RemainingCapacity = () => GetAddCapacity(stat);
                    row.PlusButton.Repeated += step => AddPending(stat, step);
                }

                if (row.MinusButton != null)
                {
                    row.MinusButton.RemainingCapacity = () => GetPending(stat);
                    row.MinusButton.Repeated += step => RemovePending(stat, step);
                }
            }

            if (_commitButton != null)
                _commitButton.onClick.AddListener(Commit);

            if (_resetButton != null)
                _resetButton.onClick.AddListener(ResetPending);
        }

        // ------------------------------------------------------------------
        //  Beklemede olan dagitim
        // ------------------------------------------------------------------

        public int GetPending(StatKind stat)
        {
            int v;
            return _pending.TryGetValue(stat, out v) ? v : 0;
        }

        public int GetConfirmed(StatKind stat)
        {
            int v;
            return _confirmed.TryGetValue(stat, out v) ? v : 0;
        }

        /// <summary>Ekranda gosterilen deger: onaylanan + beklemede olan.</summary>
        public int GetDisplayValue(StatKind stat)
        {
            return GetConfirmed(stat) + GetPending(stat);
        }

        /// <summary>
        /// Bu stata daha kac puan eklenebilir?
        /// Iki sinirin kucugu: kalan puan ve stat tavani.
        /// </summary>
        public int GetAddCapacity(StatKind stat)
        {
            if (_requestInFlight)
                return 0;

            int byPoints = RemainingPoints;
            int byCap = Mathf.Max(0, _maxStatValue - GetDisplayValue(stat));
            return Mathf.Min(byPoints, byCap);
        }

        public void AddPending(StatKind stat, int amount)
        {
            if (amount <= 0 || _requestInFlight)
                return;

            int capacity = GetAddCapacity(stat);
            if (capacity <= 0)
                return;

            _pending[stat] = GetPending(stat) + Mathf.Min(amount, capacity);
            SetError(null);
            Refresh();
        }

        public void RemovePending(StatKind stat, int amount)
        {
            if (amount <= 0 || _requestInFlight)
                return;

            int current = GetPending(stat);
            if (current <= 0)
                return;

            int next = current - Mathf.Min(amount, current);
            if (next <= 0)
                _pending.Remove(stat);
            else
                _pending[stat] = next;

            SetError(null);
            Refresh();
        }

        public void ResetPending()
        {
            if (_requestInFlight || _pending.Count == 0)
                return;

            _pending.Clear();
            SetError(null);
            Refresh();
        }

        // ------------------------------------------------------------------
        //  Sunucuya gonderme
        // ------------------------------------------------------------------

        public void Commit()
        {
            if (_requestInFlight || _pending.Count == 0)
                return;

            if (_service == null)
            {
                SetError("Dağıtım servisi bağlı değil");
                return;
            }

            // Istek ucarken butonlari kilitle: cift gonderimi onler.
            _requestInFlight = true;
            Refresh();

            // Gonderilen tabloyu kopyala -- yanit gelene kadar _pending
            // degisebilir (teorik olarak), kopya ile calis.
            Dictionary<StatKind, int> payload = new Dictionary<StatKind, int>(_pending);

            _service.Allocate(payload, result =>
            {
                _requestInFlight = false;

                if (!result.Success)
                {
                    // Sunucu reddetti: beklemede olani KORU, oyuncu tekrar
                    // denesin veya sifirlasin. Bilgi kaybi olmaz.
                    SetError(string.IsNullOrEmpty(result.ErrorMessage)
                        ? "Dağıtım başarısız"
                        : result.ErrorMessage);
                    Refresh();
                    return;
                }

                // Basarili: YETKILI kaynak sunucunun yanitidir. Yerel hesabi
                // kullanma -- sunucu farkli bir sonuca varmis olabilir.
                _pending.Clear();

                if (result.ConfirmedStats != null)
                {
                    _confirmed.Clear();
                    foreach (KeyValuePair<StatKind, int> kv in result.ConfirmedStats)
                        _confirmed[kv.Key] = kv.Value;
                }

                _confirmedUnspent = Mathf.Max(0, result.ConfirmedUnspentPoints);
                SetError(null);
                Refresh();
            });
        }

        // ------------------------------------------------------------------
        //  Arayuz yenileme
        // ------------------------------------------------------------------

        private void Refresh()
        {
            for (int i = 0; i < _rows.Length; i++)
            {
                StatRow row = _rows[i];
                if (row == null)
                    continue;

                int pending = GetPending(row.Stat);

                if (row.ValueLabel != null)
                    row.ValueLabel.text = GetDisplayValue(row.Stat).ToString();

                if (row.PendingLabel != null)
                {
                    row.PendingLabel.text = pending > 0 ? "+" + pending : string.Empty;
                    row.PendingLabel.enabled = pending > 0;
                }

                if (row.PlusButton != null)
                    row.PlusButton.Interactable = GetAddCapacity(row.Stat) > 0;

                if (row.MinusButton != null)
                    row.MinusButton.Interactable = !_requestInFlight && pending > 0;
            }

            if (_unspentLabel != null)
                _unspentLabel.text = RemainingPoints.ToString();

            if (_commitButton != null)
                _commitButton.interactable = !_requestInFlight && _pending.Count > 0;

            if (_resetButton != null)
                _resetButton.interactable = !_requestInFlight && _pending.Count > 0;
        }

        private void SetError(string message)
        {
            if (_errorLabel == null)
                return;

            _errorLabel.text = message ?? string.Empty;
            _errorLabel.enabled = !string.IsNullOrEmpty(message);
        }
    }
}
