import streamlit as st
import requests
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:4px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#666;">Tocá el botón y mirá cómo gira la suerte ✨</p>
""", unsafe_allow_html=True)

# Premios y probabilidades
PRIZES = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
PROB   = [5, 12, 18, 25, 40]

# Cupones fijos (no se muestran en pantalla)
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN"
}

def pick_prize():
    return random.choices(PRIZES, weights=PROB, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# Estado de la app
st.session_state.setdefault("final_prize", None)
st.session_state.setdefault("spin_token", 0)

colA, colB, colC = st.columns([1,2,1])
with colB:
    if st.button("🎯 ¡GIRAR!", use_container_width=True):
        st.session_state.final_prize = pick_prize()
        st.session_state.spin_token += 1

final = st.session_state.final_prize or ""
token = st.session_state.spin_token

# HTML con animación de slot corregido
html = f"""
<style>
.slot-wrap {{
  display:flex; flex-direction:column; align-items:center; gap:10px; margin:22px 0;
}}
.slot-window {{
  width: 520px; max-width: 92vw; height: 90px;
  overflow: hidden; border-radius: 14px;
  border: 3px solid #111; background: #0d0d0d;
  box-shadow: 0 12px 28px rgba(0,0,0,.35), inset 0 0 30px rgba(255,255,255,.08);
  position: relative;
}}
.slot-track {{
  position:absolute; left:0; top:0; right:0;
  display:flex; flex-direction:column; align-items:center;
  padding: 12px 0;
}}
.slot-item {{
  font-size: 42px; font-weight: 900;
  color:#ff3b3b; text-shadow: 0 0 14px rgba(255,59,59,.45);
  line-height: 1.2; height: 72px;
}}
.slot-item.c2 {{ color:#ff8c00; text-shadow: 0 0 14px rgba(255,140,0,.45); }}
.slot-item.c3 {{ color:#ffd60a; text-shadow: 0 0 14px rgba(255,214,10,.45); }}
.slot-item.c4 {{ color:#2ecc71; text-shadow: 0 0 14px rgba(46,204,113,.45); }}
.slot-item.c5 {{ color:#3498db; text-shadow: 0 0 14px rgba(52,152,219,.45); }}
.glow {{
  position:absolute; inset:-6px; border-radius:16px;
  box-shadow: 0 0 22px rgba(255,153,0,.35), 0 0 40px rgba(255,59,59,.30) inset;
  pointer-events:none;
}}
</style>

<div class="slot-wrap" id="slot-{token}">
  <div class="slot-window">
    <div class="glow"></div>
    <div class="slot-track" id="track">
      <div class="slot-item">20% OFF</div>
      <div class="slot-item c3">15% OFF</div>
      <div class="slot-item c4">10% OFF</div>
      <div class="slot-item c5">Seguí participando</div>
      <div class="slot-item">25% OFF</div>
      <div class="slot-item c3">15% OFF</div>
      <div class="slot-item c4">10% OFF</div>
      <div class="slot-item c5">Seguí participando</div>
      <div class="slot-item">20% OFF</div>
      <div class="slot-item c4">10% OFF</div>
      <div class="slot-item c3">15% OFF</div>
      <div class="slot-item c5">Seguí participando</div>
      <div class="slot-item" id="finalText">{"🎉 " + final + " 🎉" if final else ""}</div>
    </div>
  </div>
</div>

<script>
(function() {{
  const final = {repr(final)};
  const track = document.getElementById('track');
  if(!track) return;

  const step = 72;
  const spinRows = 14;
  let y = 0;
  let i = 0;

  function tick() {{
    y -= step;
    track.style.transform = `translateY(${{y}}px)`;
    i++;
    if(i < spinRows) {{
      setTimeout(tick, i < 6 ? 60 : i < 10 ? 80 : 110);
    }} else {{
      const f = document.getElementById('finalText');
      if(f && final) {{
        f.textContent = "🎉 " + final + " 🎉";
      }}
    }}
  }}

  if(final) {{
    track.style.transform = 'translateY(0px)';
    setTimeout(tick, 80);
  }}
}})();
</script>
"""
components.html(html, height=260, scrolling=False)

# Resultado + formulario
if st.session_state.final_prize:
    prize = st.session_state.final_prize
    if prize == "Seguí participando":
        st.info("😅 Te tocó **Seguí participando**. ¡Probá de nuevo más tarde!")
    else:
        st.success(f"🎉 ¡Ganaste {prize}!")
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
                            st.error("⚠️ Este correo ya participó.")
                        elif res.get("status") in ["ok", "success"]:
                            st.balloons()
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos el cupón 🎁")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")





