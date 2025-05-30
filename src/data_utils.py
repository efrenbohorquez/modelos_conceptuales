# src/data_utils.py
"""
Utilidades para manejo de datos y corrección de problemas de serialización
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Any

def fix_pyarrow_serialization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige problemas de serialización PyArrow en Streamlit
    
    Args:
        df: DataFrame con posibles problemas de serialización
        
    Returns:
        DataFrame con tipos de datos optimizados para Streamlit
    """
    df_fixed = df.copy()
    
    for col in df_fixed.columns:
        # Manejar fechas problemáticas
        if df_fixed[col].dtype == 'object':
            # Intentar detectar si es una fecha en formato string
            try:
                # Verificar si parece una fecha (formato MM/DD/YYYY)
                sample_val = str(df_fixed[col].iloc[0])
                if '/' in sample_val and len(sample_val.split('/')) == 3:
                    # Convertir a datetime y luego a string optimizado
                    df_fixed[col] = pd.to_datetime(df_fixed[col], errors='ignore').dt.strftime('%Y-%m-%d')
                    continue
            except:
                pass
            
            # Para otros objetos, asegurar que sean strings
            df_fixed[col] = df_fixed[col].astype(str)
        
        # Manejar tipos de datos numéricos problemáticos
        elif pd.api.types.is_integer_dtype(df_fixed[col]):
            # Convertir enteros a int64 estándar
            df_fixed[col] = df_fixed[col].astype('int64')
        
        elif pd.api.types.is_float_dtype(df_fixed[col]):
            # Convertir flotantes a float64 estándar
            df_fixed[col] = df_fixed[col].astype('float64')
    
    return df_fixed

def optimize_dataframe_for_streamlit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimiza un DataFrame para uso en Streamlit eliminando problemas de serialización
    
    Args:
        df: DataFrame original
        
    Returns:
        DataFrame optimizado
    """
    try:
        # Aplicar correcciones de serialización
        df_optimized = fix_pyarrow_serialization(df)
        
        # Mensaje informativo para el usuario
        st.sidebar.info("🔧 **Optimización aplicada:** Tipos de datos compatibles con Streamlit")
        
        return df_optimized
        
    except Exception as e:
        st.warning(f"⚠️ No se pudo optimizar el DataFrame: {e}")
        return df

def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Valida la calidad de los datos y retorna un resumen
    
    Args:
        df: DataFrame a validar
        
    Returns:
        dict: Resumen de calidad de datos
    """
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'null_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.value_counts().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns)
    }
    
    return quality_report

def display_data_quality_summary(df: pd.DataFrame):
    """
    Muestra un resumen de calidad de datos en Streamlit
    
    Args:
        df: DataFrame a analizar
    """
    quality = validate_data_quality(df)
    
    st.markdown("### 📊 Resumen de Calidad de Datos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Registros", f"{quality['total_rows']:,}")
    
    with col2:
        st.metric("📑 Columnas", quality['total_columns'])
    
    with col3:
        null_percentage = (quality['null_values'] / (quality['total_rows'] * quality['total_columns'])) * 100
        st.metric("❌ Valores Nulos", f"{quality['null_values']} ({null_percentage:.1f}%)")
    
    with col4:
        st.metric("💾 Memoria (MB)", f"{quality['memory_usage']:.2f}")
    
    # Información adicional en expander
    with st.expander("🔍 Detalles de Calidad", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tipos de Datos:**")
            for dtype, count in quality['data_types'].items():
                st.write(f"- {dtype}: {count} columnas")
        
        with col2:
            st.write("**Resumen:**")
            st.write(f"- Variables Numéricas: {quality['numeric_columns']}")
            st.write(f"- Variables Categóricas: {quality['categorical_columns']}")
            st.write(f"- Filas Duplicadas: {quality['duplicate_rows']}")

def safe_dataframe_display(df: pd.DataFrame, title: str = "DataFrame", max_rows: int = 1000):
    """
    Muestra un DataFrame de manera segura en Streamlit
    
    Args:
        df: DataFrame a mostrar
        title: Título para mostrar
        max_rows: Número máximo de filas a mostrar
    """
    try:
        # Optimizar el DataFrame antes de mostrarlo
        df_optimized = optimize_dataframe_for_streamlit(df)
        
        # Limitar filas si es muy grande
        if len(df_optimized) > max_rows:
            st.warning(f"⚠️ Mostrando las primeras {max_rows} filas de {len(df_optimized)} totales")
            df_display = df_optimized.head(max_rows)
        else:
            df_display = df_optimized
        
        # Mostrar el DataFrame
        st.dataframe(df_display, use_container_width=True)
        
        return df_optimized
        
    except Exception as e:
        st.error(f"❌ Error al mostrar {title}: {e}")
        return df
