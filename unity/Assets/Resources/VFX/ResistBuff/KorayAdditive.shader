// Gri tonlamali dokuyu renklendirip ekleyerek (additive) cizer.
// Built-in ve URP'de calisir (isiksiz, tek gecis). Resources altinda durur ki
// build'e kendiliginden dahil olsun -- ResistBuffEffect.cs buradan yukler.
Shader "Koray/VFX/Additive"
{
    Properties
    {
        _MainTex ("Yogunluk dokusu (gri)", 2D) = "white" {}
        _TintColor ("Renk (a = opaklik)", Color) = (1, 0.72, 0.18, 1)
        _Core ("Beyaz cekirdek", Range(0, 2)) = 0.6
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" "IgnoreProjector" = "True" "PreviewType" = "Plane" }
        Blend One One
        Cull Off
        ZWrite Off
        Lighting Off
        Offset -1, -1

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _TintColor;
            fixed _Core;

            struct appdata
            {
                float4 vertex : POSITION;
                fixed4 color : COLOR;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                fixed4 color : COLOR;
                float2 uv : TEXCOORD0;
            };

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.color = v.color;
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                fixed t = tex2D(_MainTex, i.uv).r;
                fixed3 rgb = _TintColor.rgb * i.color.rgb * t + _Core * t * t * t;
                return fixed4(rgb * (_TintColor.a * i.color.a), 1);
            }
            ENDCG
        }
    }
    Fallback Off
}
