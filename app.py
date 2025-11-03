import streamlit as st
import requests
import random

# URL de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx7_601m55rWtXtKhayUah2iWRsjqc--4-AfxJMZYhxpGpbtSXeoje2uq5G363zcb8z/exec"

st.set_page_config(page_title="Cyber Monday - Ruleta Millex", layout="centered", initial_sidebar_state="collapsed")

st.markdown('<div style="text-align:center;font-size:38px;font-weight:800;">🛍️ CYBER MONDAY • RULETA MÁGICA</div>', unsafe_allow_html=True)
st.caption("Girás, ves tu premio y lo recibís por mail. ¡Así de simple!")

# --- Configurá premios y probabilidades (opcional) ---
PREMIOS = ["25% OFF", "20% OFF", "15% OFF", "10% OFF", "Seguí participando"]
PESOS   = [5,          12,         18,         25,        40]  # suma libre; random.choices normaliza

# Estado de sesión
if "premio" not in st.session_state:
    st.session_state.premio = None

# Botón ruleta
sp_col = st.container()
with sp_col:
    girar = st.button("🎯 GIRAR LA RULETA", use_container_width=True)
    if girar:
        st.session_state.premio = random.choices(PREMIOS, weights=PESOS, k=1)[0]
        st.balloons()

# Resultado + email
if st.session_state.premio:
    if st.session_state.premio == "Seguí participando":
        st.warning("¡Casi casi! Te tocó **Seguí participando**. Probá de nuevo 😊")
    else:
        st.success(f"🎉 ¡Tu premio es: **{st.session_state.premio}**!")
        with st.form("email_form", clear_on_submit=False):
            email = st.text_input("📧 Ingresá tu email para recibir el cupón*", placeholder="tu@correo.com")
            enviar = st.form_submit_button("✉️ Enviarme el cupón por mail", use_container_width=True)

            if enviar:
                if not email or "@" not in email:
                    st.error("Ingresá un email válido.")
                else:
                    try:
                        payload = {
                            "accion": "enviar_email_cybermonday",
                            "email": email.strip(),
                            "premio": st.session_state.premio
                        }
                        r = requests.post(WEB_APP_URL, json=payload, timeout=15)
                        r.raise_for_status()
                        res = r.json()
                        if res.get("status") in ["ok", "success"]:
                            st.success("✅ ¡Listo! Revisá tu correo: te enviamos el cupón.")
                        else:
                            st.error(f"❌ Error: {res.get('message','No se pudo enviar el mail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error de conexión: {e}")




