import pandas as pd
from src.mapeo_columnas import mapear_columnas_dataset, verificar_columnas_disponibles

print("=== TEST MAPEO COLUMNAS ===")

# Cargar dataset
df = pd.read_csv('data/test_supermarket_data.csv')
print(f"Dataset original: {df.shape}")
print(f"Columnas: {df.columns.tolist()}")

# Verificar necesidad de mapeo
columnas_requeridas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
info = verificar_columnas_disponibles(df, columnas_requeridas)
print(f"Porcentaje disponible: {info['porcentaje_disponible']}%")
print(f"Columnas encontradas: {info['columnas_encontradas']}")
print(f"Columnas faltantes: {info['columnas_faltantes']}")

if info['porcentaje_disponible'] < 50:
    print("\n=== APLICANDO MAPEO ===")
    df_mapped = mapear_columnas_dataset(df)
    print(f"Columnas después del mapeo: {df_mapped.columns.tolist()}")
    
    info2 = verificar_columnas_disponibles(df_mapped, columnas_requeridas)
    print(f"Porcentaje después del mapeo: {info2['porcentaje_disponible']}%")
    print(f"Columnas encontradas: {info2['columnas_encontradas']}")
    print(f"Columnas faltantes: {info2['columnas_faltantes']}")
    
    # Verificar columnas específicas para modelos
    print(f"\n=== VERIFICACIÓN MODELOS ===")
    print(f"Rating disponible: {'Rating' in df_mapped.columns}")
    print(f"Product line disponible: {'Product line' in df_mapped.columns}")
    print(f"Variables numéricas: {len(df_mapped.select_dtypes(include=['number']).columns)}")
else:
    print("No se necesita mapeo")
