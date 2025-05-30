@echo off
echo ========================================
echo DASHBOARD DE MODELOS CONCEPTUALES
echo ========================================
echo.
echo Iniciando dashboard en puerto 8506...
echo URL: http://localhost:8506
echo.
echo Presiona Ctrl+C para detener
echo.

cd /d "C:\Users\Public\modelos_conceptuales"
python -m streamlit run app.py --server.port 8506

pause
