"""Módulo para el modelo de clasificación (predicción de línea de producto).

Este módulo contiene funciones para preprocesar los datos, entrenar un modelo
de clasificación MLP (Multi-layer Perceptron) y evaluar su rendimiento.
El objetivo es predecir la próxima línea de producto ('Product line')
que un cliente podría adquirir.
"""
# Este módulo está alineado y documentado según la arquitectura conceptual.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
from typing import Tuple, Any, Dict, List # Ensure List is imported if used for type hints

# Función para preparar los datos para clasificación
def preparar_datos_clasificacion(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, ColumnTransformer, LabelEncoder]:
    """Prepara los datos para el modelo de clasificación.

    Identifica dinámicamente características categóricas y numéricas.
    La variable objetivo 'Product line' se codifica usando LabelEncoder.
    Las características se preprocesan con One-Hot Encoding (categóricas)
    y escalado estándar (numéricas).

    Args:
        df (pd.DataFrame): DataFrame de entrada con características y la
                           columna objetivo 'Product line'.

    Returns:
        Tuple[np.ndarray, np.ndarray, ColumnTransformer, LabelEncoder]:
            - X_processed (np.ndarray): Matriz de características procesadas.
            - y_encoded (np.ndarray): Array de la variable objetivo codificada.
            - preprocessor (ColumnTransformer): Objeto ColumnTransformer ajustado.
            - le (LabelEncoder): Objeto LabelEncoder ajustado para la variable objetivo.

    Raises:
        ValueError: Si la columna 'Product line' no se encuentra en el DataFrame.
    """
    target = 'Product line'

    # Asegurarse de que la columna target exista
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in DataFrame.")

    y = df[target]
    X = df.drop(columns=[target])

    # Identificar dinámicamente características categóricas y numéricas
    cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    num_features = X.select_dtypes(include=np.number).columns.tolist()

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Preprocesamiento: imputación, codificación y escalado
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))

    if not transformers:
        # Similar al caso de regresión, manejar si no hay características para procesar.
        # ColumnTransformer([]) es válido.
        pass

    preprocessor = ColumnTransformer(transformers)
    X_processed = preprocessor.fit_transform(X)
    return X_processed, y_encoded, preprocessor, le

# Función para crear y entrenar el modelo de clasificación
def entrenar_clasificacion(df: pd.DataFrame, 
                           hidden_layer_sizes: Tuple[int, ...] = (128, 64, 32), 
                           max_iter: int = 500, 
                           activation: str = 'relu'
                           ) -> Tuple[MLPClassifier, ColumnTransformer, Dict[str, Any]]:
    """Entrena un modelo de clasificación MLP y evalúa su rendimiento.

    Utiliza `preparar_datos_clasificacion` para el preprocesamiento.
    Divide los datos, entrena un MLPClassifier y calcula métricas como
    exactitud, reporte de clasificación y matriz de confusión.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        hidden_layer_sizes (Tuple[int, ...]): Arquitectura de capas ocultas del MLP.
        max_iter (int): Número máximo de iteraciones para el entrenamiento.
        activation (str): Función de activación para capas ocultas.

    Returns:
        Tuple[MLPClassifier, ColumnTransformer, Dict[str, Any]]:
            - model (MLPClassifier): El modelo MLPClassifier entrenado.
            - preprocessor (ColumnTransformer): El preprocesador ajustado.
            - resultados (Dict[str, Any]): Diccionario con métricas de evaluación
              ('accuracy', 'reporte', 'matriz_confusion'), datos de prueba
              ('y_test', 'y_pred'), y el LabelEncoder ('label_encoder').
    """
    X, y, preprocessor, le = preparar_datos_clasificacion(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes, 
        activation=activation, 
        max_iter=max_iter, 
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    resultados = {
        'accuracy': accuracy_score(y_test, y_pred),
        'reporte': classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True),
        'matriz_confusion': confusion_matrix(y_test, y_pred),
        'y_test': y_test,
        'y_pred': y_pred,
        'label_encoder': le
    }
    return model, preprocessor, resultados
