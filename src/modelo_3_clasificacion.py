# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier

# Función para preparar los datos para clasificación
def preparar_datos_clasificacion(df):
    # Variables ideales para clasificación
    ideal_cat_features = ['Branch', 'City', 'Customer type', 'Gender', 'Payment']
    ideal_num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    target = 'Product line'
    
    # Verificar disponibilidad de columnas
    available_columns = list(df.columns)
    
    # Verificar que el target existe
    if target not in available_columns:
        raise ValueError(f"Columna objetivo '{target}' no encontrada en el dataset")
    
    # Filtrar características disponibles
    cat_features = [col for col in ideal_cat_features if col in available_columns]
    num_features = [col for col in ideal_num_features if col in available_columns]
    
    # Asegurar que tenemos características suficientes
    if len(cat_features) == 0:
        cat_features = [col for col in available_columns 
                       if df[col].dtype == 'object' and col != target][:5]
    
    if len(num_features) < 2:
        num_features = [col for col in available_columns 
                       if pd.api.types.is_numeric_dtype(df[col]) and col != target][:6]
    
    all_features = cat_features + num_features
    
    if len(all_features) == 0:
        raise ValueError("No se encontraron características válidas para clasificación")
    
    X = df[all_features].copy()
    y = df[target].copy()
    
    # Codificar el target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Crear preprocesador dinámicamente
    transformers = []
    if cat_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat_features))
    if num_features:
        transformers.append(('num', StandardScaler(), num_features))
    
    preprocessor = ColumnTransformer(transformers)
    X_processed = preprocessor.fit_transform(X)
    
    return X_processed, y_encoded, preprocessor, le

# Función para crear y entrenar el modelo de clasificación
def entrenar_clasificacion(df):
    X, y, preprocessor, le = preparar_datos_clasificacion(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu', max_iter=500, random_state=42)
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
