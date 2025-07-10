import streamlit as st 
import streamlit.components.v1 as components
import urllib.parse
import requests

# URL actualizada de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxg1j5w57os20mywlO0Kup-kqMxfnCuIeTbJBcSqJFGPizKVls1xp5WErH0K_yKypMQ/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide", initial_sidebar_state="collapsed")

# Listas de opciones (las mismas que tenías)
PROVINCIAS_ARGENTINA = [
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", 
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", 
    "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", 
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
    "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

INTERESES = ["Perro", "Gato", "Roedores", "Aves", "Acuario"]

CATEGORIAS_PRODUCTOS = [
    # ... tu lista completa de categorías ...
]

# Aquí sigue todo tu código de estilos CSS y estructura (sin cambios)
# ...

# Formulario desplegable
with st.expander("CARGAR DATOS DEL GANADOR", expanded=False):
    st.markdown('<div class="form-content">', unsafe_allow_html=True)
    
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
                # Creo lista con los datos en el orden exacto que espera tu Google Sheet
                fila_ordenada = [
                    nombre,
                    razon,
                    fantasia,
                    cuil_cuit,
                    whatsapp,
                    cliente_tipo,
                    "Sí" if estrella else "No",
                    tipo_cliente,
                    provincia,
                    ", ".join(interes) if interes else "",
                    ", ".join(categoria_productos) if categoria_productos else "",
                    ", ".join(marcas) if marcas else "",
                    premio
                ]
                
                datos = {"fila": fila_ordenada}
                
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

st.markdown('</div>', unsafe_allow_html=True)




