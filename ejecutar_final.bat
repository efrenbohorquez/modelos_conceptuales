@echo off
echo 🚀 Ejecutando Dashboard de Streamlit - Versión Final
echo ================================================

cd /d "c:\Users\Public\modelos_conceptuales"

echo 📍 Directorio actual: %cd%
echo 🔧 Instalando dependencias si es necesario...
pip install -q streamlit pandas numpy matplotlib seaborn scikit-learn openpyxl xlrd

echo 🌐 Iniciando Streamlit...
echo ✅ Dashboard estará disponible en: http://localhost:8508
echo 🔗 Para Streamlit Cloud, sube este proyecto a GitHub

streamlit run app.py --server.port 8508 --server.headless false

pause
