#!/usr/bin/env python3
"""
Test de validación del sistema optimizado
Verifica que todos los componentes funcionen correctamente con datos de supermercado
"""

import sys
import traceback
import pandas as pd
from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias
from src.mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles

def test_carga_datos():
    """Test de carga de datos"""
    print("🔄 Probando carga de datos...")
    try:
        df = data_loader.cargar_datos()
        if df is not None and len(df) > 0:
            print(f"✅ Datos cargados exitosamente: {df.shape}")
            print(f"   Columnas: {list(df.columns)}")
            return df
        else:
            print("❌ Error: No se pudieron cargar los datos")
            return None
    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")
        return None

def test_mapeo_columnas(df):
    """Test de mapeo de columnas"""
    print("\n🔄 Probando mapeo de columnas...")
    try:
        columnas_requeridas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
        info_columnas = verificar_columnas_disponibles(df, columnas_requeridas)
        print(f"✅ Compatibilidad: {info_columnas['porcentaje_disponible']:.1f}%")
        print(f"   Encontradas: {info_columnas['columnas_encontradas']}")
        if info_columnas['columnas_faltantes']:
            print(f"   Faltantes: {info_columnas['columnas_faltantes']}")
        return True
    except Exception as e:
        print(f"❌ Error en mapeo: {e}")
        return False

def test_modelo_regresion(df):
    """Test del modelo de regresión"""
    print("\n🔄 Probando modelo de regresión...")
    try:
        if 'Rating' not in df.columns:
            print("⚠️ Columna 'Rating' no disponible, saltando test")
            return False
        
        # Usar solo variables numéricas para test rápido
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        test_cols = [col for col in numeric_cols if col != 'Rating'][:5]  # Máximo 5 variables
        test_df = df[test_cols + ['Rating']].dropna().head(100)  # Solo 100 registros para test
        
        modelo, preproc, resultados = modelo_1_regresion.entrenar_regresion(test_df)
        print(f"✅ Regresión completada - R²: {resultados['R2']:.3f}")
        return True
    except Exception as e:
        print(f"❌ Error en regresión: {e}")
        traceback.print_exc()
        return False

def test_modelo_segmentacion(df):
    """Test del modelo de segmentación"""
    print("\n🔄 Probando modelo de segmentación...")
    try:
        # Usar solo variables numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]  # Máximo 4 variables
        test_df = df[numeric_cols].dropna().head(100)  # Solo 100 registros para test
        
        if len(numeric_cols) < 2:
            print("⚠️ Menos de 2 variables numéricas, saltando test")
            return False
        
        df_seg, kmeans, pca, preproc = modelo_2_segmentacion.segmentar_clientes(test_df, n_clusters=3)
        print(f"✅ Segmentación completada - {len(df_seg)} clientes segmentados")
        return True
    except Exception as e:
        print(f"❌ Error en segmentación: {e}")
        traceback.print_exc()
        return False

def test_modelo_clasificacion(df):
    """Test del modelo de clasificación"""
    print("\n🔄 Probando modelo de clasificación...")
    try:
        if 'Product line' not in df.columns:
            print("⚠️ Columna 'Product line' no disponible, saltando test")
            return False
        
        # Usar solo algunas variables para test rápido
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:3]
        categorical_cols = ['Gender', 'Customer type'] if 'Gender' in df.columns and 'Customer type' in df.columns else []
        test_cols = numeric_cols + categorical_cols
        test_df = df[test_cols + ['Product line']].dropna().head(100)  # Solo 100 registros
        
        modelo, preproc, resultados = modelo_3_clasificacion.entrenar_clasificacion(test_df)
        print(f"✅ Clasificación completada - Accuracy: {resultados['accuracy']:.3f}")
        return True
    except Exception as e:
        print(f"❌ Error en clasificación: {e}")
        traceback.print_exc()
        return False

def test_modelo_anomalias(df):
    """Test del modelo de anomalías"""
    print("\n🔄 Probando modelo de anomalías...")
    try:
        # Usar solo variables numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:3]  # Máximo 3 variables
        test_df = df[numeric_cols].dropna().head(100)  # Solo 100 registros para test
        
        if len(numeric_cols) < 1:
            print("⚠️ Sin variables numéricas, saltando test")
            return False
        
        df_anom, modelo, preproc = modelo_4_anomalias.detectar_anomalias(test_df, numeric_cols, contamination=0.1)
        anomalias = (df_anom['Anomalía'] == 'Sí').sum()
        print(f"✅ Detección completada - {anomalias} anomalías detectadas")
        return True
    except Exception as e:
        print(f"❌ Error en anomalías: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal del test"""
    print("🚀 INICIANDO VALIDACIÓN DEL SISTEMA OPTIMIZADO")
    print("=" * 50)
    
    resultados = []
    
    # Test 1: Carga de datos
    df = test_carga_datos()
    resultados.append(("Carga de datos", df is not None))
    
    if df is None:
        print("\n❌ CRÍTICO: No se pueden cargar datos. Abortando tests.")
        return
    
    # Test 2: Mapeo de columnas
    mapeo_ok = test_mapeo_columnas(df)
    resultados.append(("Mapeo de columnas", mapeo_ok))
    
    # Test 3-6: Modelos
    reg_ok = test_modelo_regresion(df)
    resultados.append(("Modelo regresión", reg_ok))
    
    seg_ok = test_modelo_segmentacion(df)
    resultados.append(("Modelo segmentación", seg_ok))
    
    clas_ok = test_modelo_clasificacion(df)
    resultados.append(("Modelo clasificación", clas_ok))
    
    anom_ok = test_modelo_anomalias(df)
    resultados.append(("Modelo anomalías", anom_ok))
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 50)
    
    exitosos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        status = "✅" if resultado else "❌"
        print(f"{status} {nombre}")
    
    print(f"\n🎯 RESULTADO: {exitosos}/{total} tests exitosos ({exitosos/total*100:.1f}%)")
    
    if exitosos == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
    elif exitosos >= total * 0.8:
        print("✅ Sistema mayormente funcional")
    else:
        print("⚠️ Sistema requiere atención")

if __name__ == "__main__":
    main()
