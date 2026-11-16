// OLYMPOS-KO · 1298 mob hasar rengi — kurucu (sadece Editor). Menu: OLYMPOS > 1298 > Mob Hasar Rengi (Kırmızı) Oluştur
using System.IO;
using Olympos.MobHasar;
using UnityEditor;
using UnityEngine;

namespace Olympos.MobHasar.EditorTools
{
    public static class OlymposMobHasarBuilder
    {
        const string Klasor = "OlymposMobHasar1298";

        [MenuItem("OLYMPOS/1298/Mob Hasar Rengi (Kırmızı) Oluştur")]
        public static void Build()
        {
            string root = FindRoot();
            var sh = Shader.Find("Olympos/Mob Hasar Kirmizi");
            if (sh == null) { Debug.LogError("[OLYMPOS] Shader bulunamadı: Olympos/Mob Hasar Kirmizi"); return; }
            string md = root + "/Materials";
            if (!AssetDatabase.IsValidFolder(md)) AssetDatabase.CreateFolder(root, "Materials");
            string p = md + "/MobHasarKirmizi.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (mat == null) { mat = new Material(sh); AssetDatabase.CreateAsset(mat, p); }

            var kok = new GameObject("OlymposMobHasarRengi");
            var h = kok.AddComponent<OlymposMobHasarRengi>(); h.kirmiziMalzeme = mat;
            var hd = new GameObject("Hedef (deneme: mobu buraya koyun)"); hd.transform.SetParent(kok.transform, false);
            h.hedefDeneme = hd.transform; h.denemeDongusu = true;
            string pd = root + "/Prefabs";
            if (!AssetDatabase.IsValidFolder(pd)) AssetDatabase.CreateFolder(root, "Prefabs");
            PrefabUtility.SaveAsPrefabAssetAndConnect(kok, pd + "/OlymposMobHasarRengi.prefab", InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(kok, "Mob hasar rengi");
            Selection.activeGameObject = kok; AssetDatabase.SaveAssets();
            Debug.Log("[OLYMPOS] Mob hasar rengi oluşturuldu.");
        }

        static string FindRoot()
        {
            var g = AssetDatabase.FindAssets("OlymposMobHasarBuilder t:MonoScript");
            if (g.Length > 0) return Path.GetDirectoryName(Path.GetDirectoryName(AssetDatabase.GUIDToAssetPath(g[0]).Replace('\\', '/')).Replace('\\', '/')).Replace('\\', '/');
            return "Assets/" + Klasor;
        }
    }
}
