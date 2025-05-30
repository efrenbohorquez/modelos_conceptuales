# -*- coding: utf-8 -*-
"""
MAPEO DE COLUMNAS PARA COMPATIBILIDAD
=====================================

Mapea las columnas del dataset actual a las columnas esperadas por los modelos
para mantener compatibilidad sin cambiar los algoritmos ML.
"""

def mapear_columnas_dataset(df):
    """
    Mapea las columnas del dataset actual a las columnas esperadas por los modelos ML.
    
    Maneja múltiples formatos de dataset de supermercado:
    - Dataset estándar de Kaggle (supermarket_sales.xlsx)
    - Dataset personalizado en español
    - Otros formatos comunes
    
    Args:
        df (pandas.DataFrame): Dataset con columnas originales
        
    Returns:
        pandas.DataFrame: Dataset con columnas mapeadas para compatibilidad
    """
    
    # Mapeo principal: columnas comunes -> inglés (esperado por los modelos)
    mapeo_columnas = {
        # Mapeo para dataset estándar de Kaggle
        'Invoice ID': 'Invoice ID',  # Mantener
        'Branch': 'Branch',  # Ya correcto
        'City': 'City',      # Ya correcto
        'Customer type': 'Customer type',  # Ya correcto
        'Gender': 'Gender',  # Ya correcto
        'Product line': 'Product line',  # Ya correcto
        'Unit price': 'Unit price',  # Ya correcto
        'Quantity': 'Quantity',  # Ya correcto
        'Tax 5%': 'Tax 5%',  # Ya correcto
        'Total': 'Total',    # Ya correcto
        'Date': 'Date',      # Ya correcto
        'Time': 'Time',      # Ya correcto
        'Payment': 'Payment', # Ya correcto
        'cogs': 'cogs',      # Ya correcto
        'gross margin percentage': 'gross margin percentage',  # Mantener
        'gross income': 'gross income',  # Ya correcto
        'Rating': 'Rating',  # Ya correcto
        
        # Mapeo para dataset en español (si existe)
        'tienda_id': 'Branch',
        'ciudad': 'City',
        'genero_cliente': 'Gender', 
        'categoria': 'Product line',
        'metodo_pago': 'Payment',
        'frecuencia_compra': 'Customer type',
        'canal_marketing': 'City',  # Backup para City si no existe
        'precio': 'Unit price',
        'cantidad_vendida': 'Quantity', 
        'descuento': 'Tax 5%',
        'total': 'Total',
        'costo_producto': 'cogs',
        'margen': 'gross income',
        'satisfaccion_cliente': 'Rating',
        'calificacion': 'Rating',
        
        # Mapeo adicional para variaciones comunes
        'producto': 'Product line',
        'linea_producto': 'Product line',
        'tipo_cliente': 'Customer type',
        'sucursal': 'Branch',
        'tienda': 'Branch',
        'sexo': 'Gender',
        'genero': 'Gender',
        'precio_unitario': 'Unit price',
        'cantidad': 'Quantity',
        'impuesto': 'Tax 5%',
        'fecha': 'Date',
        'hora': 'Time',
        'pago': 'Payment',
        'forma_pago': 'Payment',
        'ingreso_bruto': 'gross income',
        'margen_bruto': 'gross income'
    }
    
    # Crear una copia del dataframe original
    df_mapped = df.copy()
    
    # Aplicar mapeo solo si la columna original existe y la nueva no existe
    for col_orig, col_nuevo in mapeo_columnas.items():
        if col_orig in df_mapped.columns and col_nuevo not in df_mapped.columns:
            df_mapped[col_nuevo] = df_mapped[col_orig]
    
    # Calcular columnas derivadas necesarias
    if 'precio' in df.columns and 'cantidad_vendida' in df.columns:
        df_mapped['Total'] = df['precio'] * df['cantidad_vendida']
        
    if 'costo_producto' in df.columns and 'cantidad_vendida' in df.columns:
        df_mapped['cogs'] = df['costo_producto'] * df['cantidad_vendida']
        
    if 'margen' in df.columns and 'cantidad_vendida' in df.columns:
        df_mapped['gross income'] = df['margen'] * df['cantidad_vendida']
    
    # Asegurar que tengamos las columnas necesarias con valores por defecto
    columnas_requeridas = {
        'Branch': df_mapped.get('tienda_id', 'T001'),
        'City': df_mapped.get('canal_marketing', 'Email'), 
        'Customer type': df_mapped.get('frecuencia_compra', 'Normal'),
        'Gender': df_mapped.get('genero_cliente', 'M'),
        'Product line': df_mapped.get('categoria', 'General'),
        'Payment': df_mapped.get('metodo_pago', 'Cash'),
        'Unit price': df_mapped.get('precio', 10.0),
        'Quantity': df_mapped.get('cantidad_vendida', 1),
        'Tax 5%': df_mapped.get('descuento', 0.05),
        'Total': df_mapped.get('Total', 10.0),
        'cogs': df_mapped.get('cogs', 8.0),
        'gross income': df_mapped.get('gross income', 2.0),
        'Rating': df_mapped.get('satisfaccion_cliente', 4.0)
    }
    
    # Añadir columnas faltantes
    for col, valor_default in columnas_requeridas.items():
        if col not in df_mapped.columns:
            if isinstance(valor_default, str):
                df_mapped[col] = valor_default
            else:
                df_mapped[col] = valor_default
    
    return df_mapped

def verificar_columnas_disponibles(df, columnas_requeridas):
    """
    Verifica qué columnas están disponibles y cuáles faltan.
    
    Args:
        df (pandas.DataFrame): Dataset a verificar
        columnas_requeridas (list): Lista de columnas necesarias
        
    Returns:
        dict: Información sobre columnas disponibles y faltantes    """
    disponibles = [col for col in columnas_requeridas if col in df.columns]
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    return {
        'columnas_encontradas': disponibles,
        'columnas_faltantes': faltantes,
        'porcentaje_disponible': len(disponibles) / len(columnas_requeridas) * 100
    }
