// =============================================================================
//  UnityEngine SAPLAMASI -- yalnizca derleme kontrolu icin
// =============================================================================
//  Bu dosya Unity'nin KENDISI DEGIL. unity/Assets/Scripts altindaki kodun
//  sozdizimi ve tip hatasi icermedigini Unity kurmadan dogrulamak icin
//  yazilmis minimal bir saplamadir.
//
//  Oyunun derlemesine ASLA dahil edilmez -- Unity projesinin disinda,
//  tools/ altinda durur.
//
//  Kullanim:  bash tools/unity-compile-check/check.sh
// =============================================================================

using System;
using System.Collections;
using System.Collections.Generic;

namespace UnityEngine
{
    public class Object
    {
        public string name { get; set; }
        public HideFlags hideFlags { get; set; }
        public static void Destroy(Object obj) { }
        public static void DestroyImmediate(Object obj) { }
        public override string ToString() { return name ?? base.ToString(); }
    }

    public class Component : Object
    {
        public Transform transform { get { return null; } }
        public GameObject gameObject { get { return null; } }
    }

    public class Behaviour : Component
    {
        public bool enabled { get; set; }
    }

    public class Coroutine { }

    public class MonoBehaviour : Behaviour
    {
        public Coroutine StartCoroutine(IEnumerator routine) { return new Coroutine(); }
        public void StopCoroutine(IEnumerator routine) { }
        public void StopAllCoroutines() { }
        public T GetComponent<T>() where T : class { return null; }
    }

    public class ScriptableObject : Object
    {
        public static T CreateInstance<T>() where T : ScriptableObject, new()
        {
            return new T();
        }
    }

    public class WaitForSecondsRealtime : IEnumerator
    {
        public WaitForSecondsRealtime(float seconds) { }
        public object Current { get { return null; } }
        public bool MoveNext() { return false; }
        public void Reset() { }
    }

    public static class Mathf
    {
        public static float Clamp01(float v) { return v < 0f ? 0f : (v > 1f ? 1f : v); }
        public static float Pow(float a, float b) { return (float)Math.Pow(a, b); }
        public static float Lerp(float a, float b, float t) { return a + (b - a) * Clamp01(t); }
        public static int   Min(int a, int b) { return Math.Min(a, b); }
        public static int   Max(int a, int b) { return Math.Max(a, b); }
        public static float Min(float a, float b) { return Math.Min(a, b); }
        public static float Max(float a, float b) { return Math.Max(a, b); }
        public const float PI = 3.14159265f;
        public static float Sqrt(float v) { return (float)Math.Sqrt(v); }
        public static float Sin(float v) { return (float)Math.Sin(v); }
        public static float Cos(float v) { return (float)Math.Cos(v); }
    }

    public static class Time
    {
        // Testin zamani surmesi icin yazilabilir. Gercek Unity'de salt okunur.
        public static float unscaledDeltaTime = 0.016f;
        public static float deltaTime = 0.016f;
        public static float time = 0f;
        public static float timeScale = 1f;
    }

    public static class Debug
    {
        public static void Log(object message) { }
        public static void LogWarning(object message) { }
        public static void LogWarning(object message, Object context) { }
        public static void LogError(object message) { }
    }

    public static class Random
    {
        public static float value { get { return 0.5f; } }
        public static float Range(float min, float max) { return (min + max) * 0.5f; }
    }

    // --- Attribute'lar ---
    [AttributeUsage(AttributeTargets.Field)]
    public class SerializeField : Attribute { }

    [AttributeUsage(AttributeTargets.Field)]
    public class HeaderAttribute : Attribute { public HeaderAttribute(string header) { } }

    [AttributeUsage(AttributeTargets.Field)]
    public class TooltipAttribute : Attribute { public TooltipAttribute(string tooltip) { } }

    [AttributeUsage(AttributeTargets.Field)]
    public class MinAttribute : Attribute { public MinAttribute(float min) { } }

    [AttributeUsage(AttributeTargets.Field)]
    public class RangeAttribute : Attribute { public RangeAttribute(float min, float max) { } }

    [AttributeUsage(AttributeTargets.Class)]
    public class AddComponentMenu : Attribute { public AddComponentMenu(string menu) { } }

    [AttributeUsage(AttributeTargets.Class)]
    public class CreateAssetMenuAttribute : Attribute
    {
        public string fileName { get; set; }
        public string menuName { get; set; }
        public int order { get; set; }
    }
}

namespace UnityEngine.Events
{
    public delegate void UnityAction();
    public delegate void UnityAction<T>(T arg);

    public class UnityEvent
    {
        private readonly List<UnityAction> _calls = new List<UnityAction>();
        public void AddListener(UnityAction call) { _calls.Add(call); }
        public void RemoveListener(UnityAction call) { _calls.Remove(call); }
        public void Invoke() { foreach (UnityAction c in _calls) c(); }
    }
}

namespace UnityEngine.EventSystems
{
    public class PointerEventData
    {
        public int pointerId { get; set; }
    }

    public interface IPointerDownHandler  { void OnPointerDown(PointerEventData eventData); }
    public interface IPointerUpHandler    { void OnPointerUp(PointerEventData eventData); }
    public interface IPointerClickHandler { void OnPointerClick(PointerEventData eventData); }
    public interface IPointerEnterHandler { void OnPointerEnter(PointerEventData eventData); }
    public interface IPointerExitHandler  { void OnPointerExit(PointerEventData eventData); }
}

namespace UnityEngine.UI
{
    public class Graphic : Behaviour { }

    public class Text : Graphic
    {
        public string text { get; set; }
    }

    public class Selectable : Behaviour
    {
        public bool interactable { get; set; }
    }

    public class Button : Selectable
    {
        public UnityEngine.Events.UnityEvent onClick = new UnityEngine.Events.UnityEvent();
    }
}
