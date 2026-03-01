import streamlit as st
import pandas as pd

# Configuración visual inspirada en SIGAS
st.set_page_config(page_title="SIGAS - Profe Sergio", layout="wide")

# Estilo CSS para imitar la interfaz de la imagen
st.markdown("""
    <style>
    .card {
        background-color: #43342e;
        color: white;
        padding: 20px;
        border-radius: 25px;
        margin-bottom: 20px;
    }
    .btn-gestionar {
        background-color: white;
        color: black;
        padding: 10px 20px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    .stDataFrame { border: 1px solid #e6e6e6; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar datos de 5° D (Nómina cargada)
if 'db' not in st.session_state:
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
    st.session_state.db = pd.DataFrame({
        "Nombre": nombres,
        "Act1 (35%)": [0.0] * len(nombres),
        "Act2 (35%)": [0.0] * len(nombres),
        "Prueba (30%)": [0.0] * len(nombres),
        "Promedio": [0.0] * len(nombres),
        "Méritos": [0] * len(nombres),
        "Demeritos": [0] * len(nombres)
    })

# --- LÓGICA DE NAVEGACIÓN ---
if 'vista' not in st.session_state:
    st.session_state.vista = "panel"

# --- PANTALLA PRINCIPAL (PANEL DE MIS GRADOS) ---
if st.session_state.vista == "panel":
    st.write("### PANEL DE MIS GRADOS")
    st.write("SIGAS - GESTIÓN ACADÉMICA")
    
    st.selectbox("Todas las escuelas", ["Centro Escolar Actual"])
    st.button("+ CREAR NUEVO")

    # Tarjeta de Grado
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 1.5rem; font-weight: bold;">D</div>
        <div style="font-size: 1.2rem;">QUINTO D</div>
        <hr style="border-top: 1px solid #6d5b54;">
        <p style="font-size: 0.8rem; color: #bcaaa4;">SISTEMA GESTOR DE AULA</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("GESTIONAR GRADO →"):
        st.session_state.vista = "gestion"
        st.rerun()

# --- PANTALLA DE GESTIÓN (LISTA Y NOTAS) ---
elif st.session_state.vista == "gestion":
    if st.button("← Volver al Panel"):
        st.session_state.vista = "panel"
        st.rerun()

    st.header("Gestionar: Quinto D - Ciencia y Tecnología")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar estudiante por nombre...")
    
    # Cálculo automático 35/35/30
    df = st.session_state.db
    df["Promedio"] = (df["Act1 (35%)"] * 0.35) + (df["Act2 (35%)"] * 0.35) + (df["Prueba (30%)"] * 0.30)
    
    # Filtrar si hay búsqueda
    df_mostrar = df[df["Nombre"].str.contains(busqueda, case=False)] if busqueda else df

    st.write("### Registro de Calificaciones")
    st.write("Modifica las notas abajo y el promedio se calculará solo.")
    
    # Editor de datos
    edited_df = st.data_editor(
        df_mostrar,
        column_config={
            "Promedio": st.column_config.NumberColumn("Promedio Final", format="%.1f"),
            "Nombre": st.column_config.TextColumn("Estudiante", disabled=True)
        },
        hide_index=True,
    )

    if st.button("💾 Guardar Cambios"):
        st.session_state.db.update(edited_df)
        st.success("Información guardada localmente.")

    # --- SECCIÓN DE MÉRITOS ---
    st.divider()
    st.subheader("🎖️ Control de Méritos y Demeritos")
    col_sel, col_btn1, col_btn2 = st.columns([2,1,1])
    
    with col_sel:
        est_sel = st.selectbox("Seleccionar Alumno", df["Nombre"])
    with col_btn1:
        if st.button("👍 Mérito"):
            idx = st.session_state.db.index[st.session_state.db['Nombre'] == est_sel][0]
            st.session_state.db.at[idx, 'Méritos'] += 1
            st.toast("Mérito añadido")
    with col_btn2:
        if st.button("👎 Demérito"):
            idx = st.session_state.db.index[st.session_state.db['Nombre'] == est_sel][0]
            st.session_state.db.at[idx, 'Demeritos'] += 1
            st.toast("Demérito registrado")
