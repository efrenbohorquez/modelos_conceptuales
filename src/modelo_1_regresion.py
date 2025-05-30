# Modelo 1: Predicción de la Calificación del Cliente (Regresión)
# Este módulo implementa el modelo de regresión descrito en docs/modelos_conceptuales.md
# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.impute import SimpleImputer

# Función para preparar los datos para regresión
def preparar_datos_regresion(df):
    # Variables ideales para regresión
    ideal_cat_features = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
    ideal_num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    target = 'Rating'
    
    # Verificar disponibilidad de columnas
    available_columns = list(df.columns)
    
    # Verificar que el target existe
    if target not in available_columns:
        raise ValueError(f"Columna objetivo '{target}' no encontrada en el dataset")
    
    # Filtrar características disponibles
    cat_features = [col for col in ideal_cat_features if col in available_columns]
    num_features = [col for col in ideal_num_features if col in available_columns]
    
    # Asegurar que tenemos al menos algunas características
    if len(cat_features) == 0:
        cat_features = [col for col in available_columns if df[col].dtype == 'object' and col != target][:6]
    
    if len(num_features) < 2:
        num_features = [col for col in available_columns 
                       if pd.api.types.is_numeric_dtype(df[col]) and col != target][:6]
    
    all_features = cat_features + num_features
    
    if len(all_features) == 0:
        raise ValueError("No se encontraron características válidas para regresión")
    
    X = df[all_features].copy()
    y = df[target].copy()

    # Crear preprocesador dinámicamente
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))
    
    preprocessor = ColumnTransformer(transformers)

    X_processed = preprocessor.fit_transform(X)
    return X_processed, y, preprocessor

# Función para crear y entrenar el modelo de regresión
def entrenar_regresion(df):
    X, y, preprocessor = preparar_datos_regresion(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MLPRegressor(hidden_layer_sizes=(128, 64, 32), activation='relu', max_iter=500, random_state=42)
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
