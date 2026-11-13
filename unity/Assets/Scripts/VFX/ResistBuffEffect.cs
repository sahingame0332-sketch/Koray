using UnityEngine;
using UnityEngine.Rendering;

namespace Koray.VFX
{
    public enum ResistElement
    {
        Fire,
        Ice,
        Lightning,
        Poison,
        Custom
    }

    /// <summary>
    /// Direnc (resist) buff'i kullanim efekti: yerde donen run cemberi, govdenin
    /// etrafinda yalpalayan uc halka ve yukselen kivilcimlar.
    ///
    /// KURULUM GEREKMEZ. Butun parcalar kodla kurulur; doku ve shader
    /// Resources/VFX/ResistBuff altindan yuklenir. Prefab, materyal, Particle
    /// System ayari yok.
    ///
    /// Kullanim (tek satir):
    ///     ResistBuffEffect.Play(karakter.transform, ResistElement.Fire);
    ///
    /// Kalici aura olarak:
    ///     var fx = ResistBuffEffect.Play(karakter.transform, ResistElement.Ice, loop: true);
    ///     ...
    ///     fx.Stop();   // yumusakca soner ve kendini yok eder
    ///
    /// Prefab olarak (SkillDefinition.CastVfx alanina baglamak icin):
    ///     Tools > Koray > VFX > Resist Efekti Prefab'larini Uret
    /// </summary>
    [AddComponentMenu("Koray/VFX/Resist Buff Effect")]
    public class ResistBuffEffect : MonoBehaviour
    {
        private const string ResourceDir = "VFX/ResistBuff/";
        private const float FadeIn = 0.18f;
        private const float FadeOut = 0.45f;
        private const int HoopCount = 3;

        [Header("Gorunum")]
        public ResistElement element = ResistElement.Fire;
        [Tooltip("Yalnizca element = Custom iken kullanilir.")]
        public Color customColor = new Color(1f, 0.72f, 0.18f, 1f);
        [Tooltip("Yerdeki cemberin yaricapi (metre).")]
        [Min(0.1f)] public float radius = 1.15f;
        [Tooltip("Karakter boyu (metre). Halkalarin ve kivilcimlarin yuksekligini belirler.")]
        [Min(0.1f)] public float height = 1.7f;
        [Range(0f, 3f)] public float intensity = 1f;
        [Range(0, 64)] public int sparkCount = 26;
        [Tooltip("Zeminle titresmeyi (z-fighting) onlemek icin yerden yukseklik.")]
        public float groundOffset = 0.04f;

        [Header("Zamanlama")]
        [Min(0.7f)] public float duration = 1.8f;
        [Tooltip("Acikken Stop() cagrilana kadar surer (kalici aura).")]
        public bool loop;
        public bool playOnEnable = true;
        public bool destroyOnFinish = true;

        [Header("Takip")]
        [Tooltip("Bos birakilirsa efekt oldugu yerde / ebeveynine bagli kalir.")]
        public Transform target;

        // --- paylasilan kaynaklar (butun ornekler ortak kullanir) ---
        private static Mesh s_quad;
        private static Material s_runeMat, s_hoopMat, s_glowMat, s_sparkMat;
        private static readonly int TintId = Shader.PropertyToID("_TintColor");

        // Halka basina sabitler: egim, yalpa hizi (derece/sn), yaricap ve yukseklik oranlari
        private static readonly float[] HoopTilt = { 18f, -27f, 35f };
        private static readonly float[] HoopPrecession = { 230f, -175f, 265f };
        private static readonly float[] HoopRadius = { 0.52f, 0.60f, 0.46f };
        private static readonly float[] HoopHeight = { 0.34f, 0.52f, 0.70f };

        private Transform _glow, _runeOuter, _runeInner, _shock, _sparksTf;
        private readonly Transform[] _hoops = new Transform[HoopCount];
        private Renderer _glowR, _runeOuterR, _runeInnerR, _shockR, _sparksR;
        private readonly Renderer[] _hoopR = new Renderer[HoopCount];
        private MaterialPropertyBlock _mpb;

        // kivilcimlar: tek dinamik mesh
        private Mesh _sparkMesh;
        private Vector3[] _sparkPos, _sparkVel, _verts;
        private float[] _sparkAge, _sparkLife, _sparkSize;
        private Color[] _cols;

        private Camera _cam;
        private float _age, _end;
        private bool _built, _playing, _looping;

        public bool IsPlaying { get { return _playing; } }

        // ------------------------------------------------------------------
        //  Statik giris noktalari
        // ------------------------------------------------------------------

        /// <summary>Efekti hedefin ayaginda oynatir; hedefi takip eder, bitince kendini yok eder.</summary>
        public static ResistBuffEffect Play(Transform target, ResistElement element = ResistElement.Fire,
                                            float duration = 1.8f, bool loop = false)
        {
            ResistBuffEffect fx = Create(element, duration, loop);
            fx.target = target;
            if (target != null) fx.transform.position = target.position;
            fx.Play();
            return fx;
        }

        /// <summary>Efekti sabit bir dunya konumunda oynatir.</summary>
        public static ResistBuffEffect PlayAt(Vector3 position, ResistElement element = ResistElement.Fire,
                                              float duration = 1.8f)
        {
            ResistBuffEffect fx = Create(element, duration, false);
            fx.transform.position = position;
            fx.Play();
            return fx;
        }

        private static ResistBuffEffect Create(ResistElement element, float duration, bool loop)
        {
            GameObject go = new GameObject("ResistBuffEffect");
            go.SetActive(false); // OnEnable alanlar atanmadan calismasin
            ResistBuffEffect fx = go.AddComponent<ResistBuffEffect>();
            fx.element = element;
            fx.duration = duration;
            fx.loop = loop;
            fx.playOnEnable = false;
            go.SetActive(true);
            return fx;
        }

        public static Color ColorOf(ResistElement element, Color custom)
        {
            switch (element)
            {
                case ResistElement.Fire:      return new Color(1.00f, 0.70f, 0.16f, 1f);
                case ResistElement.Ice:       return new Color(0.30f, 0.72f, 1.00f, 1f);
                case ResistElement.Lightning: return new Color(0.72f, 0.50f, 1.00f, 1f);
                case ResistElement.Poison:    return new Color(0.42f, 1.00f, 0.32f, 1f);
                default:                      return custom;
            }
        }

        // ------------------------------------------------------------------
        //  Yasam dongusu
        // ------------------------------------------------------------------

        private void OnEnable()
        {
            if (playOnEnable) Play();
        }

        private void OnDestroy()
        {
            if (_sparkMesh != null) Destroy(_sparkMesh);
        }

        /// <summary>Efekti bastan oynatir.</summary>
        public void Play()
        {
            if (!_built) Build();
            _age = 0f;
            _looping = loop;
            _end = Mathf.Max(duration, FadeIn + FadeOut);
            _playing = true;
            for (int i = 0; i < _sparkPos.Length; i++) RespawnSpark(i, true);
            SetVisible(true);
            Apply(0f);
        }

        /// <summary>Yumusakca sondurur (loop modundaki aurayi bitirmek icin).</summary>
        public void Stop()
        {
            if (!_playing) return;
            _looping = false;
            _end = Mathf.Min(_end, _age + FadeOut);
        }

        private void LateUpdate()
        {
            if (!_playing) return;

            if (target != null) transform.position = target.position;
            transform.rotation = Quaternion.identity; // cember hep yere paralel kalsin

            float dt = Time.deltaTime;
            _age += dt;

            if (!_looping && _age >= _end)
            {
                _playing = false;
                SetVisible(false);
                if (destroyOnFinish) Destroy(gameObject);
                return;
            }
            Apply(dt);
        }

        // ------------------------------------------------------------------
        //  Animasyon
        // ------------------------------------------------------------------

        private void Apply(float dt)
        {
            Color c = ColorOf(element, customColor);
            float fadeOut = _looping ? 1f : 1f - Mathf.Clamp01((_age - (_end - FadeOut)) / FadeOut);
            float env = Mathf.Clamp01(_age / FadeIn) * fadeOut * intensity;
            float pulse = 0.85f + 0.15f * Mathf.Sin(_age * 9f);

            // yer cemberi: kucukten buyuyerek acilir, yavasca doner
            float open = EaseOutBack(Mathf.Clamp01(_age / 0.32f));
            float d = radius * 2f * Mathf.Lerp(0.35f, 1f, open);
            Place(_runeOuter, groundOffset, d, _age * 38f);
            Place(_runeInner, groundOffset + 0.01f, d * 0.56f, -_age * 72f);
            Place(_glow, groundOffset * 0.5f, d * 1.25f, 0f);
            Tint(_runeOuterR, c, env * pulse);
            Tint(_runeInnerR, c, env * 0.8f);
            Tint(_glowR, c, env * 0.9f * pulse);

            // acilis sok halkasi
            float s = Mathf.Clamp01(_age / 0.55f);
            Place(_shock, groundOffset + 0.02f, radius * 2f * Mathf.Lerp(0.3f, 1.7f, EaseOut(s)), 0f);
            Tint(_shockR, c, (1f - s) * (1f - s) * intensity);

            // govde halkalari: ayaktan yukselir, sonra hafifce salinir
            float rise = EaseOut(Mathf.Clamp01(_age / 0.6f));
            for (int i = 0; i < HoopCount; i++)
            {
                float bob = Mathf.Sin(_age * 2.6f + i * 2.1f) * 0.05f;
                float y = height * (Mathf.Lerp(0.06f, HoopHeight[i], rise) + bob);
                float r = radius * HoopRadius[i] * Mathf.Lerp(1.5f, 1f, rise);
                Transform t = _hoops[i];
                t.localPosition = new Vector3(0f, y, 0f);
                t.localRotation = Quaternion.AngleAxis(_age * HoopPrecession[i] + i * 120f, Vector3.up)
                                * Quaternion.AngleAxis(HoopTilt[i], Vector3.right)
                                * Quaternion.AngleAxis(_age * 300f, Vector3.up);
                t.localScale = new Vector3(r * 2f, 1f, r * 2f);
                Tint(_hoopR[i], c, env * 0.9f);
            }

            UpdateSparks(dt, c, env, fadeOut >= 1f);
        }

        private static void Place(Transform t, float y, float diameter, float yaw)
        {
            t.localPosition = new Vector3(0f, y, 0f);
            t.localRotation = Quaternion.AngleAxis(yaw, Vector3.up);
            t.localScale = new Vector3(diameter, 1f, diameter);
        }

        private void Tint(Renderer r, Color c, float alpha)
        {
            c.a = alpha;
            _mpb.SetColor(TintId, c);
            r.SetPropertyBlock(_mpb);
        }

        private static float EaseOut(float t)
        {
            float u = 1f - t;
            return 1f - u * u * u;
        }

        private static float EaseOutBack(float t)
        {
            float u = t - 1f;
            return 1f + 2.7f * u * u * u + 1.7f * u * u;
        }

        // ------------------------------------------------------------------
        //  Kivilcimlar
        // ------------------------------------------------------------------

        private void RespawnSpark(int i, bool stagger)
        {
            float a = Random.Range(0f, Mathf.PI * 2f);
            float r = radius * Random.Range(0.25f, 0.85f);
            _sparkPos[i] = new Vector3(Mathf.Cos(a) * r, Random.Range(0f, height * 0.35f), Mathf.Sin(a) * r);
            // yukari + hafif girdap
            _sparkVel[i] = new Vector3(-Mathf.Sin(a) * 0.5f, Random.Range(0.5f, 1.3f) * height * 0.55f, Mathf.Cos(a) * 0.5f);
            _sparkLife[i] = Random.Range(0.55f, 1.05f);
            _sparkSize[i] = Random.Range(0.06f, 0.14f) * radius;
            _sparkAge[i] = stagger ? -Random.Range(0f, 0.9f) : 0f; // eksi = bekleme
        }

        private void UpdateSparks(float dt, Color c, float env, bool emitting)
        {
            int n = Mathf.Min(sparkCount, _sparkPos.Length); // Inspector'da sonradan arttirilmis olabilir
            if (n == 0) return;

            if (_cam == null) _cam = Camera.main;
            Vector3 right = Vector3.right, up = Vector3.forward;
            if (_cam != null)
            {
                right = _sparksTf.InverseTransformDirection(_cam.transform.right);
                up = _sparksTf.InverseTransformDirection(_cam.transform.up);
            }

            for (int i = 0; i < n; i++)
            {
                _sparkAge[i] += dt;
                if (_sparkAge[i] >= _sparkLife[i])
                {
                    if (emitting) RespawnSpark(i, false);
                    else _sparkAge[i] = _sparkLife[i];
                }

                float k = _sparkAge[i] / _sparkLife[i]; // 0..1, eksi ise henuz dogmadi
                float a = 0f;
                if (k > 0f && k < 1f)
                {
                    _sparkPos[i] += _sparkVel[i] * dt;
                    a = Mathf.Sin(k * Mathf.PI) * (0.7f + 0.3f * Mathf.Sin(_age * 30f + i * 1.7f));
                }

                float h = _sparkSize[i] * 0.5f * (a > 0f ? 1f : 0f);
                Vector3 p = _sparkPos[i], rx = right * h, uy = up * h;
                int v = i * 4;
                _verts[v] = p - rx - uy;
                _verts[v + 1] = p - rx + uy;
                _verts[v + 2] = p + rx + uy;
                _verts[v + 3] = p + rx - uy;
                Color col = new Color(1f, 1f, 1f, a);
                _cols[v] = _cols[v + 1] = _cols[v + 2] = _cols[v + 3] = col;
            }

            _sparkMesh.vertices = _verts;
            _sparkMesh.colors = _cols;
            Tint(_sparksR, c, env * 1.4f);
        }

        // ------------------------------------------------------------------
        //  Kurulum
        // ------------------------------------------------------------------

        private void Build()
        {
            EnsureShared();
            _mpb = new MaterialPropertyBlock();

            _glow = Part("GroundGlow", s_quad, s_glowMat, out _glowR);
            _runeOuter = Part("RuneOuter", s_quad, s_runeMat, out _runeOuterR);
            _runeInner = Part("RuneInner", s_quad, s_runeMat, out _runeInnerR);
            _shock = Part("Shockwave", s_quad, s_hoopMat, out _shockR);
            for (int i = 0; i < HoopCount; i++)
                _hoops[i] = Part("Hoop" + i, s_quad, s_hoopMat, out _hoopR[i]);

            BuildSparkMesh();
            _sparksTf = Part("Sparks", _sparkMesh, s_sparkMat, out _sparksR);
            _built = true;
        }

        private Transform Part(string partName, Mesh mesh, Material mat, out Renderer renderer)
        {
            GameObject go = new GameObject(partName);
            go.hideFlags = HideFlags.DontSave; // prefab'a / sahneye kaydedilmesin, her seferinde kodla kurulur
            go.transform.SetParent(transform, false);
            go.AddComponent<MeshFilter>().sharedMesh = mesh;
            MeshRenderer mr = go.AddComponent<MeshRenderer>();
            mr.sharedMaterial = mat;
            mr.shadowCastingMode = ShadowCastingMode.Off;
            mr.receiveShadows = false;
            renderer = mr;
            return go.transform;
        }

        private void SetVisible(bool visible)
        {
            _glowR.enabled = _runeOuterR.enabled = _runeInnerR.enabled = _shockR.enabled = visible;
            _sparksR.enabled = visible && sparkCount > 0;
            for (int i = 0; i < HoopCount; i++) _hoopR[i].enabled = visible;
        }

        private void BuildSparkMesh()
        {
            int n = Mathf.Max(sparkCount, 1);
            _sparkPos = new Vector3[n];
            _sparkVel = new Vector3[n];
            _sparkAge = new float[n];
            _sparkLife = new float[n];
            _sparkSize = new float[n];
            _verts = new Vector3[n * 4];
            _cols = new Color[n * 4];
            Vector2[] uv = new Vector2[n * 4];
            int[] tris = new int[n * 6];
            for (int i = 0; i < n; i++)
            {
                int v = i * 4, t = i * 6;
                uv[v] = new Vector2(0f, 0f);
                uv[v + 1] = new Vector2(0f, 1f);
                uv[v + 2] = new Vector2(1f, 1f);
                uv[v + 3] = new Vector2(1f, 0f);
                tris[t] = v; tris[t + 1] = v + 1; tris[t + 2] = v + 2;
                tris[t + 3] = v; tris[t + 4] = v + 2; tris[t + 5] = v + 3;
                _sparkLife[i] = 1f;
            }
            _sparkMesh = new Mesh();
            _sparkMesh.name = "ResistBuffSparks";
            _sparkMesh.hideFlags = HideFlags.DontSave;
            _sparkMesh.MarkDynamic();
            _sparkMesh.vertices = _verts;
            _sparkMesh.uv = uv;
            _sparkMesh.colors = _cols;
            _sparkMesh.triangles = tris;
            // Kivilcimlar hareket eder; her karede sinir hesaplamak yerine genis sabit kutu.
            _sparkMesh.bounds = new Bounds(new Vector3(0f, height, 0f),
                                           new Vector3(radius * 4f, height * 4f, radius * 4f));
        }

        private static void EnsureShared()
        {
            if (s_quad == null)
            {
                // XZ duzleminde 1x1 kare (yukari bakar); shader Cull Off oldugu icin iki yuzu de gorunur.
                s_quad = new Mesh();
                s_quad.name = "ResistBuffQuad";
                s_quad.hideFlags = HideFlags.DontSave;
                s_quad.vertices = new[]
                {
                    new Vector3(-0.5f, 0f, -0.5f), new Vector3(-0.5f, 0f, 0.5f),
                    new Vector3(0.5f, 0f, 0.5f), new Vector3(0.5f, 0f, -0.5f)
                };
                s_quad.uv = new[]
                {
                    new Vector2(0f, 0f), new Vector2(0f, 1f), new Vector2(1f, 1f), new Vector2(1f, 0f)
                };
                Color w = Color.white;
                s_quad.colors = new[] { w, w, w, w };
                s_quad.triangles = new[] { 0, 1, 2, 0, 2, 3 };
                s_quad.RecalculateBounds();
            }

            if (s_runeMat != null && s_hoopMat != null && s_glowMat != null && s_sparkMat != null) return;

            Shader shader = Resources.Load<Shader>(ResourceDir + "KorayAdditive");
            if (shader == null)
            {
                Debug.LogWarning("ResistBuffEffect: Resources/" + ResourceDir +
                                 "KorayAdditive.shader bulunamadi; yedek shader kullaniliyor.");
                shader = Shader.Find("Legacy Shaders/Particles/Additive");
                if (shader == null) shader = Shader.Find("Sprites/Default");
            }
            s_runeMat = MakeMaterial(shader, "rune_circle", 0.5f);
            s_hoopMat = MakeMaterial(shader, "hoop", 0.8f);
            s_glowMat = MakeMaterial(shader, "glow", 0.1f);
            s_sparkMat = MakeMaterial(shader, "spark", 1.2f);
        }

        private static Material MakeMaterial(Shader shader, string textureName, float core)
        {
            Material m = new Material(shader);
            m.name = "ResistBuff_" + textureName;
            m.hideFlags = HideFlags.DontSave;
            Texture2D tex = Resources.Load<Texture2D>(ResourceDir + textureName);
            if (tex == null)
            {
                Debug.LogWarning("ResistBuffEffect: Resources/" + ResourceDir + textureName + ".png bulunamadi.");
            }
            else
            {
                tex.wrapMode = TextureWrapMode.Clamp;
                m.mainTexture = tex;
            }
            m.SetFloat("_Core", core);
            return m;
        }
    }
}
