import streamlit as st
import requests
import random
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

# Tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Caja Sorpresa Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:800;font-size:40px;line-height:1.2;margin-bottom:6px;">
🎁 CYBER MONDAY • CAJA SORPRESA MILLEX
</div>
<p style="text-align:center;color:#555;">Hacé clic en la caja y descubrí tu premio mágico 🎉</p>
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
if "opened" not in st.session_state:
    st.session_state.opened = False
if "prize" not in st.session_state:
    st.session_state.prize = None

# --- Caja animada ---
html_box = """
<div style="display:flex;flex-direction:column;align-items:center;gap:15px;">
  <div id="box" style="position:relative;width:180px;height:180px;cursor:pointer;">
    <div id="lid" style="position:absolute;width:100%;height:35%;background:#ff3b3b;border-radius:10px 10px 0 0;top:0;transition:transform 0.6s ease;z-index:2;"></div>
    <div id="base" style="position:absolute;width:100%;height:70%;background:#ff6f00;border-radius:0 0 10px 10px;bottom:0;z-index:1;"></div>
    <div id="ribbon" style="position:absolute;width:20%;height:100%;background:#fff;left:40%;z-index:3;"></div>
  </div>
  <p style="color:#444;font-size:18px;">🎁 Tocá la caja para abrirla</p>
</div>
<script>
  const box = document.getElementById('box');
  const lid = document.getElementById('lid');
  let opened = false;
  box.addEventListener('click', ()=>{
    if(opened) return;
    opened = true;
    lid.style.transform = 'rotateX(160deg)';
    setTimeout(()=>{window.parent.postMessage({type:'opened'},'*');},1000);
  });
</script>
"""
components.html(html_box, height=300)

# --- Evento de apertura ---
if not st.session_state.opened:
    st.session_state.opened = False

if st.session_state.prize is None:
    st.markdown("<script>window.addEventListener('message',(e)=>{if(e.data.type==='opened'){parent.postMessage({isStreamlitMessage:true,type:'streamlit:setComponentValue',value:true},'*');}})</script>", unsafe_allow_html=True)
    st.session_state.opened = False

# Simular detección de “abierta”
placeholder = st.empty()
if not st.session_state.opened:
    st.session_state.opened = st.button("💥 Abrir la caja (si no se abre arriba)", use_container_width=True)

# --- Mostrar premio cuando se abre ---
if st.session_state.opened and st.session_state.prize is None:
    st.session_state.prize = pick_prize()

if st.session_state.prize:
    prize = st.session_state.prize
    if prize == "Seguí participando":
        st.warning("😅 Te tocó **Seguí participando**. ¡Probá de nuevo más tarde!")
    else:
        st.markdown(
            f"<div style='text-align:center;font-size:26px;font-weight:700;color:#ff3b3b;'>🎉 ¡Tu premio es: {prize}!</div>",
            unsafe_allow_html=True,
        )
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
                            st.error("⚠️ Este correo ya participó en la Caja Sorpresa.")
                        elif res.get("status") in ["ok", "success"]:
                            st.balloons()
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos tu cupón 🎁")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")



