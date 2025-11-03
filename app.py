import streamlit as st
import requests
import random
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Caja Sorpresa Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:900;font-size:40px;margin-bottom:8px;">
🎁 CYBER MONDAY • CAJA SORPRESA MILLEX
</div>
<p style="text-align:center;color:#666;">Hacé clic en la caja y descubrí tu premio 🎉</p>
""", unsafe_allow_html=True)

# --- Premios ---
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

# --- Estado ---
if "opened" not in st.session_state:
    st.session_state.opened = False
if "prize" not in st.session_state:
    st.session_state.prize = None

# --- Caja 3D animada con confetti ---
html = """
<style>
.box-scene {
  width: 180px;
  height: 180px;
  margin: 40px auto;
  perspective: 800px;
  cursor: pointer;
  position: relative;
}
.box {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 1s ease;
  animation: floaty 2.5s ease-in-out infinite;
}
@keyframes floaty {
  0%{transform:translateY(0px);}
  50%{transform:translateY(-10px);}
  100%{transform:translateY(0px);}
}
.face {
  position: absolute;
  width: 180px;
  height: 180px;
  background: linear-gradient(145deg,#ff3b3b,#ff8c00);
  border: 3px solid #111;
  border-radius: 10px;
}
.face.top { transform: rotateX(90deg) translateZ(90px); background:#ff3b3b; }
.face.bottom { transform: rotateX(-90deg) translateZ(90px); }
.face.left { transform: rotateY(-90deg) translateZ(90px); }
.face.right { transform: rotateY(90deg) translateZ(90px); }
.face.back { transform: rotateY(180deg) translateZ(90px); }
.face.front { transform: translateZ(90px); background:#ff6f00; }

#confetti-canvas {
  position: fixed;
  top:0;left:0;
  width:100%;height:100%;
  pointer-events:none;
  z-index:9999;
}
.reveal {
  text-align:center;
  font-size:32px;
  font-weight:900;
  color:#ff3b3b;
  animation:fadeInUp 1s ease forwards;
}
@keyframes fadeInUp {
  from{opacity:0;transform:translateY(30px);}
  to{opacity:1;transform:translateY(0);}
}
</style>

<canvas id="confetti-canvas"></canvas>
<div class="box-scene" id="boxScene">
  <div class="box" id="giftBox">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face left"></div>
    <div class="face right"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
  </div>
</div>
<p style="text-align:center;font-size:18px;color:#333;">🎁 Tocá la caja para abrirla</p>

<script>
// Confetti setup
function launchConfetti(){
  const duration = 1500;
  const end = Date.now() + duration;
  (function frame(){
    const colors = ['#ff3b3b','#ff9f1a','#ffd60a','#2ecc71','#3498db'];
    for(let i=0;i<10;i++){
      const confetti = document.createElement('div');
      confetti.style.position='fixed';
      confetti.style.width='10px';
      confetti.style.height='10px';
      confetti.style.background=colors[Math.floor(Math.random()*colors.length)];
      confetti.style.top='50%';
      confetti.style.left='50%';
      confetti.style.opacity='0.9';
      confetti.style.transform=`translate(-50%,-50%) rotate(${Math.random()*360}deg)`;
      confetti.style.transition='all 1.5s linear';
      document.body.appendChild(confetti);
      setTimeout(()=>{
        confetti.style.transform=`translate(${(Math.random()-0.5)*1000}px,${600+Math.random()*400}px) rotate(${Math.random()*720}deg)`;
        confetti.style.opacity='0';
      },10);
      setTimeout(()=>{confetti.remove();},1600);
    }
    if(Date.now()<end){requestAnimationFrame(frame);}
  })();
}

const boxScene=document.getElementById('boxScene');
const giftBox=document.getElementById('giftBox');
let opened=false;
boxScene.addEventListener('click',()=>{
  if(opened)return;
  opened=true;
  giftBox.style.transform='rotateX(120deg) rotateY(720deg)';
  launchConfetti();
  setTimeout(()=>{window.parent.postMessage({type:'opened'},'*');},1500);
});
</script>
"""
components.html(html, height=420)

# --- Esperar evento de apertura ---
if st.session_state.prize is None:
    st.markdown("<script>window.addEventListener('message',(e)=>{if(e.data.type==='opened'){parent.postMessage({isStreamlitMessage:true,type:'streamlit:setComponentValue',value:true},'*');}})</script>", unsafe_allow_html=True)
    st.session_state.opened = False

if st.button("💥 Abrir caja (si no se abre arriba)", use_container_width=True):
    st.session_state.opened = True

if st.session_state.opened and st.session_state.prize is None:
    st.session_state.prize = pick_prize()

# --- Mostrar resultado ---
if st.session_state.prize:
    prize = st.session_state.prize
    if prize == "Seguí participando":
        st.warning("😅 Te tocó **Seguí participando**. ¡Probá otra vez más tarde!")
    else:
        st.markdown(f"<div class='reveal'>🎉 ¡Tu premio es: {prize}!</div>", unsafe_allow_html=True)
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
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos tu cupón 🎁")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")




