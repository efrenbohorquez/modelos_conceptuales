#!/usr/bin/env python3
"""
Script simple para ejecutar el dashboard
"""
import subprocess
import sys
import os

# Cambiar al directorio del proyecto
os.chdir(r"c:\Users\Public\modelos_conceptuales")

print("🚀 Iniciando Dashboard de Streamlit...")
print("📍 Directorio:", os.getcwd())
print("🌐 URL: http://localhost:8508")
print("=" * 50)

try:
    # Ejecutar Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py", 
        "--server.port", "8508",
        "--server.headless", "false"
    ])
except KeyboardInterrupt:
    print("\n🛑 Dashboard detenido por el usuario")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Intenta ejecutar manualmente: streamlit run app.py --server.port 8508")
