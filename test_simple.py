#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

print("🚀 Iniciando pruebas del dashboard de modelos conceptuales")
print("=" * 60)

# Prueba 1: Importar módulos
try:
    from src import eda
    print("✅ Módulo EDA importado correctamente")
except Exception as e:
    print(f"❌ Error importando EDA: {e}")

try:
    from src import modelo_1_regresion
    print("✅ Módulo de regresión importado correctamente")
except Exception as e:
    print(f"❌ Error importando modelo de regresión: {e}")

try:
    from src import modelo_2_segmentacion
    print("✅ Módulo de segmentación importado correctamente")
except Exception as e:
    print(f"❌ Error importando modelo de segmentación: {e}")

try:
    from src import modelo_3_clasificacion
    print("✅ Módulo de clasificación importado correctamente")
except Exception as e:
    print(f"❌ Error importando modelo de clasificación: {e}")

try:
    from src import modelo_4_anomalias
    print("✅ Módulo de detección de anomalías importado correctamente")
except Exception as e:
    print(f"❌ Error importando modelo de detección de anomalías: {e}")

# Prueba 2: Importar dependencias principales
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly
    print("✅ Todas las dependencias principales disponibles")
except Exception as e:
    print(f"❌ Error con dependencias: {e}")

# Prueba 3: Verificar archivos de datos
data_files = ['data/test_supermarket_data.csv', 'data/clientes_info.csv']
for file in data_files:
    if os.path.exists(file):
        print(f"✅ Archivo de datos encontrado: {file}")
    else:
        print(f"⚠️  Archivo de datos no encontrado: {file}")

print("\n" + "=" * 60)
print("🎉 Pruebas básicas completadas")
