import streamlit as st 
import streamlit.components.v1 as components
import urllib.parse
import requests

# URL actualizada de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxg1j5w57os20mywlO0Kup-kqMxfnCuIeTbJBcSqJFGPizKVls1xp5WErH0K_yKypMQ/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide", initial_sidebar_state="collapsed")

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
    "ACCESORIOS IMPORTADOS P/PAJARO", "ACCESORIOS PARA ROEDORES", "ACCESORIOS VARIOS ACUARIO",
    "ACCESORIOS VARIOS P/GATOS", "ACCESORIOS VARIOS P/PERROS", "ADORNOS CON MOVIMIENTO",
    # ... (resto de categorías)
]

# Estilos CSS personalizados
st.markdown("""
<style>
html, body, [class*="css"] {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    font-family: Arial, sans-serif !important;
    color: #000000 !important;
}
header, footer {visibility: hidden; height: 0;}
.block-container {padding: 0; margin: 0 auto; max-width: 900px;}
.stApp {background: #f5f5f5; padding: 0 !important;}
.title-container {
    background: #ffffff;
    padding: 15px;
    text-align: center;
    color: #000000 !important;
    font-family: 'Arial Black', sans-serif;
    font-size: 2.5rem;
    border-bottom: 2px solid #000000;
}
</style>
""", unsafe_allow_html=True)

# Estructura principal
st.markdown("""
<div class="main-container">
    <div class="title-container">RULETA MÁGICA MILLEX</div>
""", unsafe_allow_html=True)

# Formulario desplegable
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    with st.form("formulario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre y apellido*")
            razon = st.text_input("Razón social*")
            fantasia = st.text_input("Nombre de fantasía")
            cuil_cuit = st.text_input("Número de CUIL o CUIT")
            whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...")
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"])
            estrella = st.checkbox("⭐ Marcar como cliente estrella")
            
        with col2:
            tipo_cliente = st.selectbox("Tipo de cliente*", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"])
            provincia = st.selectbox("Provincia*", PROVINCIAS_ARGENTINA)
            interes = st.multiselect("Interés principal", INTERESES)
            
        categoria_productos = st.multiselect("Categorías de productos que maneja", CATEGORIAS_PRODUCTOS)
        marcas = st.multiselect("Marcas que maneja", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
        premio = st.selectbox("Premio ganado*", ["", "10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento", "Seguí participando"])
        
        enviar = st.form_submit_button("ENVIAR Y GUARDAR DATOS")
        
        if enviar:
            if nombre and razon and whatsapp and premio and provincia:
                datos = {
                    "Nombre y Apellido": nombre,
                    "Razon Social": razon,
                    "Nombre Fantasía": fantasia,
                    "CUIL/CUIT": cuil_cuit,
                    "whatsapp": whatsapp,
                    "Cliente Tipo": cliente_tipo,
                    "Cliente Estrella": "SI" if estrella else "NO",
                    "Tipo Cliente": tipo_cliente,
                    "Provincia": provincia,
                    "Interés Principal": ", ".join(interes) if interes else "",
                    "Categorías Productos": ", ".join(categoria_productos) if categoria_productos else "",
                    "Marcas": ", ".join(marcas) if marcas else "",
                    "premio ganado": premio
                }

                try:
                    headers = {'Content-Type': 'application/json'}
                    respuesta = requests.post(WEB_APP_URL, json=datos, headers=headers)
                    respuesta.raise_for_status()
                    
                    respuesta_json = respuesta.json()
                    if respuesta_json.get("status") in ["success", "ok"]:
                        mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste: *{premio}*. Presentá este mensaje para canjearlo."
                        whatsapp_limpio = whatsapp.strip().replace(" ", "").replace("-", "")
                        link = f"https://wa.me/{whatsapp_limpio}?text={urllib.parse.quote(mensaje)}"
                        st.success("✅ Datos guardados correctamente!")
                        st.markdown(f"[📱 Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {respuesta_json.get('message', 'Error desconocido')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
            else:
                st.warning("⚠️ Por favor completa todos los campos obligatorios (*)")

st.markdown('</div>', unsafe_allow_html=True)

