import streamlit as st
import requests
import random
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.2;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#666;">Tocá el botón y mirá cómo gira la suerte ✨</p>
""", unsafe_allow_html=True)

# Premios
PRIZES = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
PROB = [5, 12, 18, 25, 40]
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

# Estado
if "final_prize" not in st.session_state:
    st.session_state.final_prize = None

# Slot machine HTML
html = """
<style>
@keyframes flicker {
  0%,19%,21%,23%,25%,54%,56%,100% {opacity:1;}
  20%,24%,55% {opacity:0;}
}
.slot {
  font-size:50px;
  font-weight:900;
  text-align:center;
  margin:40px auto 20px;
  color:#ff3b3b;
  text-shadow:0 0 15px rgba(255,0,0,0.6);
  min-height:80px;
}
.spin-btn {
  background:linear-gradient(90deg,#ff3b3b,#ff8c00);
  color:white;
  font-weight:800;
  border:none;
  border-radius:8px;
  padding:16px 40px;
  font-size:20px;
  cursor:pointer;
  transition:0.3s;
}
.spin-btn:hover {
  transform:scale(1.05);
  background:linear-gradient(90deg,#ff8c00,#ff3b3b);
}
</style>

<div style="text-align:center;">
  <div id="slotText" class="slot">🎁 ¡Preparando tu premio!</div>
  <button id="spinButton" class="spin-btn">🎯 GIRAR</button>
</div>

<script>
const prizes = ["25% OFF","20% OFF","15% OFF","10% OFF","Seguí participando"];
const slot = document.getElementById("slotText");
const button = document.getElementById("spinButton");
let spinning = false;

button.addEventListener("click", ()=>{
  if(spinning) return;
  spinning = true;
  button.disabled = true;
  let count = 0;
  const total = 40 + Math.floor(Math.random()*20);
  const interval = setInterval(()=>{
    slot.textContent = prizes[count % prizes.length];
    count++;
    slot.style.color = ["#ff3b3b","#ff8c00","#ffd60a","#2ecc71","#3498db"][count % prizes.length];
    slot.style.textShadow = `0 0 20px ${slot.style.color}`;
    if(count > total){
      clearInterval(interval);
      const result = prizes[Math.floor(Math.random()*prizes.length)];
      slot.textContent = "🎉 " + result + " 🎉";
      slot.style.animation = "flicker 1.2s ease-in-out 3";
      setTimeout(()=>{
        window.parent.postMessage({type:'result', prize: result}, '*');
      }, 1800);
    }
  }, 80);
});
</script>
"""
components.html(html, height=260)

# JS event listener
st.markdown("""
<script>
window.addEventListener('message',(e)=>{
  if(e.data && e.data.type==='result'){
    parent.postMessage({isStreamlitMessage:true,type:'streamlit:setComponentValue',value:e.data.prize},'*');
  }
});
</script>
""", unsafe_allow_html=True)

# Resultado
if st.session_state.final_prize is None:
    st.session_state.final_prize = None

slot_result = st.empty()
if st.session_state.final_prize is None:
    st.session_state.final_prize = st.text_input("", value="", key="slot_prize_input")

if st.session_state.slot_prize_input:
    prize = st.session_state.slot_prize_input
    st.session_state.final_prize = prize

# Mostrar premio y formulario
if st.session_state.final_prize:
    prize = st.session_state.final_prize
    if prize == "Seguí participando":
        st.warning("😅 Te tocó **Seguí participando**. ¡Probá de nuevo más tarde!")
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




