import streamlit as st
import requests
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx4_b7YvdjTDA4YGDlHAGr5u0Gnk1UEeR9qQVS_dRaWMMOUi8hW4lfziXhvvyhwXn5A/exec"

st.set_page_config(page_title="Cyber Monday - Ruleta Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown('<div style="text-align:center;font-weight:800;font-size:40px;">🛍️ CYBER MONDAY • RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)
st.caption("Girás, ves tu premio y te mandamos el cupón por mail. Solo una vez por participante 😉")

PRIZES = [
    {"label": "25% OFF", "color": "#ff3b3b"},
    {"label": "20% OFF", "color": "#ff8c00"},
    {"label": "15% OFF", "color": "#ffd60a"},
    {"label": "10% OFF", "color": "#2ecc71"},
    {"label": "Seguí participando", "color": "#3498db"},
]

# Cupones fijos
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN"
}

st.session_state.setdefault("result_idx", None)
st.session_state.setdefault("angle", 0)
st.session_state.setdefault("coupon", "")
st.session_state.setdefault("prize", "")

segment_deg = 360 / len(PRIZES)
conic = ", ".join([f"{p['color']} {i*segment_deg}deg {(i+1)*segment_deg}deg" for i, p in enumerate(PRIZES)])

def pick_index():
    weights = [5, 12, 18, 25, 40]
    return random.choices(range(len(PRIZES)), weights=weights, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# ---- Ruleta ----
colA, colB, colC = st.columns([1,2,1])
with colB:
    if st.button("🎯 ¡GIRAR LA RULETA!", use_container_width=True):
        idx = pick_index()
        center = idx * segment_deg + segment_deg/2
        spins = random.randint(5, 8)
        st.session_state.angle = spins * 360 + (360 - center)
        st.session_state.result_idx = idx
        st.session_state.prize = PRIZES[idx]["label"]
        st.session_state.coupon = COUPONS[st.session_state.prize]

wheel_html = f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:12px;">
  <div style="position:relative;width:340px;height:340px;">
    <div style="position:absolute;top:-6px;left:50%;transform:translateX(-50%);
                width:0;height:0;border-left:12px solid transparent;border-right:12px solid transparent;
                border-bottom:20px solid #000;border-radius:2px;z-index:5;"></div>
    <div id="wheel" style="
      width:100%;height:100%;border-radius:50%;
      background: conic-gradient({conic});
      transform: rotate({st.session_state.angle}deg);
      transition: transform 3.6s cubic-bezier(.12,.64,.19,1.02);
      position:relative;display:flex;align-items:center;justify-content:center;
      box-shadow:0 12px 30px rgba(0,0,0,.25);
    ">
      <div style="position:absolute;inset:0;">
        {"".join([
          f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate({i*segment_deg + segment_deg/2}deg);transform-origin:center;">'
          f'  <div style="transform:rotate(-{i*segment_deg + segment_deg/2}deg) translateY(-128px);font-size:14px;font-weight:800;color:#111;text-shadow:0 1px 0 rgba(255,255,255,.6);white-space:nowrap;">{p["label"]}</div>'
          f'</div>'
          for i,p in enumerate(PRIZES)
        ])}
      </div>
      <div style="width:76px;height:76px;border-radius:50%;background:#fff;border:7px solid #111;"></div>
    </div>
  </div>
</div>
"""
components.html(wheel_html, height=380)

# ---- Resultado + Email ----
if st.session_state.result_idx is not None:
    prize = st.session_state.prize
    coupon = st.session_state.coupon

    if prize == "Seguí participando":
        st.info("😅 Te tocó **Seguí participando**. ¡Probá otra vez!")
    else:
        st.success(f"🎉 ¡Tu premio es: {prize}!")
        with st.form("email_form", clear_on_submit=False):
            email = st.text_input("📧 Ingresá tu email para recibir tu cupón*", placeholder="tu@correo.com")
            enviar = st.form_submit_button("✉️ Enviarme el cupón", use_container_width=True)
            if enviar:
                if not email or "@" not in email:
                    st.error("Ingresá un email válido.")
                else:
                    payload = {
                        "accion": "enviar_email_cybermonday",
                        "email": email.strip(),
                        "premio": prize,
                        "cupon": coupon,
                        "periodo": current_period()
                    }
                    try:
                        r = requests.post(WEB_APP_URL, json=payload, timeout=15)
                        r.raise_for_status()
                        res = r.json()
                        if res.get("status") == "ya_participo":
                            st.error("⚠️ Este correo ya participó en la Ruleta Mágica.")
                        elif res.get("status") in ["ok", "success"]:
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos el cupón.")
                            st.write(f"Tu código (por si querés copiarlo ahora): `{coupon}`")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")




