#if UNITY_EDITOR
using Koray.Props;
using UnityEditor;
using UnityEngine;

namespace Koray.EditorTools
{
    /// <summary>GameObject > Koray > Yukseltme Sunagi: sahneye bir sunak ekler.</summary>
    public static class UpgradeAltarMenu
    {
        [MenuItem("GameObject/Koray/Yükseltme Sunağı", false, 10)]
        public static void Create()
        {
            GameObject go = new GameObject("UpgradeAltar");
            go.AddComponent<UpgradeAltar>();
            Undo.RegisterCreatedObjectUndo(go, "Yükseltme Sunağı ekle");
            Selection.activeGameObject = go;
        }
    }
}
#endif
