import streamlit as st
from backend import aritmetica

def render():
    st.header("🧮 Aritmética")
    a = st.number_input("Número A", value=0.0)
    b = st.number_input("Número B", value=0.0)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sumar"):
            st.success(f"Resultado: {aritmetica.sumar(a, b)}")
    with col2:
        if st.button("Dividir"):
            st.info(f"Resultado: {aritmetica.division(a, b)}")
