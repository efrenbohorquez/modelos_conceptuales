import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def analisis_descriptivo(df: pd.DataFrame):
    st.write('Vista previa de los datos:')
    st.dataframe(df.head())
    st.write('Descripción estadística:')
    st.dataframe(df.describe(include='all'))
    st.write('Distribución de la variable "Rating":')
    fig, ax = plt.subplots()
    sns.histplot(df['Rating'], kde=True, ax=ax)
    st.pyplot(fig)
