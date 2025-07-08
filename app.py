import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# URL actualizada de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxg1j5w57os20mywlO0Kup-kqMxfnCuIeTbJBcSqJFGPizKVls1xp5WErH0K_yKypMQ/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

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
    "ACCESORIOS DE LIMPIEZA",
    "ACCESORIOS DE PELUQUERIA IMPOR",
    "ACCESORIOS IMPOR. P/PAJAROS -A",
    "ACCESORIOS IMPORTADOS P/PAJARO",
    "ACCESORIOS PARA ROEDORES",
    "ACCESORIOS VARIOS ACUARIO",
    "ACCESORIOS VARIOS P/GATOS",
    "ACCESORIOS VARIOS P/PERROS",
    "ADORNOS CON MOVIMIENTO",
    "AIREADORES BOYU",
    "AIREADORES SHANDA",
    "ALICATE P/ PERROS Y GATOS",
    "ARBOLES P/GATO",
    "BEBEDEROS PARA HAMSTER",
    "BEBEDEROS PARA ROEDORES",
    "BEBEDERO P/PERRO",
    "BOMBAS",
    "BOMBAS PARA ACUARISMO",
    "BOZAL IMPORTADO TIPO CANASTA",
    "CALEFACTORES IMPORTADOS",
    "CANILES PLEGABLES DE METAL",
    "CARDINAS DE MADERA",
    "CARDINAS DE PLASTICO",
    "COLLARES DE AHORQUE CON PUAS",
    "COLLARES DE CUERO IMPORTADOS",
    "COLLARES DE NYLON IMPORTADOS",
    "COLLARES ELASTIZADOS P/GATOS",
    "COMEDEROS ACERO INOXIDABLE",
    "COMEDEROS AUTOMATICOS IMPORT.",
    "COMEDEROS DE PLASTICO IMPORTAD",
    "CONJUNTO ALPINISTA",
    "CONJUNTO NYLON HUESOS",
    "CONJ.CORREA-COLLAR 10MM",
    "CONJUNTOS CORREA PRETAL",
    "CORREA CORTA CON RESORTE",
    "CORREAS COLLARES PRETALES",
    "CORREAS DE NYLON IMPORTADOS",
    "CORREAS EXTENSIBLES",
    "CUCHAS PARA PERROS",
    "DESCANSO Y RELAX",
    "DIFUSORES DE AIRE",
    "ELEMENTOS DE FILTRACION",
    "EDUCATIVOS HIGIÉNICOS",
    "FILTRO EXTERNO BOTELLON",
    "FILTROS ELECT. INTERNO",
    "FILTROS ELECTRICOS REBALSE",
    "FLETES VARIOS",
    "GRAVAS Y PIEDRAS DECORATIVAS",
    "HERMIT CRABB ACCESORIOS",
    "HUESOS DE ALGODON",
    "JAULA COBAYOS/CONEJOS IMPORT.",
    "JAULA PARA LOROS",
    "JAULAS GRANDES DORADAS",
    "JAULAS GRANDES PINTADAS",
    "JAULAS MEDIANAS EPOXI IMPORT.",
    "JAULAS PARA GATOS",
    "JAULAS PARA HAMSTERS",
    "JUGUETES BEEZTEES",
    "JUGUETES CHUCKIT",
    "JUGUETES CON SOGA",
    "JUGUETES DE GOMA IMPORT.",
    "JUGUETES DE LATEX",
    "JUGUETES DOGZILLA",
    "JUGUETES GATOS CAT NIP",
    "JUGUETES GATOS PELOTAS",
    "JUGUETES GATOS RATITAS",
    "JUGUETES GATOS VARIOS",
    "JUGUETES JACKSON GALAXY",
    "JUGUETES JW",
    "JUGUETES PARA PERROS",
    "JUGUETES VINILICOS JUMBO",
    "LITERAS IMPORTADAS",
    "MINERALES ABSORBENTES",
    "MOISES PLASTICO PARA MASCOTAS",
    "NIDOS IMPORTADOS P/PAJAROS",
    "PARIDERAS",
    "PEINES",
    "PELOTA P-MASCOTAS",
    "PECERAS DE ACRILICO",
    "PLANTA PLASTICA EN SOBRE",
    "PORTANOMBRE COLGANTE",
    "PRETALES NYLON IMPORTADOS",
    "PRODAC ALIMENTOS VARIOS",
    "RASCADORES VARIOS",
    "REPU. PARA AIREADORES IMPO",
    "REPU. PARA FILTROS IMPORTA",
    "REPUESTOS BOMBAS DE AGUA",
    "REPUESTOS PARA JAULAS IMPORTAD",
    "RESINA IMPORTADOS",
    "STICKERS Y DISPLAYS",
    "TAPA PARA TERRARIOS",
    "TERMOMETROS",
    "TRANSPORTADORAS DAYANG",
    "TRANSPORTADORAS MP",
    "TUBOS DE ILUMINACION"
]

# Estilos CSS
st.markdown("""
<style>
    header, footer {visibility: hidden;}
    .block-container {padding: 0; margin: 0;}
    .title-container {
        background: rgba(0,0,0,0.9);
        padding: 16px 32px;
        text-align: center;
        color: white;
        font-family: 'Arial Black';
        font-size: 2.5rem;
        text-shadow: 1px 1px 4px rgba(255,255,255,0.5);
        border-bottom: 1px solid #333;
    }
    ::-webkit-scrollbar {
        display: none;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        margin-top: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    .ruleta-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        background-color: #000;
    }
    .form-container {
        padding: 20px;
        background: white;
    }
    .stMultiSelect [data-baseweb=select] span{
        max-width: 250px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# 🎡 Ruleta embebida centrada
st.markdown('<div class="ruleta-container">', unsafe_allow_html=True)
components.html("""
    <iframe src="https://wheelofnames.com/es/vug-z3k" width="800" height="800" style="border:none;"></iframe>
""", height=800, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# 📋 Formulario
with st.expander("🎁 Cargar datos del ganador", expanded=False):
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
            interes = st.multiselect("Interés", INTERESES)
            categoria_productos = st.multiselect("Categorías de productos", CATEGORIAS_PRODUCTOS)
        
        marcas = st.multiselect("Marcas que maneja", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
        premio = st.selectbox("Premio ganado*", ["", "10off", "20off", "25off", "5off", "Seguí participando"])
        
        enviar = st.form_submit_button("Enviar y guardar")
        
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
                    # Envío como POST
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
                            st.markdown(f"[Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Error: {respuesta_json.get('message', 'Error desconocido')}")
                    except ValueError:
                        st.error("❌ La respuesta no es JSON válido.")
                        st.info("Respuesta cruda recibida: " + respuesta.text[:200] + "...")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
                    st.info("Verifica tu conexión a internet o la URL del script")
            else:
                st.warning("⚠️ Por favor completa todos los campos obligatorios (*)")

