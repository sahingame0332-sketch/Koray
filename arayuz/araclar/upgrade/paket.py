"""Dort Upgrade penceresi icin Unity kaynaklarini uretir (unity_kaynak/Assets/Olympos<Ad>1298/) — sprite, fontlar, referans,
calisma zamani sinifi, harf araligi efekti, Editor kurucu. Calisma klasoru: pencere2.py / secim.py ciktilari + jpg'ler."""
import json, os, shutil
from PIL import Image
A='/home/user/Koray/arayuz/unity_kaynak/Assets'; FD='/home/user/Koray/arayuz/kaynak/char_info/fonts/'
SX,SY=2266,1488; S=1220/1488
DUG={'item':{'upgrade':[117,558,188,64],'cancel':[345,558,190,64],'preview':[571,557,190,64],'x':(776,51)},
     'aksesuar':{'upgrade':[111,560,188,63],'cancel':[339,560,192,63],'preview':[565,558,190,65],'x':(768,47)},
     'hizli':{'upgrade':[245,566,190,65],'cancel':[476,566,192,65],'x':(808,57)}}
YAZ={'item':dict(need=(1329.5,597),rate=(1876,597),para=(1860,852.5)),
     'aksesuar':dict(need=(1328.5,623.5),rate=(1884.5,623.5),para=(1862,854)),
     'hizli':dict(need=(1609,656.5),para=(1860,863))}
BUYUK={'item':[(1266,398,1390,517),(1813,396,1938,517)],
       'aksesuar':[(1256,304,1384,428),(1256,433,1384,557),(1823,371,1950,496)],'hizli':[]}
PAK={'item':('ItemUpgrade','ITEM UPGRADE','Item Upgrade Penceresi'),'aksesuar':('AccessoryUpgrade','ACCESSORY UPGRADE','Accessory Upgrade Penceresi'),
     'hizli':('FastUpgrade','FAST UPGRADE +1 +2 +3 +4 +5','Fast Upgrade Penceresi'),'secim':('SelectUpgrade','Select Upgrade','Select Upgrade Menüsü')}
REF={'item':['item.jpg','item2.jpg'],'aksesuar':['aksesuar.jpg'],'hizli':['hizli.jpg'],'secim':['secim.jpg']}
def cs_harf(P): return f'''// OLYMPOS-KO · legacy UI.Text icin harf araligi ({P} paketi). Tek satirli yazilar: her harf sira * aralik kaydirilir.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{{
    [AddComponentMenu("OLYMPOS/1298/{P}/Harf Araligi")]
    [RequireComponent(typeof(Text))]
    public class Olympos{P}HarfAraligi : BaseMeshEffect
    {{
        public float aralik = 1f;
        void OnValidate() {{ var g = GetComponent<Text>(); if (g != null) g.SetVerticesDirty(); }}
        public override void ModifyMesh(VertexHelper vh)
        {{
            if (!IsActive() || aralik == 0f) return;
            var t = GetComponent<Text>(); if (t == null || string.IsNullOrEmpty(t.text)) return;
            string s = t.text; int dortgen = vh.currentVertCount / 4; bool boslukDahil = dortgen >= s.Length;
            float toplam = aralik * (s.Length - 1), hiza = 0f; var a = t.alignment;
            if (a == TextAnchor.UpperCenter || a == TextAnchor.MiddleCenter || a == TextAnchor.LowerCenter) hiza = -toplam * 0.5f;
            else if (a == TextAnchor.UpperRight || a == TextAnchor.MiddleRight || a == TextAnchor.LowerRight) hiza = -toplam;
            var v = new UIVertex(); int q = 0;
            for (int i = 0; i < s.Length && q < dortgen; i++)
            {{
                if (!boslukDahil && char.IsWhiteSpace(s[i])) continue;
                float dx = hiza + aralik * i;
                for (int k = 0; k < 4; k++) {{ int idx = q * 4 + k; vh.PopulateUIVertex(ref v, idx); v.position = new Vector3(v.position.x + dx, v.position.y, v.position.z); vh.SetUIVertex(v, idx); }}
                q++;
            }}
        }}
    }}
}}
'''
def cs_pencere(P,baslik,rate,preview):
    return f'''// OLYMPOS-KO · 1298 {baslik} penceresi — TEK BASINA paket (Olympos{P}1298). Olculer: arayuz/23-upgrade.md
// Govde duz siyah alfa 0.895 (olculdu); panel / yuva saydamliklari sprite'in alfasinda. Krom + dugmeler opak (orijinal piksel).
using System;
using System.Globalization;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/{P}/{P} Penceresi")]
    public class Olympos{P}Penceresi : MonoBehaviour
    {{
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.895f;

        [Header("Yazilar")]
        public Text needCoinsText;
        {"public Text upgradeRateText;" if rate else ""}
        public Text paraText;

        [Header("Dugmeler")]
        public Button upgradeButton;
        public Button cancelButton;
        {"public Button previewButton;" if preview else ""}
        public Button closeButton;

        [Header("Yuvalar (ikon Image'lari; bos yuva = devre disi)")]
        public Image[] upgradeYuvalari = new Image[0];
        public Image[] envanterYuvalari = new Image[0];
        public Text[] envanterAdetleri = new Text[0];

        [Header("Deneme")]
        public bool acilistaGoster = true;
        public long denemePara = 5042580;

        [Header("Olaylar")]
        public UnityEvent onUpgrade = new UnityEvent();
        public UnityEvent onCancel = new UnityEvent();
        {"public UnityEvent onPreview = new UnityEvent();" if preview else ""}
        public UnityEvent onClose = new UnityEvent();

        void Awake()
        {{
            if (upgradeButton != null) upgradeButton.onClick.AddListener(() => onUpgrade.Invoke());
            if (cancelButton != null) cancelButton.onClick.AddListener(() => onCancel.Invoke());
            {"if (previewButton != null) previewButton.onClick.AddListener(() => onPreview.Invoke());" if preview else ""}
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }}

        void Start()
        {{
            if (!acilistaGoster) {{ gameObject.SetActive(false); return; }}
            Ac(denemePara);
        }}

        void OnValidate() {{ ZeminiUygula(); }}
        void ZeminiUygula() {{ if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }}

        /// <summary>Pencereyi acar; degerler "-" ile baslar (orijinaldeki gibi).</summary>
        public void Ac(long para)
        {{
            gameObject.SetActive(true); transform.SetAsLastSibling();
            SetNeedCoins("-"); {"SetUpgradeRate(\"-\");" if rate else ""} SetPara(para);
            for (int i = 0; i < upgradeYuvalari.Length; i++) SetUpgradeYuvasi(i, null);
        }}

        public void Kapat() {{ gameObject.SetActive(false); onClose.Invoke(); }}

        public void SetNeedCoins(string metin) {{ if (needCoinsText != null) needCoinsText.text = metin; }}
        {"public void SetUpgradeRate(string metin) { if (upgradeRateText != null) upgradeRateText.text = metin; }" if rate else ""}
        {"/// <summary>Oran: 100 -> \"%100,0\" (orijinal bicim).</summary>" if rate else ""}
        {"public void SetUpgradeRate(float yuzde) { SetUpgradeRate(\"%\" + yuzde.ToString(\"0.0\", CultureInfo.GetCultureInfo(\"tr-TR\"))); }" if rate else ""}
        /// <summary>Para: 5042580 -> "5,042,580".</summary>
        public void SetPara(long para) {{ if (paraText != null) paraText.text = para.ToString("#,0", CultureInfo.InvariantCulture); }}

        public void SetUpgradeYuvasi(int i, Sprite ikon)
        {{
            if (i < 0 || i >= upgradeYuvalari.Length || upgradeYuvalari[i] == null) return;
            upgradeYuvalari[i].sprite = ikon; upgradeYuvalari[i].enabled = ikon != null;
        }}

        public void SetEnvanter(int i, Sprite ikon, int adet)
        {{
            if (i < 0 || i >= envanterYuvalari.Length || envanterYuvalari[i] == null) return;
            envanterYuvalari[i].sprite = ikon; envanterYuvalari[i].enabled = ikon != null;
            if (i < envanterAdetleri.Length && envanterAdetleri[i] != null) envanterAdetleri[i].text = (ikon != null && adet > 1) ? adet.ToString() : "";
        }}
    }}
}}
'''
CS_SECIM='''// OLYMPOS-KO · 1298 Select Upgrade menusu — TEK BASINA paket (OlymposSelectUpgrade1298). Olculer: arayuz/23-upgrade.md
// Govde duz siyah alfa 0.93 (sol kenardan olculdu); baslik + kenar + 4 dugme opak (orijinal piksel, yazilar sprite'ta).
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/SelectUpgrade/Select Upgrade Menusu")]
    public class OlymposSelectUpgradePenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;
        [Header("Dugmeler")]
        public Button itemUpgradeButton;
        public Button fastUpgradeButton;
        public Button accessoryUpgradeButton;
        public Button closeButton;
        [Header("Deneme")]
        public bool acilistaGoster = true;
        [Header("Olaylar (secimden sonra menu kapanir)")]
        public UnityEvent onItemUpgrade = new UnityEvent();
        public UnityEvent onFastUpgrade = new UnityEvent();
        public UnityEvent onAccessoryUpgrade = new UnityEvent();
        public UnityEvent onClose = new UnityEvent();

        void Awake()
        {
            if (itemUpgradeButton != null) itemUpgradeButton.onClick.AddListener(() => Sec(onItemUpgrade));
            if (fastUpgradeButton != null) fastUpgradeButton.onClick.AddListener(() => Sec(onFastUpgrade));
            if (accessoryUpgradeButton != null) accessoryUpgradeButton.onClick.AddListener(() => Sec(onAccessoryUpgrade));
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }
        void Start() { if (!acilistaGoster) gameObject.SetActive(false); }
        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }
        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Kapat() { gameObject.SetActive(false); onClose.Invoke(); }
        void Sec(UnityEvent e) { gameObject.SetActive(false); e.Invoke(); }
    }
}
'''
def builder(P,menu,govde_kod,X0,Y0,W,H,font=True):
    fontlar=('            var slab = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Bold.ttf");\n            var slabR = AssetDatabase.LoadAssetAtPath<Font>(Root + "/Fonts/RobotoSlab-Regular.otf");\n') if font else ''
    src=open(A+'/OlymposItemRemove1298/Editor/OlymposItemRemoveBuilder.cs').read()
    a=src.index('        [MenuItem('); b=src.index('        static Text Yazi(')
    c_=src.index('        // ---------------------------------------------------------------- yardimcilar')
    s=src[:a]+f'''        // Kaynak goruntu {SX}x{SY} (tablet); ortak 2712x1220 Canvas'a yukseklige gore olcek {S:.4f}, sag kenara yasli.
        const float SX = {SX}f, SY = {SY}f, OLCEK = {S:.6f}f;

        [MenuItem("OLYMPOS/1298/{menu} Oluştur")]
        public static void Build()
        {{
            Root = FindRoot();
            Tex("{P.lower()}_pencere");
            AssetDatabase.Refresh();
{fontlar}            const float X = {X0}, Y = {Y0};
            var go = Kok("{P}_1298", X, Y, {W}, {H});
{govde_kod}
            SaveAndPlace(go, "{P}_1298");
        }}

        /// <summary>Kok: kaynak goruntudeki sol-ust (x,y), boyut (w,h) piksel; sag-orta capali, OLCEK ile kucultulmus.</summary>
        static GameObject Kok(string name, float x, float y, float w, float h)
        {{
            var go = new GameObject(name, typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.anchorMin = rt.anchorMax = new Vector2(1f, 0.5f); rt.pivot = new Vector2(0f, 1f);
            rt.sizeDelta = new Vector2(w, h); rt.localScale = new Vector3(OLCEK, OLCEK, 1f);
            rt.anchoredPosition = new Vector2(-(SX - x) * OLCEK, (SY * 0.5f - y) * OLCEK);
            return go;
        }}

        /// <summary>Ortali tek satir yazi; (cx, cy) murekkep merkezi, pencere ici piksel.</summary>
        static Text Yazi(GameObject parent, string ad, string metin, float cx, float cy, Font f, int punto, float aralik, Color renk)
        {{
            var t = Txt(parent, ad, metin, cx - 200f, cy - 30f, 400f, 60f, f, punto, renk, TextAnchor.MiddleCenter);
            if (aralik != 0f) t.gameObject.AddComponent<Olympos{P}HarfAraligi>().aralik = aralik;
            return t;
        }}

        static Image Ikon(GameObject parent, string ad, float x, float y, float w, float h)
        {{
            var img = Img(parent, ad, null, x, y, w, h); img.preserveAspect = true; img.enabled = false; return img;
        }}

'''+src[c_:]
    s=s.replace('OlymposItemRemoveBuilder',f'Olympos{P}Builder').replace('"OlymposItemRemove1298"',f'"Olympos{P}1298"')
    s=s.replace('// OLYMPOS-KO · 1298 Item Remove penceresi — kurucu (sadece Editor)',f'// OLYMPOS-KO · 1298 {P} — kurucu (sadece Editor)')
    s=s.replace('// Menu: OLYMPOS > 1298 > Item Remove Penceresi Oluştur.  Olculer: arayuz/22-item-remove.md (ekran pikseli, sol-ust).',f'// Menu: OLYMPOS > 1298 > {menu} Oluştur.  Olculer: arayuz/23-upgrade.md (kaynak goruntu pikseli, sol-ust).')
    return s
for ad,(P,baslik,menu) in PAK.items():
    K=f'{A}/Olympos{P}1298'
    for d in ['Editor','Scripts','Fonts','Referans',f'Resources/Olympos{P}1298']: os.makedirs(f'{K}/{d}',exist_ok=True)
    if ad!='secim': shutil.copy(FD+'RobotoSlab-Bold.ttf',f'{K}/Fonts/'); shutil.copy(FD+'RobotoSlab-Regular.otf',f'{K}/Fonts/')
    else: shutil.rmtree(f'{K}/Fonts',ignore_errors=True)
    shutil.copy(f'{ad}_sprite.png',f'{K}/Resources/Olympos{P}1298/{P.lower()}_pencere.png')
    for i,r in enumerate(REF[ad]): Image.open(r).save(f'{K}/Referans/{P.lower()}_{i+1}.jpg',quality=92)
    if ad=='secim':
        cf=json.load(open('secim_cfg.json')); X0,Y0,W,H=cf['sprite']; gx,gy,gw,gh=cf['govde']; d=cf['dugmeler']
        kod=f'''            var p = go.AddComponent<OlymposSelectUpgradePenceresi>();
            var bg = Img(go, "Background", null, {gx}, {gy}, {gw}, {gh}); bg.raycastTarget = true; p.background = bg; bg.color = new Color(0f, 0f, 0f, p.backgroundAlpha);
            Img(go, "Krom", "{P.lower()}_pencere", 0, 0, {W}, {H});
            p.itemUpgradeButton = Hit(go, "Btn_ItemUpgrade", {", ".join(map(str,d['item']))});
            p.fastUpgradeButton = Hit(go, "Btn_FastUpgrade", {", ".join(map(str,d['fast']))});
            p.accessoryUpgradeButton = Hit(go, "Btn_AccessoryUpgrade", {", ".join(map(str,d['accessory']))});
            p.closeButton = Hit(go, "Btn_Close", {", ".join(map(str,d['close']))});'''
        open(f'{K}/Scripts/OlymposSelectUpgradePenceresi.cs','w').write(CS_SECIM)
    else:
        cf=json.load(open(f'{ad}_cfg.json')); X0,Y0,X1,Y1=cf['kutu']; W,H=X1-X0,Y1-Y0; u=cf['U']
        rate='rate' in YAZ[ad]; prev='preview' in DUG[ad]; Dg=DUG[ad]; y=YAZ[ad]
        L=[f'            var p = go.AddComponent<Olympos{P}Penceresi>();',
           f'            var bg = Img(go, "Background", null, {u[0]-X0}, {u[1]-Y0}, {u[2]-u[0]}, {u[3]-u[1]}); bg.raycastTarget = true; p.background = bg; bg.color = new Color(0f, 0f, 0f, p.backgroundAlpha);',
           f'            Img(go, "Krom", "{P.lower()}_pencere", 0, 0, {W}, {H});',
           '            var yuv = new System.Collections.Generic.List<Image>();']
        n=0
        for (x0,y0,x1,y1) in BUYUK[ad]:
            L.append(f'            yuv.Add(Ikon(go, "Yuva_{n}", {x0-X0+12}, {y0-Y0+12}, {x1-x0-24}, {y1-y0-24}));'); n+=1
        for (x,yy,w,h) in cf['kucuk_yuvalar']:
            if w>95: continue
            L.append(f'            yuv.Add(Ikon(go, "Yuva_{n}", {x+2}, {yy+2}, {w-4}, {h-4}));'); n+=1
        L.append('            p.upgradeYuvalari = yuv.ToArray();')
        e=cf['envanter']
        L.append(f'            int[] ex = {{ {", ".join(map(str,e["x"]))} }}, ey = {{ {", ".join(map(str,e["y"]))} }};')
        L.append('            var env = new Image[ex.Length * ey.Length]; var adt = new Text[env.Length];')
        L.append(f'            for (int r = 0; r < ey.Length; r++) for (int k = 0; k < ex.Length; k++) {{ int i = r * ex.Length + k; env[i] = Ikon(go, "Envanter_" + i, ex[k] + 2, ey[r] + 2, {e["w"]-4}, {e["h"]-4});')
        L.append(f'                adt[i] = Txt(go, "Adet_" + i, "", ex[k], ey[r] + {e["h"]-30}, {e["w"]-3}, 28, slab, 18, Color.white, TextAnchor.LowerRight); }}')
        L.append('            p.envanterYuvalari = env; p.envanterAdetleri = adt;')
        cx,cy=y['need']; L.append(f'            p.needCoinsText = Yazi(go, "NeedCoins", "-", {cx-X0}f, {cy-Y0}f, slabR, 27, 0f, Hex("#F0F2F5"));')
        if rate: cx,cy=y['rate']; L.append(f'            p.upgradeRateText = Yazi(go, "UpgradeRate", "-", {cx-X0}f, {cy-Y0}f, slabR, 39, 1.5f, Hex("#E1E1E3"));')
        cx,cy=y['para']; L.append(f'            p.paraText = Yazi(go, "Para", "5,042,580", {cx-X0}f, {cy-Y0}f, slab, 34, 1f, Hex("#FFFFFF"));')
        L.append(f'            p.upgradeButton = Hit(go, "Btn_Upgrade", {", ".join(map(str,Dg["upgrade"]))});')
        L.append(f'            p.cancelButton = Hit(go, "Btn_Cancel", {", ".join(map(str,Dg["cancel"]))});')
        if prev: L.append(f'            p.previewButton = Hit(go, "Btn_Preview", {", ".join(map(str,Dg["preview"]))});')
        xc,yc=Dg['x']; L.append(f'            p.closeButton = Hit(go, "Btn_Close", {xc-32}, {yc-32}, 64, 64);')
        kod='\n'.join(L)
        open(f'{K}/Scripts/Olympos{P}Penceresi.cs','w').write(cs_pencere(P,baslik,rate,prev))
    open(f'{K}/Scripts/Olympos{P}HarfAraligi.cs','w').write(cs_harf(P))
    open(f'{K}/Editor/Olympos{P}Builder.cs','w').write(builder(P,menu,kod,X0,Y0,W,H,ad!='secim'))
    open(f'{K}/BENIOKU.txt','w').write(f'''OLYMPOS-KO · 1298 — {baslik} (tek başına paket)
Menü: OLYMPOS > 1298 > {menu} Oluştur -> Prefabs/{P}_1298, ortak Canvas "OlymposOyunIciCanvas (2712x1220)".
Kaynak: kullanıcının tablet ekran görüntüleri (2266 x 1488), Referans/. Pencere Canvas'a yüksekliğe göre {S:.3f} ölçekle, sağ kenara yaslı konur
(kaynakta sağ kenardan {SX-X0-W} px boşluk). Sprite {W} x {H} (kaynak pikseli).
Zemin: düz siyah {"0.93" if ad=="secim" else "0.895"} (ölçüldü; Inspector backgroundAlpha). Panel / yuva saydamlıkları sprite'ın alfasında (arayuz/23-upgrade.md).
Krom, düğmeler, büyük yuvalar, envanter yuvaları opak (orijinal piksel); sabit yazılar sprite'ta.
Değişken yazılar: Roboto Slab Regular 27 (Need Coins), Regular 39 +1.5 (Upgrade Rate), Bold 34 +1 (para). Fontlar Apache 2.0.
''')
    print(P,W,H)
