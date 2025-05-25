"""Módulo para el modelo de segmentación de clientes.

Este módulo contiene funciones para preprocesar datos, aplicar PCA para
reducción de dimensionalidad (simulando embeddings de autoencoder),
y luego usar KMeans para agrupar clientes en segmentos. También incluye
una función para caracterizar los segmentos resultantes.
"""
# Este módulo está alineado y documentado según la arquitectura conceptual.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Any, Dict, List

# Función para preparar los datos para clustering/autoencoder
def preparar_datos_segmentacion(df: pd.DataFrame) -> Tuple[np.ndarray, ColumnTransformer]:
    """Prepara los datos para el modelo de segmentación (clustering).

    Identifica dinámicamente características categóricas y numéricas del DataFrame
    proporcionado (que ya debería contener solo las características seleccionadas
    por el usuario para la segmentación). Realiza preprocesamiento como
    One-Hot Encoding para categóricas y escalado estándar para numéricas.

    Args:
        df (pd.DataFrame): DataFrame de entrada con las características
                           seleccionadas para la segmentación.

    Returns:
        Tuple[np.ndarray, ColumnTransformer]:
            - X_processed (np.ndarray): Matriz de características procesadas.
            - preprocessor (ColumnTransformer): Objeto ColumnTransformer ajustado.
    """
    X = df.copy() # df already contains user-selected variables for segmentation

    # Identificar dinámicamente características categóricas y numéricas
    cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    num_features = X.select_dtypes(include=np.number).columns.tolist()

    # Preprocesamiento: imputación, codificación y escalado
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))

    if not transformers:
        # Si no hay características para procesar, X se devuelve sin transformar
        # Esto puede ocurrir si el df de entrada no tiene tipos 'object', 'category' o numéricos.
        # O si está vacío. El código subsiguiente (PCA, KMeans) podría necesitar manejo de este caso.
        # Por ahora, si no hay transformadores, X_processed será X y preprocessor un objeto no ajustado.
        # ColumnTransformer([]) es válido y fit_transform devolverá X sin cambios.
        pass
        
    preprocessor = ColumnTransformer(transformers)
    X_processed = preprocessor.fit_transform(X)
    return X_processed, preprocessor

# Función para segmentar clientes usando KMeans sobre reducción PCA (simulación de autoencoder)
def segmentar_clientes(df: pd.DataFrame, 
                       n_clusters: int = 3, 
                       pca_n_components: int = 6
                       ) -> Tuple[pd.DataFrame, KMeans, PCA, ColumnTransformer]:
    """Segmenta clientes usando PCA para reducción y KMeans para clustering.

    Preprocesa los datos, aplica PCA para reducir la dimensionalidad, y luego
    utiliza KMeans para agrupar los datos transformados en el número especificado
    de clusters. Añade una columna 'Segmento' al DataFrame original.

    Args:
        df (pd.DataFrame): DataFrame de entrada con las características.
        n_clusters (int): Número de clusters a formar.
        pca_n_components (int): Número de componentes principales para PCA.

    Returns:
        Tuple[pd.DataFrame, KMeans, PCA, ColumnTransformer]:
            - df_segmentado (pd.DataFrame): DataFrame original con una columna
              adicional 'Segmento'.
            - kmeans_model (KMeans): El modelo KMeans ajustado.
            - pca_model (PCA): El modelo PCA ajustado.
            - preprocessor (ColumnTransformer): El preprocesador ajustado.
    """
    X_processed, preprocessor = preparar_datos_segmentacion(df) # X_processed is the data ready for PCA
    
    # Asegurarse de que pca_n_components no sea mayor que el número de características en X_processed
    if pca_n_components > X_processed.shape[1]:
        # Este caso debería manejarse idealmente en app.py, pero como salvaguarda:
        pca_n_components = X_processed.shape[1]

    # Reducción de dimensionalidad (simulación de embeddings de autoencoder)
    pca = PCA(n_components=pca_n_components, random_state=42)
    X_latent = pca.fit_transform(X_processed) # Use X_processed here
    
    # Kmeans se aplica sobre los datos transformados por PCA (X_latent)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10) # Added n_init for future versions
    clusters = kmeans.fit_predict(X_latent)
    df_segmentado = df.copy()
    df_segmentado['Segmento'] = clusters
    return df_segmentado, kmeans, pca, preprocessor

# Función para caracterizar segmentos
def caracterizar_segmentos(df_segmentado: pd.DataFrame) -> pd.DataFrame:
    """Calcula estadísticas descriptivas para cada segmento de clientes.

    Agrupa el DataFrame por la columna 'Segmento' y calcula la media y conteo
    para 'Total', y la moda (valor más frecuente) para 'Product line',
    'Customer type', y 'Gender'.

    Args:
        df_segmentado (pd.DataFrame): DataFrame que incluye una columna 'Segmento'
                                      y las características originales.

    Returns:
        pd.DataFrame: Un DataFrame con las características agregadas por segmento.
    """
    return df_segmentado.groupby('Segmento').agg({
        'Total': ['mean', 'count'],
        'Product line': lambda x: x.value_counts().index[0],
        'Customer type': lambda x: x.value_counts().index[0],
        'Gender': lambda x: x.value_counts().index[0]
    })
