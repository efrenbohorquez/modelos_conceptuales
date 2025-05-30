#!/usr/bin/env python3
"""
Script para probar el flujo completo del análisis EDA
"""

import pandas as pd
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.getcwd())

from src import data_loader

def test_eda_flow():
    """Prueba el flujo completo de EDA sin Streamlit"""
    print("🔄 Cargando datos...")
    
    # Cargar datos
    df = data_loader.cargar_datos()
    
    if df is None:
        print("❌ Error: No se pudieron cargar los datos")
        return False
    
    print(f"✅ Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
    
    # Verificar variables numéricas
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    print(f"\n📊 Variables numéricas encontradas: {len(num_cols)}")
    
    if len(num_cols) > 0:
        print("Variables disponibles:")
        for i, col in enumerate(num_cols, 1):
            print(f"  {i}. {col}")
        
        # Verificar que están las variables esperadas
        expected_vars = ['Unit price', 'Quantity', 'Tax 5%', 'Total']
        found_vars = [var for var in expected_vars if var in num_cols]
        
        print(f"\n✅ Variables esperadas encontradas: {len(found_vars)}/{len(expected_vars)}")
        print(f"Variables encontradas: {found_vars}")
        
        if len(found_vars) == len(expected_vars):
            print("🎉 ¡Todas las variables esperadas están presentes!")
            return True
        else:
            missing = [var for var in expected_vars if var not in found_vars]
            print(f"⚠️ Variables faltantes: {missing}")
            return False
    else:
        print("❌ No se encontraron variables numéricas")
        return False

if __name__ == "__main__":
    print("🧪 Prueba de Flujo EDA - Variables Numéricas")
    print("=" * 50)
    
    success = test_eda_flow()
    
    if success:
        print("\n✅ El flujo EDA funciona correctamente")
        print("💡 La sección 'Selecciona variables numéricas para análisis detallado' debería aparecer en el dashboard")
    else:
        print("\n❌ Hay problemas en el flujo EDA")
