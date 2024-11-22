import streamlit as st
import pandas as pd

st.title("Prueba Inicial del Proyecto Chakana")
st.write("¡El entorno virtual está funcionando correctamente!")
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
st.write(df)