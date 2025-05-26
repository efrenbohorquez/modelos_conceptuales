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
    X = df[variables].copy() # Usar .copy() para evitar SettingWithCopyWarning

    # Identificar tipos de columnas
    datetime_features = [col for col in variables if pd.api.types.is_datetime64_any_dtype(X[col])]
    cat_features = [col for col in variables if X[col].dtype == 'object' and col not in datetime_features]
    
    # Convertir columnas datetime a timestamp numérico
    for col in datetime_features:
        X[col] = X[col].astype(np.int64) // 10**9 # Convertir a segundos Unix

    # Actualizar lista de características numéricas para incluir las fechas convertidas
    num_features = [col for col in variables if (X[col].dtype != 'object' or col in datetime_features)]
    
    # Asegurarse de que las cat_features no estén en num_features si originalmente eran object pero no datetime
    # y viceversa, aunque la lógica anterior debería cubrirlo.
    # Re-evaluar cat_features para asegurar que solo sean strings después de la conversión de datetime
    cat_features = [col for col in cat_features if X[col].dtype == 'object']


    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ])
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
