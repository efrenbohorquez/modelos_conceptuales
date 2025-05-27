#!/usr/bin/env python3
"""
Script de prueba para verificar que las correcciones del dashboard funcionan correctamente.
"""

import sys
import os
import pandas as pd

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Verificar que todas las importaciones funcionen."""
    try:
        import streamlit as st
        import plotly.express as px
        import plotly.graph_objects as go
        from src.eda import create_eda_visualizations
        print("✅ Todas las importaciones exitosas")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_data_loading():
    """Verificar que los datos se puedan cargar."""
    try:
        # Verificar archivo de datos principal
        data_file = "data/test_supermarket_data.csv"
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            print(f"✅ Datos principales cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            return True
        else:
            print(f"❌ Archivo de datos no encontrado: {data_file}")
            return False
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return False

def test_eda_module():
    """Verificar que el módulo EDA funcione."""
    try:
        from src.eda import create_eda_visualizations
        
        # Cargar datos de prueba
        data_file = "data/test_supermarket_data.csv"
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            
            # Intentar crear visualizaciones
            figs = create_eda_visualizations(df)
            print(f"✅ Módulo EDA funcional: {len(figs)} visualizaciones creadas")
            return True
        else:
            print("❌ No se pueden probar visualizaciones sin datos")
            return False
    except Exception as e:
        print(f"❌ Error en módulo EDA: {e}")
        return False

def main():
    """Ejecutar todas las pruebas."""
    print("🔍 Iniciando pruebas del dashboard corregido...")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Carga de datos", test_data_loading),
        ("Módulo EDA", test_eda_module)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Probando: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron! El dashboard debería funcionar correctamente.")
        print("👉 Para ejecutar el dashboard:")
        print("   streamlit run app.py --server.port 8506")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar los errores arriba.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
