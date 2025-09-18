import streamlit as st
from frontend import home_view, aritmetica_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa", 
    layout="wide"
)

# ====== BARRA LATERAL ======
st.sidebar.title("📂 Navegación")
modulo = st.sidebar.selectbox(
    "Selecciona un módulo",
    ["Home", "Álgebra"]
)

# ====== RUTEO SIMPLE ======
if modulo == "Home":
    home_view.render()
elif modulo == "Álgebra":
    aritmetica_view.render()
