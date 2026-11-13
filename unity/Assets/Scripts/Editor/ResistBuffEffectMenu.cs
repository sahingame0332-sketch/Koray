#if UNITY_EDITOR
using System.IO;
using Koray.VFX;
using UnityEditor;
using UnityEngine;

namespace Koray.EditorTools
{
    /// <summary>
    /// Resist efekti icin editor kisayollari.
    ///
    ///   Tools > Koray > VFX > Resist Efektini Dene
    ///       Play modunda secili objenin (yoksa orijinin) ustunde efekti oynatir.
    ///
    ///   Tools > Koray > VFX > Resist Efekti Prefab'larini Uret
    ///       Assets/GameData/VFX altina her element icin bir prefab yazar.
    ///       Prefab yalnizca ResistBuffEffect bilesenini tasir; gorsel parcalar
    ///       oyun sirasinda kodla kurulur. SkillDefinition.CastVfx alanina
    ///       surukleyip Instantiate etmen yeterli.
    /// </summary>
    public static class ResistBuffEffectMenu
    {
        private const string OutputDir = "Assets/GameData/VFX";

        [MenuItem("Tools/Koray/VFX/Resist Efektini Dene")]
        public static void Preview()
        {
            if (!EditorApplication.isPlaying)
            {
                EditorUtility.DisplayDialog("Play modu gerekli",
                    "Efekt oyun sırasında kurulur. Önce Play'e bas, sonra bu menüyü tekrar seç.", "Tamam");
                return;
            }
            Transform t = Selection.activeTransform;
            if (t != null) ResistBuffEffect.Play(t, ResistElement.Fire);
            else ResistBuffEffect.PlayAt(Vector3.zero, ResistElement.Fire);
        }

        [MenuItem("Tools/Koray/VFX/Resist Efekti Prefab'larını Üret")]
        public static void GeneratePrefabs()
        {
            Directory.CreateDirectory(OutputDir);
            ResistElement[] elements =
            {
                ResistElement.Fire, ResistElement.Ice, ResistElement.Lightning, ResistElement.Poison
            };
            foreach (ResistElement e in elements)
            {
                GameObject go = new GameObject("ResistBuff_" + e);
                ResistBuffEffect fx = go.AddComponent<ResistBuffEffect>();
                fx.element = e;
                PrefabUtility.SaveAsPrefabAsset(go, OutputDir + "/ResistBuff_" + e + ".prefab");
                Object.DestroyImmediate(go);
            }
            AssetDatabase.Refresh();
            EditorUtility.DisplayDialog("Prefab'lar üretildi",
                elements.Length + " prefab yazıldı:\n" + OutputDir, "Tamam");
        }
    }
}
#endif
