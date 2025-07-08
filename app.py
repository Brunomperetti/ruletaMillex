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
    "AIREADORES BOYU", "AIREADORES SHANDA", "ALICATE P/ PERROS Y GATOS", "ARBOLES P/GATO",
    "BEBEDEROS PARA HAMSTER", "BEBEDEROS PARA ROEDORES", "BEBEDERO P/PERRO", "BOMBAS",
    "BOMBAS PARA ACUARISMO", "BOZAL IMPORTADO TIPO CANASTA", "CALEFACTORES IMPORTADOS",
    "CANILES PLEGABLES DE METAL", "CARDINAS DE MADERA", "CARDINAS DE PLASTICO",
    "COLLARES DE AHORQUE CON PUAS", "COLLARES DE CUERO IMPORTADOS", "COLLARES DE NYLON IMPORTADOS",
    "COLLARES ELASTIZADOS P/GATOS", "COMEDEROS ACERO INOXIDABLE", "COMEDEROS AUTOMATICOS IMPORT.",
    "COMEDEROS DE PLASTICO IMPORTAD", "CONJUNTO ALPINISTA", "CONJUNTO NYLON HUESOS",
    "CONJ.CORREA-COLLAR 10MM", "CONJUNTOS CORREA PRETAL", "CORREA CORTA CON RESORTE",
    "CORREAS COLLARES PRETALES", "CORREAS DE NYLON IMPORTADOS", "CORREAS EXTENSIBLES",
    "CUCHAS PARA PERROS", "DESCANSO Y RELAX", "DIFUSORES DE AIRE", "ELEMENTOS DE FILTRACION",
    "EDUCATIVOS HIGIÉNICOS", "FILTRO EXTERNO BOTELLON", "FILTROS ELECT. INTERNO",
    "FILTROS ELECTRICOS REBALSE", "FLETES VARIOS", "GRAVAS Y PIEDRAS DECORATIVAS",
    "HERMIT CRABB ACCESORIOS", "HUESOS DE ALGODON", "JAULA COBAYOS/CONEJOS IMPORT.",
    "JAULA PARA LOROS", "JAULAS GRANDES DORADAS", "JAULAS GRANDES PINTADAS",
    "JAULAS MEDIANAS EPOXI IMPORT.", "JAULAS PARA GATOS", "JAULAS PARA HAMSTERS",
    "JUGUETES BEEZTEES", "JUGUETES CHUCKIT", "JUGUETES CON SOGA", "JUGUETES DE GOMA IMPORT.",
    "JUGUETES DE LATEX", "JUGUETES DOGZILLA", "JUGUETES GATOS CAT NIP",
    "JUGUETES GATOS PELOTAS", "JUGUETES GATOS RATITAS", "JUGUETES GATOS VARIOS",
    "JUGUETES JACKSON GALAXY", "JUGUETES JW", "JUGUETES PARA PERROS", "JUGUETES VINILICOS JUMBO",
    "LITERAS IMPORTADAS", "MINERALES ABSORBENTES", "MOISES PLASTICO PARA MASCOTAS",
    "NIDOS IMPORTADOS P/PAJAROS", "PARIDERAS", "PEINES", "PELOTA P-MASCOTAS",
    "PECERAS DE ACRILICO", "PLANTA PLASTICA EN SOBRE", "PORTANOMBRE COLGANTE",
    "PRETALES NYLON IMPORTADOS", "PRODAC ALIMENTOS VARIOS", "RASCADORES VARIOS",
    "REPU. PARA AIREADORES IMPO", "REPU. PARA FILTROS IMPORTA", "REPUESTOS BOMBAS DE AGUA",
    "REPUESTOS PARA JAULAS IMPORTAD", "RESINA IMPORTADOS", "STICKERS Y DISPLAYS",
    "TAPA PARA TERRARIOS", "TERMOMETROS", "TRANSPORTADORAS DAYANG", "TRANSPORTADORAS MP",
    "TUBOS DE ILUMINACION"
]

# Estilos CSS forzando textos negros y campos más angostos
st.markdown("""
<style>
html, body, [class*="css"] {
    color: #000000 !important;
    font-family: Arial, sans-serif !important;
}
.st-emotion-cache-1avcm0n, .st-emotion-cache-1avcm0n h1, .st-emotion-cache-1avcm0n label,
.st-emotion-cache-1c7y2kd, .st-emotion-cache-1c7y2kd span, .stMarkdown p, label {
    color: #000000 !important;
}
.st-expanderHeader {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: bold !important;
}
.stTextInput>div>div>input,
.stSelectbox>div>div>select,
.stMultiselect>div>div>div {
    max-width: 250px !important; /* Campos más angostos */
}
.stButton>button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border-radius: 6px;
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

# Formulario desplegable
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    st.markdown('<div class="form-content">', unsafe_allow_html=True)
    
    with st.form("formulario", clear_on_submit=True):
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
        marcas = st.multiselect("Interés de marcas", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
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



