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
    # Verificar que el DataFrame no esté vacío
    if df.empty:
        raise ValueError("El DataFrame está vacío")
    
    # Columnas ideales para segmentación
    ideal_cat_features = ['Customer type', 'Gender', 'Product line', 'Payment']
    ideal_num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    
    # Verificar qué columnas están realmente disponibles
    available_columns = list(df.columns)
    
    # Filtrar solo las columnas que existen en el DataFrame
    cat_features = [col for col in ideal_cat_features if col in available_columns]
    num_features = [col for col in ideal_num_features if col in available_columns]
    
    # Si no hay suficientes columnas, usar alternativas
    if len(cat_features) == 0:
        # Buscar cualquier columna categórica disponible
        cat_features = [col for col in available_columns if df[col].dtype == 'object'][:4]
    
    if len(num_features) < 2:
        # Buscar cualquier columna numérica disponible
        numeric_cols = [col for col in available_columns if pd.api.types.is_numeric_dtype(df[col])]
        num_features = numeric_cols[:6] if len(numeric_cols) >= 6 else numeric_cols
    
    # Crear el conjunto de características
    all_features = cat_features + num_features
    
    if len(all_features) == 0:
        raise ValueError("No se encontraron características válidas para segmentación")
    
    # Asegurar que las columnas seleccionadas existan y no tengan valores nulos problemáticos
    for col in all_features:
        if col not in df.columns:
            raise ValueError(f"La columna {col} no existe en el DataFrame")
    
    X = df[all_features].copy()
    
    # Manejar valores nulos
    for col in cat_features:
        if col in X.columns:
            X[col] = X[col].fillna('Unknown')
    
    for col in num_features:
        if col in X.columns:
            X[col] = X[col].fillna(X[col].median())
    
    # Crear preprocesador solo con las columnas disponibles
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))
    
    if not transformers:
        raise ValueError("No se pueden crear transformadores para las características")
    
    preprocessor = ColumnTransformer(transformers)
    
    try:
        X_processed = preprocessor.fit_transform(X)
        return X_processed, preprocessor
    except Exception as e:
        raise ValueError(f"Error en el preprocesamiento: {str(e)}")
    
    preprocessor = ColumnTransformer(transformers)
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
    # Verificar qué columnas están disponibles para caracterización
    available_cols = df_segmentado.columns.tolist()
    
    # Crear caracterización básica por segmento
    try:
        # Contar número de elementos por segmento
        segment_summary = df_segmentado.groupby('Segmento').size().to_frame('count')
        
        # Agregar estadísticas para columnas numéricas disponibles
        numeric_cols = ['Total', 'Unit price', 'Quantity', 'Tax 5%', 'cogs', 'gross income', 'Rating']
        available_numeric = [col for col in numeric_cols if col in available_cols]
        
        if available_numeric:
            for col in available_numeric[:3]:  # Limitar a 3 columnas para evitar sobrecarga
                try:
                    segment_summary[f'{col}_mean'] = df_segmentado.groupby('Segmento')[col].mean()
                except Exception:
                    continue
        
        # Agregar moda para columnas categóricas disponibles
        categorical_cols = ['Product line', 'Customer type', 'Gender', 'Payment']
        available_categorical = [col for col in categorical_cols if col in available_cols]
        
        if available_categorical:
            for col in available_categorical[:2]:  # Limitar a 2 columnas categóricas
                try:
                    segment_summary[f'{col}_mode'] = df_segmentado.groupby('Segmento')[col].apply(
                        lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else 'N/A'
                    )
                except Exception:
                    continue
        
        return segment_summary
        
    except Exception as e:
        # Fallback mínimo: solo contar elementos por segmento
        return df_segmentado.groupby('Segmento').size().to_frame('count')
