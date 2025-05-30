#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación final y ejecución del dashboard
Verifica que todos los componentes estén funcionando y luego ejecuta el dashboard
"""

import sys
import os
import subprocess
from pathlib import Path

def verificar_dependencias():
    """Verifica que todas las dependencias estén disponibles"""
    print("🔍 Verificando dependencias...")
    
    try:
        import streamlit as st
        print("✅ Streamlit disponible")
    except ImportError:
        print("❌ Streamlit no está instalado")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        import seaborn as sns
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.cluster import KMeans
        from sklearn.ensemble import IsolationForest
        print("✅ Todas las librerías ML disponibles")
    except ImportError as e:
        print(f"❌ Falta librería ML: {e}")
        return False
    
    return True

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("📁 Verificando archivos...")
    
    archivos_requeridos = [
        'app.py',
        'src/data_loader.py',
        'src/mapeo_columnas.py',
        'src/modelo_1_regresion.py',
        'src/modelo_2_segmentacion.py',
        'src/modelo_3_clasificacion.py',
        'src/modelo_4_anomalias.py',
        'data/test_supermarket_data.csv'
    ]
    
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            print(f"❌ Archivo faltante: {archivo}")
            return False
        else:
            print(f"✅ {archivo}")
    
    return True

def verificar_dataset_real():
    """Verifica el dataset real"""
    print("📊 Verificando dataset real...")
    
    try:
        sys.path.append('src')
        from data_loader import verificar_dataset_real
        
        info_real = verificar_dataset_real()
        print(f"📊 Dataset real disponible: {info_real['disponible']}")
        if info_real['disponible']:
            print(f"   📍 Ubicación: {info_real['ruta']}")
            print(f"   📏 Filas: {info_real['filas']}, Columnas: {info_real['columnas']}")
        
        return True
    except Exception as e:
        print(f"⚠️ Error verificando dataset real: {e}")
        return True  # No es crítico

def verificar_sintaxis_app():
    """Verifica que app.py no tenga errores de sintaxis"""
    print("🔍 Verificando sintaxis de app.py...")
    
    try:
        import py_compile
        py_compile.compile('app.py', doraise=True)
        print("✅ app.py sin errores de sintaxis")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Error de sintaxis en app.py: {e}")
        return False

def ejecutar_dashboard():
    """Ejecuta el dashboard"""
    print("\n🚀 Iniciando dashboard...")
    print("📋 El dashboard se abrirá en: http://localhost:8501")
    print("💡 Para detener: Ctrl+C")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando dashboard: {e}")
    except FileNotFoundError:
        print("❌ Streamlit no encontrado. Instala con: pip install streamlit")

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN FINAL DEL DASHBOARD")
    print("=" * 50)
    
    # Cambiar al directorio correcto
    os.chdir(Path(__file__).parent)
    
    # Verificaciones
    if not verificar_dependencias():
        print("\n❌ Fallo en verificación de dependencias")
        return False
    
    if not verificar_archivos():
        print("\n❌ Fallo en verificación de archivos")
        return False
    
    if not verificar_sintaxis_app():
        print("\n❌ Fallo en verificación de sintaxis")
        return False
    
    verificar_dataset_real()
    
    print("\n✅ TODAS LAS VERIFICACIONES PASARON")
    print("🎉 El dashboard está listo para ejecutarse")
    
    # Preguntar si ejecutar
    respuesta = input("\n¿Deseas ejecutar el dashboard ahora? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'y', 'yes']:
        ejecutar_dashboard()
    else:
        print("👍 Para ejecutar manualmente usa: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main()
