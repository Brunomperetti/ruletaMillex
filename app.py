import time
import random
import requests
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

# -------- CONFIG --------
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

PRIZES  = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
WEIGHTS = [5,          12,         18,          25,         40]
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN",
}

ITEM_H = 72
VISIBLE_ROWS = 3
CENTER_IDX = 1

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#8a8a8a;">Tocá GIRAR, mirá cómo vuela y frenalo cuando quieras ✨</p>
""", unsafe_allow_html=True)

def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# -------- STATE --------
st.session_state.setdefault("final_prize", None)     # premio decidido (oculto hasta revelar)
st.session_state.setdefault("spin_seed", 0)          # cambia para reiniciar animación
st.session_state.setdefault("spinning", False)       # está girando?
st.session_state.setdefault("reveal", False)         # mostrar resultado?
st.session_state.setdefault("spin_start", 0.0)       # timestamp inicio
st.session_state.setdefault("spin_duration", 1.6)    # duración animación (rápido)
st.session_state.setdefault("target_px", 0)          # desplazamiento final

# -------- CONTROLES --------
c1, c2, c3 = st.columns([1,1,1])
with c2:
    if st.button("🎯 ¡GIRAR!", use_container_width=True, disabled=st.session_state.spinning):
        st.session_state.final_prize = pick_prize()
        st.session_state.spin_seed += 1
        st.session_state.reveal = False
        st.session_state.spinning = True
        st.session_state.spin_start = time.time()

# Botón Frenar solo visible mientras gira
if st.session_state.spinning and not st.session_state.reveal:
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("🛑 Frenar", use_container_width=True):
            st.session_state.reveal = True
            st.session_state.spinning = False

# Auto-revelar cuando termine la animación
if st.session_state.spinning and (time.time() - st.session_state.spin_start) >= (st.session_state.spin_duration + 0.1):
    st.session_state.reveal = True
    st.session_state.spinning = False

# -------- ARMAR CARRIL --------
base_cycle = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]
scroll = []

# siempre mostramos un carril largo (para que vuele rápido)
for _ in range(14):
    scroll.extend(base_cycle)

# si ya hay premio decidido, agregamos final al centro
final = st.session_state.final_prize
if final:
    scroll.extend(["15% OFF","20% OFF","10% OFF","Seguí participando"])
    scroll.append(final)

# calcular desplazamiento para centrar el final
if final:
    stop_index = len(scroll) - 1
    top_index  = stop_index - CENTER_IDX
    st.session_state.target_px = max(0, top_index * ITEM_H)
else:
    st.session_state.target_px = 0

target_px = st.session_state.target_px
seed      = st.session_state.spin_seed
duration  = st.session_state.spin_duration  # segundos

colors = {
    "25% OFF": ("#ff3b3b", "rgba(255,59,59,.45)"),
    "20% OFF": ("#ff8c00", "rgba(255,140,0,.45)"),
    "15% OFF": ("#ffd60a", "rgba(255,214,10,.45)"),
    "10% OFF": ("#2ecc71", "rgba(46,204,113,.45)"),
    "Seguí participando": ("#5fa8d3", "rgba(95,168,211,.45)"),
}
DEFAULT_COL = ("#dddddd", "rgba(255,255,255,.25)")

def slot_html(items, target_px, seed, animate):
    style = f"""
    <style>
      .slot-wrap {{
        display:flex; flex-direction:column; align-items:center; gap:12px; margin:20px 0;
      }}
      .slot-window {{
        width: 560px; max-width: 96vw; height: {ITEM_H*VISIBLE_ROWS}px;
        overflow:hidden; border-radius:16px;
        background:#0f0f12; border:2px solid rgba(255,255,255,.08);
        position:relative; box-shadow:0 14px 36px rgba(0,0,0,.35), inset 0 0 30px rgba(255,255,255,.06);
      }}
      .slot-track {{
        position:absolute; left:0; right:0; top:0;
        display:flex; flex-direction:column; align-items:center;
        transform: translateY(0);
        {"animation: spin-"+str(seed)+f" {duration}s cubic-bezier(.12,.82,.16,1) forwards;" if animate else ""}
      }}
      .slot-item {{
        height:{ITEM_H}px; line-height:{ITEM_H}px;
        font-size:46px; font-weight:900; letter-spacing:.3px;
        color:#ddd; text-shadow:0 0 14px rgba(255,255,255,.2);
      }}
      .slot-window:before, .slot-window:after {{
        content:""; position:absolute; left:0; right:0; height:{ITEM_H}px; z-index:2;
        background:linear-gradient(to bottom, rgba(15,15,18,1) 0%, rgba(15,15,18,0) 100%);
        pointer-events:none;
      }}
      .slot-window:before {{ top:0; transform:rotate(180deg); }}
      .slot-window:after {{ bottom:0; }}
      .center-line {{
        position:absolute; left:0; right:0; top:{ITEM_H}px; height:{ITEM_H}px; z-index:3;
        border-top:1px solid rgba(255,255,255,.08); border-bottom:1px solid rgba(255,255,255,.08);
        box-shadow: inset 0 0 24px rgba(255,255,255,.04);
        pointer-events:none;
      }}
      @keyframes spin-{seed} {{
        0%   {{ transform: translateY(0); }}
        80%  {{ transform: translateY(-{int(target_px*0.90)}px); }}
        100% {{ transform: translateY(-{target_px}px); }}
      }}
    </style>
    """
    def item_div(text):
        col, glow = colors.get(text, DEFAULT_COL)
        return f'<div class="slot-item" style="color:{col}; text-shadow:0 0 16px {glow};">{text}</div>'

    items_html = "".join(item_div(t) for t in items) if final else \
                 (item_div("— — —") + item_div("— Tocá GIRAR —") + item_div("— — —"))

    body = f"""
      <div class="slot-wrap">
        <div class="slot-window">
          <div class="center-line"></div>
          <div class="slot-track">{items_html}</div>
        </div>
      </div>
    """
    return style + body

# animar solo cuando se presionó GIRAR (y aún no revelamos)
animate = bool(final) and not st.session_state.reveal
components.html(
    slot_html(scroll, target_px, seed, animate=animate),
    height=ITEM_H*VISIBLE_ROWS + 40,
    scrolling=False
)

# -------- RESULTADO (solo después de revelar) --------
if st.session_state.reveal and final:
    if final == "Seguí participando":
        st.info("😅 Te tocó **Seguí participando**. ¡Probá de nuevo más tarde!")
    else:
        st.success(f"🎉 ¡Ganaste {final}!")
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
                        "premio": final,
                        "cupon": COUPONS[final],
                        "periodo": current_period()
                    }
                    try:
                        r = requests.post(WEB_APP_URL, json=payload, timeout=15)
                        r.raise_for_status()
                        res = r.json()
                        if res.get("status") == "ya_participo":
                            st.error("⚠️ Este correo ya participó.")
                        elif res.get("status") in ["ok", "success"]:
                            st.success("✅ ¡Listo! Revisá tu correo, te mandamos el cupón 🎁")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")



