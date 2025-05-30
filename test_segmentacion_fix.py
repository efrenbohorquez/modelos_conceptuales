#!/usr/bin/env python3
"""
Test específico para verificar que el modelo de segmentación funciona correctamente
después de las correcciones realizadas.
"""

import sys
import os
import pandas as pd
import numpy as np

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import cargar_datos
from modelo_2_segmentacion import preparar_datos_segmentacion, segmentar_clientes, caracterizar_segmentos

def test_segmentacion_completa():
    """Test completo del modelo de segmentación"""
    print("🧪 Iniciando test del modelo de segmentación...")
    
    try:
        # 1. Cargar datos
        print("\n1️⃣ Cargando datos...")
        df = cargar_datos()
        print(f"   ✅ Datos cargados: {df.shape}")
        print(f"   📊 Columnas disponibles: {list(df.columns)}")
        
        # 2. Preparar datos para segmentación
        print("\n2️⃣ Preparando datos para segmentación...")
        X_processed, preprocessor = preparar_datos_segmentacion(df)
        print(f"   ✅ Datos procesados: {X_processed.shape}")
        print(f"   🔄 Preprocesador creado exitosamente")
        
        # 3. Realizar segmentación
        print("\n3️⃣ Realizando segmentación de clientes...")
        df_segmentado, kmeans, pca, preprocessor = segmentar_clientes(df, n_clusters=3)
        print(f"   ✅ Segmentación completada")
        print(f"   📊 Segmentos únicos: {df_segmentado['Segmento'].unique()}")
        print(f"   🔢 Distribución de segmentos:")
        print(df_segmentado['Segmento'].value_counts().to_string())
        
        # 4. Caracterizar segmentos
        print("\n4️⃣ Caracterizando segmentos...")
        caracterizacion = caracterizar_segmentos(df_segmentado)
        print(f"   ✅ Caracterización completada")
        print(f"   📋 Características por segmento:")
        print(caracterizacion)
        
        # 5. Verificaciones adicionales
        print("\n5️⃣ Verificaciones adicionales...")
        
        # Verificar que todos los registros tienen segmento
        assert 'Segmento' in df_segmentado.columns, "La columna 'Segmento' no existe"
        assert df_segmentado['Segmento'].isna().sum() == 0, "Hay valores nulos en 'Segmento'"
        
        # Verificar que hay exactamente 3 segmentos
        n_segmentos = df_segmentado['Segmento'].nunique()
        assert n_segmentos == 3, f"Esperado 3 segmentos, encontrado {n_segmentos}"
        
        # Verificar que la caracterización tiene datos
        assert not caracterizacion.empty, "La caracterización está vacía"
        assert len(caracterizacion) == 3, f"Esperado 3 filas en caracterización, encontrado {len(caracterizacion)}"
        
        print("   ✅ Todas las verificaciones pasaron")
        
        print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print("✅ El modelo de segmentación funciona correctamente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en el test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test de casos límite"""
    print("\n🔍 Probando casos límite...")
    
    try:
        # Cargar datos original
        df = cargar_datos()
        
        # Test con pocos datos
        df_small = df.head(10)
        print(f"   🧪 Probando con datos pequeños ({len(df_small)} filas)...")
        df_seg_small, _, _, _ = segmentar_clientes(df_small, n_clusters=2)
        caracterizacion_small = caracterizar_segmentos(df_seg_small)
        print(f"   ✅ Funciona con datos pequeños")
        
        print("   ✅ Casos límite funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en casos límite: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔬 TEST DEL MODELO DE SEGMENTACIÓN CORREGIDO")
    print("=" * 60)
    
    # Ejecutar tests
    test1_ok = test_segmentacion_completa()
    test2_ok = test_edge_cases()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE RESULTADOS:")
    print(f"   • Test principal: {'✅ PASÓ' if test1_ok else '❌ FALLÓ'}")
    print(f"   • Test casos límite: {'✅ PASÓ' if test2_ok else '❌ FALLÓ'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 TODOS LOS TESTS PASARON - MODELO CORREGIDO EXITOSAMENTE")
        sys.exit(0)
    else:
        print("\n❌ ALGUNOS TESTS FALLARON - REVISAR CORRECCIONES")
        sys.exit(1)
