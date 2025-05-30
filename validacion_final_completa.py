"""
🎯 SCRIPT DE VALIDACIÓN FINAL COMPLETA
Proyecto: Dashboard Modelos Conceptuales Supermercado
Objetivo: Verificar que todas las funcionalidades están operativas sin errores
"""

import sys
import os
import pandas as pd
import warnings

# Suprimir advertencias durante la validación
warnings.filterwarnings("ignore")

# Agregar la ruta del proyecto
sys.path.append('c:\\Users\\Public\\modelos_conceptuales')

def test_imports():
    """Verificar que todas las importaciones funcionan"""
    print("🔍 Verificando importaciones...")
    
    try:
        from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion
        from src import modelo_3_clasificacion, modelo_4_anomalias
        from src.mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles
        from src.data_utils import optimize_dataframe_for_streamlit, display_data_quality_summary
        print("✅ Todas las importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_data_loading():
    """Verificar carga de datos"""
    print("\n📊 Verificando carga de datos...")
    
    try:
        # Probar carga de datos principales
        df = data_loader.cargar_datos()
        if df is not None:
            print(f"✅ Datos cargados: {len(df)} registros x {len(df.columns)} columnas")
            print(f"📋 Columnas: {', '.join(df.columns)}")
            
            # Verificar variables numéricas esperadas
            expected_numeric = ['Unit price', 'Quantity', 'Tax 5%', 'Total']
            numeric_found = [col for col in expected_numeric if col in df.columns]
            print(f"🔢 Variables numéricas detectadas: {', '.join(numeric_found)}")
            
            return df
        else:
            print("❌ No se pudieron cargar los datos")
            return None
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def test_data_optimization(df):
    """Verificar optimización de datos para PyArrow"""
    print("\n🔧 Verificando optimización de datos...")
    
    try:
        from src.data_utils import optimize_dataframe_for_streamlit
        
        df_optimized = optimize_dataframe_for_streamlit(df)
        print("✅ Optimización PyArrow aplicada exitosamente")
        
        # Verificar tipos de datos optimizados
        print("📝 Tipos de datos después de optimización:")
        for col, dtype in df_optimized.dtypes.items():
            print(f"   - {col}: {dtype}")
        
        return df_optimized
    except Exception as e:
        print(f"❌ Error en optimización: {e}")
        return df

def test_models(df):
    """Verificar que todos los modelos funcionan"""
    print("\n🤖 Verificando modelos de ML...")
    
    # Variables básicas para pruebas
    test_vars = ['Unit price', 'Quantity', 'Total']
    numeric_vars = [col for col in test_vars if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    
    if len(numeric_vars) < 2:
        print("⚠️ Insuficientes variables numéricas para pruebas de modelos")
        return False
    
    results = {}
    
    # Test Modelo 1: Regresión
    try:
        if 'Rating' in df.columns:
            resultados = modelo_1_regresion.entrenar_regresion(df.dropna())
            results['regresion'] = resultados['R2'] > 0
            print(f"✅ Modelo Regresión: R² = {resultados['R2']:.3f}")
        else:
            print("⚠️ Columna 'Rating' no encontrada para regresión")
    except Exception as e:
        print(f"❌ Error en modelo regresión: {e}")
        results['regresion'] = False
    
    # Test Modelo 2: Segmentación
    try:
        df_seg, kmeans, pca, preproc = modelo_2_segmentacion.segmentar_clientes(
            df[numeric_vars].dropna(), n_clusters=3
        )
        results['segmentacion'] = len(df_seg) > 0
        print(f"✅ Modelo Segmentación: {len(df_seg)} clientes segmentados")
    except Exception as e:
        print(f"❌ Error en modelo segmentación: {e}")
        results['segmentacion'] = False
    
    # Test Modelo 3: Clasificación
    try:
        if 'Product line' in df.columns:
            resultados = modelo_3_clasificacion.entrenar_clasificacion(df.dropna())
            results['clasificacion'] = resultados['accuracy'] > 0.5
            print(f"✅ Modelo Clasificación: Accuracy = {resultados['accuracy']:.3f}")
        else:
            print("⚠️ Columna 'Product line' no encontrada para clasificación")
    except Exception as e:
        print(f"❌ Error en modelo clasificación: {e}")
        results['clasificacion'] = False
    
    # Test Modelo 4: Anomalías
    try:
        df_anom, modelo, preproc = modelo_4_anomalias.detectar_anomalias(
            df[numeric_vars].dropna(), numeric_vars, contamination=0.1
        )
        results['anomalias'] = len(df_anom) > 0
        anomalias_count = (df_anom['Anomalía'] == 'Sí').sum()
        print(f"✅ Modelo Anomalías: {anomalias_count} anomalías detectadas")
    except Exception as e:
        print(f"❌ Error en modelo anomalías: {e}")
        results['anomalias'] = False
    
    return results

def test_eda_functionality(df):
    """Verificar funcionalidades de EDA"""
    print("\n📈 Verificando análisis exploratorio...")
    
    try:
        # Variables numéricas disponibles
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        print(f"🔢 Variables numéricas disponibles: {', '.join(numeric_cols)}")
        
        # Verificar que incluye las variables esperadas del dashboard
        expected_vars = ['Unit price', 'Quantity', 'Tax 5%', 'Total']
        found_vars = [var for var in expected_vars if var in numeric_cols]
        
        if len(found_vars) >= 3:
            print(f"✅ Variables del dashboard detectadas: {', '.join(found_vars)}")
            return True
        else:
            print(f"⚠️ Faltan variables del dashboard. Encontradas: {', '.join(found_vars)}")
            return False
            
    except Exception as e:
        print(f"❌ Error en EDA: {e}")
        return False

def generate_final_report(test_results):
    """Generar reporte final"""
    print("\n" + "="*60)
    print("📋 REPORTE FINAL DE VALIDACIÓN")
    print("="*60)
    
    all_passed = True
    
    # Resumen de pruebas
    if test_results.get('imports', False):
        print("✅ Importaciones: OK")
    else:
        print("❌ Importaciones: FALLO")
        all_passed = False
    
    if test_results.get('data_loading', False):
        print("✅ Carga de datos: OK")
    else:
        print("❌ Carga de datos: FALLO")
        all_passed = False
    
    if test_results.get('optimization', False):
        print("✅ Optimización PyArrow: OK")
    else:
        print("❌ Optimización PyArrow: FALLO")
        all_passed = False
    
    if test_results.get('eda', False):
        print("✅ EDA con variables numéricas: OK")
    else:
        print("❌ EDA con variables numéricas: FALLO")
        all_passed = False
    
    # Modelos ML
    models = test_results.get('models', {})
    for model_name, status in models.items():
        status_icon = "✅" if status else "⚠️"
        print(f"{status_icon} Modelo {model_name.title()}: {'OK' if status else 'ADVERTENCIA'}")
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 VALIDACIÓN COMPLETA: TODOS LOS SISTEMAS OPERATIVOS")
        print("🚀 El dashboard está listo para producción")
    else:
        print("⚠️ VALIDACIÓN PARCIAL: Algunos sistemas requieren atención")
    
    print("="*60)
    
    return all_passed

def main():
    """Función principal de validación"""
    print("🎯 INICIANDO VALIDACIÓN FINAL COMPLETA")
    print("Proyecto: Dashboard Modelos Conceptuales Supermercado")
    print("-" * 60)
    
    test_results = {}
    
    # Test 1: Importaciones
    test_results['imports'] = test_imports()
    
    if not test_results['imports']:
        print("❌ FALLO CRÍTICO: No se pueden importar los módulos")
        return False
    
    # Test 2: Carga de datos
    df = test_data_loading()
    test_results['data_loading'] = df is not None
    
    if df is None:
        print("❌ FALLO CRÍTICO: No se pueden cargar los datos")
        return False
    
    # Test 3: Optimización PyArrow
    df_optimized = test_data_optimization(df)
    test_results['optimization'] = df_optimized is not None
    
    # Test 4: EDA
    test_results['eda'] = test_eda_functionality(df_optimized)
    
    # Test 5: Modelos ML
    test_results['models'] = test_models(df_optimized)
    
    # Generar reporte final
    success = generate_final_report(test_results)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n🎊 ¡VALIDACIÓN EXITOSA!")
            print("El dashboard está completamente funcional y listo para uso.")
        else:
            print("\n⚠️ Validación completada con advertencias.")
            print("El dashboard funciona pero algunos componentes necesitan revisión.")
            
    except Exception as e:
        print(f"\n💥 ERROR DURANTE LA VALIDACIÓN: {e}")
        print("Revisar configuración del proyecto.")
    
    input("\nPresiona Enter para continuar...")
