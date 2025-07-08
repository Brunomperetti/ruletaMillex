import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Reset y base */
    html, body, [class*="css"] {
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif;
    }
    
    /* Título principal */
    .title-container {
        background: #ce1f2d;
        padding: 20px 0;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    /* Contenedor de la ruleta */
    .ruleta-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #000;
        height: 70vh;
        padding: 20px 0;
    }
    
    /* Estilos del expander del formulario */
    .st-expander {
        background: #ce1f2d;
        border: none !important;
        border-radius: 0 !important;
        margin: 0 !important;
    }
    
    .st-expanderHeader {
        background: #ce1f2d !important;
        color: white !important;
        font-size: 1.5rem !important;
        padding: 15px 20px !important;
    }
    
    .st-expanderHeader:hover {
        background: #b51a27 !important;
    }
    
    .st-expanderContent {
        background: white;
        padding: 25px;
    }
    
    /* Campos del formulario */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stMultiselect>div>div>div {
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Labels en rojo */
    .stTextInput label, .stSelectbox label,
    .stMultiselect label, .stRadio label {
        color: #ce1f2d !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    
    /* Botón de enviar */
    .stButton>button {
        background: #ce1f2d !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 20px !important;
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        background: #b51a27 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Radio buttons */
    .stRadio>div {
        flex-direction: row !important;
        gap: 30px !important;
    }
    
    /* Columnas del formulario */
    .stForm {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# Contenedor de la ruleta
st.markdown('<div class="ruleta-container">', unsafe_allow_html=True)
components.html("""
    <iframe src="https://wheelofnames.com/es/vug-z3k" width="700" height="700" style="border:none;"></iframe>
""", height=720)
st.markdown('</div>', unsafe_allow_html=True)

# Formulario desplegable (siempre visible)
with st.expander("📝 CARGAR DATOS DEL GANADOR", expanded=True):  # Cambiado a expanded=True
    with st.form(key='formulario_ganador'):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre y apellido*", key='nombre')
            razon_social = st.text_input("Razón social*", key='razon_social')
            whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...", key='whatsapp')
            
        with col2:
            tipo_cliente = st.selectbox("Tipo de cliente*", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"], key='tipo_cliente')
            provincia = st.selectbox("Provincia*", ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Otra"], key='provincia')
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"], key='cliente_tipo', horizontal=True)
        
        premio = st.selectbox("Premio ganado*", ["", "10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento", "Seguí participando"], key='premio')
        
        submit_button = st.form_submit_button("ENVIAR Y GUARDAR DATOS")
        
        if submit_button:
            if nombre and razon_social and whatsapp and premio:
                st.success("Datos enviados correctamente!")
            else:
                st.warning("Por favor complete todos los campos obligatorios (*)")
