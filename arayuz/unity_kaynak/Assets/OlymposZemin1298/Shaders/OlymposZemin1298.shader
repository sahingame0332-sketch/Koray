// OLYMPOS-KO · 1298 zemin shader'i
// Knight Online 1298 zemini gibi ISIKSIZ: renk = (katman dokulari, kontrol haritasiyla karisik) x renk haritasi x genel renk.
// Dokular dunya XZ koordinatiyla doser (UV'ye bagli degil): her katmanin karo boyu dunya biriminde verilir.
// Renk haritasinda gri 0.5 = "degisiklik yok" (x2 carpilir; 1298'deki modulate2x gibi).
// Built-in boru hattinda yazildi; isiksiz tek gecis oldugu icin URP'de de cizilir (URP'de denenmedi).
Shader "Olympos/Zemin1298"
{
    Properties
    {
        _Katman0 ("Katman 0 (kontrol R)", 2D) = "white" {}
        _Katman1 ("Katman 1 (kontrol G)", 2D) = "white" {}
        _Katman2 ("Katman 2 (kontrol B)", 2D) = "white" {}
        _Katman3 ("Katman 3 (kontrol A)", 2D) = "white" {}
        _KaroBoyu ("Karo boyu: katman 0-3 (dunya birimi)", Vector) = (10, 10, 10, 10)
        _Kontrol ("Kontrol haritasi (RGBA = katman agirliklari)", 2D) = "red" {}
        _RenkHaritasi ("Renk haritasi (gri 0.5 = degisiklik yok)", 2D) = "gray" {}
        _HaritaAlani ("Harita alani: x, z baslangic; genislik, derinlik", Vector) = (0, 0, 100, 100)
        _Renk ("Genel renk (sicaklik/ton buradan)", Color) = (1, 1, 1, 1)
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "Queue" = "Geometry" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fog
            #include "UnityCG.cginc"

            sampler2D _Katman0;
            sampler2D _Katman1;
            sampler2D _Katman2;
            sampler2D _Katman3;
            sampler2D _Kontrol;
            sampler2D _RenkHaritasi;
            float4 _KaroBoyu;
            float4 _HaritaAlani;
            fixed4 _Renk;

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 xz : TEXCOORD0;
                float2 harita : TEXCOORD1;
                UNITY_FOG_COORDS(2)
            };

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                float3 dunya = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.xz = dunya.xz;
                o.harita = (dunya.xz - _HaritaAlani.xy) / max(_HaritaAlani.zw, 0.0001);
                UNITY_TRANSFER_FOG(o, o.pos);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 k = tex2D(_Kontrol, i.harita);
                k /= max(k.r + k.g + k.b + k.a, 0.0001);
                float4 olcek = 1.0 / max(_KaroBoyu, 0.0001);
                fixed3 c = tex2D(_Katman0, i.xz * olcek.x).rgb * k.r
                         + tex2D(_Katman1, i.xz * olcek.y).rgb * k.g
                         + tex2D(_Katman2, i.xz * olcek.z).rgb * k.b
                         + tex2D(_Katman3, i.xz * olcek.w).rgb * k.a;
                // gri 0.5 -> 1.0 (gamma'da x2, linear'da x4.59: unity_ColorSpaceDouble)
                c *= tex2D(_RenkHaritasi, i.harita).rgb * unity_ColorSpaceDouble.rgb;
                c *= _Renk.rgb;
                fixed4 col = fixed4(c, 1);
                UNITY_APPLY_FOG(i.fogCoord, col);
                return col;
            }
            ENDCG
        }
    }
    FallBack "Unlit/Texture"
}
