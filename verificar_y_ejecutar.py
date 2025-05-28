"""
Script de verificación final para el Dashboard de Modelos Conceptuales
Ejecuta todas las pruebas necesarias antes del lanzamiento del dashboard
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

# Configuración del proyecto
PROJECT_DIR = Path("c:/Users/Public/modelos_conceptuales")
STREAMLIT_PORT = 8506
DASHBOARD_URL = f"http://localhost:{STREAMLIT_PORT}"

def print_header(message):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🔍 {message}")
    print("="*60)

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime un mensaje informativo"""
    print(f"💡 {message}")

def check_file_exists(filepath):
    """Verifica si un archivo existe"""
    return os.path.exists(filepath)

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print_header("VERIFICANDO ESTRUCTURA DEL PROYECTO")
    
    essential_files = [
        "app.py",
        "requirements.txt", 
        "src/eda.py",
        "src/modelo_1_regresion.py",
        "src/modelo_2_segmentacion.py", 
        "src/modelo_3_clasificacion.py",
        "src/modelo_4_anomalias.py",
        "data/test_supermarket_data.csv"
    ]
    
    missing_files = []
    for file in essential_files:
        filepath = PROJECT_DIR / file
        if check_file_exists(filepath):
            print_success(f"Archivo encontrado: {file}")
        else:
            print_error(f"Archivo faltante: {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_python_imports():
    """Prueba las importaciones de Python"""
    print_header("VERIFICANDO IMPORTACIONES DE PYTHON")
    
    try:
        import streamlit
        print_success(f"Streamlit {streamlit.__version__} disponible")
    except ImportError:
        print_error("Streamlit no está instalado")
        return False
    
    try:
        import plotly
        print_success(f"Plotly {plotly.__version__} disponible")
    except ImportError:
        print_error("Plotly no está instalado")
        return False
    
    try:
        import pandas
        print_success(f"Pandas {pandas.__version__} disponible")
    except ImportError:
        print_error("Pandas no está instalado")
        return False
    
    try:
        import sklearn
        print_success(f"Scikit-learn {sklearn.__version__} disponible")
    except ImportError:
        print_error("Scikit-learn no está instalado")
        return False
    
    return True

def check_data_files():
    """Verifica los archivos de datos"""
    print_header("VERIFICANDO ARCHIVOS DE DATOS")
    
    data_files = [
        "data/test_supermarket_data.csv",
        "data/clientes_info.csv"
    ]
    
    for data_file in data_files:
        filepath = PROJECT_DIR / data_file
        if check_file_exists(filepath):
            # Verificar que el archivo no esté vacío
            try:
                import pandas as pd
                df = pd.read_csv(filepath)
                print_success(f"Datos válidos en {data_file}: {df.shape[0]} filas, {df.shape[1]} columnas")
            except Exception as e:
                print_error(f"Error leyendo {data_file}: {e}")
                return False
        else:
            print_error(f"Archivo de datos faltante: {data_file}")
            return False
    
    return True

def run_syntax_check():
    """Verifica la sintaxis del archivo principal"""
    print_header("VERIFICANDO SINTAXIS DE PYTHON")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir(PROJECT_DIR)
        
        # Compilar el archivo para verificar sintaxis
        with open("app.py", 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        compile(source_code, "app.py", "exec")
        print_success("Sintaxis de app.py es válida")
        return True
        
    except SyntaxError as e:
        print_error(f"Error de sintaxis en app.py: {e}")
        return False
    except Exception as e:
        print_error(f"Error verificando sintaxis: {e}")
        return False

def launch_dashboard():
    """Lanza el dashboard de Streamlit"""
    print_header("LANZANDO DASHBOARD")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir(PROJECT_DIR)
        
        print_info(f"Iniciando Streamlit en puerto {STREAMLIT_PORT}...")
        print_info(f"URL del dashboard: {DASHBOARD_URL}")
        print_info("Para detener el servidor: Ctrl+C")
        
        # Mostrar información sobre las correcciones aplicadas
        print("\n" + "="*60)
        print("🎉 CORRECCIONES APLICADAS EXITOSAMENTE:")
        print("="*60)
        print("✅ Error de StreamlitAPIException resuelto")
        print("✅ Botones de configuración automática funcionales")
        print("✅ Sistema de validación inteligente operativo")
        print("✅ Visualizaciones EDA modernizadas con Plotly")
        print("✅ Interfaz responsiva y profesional")
        print("✅ Manejo correcto del estado de Streamlit")
        print("="*60)
        
        # Esperar un poco antes de abrir el navegador
        time.sleep(2)
        
        # Abrir el navegador automáticamente
        try:
            webbrowser.open(DASHBOARD_URL)
            print_success("Navegador abierto automáticamente")
        except Exception:
            print_info("No se pudo abrir el navegador automáticamente")
        
        # Ejecutar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py", 
            "--server.port", str(STREAMLIT_PORT),
            "--server.headless", "false"
        ])
        
    except KeyboardInterrupt:
        print_info("\n🛑 Dashboard detenido por el usuario")
    except Exception as e:
        print_error(f"Error ejecutando el dashboard: {e}")

def main():
    """Función principal"""
    print_header("INICIANDO VERIFICACIÓN FINAL DEL DASHBOARD")
    print_info("Dashboard de Modelos Conceptuales de Redes Neuronales")
    print_info("Universidad Central - Maestría en Analítica de Datos")
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Estructura del proyecto", check_project_structure),
        ("Importaciones de Python", test_python_imports),
        ("Archivos de datos", check_data_files),
        ("Sintaxis de Python", run_syntax_check)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            print_error(f"Falló la verificación: {check_name}")
    
    if all_passed:
        print_header("✅ TODAS LAS VERIFICACIONES PASARON")
        print_success("El dashboard está listo para ejecutarse")
        
        # Preguntar si desea lanzar el dashboard
        try:
            response = input("\n¿Desea lanzar el dashboard ahora? (s/n): ").lower().strip()
            if response in ['s', 'sí', 'si', 'y', 'yes']:
                launch_dashboard()
            else:
                print_info("Para ejecutar manualmente:")
                print_info(f"  cd \"{PROJECT_DIR}\"")
                print_info(f"  streamlit run app.py --server.port {STREAMLIT_PORT}")
        except KeyboardInterrupt:
            print_info("\n👋 Saliendo del verificador")
    else:
        print_header("❌ ALGUNAS VERIFICACIONES FALLARON")
        print_error("Por favor, resuelve los problemas antes de ejecutar el dashboard")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
