import streamlit as st
import pandas as pd

# Configuración de Identidad Visual
st.set_page_config(page_title="SIGAS - Prof. Sergio Cruz", layout="wide")

# CSS Avanzado para imitar SIGAS.digital
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; }
    /* Estilo de Tarjeta Estudiante */
    .student-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #43342e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .avatar {
        background-color: #43342e;
        color: white;
        width: 40px; height: 40px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Datos de la Nómina 5° D
if 'alumnos' not in st.session_state:
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
        "Act1": [0.0]*22, "Act2": [0.0]*22, "Prueba": [0.0]*22,
        "Meritos": [0]*22, "Demeritos": [0]*22
    })

# --- NAVEGACIÓN LATERAL (Como en el video) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=100)
    st.title("SIGAS Digital")
    st.write(f"**Prof. Sergio Cruz**")
    menu = st.radio("MENÚ", ["🏠 Panel de Grados", "📝 Registro de Notas", "🎖️ Méritos/Deméritos"])

# --- PANTALLA 1: PANEL ---
if menu == "🏠 Panel de Grados":
    st.write("### Mis Grados")
    st.markdown("""
        <div style="background-color: #43342e; color: white; padding: 30px; border-radius: 25px;">
            <div style="background: rgba(255,255,255,0.2); width: 40px; border-radius: 5px; text-align: center;">D</div>
            <h2 style="margin: 10px 0;">QUINTO GRADO D</h2>
            <p style="font-size: 0.8rem; opacity: 0.8;">CIENCIA Y TECNOLOGÍA</p>
        </div>
    """, unsafe_allow_html=True)

# --- PANTALLA 2: NOTAS ---
elif menu == "📝 Registro de Notas":
    st.write("### Calificaciones - Ciencia y Tecnología")
    df = st.session_state.alumnos
    df["Promedio"] = (df["Act1"]*0.35 + df["Act2"]*0.35 + df["Prueba"]*0.30).round(1)
    
    # Editor de notas
    editado = st.data_editor(df[["Nombre", "Act1", "Act2", "Prueba", "Promedio"]], hide_index=True)
    if st.button("💾 Guardar Cambios"):
        st.session_state.alumnos.update(editado)
        st.success("Notas actualizadas localmente")

# --- PANTALLA 3: MÉRITOS ---
elif menu == "🎖️ Méritos/Deméritos":
    st.write("### Gestión de Conducta 5° D")
    for index, row in st.session_state.alumnos.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"""
                <div class="student-card">
                    <div style="display: flex; align-items: center;">
                        <div class="avatar">{row['Nombre'][0]}</div>
                        <div><b>{row['Nombre']}</b><br><small>Méritos: {row['Meritos']} | Deméritos: {row['Demeritos']}</small></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(f"👍", key=f"m_{index}"):
                st.session_state.alumnos.at[index, 'Meritos'] += 1
                st.rerun()
        with col3:
            if st.button(f"👎", key=f"d_{index}"):
                st.session_state.alumnos.at[index, 'Demeritos'] += 1
                st.rerun()
