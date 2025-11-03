import time
import random
import requests
import streamlit as st
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

SPIN_SECONDS = 10.0  # duración total del giro (pedido)
TICK_MS = 45         # refresco de la “ruleta” (más chico = más fluido)

# ---------- PAGE ----------
st.set_page_config(page_title="Cyber Monday - Petsu", layout="centered")
st.markdown("""
<div style="text-align:center;font-weight:900;font-size:38px;line-height:1.15;margin-bottom:6px;">
🎰 CYBER MONDAY • SLOT MÁGICO PETSU (hasta 25% de descuento)
</div>
<p style="text-align:center;color:#8a8a8a;">Ingresá tu email para jugar. Gira ~10s, desacelera y frena una vez. Al frenar se revela tu premio ✨</p>
""", unsafe_allow_html=True)

# ---------- HELPERS ----------
def pick_prize():
    return random.choices(PRIZES, weights=WEIGHTS, k=1)[0]

def current_period():
    hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    # Ej: "Noviembre de 2025"
    return hoy.strftime("%B de %Y").capitalize()

def post_json(url, payload, timeout=15):
    """Envía JSON y devuelve dict (o lanza excepción legible)."""
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    try:
        return r.json()
    except Exception as e:
        raise RuntimeError(f"Respuesta no JSON: {r.text[:200]}") from e

# Colores por premio (para el slot)
COL = {
    "25% OFF": "#ff3b3b",
    "20% OFF": "#ff8c00",
    "15% OFF": "#ffd60a",
    "10% OFF": "#2ecc71",
    "Seguí participando": "#5fa8d3",
}

# ---------- STATE ----------
st.session_state.setdefault("email", "")
st.session_state.setdefault("ya_jugo", False)
st.session_state.setdefault("final_prize", None)
st.session_state.setdefault("mail_sent", False)

# ---------- EMAIL FIRST ----------
with st.form("email_form", clear_on_submit=False):
    email_in = st.text_input("📧 Ingresá tu email para jugar*", placeholder="tu@correo.com")
    ok = st.form_submit_button("✅ Confirmar email")
    if ok:
        if not email_in or "@" not in email_in:
            st.error("Ingresá un email válido.")
        else:
            st.session_state.email = email_in.strip()
            # chequear en backend si ya jugó
            try:
                res = post_json(WEB_APP_URL, {"accion": "check_email", "email": st.session_state.email}, timeout=12)
                if res.get("status") == "ya_participo":
                    st.session_state.ya_jugo = True
                    st.error("⚠️ Este correo ya jugó. Solo una vez por persona.")
                elif res.get("status") == "libre":
                    st.session_state.ya_jugo = False
                    st.success("✅ ¡Listo! Ya podés jugar.")
                else:
                    st.warning("No se pudo validar el correo. Probá de nuevo.")
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")

# ---------- SLOT (PYTHON-ONLY ANIMATION) ----------
if st.session_state.email and not st.session_state.ya_jugo:
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        spin_clicked = st.button("🎯 ¡GIRAR!", use_container_width=True, disabled=st.session_state.final_prize is not None and not st.session_state.mail_sent)

    # Si presiona GIRAR: 1) decide premio; 2) corre animación 10s; 3) revela y envía cupón
    if spin_clicked:
        st.session_state.final_prize = pick_prize()
        st.session_state.mail_sent = False

        # Preparamos una lista "infinita" de premios para ir ciclando visualmente
        reel = ["20% OFF", "15% OFF", "10% OFF", "Seguí participando", "25% OFF"]

        # Placeholder visual
        slot_box = st.empty()

        start = time.time()
        elapsed = 0.0
        steps = 0

        # Easing simétrico (suave) con curva cónica (easeInOutQuad)
        def ease(t):
            # t en [0,1] -> curva suave simétrica
            return 2*t*t if t < 0.5 else 1 - pow(-2*t + 2, 2)/2

        # Vamos cambiando el índice con velocidad que va bajando
        # Al principio avanza muchos items por tick, al final 1-item por tick
        current_idx = 0
        last_label = None

        while elapsed < SPIN_SECONDS:
            t = (time.time() - start) / SPIN_SECONDS
            t = max(0.0, min(1.0, t))
            speed = 12 * (1.0 - ease(t)) + 1.0  # 13 -> 1 items/tick (desacelera simétrico)

            # avanzamos "speed" posiciones
            current_idx = (current_idx + int(max(1, round(speed)))) % len(reel)
            label = reel[current_idx]

            # Dibujo del “slot” (una sola fila grande, look nítido)
            slot_box.markdown(f"""
            <div style="
                margin:18px auto;
                width: min(560px, 96vw);
                height: 88px;
                border-radius: 14px;
                border: 2px solid rgba(255,255,255,.09);
                background: #0f0f12;
                box-shadow: 0 12px 28px rgba(0,0,0,.35), inset 0 0 30px rgba(255,255,255,.06);
                display:flex; align-items:center; justify-content:center;">
              <div style="
                  font-size: 46px; font-weight: 900; letter-spacing: .3px;
                  color: {COL[label]}; text-shadow: 0 0 16px rgba(255,255,255,.15);">
                {label}
              </div>
            </div>
            """, unsafe_allow_html=True)

            last_label = label
            time.sleep(TICK_MS/1000.0)
            elapsed = time.time() - start
            steps += 1

        # Al terminar, mostramos el premio real elegido por Python
        prize = st.session_state.final_prize
        slot_box.markdown(f"""
        <div style="
            margin:18px auto;
            width: min(560px, 96vw);
            height: 88px;
            border-radius: 14px;
            border: 2px solid rgba(255,255,255,.12);
            background: #0f0f12;
            box-shadow: 0 12px 28px rgba(0,0,0,.35), inset 0 0 30px rgba(255,255,255,.06);
            display:flex; align-items:center; justify-content:center;">
          <div style="
              font-size: 46px; font-weight: 900; letter-spacing: .3px;
              color: {COL[prize]}; text-shadow: 0 0 16px rgba(255,255,255,.15);">
            🎉 {prize} 🎉
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Enviar cupón automáticamente al terminar (una sola vez)
        try:
            payload = {
                "accion": "enviar_email_cybermonday",
                "email": st.session_state.email,
                "premio": prize,
                "cupon": COUPONS[prize],
                "periodo": current_period()
            }
            res = post_json(WEB_APP_URL, payload, timeout=20)
            if res.get("status") == "ya_participo":
                st.warning("⚠️ Este correo ya había jugado.")
                st.session_state.ya_jugo = True
            elif res.get("status") in ["ok", "success"]:
                st.success("✅ ¡Listo! Te enviamos el cupón por mail 🎁")
                st.session_state.mail_sent = True
                st.session_state.ya_jugo = True
            else:
                st.error(f"❌ Error: {res.get('message', 'No se pudo enviar el mail')}")
        except Exception as e:
            st.error(f"❌ Error de conexión al enviar el mail: {e}")

# Si ya jugó, bloqueamos
if st.session_state.ya_jugo:
    st.info("🔒 Este correo ya usó su jugada.")


