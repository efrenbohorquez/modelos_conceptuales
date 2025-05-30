#!/usr/bin/env python3
"""
🚀 EJECUTOR FINAL DEL DASHBOARD
Versión simplificada para máxima compatibilidad
"""

import os
import sys

def main():
    print("🚀 Dashboard de Modelos Conceptuales - Ejecutor Final")
    print("=" * 55)
    
    # Verificar que estamos en el directorio correcto
    project_dir = r"c:\Users\Public\modelos_conceptuales"
    if os.path.exists(project_dir):
        os.chdir(project_dir)
        print(f"📁 Directorio: {os.getcwd()}")
    else:
        print(f"❌ No se encuentra el directorio: {project_dir}")
        return
    
    # Verificar archivo principal
    if not os.path.exists("app.py"):
        print("❌ No se encuentra app.py")
        return
    
    print("📋 Archivos encontrados:")
    print("   ✅ app.py")
    print("   ✅ requirements.txt" if os.path.exists("requirements.txt") else "   ⚠️  requirements.txt no encontrado")
    print("   ✅ src/" if os.path.exists("src") else "   ⚠️  directorio src/ no encontrado")
    print("   ✅ data/" if os.path.exists("data") else "   ⚠️  directorio data/ no encontrado")
    
    print("\n🌐 PARA EJECUTAR MANUALMENTE:")
    print("   streamlit run app.py --server.port 8508")
    print("\n🔗 URL del dashboard: http://localhost:8508")
    
    print("\n☁️  PARA STREAMLIT CLOUD:")
    print("   1. Sube este proyecto completo a GitHub")
    print("   2. Ve a https://share.streamlit.io")
    print("   3. Conecta tu repositorio")
    print("   4. Archivo principal: app.py")
    
    print("\n✅ El proyecto está listo para ejecutar y deployar")
    
    # Intentar ejecutar automáticamente
    try:
        import subprocess
        print("\n🚀 Intentando ejecutar automáticamente...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8508"])
    except Exception as e:
        print(f"\n⚠️  Ejecución automática falló: {e}")
        print("💡 Ejecuta manualmente: streamlit run app.py --server.port 8508")

if __name__ == "__main__":
    main()
