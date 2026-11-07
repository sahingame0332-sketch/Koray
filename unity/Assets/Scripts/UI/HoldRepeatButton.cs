using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace Koray.UI
{
    /// <summary>
    /// Basili tutuldukca hizlanarak tekrar eden buton.
    ///
    /// Stat dagitim panelindeki "+" / "-" butonlari icin yazildi ama genel
    /// amaclidir: envanterde yigin bolme, magazada adet secme gibi her yerde
    /// kullanilabilir.
    ///
    /// DAVRANIS
    ///   - Parmak degdigi an 1 adim uygulanir  -> tek dokunus daima hassas
    ///   - InitialDelay boyunca tekrar YOK     -> kazara tekrar baslamaz
    ///   - Sonra hizlanarak tekrar eder        -> 297 puan ~4.07 sn'de dagilir
    ///
    /// NEDEN Update(), coroutine DEGIL
    ///   Coroutine + WaitForSeconds kare hizina kilitlenir ve 30 FPS'te
    ///   tekrar hizi yariya duser. Update icinde biriktirici kullanmak
    ///   kare hizindan bagimsiz sonuc verir.
    ///
    /// NEDEN unscaledDeltaTime
    ///   Panel acikken oyun duraklatilmis olabilir (Time.timeScale = 0).
    ///   Olceklenmis zamanla buton hic tekrar etmez.
    /// </summary>
    [AddComponentMenu("Koray/UI/Hold Repeat Button")]
    public class HoldRepeatButton : MonoBehaviour,
        IPointerDownHandler, IPointerUpHandler, IPointerExitHandler
    {
        [Tooltip("Tekrarlama egrisi. Bos birakilirsa varsayilan egri kullanilir.")]
        [SerializeField] private StatRepeatTuning _tuning;

        [Tooltip("Kapaliysa buton hic tepki vermez (orn. puan kalmadiginda).")]
        [SerializeField] private bool _interactable = true;

        [Tooltip("Tek bir karede uygulanabilecek en fazla tick. Kare atlamalarinda " +
                 "kilitlenmeyi onler.")]
        [SerializeField, Min(1)] private int _maxTicksPerFrame = 8;

        /// <summary>
        /// Her tick'te cagrilir; parametre uygulanacak adim boyu (daima >= 1).
        /// Panel bu degeri alip statlari gunceller.
        /// </summary>
        public event Action<int> Repeated;

        /// <summary>
        /// Basma baslangicinda ve bitiminde cagrilir (true = basildi).
        /// Gorsel durum (basili gorunum, titresim) icin.
        /// </summary>
        public event Action<bool> PressedChanged;

        /// <summary>
        /// Daha kac adim uygulanabilir? Panel baglar.
        ///
        /// 0 veya daha kucuk donerse tekrar DURUR -- yani puan bittiginde
        /// buton bosa calismaz. Baglanmazsa sinir yok sayilir.
        /// </summary>
        public Func<int> RemainingCapacity;

        private bool _held;
        private int _pointerId = int.MinValue;   // cok dokunuslu ekran guvenligi
        private float _holdTime;
        private float _nextTickTime;

        private static StatRepeatTuning _fallbackTuning;

        public bool Interactable
        {
            get { return _interactable; }
            set
            {
                _interactable = value;
                if (!value) Cancel();
            }
        }

        /// <summary>Tuning atanmamissa varsayilan degerlerle bir tane uretir.</summary>
        private StatRepeatTuning Tuning
        {
            get
            {
                if (_tuning != null)
                    return _tuning;

                if (_fallbackTuning == null)
                {
                    _fallbackTuning = ScriptableObject.CreateInstance<StatRepeatTuning>();
                    _fallbackTuning.name = "StatRepeatTuning (varsayilan)";
                }
                return _fallbackTuning;
            }
        }

        public void OnPointerDown(PointerEventData eventData)
        {
            if (!_interactable || _held)
                return;

            int capacity = GetCapacity();
            if (capacity <= 0)
                return;

            _held = true;
            _pointerId = eventData != null ? eventData.pointerId : 0;
            _holdTime = 0f;
            _nextTickTime = Tuning.InitialDelay;

            PressedChanged?.Invoke(true);

            // Dokunus aninda ilk adim: tek dokunus her zaman tam 1 birim.
            Emit(1);
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            // Basmayi baslatan parmak kalkmadikca birakma sayilmaz.
            if (eventData != null && eventData.pointerId != _pointerId)
                return;

            Cancel();
        }

        public void OnPointerExit(PointerEventData eventData)
        {
            // Parmak butonun disina kayarsa tekrar durur -- yoksa oyuncu
            // parmagini kaydirip puanlari farkinda olmadan harcar.
            if (eventData != null && eventData.pointerId != _pointerId)
                return;

            Cancel();
        }

        private void OnDisable()
        {
            // Panel kapanirsa veya nesne devre disi kalirsa tekrar birakilmali,
            // aksi halde tekrar acildiginda basili sayilir.
            Cancel();
        }

        private void Update()
        {
            if (!_held)
                return;

            _holdTime += Time.unscaledDeltaTime;

            if (_holdTime < _nextTickTime)
                return;

            int ticks = 0;
            while (_holdTime >= _nextTickTime && ticks < _maxTicksPerFrame)
            {
                int capacity = GetCapacity();
                if (capacity <= 0)
                {
                    Cancel();
                    return;
                }

                // Adim ve hiz, tick'in PLANLANAN anina gore hesaplanir --
                // gerceklesen anina gore degil. Fark kritik: bir kare 16.7 ms
                // surerken tick araligi 50 ms ise, tick her zaman biraz GECIKIR.
                // Gecikmeyi bir sonraki planlamaya tasirsan sapma birikir ve
                // 297 puanlik dagitim 60 FPS'te ~0.5 sn, 30 FPS'te ~1 sn uzar.
                // Ideal zamana gore planlayinca sonuc kare hizindan bagimsiz olur.
                int step = Mathf.Min(Tuning.GetStepSize(_nextTickTime), capacity);
                Emit(step);

                _nextTickTime += Tuning.GetTickInterval(_nextTickTime);
                ticks++;
            }
        }

        private void Cancel()
        {
            if (!_held)
                return;

            _held = false;
            _pointerId = int.MinValue;
            _holdTime = 0f;
            PressedChanged?.Invoke(false);
        }

        private int GetCapacity()
        {
            return RemainingCapacity != null ? RemainingCapacity() : int.MaxValue;
        }

        private void Emit(int step)
        {
            if (step <= 0)
                return;

            Repeated?.Invoke(step);
        }
    }
}
