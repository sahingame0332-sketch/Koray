// =============================================================================
//  UnityEngine SAPLAMASI (VFX kismi) -- yalnizca derleme kontrolu icin
// =============================================================================
//  unity/Assets/Scripts/VFX altindaki kodun kullandigi tipler. Govdeler bos:
//  amac yalnizca sozdizimi ve tip kontroludur, goruntu uretmez.
// =============================================================================

using System;

namespace UnityEngine
{
    public enum HideFlags { None = 0, DontSave = 52 }
    public enum TextureWrapMode { Repeat, Clamp }

    public struct Vector2
    {
        public float x, y;
        public Vector2(float x, float y) { this.x = x; this.y = y; }
    }

    public struct Vector3
    {
        public float x, y, z;
        public Vector3(float x, float y, float z) { this.x = x; this.y = y; this.z = z; }
        public static Vector3 zero { get { return new Vector3(0, 0, 0); } }
        public static Vector3 up { get { return new Vector3(0, 1, 0); } }
        public static Vector3 right { get { return new Vector3(1, 0, 0); } }
        public static Vector3 forward { get { return new Vector3(0, 0, 1); } }
        public static Vector3 operator +(Vector3 a, Vector3 b) { return new Vector3(a.x + b.x, a.y + b.y, a.z + b.z); }
        public static Vector3 operator -(Vector3 a, Vector3 b) { return new Vector3(a.x - b.x, a.y - b.y, a.z - b.z); }
        public static Vector3 operator *(Vector3 a, float s) { return new Vector3(a.x * s, a.y * s, a.z * s); }
    }

    public struct Quaternion
    {
        public static Quaternion identity { get { return new Quaternion(); } }
        public static Quaternion AngleAxis(float angle, Vector3 axis) { return new Quaternion(); }
        public static Quaternion operator *(Quaternion a, Quaternion b) { return a; }
    }

    public struct Color
    {
        public float r, g, b, a;
        public Color(float r, float g, float b, float a) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static Color white { get { return new Color(1, 1, 1, 1); } }
    }

    public struct Bounds
    {
        public Bounds(Vector3 center, Vector3 size) { }
    }

    public class GameObject : Object
    {
        public GameObject() { }
        public GameObject(string name) { this.name = name; }
        public Transform transform { get { return null; } }
        public void SetActive(bool value) { }
        public T AddComponent<T>() where T : Component, new() { return new T(); }
    }

    public class Transform : Component
    {
        public Vector3 position { get; set; }
        public Quaternion rotation { get; set; }
        public Vector3 localPosition { get; set; }
        public Quaternion localRotation { get; set; }
        public Vector3 localScale { get; set; }
        public Vector3 right { get { return Vector3.right; } }
        public Vector3 up { get { return Vector3.up; } }
        public void SetParent(Transform parent, bool worldPositionStays) { }
        public Vector3 InverseTransformDirection(Vector3 direction) { return direction; }
    }

    public class Camera : Behaviour
    {
        public static Camera main { get { return null; } }
    }

    public class Texture : Object
    {
        public TextureWrapMode wrapMode { get; set; }
    }

    public class Texture2D : Texture { }

    public class Shader : Object
    {
        public static Shader Find(string name) { return null; }
        public static int PropertyToID(string name) { return 0; }
    }

    public class Material : Object
    {
        public Material(Shader shader) { }
        public Texture mainTexture { get; set; }
        public void SetFloat(string name, float value) { }
    }

    public class MaterialPropertyBlock
    {
        public void SetColor(int nameId, Color value) { }
    }

    public class Mesh : Object
    {
        public Vector3[] vertices { get; set; }
        public Vector2[] uv { get; set; }
        public Color[] colors { get; set; }
        public int[] triangles { get; set; }
        public Bounds bounds { get; set; }
        public void MarkDynamic() { }
        public void RecalculateBounds() { }
    }

    public class MeshFilter : Component
    {
        public Mesh sharedMesh { get; set; }
    }

    public class Renderer : Component
    {
        public bool enabled { get; set; }
        public Material sharedMaterial { get; set; }
        public Rendering.ShadowCastingMode shadowCastingMode { get; set; }
        public bool receiveShadows { get; set; }
        public void SetPropertyBlock(MaterialPropertyBlock properties) { }
    }

    public class MeshRenderer : Renderer { }
}

namespace UnityEngine.Rendering
{
    public enum ShadowCastingMode { Off, On }
}
