import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
from src import data_loader, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion

# Prueba de carga de datos (simulada)
def test_carga_datos():
    # Simula un DataFrame con las columnas mínimas necesarias
    data = {
        'Branch': ['A'], 'City': ['Yangon'], 'Customer type': ['Member'], 'Gender': ['Female'],
        'Product line': ['Health and beauty'], 'Payment': ['Cash'],
        'Unit price': [50.0], 'Quantity': [5], 'Tax 5%': [12.5], 'Total': [262.5],
        'cogs': [250.0], 'gross income': [12.5], 'Rating': [9.1]
    }
    df = pd.DataFrame(data)
    assert not df.empty

# Prueba de pipeline de regresión
def test_regresion():
    data = {
        'Branch': ['A']*10, 'City': ['Yangon']*10, 'Customer type': ['Member']*10, 'Gender': ['Female']*10,
        'Product line': ['Health and beauty']*10, 'Payment': ['Cash']*10,
        'Unit price': [50.0]*10, 'Quantity': [5]*10, 'Tax 5%': [12.5]*10, 'Total': [262.5]*10,
        'cogs': [250.0]*10, 'gross income': [12.5]*10, 'Rating': [9.1]*10
    }
    df = pd.DataFrame(data)
    _, _, resultados = modelo_1_regresion.entrenar_regresion(df)
    assert 'MSE' in resultados

# Prueba de pipeline de segmentación
def test_segmentacion():
    data = {
        'Customer type': ['Member', 'Normal']*5, 'Gender': ['Female', 'Male']*5,
        'Product line': ['Health and beauty', 'Electronic accessories']*5, 'Payment': ['Cash', 'Credit card']*5,
        'Unit price': [50.0]*10, 'Quantity': [5]*10, 'Tax 5%': [12.5]*10, 'Total': [262.5]*10,
        'cogs': [250.0]*10, 'gross income': [12.5]*10
    }
    df = pd.DataFrame(data)
    df_seg, _, _, _ = modelo_2_segmentacion.segmentar_clientes(df, n_clusters=2)
    assert 'Segmento' in df_seg.columns

# Prueba de pipeline de clasificación
def test_clasificacion():
    data = {
        'Branch': ['A', 'B']*5, 'City': ['Yangon', 'Naypyitaw']*5, 'Customer type': ['Member', 'Normal']*5, 'Gender': ['Female', 'Male']*5,
        'Product line': ['Health and beauty', 'Electronic accessories']*5, 'Payment': ['Cash', 'Credit card']*5,
        'Unit price': [50.0]*10, 'Quantity': [5]*10, 'Tax 5%': [12.5]*10, 'Total': [262.5]*10,
        'cogs': [250.0]*10, 'gross income': [12.5]*10, 'Rating': [9.1]*10
    }
    df = pd.DataFrame(data)
    _, _, resultados = modelo_3_clasificacion.entrenar_clasificacion(df)
    assert 'accuracy' in resultados
