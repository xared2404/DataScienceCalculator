import streamlit as st
from backend import aritmetica

def render():
    st.header("🧮 Suma de dos números")
    a = st.number_input("Número A", value=0.0)
    b = st.number_input("Número B", value=0.0)
    if st.button("Sumar"):
        st.success(f"Resultado: {aritmetica.sumar(a, b)}")
