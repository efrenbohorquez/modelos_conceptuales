import sys
import os
import pandas as pd

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("🧪 Test simple del modelo de segmentación...")

try:
    from data_loader import cargar_datos
    print("✅ data_loader importado correctamente")
    
    from modelo_2_segmentacion import preparar_datos_segmentacion, segmentar_clientes, caracterizar_segmentos
    print("✅ modelo_2_segmentacion importado correctamente")
    
    # Cargar datos
    df = cargar_datos()
    print(f"✅ Datos cargados: {df.shape}")
    
    # Probar segmentación
    df_segmentado, kmeans, pca, preprocessor = segmentar_clientes(df, n_clusters=3)
    print(f"✅ Segmentación completada: {df_segmentado.shape}")
    print(f"📊 Segmentos: {df_segmentado['Segmento'].value_counts().to_dict()}")
    
    # Probar caracterización
    caracterizacion = caracterizar_segmentos(df_segmentado)
    print(f"✅ Caracterización completada: {caracterizacion.shape}")
    print(caracterizacion)
    
    print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
