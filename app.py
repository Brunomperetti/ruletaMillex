import random
import requests
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------- CONFIG ----------
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

# Altura visual de cada fila y ventana
ITEM_H = 72
VISIBLE_ROWS = 3
CENTER_IDX = 1   # 0/1/2 (1 = centro visible)

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#8a8a8a;">Tocá GIRAR: gira ~20s, desacelera y frena solo. Al frenar se revela tu premio ✨</p>
""", unsafe_allow_html=True)

def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# ---------- STATE ----------
st.session_state.setdefault("final_prize", None)   # premio decidido
st.session_state.setdefault("spin_seed", 0)        # para regenerar keyframes
st.session_state.setdefault("revealed", False)     # ya terminó la animación?
st.session_state.setdefault("target_px", 0)        # desplazamiento final px

# ---------- BOTÓN GIRAR ----------
colA, colB, colC = st.columns([1,2,1])
with colB:
    if st.button("🎯 ¡GIRAR!", use_container_width=True, disabled=bool(st.session_state.final_prize and not st.session_state.revealed)):
        # Decide el premio (Python = fuente de verdad)
        st.session_state.final_prize = pick_prize()
        st.session_state.spin_seed  += 1
        st.session_state.revealed    = False   # se revelará al terminar la animación

final = st.session_state.final_prize
seed  = st.session_state.spin_seed

# ---------- ARMAR EL CARRIL (lista que se desplaza) ----------
base_cycle = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]
scroll = []

# Carril largo para 20s de animación
for _ in range(22):
    scroll.extend(base_cycle)

# Agregamos un poco de “suspenso” y el final como última fila
if final:
    scroll.extend(["15% OFF", "20% OFF", "10% OFF", "Seguí participando"])
    scroll.append(final)

# Calcular desplazamiento para que el FINAL quede centrado al frenar
if final:
    stop_index = len(scroll) - 1
    top_index  = stop_index - CENTER_IDX
    st.session_state.target_px = max(0, top_index * ITEM_H)
else:
    st.session_state.target_px = 0

target_px = st.session_state.target_px

# ---------- PALETA ----------
colors = {
    "25% OFF": ("#ff3b3b", "rgba(255,59,59,.45)"),
    "20% OFF": ("#ff8c00", "rgba(255,140,0,.45)"),
    "15% OFF": ("#ffd60a", "rgba(255,214,10,.45)"),
    "10% OFF": ("#2ecc71", "rgba(46,204,113,.45)"),
    "Seguí participando": ("#5fa8d3", "rgba(95,168,211,.45)"),
}
DEFAULT_COL = ("#dddddd", "rgba(255,255,255,.25)")

# ---------- HTML + CSS (20s con desaceleración y señal de fin hacia Python) ----------
def slot_html(items, target_px, seed, animate: bool):
    duration = 20.0  # segundos
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
        {"animation: spin-"+str(seed)+f" {duration}s linear forwards;" if animate else ""}
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
      .slot-window:after  {{ bottom:0; }}
      .center-line {{
        position:absolute; left:0; right:0; top:{ITEM_H}px; height:{ITEM_H}px; z-index:3;
        border-top:1px solid rgba(255,255,255,.08); border-bottom:1px solid rgba(255,255,255,.08);
        box-shadow: inset 0 0 24px rgba(255,255,255,.04);
        pointer-events:none;
      }}
      /* Desaceleración simulada con keyframes: grandes saltos al inicio, pasos cortos al final */
      @keyframes spin-{seed} {{
        0%   {{ transform: translateY(0); }}
        10%  {{ transform: translateY(-{int(target_px*0.55)}px); }}
        40%  {{ transform: translateY(-{int(target_px*0.82)}px); }}
        70%  {{ transform: translateY(-{int(target_px*0.92)}px); }}
        85%  {{ transform: translateY(-{int(target_px*0.965)}px); }}
        92%  {{ transform: translateY(-{int(target_px*0.985)}px); }}
        96%  {{ transform: translateY(-{int(target_px*0.994)}px); }}
        100% {{ transform: translateY(-{target_px}px); }}
      }}
    </style>
    """
    def item_div(text):
        col, glow = colors.get(text, DEFAULT_COL)
        return f'<div class="slot-item" style="color:{col}; text-shadow:0 0 16px {glow};">{text}</div>'

    if animate:
        items_html = "".join(item_div(t) for t in items)
    else:
        # Pantalla inicial sin resultado
        items_html = item_div("— — —") + item_div("— Tocá GIRAR —") + item_div("— — —")

    # JS: cuando termina la animación, enviamos 'done' a Streamlit para revelar el resultado
    end_signal = f"""
    <script>
      (function(){{
        const track = document.querySelector('.slot-track');
        if (track) {{
          track.addEventListener('animationend', function() {{
            window.parent.postMessage({{isStreamlitMessage:true, type:'streamlit:setComponentValue', value:'done'}}, '*');
          }});
        }}
      }})();
    </script>
    """ if animate else ""

    body = f"""
      <div class="slot-wrap">
        <div class="slot-window">
          <div class="center-line"></div>
          <div class="slot-track">{items_html}</div>
        </div>
      </div>
      {end_signal}
    """
    return style + body

# Render del slot; capturamos si terminó (value == 'done')
animate_now = bool(final) and not st.session_state.revealed
done = components.html(
    slot_html(scroll, target_px, seed, animate=animate_now),
    height=ITEM_H*VISIBLE_ROWS + 40,
    scrolling=False
)

if done == 'done' and final and not st.session_state.revealed:
    st.session_state.revealed = True
    st.rerun()

# ---------- RESULTADO + EMAIL (solo cuando terminó la animación) ----------
if st.session_state.revealed and final:
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
                        "cupon": COUPONS[final],          # cupón fijo (NO se muestra en pantalla)
                        "periodo": current_period()
                    }
                    try:
                        r = requests.post(WEB_APP_URL, json=payload, timeout=20)
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


