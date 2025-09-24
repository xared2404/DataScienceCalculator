import streamlit as st
from backend import aritmetica

def render():
    st.header("➗ División de dos números")
    a = st.number_input("Número A", value=0.0)
    b = st.number_input("Número B", value=0.0)
    if st.button("Dividir"):
        st.info(f"Resultado: {aritmetica.division(a, b)}")
