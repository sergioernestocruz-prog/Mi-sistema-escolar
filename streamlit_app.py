import streamlit as st
import pandas as pd
import requests
import json

# Configuración de Identidad Visual
st.set_page_config(page_title="SIGAS - Prof. Sergio Cruz", layout="wide")

# URL de su Google Apps Script (Extraída de su captura)
URL_API = "https://script.google.com/macros/s/AKfycbzPEiS2C55oZ2mqOlDLiagVq-3a58cl99Z5v6Gx8rATlEiksYK0ZjrbXkRtK1RLV8Uknw/exec"

# CSS para imitar SIGAS con letras visibles (Negras)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .student-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 15px;
        border-left: 6px solid #43342e;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .student-name {
        color: #1a1a1a !important; /* Texto negro para que se vea */
        font-weight: bold;
        font-size: 1.1rem;
    }
    .student-stats {
        color: #555555 !important; /* Gris oscuro para méritos */
        font-size: 0.9rem;
    }
    .avatar {
        background-color: #43342e;
        color: white !important;
        width: 45px; height: 45px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Nómina de 5° D
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
        "Act1": [0.0]*22, "Act2": [0.0]*22, "Prueba": [0.0]*22,
        "Meritos": [0]*22, "Demeritos": [0]*22
    })

# Navegación lateral
with st.sidebar:
    st.title("SIGAS Digital")
    st.write(f"**Prof. Sergio Cruz**")
    menu = st.radio("MENÚ", ["📝 Registro de Notas", "🎖️ Méritos/Deméritos"])

# --- PESTAÑA NOTAS (CON CÁLCULO AUTOMÁTICO) ---
if menu == "📝 Registro de Notas":
    st.header("Calificaciones - 5° D")
    df = st.session_state.db
    # Cálculo automático del promedio salvadoreño
    df["Promedio"] = (df["Act1"]*0.35 + df["Act2"]*0.35 + df["Prueba"]*0.30).round(1)
    
    st.write("Edite las notas abajo y presione el botón de abajo para guardar en Excel.")
    df_editado = st.data_editor(df[["Nombre", "Act1", "Act2", "Prueba", "Promedio"]], hide_index=True)
    
    if st.button("🚀 GUARDAR EN GOOGLE SHEETS"):
        with st.spinner("Sincronizando con Excel..."):
            try:
                # Sincronizamos el estado actual de la base de datos completa
                st.session_state.db.update(df_editado)
                datos_json = st.session_state.db.to_dict('records')
                respuesta = requests.post(URL_API, data=json.dumps(datos_json))
                if respuesta.status_code == 200:
                    st.success("¡Datos guardados con éxito en su Google Sheets!")
                else:
                    st.error("Error al conectar con el servidor de Google.")
            except Exception as e:
                st.error(f"Fallo de conexión: {e}")

# --- PESTAÑA MÉRITOS (CON LETRA VISIBLE) ---
elif menu == "🎖️ Méritos/Deméritos":
    st.header("Control de Conducta")
    for idx, row in st.session_state.db.iterrows():
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            st.markdown(f"""
                <div class="student-card">
                    <div style="display: flex; align-items: center;">
                        <div class="avatar">{row['Nombre'][0]}</div>
                        <div>
                            <div class="student-name">{row['Nombre']}</div>
                            <div class="student-stats">M: {row['Meritos']} | D: {row['Demeritos']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button(f"👍", key=f"m{idx}"):
                st.session_state.db.at[idx, 'Meritos'] += 1
                st.rerun()
        with col3 if 'col3' in locals() else c3: # Corrección de nombre de columna
             if c3.button(f"👎", key=f"d{idx}"):
                st.session_state.db.at[idx, 'Demeritos'] += 1
                st.rerun()
    
    st.write("---")
    if st.button("💾 GUARDAR MÉRITOS EN EXCEL"):
        datos_json = st.session_state.db.to_dict('records')
        requests.post(URL_API, data=json.dumps(datos_json))
        st.success("Conducta sincronizada.")
