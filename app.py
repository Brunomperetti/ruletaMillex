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
    "ACCESORIOS DE LIMPIEZA", "ACCESORIOS DE PELUQUERIA IMPOR", "ACCESORIOS IMPOR. P/PAJAROS -A", "ACCESORIOS IMPORTADOS P/PAJARO", "ACCESORIOS PARA ROEDORES", "ACCESORIOS VARIOS ACUARIO", "ACCESORIOS VARIOS P/GATOS", "ACCESORIOS VARIOS P/PERROS", "ADORNOS CON MOVIMIENTO", "AIREADORES BOYU", "AIREADORES SHANDA", "ALICATE P/ PERROS Y GATOS", "ARBOLES P/GATO", "BEBEDEROS PARA HAMSTER", "BEBEDEROS PARA ROEDORES", "BEBEDERO P/PERRO", "BOMBAS", "BOMBAS PARA ACUARISMO", "BOZAL IMPORTADO TIPO CANASTA", "CALEFACTORES IMPORTADOS", "CANILES PLEGABLES DE METAL", "CARDINAS DE MADERA", "CARDINAS DE PLASTICO", "COLLARES DE AHORQUE CON PUAS", "COLLARES DE CUERO IMPORTADOS", "COLLARES DE NYLON IMPORTADOS", "COLLARES ELASTIZADOS P/GATOS", "COMEDEROS ACERO INOXIDABLE", "COMEDEROS AUTOMATICOS IMPORT.", "COMEDEROS DE PLASTICO IMPORTAD", "CONJUNTO ALPINISTA", "CONJUNTO NYLON HUESOS", "CONJ.CORREA-COLLAR 10MM", "CONJUNTOS CORREA PRETAL", "CORREA CORTA CON RESORTE", "CORREAS COLLARES PRETALES", "CORREAS DE NYLON IMPORTADOS", "CORREAS EXTENSIBLES", "CUCHAS PARA PERROS", "DESCANSO Y RELAX", "DIFUSORES DE AIRE", "ELEMENTOS DE FILTRACION", "EDUCATIVOS HIGIÉNICOS", "FILTRO EXTERNO BOTELLON", "FILTROS ELECT. INTERNO", "FILTROS ELECTRICOS REBALSE", "FLETES VARIOS", "GRAVAS Y PIEDRAS DECORATIVAS", "HERMIT CRABB ACCESORIOS", "HUESOS DE ALGODON", "JAULA COBAYOS/CONEJOS IMPORT.", "JAULA PARA LOROS", "JAULAS GRANDES DORADAS", "JAULAS GRANDES PINTADAS", "JAULAS MEDIANAS EPOXI IMPORT.", "JAULAS PARA GATOS", "JAULAS PARA HAMSTERS", "JUGUETES BEEZTEES", "JUGUETES CHUCKIT", "JUGUETES CON SOGA", "JUGUETES DE GOMA IMPORT.", "JUGUETES DE LATEX", "JUGUETES DOGZILLA", "JUGUETES GATOS CAT NIP", "JUGUETES GATOS PELOTAS", "JUGUETES GATOS RATITAS", "JUGUETES GATOS VARIOS", "JUGUETES JACKSON GALAXY", "JUGUETES JW", "JUGUETES PARA PERROS", "JUGUETES VINILICOS JUMBO", "LITERAS IMPORTADAS", "MINERALES ABSORBENTES", "MOISES PLASTICO PARA MASCOTAS", "NIDOS IMPORTADOS P/PAJAROS", "PARIDERAS", "PEINES", "PELOTA P-MASCOTAS", "PECERAS DE ACRILICO", "PLANTA PLASTICA EN SOBRE", "PORTANOMBRE COLGANTE", "PRETALES NYLON IMPORTADOS", "PRODAC ALIMENTOS VARIOS", "RASCADORES VARIOS", "REPU. PARA AIREADORES IMPO", "REPU. PARA FILTROS IMPORTA", "REPUESTOS BOMBAS DE AGUA", "REPUESTOS PARA JAULAS IMPORTAD", "RESINA IMPORTADOS", "STICKERS Y DISPLAYS", "TAPA PARA TERRARIOS", "TERMOMETROS", "TRANSPORTADORAS DAYANG", "TRANSPORTADORAS MP", "TUBOS DE ILUMINACION"
]

# Estilos CSS personalizados
st.markdown("""
<style>
    html, body, [class*="css"] {
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    header, footer {visibility: hidden; height: 0;}
    .block-container {padding: 0; margin: 0; max-width: 100%;}
    .stApp {background: #f5f5f5; padding: 0 !important;}

    .title-container {
        background: #f5f5f5;
        padding: 20px 0;
        text-align: center;
        color: #000000;
        font-family: 'Arial Black', sans-serif;
        font-size: 2.8rem;
        margin: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .main-container {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .ruleta-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #000;
        height: 80vh;
        padding: 0;
        margin: 0;
    }

    .ruleta-frame {
        width: 800px;
        height: 800px;
        border: none;
    }

    .st-expanderHeader {
        background: #000 !important;
        color: #ffffff !important;
        font-weight: bold;
    }

    .form-content {
        background: white;
        padding: 20px;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stMultiselect>div>div>div {
        border-radius: 6px;
        padding: 8px;
        border: 1px solid #bbb;
        max-width: 200px; /* Más angosto */
        color: #000000;
    }

    .stTextInput label, .stSelectbox label, .stMultiselect label, .stRadio label {
        color: #000000 !important;
        font-weight: 500;
    }

    .stButton>button {
        background: #000000;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px 15px;
        width: 40%;
        border: none;
        font-size: 1rem;
        margin-top: 10px;
    }

    .stButton>button:hover {
        background: #333333;
        transform: translateY(-2px);
    }

    .stRadio>div {
        flex-direction: row;
        gap: 10px;
    }
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

# Formulario desplegable pegado abajo
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    st.markdown('<div class="form-content">', unsafe_allow_html=True)
    
    with st.form("formulario", clear_on_submit=True):
        col1, col2 = st.columns([1, 1])  # Igual ancho pero más chicos
        
        with col1:
            nombre = st.text_input("Nombre y apellido*")
            razon = st.text_input("Razón social*")
            whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...")
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"])
            
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

st.markdown('</div>', unsafe_allow_html=True)



