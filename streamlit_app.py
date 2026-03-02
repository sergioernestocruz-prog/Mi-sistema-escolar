import streamlit as st
import pandas as pd

# Configuración de Identidad Visual
st.set_page_config(page_title="SIGAS - Prof. Sergio Cruz", layout="wide")

# CSS CORREGIDO (Letra oscura sobre fondo blanco)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 20px; }
    
    .student-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #43342e;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* CORRECCIÓN DE COLOR DE TEXTO */
    .student-name {
        color: #1a1a1a !important; /* Negro casi puro */
        font-weight: bold;
        font-size: 1.1rem;
    }
    .student-stats {
        color: #4a4a4a !important; /* Gris oscuro para las notas */
        font-size: 0.85rem;
    }
    
    .avatar {
        background-color: #43342e;
        color: white !important;
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

# --- NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.title("SIGAS Digital")
    st.write(f"**Prof. Sergio Cruz**")
    menu = st.radio("MENÚ", ["🏠 Panel de Grados", "📝 Registro de Notas", "🎖️ Méritos/Deméritos"])

# --- PANTALLA 3: MÉRITOS (DONDE ESTABA EL ERROR DE COLOR) ---
if menu == "🎖️ Méritos/Deméritos":
    st.write("### Gestión de Conducta 5° D")
    for index, row in st.session_state.alumnos.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"""
                <div class="student-card">
                    <div style="display: flex; align-items: center;">
                        <div class="avatar">{row['Nombre'][0]}</div>
                        <div>
                            <div class="student-name">{row['Nombre']}</div>
                            <div class="student-stats">Méritos: {row['Meritos']} | Deméritos: {row['Demeritos']}</div>
                        </div>
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

# --- LAS OTRAS PANTALLAS (Panel y Notas) ---
elif menu == "🏠 Panel de Grados":
    st.write("### Mis Grados")
    st.markdown('<div style="background-color: #43342e; color: white; padding: 30px; border-radius: 25px;"><h2>QUINTO GRADO D</h2><p>CIENCIA Y TECNOLOGÍA</p></div>', unsafe_allow_html=True)

elif menu == "📝 Registro de Notas":
    st.write("### Calificaciones")
    df = st.session_state.alumnos
    df["Promedio"] = (df["Act1"]*0.35 + df["Act2"]*0.35 + df["Prueba"]*0.30).round(1)
    editado = st.data_editor(df[["Nombre", "Act1", "Act2", "Prueba", "Promedio"]], hide_index=True)
