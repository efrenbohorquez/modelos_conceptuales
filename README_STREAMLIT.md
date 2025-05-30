# 🎓 Dashboard de Modelos Conceptuales de Supermercado

## 🚀 Para ejecutar localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run app.py
```

## ☁️ Para Streamlit Cloud:

1. **Subir a GitHub**: Sube este proyecto completo a un repositorio de GitHub
2. **Conectar Streamlit Cloud**: 
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona este repositorio
   - Archivo principal: `app.py`
3. **Deploy automático**: Streamlit Cloud detectará automáticamente el `requirements.txt`

## 📊 Características:

- ✅ **Análisis Exploratorio de Datos (EDA)**
- ✅ **Modelo de Regresión** (Predicción de Rating)
- ✅ **Modelo de Segmentación** (Clustering de Clientes)
- ✅ **Modelo de Clasificación** (Categorización de Productos)
- ✅ **Detección de Anomalías** (Outliers en Ventas)

## 🔧 Estructura del Proyecto:

```
├── app.py                 # Dashboard principal
├── requirements.txt       # Dependencias
├── .streamlit/           # Configuración Streamlit
├── src/                  # Módulos de análisis
│   ├── data_loader.py    # Carga de datos
│   ├── eda.py           # Análisis exploratorio
│   ├── modelo_*.py      # Modelos ML
│   └── ...
└── data/                # Datasets
    └── supermarket_sales.xlsx
```

## 📈 Dataset:

El dashboard funciona con el dataset `supermarket_sales.xlsx` que contiene:
- **1000 registros** de ventas de supermercado
- **17 columnas** incluyendo precios, cantidades, ratings, etc.
- **Variables categóricas**: Branch, City, Customer type, Gender, Product line, Payment
- **Variables numéricas**: Unit price, Quantity, Tax 5%, Total, Rating, etc.

## 🎯 Uso:

1. **Cargar datos** (automático o subir archivo)
2. **Explorar** variables en la sección EDA
3. **Ejecutar modelos** de ML desde la barra lateral
4. **Visualizar resultados** con gráficos interactivos

---
**Desarrollado para**: Maestría en Analítica de Datos - Universidad Central
