using System;
using UnityEngine;

namespace Koray.UI
{
    /// <summary>
    /// Basili-tutma tekrarlama egrisinin ayarlari.
    ///
    /// Buradaki varsayilanlar tahmin degil: tools/analyze_hold_repeat.py
    /// betigiyle simule edilip hedeflere gore ayarlandi. Olculen sonuclar:
    ///
    ///     puan   sure
    ///        1   0.00 sn  (tek dokunus, aninda)
    ///        3   0.47 sn
    ///       15   1.35 sn
    ///       30   1.72 sn
    ///       60   2.32 sn
    ///      150   3.22 sn
    ///      297   4.02 sn  (seviye 1->100 hic dagitilmamis, en kotu durum)
    ///
    /// Bu sayilar yalnizca Python'da hesaplanmakla kalmadi: bu dosyadaki
    /// GERCEK kod derlenip calistirilarak dogrulandi (3 ms icinde ayni) ve
    /// 30/60/120/240 FPS'te ayni sonucu verdigi olculdu.
    ///     bash tools/unity-compile-check/check.sh --run
    ///
    /// Hassasiyet: 340 ms basili tutma hala 1 puan ekler, yani kazara
    /// tekrar baslamaz (insan dokunusu ~100-150 ms).
    ///
    /// BU DEGERLERI DEGISTIRIRSEN analyze_hold_repeat.py icindeki
    /// sabitleri de ayni yap ve betigi yeniden calistir -- aksi halde
    /// analiz ile oyun birbirinden kopar.
    /// </summary>
    [CreateAssetMenu(fileName = "StatRepeatTuning",
                     menuName = "Koray/UI/Stat Repeat Tuning")]
    public class StatRepeatTuning : ScriptableObject
    {
        /// <summary>Basili tutma suresi esigi -> o esikten sonraki adim boyu.</summary>
        [Serializable]
        public struct StepThreshold
        {
            [Tooltip("Basili tutma suresi (saniye)")]
            public float HoldSeconds;

            [Tooltip("Bu esikten sonra her tick'te eklenecek puan")]
            [Min(1)] public int Step;
        }

        [Header("Tekrarin baslamasi")]
        [Tooltip("Parmak degdikten sonra tekrarin baslamasi icin gecmesi gereken sure. " +
                 "Insan dokunusu ~100-150 ms oldugu icin 0.30'un altina inme.")]
        [Min(0.05f)] public float InitialDelay = 0.35f;

        [Header("Tick hizi (tick/saniye)")]
        [Tooltip("Tekrar basladigi andaki hiz")]
        [Min(1f)] public float TickRateStart = 8f;

        [Tooltip("Ulasilabilecek en yuksek hiz. 25'in ustune cikmak anlamsiz: " +
                 "60 Hz ekranda kare basina birden fazla tick dusmeye baslar, " +
                 "bunun yerine adim boyunu buyut.")]
        [Min(1f)] public float TickRateMax = 20f;

        [Tooltip("Baslangic hizindan en yuksek hiza ulasma suresi")]
        [Min(0.01f)] public float RateRampTime = 1.20f;

        [Tooltip("Hizlanma egrisi. 1 = dogrusal, >1 = basta daha yavas (daha kontrollu)")]
        [Min(0.1f)] public float RateRampExponent = 1.60f;

        [Header("Adim boyu")]
        [Tooltip("Sureye gore adim buyumesi. HoldSeconds'a gore artan sirada olmali.")]
        public StepThreshold[] StepThresholds =
        {
            new StepThreshold { HoldSeconds = 0.00f, Step = 1  },
            new StepThreshold { HoldSeconds = 1.20f, Step = 2  },
            new StepThreshold { HoldSeconds = 2.20f, Step = 5  },
            new StepThreshold { HoldSeconds = 3.40f, Step = 10 },
            // 5.00 sn esigi mevcut sayilarla ULASILMIYOR (en kotu durum 4.07 sn'de
            // bitiyor). Ileride azami seviye veya seviye basina puan artarsa
            // devreye girecek diye bilincli olarak birakildi.
            new StepThreshold { HoldSeconds = 5.00f, Step = 25 },
        };

        /// <summary>
        /// Verilen basili tutma suresindeki tick hizi (tick/saniye).
        /// analyze_hold_repeat.py icindeki tick_rate() ile ayni formul.
        /// </summary>
        public float GetTickRate(float holdTime)
        {
            float t = holdTime - InitialDelay;
            if (t <= 0f)
                return TickRateStart;

            float f = Mathf.Pow(Mathf.Clamp01(t / RateRampTime), RateRampExponent);
            return Mathf.Lerp(TickRateStart, TickRateMax, f);
        }

        /// <summary>Iki tick arasindaki sure (saniye).</summary>
        public float GetTickInterval(float holdTime)
        {
            return 1f / Mathf.Max(0.0001f, GetTickRate(holdTime));
        }

        /// <summary>
        /// Verilen basili tutma suresindeki adim boyu.
        /// analyze_hold_repeat.py icindeki step_size() ile ayni mantik.
        /// </summary>
        public int GetStepSize(float holdTime)
        {
            int step = 1;
            if (StepThresholds == null)
                return step;

            for (int i = 0; i < StepThresholds.Length; i++)
            {
                if (holdTime >= StepThresholds[i].HoldSeconds)
                    step = Mathf.Max(1, StepThresholds[i].Step);
            }
            return step;
        }

#if UNITY_EDITOR
        private void OnValidate()
        {
            // Esikler artan sirada olmali, yoksa GetStepSize yanlis sonuc verir.
            if (StepThresholds == null || StepThresholds.Length < 2)
                return;

            for (int i = 1; i < StepThresholds.Length; i++)
            {
                if (StepThresholds[i].HoldSeconds < StepThresholds[i - 1].HoldSeconds)
                {
                    Debug.LogWarning(
                        $"[{name}] StepThresholds artan sirada degil (index {i}). " +
                        "Siralamayi duzelt, aksi halde adim boyu beklenmedik davranir.",
                        this);
                    break;
                }
            }

            if (TickRateMax < TickRateStart)
            {
                Debug.LogWarning($"[{name}] TickRateMax, TickRateStart'tan kucuk.", this);
            }
        }
#endif
    }
}
