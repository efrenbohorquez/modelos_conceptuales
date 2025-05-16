# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

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

# Función para preparar los datos para clustering/autoencoder
def preparar_datos_segmentacion(df):
    cat_features = ['Customer type', 'Gender', 'Product line', 'Payment']
    num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    X = df[cat_features + num_features]
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ])
    X_processed = preprocessor.fit_transform(X)
    return X_processed, preprocessor

# Función para segmentar clientes usando KMeans sobre reducción PCA (simulación de autoencoder)
def segmentar_clientes(df, n_clusters=3):
    X, preprocessor = preparar_datos_segmentacion(df)
    # Reducción de dimensionalidad (simulación de embeddings de autoencoder)
    pca = PCA(n_components=6, random_state=42)
    X_latent = pca.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_latent)
    df_segmentado = df.copy()
    df_segmentado['Segmento'] = clusters
    return df_segmentado, kmeans, pca, preprocessor

# Función para caracterizar segmentos
def caracterizar_segmentos(df_segmentado):
    return df_segmentado.groupby('Segmento').agg({
        'Total': ['mean', 'count'],
        'Product line': lambda x: x.value_counts().index[0],
        'Customer type': lambda x: x.value_counts().index[0],
        'Gender': lambda x: x.value_counts().index[0]
    })
