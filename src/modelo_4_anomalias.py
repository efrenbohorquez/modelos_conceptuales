# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

'''
Modelo avanzado: Isolation Forest para detección de anomalías
-----------------------------------------------------------
Este modelo utiliza el algoritmo Isolation Forest, una técnica basada en árboles aleatorios para identificar observaciones atípicas (anómalas) en conjuntos de datos multivariados. Es especialmente útil para grandes volúmenes de datos y no requiere que las variables sigan una distribución específica.

- El modelo aísla observaciones mediante divisiones aleatorias, y aquellas que requieren menos divisiones para ser aisladas son consideradas anomalías.
- Permite detectar fraudes, errores de captura, comportamientos inusuales y otros registros atípicos en datos de supermercados.
- El parámetro `contamination` controla la proporción esperada de anomalías en el conjunto de datos.
'''

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Función para preparar los datos para detección de anomalías
def preparar_datos_anomalias(df, variables):
    X = df[variables].copy()

    # Convertir todos los tipos de datos de manera simple y robusta
    for col in X.columns:
        if pd.api.types.is_datetime64_any_dtype(X[col]):
            # Convertir datetime a timestamp numérico
            X[col] = pd.to_datetime(X[col]).astype(np.int64) // 10**9
        elif X[col].dtype == 'object':
            # Convertir todos los objetos a string para evitar tipos mixtos
            X[col] = X[col].astype(str)
    
    # Identificar columnas numéricas y categóricas después de la conversión
    num_features = [col for col in X.columns if pd.api.types.is_numeric_dtype(X[col])]
    cat_features = [col for col in X.columns if col not in num_features]
    
    # Crear preprocesador
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))
    
    if not transformers:
        raise ValueError("No se encontraron variables válidas para procesar")
    
    preprocessor = ColumnTransformer(transformers)
    X_processed = preprocessor.fit_transform(X)
    return X_processed, preprocessor

# Modelo avanzado: Isolation Forest para detección de anomalías
def detectar_anomalias(df, variables, contamination=0.05):
    X, preprocessor = preparar_datos_anomalias(df, variables)
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
