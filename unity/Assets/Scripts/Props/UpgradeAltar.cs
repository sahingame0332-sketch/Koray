using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

namespace Koray.Props
{
    /// <summary>
    /// Yukseltme sunagi: esya yukseltme (upgrade) noktasi olarak kullanilan dekor.
    /// Altigen tas kaide, icinde donen enerji havuzu, ustunde suzulen kristal
    /// cekirdek ve etrafinda iki halka.
    ///
    /// KURULUM GEREKMEZ. Mesh'ler kodla uretilir; doku ve shader'lar
    /// Resources altindan yuklenir. Bos bir objeye bu bileseni eklemek yeter
    /// (veya: GameObject > Koray > Yukseltme Sunagi). Editorde de gorunur.
    ///
    /// Isik kose renklerine onceden islenir: sahne isigindan etkilenmez,
    /// golge atmaz. Dusuk poligonlu (yaklasik 200 ucgen), 6 draw call.
    ///
    /// Yukseltme sonucu icin:
    ///     altar.Pulse();          // kisa parlama (basari)
    ///     altar.Pulse(0.4f);      // zayif parlama
    /// </summary>
    [ExecuteAlways]
    [AddComponentMenu("Koray/Props/Upgrade Altar")]
    public class UpgradeAltar : MonoBehaviour
    {
        private const int Sides = 6;
        private const string Dir = "Props/UpgradeAltar/";
        private const string VfxDir = "VFX/ResistBuff/";

        // Kaide profili: (yaricap, yukseklik) -- 1 birim yukseklige gore, asagidan yukari,
        // disi sag elde kalacak sekilde. Son iki nokta havuzun ic duvaridir.
        private static readonly float[] ProfileR = { 0.50f, 0.50f, 0.40f, 0.40f, 0.17f, 0.14f, 0.44f, 0.47f, 0.47f, 0.39f, 0.37f };
        private static readonly float[] ProfileY = { 0.00f, 0.07f, 0.07f, 0.15f, 0.26f, 0.62f, 0.80f, 0.80f, 0.92f, 0.92f, 0.86f };
        private const float PoolR = 0.37f, PoolY = 0.87f;

        [Header("Boyut")]
        [Tooltip("Kaidenin yerden havuz kenarina yuksekligi (metre). Genislik buna orantilidir.")]
        [Min(0.2f)] public float height = 1.25f;

        [Header("Renk")]
        public Color energyColor = new Color(0.20f, 0.85f, 0.90f, 1f);
        public Color stoneColor = new Color(0.66f, 0.61f, 0.54f, 1f);

        [Header("Enerji")]
        [Range(0f, 3f)] public float brightness = 1f;
        [Tooltip("Havuzdaki girdabin donus hizi.")]
        [Range(0f, 2f)] public float swirlSpeed = 0.25f;
        [Range(0f, 3f)] public float swirlTwist = 0.9f;
        [Tooltip("Havuzun ustundeki isik huzmesinin ve halkalarin opakligi.")]
        [Range(0f, 1f)] public float glowOpacity = 0.6f;

        [Header("Cekirdek")]
        public bool showCore = true;
        [Tooltip("Kristalin boyu, kaide yuksekligine oranla.")]
        [Range(0.05f, 0.6f)] public float coreSize = 0.26f;
        [Tooltip("Derece / saniye.")]
        public float coreSpinSpeed = 45f;

        private static readonly int ColorId = Shader.PropertyToID("_Color");
        private static readonly int TintId = Shader.PropertyToID("_TintColor");
        private static readonly int BrightnessId = Shader.PropertyToID("_Brightness");
        private static readonly int SpeedId = Shader.PropertyToID("_Speed");
        private static readonly int TwistId = Shader.PropertyToID("_Twist");
        private static readonly int BoostId = Shader.PropertyToID("_Boost");

        private readonly List<Object> _owned = new List<Object>();   // mesh + materyaller
        private readonly List<Renderer> _parts = new List<Renderer>();
        private Material _poolMat;
        private Transform _core, _glow, _hoopA, _hoopB;
        private Renderer _coreR, _glowR, _hoopAR, _hoopBR;
        private MaterialPropertyBlock _mpb;
        private float _pulse;
        private bool _built;

        /// <summary>Kisa parlama; yukseltme denemesinin sonucunu vurgulamak icin.</summary>
        public void Pulse(float strength = 1f)
        {
            _pulse = Mathf.Max(_pulse, strength);
        }

        private void OnEnable()
        {
            Build();
        }

        private void OnDisable()
        {
            Teardown();
        }

#if UNITY_EDITOR
        // Inspector'da boyut / renk degisince mesh'leri yeniden kur.
        private bool _dirty;
        private void OnValidate() { _dirty = true; }
#endif

        private void Update()
        {
#if UNITY_EDITOR
            if (_dirty) { _dirty = false; Teardown(); Build(); }
#endif
            if (!_built) return;

            float t = Time.time;
            _pulse = Mathf.Max(0f, _pulse - Time.deltaTime * 1.6f);
            float boost = brightness * (1f + _pulse * 1.8f);
            float breathe = 0.88f + 0.12f * Mathf.Sin(t * 2.2f);

            _poolMat.SetColor(ColorId, energyColor);
            _poolMat.SetFloat(SpeedId, swirlSpeed);
            _poolMat.SetFloat(TwistId, swirlTwist);
            _poolMat.SetFloat(BoostId, boost);

            float coreY = height * (PoolY + 0.16f + coreSize * 0.5f) + Mathf.Sin(t * 1.5f) * height * 0.025f;
            if (showCore)
            {
                _core.localPosition = new Vector3(0f, coreY, 0f);
                _core.localRotation = Quaternion.AngleAxis(t * coreSpinSpeed, Vector3.up);
                _mpb.Clear();
                _mpb.SetFloat(BrightnessId, boost * breathe);
                _coreR.SetPropertyBlock(_mpb);
            }

            float hoopD = height * coreSize * 1.5f;
            Orbit(_hoopA, coreY, hoopD, t * 70f, 62f);
            Orbit(_hoopB, coreY, hoopD * 0.8f, -t * 95f + 90f, -48f);

            Tint(_glowR, glowOpacity * 0.75f * breathe * boost);
            Tint(_hoopAR, showCore ? glowOpacity * boost : 0f);
            Tint(_hoopBR, showCore ? glowOpacity * 0.8f * boost : 0f);
        }

        private static void Orbit(Transform tr, float y, float diameter, float yaw, float tilt)
        {
            tr.localPosition = new Vector3(0f, y, 0f);
            tr.localRotation = Quaternion.AngleAxis(yaw, Vector3.up) * Quaternion.AngleAxis(tilt, Vector3.right);
            tr.localScale = new Vector3(diameter, 1f, diameter);
        }

        private void Tint(Renderer r, float alpha)
        {
            Color c = energyColor;
            c.a = alpha;
            _mpb.Clear();
            _mpb.SetColor(TintId, c);
            r.SetPropertyBlock(_mpb);
        }

        // ------------------------------------------------------------------
        //  Kurulum
        // ------------------------------------------------------------------

        private void Build()
        {
            if (_built) return;
            _mpb = new MaterialPropertyBlock();

            Shader vcol = LoadShader(Dir + "KorayVertexColor");
            Shader swirl = LoadShader(Dir + "KorayEnergySwirl");
            Shader additive = LoadShader(VfxDir + "KorayAdditive");

            Material stoneMat = Own(new Material(vcol));
            stoneMat.mainTexture = Resources.Load<Texture2D>(Dir + "stone");
            Material coreMat = Own(new Material(vcol)); // dokusuz: yalnizca kose rengi
            _poolMat = Own(new Material(swirl));
            _poolMat.mainTexture = Resources.Load<Texture2D>(Dir + "energy_noise");
            Material glowMat = Own(new Material(additive));
            glowMat.mainTexture = Resources.Load<Texture2D>(VfxDir + "glow");
            glowMat.SetFloat("_Core", 0.15f);
            Material hoopMat = Own(new Material(additive));
            hoopMat.mainTexture = Resources.Load<Texture2D>(VfxDir + "hoop");

            Renderer unused;
            Part("Pedestal", BuildPedestal(), stoneMat, out unused);
            Part("Pool", BuildPool(), _poolMat, out unused);

            Mesh quad = BuildQuad();
            _glow = Part("Glow", quad, glowMat, out _glowR);
            _glow.localPosition = new Vector3(0f, height * (PoolY + 0.06f), 0f);
            float g = height * PoolR * 3.2f;
            _glow.localScale = new Vector3(g, 1f, g);

            _core = Part("Core", BuildCore(), coreMat, out _coreR);
            _coreR.enabled = showCore;
            _hoopA = Part("HoopA", quad, hoopMat, out _hoopAR);
            _hoopB = Part("HoopB", quad, hoopMat, out _hoopBR);

            _built = true;
            Update();
        }

        private void Teardown()
        {
            for (int i = 0; i < _parts.Count; i++)
                if (_parts[i] != null) _parts[i].enabled = false;
            _parts.Clear();
            for (int i = 0; i < _owned.Count; i++)
            {
                if (_owned[i] == null) continue;
                if (Application.isPlaying) Destroy(_owned[i]);
                else DestroyImmediate(_owned[i]);
            }
            _owned.Clear();
            _built = false;
        }

        private T Own<T>(T obj) where T : Object
        {
            obj.hideFlags = HideFlags.DontSave; // her acilista kodla kurulur
            _owned.Add(obj);
            return obj;
        }

        private static Shader LoadShader(string path)
        {
            Shader s = Resources.Load<Shader>(path);
            if (s == null)
            {
                Debug.LogWarning("UpgradeAltar: Resources/" + path + ".shader bulunamadi.");
                s = Shader.Find("Sprites/Default");
            }
            return s;
        }

        private Transform Part(string partName, Mesh mesh, Material mat, out Renderer renderer)
        {
            // Parca objeleri yok edilmez, yeniden kullanilir: Unity, bir obje etkinlesirken /
            // devre disi kalirken cocuklarinin yok edilmesine izin vermez.
            Transform existing = transform.Find(partName);
            GameObject go;
            if (existing == null)
            {
                go = new GameObject(partName);
                go.hideFlags = HideFlags.DontSave; // sahneye / prefab'a kaydedilmez
                go.transform.SetParent(transform, false);
                go.AddComponent<MeshFilter>();
                go.AddComponent<MeshRenderer>();
            }
            else
            {
                go = existing.gameObject;
            }
            go.GetComponent<MeshFilter>().sharedMesh = mesh;
            MeshRenderer mr = go.GetComponent<MeshRenderer>();
            mr.enabled = true;
            _parts.Add(mr);
            mr.sharedMaterial = mat;
            mr.shadowCastingMode = ShadowCastingMode.Off;
            mr.receiveShadows = false;
            renderer = mr;
            return go.transform;
        }

        // ------------------------------------------------------------------
        //  Mesh uretimi
        // ------------------------------------------------------------------

        private static readonly Vector3 LightDir = new Vector3(0.38f, 0.80f, -0.46f);

        private static Vector3 Ring(float r, float y, int k)
        {
            float a = Mathf.PI * 2f * k / Sides;
            return new Vector3(Mathf.Cos(a) * r, y, Mathf.Sin(a) * r);
        }

        /// <summary>Profili altigen etrafinda dondurur; her yuz duz golgelenir ve isik kose rengine islenir.</summary>
        private Mesh BuildPedestal()
        {
            List<Vector3> verts = new List<Vector3>();
            List<Vector2> uvs = new List<Vector2>();
            List<Color> cols = new List<Color>();
            List<int> tris = new List<int>();

            float vRun = 0f;
            int last = ProfileR.Length - 1;
            for (int i = 0; i < last; i++)
            {
                float r0 = ProfileR[i] * height, y0 = ProfileY[i] * height;
                float r1 = ProfileR[i + 1] * height, y1 = ProfileY[i + 1] * height;
                float dr = r1 - r0, dy = y1 - y0;
                float len = Mathf.Sqrt(dr * dr + dy * dy);
                float v0 = vRun, v1 = vRun + len;
                vRun = v1;

                for (int k = 0; k < Sides; k++)
                {
                    float am = Mathf.PI * 2f * (k + 0.5f) / Sides;
                    // Profilin sag eli = dis yuz: 2B normal (dy, -dr)
                    Vector3 n = new Vector3(Mathf.Cos(am) * dy, -dr, Mathf.Sin(am) * dy) * (1f / len);

                    float lit = 0.40f + 0.60f * Mathf.Max(0f, Vector3.Dot(n, LightDir));
                    float ao = Mathf.Lerp(0.72f, 1f, (y0 + y1) * 0.5f / height);   // dibe dogru kararir
                    if (n.y < -0.1f) ao *= 0.8f;                                    // canagin alti
                    Color c = Mul(stoneColor, lit * ao);
                    if (i == last - 1) c = Color.Lerp(c, energyColor, 0.55f);       // havuz ic duvari: enerji yansimasi
                    else if (i == last - 2) c = Color.Lerp(c, energyColor, 0.18f);  // ust kenar

                    int b = verts.Count;
                    verts.Add(Ring(r0, y0, k)); verts.Add(Ring(r0, y0, k + 1));
                    verts.Add(Ring(r1, y1, k + 1)); verts.Add(Ring(r1, y1, k));
                    float u0 = k * 0.5f, u1 = (k + 1) * 0.5f, vs = 1.4f / height;
                    uvs.Add(new Vector2(u0, v0 * vs)); uvs.Add(new Vector2(u1, v0 * vs));
                    uvs.Add(new Vector2(u1, v1 * vs)); uvs.Add(new Vector2(u0, v1 * vs));
                    cols.Add(c); cols.Add(c); cols.Add(c); cols.Add(c);
                    AddQuad(tris, verts, b, n);
                }
            }
            return MakeMesh("AltarPedestal", verts, uvs, cols, tris);
        }

        private Mesh BuildPool()
        {
            List<Vector3> verts = new List<Vector3>();
            List<Vector2> uvs = new List<Vector2>();
            List<Color> cols = new List<Color>();
            List<int> tris = new List<int>();
            float y = PoolY * height;
            verts.Add(new Vector3(0f, y, 0f)); uvs.Add(new Vector2(0.5f, 0.5f)); cols.Add(Color.white);
            for (int k = 0; k < Sides; k++)
            {
                float a = Mathf.PI * 2f * k / Sides;
                verts.Add(Ring(PoolR * height, y, k));
                uvs.Add(new Vector2(0.5f + 0.5f * Mathf.Cos(a), 0.5f + 0.5f * Mathf.Sin(a)));
                cols.Add(Color.white);
            }
            for (int k = 0; k < Sides; k++)
            {
                // yukari bakan sarim (Unity: saat yonu on yuz)
                tris.Add(0); tris.Add(1 + (k + 1) % Sides); tris.Add(1 + k);
            }
            return MakeMesh("AltarPool", verts, uvs, cols, tris);
        }

        /// <summary>Uzun cift piramit kristal; her yuz farkli tonda, kendinden isikli gorunur.</summary>
        private Mesh BuildCore()
        {
            List<Vector3> verts = new List<Vector3>();
            List<Vector2> uvs = new List<Vector2>();
            List<Color> cols = new List<Color>();
            List<int> tris = new List<int>();
            float h = height * coreSize * 0.5f, r = h * 0.42f;
            const int n = 5;
            for (int s = 0; s < 2; s++)
            {
                Vector3 apex = new Vector3(0f, s == 0 ? h : -h * 0.8f, 0f);
                for (int k = 0; k < n; k++)
                {
                    float a0 = Mathf.PI * 2f * k / n, a1 = Mathf.PI * 2f * (k + 1) / n;
                    Vector3 p0 = new Vector3(Mathf.Cos(a0) * r, 0f, Mathf.Sin(a0) * r);
                    Vector3 p1 = new Vector3(Mathf.Cos(a1) * r, 0f, Mathf.Sin(a1) * r);
                    float am = (a0 + a1) * 0.5f;
                    Vector3 nrm = new Vector3(Mathf.Cos(am), s == 0 ? 0.45f : -0.45f, Mathf.Sin(am));
                    float shade = 0.5f + 0.5f * Mathf.Sin(k * 2.4f + s * 1.3f);     // yuzden yuze ton farki
                    Color c = Mul(Color.Lerp(energyColor, Color.white, 0.25f + 0.5f * shade), 0.85f + 0.5f * shade);
                    int b = verts.Count;
                    verts.Add(apex); verts.Add(p0); verts.Add(p1);
                    uvs.Add(new Vector2(0.5f, 1f)); uvs.Add(new Vector2(0f, 0f)); uvs.Add(new Vector2(1f, 0f));
                    cols.Add(c); cols.Add(c); cols.Add(c);
                    AddTri(tris, verts, b, b + 1, b + 2, nrm);
                }
            }
            return MakeMesh("AltarCore", verts, uvs, cols, tris);
        }

        private Mesh BuildQuad()
        {
            List<Vector3> verts = new List<Vector3>
            {
                new Vector3(-0.5f, 0f, -0.5f), new Vector3(-0.5f, 0f, 0.5f),
                new Vector3(0.5f, 0f, 0.5f), new Vector3(0.5f, 0f, -0.5f)
            };
            List<Vector2> uvs = new List<Vector2>
            {
                new Vector2(0f, 0f), new Vector2(0f, 1f), new Vector2(1f, 1f), new Vector2(1f, 0f)
            };
            Color w = Color.white;
            List<Color> cols = new List<Color> { w, w, w, w };
            List<int> tris = new List<int> { 0, 1, 2, 0, 2, 3 };
            return MakeMesh("AltarQuad", verts, uvs, cols, tris);
        }

        private Mesh MakeMesh(string meshName, List<Vector3> verts, List<Vector2> uvs, List<Color> cols, List<int> tris)
        {
            Mesh m = Own(new Mesh());
            m.name = meshName;
            m.vertices = verts.ToArray();
            m.uv = uvs.ToArray();
            m.colors = cols.ToArray();
            m.triangles = tris.ToArray();
            m.RecalculateBounds();
            return m;
        }

        private static Color Mul(Color c, float k)
        {
            return new Color(c.r * k, c.g * k, c.b * k, 1f);
        }

        private static void AddQuad(List<int> tris, List<Vector3> verts, int b, Vector3 outward)
        {
            AddTri(tris, verts, b, b + 1, b + 2, outward);
            AddTri(tris, verts, b, b + 2, b + 3, outward);
        }

        /// <summary>Ucgeni, on yuzu verilen dis yone bakacak sarimla ekler.</summary>
        private static void AddTri(List<int> tris, List<Vector3> verts, int a, int b, int c, Vector3 outward)
        {
            Vector3 n = Vector3.Cross(verts[b] - verts[a], verts[c] - verts[a]);
            // Unity'de on yuz: Cross(b-a, c-a) izleyiciye bakar (sol el, saat yonu).
            if (Vector3.Dot(n, outward) < 0f) { int tmp = b; b = c; c = tmp; }
            tris.Add(a); tris.Add(b); tris.Add(c);
        }
    }
}
