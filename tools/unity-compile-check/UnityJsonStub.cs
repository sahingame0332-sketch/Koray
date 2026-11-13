// =============================================================================
//  JsonUtility + Resources SAPLAMASI -- yalnizca dogrulama icin
// =============================================================================
//  Unity'nin JsonUtility'sinin calisan bir taklidi. Amaci: skills.json'un
//  GERCEKTEN SkillData siniflarina yuklendigini Unity acmadan dogrulamak.
//  Alan adi uyusmazligi, tip uyusmazligi ve eksik alan bu sayede yakalanir --
//  bu deliverable'in en buyuk riski tam olarak buydu.
//
//  Unity'nin gercek JsonUtility'si gibi davranir:
//    - yalnizca public instance ALANLARINI doldurur (property'leri degil)
//    - eksik alanlari varsayilan birakir
//    - fazla alanlari sessizce yok sayar
//  Oyunun derlemesine dahil edilmez.
// =============================================================================

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Reflection;
using System.Text;

namespace UnityEngine
{
    public class TextAsset : Object
    {
        public string text { get; set; }
        public TextAsset() { }
        public TextAsset(string content) { text = content; }
    }

    public class Sprite : Object { }
    public class AudioClip : Object { }

    public static class Resources
    {
        /// <summary>Test icin elle doldurulur: yol -> varlik.</summary>
        public static readonly Dictionary<string, Object> Registry =
            new Dictionary<string, Object>();

        public static T Load<T>(string path) where T : Object
        {
            Object o;
            return Registry.TryGetValue(path, out o) ? o as T : null;
        }
    }

    public static class JsonUtility
    {
        public static T FromJson<T>(string json) where T : new()
        {
            object parsed = MiniJson.Parse(json);
            if (!(parsed is Dictionary<string, object>))
                return default(T);

            T result = new T();
            Bind((Dictionary<string, object>)parsed, result);
            return result;
        }

        public static string ToJson(object obj, bool pretty = false)
        {
            // Dogrulama icin gerekmiyor; cagrilirsa bos nesne doner.
            return "{}";
        }

        // ------------------------------------------------------------------
        //  Yansima ile baglama
        // ------------------------------------------------------------------

        private static void Bind(Dictionary<string, object> src, object target)
        {
            Type t = target.GetType();
            foreach (KeyValuePair<string, object> kv in src)
            {
                FieldInfo f = t.GetField(kv.Key,
                    BindingFlags.Instance | BindingFlags.Public);
                if (f == null)
                    continue;          // gercek JsonUtility de fazla alani yok sayar

                object value = Convert(kv.Value, f.FieldType);
                if (value != null)
                    f.SetValue(target, value);
            }
        }

        private static object Convert(object raw, Type type)
        {
            if (raw == null)
                return null;

            if (type == typeof(string))
                return raw as string ?? raw.ToString();

            if (type == typeof(int))
                return (int)System.Convert.ToDouble(raw, CultureInfo.InvariantCulture);

            if (type == typeof(long))
                return (long)System.Convert.ToDouble(raw, CultureInfo.InvariantCulture);

            if (type == typeof(float))
                return (float)System.Convert.ToDouble(raw, CultureInfo.InvariantCulture);

            if (type == typeof(double))
                return System.Convert.ToDouble(raw, CultureInfo.InvariantCulture);

            if (type == typeof(bool))
                return raw is bool ? (bool)raw : System.Convert.ToBoolean(raw);

            if (type.IsArray)
            {
                List<object> list = raw as List<object>;
                if (list == null)
                    return null;

                Type elem = type.GetElementType();
                Array arr = Array.CreateInstance(elem, list.Count);
                for (int i = 0; i < list.Count; i++)
                    arr.SetValue(Convert(list[i], elem), i);
                return arr;
            }

            if (type.IsClass)
            {
                Dictionary<string, object> dict = raw as Dictionary<string, object>;
                if (dict == null)
                    return null;

                object inst = Activator.CreateInstance(type);
                Bind(dict, inst);
                return inst;
            }

            return null;
        }
    }

    /// <summary>Kucuk, bagimsiz JSON ayristirici (yalnizca saplama icin).</summary>
    internal static class MiniJson
    {
        public static object Parse(string json)
        {
            if (string.IsNullOrEmpty(json))
                return null;

            int i = 0;
            object value = ParseValue(json, ref i);
            return value;
        }

        private static void SkipWhitespace(string s, ref int i)
        {
            while (i < s.Length && char.IsWhiteSpace(s[i]))
                i++;
        }

        private static object ParseValue(string s, ref int i)
        {
            SkipWhitespace(s, ref i);
            if (i >= s.Length)
                return null;

            char c = s[i];
            switch (c)
            {
                case '{': return ParseObject(s, ref i);
                case '[': return ParseArray(s, ref i);
                case '"': return ParseString(s, ref i);
                case 't': i += 4; return true;
                case 'f': i += 5; return false;
                case 'n': i += 4; return null;
                default:  return ParseNumber(s, ref i);
            }
        }

        private static Dictionary<string, object> ParseObject(string s, ref int i)
        {
            var dict = new Dictionary<string, object>();
            i++;                                     // '{'
            while (true)
            {
                SkipWhitespace(s, ref i);
                if (i >= s.Length)
                    break;
                if (s[i] == '}') { i++; break; }
                if (s[i] == ',') { i++; continue; }

                string key = ParseString(s, ref i);
                SkipWhitespace(s, ref i);
                if (i < s.Length && s[i] == ':')
                    i++;
                dict[key] = ParseValue(s, ref i);
            }
            return dict;
        }

        private static List<object> ParseArray(string s, ref int i)
        {
            var list = new List<object>();
            i++;                                     // '['
            while (true)
            {
                SkipWhitespace(s, ref i);
                if (i >= s.Length)
                    break;
                if (s[i] == ']') { i++; break; }
                if (s[i] == ',') { i++; continue; }
                list.Add(ParseValue(s, ref i));
            }
            return list;
        }

        private static string ParseString(string s, ref int i)
        {
            SkipWhitespace(s, ref i);
            if (i >= s.Length || s[i] != '"')
                return string.Empty;

            i++;                                     // opening quote
            var sb = new StringBuilder();
            while (i < s.Length && s[i] != '"')
            {
                if (s[i] == '\\' && i + 1 < s.Length)
                {
                    i++;
                    switch (s[i])
                    {
                        case 'n':  sb.Append('\n'); break;
                        case 't':  sb.Append('\t'); break;
                        case 'r':  sb.Append('\r'); break;
                        case 'b':  sb.Append('\b'); break;
                        case 'f':  sb.Append('\f'); break;
                        case '/':  sb.Append('/');  break;
                        case '\\': sb.Append('\\'); break;
                        case '"':  sb.Append('"');  break;
                        case 'u':
                            if (i + 4 < s.Length)
                            {
                                string hex = s.Substring(i + 1, 4);
                                sb.Append((char)System.Convert.ToInt32(hex, 16));
                                i += 4;
                            }
                            break;
                        default: sb.Append(s[i]); break;
                    }
                }
                else
                {
                    sb.Append(s[i]);
                }
                i++;
            }
            i++;                                     // closing quote
            return sb.ToString();
        }

        private static object ParseNumber(string s, ref int i)
        {
            int start = i;
            while (i < s.Length && (char.IsDigit(s[i]) || s[i] == '-' || s[i] == '+'
                                    || s[i] == '.' || s[i] == 'e' || s[i] == 'E'))
                i++;

            string text = s.Substring(start, i - start);
            double d;
            if (double.TryParse(text, NumberStyles.Float,
                                CultureInfo.InvariantCulture, out d))
                return d;
            return 0d;
        }
    }
}

namespace UnityEditor
{
    [AttributeUsage(AttributeTargets.Method)]
    public class MenuItem : Attribute
    {
        public MenuItem(string itemName) { }
        public MenuItem(string itemName, bool isValidateFunction) { }
        public MenuItem(string itemName, bool isValidateFunction, int priority) { }
    }

    public static class AssetDatabase
    {
        public static T LoadAssetAtPath<T>(string path) where T : UnityEngine.Object
        {
            return null;
        }
        public static void CreateAsset(UnityEngine.Object asset, string path) { }
        public static void SaveAssets() { }
        public static void Refresh() { }
        public static void StartAssetEditing() { }
        public static void StopAssetEditing() { }
    }

    public static class EditorApplication
    {
        public static bool isPlaying { get { return false; } }
    }

    public static class Selection
    {
        public static UnityEngine.Transform activeTransform { get { return null; } }
        public static UnityEngine.GameObject activeGameObject { get; set; }
    }

    public static class Undo
    {
        public static void RegisterCreatedObjectUndo(UnityEngine.Object obj, string name) { }
    }

    public static class PrefabUtility
    {
        public static UnityEngine.GameObject SaveAsPrefabAsset(UnityEngine.GameObject go, string path) { return go; }
    }

    public static class EditorUtility
    {
        public static bool DisplayDialog(string title, string message, string ok)
        {
            return true;
        }
        public static void DisplayProgressBar(string title, string info, float progress) { }
        public static void ClearProgressBar() { }
        public static void SetDirty(UnityEngine.Object target) { }
    }
}
