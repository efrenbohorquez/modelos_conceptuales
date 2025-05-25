"""Módulo para detección de anomalías usando Isolation Forest.

Este módulo implementa un modelo avanzado de detección de anomalías utilizando
el algoritmo Isolation Forest. Es adecuado para identificar observaciones
atípicas en conjuntos de datos multivariados, siendo útil para detectar
fraudes, errores de captura o comportamientos inusuales.

Características principales:
- Utiliza Isolation Forest, basado en árboles aleatorios.
- No requiere que las variables sigan una distribución específica.
- El parámetro `contamination` permite ajustar la proporción esperada de anomalías.
"""
# Este módulo está alineado y documentado según la arquitectura conceptual.

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report # Not used by current functions but kept if planned
from typing import Tuple, List, Any # Ensure List is imported

# Función para preparar los datos para detección de anomalías
def preparar_datos_anomalias(df: pd.DataFrame, variables: List[str]) -> Tuple[np.ndarray, ColumnTransformer]:
    """Prepara los datos para el modelo de detección de anomalías.

    Selecciona las `variables` especificadas del DataFrame, identifica
    características categóricas y numéricas dentro de estas variables,
    y aplica preprocesamiento (One-Hot Encoding y escalado estándar).

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        variables (List[str]): Lista de nombres de columnas a utilizar
                               como características.

    Returns:
        Tuple[np.ndarray, ColumnTransformer]:
            - X_processed (np.ndarray): Matriz de características procesadas.
            - preprocessor (ColumnTransformer): Objeto ColumnTransformer ajustado.
    """
    cat_features = [col for col in variables if df[col].dtype == 'object']
    num_features = [col for col in variables if df[col].dtype != 'object']
    
    # Create a copy of the DataFrame sliced with the selected variables to avoid SettingWithCopyWarning
    X_subset = df[variables].copy()

    # Define transformers, ensuring they are only added if features of that type exist
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))

    if not transformers: # If no features to process, perhaps return original data or handle error
        # For now, ColumnTransformer handles empty list correctly, returning X as is.
        # If X_subset is empty or has no processable dtypes, X_processed might be empty or unchanged.
        pass

    preprocessor = ColumnTransformer(transformers)
    X_processed = preprocessor.fit_transform(X_subset)
    return X_processed, preprocessor

# Modelo avanzado: Isolation Forest para detección de anomalías
def detectar_anomalias(df: pd.DataFrame, 
                       variables: List[str], 
                       contamination: float = 0.05
                       ) -> Tuple[pd.DataFrame, IsolationForest, ColumnTransformer]:
    """Detecta anomalías en un DataFrame usando el algoritmo Isolation Forest.

    Preprocesa los datos utilizando `preparar_datos_anomalias`, luego entrena
    un modelo IsolationForest y predice qué filas son anomalías. Añade una
    columna 'Anomalía' ('Sí'/'No') al DataFrame original.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        variables (List[str]): Lista de nombres de columnas a utilizar para
                               la detección de anomalías.
        contamination (float): Proporción esperada de anomalías en el conjunto
                               de datos. Parámetro para IsolationForest.

    Returns:
        Tuple[pd.DataFrame, IsolationForest, ColumnTransformer]:
            - df_result (pd.DataFrame): DataFrame original con una columna
              adicional 'Anomalía'.
            - model (IsolationForest): El modelo IsolationForest entrenado.
            - preprocessor (ColumnTransformer): El preprocesador ajustado.
    """
    X_processed, preprocessor = preparar_datos_anomalias(df, variables)
    model = IsolationForest(n_estimators=200, contamination=contamination, random_state=42)
    model.fit(X)
    pred = model.predict(X)
    # -1 es anomalía, 1 es normal
    df_result = df.copy()
    df_result['Anomalía'] = np.where(pred == -1, 'Sí', 'No')
    return df_result, model, preprocessor

# Ejemplo de uso en notebook o script:
# df_anom, modelo, preproc = detectar_anomalias(df, variables, contamination=0.05)
# print(df_anom[df_anom['Anomalía']=='Sí'])
