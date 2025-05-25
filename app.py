"""Aplicación Streamlit para demostración de modelos de Machine Learning.

Esta aplicación permite a los usuarios cargar datos de ventas de supermercados,
realizar un análisis descriptivo y aplicar diversos modelos de Machine Learning
como regresión, segmentación, clasificación y detección de anomalías.
Los usuarios pueden interactuar con los modelos ajustando hiperparámetros
y visualizando los resultados.
"""
# Este archivo está alineado y documentado según la arquitectura conceptual.

import streamlit as st
import pandas as pd
from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias

st.set_page_config(page_title="Modelos Conceptuales Supermercado", layout="wide", initial_sidebar_state="expanded")

def load_css(file_name: str):
    """Carga y aplica un archivo CSS a la aplicación Streamlit.

    Args:
        file_name (str): La ruta al archivo CSS que se va a cargar.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_markdown_from_file(file_path: str):
    """Lee un archivo Markdown y lo muestra en la aplicación Streamlit.

    Si el archivo no se encuentra, muestra una advertencia en la aplicación.

    Args:
        file_path (str): La ruta al archivo Markdown.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        st.markdown(markdown_content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Advertencia: No se pudo encontrar el archivo de documentación: {file_path}")

load_css("assets/styles.css")

st.markdown('<div class="main-title">Modelos Conceptuales de Redes Neuronales para Supermercados</div>', unsafe_allow_html=True)

st.sidebar.header("Carga de datos")
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
    display_markdown_from_file("docs/modelos_conceptuales.md")
    st.markdown('<div class="subtitle">Selecciona y ejecuta el modelo de tu interés</div>', unsafe_allow_html=True)
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
        elif not set(['Rating']).issubset(set(variables + ['Rating'])): # Ensure 'Rating' is part of selected variables for the model
            st.warning("Debes incluir la variable 'Rating' en la selección para poder entrenar el modelo de regresión.")
        else:
            st.markdown("##### Hiperparámetros para MLPRegressor")
            hidden_layer_sizes_str_reg = st.text_input("Tamaños de capas ocultas (MLP Regresión - ej: 128,64,32)", value="128,64,32", key="hls_reg")
            max_iter_reg = st.number_input("Máximo de iteraciones (MLP Regresión)", min_value=100, max_value=1000, value=500, step=50, key="max_iter_reg")
            activation_reg = st.selectbox("Función de activación (MLP Regresión)", options=['relu', 'tanh', 'logistic'], index=0, key="act_reg")

            if st.button("Entrenar modelo de regresión"):
                with st.spinner("Entrenando modelo..."):
                    try:
                        # Parse hidden_layer_sizes
                        parsed_hidden_layers_reg = tuple(map(int, hidden_layer_sizes_str_reg.split(',')))
                    except ValueError:
                        st.warning(f"Error al parsear tamaños de capas ocultas '{hidden_layer_sizes_str_reg}'. Usando valor por defecto (128,64,32).")
                        parsed_hidden_layers_reg = (128, 64, 32)
                    
                    try:
                        # Prepare df_subset for regression model making sure only selected variables are passed
                        df_subset_reg = df[variables].copy() # Start with user-selected variables
                        if 'Rating' not in df_subset_reg.columns: # Add Rating if not already selected by user in multiselect
                             df_subset_reg['Rating'] = df['Rating']
                        
                        modelo, preproc, resultados = modelo_1_regresion.entrenar_regresion(
                            df_subset_reg.dropna(), # df_subset_reg has selected vars + 'Rating'
                            hidden_layer_sizes=parsed_hidden_layers_reg,
                            max_iter=max_iter_reg,
                            activation=activation_reg
                        )
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
            st.markdown("##### Hiperparámetros para Segmentación")
            n_clusters = st.slider("Número de segmentos (KMeans)", min_value=2, max_value=8, value=3, key="n_clusters_seg")
            
            # Max PCA components should be min(num_samples, num_features)
            # df[variables].dropna() is the input to the model
            df_segment_input = df[variables].dropna()
            max_pca_val = min(df_segment_input.shape[0], df_segment_input.shape[1])
            
            if max_pca_val < 2: # PCA needs at least 2 components, and also input features
                st.warning(f"Se necesitan al menos 2 características (y muestras) para PCA. Actualmente hay {df_segment_input.shape[1]} características y {df_segment_input.shape[0]} muestras después de eliminar NAs.")
                pca_n_components = 2 # Default to 2, but it might fail if max_pca_val is 0 or 1
            else:
                pca_n_components = st.number_input("Número de Componentes PCA", min_value=2, max_value=max_pca_val, value=min(6, max_pca_val), step=1, key="pca_comp_seg")

            if st.button("Ejecutar segmentación"):
                with st.spinner("Segmentando clientes..."):
                    try:
                        if df_segment_input.shape[1] < pca_n_components: # Double check before running
                            st.error(f"El número de componentes PCA ({pca_n_components}) no puede ser mayor que el número de características disponibles ({df_segment_input.shape[1]}). Ajustando a {df_segment_input.shape[1]}.")
                            pca_n_components = df_segment_input.shape[1]
                        
                        df_seg, kmeans, pca, preproc = modelo_2_segmentacion.segmentar_clientes(
                            df_segment_input, # Use the already prepared df
                            n_clusters=n_clusters,
                            pca_n_components=pca_n_components
                        )
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
            st.markdown("##### Hiperparámetros para MLPClassifier")
            hidden_layer_sizes_str_cls = st.text_input("Tamaños de capas ocultas (MLP Clasificación - ej: 128,64,32)", value="128,64,32", key="hls_cls")
            max_iter_cls = st.number_input("Máximo de iteraciones (MLP Clasificación)", min_value=100, max_value=1000, value=500, step=50, key="max_iter_cls")
            activation_cls = st.selectbox("Función de activación (MLP Clasificación)", options=['relu', 'tanh', 'logistic'], index=0, key="act_cls")

            if st.button("Entrenar modelo de clasificación"):
                with st.spinner("Entrenando modelo..."):
                    try:
                        # Parse hidden_layer_sizes
                        parsed_hidden_layers_cls = tuple(map(int, hidden_layer_sizes_str_cls.split(',')))
                    except ValueError:
                        st.warning(f"Error al parsear tamaños de capas ocultas '{hidden_layer_sizes_str_cls}'. Usando valor por defecto (128,64,32).")
                        parsed_hidden_layers_cls = (128, 64, 32)

                    try:
                        # Prepare df_subset for classification model
                        df_subset_cls = df[variables].copy() # Start with user-selected variables
                        if 'Product line' not in df_subset_cls.columns: # Add Product line if not already selected
                             df_subset_cls['Product line'] = df['Product line']

                        modelo, preproc, resultados = modelo_3_clasificacion.entrenar_clasificacion(
                            df_subset_cls.dropna(), # df_subset_cls has selected vars + 'Product line'
                            hidden_layer_sizes=parsed_hidden_layers_cls,
                            max_iter=max_iter_cls,
                            activation=activation_cls
                        )
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
        # The detailed explanation for Isolation Forest is now part of docs/modelos_conceptuales.md
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
