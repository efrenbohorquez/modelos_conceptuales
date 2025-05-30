#!/usr/bin/env python3
"""
Script de prueba final para el dashboard con dataset real
"""
import pandas as pd
import sys
import os

# Agregar src al path
sys.path.append('src')

def main():
    print("🧪 PRUEBA FINAL - DATASET REAL DE SUPERMERCADO")
    print("="*60)
    
    # 1. Verificar dataset real
    dataset_real = r'C:\Users\efren\Downloads\supermarket_sales.xlsx'
    print(f"📁 Buscando dataset: {dataset_real}")
    
    if not os.path.exists(dataset_real):
        print("❌ Dataset real no encontrado")
        print("🔄 Usando dataset de prueba como alternativa...")
        dataset_real = 'data/test_supermarket_data.csv'
        if not os.path.exists(dataset_real):
            print("❌ Dataset de prueba tampoco encontrado")
            return False
    
    # 2. Cargar dataset
    try:
        if dataset_real.endswith('.xlsx'):
            df = pd.read_excel(dataset_real)
        else:
            df = pd.read_csv(dataset_real)
        print(f"✅ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    except Exception as e:
        print(f"❌ Error cargando dataset: {e}")
        return False
    
    # 3. Mostrar estructura del dataset
    print(f"\n📋 ESTRUCTURA DEL DATASET:")
    print(f"Columnas encontradas ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # 4. Verificar compatibilidad con modelos
    from mapeo_columnas import verificar_columnas_disponibles, mapear_columnas_dataset
    
    columnas_requeridas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment', 'Rating']
    info = verificar_columnas_disponibles(df, columnas_requeridas)
    
    print(f"\n🎯 COMPATIBILIDAD CON MODELOS ML:")
    print(f"Porcentaje de columnas disponibles: {info['porcentaje_disponible']:.1f}%")
    print(f"✅ Columnas encontradas: {info['columnas_encontradas']}")
    print(f"❌ Columnas faltantes: {info['columnas_faltantes']}")
    
    # 5. Aplicar mapeo si es necesario
    if info['porcentaje_disponible'] < 100:
        print(f"\n🔄 APLICANDO MAPEO DE COLUMNAS...")
        try:
            df_mapped = mapear_columnas_dataset(df)
            print(f"✅ Mapeo completado")
            
            # Verificar resultado
            info_despues = verificar_columnas_disponibles(df_mapped, columnas_requeridas)
            print(f"📊 Compatibilidad después del mapeo: {info_despues['porcentaje_disponible']:.1f}%")
            print(f"✅ Columnas encontradas: {info_despues['columnas_encontradas']}")
            print(f"❌ Columnas aún faltantes: {info_despues['columnas_faltantes']}")
            
            df_final = df_mapped
        except Exception as e:
            print(f"❌ Error en mapeo: {e}")
            df_final = df
    else:
        print("✅ Dataset ya es compatible")
        df_final = df
    
    # 6. Verificar modelos específicos
    print(f"\n🔍 VERIFICACIÓN POR MODELO:")
    
    # Modelo 1: Regresión
    rating_ok = 'Rating' in df_final.columns
    numeric_cols = df_final.select_dtypes(include=['number']).columns.tolist()
    print(f"🎯 Regresión: {'✅' if rating_ok and len(numeric_cols) >= 3 else '❌'}")
    print(f"   - Rating: {'✅' if rating_ok else '❌'}")
    print(f"   - Variables numéricas: {len(numeric_cols)}")
    
    # Modelo 2: Segmentación
    seg_ok = len(numeric_cols) >= 2
    print(f"👥 Segmentación: {'✅' if seg_ok else '❌'}")
    print(f"   - Variables numéricas: {len(numeric_cols)}")
    
    # Modelo 3: Clasificación
    product_ok = 'Product line' in df_final.columns
    print(f"🛍️ Clasificación: {'✅' if product_ok else '❌'}")
    print(f"   - Product line: {'✅' if product_ok else '❌'}")
    
    # Modelo 4: Anomalías
    anom_ok = len(df_final.columns) >= 3
    print(f"🔍 Anomalías: {'✅' if anom_ok else '❌'}")
    print(f"   - Variables totales: {len(df_final.columns)}")
    
    # 7. Resumen final
    modelos_ok = sum([
        rating_ok and len(numeric_cols) >= 3,  # Regresión
        seg_ok,                                # Segmentación
        product_ok,                           # Clasificación
        anom_ok                               # Anomalías
    ])
    
    print(f"\n📋 RESUMEN FINAL:")
    print(f"✅ Modelos compatibles: {modelos_ok}/4")
    print(f"✅ Dataset final: {df_final.shape[0]} × {df_final.shape[1]}")
    
    if modelos_ok >= 3:
        print(f"\n🎉 ¡DASHBOARD LISTO!")
        print(f"Para ejecutar:")
        print(f"  streamlit run app.py --server.port 8506")
        return True
    else:
        print(f"\n⚠️ Algunos modelos pueden tener problemas")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🚀 Todo listo para la demostración!")
    else:
        print(f"\n❌ Revisar configuración antes de la demo")
