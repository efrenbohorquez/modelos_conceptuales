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
    cat_features = ['Branch', 'City', 'Customer type', 'Gender', 'Payment']
    num_features = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
    target = 'Product line'
    X = df[cat_features + num_features]
    y = df[target]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ])
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
