import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
import numpy as np
from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion

# Sklearn specific imports for isinstance checks
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPRegressor, MLPClassifier

import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for matplotlib

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
    # Create a diverse DataFrame for regression test (14 rows)
    data_reg = {
        'Branch': ['A']*7 + ['B']*7, 
        'City': ['Yangon']*7 + ['Mandalay']*7,
        'Customer type': ['Member', 'Normal']*7, 
        'Gender': ['Female', 'Male']*7,
        'Product line': ['Health and beauty', 'Electronics']*7,
        'Payment': ['Cash', 'Credit card']*7,
        'Unit price': np.abs(np.random.randn(14))*50 + 10,
        'Quantity': np.random.randint(1, 5, 14),
        'Tax 5%': np.abs(np.random.randn(14))*5 + 1,
        'Total': np.abs(np.random.randn(14))*200 + 20,
        'cogs': np.abs(np.random.randn(14))*190 + 10,
        'gross income': np.abs(np.random.randn(14))*10 + 1,
        'Rating': np.random.rand(14)*6 + 4  # Ratings between 4 and 10
    }
    df_reg = pd.DataFrame(data_reg)
    
    # Call the regression model training function using default hyperparameters
    modelo, preprocessor, resultados = modelo_1_regresion.entrenar_regresion(df_reg)
    
    # Output Assertions
    assert isinstance(resultados, dict)
    assert isinstance(modelo, MLPRegressor)
    assert isinstance(preprocessor, ColumnTransformer) 
    assert isinstance(resultados['y_test'], np.ndarray)
    assert isinstance(resultados['y_pred'], np.ndarray)
    assert len(resultados['y_test']) == len(resultados['y_pred'])
    assert len(resultados['y_test']) > 0  # Test split was successful
    assert resultados['y_test'].ndim == 1
    assert resultados['y_pred'].ndim == 1
    assert isinstance(resultados['MSE'], float)
    assert isinstance(resultados['MAE'], float)
    assert isinstance(resultados['R2'], float)

# Prueba de pipeline de segmentación
def test_segmentacion():
    # Create a DataFrame for segmentation test (14 rows)
    data_seg = {
        'Customer type': ['Member', 'Normal']*7, 
        'Gender': ['Female', 'Male']*7,
        'Product line': ['Health and beauty', 'Electronics', 'Home & Lifestyle', 'Sports & Travel']*3 + ['Fashion accessories', 'Food and beverages'], 
        'Payment': ['Cash', 'Credit card', 'Ewallet']*4 + ['Cash', 'Credit card'],
        'Unit price': np.abs(np.random.randn(14))*50 + 10,
        'Quantity': np.random.randint(1, 5, 14),
        'Tax 5%': np.abs(np.random.randn(14))*5 + 1,
        'Total': np.abs(np.random.randn(14))*200 + 20,
        'cogs': np.abs(np.random.randn(14))*190 + 10,
        'gross income': np.abs(np.random.randn(14))*10 + 1
    }
    df_seg = pd.DataFrame(data_seg)

    # Call the segmentation model training function
    # Ensure pca_n_components is less than number of features (10 in this case for df_seg)
    df_result_seg, kmeans_model, pca_model, preprocessor = modelo_2_segmentacion.segmentar_clientes(df_seg, n_clusters=2, pca_n_components=3)
    
    # Output Assertions
    assert isinstance(df_result_seg, pd.DataFrame)
    assert 'Segmento' in df_result_seg.columns
    assert df_result_seg.shape[0] == df_seg.shape[0]
    assert pd.api.types.is_integer_dtype(df_result_seg['Segmento']) 
    assert sorted(list(df_result_seg['Segmento'].unique())) == [0, 1] 
    assert isinstance(kmeans_model, KMeans)
    assert isinstance(pca_model, PCA)
    assert isinstance(preprocessor, ColumnTransformer)

# Prueba de pipeline de clasificación
def test_clasificacion():
    # Create a DataFrame for classification test (30 rows)
    data_cls = {
        'Branch': ['A']*15 + ['B']*15, 
        'City': ['Yangon']*15 + ['Mandalay']*15,
        'Customer type': ['Member', 'Normal']*15, 
        'Gender': ['Female', 'Male']*15,
        'Product line': ['Electronic accessories']*10 + ['Home and lifestyle']*10 + ['Sports and travel']*10, # 30 rows, 3 classes
        'Payment': ['Cash', 'Credit card', 'Ewallet']*10,
        'Unit price': np.abs(np.random.randn(30))*50 + 10,
        'Quantity': np.random.randint(1, 5, 30),
        'Tax 5%': np.abs(np.random.randn(30))*5 + 1,
        'Total': np.abs(np.random.randn(30))*200 + 20,
        'cogs': np.abs(np.random.randn(30))*190 + 10,
        'gross income': np.abs(np.random.randn(30))*10 + 1,
        'Rating': np.random.rand(30)*6 + 4 
    }
    df_cls = pd.DataFrame(data_cls)

    # Call the classification model training function using default hyperparameters
    modelo, preprocessor, resultados = modelo_3_clasificacion.entrenar_clasificacion(df_cls)
    
    # Output Assertions
    assert isinstance(resultados, dict)
    assert isinstance(modelo, MLPClassifier)
    assert isinstance(preprocessor, ColumnTransformer) 
    assert isinstance(resultados['y_test'], np.ndarray)
    assert isinstance(resultados['y_pred'], np.ndarray)
    assert len(resultados['y_test']) == len(resultados['y_pred'])
    assert len(resultados['y_test']) > 0
    assert isinstance(resultados['accuracy'], float)
    assert 0.0 <= resultados['accuracy'] <= 1.0
    assert isinstance(resultados['matriz_confusion'], np.ndarray)
    assert resultados['matriz_confusion'].ndim == 2
    assert resultados['matriz_confusion'].shape[0] == resultados['matriz_confusion'].shape[1]
    assert resultados['matriz_confusion'].shape[0] == len(resultados['label_encoder'].classes_)
    assert isinstance(resultados['label_encoder'], LabelEncoder)
    
    unique_pred_labels = np.unique(resultados['y_pred'])
    valid_labels = np.arange(len(resultados['label_encoder'].classes_))
    assert all(label in valid_labels for label in unique_pred_labels)

def test_cargar_datos_excel():
    # Create dummy data and excel file for testing
    test_data_dir = "tests/data"
    # This directory should have been created in a previous step,
    # but we ensure it exists here for test atomicity.
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    dummy_file_path = os.path.join(test_data_dir, "dummy_data.xlsx")
    
    # Data for the dummy excel file
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [30, 24, 35],
            'City': ['New York', 'London', 'Paris']}
    df_expected = pd.DataFrame(data)
    
    # Create the dummy excel file using pandas ExcelWriter
    try:
        with pd.ExcelWriter(dummy_file_path, engine='openpyxl') as writer:
            df_expected.to_excel(writer, index=False, sheet_name='Sheet1')
    except ImportError:
        pytest.skip("openpyxl not installed, skipping excel test")
        return # Ensure test execution stops if openpyxl is not found

    # Test cargar_datos function with the created Excel file
    df_loaded = data_loader.cargar_datos(dummy_file_path)

    assert df_loaded is not None, "Failed to load data, DataFrame is None."
    assert isinstance(df_loaded, pd.DataFrame), "Loaded data is not a pandas DataFrame."
    # Use check_dtype=False as Excel might alter integer types (e.g. int64 to int32)
    pd.testing.assert_frame_equal(df_loaded, df_expected, check_dtype=False)

    # Test case for non-existent file
    df_non_existent = data_loader.cargar_datos("non_existent_file.xlsx")
    assert df_non_existent is None, "Should return None for non-existent file."
    
    # Optional: Clean up the dummy file.
    # For now, leaving it for inspection, especially if tests fail.
    # If running in CI, it's ephemeral. If local, gitignore should cover tests/data.
    # if os.path.exists(dummy_file_path):
    #     os.remove(dummy_file_path)

def test_analisis_descriptivo_runs():
    # Create a sample DataFrame
    data = {
        'NumericCol1': [1, 2, 3, 4, 5, None, 7], # Include None for isnull().sum() check
        'NumericCol2': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7],
        'CategoricalCol1': ['A', 'B', 'A', 'C', 'B', 'A', None], # Include None
        'CategoricalCol2': ['X', 'Y', 'X', 'Z', 'Y', 'Z', 'Y']
    }
    df_sample = pd.DataFrame(data)

    try:
        eda.analisis_descriptivo(df_sample)
        # If the function completes without error, the test implicitly passes for "runs without errors".
        assert True
    except Exception as e:
        pytest.fail(f"analisis_descriptivo raised an exception: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
