import pandas as pd
import os

print("🔍 Verificando dataset real de supermercado...")

# Verificar si el archivo existe
archivo = r'C:\Users\efren\Downloads\supermarket_sales.xlsx'
print(f"📁 Buscando archivo: {archivo}")

if os.path.exists(archivo):
    print('✅ Archivo encontrado')
    try:
        df = pd.read_excel(archivo)
        print(f'📊 Forma del dataset: {df.shape}')
        print(f'📋 Columnas disponibles:')
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f'\n🔍 Primeras 3 filas:')
        print(df.head(3).to_string())
        
        print(f'\n📈 Tipos de datos:')
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
            
        # Verificar si necesita mapeo
        columnas_modelos = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment', 'Rating']
        columnas_encontradas = [col for col in columnas_modelos if col in df.columns]
        print(f'\n🎯 Columnas requeridas por modelos encontradas: {len(columnas_encontradas)}/{len(columnas_modelos)}')
        print(f'✅ Encontradas: {columnas_encontradas}')
        print(f'❌ Faltantes: {[col for col in columnas_modelos if col not in df.columns]}')
        
    except Exception as e:
        print(f'❌ Error al leer el archivo: {e}')
else:
    print('❌ Archivo no encontrado en la ruta especificada')
    print('🔍 Verificando archivos .xlsx en Downloads...')
    downloads_dir = r'C:\Users\efren\Downloads'
    if os.path.exists(downloads_dir):
        xlsx_files = [f for f in os.listdir(downloads_dir) if f.endswith('.xlsx')]
        print(f'📁 Archivos .xlsx encontrados: {xlsx_files}')
    else:
        print('❌ Directorio Downloads no encontrado')
