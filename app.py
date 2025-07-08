import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide", initial_sidebar_state="collapsed")

# URL de Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxg1j5w57os20mywlO0Kup-kqMxfnCuIeTbJBcSqJFGPizKVls1xp5WErH0K_yKypMQ/exec"

# Listas de opciones
PROVINCIAS_ARGENTINA = [
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", 
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", 
    "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", 
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
    "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

INTERESES = ["Perro", "Gato", "Roedores", "Aves", "Acuario"]

CATEGORIAS_PRODUCTOS = [
    "ACCESORIOS DE LIMPIEZA", "ACCESORIOS DE PELUQUERIA IMPOR", "ACCESORIOS IMPOR. P/PAJAROS -A",
    # ... (mantener el resto de categorías igual)
]

# Estilos CSS personalizados (VERSIÓN CORREGIDA)
st.markdown("""
<style>
/* Reset general - Texto NEGRO en todo */
* {
    color: #000000 !important;
}

/* Estructura principal */
.stApp {
    background: #f5f5f5;
    font-family: Arial, sans-serif;
}

/* Título */
.title-container {
    background: white;
    padding: 15px;
    text-align: center;
    font-family: 'Arial Black', sans-serif;
    font-size: 2.5rem;
    border-bottom: 2px solid black;
    margin-bottom: 0;
}

/* Contenedor de la ruleta - AHORA VISIBLE */
.ruleta-container {
    background: black;
    height: 60vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    margin: 0 auto;
}

.ruleta-frame {
    width: 600px;
    height: 600px;
    border: none;
}

/* Formulario - Texto negro sobre blanco */
.stTextInput input,
.stSelectbox select,
.stMultiselect div,
.stRadio span,
.stTextArea textarea {
    color: #000000 !important;
    background: #ffffff !important;
    border: 1px solid #888 !important;
}

/* Labels del formulario */
.stTextInput label,
.stSelectbox label,
.stMultiselect label,
.stRadio label,
.stTextArea label {
    color: #000000 !important;
    font-weight: bold;
}

/* Dropdowns visibles */
.st-bd, .st-be, .st-bf, .st-bg {
    background: white !important;
    color: black !important;
}

/* Radio buttons */
.stRadio [role="radiogroup"] {
    background: white;
}

.stRadio [role="radiogroup"] label {
    color: black !important;
}

/* Botón de enviar */
.stButton>button {
    background: #000000 !important;
    color: #ffffff !important;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* Expander - Fondo blanco */
.st-emotion-cache-1h9us2l {
    background: white !important;
    border: 1px solid black !important;
}

.st-emotion-cache-5rimss {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# --- ESTRUCTURA DE LA APLICACIÓN ---
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# RUELA (ahora visible)
st.markdown("""
<div class="ruleta-container">
    <iframe class="ruleta-frame" src="https://wheelofnames.com/es/vug-z3k"></iframe>
</div>
""", unsafe_allow_html=True)

# FORMULARIO (con estilos corregidos)
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    with st.form("formulario"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre y apellido*")
            razon = st.text_input("Razón social*")
            whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...")
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"])
            
        with col2:
            tipo_cliente = st.selectbox("Tipo de cliente*", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"])
            provincia = st.selectbox("Provincia*", PROVINCIAS_ARGENTINA)
            interes = st.multiselect("Segmento de interés", INTERESES)
        
        categoria_productos = st.multiselect("Categorías de productos interesado", CATEGORIAS_PRODUCTOS)
        premio = st.selectbox("Premio ganado*", ["", "10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento"])
        
        if st.form_submit_button("ENVIAR Y GUARDAR DATOS"):
            if nombre and razon and whatsapp and premio:
                # (Mantener la lógica de envío del formulario)
                st.success("Datos enviados correctamente!")

# --- FIN DEL CÓDIGO ---
