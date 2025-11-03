import streamlit as st
import requests
import random
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Ruleta Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:800;font-size:38px;line-height:1.2;margin-bottom:8px;">
🛍️ CYBER MONDAY<br>🎡 RULETA MÁGICA MILLEX 🎡
</div>
<p style="text-align:center;color:#555;">Girás, ganás y te llega el cupón por mail. ¡Probá tu suerte!</p>
""", unsafe_allow_html=True)

PRIZES = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
PROBABILITIES = [5, 12, 18, 25, 40]
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN"
}

def pick_prize():
    return random.choices(PRIZES, weights=PROBABILITIES, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# Estado
if "result" not in st.session_state:
    st.session_state.result = None

# --- Ruleta interactiva (animación SVG + confetti) ---
html_code = """
<div style="text-align:center;">
  <svg id="wheel" viewBox="0 0 500 500" width="300" height="300" style="transform:rotate(0deg);transition:transform 4s cubic-bezier(.17,.67,.29,1.29);">
    <defs>
      <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#ff3b3b;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#ff9f1a;stop-opacity:1" />
      </linearGradient>
    </defs>
    <circle cx="250" cy="250" r="240" fill="url(#grad)" stroke="#222" stroke-width="6"/>
    <text x="250" y="260" text-anchor="middle" font-size="40" font-weight="bold" fill="#fff">🎡</text>
  </svg>
  <div style="position:relative;margin-top:8px;">
    <div style="position:absolute;left:50%;transform:translateX(-50%);width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-bottom:20px solid #000;"></div>
  </div>
</div>
<script>
const wheel = document.getElementById('wheel');
window.addEventListener('message', (event)=>{
  if(event.data.type==='spin'){
    const spins = Math.floor(Math.random()*5)+5;
    const target = event.data.angle || 0;
    wheel.style.transform = `rotate(${spins*360+target}deg)`;
    setTimeout(()=>{window.parent.postMessage({type:'done'},'*');},3800);
  }
});
</script>
"""
components.html(html_code, height=360)

# --- Botón para girar ---
if st.button("🎯 ¡GIRAR AHORA!", use_container_width=True):
    prize = pick_prize()
    st.session_state.result = prize
    components.html(
        f"<script>window.parent.postMessage({{type:'spin',angle:{random.randint(0,360)}}},'*');</script>",
        height=0
    )

# --- Resultado ---
if st.session_state.result:
    prize = st.session_state.result
    if prize == "Seguí participando":
        st.warning("😅 Te tocó **Seguí participando**. ¡Probá de nuevo más tarde!")
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
                        "cupon": COUPONS[prize],
                        "periodo": current_period()
                    }
                    try:
                        r = requests.post(WEB_APP_URL, json=payload, timeout=15)
                        r.raise_for_status()
                        res = r.json()
                        if res.get("status") == "ya_participo":
                            st.error("⚠️ Este correo ya participó en la Ruleta Mágica.")
                        elif res.get("status") in ["ok", "success"]:
                            st.balloons()
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos el cupón 🎁")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")




