# Este archivo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import streamlit as st
import pandas as pd
from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias

st.set_page_config(page_title="Modelos Conceptuales Supermercado", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
    body, .main, .stApp {
        background-color: #ffffff !important;
        color: #222 !important;
    }
    .main-title {
        font-size:2.5rem;
        font-weight:bold;
        color:#2c3e50;
        margin-bottom:0.5em;
    }
    .subtitle {
        font-size:1.3rem;
        color:#34495e;
        margin-bottom:0.5em;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        margin: 0.5em 0;
    }
    .stButton>button:hover {
        background-color: #217dbb;
        color: #ecf0f1;
    }
    .stDataFrame, .stTable {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.5em;
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">Modelos Conceptuales de Redes Neuronales para Supermercados</div>', unsafe_allow_html=True)

st.sidebar.header("Carga de datos")
try:
    st.sidebar.image("data/logo_uc.png", width=120)
except Exception:
    st.sidebar.warning("No se pudo cargar el logo institucional. Verifica que 'data/logo_uc.png' exista.")
st.sidebar.markdown('<div class="subtitle">Maestría en Analítica de Datos<br>Universidad Central</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="subtitle">Carga de datos</div>', unsafe_allow_html=True)
archivo = st.sidebar.file_uploader("Sube tu archivo de datos (xlsx)", type=["xlsx"])

df = None
if archivo:
    df = data_loader.cargar_datos(archivo)
    st.success("Datos cargados correctamente.")
else:
    st.info("Por favor, sube un archivo de datos para comenzar.")

if df is not None:
    st.header("Análisis Descriptivo")
    st.markdown('<div class="subtitle">Explora los datos antes de aplicar los modelos</div>', unsafe_allow_html=True)
    eda.analisis_descriptivo(df)
    st.header("Modelos Propuestos")
    st.markdown('<div class="subtitle">Selecciona y ejecuta el modelo de tu interés</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#eaf2fb; border-radius:8px; padding:1em; margin-bottom:1em;'>
    <b>Explicación de los modelos y conceptos de redes neuronales aplicados:</b><br><br>
    <ul>
    <li><b>Regresión (MLPRegressor):</b> Utiliza un perceptrón multicapa (red neuronal feedforward) para predecir la calificación del cliente. El modelo aprende relaciones no lineales entre variables transaccionales/demográficas y la calificación, usando capas ocultas y activación ReLU.</li>
    <li><b>Segmentación (PCA + KMeans):</b> Simula el uso de autoencoders (redes neuronales para reducción de dimensionalidad) mediante PCA para obtener una representación latente de los datos y luego agrupa clientes con KMeans. Los autoencoders permiten encontrar patrones complejos y PCA es una aproximación clásica.</li>
    <li><b>Clasificación (MLPClassifier):</b> Implementa una red neuronal multicapa para predecir la próxima línea de producto. Utiliza softmax en la salida para clasificación multiclase y aprende límites de decisión complejos mediante retropropagación.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    # Permitir selección de variables
    st.markdown('<div class="subtitle">Selecciona las variables de entrada para los modelos</div>', unsafe_allow_html=True)
    variables = st.multiselect("Variables disponibles:", options=list(df.columns), default=list(df.columns), key="var_select")
    opcion = st.selectbox("Selecciona un modelo:", [
        "Regresión: Predicción de Calificación",
        "Segmentación de Clientes",
        "Clasificación de Producto",
        "Detección de Anomalías (Isolation Forest)"
    ], key="modelo_select")
    if opcion == "Regresión: Predicción de Calificación":
        st.subheader("Modelo de Regresión (MLPRegressor)")
        if 'Rating' not in df.columns:
            st.warning("La variable 'Rating' es necesaria para este modelo. Selecciona un archivo de datos que la contenga.")
        elif not set(['Rating']).issubset(set(variables + ['Rating'])):
            st.warning("Debes incluir la variable 'Rating' en la selección para poder entrenar el modelo de regresión.")
        else:
            if st.button("Entrenar modelo de regresión"):
                with st.spinner("Entrenando modelo..."):
                    try:
                        modelo, preproc, resultados = modelo_1_regresion.entrenar_regresion(df[variables + ['Rating']].dropna())
                        st.success("Entrenamiento finalizado.")
                        st.write(f"**MSE:** {resultados['MSE']:.3f}")
                        st.write(f"**MAE:** {resultados['MAE']:.3f}")
                        st.write(f"**R2:** {resultados['R2']:.3f}")
                        st.line_chart({"Real": resultados['y_test'].values, "Predicción": resultados['y_pred']})
                        # Importancia de variables
                        st.subheader("Importancia de variables")
                        if hasattr(modelo, 'feature_importances_'):
                            importancias = modelo.feature_importances_
                        elif hasattr(modelo, 'coefs_'):
                            import numpy as np
                            importancias = np.abs(modelo.coefs_[0]).sum(axis=1)
                        else:
                            importancias = None
                        if importancias is not None:
                            try:
                                feature_names = preproc.get_feature_names_out()
                            except Exception:
                                feature_names = [f"var_{i}" for i in range(len(importancias))]
                            imp_df = pd.DataFrame({"Variable": feature_names, "Importancia": importancias})
                            imp_df = imp_df.sort_values("Importancia", ascending=False)
                            st.bar_chart(imp_df.set_index("Variable"))
                        else:
                            st.info("El modelo no permite calcular importancia de variables directamente.")
                    except Exception as e:
                        st.error(f"No es posible analizar la selección de variables con el modelo de regresión. Detalle: {e}")
            st.info("El modelo utiliza las variables seleccionadas para predecir la calificación del cliente.")
    elif opcion == "Segmentación de Clientes":
        st.subheader("Segmentación de Clientes (PCA + KMeans)")
        if len(variables) < 2:
            st.warning("Selecciona al menos dos variables para realizar la segmentación.")
        else:
            n_clusters = st.slider("Número de segmentos", min_value=2, max_value=8, value=3)
            if st.button("Ejecutar segmentación"):
                with st.spinner("Segmentando clientes..."):
                    try:
                        df_seg, kmeans, pca, preproc = modelo_2_segmentacion.segmentar_clientes(df[variables].dropna(), n_clusters=n_clusters)
                        caracteristicas = modelo_2_segmentacion.caracterizar_segmentos(df_seg)
                        st.success("Segmentación completada.")
                        st.write("Vista previa de segmentos:")
                        st.dataframe(df_seg[['Segmento'] + [col for col in df_seg.columns if col != 'Segmento']].head())
                        st.write("Características por segmento:")
                        st.dataframe(caracteristicas)
                        st.write("Visualización PCA de segmentos:")
                        import matplotlib.pyplot as plt
                        import seaborn as sns
                        fig, ax = plt.subplots()
                        pca_coords = pca.transform(preproc.transform(df[variables]))
                        sns.scatterplot(x=pca_coords[:,0], y=pca_coords[:,1], hue=df_seg['Segmento'], palette='Set2', ax=ax)
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"No es posible analizar la selección de variables con el modelo de segmentación. Detalle: {e}")
            st.info("La segmentación utiliza las variables seleccionadas para agrupar clientes en segmentos homogéneos.")
    elif opcion == "Clasificación de Producto":
        st.subheader("Clasificación de la Siguiente Línea de Producto (MLPClassifier)")
        if 'Product line' not in df.columns:
            st.warning("La variable 'Product line' es necesaria para este modelo. Selecciona un archivo de datos que la contenga.")
        elif not set(['Product line']).issubset(set(variables + ['Product line'])):
            st.warning("Debes incluir la variable 'Product line' en la selección para poder entrenar el modelo de clasificación.")
        else:
            if st.button("Entrenar modelo de clasificación"):
                with st.spinner("Entrenando modelo..."):
                    try:
                        modelo, preproc, resultados = modelo_3_clasificacion.entrenar_clasificacion(df[variables + ['Product line']].dropna())
                        st.success("Entrenamiento finalizado.")
                        st.write(f"**Exactitud (accuracy):** {resultados['accuracy']:.3f}")
                        st.write("Reporte de clasificación:")
                        st.dataframe(pd.DataFrame(resultados['reporte']).transpose())
                        st.write("Matriz de confusión:")
                        import matplotlib.pyplot as plt
                        import seaborn as sns
                        fig, ax = plt.subplots()
                        sns.heatmap(resultados['matriz_confusion'], annot=True, fmt='d', cmap='Blues', ax=ax)
                        ax.set_xlabel('Predicción')
                        ax.set_ylabel('Real')
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"No es posible analizar la selección de variables con el modelo de clasificación. Detalle: {e}")
            st.info("El modelo utiliza las variables seleccionadas para predecir la próxima línea de producto.")
    elif opcion == "Detección de Anomalías (Isolation Forest)":
        st.subheader("Detección de Anomalías con Isolation Forest")
        st.markdown('''
        <div style='background:#f9f9e3; border-radius:8px; padding:1em; margin-bottom:1em;'>
        <b>Descripción del modelo:</b><br>
        Isolation Forest es un algoritmo basado en árboles aleatorios que identifica observaciones atípicas (anómalas) en conjuntos de datos multivariados. Es eficiente para grandes volúmenes de datos y no requiere que las variables sigan una distribución específica.<br>
        - Aísla observaciones mediante divisiones aleatorias; las que requieren menos divisiones para ser aisladas son consideradas anomalías.<br>
        - Útil para detectar fraudes, errores de captura y comportamientos inusuales.<br>
        - El parámetro <b>contamination</b> controla la proporción esperada de anomalías.
        </div>
        ''', unsafe_allow_html=True)
        if len(variables) < 1:
            st.warning("Selecciona al menos una variable para detectar anomalías.")
        else:
            contamination = st.slider("Proporción esperada de anomalías", min_value=0.01, max_value=0.2, value=0.05, step=0.01)
            if st.button("Detectar anomalías"):
                with st.spinner("Detectando anomalías..."):
                    try:
                        df_anom, modelo, preproc = modelo_4_anomalias.detectar_anomalias(df[variables].dropna(), variables, contamination)
                        st.success("Detección completada.")
                        st.write("Vista previa de anomalías detectadas:")
                        st.dataframe(df_anom.head())
                        st.write(f"Total de anomalías detectadas: {sum(df_anom['Anomalía']=='Sí')}")
                        st.write("Distribución de anomalías:")
                        st.bar_chart(df_anom['Anomalía'].value_counts())
                    except Exception as e:
                        st.error(f"No es posible analizar la selección de variables con el modelo de anomalías. Detalle: {e}")
            st.info("El modelo utiliza Isolation Forest para detectar registros atípicos en las variables seleccionadas.")
    else:
        st.warning("Funcionalidad próximamente disponible.")
