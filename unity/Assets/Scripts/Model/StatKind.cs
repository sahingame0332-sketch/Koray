namespace Koray.Model
{
    /// <summary>
    /// Karakterin ana statlari. Degerler veritabanindaki game_character
    /// kolonlariyla birebir eslesir (stat_strength, stat_stamina, ...).
    ///
    /// Sayisal degerler ag protokolunde kullanilir, bu yuzden ASLA
    /// degistirilmemeli; yeni stat eklenecekse sona eklenir.
    /// </summary>
    public enum StatKind
    {
        Strength  = 0,   // stat_strength  -- Guc
        Stamina   = 1,   // stat_stamina   -- Dayaniklilik
        Dexterity = 2,   // stat_dexterity -- Ceviklik
        Intellect = 3,   // stat_intellect -- Zeka
        Charisma  = 4,   // stat_charisma  -- Karizma
    }

    public static class StatKindExtensions
    {
        /// <summary>Veritabani kolon adi.</summary>
        public static string ToColumnName(this StatKind stat)
        {
            switch (stat)
            {
                case StatKind.Strength:  return "stat_strength";
                case StatKind.Stamina:   return "stat_stamina";
                case StatKind.Dexterity: return "stat_dexterity";
                case StatKind.Intellect: return "stat_intellect";
                case StatKind.Charisma:  return "stat_charisma";
                default:                 return "unknown";
            }
        }

        /// <summary>Arayuzde gosterilecek Turkce ad.</summary>
        public static string ToDisplayName(this StatKind stat)
        {
            switch (stat)
            {
                case StatKind.Strength:  return "Güç";
                case StatKind.Stamina:   return "Dayanıklılık";
                case StatKind.Dexterity: return "Çeviklik";
                case StatKind.Intellect: return "Zekâ";
                case StatKind.Charisma:  return "Karizma";
                default:                 return stat.ToString();
            }
        }
    }
}
