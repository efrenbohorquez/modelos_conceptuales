# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def analisis_descriptivo(df: pd.DataFrame):
    st.write('Vista previa de los datos:')
    st.dataframe(df.head())
    st.write('Descripción estadística:')
    st.dataframe(df.describe(include='all'))
    # Distribución de variables numéricas
    st.subheader('Distribución de variables numéricas')
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) > 0:
        cols = st.columns(3)
        for i, col in enumerate(num_cols):
            with cols[i % 3]:
                fig, ax = plt.subplots(figsize=(3,2))
                sns.histplot(df[col].dropna(), kde=True, ax=ax, color='#3498db')
                ax.set_title(f'{col}')
                st.pyplot(fig)
    # Distribución de variables categóricas
    st.subheader('Distribución de variables categóricas')
    cat_cols = df.select_dtypes(include='object').columns
    if len(cat_cols) > 0:
        cols = st.columns(3)
        for i, col in enumerate(cat_cols):
            with cols[i % 3]:
                fig, ax = plt.subplots(figsize=(3,2))
                df[col].value_counts().plot(kind='bar', ax=ax, color='#34495e')
                ax.set_title(f'{col}')
                st.pyplot(fig)
    # Matriz de correlación
    if len(num_cols) > 1:
        st.subheader('Matriz de correlación')
        fig, ax = plt.subplots(figsize=(8, 4))
        corr = df[num_cols].corr()
        sns.heatmap(corr, annot=True, cmap='Blues', ax=ax)
        st.pyplot(fig)
    # Valores nulos
    st.subheader('Valores nulos por columna')
    st.dataframe(df.isnull().sum().reset_index().rename(columns={0:'Nulos', 'index':'Columna'}))
