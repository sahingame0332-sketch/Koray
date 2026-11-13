// Havuzun icinde donen enerji: dikissiz gurultu dokusu kutupsal koordinatta
// iki katman halinde, farkli hiz ve burgu ile kaydirilir.
Shader "Koray/Prop/EnergySwirl"
{
    Properties
    {
        _MainTex ("Gurultu (gri, dikissiz)", 2D) = "gray" {}
        _Color ("Enerji rengi", Color) = (0.2, 0.85, 0.9, 1)
        _Speed ("Donus hizi", Range(0, 2)) = 0.25
        _Twist ("Burgu", Range(0, 3)) = 0.9
        _Boost ("Parlaklik", Range(0, 4)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Geometry" "RenderType" = "Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            sampler2D _MainTex;
            fixed4 _Color;
            half _Speed, _Twist, _Boost;

            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };

            v2f vert(appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord.xy;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float2 p = i.uv - 0.5;
                float r = length(p) * 2.0;
                float a = atan2(p.y, p.x) * 0.15915494; // / 2pi -> 0..1, tam tur = 1 doku tekrari
                float t = _Time.y * _Speed;
                half n1 = tex2D(_MainTex, float2(a * 2.0 + r * _Twist + t, r * 0.9 - t * 0.6)).r;
                half n2 = tex2D(_MainTex, float2(a * 3.0 - r * _Twist * 0.6 - t * 1.7, r * 1.4 + t * 0.4)).r;
                half v = saturate(n1 * n2 * 2.6);
                half edge = saturate(1.15 - r * r * 0.55);        // kenara dogru hafif kararma
                half3 rgb = _Color.rgb * (0.16 + v * 1.5) + v * v * v * 0.9;
                return fixed4(rgb * edge * _Boost, 1);
            }
            ENDCG
        }
    }
    Fallback Off
}
