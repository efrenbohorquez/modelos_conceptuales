# 🚀 INSTRUCCIONES PARA EJECUTAR EL DASHBOARD

## Método 1: Ejecución Manual (RECOMENDADO)

Abre PowerShell o Command Prompt y ejecuta:

```bash
cd "c:\Users\Public\modelos_conceptuales"
streamlit run app.py --server.port 8508
```

## Método 2: Doble clic en archivo

Ejecuta cualquiera de estos archivos:
- `ejecutar_final.bat`
- `ejecutar_simple.ps1`

## 🌐 URL del Dashboard

Una vez ejecutado, abre tu navegador en:
**http://localhost:8508**

## ☁️ Para Streamlit Cloud

1. **Sube el proyecto completo a GitHub**
2. **Conecta con Streamlit Cloud**:
   - Ve a: https://share.streamlit.io
   - Conecta GitHub
   - Selecciona este repositorio
   - Archivo principal: `app.py`

## 📁 Archivos importantes para Cloud:

✅ `app.py` - Dashboard principal
✅ `requirements.txt` - Dependencias
✅ `src/` - Módulos de código
✅ `data/supermarket_sales.xlsx` - Dataset
✅ `.streamlit/config.toml` - Configuración

## 🔧 Si hay errores:

1. **Instalar dependencias**:
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn scikit-learn openpyxl
   ```

2. **Verificar Python**:
   ```bash
   python --version
   # Debe ser Python 3.8+
   ```

3. **Probar carga simple**:
   ```bash
   python -c "import streamlit; print('Streamlit OK')"
   ```

---
🎯 **El dashboard está listo para ejecutar y deployar en Streamlit Cloud**
