// Derleme doğrulaması için minimal UnityEditor API taslakları.
using System;
using UnityEngine;

namespace UnityEditor
{
    [AttributeUsage(AttributeTargets.Method)]
    public class MenuItemAttribute : Attribute {
        public MenuItemAttribute(string itemName) { }
        public MenuItemAttribute(string itemName, bool isValidateFunction) { }
        public MenuItemAttribute(string itemName, bool isValidateFunction, int priority) { }
    }

    public static class AssetDatabase {
        public static string[] FindAssets(string filter) { return new string[0]; }
        public static string[] FindAssets(string filter, string[] searchInFolders) { return new string[0]; }
        public static string GUIDToAssetPath(string guid) { return ""; }
        public static T LoadAssetAtPath<T>(string path) where T : UnityEngine.Object { return null; }
        public static bool IsValidFolder(string path) { return false; }
        public static string CreateFolder(string parentFolder, string newFolderName) { return ""; }
        public static void Refresh() { }
        public static void SaveAssets() { }
        public static void CreateAsset(UnityEngine.Object asset, string path) { }
    }

    public static class PrefabUtility {
        public static GameObject SaveAsPrefabAsset(GameObject root, string assetPath) { return null; }
        public static UnityEngine.Object InstantiatePrefab(UnityEngine.Object assetComponentOrGameObject) { return null; }
        public static UnityEngine.Object InstantiatePrefab(UnityEngine.Object assetComponentOrGameObject, Transform parent) { return null; }
    }

    public static class EditorUtility { public static void SetDirty(UnityEngine.Object o) { } }

    public static class Undo {
        public static void RegisterCreatedObjectUndo(UnityEngine.Object objectToUndo, string name) { }
    }

    public static class Selection {
        public static GameObject activeGameObject;
        public static UnityEngine.Object activeObject;
    }

    public enum TextureImporterType { Default, NormalMap, GUI, Sprite, Cursor, Cookie, Lightmap, SingleChannel }
    public enum SpriteImportMode { None, Single, Multiple, Polygon }
    public enum TextureImporterCompression { Uncompressed, Compressed, CompressedHQ, CompressedLQ }

    public class AssetImporter : UnityEngine.Object {
        public string assetPath;
        public static AssetImporter GetAtPath(string path) { return null; }
        public void SaveAndReimport() { }
    }

    public class TextureImporter : AssetImporter {
        public TextureImporterType textureType;
        public SpriteImportMode spriteImportMode;
        public float spritePixelsPerUnit;
        public bool mipmapEnabled;
        public bool alphaIsTransparency;
        public UnityEngine.FilterMode filterMode;
        public UnityEngine.TextureWrapMode wrapMode;
        public TextureImporterCompression textureCompression;
        public int maxTextureSize;
        public UnityEngine.Vector4 spriteBorder;
        public bool sRGBTexture;
        public int anisoLevel;
    }
}
