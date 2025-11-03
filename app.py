import random
import requests
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------- CONFIG ----------
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw-M2XeKCLCL49Egk7LX4y3TmXh7A-OKqxAaXjOubrUG-6I8MJlWSOvS5S-IVR0uMOs/exec"

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
ANIMATION_DURATION = 10.0  # segundos

st.set_page_config(page_title="Cyber Monday - Millex", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
<div style="text-align:center;font-weight:900;font-size:42px;line-height:1.15;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO MILLEX
</div>
<p style="text-align:center;color:#8a8a8a;">Ingresá tu mail para jugar. Gira ~10s, desacelera y frena solo. Al frenar se revela tu premio ✨</p>
""", unsafe_allow_html=True)

def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    return hoy.strftime("%B de %Y").capitalize()

# ---------- STATE ----------
st.session_state.setdefault("email", "")
st.session_state.setdefault("ya_jugo", False)
st.session_state.setdefault("final_prize", None)
st.session_state.setdefault("spin_seed", 0)
st.session_state.setdefault("revealed", False)
st.session_state.setdefault("target_px", 0)
st.session_state.setdefault("mail_sent", False)

# ---------- FORM EMAIL ----------
with st.form("email_form_inicio", clear_on_submit=False):
    email_input = st.text_input("📧 Ingresá tu email para jugar*", placeholder="tu@correo.com")
    confirmar = st.form_submit_button("✅ Confirmar email")
    if confirmar:
        if not email_input or "@" not in email_input:
            st.error("Por favor ingresá un email válido.")
        else:
            try:
                r = requests.post(WEB_APP_URL, json={"accion":"check_email","email":email_input.strip()}, timeout=12)
                r.raise_for_status()
                res = r.json()
                st.session_state.email = email_input.strip()
                if res.get("status") == "ya_participo":
                    st.session_state.ya_jugo = True
                    st.error("⚠️ Este correo ya jugó. Solo se permite una vez.")
                elif res.get("status") == "libre":
                    st.session_state.ya_jugo = False
                    st.success("✅ ¡Listo! Ya podés jugar.")
                else:
                    st.error("❌ No se pudo validar el correo.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error de conexión: {e}")

# ---------- SLOT ----------
if st.session_state.email and not st.session_state.ya_jugo:
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        disabled_state = bool(not st.session_state.revealed and st.session_state.final_prize)
        if st.button("🎯 ¡GIRAR!", use_container_width=True, disabled=disabled_state):
            st.session_state.final_prize = pick_prize()
            st.session_state.spin_seed  += 1
            st.session_state.revealed    = False
            st.session_state.mail_sent   = False

    final = st.session_state.final_prize
    seed  = st.session_state.spin_seed

    # carril
    base_cycle = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]
    scroll = []
    for _ in range(16):
        scroll.extend(base_cycle)
    if final:
        scroll.extend(["15% OFF", "20% OFF", "10% OFF", "Seguí participando"])
        scroll.append(final)

    if final:
        stop_index = len(scroll) - 1
        top_index  = stop_index - CENTER_IDX
        st.session_state.target_px = max(0, top_index * ITEM_H)
    else:
        st.session_state.target_px = 0

    target_px = st.session_state.target_px

    colors = {
        "25% OFF": ("#ff3b3b", "rgba(255,59,59,.45)"),
        "20% OFF": ("#ff8c00", "rgba(255,140,0,.45)"),
        "15% OFF": ("#ffd60a", "rgba(255,214,10,.45)"),
        "10% OFF": ("#2ecc71", "rgba(46,204,113,.45)"),
        "Seguí participando": ("#5fa8d3", "rgba(95,168,211,.45)"),
    }
    DEFAULT_COL = ("#dddddd", "rgba(255,255,255,.25)")

    def slot_html(items, target_px, seed, animate: bool):
        dur = ANIMATION_DURATION
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
            {"animation: spin-"+str(seed)+f" {dur}s cubic-bezier(.22,.61,.36,1) forwards;" if animate else ""}
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
          /* Desaceleración suave SIN rebotes ni overshoot */
          @keyframes spin-{seed} {{
            0%   {{ transform: translateY(0); }}
            15%  {{ transform: translateY(-{int(target_px*0.55)}px); }}
            45%  {{ transform: translateY(-{int(target_px*0.80)}px); }}
            70%  {{ transform: translateY(-{int(target_px*0.92)}px); }}
            85%  {{ transform: translateY(-{int(target_px*0.97)}px); }}
            93%  {{ transform: translateY(-{int(target_px*0.985)}px); }}
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
            items_html = item_div("— — —") + item_div("— Tocá GIRAR —") + item_div("— — —")

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

        return f"""
        {style}
        <div class="slot-wrap">
          <div class="slot-window">
            <div class="center-line"></div>
            <div class="slot-track">{items_html}</div>
          </div>
        </div>
        {end_signal}
        """

    animate_now = bool(st.session_state.final_prize) and not st.session_state.revealed
    done = components.html(
        slot_html(scroll, target_px, seed, animate=animate_now),
        height=ITEM_H*VISIBLE_ROWS + 40,
        scrolling=False
    )

    if done == 'done' and st.session_state.final_prize and not st.session_state.revealed:
        st.session_state.revealed = True
        st.experimental_rerun()

    # Resultado + envío (una vez) y bloqueo
    if st.session_state.revealed and st.session_state.final_prize:
        final = st.session_state.final_prize
        if final == "Seguí participando":
            st.info("😅 Te tocó **Seguí participando**. ¡Gracias por jugar!")
            st.session_state.ya_jugo = True
        else:
            st.success(f"🎉 ¡Ganaste {final}!")
            if not st.session_state.mail_sent:
                try:
                    payload = {
                        "accion": "enviar_email_cybermonday",
                        "email": st.session_state.email,
                        "premio": final,
                        "cupon": COUPONS[final],
                        "periodo": current_period()
                    }
                    r = requests.post(WEB_APP_URL, json=payload, timeout=20)
                    r.raise_for_status()
                    res = r.json()
                    if res.get("status") == "ya_participo":
                        st.warning("⚠️ Este correo ya había jugado (no se volvió a enviar).")
                        st.session_state.ya_jugo = True
                    elif res.get("status") in ["ok", "success"]:
                        st.success("✅ ¡Listo! Te enviamos el cupón por mail 🎁")
                        st.session_state.mail_sent = True
                        st.session_state.ya_jugo = True
                    else:
                        st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error de conexión: {e}")


