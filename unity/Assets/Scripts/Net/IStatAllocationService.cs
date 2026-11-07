using System;
using System.Collections.Generic;
using Koray.Model;

namespace Koray.Net
{
    /// <summary>Sunucunun stat dagitim istegine verdigi yanit.</summary>
    public struct StatAllocationResult
    {
        public bool Success;
        public string ErrorMessage;

        /// <summary>Sunucunun onayladigi NIHAI stat degerleri (yetkili kaynak).</summary>
        public Dictionary<StatKind, int> ConfirmedStats;

        /// <summary>Islemden sonra kalan dagitilmamis puan (yetkili kaynak).</summary>
        public int ConfirmedUnspentPoints;

        public static StatAllocationResult Fail(string message)
        {
            return new StatAllocationResult
            {
                Success = false,
                ErrorMessage = message,
                ConfirmedStats = null,
                ConfirmedUnspentPoints = 0,
            };
        }
    }

    /// <summary>
    /// Stat dagitimini sunucuya gonderen katman.
    ///
    /// NEDEN TEK SEFERDE TOPLU GONDERILIR
    ///   Oyuncu "+" butonunu basili tuttugunda ~66 tick olusur (297 puan icin).
    ///   Her tick icin paket gondermek saniyede 20 paket demektir ve 1000
    ///   oyuncuda sunucuyu bosa yere dover. Bunun yerine istemci degisiklikleri
    ///   YEREL olarak biriktirir, oyuncu "Onayla"ya bastiginda TEK istek gider.
    ///
    /// NEDEN ISTEMCI YETKILI DEGIL
    ///   Istemci "gucum artik 500" diyemez. "Guce +120 vermek istiyorum" der;
    ///   sunucu puanin gercekten var oldugunu dogrular ve NIHAI degerleri
    ///   geri gonderir. Istemci yalnizca o degerleri gosterir.
    ///   (Mimari gerekcesi: docs/01-mykomobile-altyapi-analizi.md Bolum 6.2)
    /// </summary>
    public interface IStatAllocationService
    {
        /// <param name="deltas">Stat basina EKLENECEK puan (artis, nihai deger degil).</param>
        /// <param name="onComplete">Sunucu yanitiyla cagrilir.</param>
        void Allocate(IReadOnlyDictionary<StatKind, int> deltas,
                      Action<StatAllocationResult> onComplete);
    }
}
