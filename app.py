import streamlit as st
from src import data_loader, eda

st.set_page_config(page_title="Modelos Conceptuales Supermercado", layout="wide")
st.title("Modelos Conceptuales de Redes Neuronales para Supermercados")

st.sidebar.header("Carga de datos")
archivo = st.sidebar.file_uploader("Sube tu archivo de datos (xlsx)", type=["xlsx"])

df = None
if archivo:
    df = data_loader.cargar_datos(archivo)
    st.success("Datos cargados correctamente.")
else:
    st.info("Por favor, sube un archivo de datos para comenzar.")

if df is not None:
    st.header("Análisis Descriptivo")
    eda.analisis_descriptivo(df)
    # Aquí se agregarán las opciones para los modelos
    st.header("Modelos Propuestos")
    st.write("Selecciona un modelo en el menú lateral para continuar.")
