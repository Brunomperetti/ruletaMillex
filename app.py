import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# URL actualizada de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzEPDyzQsLuB26d3JQSb60I8xu7tYfI7lZbUnMhNarA0Dh8odExRAPOWzknhCiaG6ES/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="centered", initial_sidebar_state="collapsed")

# Listas de opciones
PROVINCIAS_ARGENTINA = [
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", 
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", 
    "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", 
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
    "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

INTERESES = ["Perro", "Gato", "Roedores", "Aves", "Acuario"]

VENDEDORES = ["Yerson", "Naza", "Eduardo", "Camila", "Axel"]

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

# Título
st.markdown('<div style="text-align: center; font-size: 40px; font-weight: bold;">🎡 RULETA MÁGICA MILLEX 🎡</div>', unsafe_allow_html=True)

# Botón para abrir la ruleta en pantalla completa
st.markdown(
    """
    <div style="text-align: center; margin: 20px;">
        <a href="https://wheelofnames.com/es/vug-z3k" target="_blank">
            <button style="
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 20px;
                cursor: pointer;
            ">
            🎯 GIRAR LA RULETA
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Formulario
with st.expander("📋 CARGAR DATOS DEL GANADOR", expanded=False):
    with st.form("formulario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre y apellido*")
            razon_social = st.text_input("Razón social*")
            nombre_fantasia = st.text_input("Nombre de fantasía")
            cuil_cuit = st.text_input("Número de CUIL o CUIT")
            whatsapp = st.text_input("WhatsApp (con código país)*", placeholder="+549...")
            email = st.text_input("Email*")
            direccion = st.text_input("Dirección*")
            cliente_tipo = st.radio("¿Es cliente nuevo o actual?*", ["Nuevo", "Actual"])
            cliente_estrella = st.checkbox("⭐ Marcar como cliente estrella")
            
        with col2:
            tipo_cliente = st.selectbox("Tipo de cliente*", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"])
            provincia = st.selectbox("Provincia*", PROVINCIAS_ARGENTINA)
            interes_principal = st.multiselect("Interés principal", INTERESES)
            categorias_productos = st.multiselect("Categorías de productos*", CATEGORIAS_PRODUCTOS)  # ✅ MULTISELECT
            marcas = st.multiselect("Marcas que maneja", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayaing", "Haintech", "The Pets", "Otros"])
            premio = st.selectbox("Premio ganado*", ["10% de descuento", "20% de descuento", "25% de descuento", "5% de descuento", "Seguí participando"])
            vendedor = st.selectbox("Vendedor*", VENDEDORES)
        
        enviar = st.form_submit_button("✅ ENVIAR Y GUARDAR DATOS")

        if enviar:
            datos = {
                "nombre": nombre,
                "razonSocial": razon_social,
                "nombreFantasia": nombre_fantasia,
                "cuilCuit": cuil_cuit,
                "whatsapp": whatsapp,
                "email": email,
                "direccion": direccion,
                "clienteTipo": cliente_tipo,
                "clienteEstrella": cliente_estrella,
                "tipoCliente": tipo_cliente,
                "provincia": provincia,
                "interes": ", ".join(interes_principal),
                "categoriaProductos": ", ".join(categorias_productos),
                "marcas": ", ".join(marcas),
                "premio": premio,
                "vendedor": vendedor
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



