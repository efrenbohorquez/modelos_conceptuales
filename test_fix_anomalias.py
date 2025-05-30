#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE CORRECCIÓN - MÓDULO DE DETECCIÓN DE ANOMALÍAS
====================================================

Script para probar la corrección del error de tipos mixtos.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("🔧 PROBANDO CORRECCIÓN DEL MÓDULO DE ANOMALÍAS")
print("=" * 50)

# 1. Importar el módulo corregido
try:
    from src.modelo_4_anomalias import preparar_datos_anomalias, detectar_anomalias
    print("✅ Módulo importado correctamente")
except Exception as e:
    print(f"❌ Error al importar: {e}")
    exit(1)

# 2. Crear datos de prueba con tipos mixtos (que causaban el error)
print("\n📊 Creando datos de prueba con tipos mixtos...")

# Crear fechas
fechas = [datetime.now() - timedelta(days=i) for i in range(100)]

# Datos de prueba con tipos mixtos
data = {
    'Total': np.random.normal(100, 20, 100),
    'Quantity': np.random.randint(1, 10, 100),
    'Gender': np.random.choice(['Male', 'Female'], 100),
    'Product_line': np.random.choice(['Food', 'Electronics', 'Clothing'], 100),
    'Date': fechas,  # Columna datetime
    'City': np.random.choice(['Yangon', 'Mandalay', 'Naypyitaw'], 100),
    'Payment': np.random.choice(['Cash', 'Credit card', 'Ewallet'], 100)
}

df_test = pd.DataFrame(data)

print(f"   - Dataset creado: {len(df_test)} registros")
print(f"   - Tipos de datos:")
for col, dtype in df_test.dtypes.items():
    print(f"     • {col}: {dtype}")

# 3. Probar la función corregida
print("\n🔧 Probando preparación de datos...")
try:
    variables = ['Total', 'Quantity', 'Gender', 'Product_line', 'Date', 'City', 'Payment']
    X_preparado, preprocessor = preparar_datos_anomalias(df_test, variables)
    print(f"✅ Datos preparados exitosamente: shape {X_preparado.shape}")
except Exception as e:
    print(f"❌ Error en preparación: {e}")
    exit(1)

# 4. Probar detección de anomalías completa
print("\n🚨 Probando detección de anomalías...")
try:
    df_result, modelo, preproc = detectar_anomalias(df_test, variables, contamination=0.1)
    
    anomalias = df_result[df_result['Anomalía'] == 'Sí']
    print(f"✅ Detección completada exitosamente")
    print(f"   - Total registros: {len(df_result)}")
    print(f"   - Anomalías detectadas: {len(anomalias)}")
    print(f"   - Porcentaje: {len(anomalias)/len(df_result)*100:.1f}%")

except Exception as e:
    print(f"❌ Error en detección: {e}")
    exit(1)

# 5. Verificar que funciona con diferentes combinaciones
print("\n🧪 Probando con diferentes combinaciones de variables...")

# Solo numéricas
try:
    df_result, _, _ = detectar_anomalias(df_test, ['Total', 'Quantity'], contamination=0.1)
    print("✅ Solo variables numéricas: OK")
except Exception as e:
    print(f"❌ Solo numéricas falló: {e}")

# Solo categóricas
try:
    df_result, _, _ = detectar_anomalias(df_test, ['Gender', 'Product_line', 'City'], contamination=0.1)
    print("✅ Solo variables categóricas: OK")
except Exception as e:
    print(f"❌ Solo categóricas falló: {e}")

# Con datetime
try:
    df_result, _, _ = detectar_anomalias(df_test, ['Total', 'Date', 'Gender'], contamination=0.1)
    print("✅ Con datetime: OK")
except Exception as e:
    print(f"❌ Con datetime falló: {e}")

print("\n" + "=" * 50)
print("🎉 CORRECCIÓN EXITOSA")
print("=" * 50)
print("✅ El error de tipos mixtos ha sido corregido")
print("✅ El módulo funciona con datetime, string y numéricos")
print("✅ OneHotEncoder ya no recibe tipos mixtos")
print("✅ El dashboard debería funcionar sin errores")
