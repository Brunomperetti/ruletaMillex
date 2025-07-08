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
    "ACCESORIOS DE LIMPIEZA", "ACCESORIOS DE PELUQUERIA IMPOR", 
    # ... (todas las demás categorías que proporcionaste)
]

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Eliminar espacios no deseados */
    header, footer {visibility: hidden;}
    .block-container {padding: 0; margin: 0; max-width: 100%;}
    .stApp {background: #f0f2f6;}
    
    /* Título centrado y con mejor diseño */
    .title-container {
        background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
        padding: 20px 0;
        text-align: center;
        color: white;
        font-family: 'Arial Black', sans-serif;
        font-size: 2.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-bottom: 4px solid #4a148c;
    }
    
    /* Contenedor de la ruleta perfectamente centrado */
    .ruleta-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #000;
        padding: 40px 0;
        margin: 0 auto;
        width: 100%;
    }
    
    .ruleta-container {
        width: 800px;
        height: 800px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Mejoras para el formulario */
    .form-container {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 30px auto;
        max-width: 900px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .form-title {
        color: #6e48aa;
        font-size: 1.8rem;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 28px;
        width: 100%;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(110, 72, 170, 0.4);
    }
    
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stMultiselect>div>div>div {
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #ddd;
    }
    
    /* Eliminar scroll no deseado */
    html, body, [class*="css"]  {
        overflow-x: hidden;
    }
    
    /* Mejorar los radio buttons */
    .stRadio>div {
        flex-direction: row;
        gap: 20px;
    }
    
    .stRadio>div>label {
        margin-left: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# 🎡 Ruleta embebida perfectamente centrada
st.markdown('<div class="ruleta-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="ruleta-container">', unsafe_allow_html=True)
components.html("""
    <iframe src="https://wheelofnames.com/es/vug-z3k" width="800" height="800" style="border:none;"></iframe>
""", height=800, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📋 Formulario mejorado
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<div class="form-title">🎁 Cargar datos del ganador</div>', unsafe_allow_html=True)

with st.form("formulario", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre y apellido*", help="Nombre completo del ganador")
        razon = st.text_input("Razón social*", help="Nombre del negocio o empresa")
        whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...", help="Ejemplo: +5491123456789")
        cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"])
        
    with col2:
        tipo_cliente = st.selectbox("Tipo de cliente*", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"])
        provincia = st.selectbox("Provincia*", PROVINCIAS_ARGENTINA)
        interes = st.multiselect("Interés principal", INTERESES, help="Seleccione los intereses principales del cliente")
    
    categoria_productos = st.multiselect("Categorías de productos que maneja", CATEGORIAS_PRODUCTOS, help="Seleccione las categorías relevantes")
    marcas = st.multiselect("Marcas de interes", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
    premio = st.selectbox("Premio ganado*", ["", "10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento", "Seguí participando"])
    
    enviar = st.form_submit_button("ENVIAR Y GUARDAR DATOS")
    
    if enviar:
        if nombre and razon and whatsapp and premio and provincia:
            datos = {
                "nombre": nombre,
                "razonSocial": razon,
                "whatsapp": whatsapp,
                "clienteTipo": cliente_tipo,
                "tipoCliente": tipo_cliente,
                "provincia": provincia,
                "interes": ", ".join(interes) if interes else "",
                "categoriaProductos": ", ".join(categoria_productos) if categoria_productos else "",
                "marcas": ", ".join(marcas) if marcas else "",
                "premio": premio
            }
            
            try:
                headers = {'Content-Type': 'application/json'}
                respuesta = requests.post(WEB_APP_URL, json=datos, headers=headers)
                respuesta.raise_for_status()
                
                try:
                    respuesta_json = respuesta.json()
                    if respuesta_json.get("status") in ["success", "ok"]:
                        mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste: *{premio}*. Presentá este mensaje para canjearlo."
                        whatsapp_limpio = whatsapp.strip().replace(" ", "").replace("-", "")
                        link = f"https://wa.me/{whatsapp_limpio}?text={urllib.parse.quote(mensaje)}"
                        st.success("✅ Datos guardados correctamente!")
                        st.markdown(f"[📱 Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {respuesta_json.get('message', 'Error desconocido')}")
                except ValueError:
                    st.error("❌ La respuesta no es JSON válido.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error de conexión: {str(e)}")
        else:
            st.warning("⚠️ Por favor completa todos los campos obligatorios (*)")

st.markdown('</div>', unsafe_allow_html=True)

