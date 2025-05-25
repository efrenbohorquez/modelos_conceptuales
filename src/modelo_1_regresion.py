"""Módulo para el modelo de regresión (predicción de calificación de clientes).

Este módulo contiene funciones para preprocesar los datos, entrenar un modelo
de regresión MLP (Multi-layer Perceptron) y evaluar su rendimiento.
El objetivo es predecir la calificación ('Rating') de un cliente.
"""
# Modelo 1: Predicción de la Calificación del Cliente (Regresión)
# Este módulo implementa el modelo de regresión descrito en docs/modelos_conceptuales.md
# Este módulo está alineado y documentado según la arquitectura conceptual.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.impute import SimpleImputer
from typing import Tuple, Any, Dict, List

# Función para preparar los datos para regresión
def preparar_datos_regresion(df: pd.DataFrame) -> Tuple[np.ndarray, pd.Series, ColumnTransformer]:
    """Prepara los datos para el modelo de regresión.

    Identifica dinámicamente características categóricas y numéricas,
    realiza preprocesamiento como One-Hot Encoding para categóricas y
    escalado estándar para numéricas. La columna objetivo 'Rating' se separa.

    Args:
        df (pd.DataFrame): DataFrame de entrada que contiene las características
                           y la columna objetivo 'Rating'.

    Returns:
        Tuple[np.ndarray, pd.Series, ColumnTransformer]:
            - X_processed (np.ndarray): Matriz de características procesadas.
            - y (pd.Series): Serie de la variable objetivo ('Rating').
            - preprocessor (ColumnTransformer): Objeto ColumnTransformer ajustado
              utilizado para el preprocesamiento.
    
    Raises:
        ValueError: Si la columna 'Rating' no se encuentra en el DataFrame.
    """
    target = 'Rating'
    
    # Asegurarse de que la columna target exista antes de intentar accederla o dropearla
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in DataFrame.")
        
    y = df[target]
    X = df.drop(columns=[target])

    # Identificar dinámicamente características categóricas y numéricas
    cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    num_features = X.select_dtypes(include=np.number).columns.tolist()

    # Preprocesamiento: imputación, codificación y escalado
    # Asegurarse de que solo se incluyan transformadores si hay características de ese tipo
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))
    
    if not transformers:
        # Si no hay características para procesar, devolver X tal cual o manejar como error
        # En este caso, si X está vacío o no tiene tipos procesables, podría ser un problema
        # Devolver X_processed como X, y el preprocesador como None o un objeto no ajustado
        # Esto dependerá de cómo el código subsiguiente maneje un preprocesador vacío.
        # Por ahora, asumimos que siempre habrá características para procesar,
        # o que ColumnTransformer maneja listas vacías de features (lo cual hace).
        pass

    preprocessor = ColumnTransformer(transformers)

    X_processed = preprocessor.fit_transform(X)
    return X_processed, y, preprocessor

# Función para crear y entrenar el modelo de regresión
def entrenar_regresion(df: pd.DataFrame, 
                       hidden_layer_sizes: Tuple[int, ...] = (128, 64, 32), 
                       max_iter: int = 500, 
                       activation: str = 'relu'
                       ) -> Tuple[MLPRegressor, ColumnTransformer, Dict[str, Any]]:
    """Entrena un modelo de regresión MLP y evalúa su rendimiento.

    Utiliza la función `preparar_datos_regresion` para preprocesar los datos,
    luego divide los datos en conjuntos de entrenamiento y prueba, entrena
    un MLPRegressor y calcula métricas de evaluación (MSE, MAE, R2).

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        hidden_layer_sizes (Tuple[int, ...]): Arquitectura de las capas ocultas
                                               del MLPRegressor.
        max_iter (int): Número máximo de iteraciones para el entrenamiento.
        activation (str): Función de activación para las capas ocultas.

    Returns:
        Tuple[MLPRegressor, ColumnTransformer, Dict[str, Any]]:
            - model (MLPRegressor): El modelo MLPRegressor entrenado.
            - preprocessor (ColumnTransformer): El preprocesador ajustado.
            - resultados (Dict[str, Any]): Un diccionario con las métricas de
              evaluación ('MSE', 'MAE', 'R2') y los datos de prueba
              ('y_test', 'y_pred').
    """
    X, y, preprocessor = preparar_datos_regresion(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MLPRegressor(
        hidden_layer_sizes=hidden_layer_sizes, 
        activation=activation, 
        max_iter=max_iter, 
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    resultados = {
        'MSE': mean_squared_error(y_test, y_pred),
        'MAE': mean_absolute_error(y_test, y_pred),
        'R2': r2_score(y_test, y_pred),
        'y_test': y_test,
        'y_pred': y_pred
    }
    return model, preprocessor, resultados
