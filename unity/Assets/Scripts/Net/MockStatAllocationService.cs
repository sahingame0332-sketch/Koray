using System;
using System.Collections;
using System.Collections.Generic;
using Koray.Model;
using UnityEngine;

namespace Koray.Net
{
    /// <summary>
    /// Sunucu yerine gecen test servisi.
    ///
    /// Sunucu henuz yazilmadan arayuzu calistirip test etmek icin. Gercek ag
    /// gecikmesini taklit eder ve istege bagli olarak hata dondurebilir --
    /// boylece "istek basarisiz olursa arayuz ne yapiyor" yolunu da test
    /// edebilirsin. Cogu hata bu yolda bulunur.
    ///
    /// Gercek sunucu hazir oldugunda bu bileseni sahneden cikarip
    /// IStatAllocationService'i uygulayan gercek istemciyi tak.
    /// </summary>
    [AddComponentMenu("Koray/Net/Mock Stat Allocation Service")]
    public class MockStatAllocationService : MonoBehaviour, IStatAllocationService
    {
        [Header("Taklit edilen ag davranisi")]
        [Tooltip("Yanitin donmesi icin beklenecek sure (saniye)")]
        [Min(0f)] public float SimulatedLatency = 0.25f;

        [Tooltip("Isteklerin yuzde kaci basarisiz olsun? Hata yolunu test etmek icin.")]
        [Range(0f, 1f)] public float FailureRate = 0f;

        [Header("Taklit edilen sunucu durumu")]
        public int UnspentPoints = 297;

        [SerializeField] private int _strength  = 10;
        [SerializeField] private int _stamina   = 10;
        [SerializeField] private int _dexterity = 10;
        [SerializeField] private int _intellect = 10;
        [SerializeField] private int _charisma  = 10;

        public void Allocate(IReadOnlyDictionary<StatKind, int> deltas,
                             Action<StatAllocationResult> onComplete)
        {
            StartCoroutine(AllocateRoutine(deltas, onComplete));
        }

        private IEnumerator AllocateRoutine(IReadOnlyDictionary<StatKind, int> deltas,
                                            Action<StatAllocationResult> onComplete)
        {
            if (SimulatedLatency > 0f)
                yield return new WaitForSecondsRealtime(SimulatedLatency);

            if (onComplete == null)
                yield break;

            if (FailureRate > 0f && UnityEngine.Random.value < FailureRate)
            {
                onComplete(StatAllocationResult.Fail("Taklit edilen ag hatasi"));
                yield break;
            }

            // --- Sunucunun yapmasi gereken dogrulamalar ---
            int total = 0;
            if (deltas != null)
            {
                foreach (KeyValuePair<StatKind, int> kv in deltas)
                {
                    if (kv.Value < 0)
                    {
                        onComplete(StatAllocationResult.Fail("Negatif dagitim reddedildi"));
                        yield break;
                    }
                    total += kv.Value;
                }
            }

            if (total > UnspentPoints)
            {
                onComplete(StatAllocationResult.Fail(
                    $"Yetersiz puan: {total} istendi, {UnspentPoints} var"));
                yield break;
            }

            // --- Uygula ---
            if (deltas != null)
            {
                foreach (KeyValuePair<StatKind, int> kv in deltas)
                    Apply(kv.Key, kv.Value);
            }
            UnspentPoints -= total;

            onComplete(new StatAllocationResult
            {
                Success = true,
                ErrorMessage = null,
                ConfirmedStats = Snapshot(),
                ConfirmedUnspentPoints = UnspentPoints,
            });
        }

        private void Apply(StatKind stat, int amount)
        {
            switch (stat)
            {
                case StatKind.Strength:  _strength  += amount; break;
                case StatKind.Stamina:   _stamina   += amount; break;
                case StatKind.Dexterity: _dexterity += amount; break;
                case StatKind.Intellect: _intellect += amount; break;
                case StatKind.Charisma:  _charisma  += amount; break;
            }
        }

        public Dictionary<StatKind, int> Snapshot()
        {
            return new Dictionary<StatKind, int>
            {
                { StatKind.Strength,  _strength  },
                { StatKind.Stamina,   _stamina   },
                { StatKind.Dexterity, _dexterity },
                { StatKind.Intellect, _intellect },
                { StatKind.Charisma,  _charisma  },
            };
        }
    }
}
