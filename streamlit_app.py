import streamlit as st
import pandas as pd

# Configuración visual inspirada en su imagen de SIGAS
st.set_page_config(page_title="SIGAS - Profe Sergio", layout="wide")

st.markdown("""
    <style>
    .card { background-color: #43342e; color: white; padding: 20px; border-radius: 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ENLACE DIRECTO A SU BASE DE DATOS (YA CONFIGURADO)
sheet_id = "154rAAUmIVU6nWiTbBJmPRnHqpEP1weZ95GtYlJfzsDk"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

# Función para cargar datos de forma segura
@st.cache_data
def cargar_datos():
    return pd.read_csv(url)

try:
    df = cargar_datos()
except:
    st.error("No se pudo conectar con Google Sheets. Asegúrese de que el archivo sea 'Público' o tenga permiso de 'Editor' para cualquier persona con el enlace.")
    st.stop()

# --- NAVEGACIÓN ---
if 'vista' not in st.session_state:
    st.session_state.vista = "panel"

if st.session_state.vista == "panel":
    st.write("### PANEL DE MIS GRADOS")
    st.write("SIGAS - GESTIÓN ACADÉMICA")
    
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 1.5rem; font-weight: bold;">D</div>
        <div style="font-size: 1.2rem;">QUINTO GRADO D</div>
        <hr style="border-top: 1px solid #6d5b54;">
        <p style="font-size: 0.8rem; color: #bcaaa4;">CIENCIA Y TECNOLOGÍA</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("GESTIONAR GRADO →"):
        st.session_state.vista = "gestion"
        st.rerun()

elif st.session_state.vista == "gestion":
    if st.button("← Volver al Panel"):
        st.session_state.vista = "panel"
        st.rerun()

    st.header(f"Gestión: Quinto D - Prof. Sergio Ernesto Cruz")
    
    # Buscador rápido
    busqueda = st.text_input("🔍 Buscar estudiante por nombre...")
    
    # Cálculo de Promedio 35/35/30
    # Aseguramos que las columnas existan en su Excel
    for col in ["Act1", "Act2", "Prueba"]:
        if col not in df.columns:
            df[col] = 0.0
            
    df["Promedio"] = (df["Act1"] * 0.35) + (df["Act2"] * 0.35) + (df["Prueba"] * 0.30)
    
    df_mostrar = df[df["Nombre"].str.contains(busqueda, case=False)] if busqueda else df

    st.write("### Registro de Calificaciones")
    edited_df = st.data_editor(df_mostrar, hide_index=True)

    if st.button("💾 Guardar Cambios"):
        st.info("Para guardar permanentemente en Google Sheets desde la app se requiere una configuración avanzada de 'Secrets'. Por ahora, use esta tabla para calcular y visualizarlos.")

    # Módulo de Méritos
    st.divider()
    st.subheader("🎖️ Registro de Méritos y Deméritos")
    alumno_sel = st.selectbox("Seleccione al estudiante", df["Nombre"])
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👍 Registrar Mérito"):
            st.toast(f"Mérito anotado para {alumno_sel}")
    with c2:
        if st.button("👎 Registrar Demérito"):
            st.toast(f"Demérito anotado para {alumno_sel}")
