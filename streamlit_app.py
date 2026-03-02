import streamlit as st
import pandas as pd

# Configuración de Identidad
st.set_page_config(page_title="SIGAS Sergio Cruz", layout="wide")

# Estilo de la tarjeta (Igual a su foto)
st.markdown("""
    <style>
    .card { background-color: #43342e; color: white; padding: 25px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL (Para evitar errores de conexión) ---
if 'alumnos' not in st.session_state:
    # Datos de su nómina proporcionada
    nombres = [
        "Alfaro Morales Osael Nehemías", "Anzora Martínez Nestor Benjamín", "Canjura Coreas Mateo Isaac",
        "Cerón López Johanna Lisseth", "Fuentes Martínez Alexa Guadalupe", "García Guerra Hazel Janadari",
        "Granados Salmerón David Salomón", "Guerrero Amaya Sofia Okairy", "Guevara Flores Byron Alexander",
        "Hernández Henríquez Jason Eduardo", "López García Liam Eliseo", "López Martínez Saida Belén",
        "Martínez Hernández Valeria Monserratt", "Martínez Siliézar Matías Adonai", "Monroy Marroquín Oskar André",
        "Moran Torres Jennifer Lizeth", "Moz Granados Medani Odali", "Portillo González Cesar Emanuel",
        "Ramos Hernández Daniel Alejandro", "Ramos Sacaray Jonathan Ezequiel", "Rauda Granados Melvin Alessandro",
        "Vásquez Sandoval Alexa Mariel"
    ]
    st.session_state.alumnos = pd.DataFrame({
        "Nombre": nombres,
        "Act1 (35%)": [0.0] * 22,
        "Act2 (35%)": [0.0] * 22,
        "Prueba (30%)": [0.0] * 22,
        "Méritos": [0] * 22,
        "Deméritos": [0] * 22
    })

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

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
    st.write("Prof. Sergio Ernesto Cruz")

    # Tabla de Notas con Cálculo Automático
    df = st.session_state.alumnos
    df["Promedio"] = (df["Act1 (35%)"] * 0.35) + (df["Act2 (35%)"] * 0.35) + (df["Prueba (30%)"] * 0.30)
    
    st.write("### Registro de Calificaciones")
    # El editor permite escribir notas directamente
    editado = st.data_editor(df, hide_index=True)
    st.session_state.alumnos = editado

    # Sección de Conducta
    st.divider()
    st.subheader("🎖️ Control de Méritos y Deméritos")
    est_sel = st.selectbox("Seleccione Estudiante", df["Nombre"])
    c1, c2 = st.columns(2)
    if c1.button("👍 Registrar Mérito"):
        st.success(f"Mérito registrado para {est_sel}")
    if c2.button("👎 Registrar Demérito"):
        st.error(f"Demérito registrado para {est_sel}")
