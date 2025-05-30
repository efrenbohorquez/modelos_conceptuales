#!/usr/bin/env python3
"""Test del mapeo de columnas para verificar la compatibilidad"""

from src.mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles
import pandas as pd

def main():
    # Cargar el dataset de prueba
    print("🔍 Cargando dataset de prueba...")
    df = pd.read_csv('data/test_supermarket_data.csv')
    print(f"✅ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"📋 Columnas originales: {list(df.columns)}")
    
    # Verificar si necesita mapeo
    print("\n🔍 Verificando necesidad de mapeo...")
    columnas_requeridas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
    info_columnas = verificar_columnas_disponibles(df, columnas_requeridas)
    print(f"📊 Porcentaje de columnas disponibles: {info_columnas['porcentaje_disponible']}%")
    print(f"✅ Columnas encontradas: {info_columnas['columnas_encontradas']}")
    print(f"❌ Columnas faltantes: {info_columnas['columnas_faltantes']}")
    
    if info_columnas['porcentaje_disponible'] < 50:
        print("\n🔄 Aplicando mapeo de columnas...")
        df_mapped = mapear_columnas_dataset(df)
        print(f"✅ Mapeo completado: {df_mapped.shape[0]} filas, {df_mapped.shape[1]} columnas")
        print(f"📋 Columnas después del mapeo: {list(df_mapped.columns)}")
        
        # Verificar que las columnas requeridas estén disponibles
        print("\n🔍 Verificando columnas después del mapeo...")
        info_despues = verificar_columnas_disponibles(df_mapped, columnas_requeridas)
        print(f"📊 Porcentaje disponible después del mapeo: {info_despues['porcentaje_disponible']}%")
        print(f"✅ Columnas encontradas: {info_despues['columnas_encontradas']}")
        print(f"❌ Columnas faltantes: {info_despues['columnas_faltantes']}")
        
        # Verificar columnas específicas para cada modelo
        print("\n🔍 Verificando columnas para modelos específicos...")
        
        # Modelo 1: Regresión (necesita Rating)
        rating_disponible = 'Rating' in df_mapped.columns
        print(f"🎯 Modelo Regresión - Rating disponible: {'✅' if rating_disponible else '❌'}")
        
        # Modelo 2: Segmentación (necesita variables numéricas)
        numeric_cols = df_mapped.select_dtypes(include=['number']).columns.tolist()
        print(f"📊 Modelo Segmentación - Variables numéricas disponibles: {len(numeric_cols)} ({numeric_cols})")
        
        # Modelo 3: Clasificación (necesita Product line)
        product_line_disponible = 'Product line' in df_mapped.columns
        print(f"🏷️ Modelo Clasificación - Product line disponible: {'✅' if product_line_disponible else '❌'}")
        
        # Modelo 4: Anomalías (puede usar cualquier variable)
        total_vars = len(df_mapped.columns)
        print(f"🔍 Modelo Anomalías - Variables totales disponibles: {total_vars}")
        
        return df_mapped
    else:
        print("✅ No se necesita mapeo, las columnas ya están en el formato correcto")
        return df

if __name__ == "__main__":
    result_df = main()
    print(f"\n🎉 Proceso completado. Dataset final tiene {result_df.shape[1]} columnas.")
