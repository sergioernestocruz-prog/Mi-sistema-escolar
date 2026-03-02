import streamlit as st
import pandas as pd

# Configuración Profe Sergio
st.set_page_config(page_title="SIGAS Sergio Cruz", layout="wide")

# Estilo visual
st.markdown("<style>.card { background-color: #43342e; color: white; padding: 25px; border-radius: 20px; }</style>", unsafe_allow_html=True)

# ENLACE DE SU BASE DE DATOS
# Usamos el formato /export?format=csv para leerla directamente
sheet_url = "https://docs.google.com/spreadsheets/d/154rAAUmIVU6nWiTbBJmPRnHqpEP1weZ95GtYlJfzsDk/export?format=csv"

if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# Cargar datos desde Google
@st.cache_data(ttl=60) # Se actualiza cada minuto
def cargar_desde_google():
    return pd.read_csv(sheet_url)

try:
    df_google = cargar_desde_google()
except:
    st.error("Error al conectar con Google Sheets. Verifique que el enlace sea público.")
    st.stop()

if st.session_state.pagina == "inicio":
    st.write("### PANEL DE MIS GRADOS")
    st.markdown('<div class="card"><h2>D</h2><h3>QUINTO GRADO D</h3><p>CIENCIA Y TECNOLOGÍA</p></div>', unsafe_allow_html=True)
    if st.button("GESTIONAR GRADO →"):
        st.session_state.pagina = "gestion"
        st.rerun()

else:
    if st.button("← VOLVER"):
        st.session_state.pagina = "inicio"
        st.rerun()

    st.title("Gestión Académica - 5° D")
    
    # Cálculo de Promedio 35/35/30
    df_google["Promedio"] = (df_google["Act1"] * 0.35) + (df_google["Act2"] * 0.35) + (df_google["Prueba"] * 0.30)
    
    st.write("### Registro de Calificaciones")
    st.info("Nota: Para que los cambios sean permanentes en esta versión, edite directamente su archivo de Google Sheets y refresque esta página.")
    
    st.data_editor(df_google, hide_index=True, disabled=["Nombre", "Promedio"])

    # Sección de Conducta (Informativa)
    st.divider()
    st.subheader("🎖️ Control de Méritos y Deméritos")
    est_sel = st.selectbox("Seleccione Estudiante", df_google["Nombre"])
    if st.button("👍 Registrar Mérito"):
        st.success(f"Mérito para {est_sel}. Regístrelo en su Excel para guardarlo.")
