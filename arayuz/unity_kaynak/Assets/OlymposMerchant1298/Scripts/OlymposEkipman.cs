// OLYMPOS-KO · 1298 Equip / UnEquip
// Envanterdeki kusanilabilir esyaya dokun -> bilgi penceresi (Equip / Close) -> Equip: esya ekipman yuvasina gecer,
// bonuslari eklenir (olculen: Silan Boots ile HP 419 -> 434, MP 1162 -> 1177; "Bonus HP : 15", "Bonus MP : 15").
// Kusanilmis esyaya dokun -> bilgi penceresi (UnEquip / Close) -> UnEquip: esya envantere doner, bonuslar cikar.
// Kendi envanter/ekipman pencerenizdeki yuvalara OlymposTicariYuva ekleyip bu betige baglayin.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    [Serializable] public class OlymposBonusOlayi : UnityEvent<int, int> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Ekipman (Equip - UnEquip)")]
    public class OlymposEkipman : MonoBehaviour
    {
        public OlymposEsyaBilgiPenceresi bilgi;
        [Tooltip("Envanter yuvalari (sirayla).")]
        public OlymposTicariYuva[] envanterYuvalari = new OlymposTicariYuva[0];
        [Tooltip("Ekipman yuvalari.")]
        public OlymposTicariYuva[] ekipmanYuvalari = new OlymposTicariYuva[0];
        [Tooltip("Isaretliyse sinifi uymayan esya kusanilamaz (Equip dugmesi yine gorunur; basilinca islem yapilmaz). Varsayim.")]
        public bool sinifKontrolu = true;

        [Header("Olaylar")]
        public OlymposTicariEsyaOlayi onKusanildi = new OlymposTicariEsyaOlayi();
        public OlymposTicariEsyaOlayi onCikarildi = new OlymposTicariEsyaOlayi();
        [Tooltip("Toplam bonus degisti (toplam HP bonusu, toplam MP bonusu): en yuksek HP/MP'ye ekleyin.")]
        public OlymposBonusOlayi onBonusDegisti = new OlymposBonusOlayi();

        public List<OlymposTicariEsya> envanter = new List<OlymposTicariEsya>();
        public OlymposTicariEsya[] ekipman = new OlymposTicariEsya[0];

        void Awake()
        {
            if (ekipman.Length != ekipmanYuvalari.Length) ekipman = new OlymposTicariEsya[ekipmanYuvalari.Length];
            // Inspector'dan gelen bos kayitlar (kimliksiz, ikonsuz) bos yuva sayilir
            for (int i = 0; i < envanter.Count; i++) if (Bos(envanter[i])) envanter[i] = null;
            for (int i = 0; i < ekipman.Length; i++) if (Bos(ekipman[i])) ekipman[i] = null;
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) { envanterYuvalari[i].sira = i; envanterYuvalari[i].onTiklandi.AddListener(EnvantereDokun); }
            for (int i = 0; i < ekipmanYuvalari.Length; i++)
                if (ekipmanYuvalari[i] != null) { ekipmanYuvalari[i].sira = i; ekipmanYuvalari[i].onTiklandi.AddListener(EkipmanaDokun); }
        }

        static bool Bos(OlymposTicariEsya e) { return e != null && string.IsNullOrEmpty(e.id) && e.ikon == null; }

        void Start() { Ciz(); }

        public void Ciz()
        {
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].Goster(i < envanter.Count ? envanter[i] : null);
            for (int i = 0; i < ekipmanYuvalari.Length; i++)
                if (ekipmanYuvalari[i] != null) ekipmanYuvalari[i].Goster(ekipman[i]);
        }

        void EnvantereDokun(int i)
        {
            if (bilgi == null || i >= envanter.Count || envanter[i] == null) return;
            var e = envanter[i];
            bilgi.Goster(e, null, 0, bilgi.beyaz, e.kusanilir ? OlymposBilgiDugmesi.Equip : OlymposBilgiDugmesi.Yok,
                         (RectTransform)envanterYuvalari[i].transform, KusanIc);
        }

        void EkipmanaDokun(int i)
        {
            if (bilgi == null || i >= ekipman.Length || ekipman[i] == null) return;
            bilgi.Goster(ekipman[i], null, 0, bilgi.beyaz, OlymposBilgiDugmesi.UnEquip, (RectTransform)ekipmanYuvalari[i].transform, Cikar);
        }

        public void Kusan(OlymposTicariEsya e) { KusanIc(e); }

        void KusanIc(OlymposTicariEsya e)
        {
            if (e == null || !e.kusanilir) return;
            if (sinifKontrolu && !e.sinifUygun) return;
            int yer = -1;
            for (int i = 0; i < ekipman.Length && yer < 0; i++) if (ekipman[i] == null) yer = i;
            if (yer < 0) return;                                   // bos ekipman yuvasi yok
            int ei = envanter.IndexOf(e);
            if (ei < 0) return;
            envanter[ei] = null; ekipman[yer] = e;
            Ciz();
            onKusanildi.Invoke(e);
            BonusBildir();
        }

        public void Cikar(OlymposTicariEsya e)
        {
            if (e == null) return;
            int yer = Array.IndexOf(ekipman, e);
            if (yer < 0) return;
            ekipman[yer] = null;
            bool kondu = false;
            for (int i = 0; i < envanter.Count && !kondu; i++) if (envanter[i] == null) { envanter[i] = e; kondu = true; }
            if (!kondu) envanter.Add(e);
            Ciz();
            onCikarildi.Invoke(e);
            BonusBildir();
        }

        void BonusBildir()
        {
            int hp = 0, mp = 0;
            for (int i = 0; i < ekipman.Length; i++) if (ekipman[i] != null) { hp += ekipman[i].bonusHp; mp += ekipman[i].bonusMp; }
            onBonusDegisti.Invoke(hp, mp);
        }
    }
}
