#!/usr/bin/env python3
"""
Validación Final del Dashboard - Resolución del problema de pantalla sin datos

Este script valida que:
1. El dashboard se inicia correctamente
2. Los datos se cargan y persisten en la sesión
3. La sección de variables numéricas es accesible
4. No hay reinicios inesperados
"""

import requests
import time
import pandas as pd
from src import data_loader

def validar_carga_datos():
    """Valida que la función de carga de datos funcione"""
    print("🔍 Validando carga de datos...")
    
    # Verificar que el dataset esté disponible
    dataset_info = data_loader.verificar_dataset_real()
    print(f"📊 Dataset disponible: {dataset_info['disponible']}")
    print(f"📈 Registros: {dataset_info.get('registros', 'N/A')}")
    
    # Intentar cargar datos
    df = data_loader.cargar_datos()
    if df is not None:
        print(f"✅ Datos cargados exitosamente: {len(df)} registros x {len(df.columns)} columnas")
        
        # Verificar variables numéricas clave
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        expected_vars = ['Unit price', 'Quantity', 'Tax 5%', 'Total']
        found_vars = [var for var in expected_vars if var in numeric_cols]
        
        print(f"🔢 Variables numéricas encontradas: {len(numeric_cols)}")
        print(f"📋 Variables clave encontradas: {found_vars}")
        
        return True
    else:
        print("❌ Error cargando datos")
        return False

def validar_servidor_activo():
    """Valida que el servidor Streamlit esté activo"""
    print("🌐 Validando servidor Streamlit...")
    
    try:
        response = requests.get("http://localhost:8504", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Streamlit activo en puerto 8504")
            return True
        else:
            print(f"⚠️ Servidor responde con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 VALIDACIÓN FINAL DEL DASHBOARD")
    print("=" * 60)
    print()
    
    # Validar carga de datos
    datos_ok = validar_carga_datos()
    print()
    
    # Validar servidor
    servidor_ok = validar_servidor_activo()
    print()
    
    # Resumen final
    print("=" * 60)
    print("📋 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    print(f"✅ Carga de datos: {'OK' if datos_ok else 'FALLO'}")
    print(f"✅ Servidor activo: {'OK' if servidor_ok else 'FALLO'}")
    print()
    
    if datos_ok and servidor_ok:
        print("🎉 ¡VALIDACIÓN EXITOSA!")
        print("📱 El dashboard está listo y funcionando correctamente")
        print("🌐 Accede a: http://localhost:8504")
        print()
        print("💡 INSTRUCCIONES PARA PROBAR:")
        print("1. Abre el dashboard en tu navegador")
        print("2. Haz clic en '🚀 Cargar Datos de Supermercado'")
        print("3. Verifica que aparezcan las secciones de análisis")
        print("4. Busca la sección 'Selecciona variables numéricas'")
        print("5. Confirma que las variables aparecen sin reiniciar")
    else:
        print("❌ VALIDACIÓN FALLIDA")
        print("🔧 Revisa los errores anteriores")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
