// =============================================================================
//  HoldRepeatButton dogrulama kosumu
// =============================================================================
//  unity/Assets/Scripts altindaki GERCEK HoldRepeatButton ve StatRepeatTuning
//  kodunu calistirip, tools/analyze_hold_repeat.py ile AYNI sonucu verdigini
//  dogrular.
//
//  Neden onemli: Unity kodundaki egri ile Python analizindeki egri birbirinden
//  koparsa, analiz yalan soylemeye baslar. Bu kosum ikisini birbirine baglar.
//
//  Kullanim:  bash tools/unity-compile-check/check.sh --run
// =============================================================================

using System;
using System.Reflection;
using Koray.UI;
using UnityEngine;
using UnityEngine.EventSystems;

public static class HoldRepeatHarness
{
    private const float Dt = 1f / 240f;          // ince adim: Python'un 1 ms'ine yakin
    private const float MaxSimSeconds = 40f;

    /// <summary>points kadar puanin tamami kac saniyede dagilir?</summary>
    private static bool Simulate(int points, out float seconds, out int ticks)
    {
        StatRepeatTuning tuning = ScriptableObject.CreateInstance<StatRepeatTuning>();
        HoldRepeatButton button = new HoldRepeatButton();

        // _tuning private alanina yansima ile ata (Unity'de Inspector yapar).
        FieldInfo tuningField = typeof(HoldRepeatButton)
            .GetField("_tuning", BindingFlags.Instance | BindingFlags.NonPublic);
        tuningField.SetValue(button, tuning);

        MethodInfo update = typeof(HoldRepeatButton)
            .GetMethod("Update", BindingFlags.Instance | BindingFlags.NonPublic);

        int remaining = points;
        int tickCount = 0;

        button.RemainingCapacity = () => remaining;
        button.Repeated += step =>
        {
            remaining -= step;
            tickCount++;
        };

        Time.unscaledDeltaTime = Dt;
        button.OnPointerDown(new PointerEventData { pointerId = 0 });

        float t = 0f;
        while (remaining > 0 && t < MaxSimSeconds)
        {
            t += Dt;
            update.Invoke(button, null);
        }

        seconds = t;
        ticks = tickCount;
        return remaining <= 0;
    }

    /// <summary>Belirli bir kare suresiyle simule eder.</summary>
    private static float SimulateAtFps(int points, float dt, out int ticks)
    {
        StatRepeatTuning tuning = ScriptableObject.CreateInstance<StatRepeatTuning>();
        HoldRepeatButton button = new HoldRepeatButton();
        typeof(HoldRepeatButton)
            .GetField("_tuning", BindingFlags.Instance | BindingFlags.NonPublic)
            .SetValue(button, tuning);
        MethodInfo update = typeof(HoldRepeatButton)
            .GetMethod("Update", BindingFlags.Instance | BindingFlags.NonPublic);

        int remaining = points;
        int tickCount = 0;
        button.RemainingCapacity = () => remaining;
        button.Repeated += step => { remaining -= step; tickCount++; };

        Time.unscaledDeltaTime = dt;
        button.OnPointerDown(new PointerEventData { pointerId = 0 });

        float t = 0f;
        while (remaining > 0 && t < MaxSimSeconds)
        {
            t += dt;
            update.Invoke(button, null);
        }

        ticks = tickCount;
        return t;
    }

    public static int Main(string[] args)
    {
        // (puan, Python'un olctugu sure) -- analyze_hold_repeat.py ciktisi
        var cases = new (int Points, float Expected)[]
        {
            (1,   0.00f),
            (3,   0.47f),
            (15,  1.35f),
            (30,  1.72f),
            (60,  2.32f),
            (150, 3.22f),
            (297, 4.02f),
        };

        // Tolerans tek bir simulasyon adimi (4.17 ms) + float/double farki
        // mertebesinde. Tick plani ideal zamana gore yapildigi icin sapma
        // ARTIK BIRIKMIYOR -- tolerans tick sayisiyla buyumuyor.
        const float Tolerance = 0.025f;

        Console.WriteLine("HoldRepeatButton <-> analyze_hold_repeat.py KARSILASTIRMASI");
        Console.WriteLine(new string('=', 66));
        Console.WriteLine();
        Console.WriteLine("  puan     C#      Python     fark   tick   durum");

        bool allOk = true;
        foreach (var c in cases)
        {
            float seconds;
            int ticks;
            bool finished = Simulate(c.Points, out seconds, out ticks);

            float diff = Math.Abs(seconds - c.Expected);
            bool ok = finished && diff <= Tolerance;
            allOk = allOk && ok;

            Console.WriteLine(
                "  {0,4}  {1,6:F2}s  {2,6:F2}s  {3,7:F3}s  {4,5}   {5}",
                c.Points, seconds, c.Expected, diff, ticks, ok ? "ok" : "SORUN");
        }

        Console.WriteLine();

        // Hassasiyet: kisa dokunus tek puan eklemeli
        Console.WriteLine("Hassasiyet (kisa dokunus kac puan ekler?):");
        foreach (float hold in new[] { 0.05f, 0.15f, 0.30f, 0.34f })
        {
            StatRepeatTuning tuning = ScriptableObject.CreateInstance<StatRepeatTuning>();
            HoldRepeatButton button = new HoldRepeatButton();
            typeof(HoldRepeatButton)
                .GetField("_tuning", BindingFlags.Instance | BindingFlags.NonPublic)
                .SetValue(button, tuning);
            MethodInfo update = typeof(HoldRepeatButton)
                .GetMethod("Update", BindingFlags.Instance | BindingFlags.NonPublic);

            int added = 0;
            button.RemainingCapacity = () => 1000;
            button.Repeated += step => added += step;

            Time.unscaledDeltaTime = Dt;
            button.OnPointerDown(new PointerEventData { pointerId = 0 });

            float t = 0f;
            while (t < hold)
            {
                t += Dt;
                update.Invoke(button, null);
            }

            bool ok = added == 1;
            allOk = allOk && ok;
            Console.WriteLine("  {0,4:F0} ms -> {1} puan   {2}",
                hold * 1000f, added, ok ? "ok" : "SORUN");
        }

        Console.WriteLine();

        // Kapasite siniri: puan bitince tekrar durmali
        {
            StatRepeatTuning tuning = ScriptableObject.CreateInstance<StatRepeatTuning>();
            HoldRepeatButton button = new HoldRepeatButton();
            typeof(HoldRepeatButton)
                .GetField("_tuning", BindingFlags.Instance | BindingFlags.NonPublic)
                .SetValue(button, tuning);
            MethodInfo update = typeof(HoldRepeatButton)
                .GetMethod("Update", BindingFlags.Instance | BindingFlags.NonPublic);

            int remaining = 7;
            int over = 0;
            button.RemainingCapacity = () => remaining;
            button.Repeated += step =>
            {
                remaining -= step;
                if (remaining < 0) over = -remaining;
            };

            Time.unscaledDeltaTime = Dt;
            button.OnPointerDown(new PointerEventData { pointerId = 0 });
            for (float t = 0f; t < 10f; t += Dt)
                update.Invoke(button, null);

            bool ok = remaining == 0 && over == 0;
            allOk = allOk && ok;
            Console.WriteLine("Kapasite siniri (7 puan, 10 sn basili tutuldu):");
            Console.WriteLine("  kalan {0}, tasma {1}   {2}", remaining, over, ok ? "ok" : "SORUN");
        }

        Console.WriteLine();

        // KARE HIZI BAGIMSIZLIGI -- asil mesele bu.
        // Tick plani gerceklesen ana gore yapilsaydi 30 FPS'te dagitim
        // belirgin sekilde uzardi. Ideal ana gore planlandigi icin uzamamali.
        Console.WriteLine("Kare hizi bagimsizligi (297 puan):");
        Console.WriteLine("  FPS     sure    kare suresi");
        float minSec = float.MaxValue, maxSec = float.MinValue;
        foreach (int fps in new[] { 30, 60, 120, 240 })
        {
            float savedDt = Dt;
            float seconds = SimulateAtFps(297, 1f / fps, out int ticks);
            minSec = Math.Min(minSec, seconds);
            maxSec = Math.Max(maxSec, seconds);
            Console.WriteLine("  {0,3}   {1,6:F2}s   {2,5:F1} ms", fps, seconds, 1000f / fps);
            GC.KeepAlive(savedDt);
        }
        float spread = maxSec - minSec;
        // Yayilim en buyuk kare suresi (33 ms) mertebesinde olmali; bu,
        // olcumun son kareye yuvarlanmasindan gelir, sapma birikiminden degil.
        bool fpsOk = spread <= 0.05f;
        allOk = allOk && fpsOk;
        Console.WriteLine("  yayilim {0:F3}s   {1}", spread,
            fpsOk ? "ok (sapma birikmiyor)" : "SORUN (sapma birikiyor)");

        Console.WriteLine();
        Console.WriteLine(allOk ? "SONUC: butun kontroller gecti"
                                : "SONUC: KONTROL BASARISIZ");
        return allOk ? 0 : 1;
    }
}
