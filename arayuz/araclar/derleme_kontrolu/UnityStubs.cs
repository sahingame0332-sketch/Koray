// Derleme doğrulaması için minimal Unity API taslakları.
// Yalnızca OLYMPOS betiklerinin kullandığı üyeler var; davranış taklit edilmez.
using System;

namespace UnityEngine
{
    public struct Vector2 {
        public float x, y;
        public Vector2(float x, float y) { this.x = x; this.y = y; }
        public static Vector2 zero { get { return new Vector2(0, 0); } }
        public static Vector2 one { get { return new Vector2(1, 1); } }
        public static Vector2 operator +(Vector2 a, Vector2 b) { return new Vector2(a.x + b.x, a.y + b.y); }
        public static implicit operator Vector3(Vector2 v) { return new Vector3(v.x, v.y, 0); }
    }
    public struct Vector3 {
        public float x, y, z;
        public Vector3(float x, float y, float z) { this.x = x; this.y = y; this.z = z; }
        public static Vector3 up { get { return new Vector3(0, 1, 0); } }
        public static Vector3 down { get { return new Vector3(0, -1, 0); } }
        public static Vector3 forward { get { return new Vector3(0, 0, 1); } }
        public static Vector3 ProjectOnPlane(Vector3 v, Vector3 n) { return v; }
        public static Vector3 back { get { return new Vector3(0, 0, -1); } }
        public static float Distance(Vector3 a, Vector3 b) { return 0f; }
        public static Vector3 Lerp(Vector3 a, Vector3 b, float t) { return a; }
        public static Vector3 Cross(Vector3 a, Vector3 b) { return a; }
        public static Vector3 operator -(Vector3 a, Vector3 b) { return new Vector3(a.x - b.x, a.y - b.y, a.z - b.z); }
        public float sqrMagnitude { get { return x * x + y * y + z * z; } }
        public Vector3 normalized { get { return this; } }
        public static Vector3 operator -(Vector3 a) { return new Vector3(-a.x, -a.y, -a.z); }
        public static float SignedAngle(Vector3 a, Vector3 b, Vector3 axis) { return 0f; }
        public static Vector3 operator +(Vector3 a, Vector3 b) { return new Vector3(a.x + b.x, a.y + b.y, a.z + b.z); }
        public static Vector3 operator *(Vector3 a, float d) { return new Vector3(a.x * d, a.y * d, a.z * d); }
        public static implicit operator Vector2(Vector3 v) { return new Vector2(v.x, v.y); }
    }
    public class Shader : Object {
        public static Shader Find(string name) { return null; }
        public static int PropertyToID(string name) { return 0; }
    }
    public class Material : Object {
        public Material(Shader s) { } public void SetFloat(string n, float f) { } public Texture mainTexture;
        public Shader shader;
        public bool HasProperty(int id) { return true; }
        public void SetColor(int id, Color c) { }
        public void SetColor(string name, Color c) { }
        public void SetTexture(string name, Texture t) { }
        public void SetVector(string name, Vector4 v) { }
    }
    public enum TouchScreenKeyboardType { Default, ASCIICapable, NumbersAndPunctuation, URL, NumberPad, PhonePad }
    public enum CameraClearFlags { Skybox = 1, SolidColor = 2, Depth = 3, Nothing = 4 }
    public enum FogMode { Linear = 1, Exponential = 2, ExponentialSquared = 3 }
    public enum PrimitiveType { Sphere, Capsule, Cylinder, Cube, Plane, Quad }
    public static class RenderSettings {
        public static bool fog; public static FogMode fogMode; public static Color fogColor;
        public static float fogStartDistance, fogEndDistance; public static Color ambientLight;
    }
    [AttributeUsage(AttributeTargets.Class)] public class ExecuteAlways : Attribute { }
    public struct Quaternion { public float x, y, z, w; public static Quaternion LookRotation(Vector3 f, Vector3 up) { return new Quaternion(); } public static Quaternion identity { get { return new Quaternion(); } } public static Quaternion Euler(float x, float y, float z) { return new Quaternion(); } public static Vector3 operator *(Quaternion q, Vector3 v) { return v; } }
    public struct Rect {
        public float x, y, width, height;
        public float xMin { get { return x; } } public float xMax { get { return x + width; } }
        public float yMin { get { return y; } } public float yMax { get { return y + height; } }
        public Vector2 center { get { return new Vector2(x + width / 2f, y + height / 2f); } }
    }
    public static class Time { public static float time { get { return 0f; } } public static float deltaTime { get { return 0f; } } public static float unscaledTime { get { return 0f; } } public static float unscaledDeltaTime { get { return 0f; } } }
    public static class PlayerPrefs {
        public static string GetString(string key, string defaultValue) { return defaultValue; }
        public static void SetString(string key, string value) { }
        public static void DeleteKey(string key) { }
        public static int GetInt(string key) { return 0; }
        public static void SetInt(string key, int value) { }
        public static bool HasKey(string key) { return false; }
        public static void Save() { }
    }
    public static class JsonUtility {
        public static string ToJson(object obj) { return ""; }
        public static T FromJson<T>(string json) { return default(T); }
    }
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
        public static Color operator *(Color a, float b) { return new Color(a.r * b, a.g * b, a.b * b, a.a * b); }
        public static Color operator *(Color a, Color b) { return new Color(a.r * b.r, a.g * b.g, a.b * b.b, a.a * b.a); }
    }
    public struct Color32 {
        public byte r, g, b, a;
        public Color32(byte r, byte g, byte b, byte a) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static implicit operator Color(Color32 c) { return new Color(c.r/255f, c.g/255f, c.b/255f, c.a/255f); }
        public static implicit operator Color32(Color c) { return new Color32((byte)(c.r*255), (byte)(c.g*255), (byte)(c.b*255), (byte)(c.a*255)); }
    }
    public static class ColorUtility {
        public static bool TryParseHtmlString(string s, out Color c) { c = Color.black; return true; }
        public static string ToHtmlStringRGB(Color c) { return ""; }
    }

    public class Object {
        public string name;
        public static void DestroyImmediate(Object o) { }
        public static void Destroy(Object o) { }
        public static T Instantiate<T>(T original, Transform parent) where T : Object { return original; }
        public static T Instantiate<T>(T original) where T : Object { return original; }
        public static T Instantiate<T>(T original, Vector3 pos, Quaternion rot) where T : Object { return original; }
        public static T FindObjectOfType<T>() where T : Object { return null; }
        public static T[] FindObjectsOfType<T>() where T : Object { return new T[0]; }
        public static bool operator ==(Object a, Object b) { return ReferenceEquals(a, b); }
        public static bool operator !=(Object a, Object b) { return !ReferenceEquals(a, b); }
        public override bool Equals(object o) { return base.Equals(o); }
        public override int GetHashCode() { return base.GetHashCode(); }
    }

    public class Component : Object {
        public GameObject gameObject { get { return null; } }
        public Transform transform { get { return null; } }
        public T GetComponent<T>() where T : Component { return null; }
        public T GetComponentInParent<T>() where T : Component { return null; }
        public T GetComponentInChildren<T>() where T : Component { return null; }
        public T[] GetComponentsInChildren<T>(bool includeInactive) where T : Component { return new T[0]; }
    }
    public class Behaviour : Component { public bool enabled; }
    public class MonoBehaviour : Behaviour { }

    public class Transform : Component {
        public void SetParent(Transform p, bool worldPositionStays) { }
        public Vector3 lossyScale;
        public Vector3 localScale;
        public Vector3 localPosition;
        public Vector3 forward { get { return new Vector3(0,0,1); } }
        public Quaternion rotation;
        public Transform parent { get { return null; } }
        public Vector3 position;
        public void SetAsLastSibling() { }
        public void SetPositionAndRotation(Vector3 p, Quaternion r) { }
        public Vector3 TransformPoint(Vector3 p) { return p; }
        public Vector3 InverseTransformPoint(Vector3 p) { return p; }
    }
    public static class RectTransformUtility {
        public static bool ScreenPointToLocalPointInRectangle(RectTransform rect, Vector2 screenPoint, Camera cam, out Vector2 localPoint) { localPoint = Vector2.zero; return true; }
    }
    public class RectTransform : Transform {
        public Vector2 anchorMin, anchorMax, pivot, sizeDelta, anchoredPosition, offsetMin, offsetMax;
        public Rect rect { get { return new Rect(); } }
    }

    public class GameObject : Object {
        public GameObject(string name, params Type[] components) { this.name = name; }
        public GameObject(string name) { this.name = name; }
        public T AddComponent<T>() where T : Component, new() { return new T(); }
        public static GameObject CreatePrimitive(PrimitiveType t) { return null; }
        public T[] GetComponentsInChildren<T>(bool includeInactive) where T : Component { return new T[0]; }
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

    public static class Mathf { public static bool Approximately(float a, float b) { return a == b; }
        public const float PI = 3.14159265f;
        public static float Cos(float f) { return (float)System.Math.Cos(f); }
        public static float Sin(float f) { return (float)System.Math.Sin(f); }
        public static float Lerp(float a, float b, float t) { return a + (b - a) * t; }
        public static float Abs(float f) { return f < 0 ? -f : f; }
        public static int Clamp(int v, int a, int b) { return v < a ? a : (v > b ? b : v); }
        public static float Clamp(float v, float a, float b) { return v < a ? a : (v > b ? b : v); }
        public static float Clamp01(float v) { return Clamp(v, 0f, 1f); }
        public static int Max(int a, int b) { return a > b ? a : b; }
        public static float Max(float a, float b) { return a > b ? a : b; }
        public static int Min(int a, int b) { return a < b ? a : b; }
        public static int CeilToInt(float f) { return (int)System.Math.Ceiling(f); }
        public static float Ceil(float f) { return (float)System.Math.Ceiling(f); }
        public static float Round(float f) { return (float)System.Math.Round(f); }
        public static float Pow(float a, float b) { return (float)System.Math.Pow(a, b); }
        public static float Log(float a) { return (float)System.Math.Log(a); }
        public static int FloorToInt(float f) { return (int)System.Math.Floor(f); }
        public static float Min(float a, float b) { return a < b ? a : b; }
        public static int RoundToInt(float f) { return (int)System.Math.Round(f); }
    }
    public static class Debug {
        public static void Log(object m) { }
        public static void LogWarning(object m) { }
        public static void LogError(object m) { }
    }

    public enum RenderMode { ScreenSpaceOverlay, ScreenSpaceCamera, WorldSpace }
    public class Camera : Behaviour { public new Transform transform { get { return null; } } public Vector3 WorldToScreenPoint(Vector3 p) { return p; } public static Camera main { get { return null; } } public CameraClearFlags clearFlags; public Color backgroundColor; }
    public class Renderer : Component { public Material sharedMaterial; public Material[] sharedMaterials; public bool enabled; public bool receiveShadows; public UnityEngine.Rendering.ShadowCastingMode shadowCastingMode; public void GetPropertyBlock(MaterialPropertyBlock b) { } public void SetPropertyBlock(MaterialPropertyBlock b) { } }
    public class MeshRenderer : Renderer { }
    public class MeshFilter : Component { public Mesh sharedMesh; }
    public class Mesh : Object { public Vector3[] vertices; public Vector2[] uv; public int[] triangles; public int subMeshCount; public void RecalculateBounds() { } public void RecalculateNormals() { } public void SetVertices(System.Collections.Generic.List<Vector3> v) { } public void SetUVs(int ch, System.Collections.Generic.List<Vector2> u) { } public void SetTriangles(int[] t, int sub) { } }
    public class MaterialPropertyBlock { public void SetTexture(int id, Texture t) { } public void SetColor(int id, Color c) { } public void SetFloat(int id, float f) { } }
    public struct LayerMask { public int value; public static implicit operator int(LayerMask m) { return m.value; } public static implicit operator LayerMask(int v) { return new LayerMask { value = v }; } }
    public enum QueryTriggerInteraction { UseGlobal, Ignore, Collide }
    public struct RaycastHit { public Vector3 point; public Vector3 normal; }
    public static class Physics { public static bool Raycast(Vector3 o, Vector3 d, out RaycastHit h, float m, int mask, QueryTriggerInteraction q) { h = new RaycastHit(); return false; } }
    public static class Application { public static bool isPlaying { get { return false; } } }
    [AttributeUsage(AttributeTargets.Class, AllowMultiple = true)] public class RequireComponent : Attribute { public RequireComponent(Type a) { } public RequireComponent(Type a, Type b) { } }
    public class Canvas : Behaviour { public Camera worldCamera; public RenderMode renderMode; public int sortingOrder; }
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
    [AttributeUsage(AttributeTargets.Field)] public class HideInInspector : Attribute { }
    [AttributeUsage(AttributeTargets.Class)] public class DisallowMultipleComponentAttribute : Attribute { }
    [AttributeUsage(AttributeTargets.Class)] public class AddComponentMenuAttribute : Attribute { public AddComponentMenuAttribute(string s) { } }
}

namespace UnityEngine.Events
{
    public class UnityEventBase { public void RemoveAllListeners() { } }
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
    public class UnityEvent<T0,T1,T2> : UnityEventBase {
        public void AddListener(UnityAction<T0,T1,T2> call) { }
        public void Invoke(T0 a0, T1 a1, T2 a2) { }
    }
    public delegate void UnityAction<T0,T1,T2>(T0 a0, T1 a1, T2 a2);
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
        public UnityEngine.Material material;
        public void SetVerticesDirty() { }
    }
    public class MaskableGraphic : Graphic { }

    public class Image : MaskableGraphic {
        public enum Type { Simple, Sliced, Tiled, Filled }
        public enum FillMethod { Horizontal, Vertical, Radial90, Radial180, Radial360 }
        public UnityEngine.Sprite sprite;
        public bool preserveAspect;
        public Type type;
        public FillMethod fillMethod;
        public int fillOrigin;
        public float fillAmount;
    }
    public class Mask : UnityEngine.Behaviour { public bool showMaskGraphic; }

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
        public float lineSpacing;
        public float preferredWidth { get { return 0f; } }
        public float preferredHeight { get { return 0f; } }
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

    public struct UIVertex { public UnityEngine.Vector3 position; public UnityEngine.Color32 color; }
    public class VertexHelper {
        public int currentVertCount { get { return 0; } }
        public void PopulateUIVertex(ref UIVertex v, int i) { }
        public void SetUIVertex(UIVertex v, int i) { }
    }
    public class BaseMeshEffect : UnityEngine.Behaviour {
        public virtual void ModifyMesh(VertexHelper vh) { }
        public bool IsActive() { return true; }
        protected Graphic graphic { get { return null; } }
    }
    public class Shadow : BaseMeshEffect {
        public UnityEngine.Color effectColor;
        public UnityEngine.Vector2 effectDistance;
    }
    public class Outline : Shadow { }

    public class InputField : Selectable {
        public string text;
        public Text textComponent;
        public Graphic placeholder;
        public int characterLimit;
        public class OnChangeEvent : UnityEngine.Events.UnityEvent<string> { }
        public OnChangeEvent onValueChanged = new OnChangeEvent();
        public int caretPosition;
        public UnityEngine.TouchScreenKeyboardType keyboardType;
        public enum LineType { SingleLine, MultiLineSubmit, MultiLineNewline }
        public LineType lineType;
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
    public class BaseEventData { }
    public class PointerEventData : BaseEventData {
        public UnityEngine.Vector2 position;
        public UnityEngine.GameObject pointerDrag;
        public UnityEngine.Camera pressEventCamera;
    }
    public interface IEventSystemHandler { }
    public interface IPointerClickHandler : IEventSystemHandler { void OnPointerClick(PointerEventData eventData); }
    public interface IBeginDragHandler : IEventSystemHandler { void OnBeginDrag(PointerEventData eventData); }
    public interface IDragHandler : IEventSystemHandler { void OnDrag(PointerEventData eventData); }
    public interface IPointerDownHandler : IEventSystemHandler { void OnPointerDown(PointerEventData eventData); }
    public interface IEndDragHandler : IEventSystemHandler { void OnEndDrag(PointerEventData eventData); }
    public interface IDropHandler : IEventSystemHandler { void OnDrop(PointerEventData eventData); }
    public class BaseInputModule : UnityEngine.Behaviour { }
    public class StandaloneInputModule : BaseInputModule { }
}

namespace UnityEngine.Rendering { public enum ShadowCastingMode { Off, On, TwoSided, ShadowsOnly } }
