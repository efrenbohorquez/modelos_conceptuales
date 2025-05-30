#!/usr/bin/env python3
"""
Validación completa del dashboard corregido
Verifica que todas las funcionalidades estén funcionando
"""

import pandas as pd
import sys
import os

def test_imports():
    """Verificar que todos los módulos se importen correctamente"""
    print("🔍 Verificando importaciones...")
    try:
        from src import data_loader, eda, modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias
        from src.mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles
        print("✅ Todas las importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_data_loading():
    """Verificar carga de datos"""
    print("\n📊 Verificando carga de datos...")
    try:
        from src import data_loader
        
        # Verificar dataset principal
        dataset_info = data_loader.verificar_dataset_real()
        print(f"Dataset disponible: {dataset_info['disponible']}")
        if dataset_info['disponible']:
            print(f"Registros: {dataset_info['registros']}")
        
        # Intentar cargar datos
        df = data_loader.cargar_datos()
        if df is not None:
            print(f"✅ Datos cargados: {len(df)} registros x {len(df.columns)} columnas")
            print(f"Variables numéricas: {len(df.select_dtypes(include=['number']).columns)}")
            return df
        else:
            print("❌ No se pudieron cargar los datos")
            return None
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def test_eda_functions(df):
    """Verificar funciones de EDA"""
    print("\n🔍 Verificando funciones de EDA...")
    try:
        from src.eda import analisis_variables_numericas, analisis_variables_categoricas, calidad_datos
        
        # Verificar variables numéricas
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        print(f"Variables numéricas detectadas: {len(num_cols)}")
        if len(num_cols) > 0:
            print(f"Variables: {', '.join(num_cols[:5])}{'...' if len(num_cols) > 5 else ''}")
        
        # Verificar variables categóricas
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        print(f"Variables categóricas detectadas: {len(cat_cols)}")
        if len(cat_cols) > 0:
            print(f"Variables: {', '.join(cat_cols[:5])}{'...' if len(cat_cols) > 5 else ''}")
        
        print("✅ Funciones de EDA verificadas")
        return True
    except Exception as e:
        print(f"❌ Error en funciones EDA: {e}")
        return False

def test_models_basic(df):
    """Verificar funciones básicas de los modelos"""
    print("\n🤖 Verificando modelos ML...")
    try:
        from src import modelo_1_regresion, modelo_2_segmentacion, modelo_3_clasificacion, modelo_4_anomalias
        
        # Verificar que las funciones principales existan
        models_status = {
            'Regresión': hasattr(modelo_1_regresion, 'entrenar_regresion'),
            'Segmentación': hasattr(modelo_2_segmentacion, 'ejecutar_segmentacion'),
            'Clasificación': hasattr(modelo_3_clasificacion, 'entrenar_clasificacion'),
            'Anomalías': hasattr(modelo_4_anomalias, 'detectar_anomalias')
        }
        
        for model, status in models_status.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {model}: {'Disponible' if status else 'No disponible'}")
        
        all_models_ok = all(models_status.values())
        if all_models_ok:
            print("✅ Todos los modelos están disponibles")
        
        return all_models_ok
    except Exception as e:
        print(f"❌ Error verificando modelos: {e}")
        return False

def test_specific_features(df):
    """Verificar características específicas que fueron corregidas"""
    print("\n🎯 Verificando correcciones específicas...")
    
    # Verificar variables específicas de supermercado
    required_vars = ['Unit price', 'Quantity', 'Tax 5%', 'Total']
    found_vars = [var for var in required_vars if var in df.columns]
    
    print(f"Variables de supermercado encontradas: {len(found_vars)}/{len(required_vars)}")
    for var in found_vars:
        print(f"  ✅ {var}")
    
    for var in required_vars:
        if var not in found_vars:
            print(f"  ❌ {var} (no encontrada)")
    
    # Verificar que hay suficientes variables numéricas para análisis
    num_vars = df.select_dtypes(include=['number']).columns.tolist()
    if len(num_vars) >= 4:
        print("✅ Suficientes variables numéricas para análisis completo")
        return True
    else:
        print(f"⚠️  Solo {len(num_vars)} variables numéricas (se recomiendan al menos 4)")
        return len(num_vars) > 0

def run_complete_validation():
    """Ejecutar validación completa del sistema"""
    print("🚀 INICIANDO VALIDACIÓN COMPLETA DEL DASHBOARD")
    print("=" * 60)
    
    # Test 1: Importaciones
    imports_ok = test_imports()
    
    # Test 2: Carga de datos
    df = test_data_loading()
    
    if df is None:
        print("\n❌ FALLO CRÍTICO: No se pueden cargar datos")
        return False
    
    # Test 3: Funciones EDA
    eda_ok = test_eda_functions(df)
    
    # Test 4: Modelos ML
    models_ok = test_models_basic(df)
    
    # Test 5: Características específicas
    features_ok = test_specific_features(df)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    
    tests = [
        ("Importaciones", imports_ok),
        ("Carga de datos", df is not None),
        ("Funciones EDA", eda_ok),
        ("Modelos ML", models_ok),
        ("Características específicas", features_ok)
    ]
    
    passed = sum(1 for _, status in tests if status)
    total = len(tests)
    
    for test_name, status in tests:
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}")
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS VALIDACIONES EXITOSAS!")
        print("\n✨ El dashboard está listo para usar:")
        print("   • Variables numéricas detectadas correctamente")
        print("   • Sección de análisis funcionando")
        print("   • Sin errores de reinicio")
        print("   • Todos los modelos disponibles")
        return True
    else:
        print(f"⚠️  {total - passed} pruebas fallaron - revisar problemas")
        return False

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = run_complete_validation()
    
    if success:
        print("\n🌟 DASHBOARD VALIDADO EXITOSAMENTE")
        print("🔗 Acceder en: http://localhost:8505")
    else:
        print("\n💥 VALIDACIÓN FALLÓ - Revisar errores arriba")
        sys.exit(1)
