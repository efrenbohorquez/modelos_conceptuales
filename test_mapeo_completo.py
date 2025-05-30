#!/usr/bin/env python3
"""
Test completo del mapeo de columnas y compatibilidad con modelos ML
"""
import pandas as pd
import sys
import os

# Agregar el directorio src al path
sys.path.append('src')

try:
    from mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles
    from data_loader import cargar_datos
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    sys.exit(1)

def test_mapeo_completo():
    """Test completo del proceso de mapeo"""
    print("\n" + "="*60)
    print("🧪 TEST COMPLETO DE MAPEO DE COLUMNAS")
    print("="*60)
    
    # 1. Cargar dataset original
    try:
        archivo = "data/test_supermarket_data.csv"
        df = cargar_datos(archivo)
        print(f"✅ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
        print(f"📋 Columnas originales: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error cargando dataset: {e}")
        return False
    
    # 2. Verificar necesidad de mapeo
    print(f"\n🔍 VERIFICACIÓN DE COMPATIBILIDAD")
    columnas_requeridas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment', 'Rating']
    info_original = verificar_columnas_disponibles(df, columnas_requeridas)
    
    print(f"📊 Porcentaje de columnas disponibles: {info_original['porcentaje_disponible']:.1f}%")
    print(f"✅ Columnas encontradas: {info_original['columnas_encontradas']}")
    print(f"❌ Columnas faltantes: {info_original['columnas_faltantes']}")
    
    # 3. Aplicar mapeo si es necesario
    if info_original['porcentaje_disponible'] < 50:
        print(f"\n🔄 APLICANDO MAPEO DE COLUMNAS")
        try:
            df_mapped = mapear_columnas_dataset(df)
            print(f"✅ Mapeo completado: {df_mapped.shape[0]} filas, {df_mapped.shape[1]} columnas")
            print(f"📋 Nuevas columnas: {list(df_mapped.columns)}")
            
            # Verificar resultado del mapeo
            info_mapped = verificar_columnas_disponibles(df_mapped, columnas_requeridas)
            print(f"📊 Porcentaje después del mapeo: {info_mapped['porcentaje_disponible']:.1f}%")
            print(f"✅ Columnas encontradas: {info_mapped['columnas_encontradas']}")
            print(f"❌ Columnas faltantes: {info_mapped['columnas_faltantes']}")
            
            df_final = df_mapped
        except Exception as e:
            print(f"❌ Error en el mapeo: {e}")
            return False
    else:
        print("✅ No se necesita mapeo, columnas ya compatibles")
        df_final = df
    
    # 4. Verificar compatibilidad con cada modelo
    print(f"\n🎯 VERIFICACIÓN DE COMPATIBILIDAD POR MODELO")
    
    # Modelo 1: Regresión
    rating_ok = 'Rating' in df_final.columns
    numeric_vars = len([col for col in df_final.columns if df_final[col].dtype in ['int64', 'float64']])
    print(f"🔸 Modelo Regresión: {'✅' if rating_ok and numeric_vars >= 3 else '❌'}")
    print(f"   - Rating disponible: {'✅' if rating_ok else '❌'}")
    print(f"   - Variables numéricas: {numeric_vars}")
    
    # Modelo 2: Segmentación  
    seg_ok = numeric_vars >= 2
    print(f"🔸 Modelo Segmentación: {'✅' if seg_ok else '❌'}")
    print(f"   - Variables numéricas suficientes: {'✅' if seg_ok else '❌'}")
    
    # Modelo 3: Clasificación
    product_line_ok = 'Product line' in df_final.columns
    class_ok = product_line_ok and numeric_vars >= 2
    print(f"🔸 Modelo Clasificación: {'✅' if class_ok else '❌'}")
    print(f"   - Product line disponible: {'✅' if product_line_ok else '❌'}")
    
    # Modelo 4: Anomalías
    anom_ok = len(df_final.columns) >= 3
    print(f"🔸 Modelo Anomalías: {'✅' if anom_ok else '❌'}")
    print(f"   - Variables suficientes: {'✅' if anom_ok else '❌'}")
    
    # 5. Resumen final
    print(f"\n📋 RESUMEN FINAL")
    print(f"✅ Dataset final: {df_final.shape[0]} filas × {df_final.shape[1]} columnas")
    print(f"✅ Compatibilidad global: {info_mapped['porcentaje_disponible'] if 'info_mapped' in locals() else info_original['porcentaje_disponible']:.1f}%")
    
    modelos_ok = sum([rating_ok and numeric_vars >= 3, seg_ok, class_ok, anom_ok])
    print(f"✅ Modelos compatibles: {modelos_ok}/4")
    
    if modelos_ok >= 3:
        print("🎉 ¡MAPEO EXITOSO! El dashboard debería funcionar correctamente.")
        return True
    else:
        print("⚠️ Algunos modelos pueden tener problemas de compatibilidad.")
        return False

if __name__ == "__main__":
    success = test_mapeo_completo()
    if success:
        print(f"\n🚀 El dashboard está listo para ejecutarse con:")
        print(f"   python -m streamlit run app.py")
    else:
        print(f"\n❌ Hay problemas que deben resolverse antes de ejecutar el dashboard.")
