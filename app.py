import streamlit as st
import requests
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")

# ---------- UI ----------
st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:4px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#888;">Tocá el botón y mirá cómo gira la suerte ✨</p>
""", unsafe_allow_html=True)

# Premios y pesos
PRIZES = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
WEIGHTS = [5, 12, 18, 25, 40]

# Cupones fijos (NO se muestran)
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN"
}

def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# Estado
st.session_state.setdefault("final_prize", None)
st.session_state.setdefault("spin_seed", 0)  # fuerza reconstruir animación

# Botón
colA, colB, colC = st.columns([1,2,1])
with colB:
    if st.button("🎯 ¡GIRAR!", use_container_width=True):
        st.session_state.final_prize = pick_prize()
        st.session_state.spin_seed += 1

# ---------- SLOT ANIMADO (CSS PURO, SIN JS NI postMessage) ----------
final = st.session_state.final_prize

# Construimos una lista de “scroll” y terminamos con el premio final alineado al centro
# Dimensiones (coinciden con CSS)
ITEM_H = 70  # px alto visible por ítem
VISIBLE_CENTER_INDEX = 6  # en qué fila queremos que quede el final (para centrar bonito)

# Secuencia visual: varias vueltas “fake” + final al centro
base_cycle = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]
scroll = []
for _ in range(9):  # velocidad visual
    scroll.extend(base_cycle)

if final:
    # colocamos varias "dummies" y aseguramos que la última línea visible sea el final
    scroll.extend(base_cycle)
    # armamos para que el 'final' quede en la posición VISIBLE_CENTER_INDEX desde arriba
    scroll.extend(random.sample(base_cycle, k=len(base_cycle)))
    scroll.extend(["15% OFF","20% OFF","10% OFF","Seguí participando"])  # un poco de suspenso
    scroll.append(final)  # último ítem es el que quedará centrado

# Altura a recorrer: total_items - VISIBLE_CENTER_INDEX - 1
total_items = len(scroll)
if final and total_items > 0:
    stop_index = total_items - 1  # última fila es el final
    target_rows = stop_index - VISIBLE_CENTER_INDEX
    target_px = max(0, target_rows * ITEM_H)
else:
    target_px = 0

colors_map = {
    "25% OFF": ("#ff3b3b", "rgba(255,59,59,.45)"),
    "20% OFF": ("#ff8c00", "rgba(255,140,0,.45)"),
    "15% OFF": ("#ffd60a", "rgba(255,214,10,.45)"),
    "10% OFF": ("#2ecc71", "rgba(46,204,113,.45)"),
    "Seguí participando": ("#3498db", "rgba(52,152,219,.45)"),
}

def slot_html(scroll_items, target_px, seed):
    # estilos
    style = f"""
    <style>
    .slot-wrap {{
      display:flex; flex-direction:column; align-items:center; gap:14px; margin:22px 0;
    }}
    .slot-window {{
      width: 560px; max-width: 95vw; height: {ITEM_H * 3}px;
      overflow: hidden; border-radius: 16px;
      border: 3px solid #111; background: #0d0d0d;
      box-shadow: 0 14px 32px rgba(0,0,0,.35), inset 0 0 30px rgba(255,255,255,.06);
      position: relative;
    }}
    .slot-track {{
      position:absolute; left:0; top:0; right:0;
      display:flex; flex-direction:column; align-items:center;
      padding: 0; margin:0;
      transform: translateY(0);
      {"animation: spin-"+str(seed)+" 2.2s cubic-bezier(.15,.65,.18,1.0) forwards;" if final else ""}
    }}
    .slot-item {{
      height: {ITEM_H}px; line-height: {ITEM_H}px;
      font-size: 46px; font-weight: 900; letter-spacing: .5px;
      color:#eee; text-shadow: 0 0 14px rgba(255,255,255,.25);
    }}
    .slot-window:before, .slot-window:after {{
      content:""; position:absolute; left:0; right:0; height: {ITEM_H}px;
      background: linear-gradient(to bottom, rgba(13,13,13,1) 0%, rgba(13,13,13,0) 100%);
      z-index:2; pointer-events:none;
    }}
    .slot-window:before {{ top:0; transform: rotate(180deg); }}
    .slot-window:after {{ bottom:0; }}
    .center-line {{
      position:absolute; left:0; right:0; top: {ITEM_H}px; height: {ITEM_H}px;
      border-top: 2px solid rgba(255,255,255,.1);
      border-bottom: 2px solid rgba(255,255,255,.1);
      z-index:3; pointer-events:none;
    }}
    @keyframes spin-{seed} {{
      0%   {{ transform: translateY(0); }}
      65%  {{ transform: translateY(-{int(target_px*0.85)}px); }}
      100% {{ transform: translateY(-{target_px}px); }}
    }}
    </style>
    """

    # items
    def item_div(text):
        col, glow = colors_map[text]
        return f'<div class="slot-item" style="color:{col}; text-shadow:0 0 16px {glow};">{text}</div>'

    items_html = "".join(item_div(t) for t in scroll_items) if final else (
        item_div("— — —") + item_div("— — —") + item_div("— — —")
    )

    body = f"""
    <div class="slot-wrap">
      <div class="slot-window">
        <div class="center-line"></div>
        <div class="slot-track">{items_html}</div>
      </div>
    </div>
    """
    return style + body

components.html(slot_html(scroll, target_px, st.session_state.spin_seed), height=260, scrolling=False)

# --------- Resultado + formulario (con envío de cupón por mail, sin mostrar el código) ----------
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
                        "cupon": COUPONS[prize],     # <- cupón fijo correspondiente (NO se muestra)
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





