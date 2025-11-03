import streamlit as st
import requests
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

# ---- CONFIG ----
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxjg_suWbXBwFhSDPxRLVrJLKLHUSOpBJL-YF2ny-qxiYRxgUkptW8lHfmAsfuU3KsR/exec"
PRIZES  = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
WEIGHTS = [5,          12,         18,          25,         40]
COUPONS = {
    "25% OFF": "CM25-ZX9R-TF8M",
    "20% OFF": "CM20-VK6R-3BZ4",
    "15% OFF": "CM15-GQ8D-PN7X",
    "10% OFF": "CM10-LW5C-HR3T",
    "Seguí participando": "CM00-TRYA-GAIN"
}

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#8a8a8a;">Tocá el botón, mirá cómo rota y frená en tu premio ✨</p>
""", unsafe_allow_html=True)

def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# ---- STATE ----
st.session_state.setdefault("final_prize", None)
st.session_state.setdefault("spin_seed", 0)  # fuerza recrear la animación

# ---- SPIN BUTTON ----
colA, colB, colC = st.columns([1,2,1])
with colB:
    if st.button("🎯 ¡GIRAR!", use_container_width=True):
        st.session_state.final_prize = pick_prize()
        st.session_state.spin_seed += 1

final = st.session_state.final_prize
seed  = st.session_state.spin_seed

# ---- BUILD THE REEL (determinístico) ----
ITEM_H = 72                    # altura de cada línea (coincide con CSS)
VISIBLE_ROWS = 3               # se ven 3 líneas (arriba/centro/abajo)
CENTER_IDX = 1                 # índice de la fila central visible (0,1,2) -> 1
base_cycle = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]

# armamos el scroll
scroll = []
for _ in range(10):            # vueltas “rápidas”
    scroll.extend(base_cycle)

if final:
    scroll.extend(base_cycle)
    # Un poquito de suspenso y terminamos con el final
    scroll.extend(["15% OFF","20% OFF","10% OFF","Seguí participando"])
    scroll.append(final)

# cuánto desplazarnos para que el FINAL quede centrado
if final:
    stop_index = len(scroll) - 1            # el final es el último item agregado
    top_index  = stop_index - CENTER_IDX    # índice del item que debe quedar arriba
    target_px  = max(0, top_index * ITEM_H)
else:
    target_px  = 0

# colores
colors = {
    "25% OFF": ("#ff3b3b", "rgba(255,59,59,.45)"),
    "20% OFF": ("#ff8c00", "rgba(255,140,0,.45)"),
    "15% OFF": ("#ffd60a", "rgba(255,214,10,.45)"),
    "10% OFF": ("#2ecc71", "rgba(46,204,113,.45)"),
    "Seguí participando": ("#5fa8d3", "rgba(95,168,211,.45)"),
}

def slot_html(items, target_px, seed, final_text):
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
        {"animation: spin-"+str(seed)+" 2.1s cubic-bezier(.18,.68,.22,1) forwards;" if final_text else ""}
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
        70%  {{ transform: translateY(-{int(target_px*0.86)}px); }}
        100% {{ transform: translateY(-{target_px}px); }}
      }}
    </style>
    """
    def item_div(text):
        col, glow = colors[text]
        return f'<div class="slot-item" style="color:{col}; text-shadow:0 0 16px {glow};">{text}</div>'

    if final_text:
        items_html = "".join(item_div(t) for t in items)
    else:
        items_html = item_div("— — —") + item_div("— — —") + item_div("— — —")

    body = f"""
      <div class="slot-wrap">
        <div class="slot-window">
          <div class="center-line"></div>
          <div class="slot-track">{items_html}</div>
        </div>
      </div>
    """
    return style + body

components.html(
    slot_html(scroll, target_px, seed, final_text=bool(final)),
    height=ITEM_H*VISIBLE_ROWS + 40,
    scrolling=False
)

# ---- RESULTADO + EMAIL (SIEMPRE COHERENTE CON 'final') ----
if final:
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
                        "cupon": COUPONS[final],          # cupón fijo correspondiente (NO se muestra)
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





