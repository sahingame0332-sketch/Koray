// Derleme doğrulaması için minimal Unity API taslakları.
// Yalnızca OLYMPOS betiklerinin kullandığı üyeler var; davranış taklit edilmez.
using System;

namespace UnityEngine
{
    public struct Vector2 {
        public float x, y;
        public Vector2(float x, float y) { this.x = x; this.y = y; }
        public static Vector2 zero { get { return new Vector2(0, 0); } }
    }
    public struct Vector3 { public float x, y, z; }
    public struct Vector4 {
        public float x, y, z, w;
        public Vector4(float x, float y, float z, float w) { this.x = x; this.y = y; this.z = z; this.w = w; }
        public static Vector4 zero { get { return new Vector4(0, 0, 0, 0); } }
    }
    public struct Color {
        public float r, g, b, a;
        public Color(float r, float g, float b) { this.r = r; this.g = g; this.b = b; this.a = 1f; }
        public Color(float r, float g, float b, float a) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static Color black { get { return new Color(0, 0, 0, 1); } }
        public static Color white { get { return new Color(1, 1, 1, 1); } }
    }
    public struct Color32 {
        public byte r, g, b, a;
        public Color32(byte r, byte g, byte b, byte a) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static implicit operator Color(Color32 c) { return new Color(c.r/255f, c.g/255f, c.b/255f, c.a/255f); }
        public static implicit operator Color32(Color c) { return new Color32((byte)(c.r*255), (byte)(c.g*255), (byte)(c.b*255), (byte)(c.a*255)); }
    }
    public static class ColorUtility {
        public static bool TryParseHtmlString(string s, out Color c) { c = Color.black; return true; }
    }

    public class Object {
        public string name;
        public static void DestroyImmediate(Object o) { }
        public static T FindObjectOfType<T>() where T : Object { return null; }
        public static bool operator ==(Object a, Object b) { return ReferenceEquals(a, b); }
        public static bool operator !=(Object a, Object b) { return !ReferenceEquals(a, b); }
        public override bool Equals(object o) { return base.Equals(o); }
        public override int GetHashCode() { return base.GetHashCode(); }
    }

    public class Component : Object {
        public GameObject gameObject { get { return null; } }
        public Transform transform { get { return null; } }
        public T GetComponent<T>() where T : Component { return null; }
    }
    public class Behaviour : Component { public bool enabled; }
    public class MonoBehaviour : Behaviour { }

    public class Transform : Component {
        public void SetParent(Transform p, bool worldPositionStays) { }
    }
    public class RectTransform : Transform {
        public Vector2 anchorMin, anchorMax, pivot, sizeDelta, anchoredPosition;
    }

    public class GameObject : Object {
        public GameObject(string name, params Type[] components) { this.name = name; }
        public GameObject(string name) { this.name = name; }
        public T AddComponent<T>() where T : Component, new() { return new T(); }
        public T GetComponent<T>() where T : Component { return null; }
        public void SetActive(bool v) { }
        public bool activeSelf { get { return true; } }
        public bool activeInHierarchy { get { return true; } }
        public Transform transform { get { return null; } }
    }

    public class Font : Object { }
    public class RectOffset {
        public int left, right, top, bottom;
        public RectOffset() { }
        public RectOffset(int l, int r, int t, int b) { left=l; right=r; top=t; bottom=b; }
    }
    public class Sprite : Object { }
    public class Texture : Object { }
    public class Texture2D : Texture { }

    public static class Mathf {
        public static int Clamp(int v, int a, int b) { return v < a ? a : (v > b ? b : v); }
        public static float Clamp(float v, float a, float b) { return v < a ? a : (v > b ? b : v); }
        public static float Clamp01(float v) { return Clamp(v, 0f, 1f); }
        public static int Max(int a, int b) { return a > b ? a : b; }
        public static float Max(float a, float b) { return a > b ? a : b; }
        public static int Min(int a, int b) { return a < b ? a : b; }
        public static int CeilToInt(float f) { return (int)System.Math.Ceiling(f); }
        public static int RoundToInt(float f) { return (int)System.Math.Round(f); }
    }
    public static class Debug {
        public static void Log(object m) { }
        public static void LogWarning(object m) { }
        public static void LogError(object m) { }
    }

    public enum RenderMode { ScreenSpaceOverlay, ScreenSpaceCamera, WorldSpace }
    public class Canvas : Behaviour { public RenderMode renderMode; }
    public class CanvasRenderer : Component { }

    public enum TextAnchor { UpperLeft, UpperCenter, UpperRight, MiddleLeft, MiddleCenter, MiddleRight, LowerLeft, LowerCenter, LowerRight }
    public enum FontStyle { Normal, Bold, Italic, BoldAndItalic }
    public enum FilterMode { Point, Bilinear, Trilinear }
    public enum TextureWrapMode { Repeat, Clamp, Mirror, MirrorOnce }

    [AttributeUsage(AttributeTargets.Field)] public class HeaderAttribute : Attribute { public HeaderAttribute(string h) { } }
    [AttributeUsage(AttributeTargets.All)]  public class TooltipAttribute : Attribute { public TooltipAttribute(string t) { } }
    [AttributeUsage(AttributeTargets.Field)] public class RangeAttribute : Attribute { public RangeAttribute(float min, float max) { } }
    [AttributeUsage(AttributeTargets.Field)] public class TextAreaAttribute : Attribute {
        public TextAreaAttribute() { }
        public TextAreaAttribute(int minLines, int maxLines) { }
    }
    [AttributeUsage(AttributeTargets.Class)] public class DisallowMultipleComponentAttribute : Attribute { }
    [AttributeUsage(AttributeTargets.Class)] public class AddComponentMenuAttribute : Attribute { public AddComponentMenuAttribute(string s) { } }
}

namespace UnityEngine.Events
{
    public class UnityEventBase { }
    public class UnityEvent : UnityEventBase {
        public void AddListener(UnityAction call) { }
        public void Invoke() { }
    }
    public class UnityEvent<T0> : UnityEventBase {
        public void AddListener(UnityAction<T0> call) { }
        public void Invoke(T0 arg0) { }
    }
    public class UnityEvent<T0,T1> : UnityEventBase {
        public void AddListener(UnityAction<T0,T1> call) { }
        public void Invoke(T0 a0, T1 a1) { }
    }
    public delegate void UnityAction();
    public delegate void UnityAction<T0>(T0 arg0);
    public delegate void UnityAction<T0,T1>(T0 a0, T1 a1);
}

namespace UnityEngine.UI
{
    public class Graphic : UnityEngine.Behaviour {
        public UnityEngine.Color color;
        public bool raycastTarget;
        public UnityEngine.RectTransform rectTransform { get { return null; } }
    }
    public class MaskableGraphic : Graphic { }

    public class Image : MaskableGraphic {
        public enum Type { Simple, Sliced, Tiled, Filled }
        public UnityEngine.Sprite sprite;
        public Type type;
    }

    public enum HorizontalWrapMode { Wrap, Overflow }
    public enum VerticalWrapMode { Truncate, Overflow }

    public class Text : MaskableGraphic {
        public UnityEngine.Font font;
        public int fontSize;
        public UnityEngine.FontStyle fontStyle;
        public UnityEngine.TextAnchor alignment;
        public string text;
        public bool supportRichText;
        public HorizontalWrapMode horizontalOverflow;
        public VerticalWrapMode verticalOverflow;
    }

    public struct ColorBlock {
        public UnityEngine.Color normalColor, highlightedColor, pressedColor, selectedColor, disabledColor;
        public float colorMultiplier, fadeDuration;
        public static ColorBlock defaultColorBlock { get { return new ColorBlock(); } }
    }
    public struct Navigation {
        public enum Mode { None, Horizontal, Vertical, Automatic, Explicit }
        public Mode mode;
    }

    public class Selectable : UnityEngine.Behaviour {
        public enum Transition { None, ColorTint, SpriteSwap, Animation }
        public Transition transition;
        public Graphic targetGraphic;
        public ColorBlock colors;
        public Navigation navigation;
        public bool interactable;
    }
    public class ButtonClickedEvent : UnityEngine.Events.UnityEvent { }
    public class Button : Selectable { public ButtonClickedEvent onClick = new ButtonClickedEvent(); }

    public class BaseMeshEffect : UnityEngine.Behaviour { }
    public class Shadow : BaseMeshEffect {
        public UnityEngine.Color effectColor;
        public UnityEngine.Vector2 effectDistance;
    }
    public class Outline : Shadow { }

    public class InputField : Selectable {
        public string text;
        public Text textComponent;
        public Text placeholder;
        public int characterLimit;
        public enum ContentType { Standard, IntegerNumber, DecimalNumber, Alphanumeric, Name, EmailAddress, Password, Pin, Custom }
        public ContentType contentType;
    }
    public class LayoutElement : UnityEngine.Behaviour {
        public float minWidth, minHeight, preferredWidth, preferredHeight, flexibleWidth, flexibleHeight;
        public bool ignoreLayout;
    }
    public class LayoutGroup : UnityEngine.Behaviour {
        public UnityEngine.RectOffset padding;
        public UnityEngine.TextAnchor childAlignment;
    }
    public class HorizontalOrVerticalLayoutGroup : LayoutGroup {
        public float spacing;
        public bool childForceExpandWidth, childForceExpandHeight;
        public bool childControlWidth, childControlHeight;
    }
    public class VerticalLayoutGroup : HorizontalOrVerticalLayoutGroup { }
    public class HorizontalLayoutGroup : HorizontalOrVerticalLayoutGroup { }
    public class ContentSizeFitter : UnityEngine.Behaviour {
        public enum FitMode { Unconstrained, MinSize, PreferredSize }
        public FitMode horizontalFit, verticalFit;
    }
    public class CanvasScaler : UnityEngine.Behaviour {
        public enum ScaleMode { ConstantPixelSize, ScaleWithScreenSize, ConstantPhysicalSize }
        public ScaleMode uiScaleMode;
        public UnityEngine.Vector2 referenceResolution;
        public float matchWidthOrHeight;
    }
    public class GraphicRaycaster : UnityEngine.Behaviour { }
}

namespace UnityEngine.EventSystems
{
    public class EventSystem : UnityEngine.Behaviour { }
    public class BaseInputModule : UnityEngine.Behaviour { }
    public class StandaloneInputModule : BaseInputModule { }
}
