import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuración visual
st.set_page_config(page_title="SIGAS Privado - Profe Sergio", layout="wide")

# Título y Materia
st.title("PANEL DE MIS GRADOS")
st.subheader("Prof. Sergio Ernesto Cruz - Ciencia y Tecnología")

# CONEXIÓN A GOOGLE SHEETS
# Reemplaza el link de abajo por el tuyo de Google Sheets
url =  "https://docs.google.com/spreadsheets/d/154rAAUmIVU6nWiTbBJmPRnHqpEP1weZ95GtYlJfzsDk/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos de los alumnos
df = conn.read(spreadsheet=url)

# --- VISTA DE TARJETAS (PANTALLA INICIAL) ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = "inicio"

if st.session_state.seccion == "inicio":
    st.markdown("""
        <div style="background-color: #43342e; color: white; padding: 25px; border-radius: 20px;">
            <h2>D</h2>
            <h3>QUINTO GRADO D</h3>
            <p>CIENCIA Y TECNOLOGÍA</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("GESTIONAR GRADO →"):
        st.session_state.seccion = "gestion"
        st.rerun()

# --- VISTA DE GESTIÓN (NOTAS Y MÉRITOS) ---
else:
    if st.button("← Volver al Panel"):
        st.session_state.seccion = "inicio"
        st.rerun()

    st.write("### Registro de 5° D")
    
    # Cálculo de Promedio 35/35/30
    df["Promedio"] = (df["Act1"] * 0.35) + (df["Act2"] * 0.35) + (df["Prueba"] * 0.30)
    
    # Editor de Notas (Lo que escribas aquí se enviará a Google Sheets)
    edited_df = st.data_editor(df, hide_index=True)

    if st.button("💾 GUARDAR CAMBIOS EN LA NUBE"):
        conn.update(spreadsheet=url, data=edited_df)
        st.success("¡Datos guardados permanentemente en tu Google Sheets!")

    # Sección de Méritos rápida
    st.divider()
    st.write("### 🎖️ Control de Conducta")
    alumno = st.selectbox("Seleccionar Estudiante", df["Nombre"])
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👍 Sumar Mérito"):
            st.balloons()
            st.info(f"Registrado mérito para {alumno}. No olvides dar clic en Guardar arriba.")
