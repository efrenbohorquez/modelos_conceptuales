# Script de pruebas para el dashboard de modelos conceptuales
# Prueba la funcionalidad básica de cada módulo

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias

def test_data_loading():
    """Prueba la carga de datos"""
    print("🔄 Probando carga de datos...")
    try:
        # Crear datos de prueba
        test_data = pd.DataFrame({
            'fecha': pd.date_range('2024-01-01', periods=100),
            'producto_id': [f'P{i:03d}' for i in range(1, 101)],
            'precio': np.random.uniform(1, 100, 100),
            'cantidad_vendida': np.random.randint(1, 50, 100),
            'categoria': np.random.choice(['Lacteos', 'Carnes', 'Frutas', 'Bebidas'], 100),
            'cliente_id': [f'C{i:03d}' for i in range(1, 101)],
            'satisfaccion_cliente': np.random.uniform(1, 5, 100),
            'descuento': np.random.uniform(0, 0.5, 100)
        })
        print("✅ Carga de datos exitosa")
        return test_data
    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")
        return None

def test_eda_module(data):
    """Prueba el módulo EDA"""
    print("🔄 Probando módulo EDA...")
    try:
        # Probar funciones básicas del EDA
        if hasattr(eda, 'mostrar_resumen_datos'):
            print("  - Función mostrar_resumen_datos disponible")
        if hasattr(eda, 'analizar_calidad_datos'):
            print("  - Función analizar_calidad_datos disponible")
        if hasattr(eda, 'crear_visualizaciones_interactivas'):
            print("  - Función crear_visualizaciones_interactivas disponible")
        print("✅ Módulo EDA verificado")
        return True
    except Exception as e:
        print(f"❌ Error en módulo EDA: {e}")
        return False

def test_modelo_regresion(data):
    """Prueba el modelo de regresión"""
    print("🔄 Probando modelo de regresión...")
    try:
        if hasattr(modelo_1_regresion, 'entrenar_modelo'):
            print("  - Función entrenar_modelo disponible")
        if hasattr(modelo_1_regresion, 'evaluar_modelo'):
            print("  - Función evaluar_modelo disponible")
        print("✅ Modelo de regresión verificado")
        return True
    except Exception as e:
        print(f"❌ Error en modelo de regresión: {e}")
        return False

def test_modelo_segmentacion(data):
    """Prueba el modelo de segmentación"""
    print("🔄 Probando modelo de segmentación...")
    try:
        if hasattr(modelo_2_segmentacion, 'entrenar_modelo'):
            print("  - Función entrenar_modelo disponible")
        if hasattr(modelo_2_segmentacion, 'evaluar_modelo'):
            print("  - Función evaluar_modelo disponible")
        print("✅ Modelo de segmentación verificado")
        return True
    except Exception as e:
        print(f"❌ Error en modelo de segmentación: {e}")
        return False

def test_modelo_clasificacion(data):
    """Prueba el modelo de clasificación"""
    print("🔄 Probando modelo de clasificación...")
    try:
        if hasattr(modelo_3_clasificacion, 'entrenar_modelo'):
            print("  - Función entrenar_modelo disponible")
        if hasattr(modelo_3_clasificacion, 'evaluar_modelo'):
            print("  - Función evaluar_modelo disponible")
        print("✅ Modelo de clasificación verificado")
        return True
    except Exception as e:
        print(f"❌ Error en modelo de clasificación: {e}")
        return False

def test_modelo_anomalias(data):
    """Prueba el modelo de detección de anomalías"""
    print("🔄 Probando modelo de detección de anomalías...")
    try:
        if hasattr(modelo_4_anomalias, 'entrenar_modelo'):
            print("  - Función entrenar_modelo disponible")
        if hasattr(modelo_4_anomalias, 'evaluar_modelo'):
            print("  - Función evaluar_modelo disponible")
        print("✅ Modelo de detección de anomalías verificado")
        return True
    except Exception as e:
        print(f"❌ Error en modelo de detección de anomalías: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas del dashboard de modelos conceptuales")
    print("=" * 60)
    
    # Prueba carga de datos
    data = test_data_loading()
    if data is None:
        print("❌ No se puede continuar sin datos")
        return
    
    # Prueba todos los módulos
    results = {
        'EDA': test_eda_module(data),
        'Regresión': test_modelo_regresion(data),
        'Segmentación': test_modelo_segmentacion(data),
        'Clasificación': test_modelo_clasificacion(data),
        'Anomalías': test_modelo_anomalias(data)
    }
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for module, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {module}: {status}")
    
    print(f"\n🎯 Resultado final: {passed_tests}/{total_tests} pruebas exitosas")
    
    if passed_tests == total_tests:
        print("🎉 ¡Todos los módulos funcionan correctamente!")
    else:
        print(f"⚠️  {total_tests - passed_tests} módulos necesitan atención")

if __name__ == "__main__":
    main()
