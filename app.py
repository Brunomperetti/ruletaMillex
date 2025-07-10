import streamlit as st 
import streamlit.components.v1 as components
import urllib.parse
import requests
from datetime import datetime

# URL de tu Apps Script
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
    # ... (resto de categorías permanece igual)
]

# Estilos CSS personalizados (permanece igual)
st.markdown("""
<style>
/* Tus estilos CSS aquí */
</style>
""", unsafe_allow_html=True)

# Estructura principal
st.markdown("""
<div class="main-container">
    <div class="title-container">RULETA MÁGICA MILLEX</div>
    <div class="ruleta-container">
        <iframe class="ruleta-frame" src="https://wheelofnames.com/es/vug-z3k"></iframe>
    </div>
""", unsafe_allow_html=True)

# Formulario desplegable
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    st.markdown('<div class="form-content">', unsafe_allow_html=True)
    
    with st.form("formulario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre y apellido")
            razon = st.text_input("Razón social")
            fantasia = st.text_input("Nombre de fantasía")
            cuil_cuit = st.text_input("Número de CUIL o CUIT")
            whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?", ["Nuevo", "Actual"], index=0)
            estrella = st.checkbox("⭐ Marcar como cliente estrella")
            
        with col2:
            tipo_cliente = st.selectbox("Tipo de cliente", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"], index=0)
            provincia = st.selectbox("Provincia", PROVINCIAS_ARGENTINA, index=0)
            interes = st.multiselect("Interés principal", INTERESES)
        
        categoria_productos = st.multiselect("Categorías de productos que maneja", CATEGORIAS_PRODUCTOS)
        marcas = st.multiselect("Marcas que maneja", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
        premio = st.selectbox("Premio ganado", ["", "10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento", "Seguí participando"], index=0)
        
        enviar = st.form_submit_button("ENVIAR Y GUARDAR DATOS")
        
        if enviar:
            # Obtener fecha y hora actual
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Preparar datos para enviar
            datos = {
                "Nombre y Apellido": nombre if nombre else "",
                "Razon Social": razon if razon else "",
                "Nombre Fantasía": fantasia if fantasia else "",
                "CUIL/CUIT": cuil_cuit if cuil_cuit else "",
                "whatsapp": whatsapp if whatsapp else "",
                "Cliente Tipo": cliente_tipo if cliente_tipo else "",
                "Cliente Estrella": "Sí" if estrella else "No",
                "Tipo Cliente": tipo_cliente if tipo_cliente else "",
                "Provincia": provincia if provincia else "",
                "Interés Principal": ", ".join(interes) if interes else "",
                "Categorías Productos": ", ".join(categoria_productos) if categoria_productos else "",
                "Marcas": ", ".join(marcas) if marcas else "",
                "premio ganado": premio if premio else "",
                "Fecha y hora": fecha_hora
            }
            
            try:
                headers = {'Content-Type': 'application/json'}
                respuesta = requests.post(WEB_APP_URL, json=datos, headers=headers)
                respuesta.raise_for_status()
                
                try:
                    respuesta_json = respuesta.json()
                    if respuesta_json.get("status") in ["success", "ok"]:
                        if nombre and premio and premio != "Seguí participando":
                            mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste: *{premio}*. Presentá este mensaje para canjearlo."
                            whatsapp_limpio = whatsapp.strip().replace(" ", "").replace("-", "")
                            if whatsapp_limpio:
                                link = f"https://wa.me/{whatsapp_limpio}?text={urllib.parse.quote(mensaje)}"
                                st.markdown(f"[📱 Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                        st.success("✅ Datos guardados correctamente!")
                    else:
                        st.error(f"❌ Error: {respuesta_json.get('message', 'Error desconocido')}")
                except ValueError:
                    st.error("❌ La respuesta no es JSON válido.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error de conexión: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

