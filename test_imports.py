#!/usr/bin/env python3
"""
Test simple para verificar que todos los imports funcionan correctamente
"""

import sys
import os

print("🧪 Verificando imports del sistema...")

try:
    # Cambiar al directorio del proyecto
    os.chdir(r"c:\Users\Public\modelos_conceptuales")
    print(f"📁 Directorio actual: {os.getcwd()}")
    
    # Agregar src al path
    src_path = os.path.join(os.getcwd(), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    print(f"🔧 Path de Python: {sys.path[:3]}...")  # Mostrar solo los primeros 3
    
    # Test 1: Import de data_loader
    print("\n1️⃣ Probando import de data_loader...")
    from src.data_loader import cargar_datos
    print("   ✅ data_loader importado correctamente")
    
    # Test 2: Carga de datos
    print("\n2️⃣ Probando carga de datos...")
    df = cargar_datos()
    print(f"   ✅ Datos cargados: {df.shape} filas x {len(df.columns)} columnas")
    
    # Test 3: Verificar columnas importantes
    print("\n3️⃣ Verificando columnas del dataset...")
    expected_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'Rating']
    found_cols = [col for col in expected_cols if col in df.columns]
    print(f"   ✅ Columnas encontradas: {found_cols}")
    
    # Test 4: Import de modelos
    print("\n4️⃣ Probando imports de modelos...")
    from src.modelo_1_regresion import preparar_datos_regresion
    print("   ✅ modelo_1_regresion importado correctamente")
    
    from src.modelo_2_segmentacion import segmentar_clientes
    print("   ✅ modelo_2_segmentacion importado correctamente")
    
    from src.modelo_3_clasificacion import preparar_datos_clasificacion
    print("   ✅ modelo_3_clasificacion importado correctamente")
    
    from src.modelo_4_anomalias import detectar_anomalias
    print("   ✅ modelo_4_anomalias importado correctamente")
    
    print("\n🎉 TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE")
    print("✅ El sistema está listo para ejecutar Streamlit")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
