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
    # Variables categóricas y numéricas según la documentación conceptual
    cat_features = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
    num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    target = 'Rating'

    X = df[cat_features + num_features]
    y = df[target]

    # Preprocesamiento: imputación, codificación y escalado
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ])

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
