import streamlit as st 
import streamlit.components.v1 as components
import urllib.parse
import requests
from datetime import datetime

# URL de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxg1j5w57os20mywlO0Kup-kqMxfnCuIeTbJBcSqJFGPizKVls1xp5WErH0K_yKypMQ/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide", initial_sidebar_state="collapsed")

# Listas de opciones (se mantienen igual)
# ... [todo el código de listas de opciones permanece igual]

# Estilos CSS personalizados (se mantienen igual)
# ... [todo el código CSS permanece igual]

# Estructura principal (se mantiene igual)
# ... [código de estructura principal permanece igual]

# Formulario desplegable - ESTA ES LA PARTE MODIFICADA
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
            
            # Preparar datos para enviar en el formato EXACTO que espera tu Google Sheet
            datos = {
                "action": "guardar_datos",
                "data": {
                    "Nombre y Apellido": nombre or "",
                    "Razon Social": razon or "",
                    "Nombre Fantasía": fantasia or "",
                    "CUIL/CUIT": cuil_cuit or "",
                    "whatsapp": whatsapp or "",
                    "Cliente Tipo": cliente_tipo or "",
                    "Cliente Estrella": "Sí" if estrella else "No",
                    "Tipo Cliente": tipo_cliente or "",
                    "Provincia": provincia or "",
                    "Interés Principal": ", ".join(interes) if interes else "",
                    "Categorías Productos": ", ".join(categoria_productos) if categoria_productos else "",
                    "Marcas": ", ".join(marcas) if marcas else "",
                    "premio ganado": premio or "",
                    "Fecha y hora": fecha_hora
                }
            }
            
            try:
                # Enviar datos con parámetros URL-encoded
                params = {
                    "nombre": nombre or "",
                    "razon_social": razon or "",
                    "nombre_fantasia": fantasia or "",
                    "cuil_cuit": cuil_cuit or "",
                    "whatsapp": whatsapp or "",
                    "cliente_tipo": cliente_tipo or "",
                    "cliente_estrella": "Sí" if estrella else "No",
                    "tipo_cliente": tipo_cliente or "",
                    "provincia": provincia or "",
                    "interes_principal": ", ".join(interes) if interes else "",
                    "categorias_productos": ", ".join(categoria_productos) if categoria_productos else "",
                    "marcas": ", ".join(marcas) if marcas else "",
                    "premio_ganado": premio or "",
                    "fecha_hora": fecha_hora
                }
                
                response = requests.get(WEB_APP_URL, params=params)
                
                if response.status_code == 200:
                    st.success("✅ Datos guardados correctamente!")
                    if nombre and premio and premio != "Seguí participando" and whatsapp:
                        mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste: *{premio}*. Presentá este mensaje para canjearlo."
                        whatsapp_limpio = whatsapp.strip().replace(" ", "").replace("-", "")
                        link = f"https://wa.me/{whatsapp_limpio}?text={urllib.parse.quote(mensaje)}"
                        st.markdown(f"[📱 Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error al guardar datos: {response.text}")
            except Exception as e:
                st.error(f"❌ Error de conexión: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
