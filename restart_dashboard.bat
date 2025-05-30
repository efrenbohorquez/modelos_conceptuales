@echo off
echo 🔄 Reiniciando Dashboard de Streamlit...

REM Detener procesos de Python existentes
echo ⏹️  Deteniendo procesos existentes...
taskkill /f /im python.exe >nul 2>&1

REM Esperar un momento
timeout /t 2 >nul

REM Navegar al directorio del proyecto
cd /d "c:\Users\Public\modelos_conceptuales"

REM Ejecutar el test de imports primero
echo 🧪 Verificando imports...
python test_imports.py
if %errorlevel% neq 0 (
    echo ❌ Error en imports. Presiona cualquier tecla para continuar...
    pause >nul
    exit /b 1
)

REM Ejecutar Streamlit
echo 🚀 Iniciando Streamlit en puerto 8507...
streamlit run app.py --server.port 8507

echo ✅ Dashboard iniciado en http://localhost:8507
pause
