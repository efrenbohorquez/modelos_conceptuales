# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import streamlit as st
from typing import Optional
import os
import sys

# Asegurar que podamos importar desde el directorio src
try:
    from dataset_generator import SupermarketDatasetGenerator
except ImportError:
    # Si falla, agregar el directorio actual al path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from dataset_generator import SupermarketDatasetGenerator

# Ruta principal del dataset
DATASET_PATH = 'data/supermarket_sales.xlsx'
DATASET_BACKUP_PATH = 'data/test_supermarket_data.csv'

def cargar_datos(archivo_subido=None):
    """
    Carga datos desde el dataset de supermercado o archivo subido.
    
    Args:
        archivo_subido: Archivo subido por el usuario (opcional)
    
    Returns:
        pandas.DataFrame: Dataset cargado
    """
    if archivo_subido:
        # Cargar archivo subido por el usuario
        try:
            if archivo_subido.name.endswith('.xlsx'):
                df = pd.read_excel(archivo_subido)
            elif archivo_subido.name.endswith('.csv'):
                df = pd.read_csv(archivo_subido)
            else:
                st.error("❌ Formato de archivo no soportado")
                return None
            
            st.success(f"✅ Archivo cargado: {len(df)} registros")
            return df
        except Exception as e:
            st.error(f"❌ Error cargando archivo: {e}")
            return None
    
    # Intentar cargar el dataset principal
    if os.path.exists(DATASET_PATH):
        df = _cargar_archivo(DATASET_PATH)
        if df is not None:
            st.info(f"📊 Dataset principal cargado: {len(df)} registros")
            return df
    
    # Si no existe el principal, usar el backup
    if os.path.exists(DATASET_BACKUP_PATH):
        df = _cargar_archivo(DATASET_BACKUP_PATH)
        if df is not None:
            st.warning(f"📋 Usando dataset de respaldo: {len(df)} registros")
            return df
    
    # Como último recurso, generar datos sintéticos
    st.warning("⚠️ Generando datos sintéticos para la demostración")
    try:
        generator = SupermarketDatasetGenerator()
        df = generator.generar_dataset_completo()
        st.info(f"🧪 Datos sintéticos generados: {len(df)} registros")
        return df
    except Exception as e:
        st.error(f"❌ Error generando datos sintéticos: {e}")
        return None

def _cargar_archivo(ruta: str):
    """Carga un archivo específico con manejo de errores y optimización de tipos"""
    try:
        if ruta.endswith('.xlsx'):
            df = pd.read_excel(ruta)
        elif ruta.endswith('.csv'):
            df = pd.read_csv(ruta)
        else:
            # Auto-detectar formato
            try:
                df = pd.read_excel(ruta)
            except:
                df = pd.read_csv(ruta)
        
        # Optimizar tipos de datos para evitar problemas de PyArrow
        for col in df.columns:
            if df[col].dtype == 'object':
                # Mantener strings como strings optimizados
                df[col] = df[col].astype(str)
            elif pd.api.types.is_integer_dtype(df[col]):
                df[col] = df[col].astype('int64')
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].astype('float64')
        
        return df
        
    except Exception as e:
        st.error(f"Error al cargar {ruta}: {e}")
        return None

def generar_dataset_automatico():
    """
    Genera automáticamente un dataset sintético para el análisis
    """
    try:
        generator = SupermarketDatasetGenerator()
        df = generator.generate_synthetic_dataset(n_records=1000, output_dir="data/datasets/processed")
        st.success("✅ Dataset sintético generado exitosamente")
        return df
    except Exception as e:
        st.error(f"Error al generar dataset sintético: {e}")
        return None

def verificar_dataset_real():
    """
    Verifica si el dataset principal está disponible y retorna información básica.
    """
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_excel(DATASET_PATH)
            return {
                'disponible': True,
                'registros': len(df),
                'columnas': list(df.columns),
                'ruta': DATASET_PATH,
                'tamaño_mb': round(os.path.getsize(DATASET_PATH) / 1024 / 1024, 2)
            }
        except Exception as e:
            return {
                'disponible': False,
                'error': str(e),
                'ruta': DATASET_PATH
            }
    else:
        return {
            'disponible': False,
            'ruta': DATASET_PATH,
            'mensaje': 'Archivo no encontrado'
        }

def verificar_datasets_disponibles():
    """
    Verifica los datasets disponibles en el proyecto
    """
    datasets_info = {}
    
    # Verificar dataset principal
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_excel(DATASET_PATH)
            datasets_info['principal'] = {
                'disponible': True,
                'registros': len(df),
                'columnas': len(df.columns),
                'ruta': DATASET_PATH,
                'tamaño_mb': round(os.path.getsize(DATASET_PATH) / 1024 / 1024, 2)
            }
        except Exception as e:
            datasets_info['principal'] = {
                'disponible': False,
                'error': str(e),
                'ruta': DATASET_PATH
            }
    else:
        datasets_info['principal'] = {
            'disponible': False,
            'ruta': DATASET_PATH,
            'mensaje': 'Archivo no encontrado'
        }
    
    # Verificar dataset de respaldo
    if os.path.exists(DATASET_BACKUP_PATH):
        try:
            df = pd.read_csv(DATASET_BACKUP_PATH)
            datasets_info['respaldo'] = {
                'disponible': True,
                'registros': len(df),
                'columnas': len(df.columns),
                'ruta': DATASET_BACKUP_PATH,
                'tamaño_mb': round(os.path.getsize(DATASET_BACKUP_PATH) / 1024 / 1024, 2)
            }
        except Exception as e:
            datasets_info['respaldo'] = {
                'disponible': False,
                'error': str(e),
                'ruta': DATASET_BACKUP_PATH
            }
    else:
        datasets_info['respaldo'] = {
            'disponible': False,
            'ruta': DATASET_BACKUP_PATH,
            'mensaje': 'Archivo no encontrado'
        }
    
    return datasets_info

def inicializar_datasets():
    """
    Inicializa los datasets del proyecto, generando datos sintéticos si es necesario
    """
    datasets_info = verificar_datasets_disponibles()
    
    # Si no hay dataset principal ni de respaldo, generar uno sintético
    if (not datasets_info.get('principal', {}).get('disponible', False) and 
        not datasets_info.get('respaldo', {}).get('disponible', False)):
        
        st.info("🔄 No se encontraron datasets. Generando dataset sintético...")
        try:
            generator = SupermarketDatasetGenerator()
            df = generator.generate_synthetic_dataset(n_records=1000, output_dir="data")
            st.success("✅ Dataset sintético generado exitosamente")
            return verificar_datasets_disponibles()
        except Exception as e:
            st.error(f"Error al generar dataset sintético: {e}")
    
    return datasets_info
