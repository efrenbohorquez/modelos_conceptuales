#!/usr/bin/env python3
"""
Prueba simple y directa del módulo de detección de anomalías
"""
print("🔍 Iniciando prueba del módulo de detección de anomalías...")

# Importaciones básicas
import pandas as pd
import numpy as np
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

try:
    # Importar el módulo
    print("📦 Importando módulo...")
    from src.modelo_4_anomalias import detectar_anomalias, preparar_datos_anomalias
    print("✅ Módulo importado correctamente")
    
    # Crear datos de prueba simples
    print("📊 Creando datos de prueba...")
    np.random.seed(42)
    data = {
        'precio': np.random.normal(10, 2, 20),
        'cantidad': np.random.poisson(5, 20),
        'descuento': np.random.uniform(0, 0.3, 20)
    }
    df_test = pd.DataFrame(data)
    print(f"✅ Datos creados: {df_test.shape}")
    
    # Probar la función
    print("🚀 Ejecutando detección de anomalías...")
    variables = ['precio', 'cantidad', 'descuento']
    df_resultado, modelo, preprocessor = detectar_anomalias(df_test, variables, contamination=0.1)
    
    # Resultados
    anomalias = df_resultado[df_resultado['Anomalía'] == 'Sí']
    print(f"✅ Detección completada!")
    print(f"📊 Total registros: {len(df_resultado)}")
    print(f"🚨 Anomalías detectadas: {len(anomalias)}")
    print(f"📈 Porcentaje: {len(anomalias)/len(df_resultado)*100:.1f}%")
    
    if len(anomalias) > 0:
        print("🎯 Primeras anomalías detectadas:")
        print(anomalias[['precio', 'cantidad', 'descuento', 'Anomalía']].head())
    
    print("\n🎉 ¡MÓDULO FUNCIONA PERFECTAMENTE!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
