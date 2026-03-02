import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="PANEL DE MIS GRADOS", layout="wide")

# ESTILO CSS PARA CLONAR SIGAS.DIGITAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f5f5f5; }
    
    .main-title { font-weight: bold; font-size: 1.2rem; color: #333; margin-bottom: 5px; }
    .sub-title { color: #888; font-size: 0.9rem; margin-bottom: 20px; text-transform: uppercase; }
    
    /* Tarjeta estilo SIGAS */
    .card-container {
        background-color: #43342e;
        border-radius: 40px 40px 10px 10px;
        padding: 30px 20px;
        color: white;
        position: relative;
        margin-bottom: 0px;
    }
    .card-letter {
        background-color: rgba(255,255,255,0.2);
        width: 40px; height: 40px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin-bottom: 15px;
    }
    .card-name { font-weight: bold; font-size: 1.3rem; margin-bottom: 5px; }
    
    .card-footer {
        background-color: white;
        border-radius: 0px 0px 40px 40px;
        padding: 20px;
        border: 1px solid #eee;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #888;
        font-size: 0.8rem;
    }
    
    .btn-crear {
        background-color: #d6c0b3;
        border: none;
        padding: 10px 25px;
        border-radius: 15px;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'vista' not in st.session_state:
    st.session_state.vista = "panel"

# --- PANTALLA 1: PANEL DE MIS GRADOS (EL CLON) ---
if st.session_state.vista == "panel":
    st.markdown('<p class="main-title">PANEL DE MIS GRADOS</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">SIGAS - GESTIÓN ACADÉMICA</p>', unsafe_allow_html=True)
    
    st.selectbox("", ["Todas las escuelas"], label_visibility="collapsed")
    st.markdown('<button class="btn-crear">+ CREAR NUEVO</button>', unsafe_allow_html=True)
    
    # Renderizado de la tarjeta café como la de la foto
    st.markdown("""
        <div class="card-container">
            <div style="display: flex; justify-content: space-between;">
                <div class="card-letter">D</div>
                <div style="display: flex; gap: 10px;">
                    <span style="background: rgba(255,255,255,0.1); padding: 5px; border-radius: 50%;">✏️</span>
                    <span style="background: rgba(255,0,0,0.2); padding: 5px; border-radius: 50%;">🗑️</span>
                </div>
            </div>
            <div class="card-name">QUINTO</div>
        </div>
        <div class="card-footer">
            <div><span style="color: #d6c0b3;">●</span> SISTEMA GESTOR DE AULA</div>
            <div style="font-weight: bold; color: #333;">GESTIONAR GRADO  &nbsp; > </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("ENTRAR A GESTIONAR GRADO D", use_container_width=True):
        st.session_state.vista = "gestion"
        st.rerun()

# --- PANTALLA 2: GESTIÓN (LISTA DE ALUMNOS) ---
else:
    if st.button("← VOLVER AL PANEL"):
        st.session_state.vista = "panel"
        st.rerun()
        
    st.write(f"### Registro de Quinto D - Prof. Sergio Cruz")
    st.write("Materia: Ciencia y Tecnología")
    
    # Carga de su nómina de 22 alumnos
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
    
    df = pd.DataFrame({
        "Estudiante": nombres,
        "Act1 (35%)": [0.0] * 22,
        "Act2 (35%)": [0.0] * 22,
        "Prueba (30%)": [0.0] * 22
    })
    
    # Cálculo de promedio automático
    df["Promedio"] = (df["Act1 (35%)"] * 0.35) + (df["Act2 (35%)"] * 0.35) + (df["Prueba (30%)"] * 0.30)
    
    # Tabla editable
    st.data_editor(df, hide_index=True, use_container_width=True)
    
    st.divider()
    st.subheader("🎖️ Méritos y Deméritos")
    sel = st.selectbox("Seleccionar Alumno", nombres)
    c1, c2 = st.columns(2)
    with c1: st.button("👍 Registrar Mérito", use_container_width=True)
    with c2: st.button("👎 Registrar Demérito", use_container_width=True)
