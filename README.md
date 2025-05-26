<!--
Este proyecto está alineado y documentado según la arquitectura conceptual ubicada en:
C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md
-->

# 🏪 Modelos Conceptuales de Redes Neuronales para Supermercados

**🎉 ¡PROYECTO COMPLETAMENTE ACTUALIZADO Y FUNCIONAL!**

Este proyecto implementa un dashboard interactivo con cuatro modelos conceptuales de redes neuronales aplicados a datos de ventas de supermercados, con las siguientes características:

## ✨ **Nuevas Funcionalidades (Actualización 2025)**
- 🎯 **Validaciones inteligentes** con recomendaciones específicas por modelo
- 📊 **Visualizaciones interactivas** con Plotly para análisis moderno
- 🔧 **Guías de selección** de variables automáticas
- 🎨 **Interfaz modernizada** con diseño profesional
- 🧪 **Datos de prueba** incluidos para demostración inmediata

## 🚀 **Modelos Implementados:**
1. **Regresión de Ventas** - Predicción de patrones de venta
2. **Segmentación de Clientes** - Clustering inteligente con PCA
3. **Clasificación de Satisfacción** - Predicción de satisfacción del cliente  
4. **Detección de Anomalías** - Identificación de patrones inusuales

## Objetivos del Proyecto

El objetivo principal es proporcionar una herramienta interactiva para el análisis y modelado de datos de supermercados, facilitando la toma de decisiones basada en datos. Los objetivos específicos son:

1. **Predicción de la Calificación del Cliente (Regresión):**
   - Desarrollar un modelo que prediga la satisfacción del cliente a partir de las características de la transacción y del cliente.
   - Identificar los factores que más influyen en la satisfacción.

2. **Segmentación de Clientes (Clustering con PCA):**
   - Agrupar clientes en segmentos homogéneos según su comportamiento de compra y características demográficas.
   - Facilitar estrategias de marketing personalizadas y optimización de servicios.

3. **Predicción de la Siguiente Línea de Producto (Clasificación):**
   - Predecir la categoría de producto que un cliente podría comprar a continuación.
   - Apoyar la gestión de inventario y la personalización de promociones.

## Estructura del proyecto

- `data/`: Suba aquí su archivo de datos (ejemplo: `supermarket_sales.xlsx`).
- `notebooks/`: Análisis exploratorio y pruebas en Jupyter.
- `src/`: Código fuente modularizado.
- `app.py`: Aplicación principal de Streamlit.
- `docs/`: Documentación y especificaciones.

# 🚀 Inicio Rápido

## **Método 1: Script Automatizado (Recomendado)**
```powershell
# Ejecutar en PowerShell desde el directorio del proyecto
.\run_dashboard.ps1
```

## **Método 2: Manual**
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar dashboard
streamlit run app.py --server.port 8506
```

## 🌐 **Acceso al Dashboard**
Una vez iniciado, abrir en el navegador: **http://localhost:8506**

## 📊 **Datos de Prueba Incluidos**
- `data/test_supermarket_data.csv` - Transacciones de ejemplo
- `data/clientes_info.csv` - Perfiles de clientes

---

## 🔧 **Características Técnicas Actualizadas**

### **Dependencias Nuevas:**
- ✅ **Plotly** - Visualizaciones interactivas modernas
- ✅ **Streamlit** - Framework web actualizado
- ✅ **Pandas/NumPy** - Procesamiento de datos optimizado

### **Validaciones Inteligentes:**
- 🎯 Recomendaciones automáticas de variables por modelo
- ⚠️ Advertencias contextuales sobre calidad de datos
- 🔧 Botones de configuración rápida
- 📊 Métricas de rendimiento en tiempo real

### **Interfaz Modernizada:**
- 🎨 Diseño profesional con paleta de colores consistente
- 📱 Diseño responsivo para diferentes dispositivos
- 🔍 Navegación intuitiva entre secciones
- 💡 Guías desplegables con explicaciones detalladas

---

## 📋 **Estado del Proyecto: COMPLETO ✅**

**Última actualización:** 26 de mayo de 2025  
**Estado:** ✅ Totalmente funcional y probado  
**Errores de sintaxis:** ✅ Corregidos completamente  
**Dependencias:** ✅ Instaladas y verificadas  
**Datos de prueba:** ✅ Incluidos y listos para uso  

---

*🎉 ¡El dashboard está listo para usar! Sigue las instrucciones de inicio rápido para comenzar.*

## Requisitos

- Python 3.8+
- Streamlit
- Pandas, Numpy, Scikit-learn, Matplotlib, Seaborn, Openpyxl
- (Tensorflow/Keras solo si usas Python <=3.11)

## Uso de la aplicación

1. Sube tu archivo de datos en formato Excel (`.xlsx`).
2. Explora el análisis descriptivo y la visualización de los datos.
3. Selecciona el modelo a ejecutar:
   - **Regresión:** Entrena y evalúa un modelo para predecir la calificación del cliente.
   - **Segmentación:** Agrupa clientes en segmentos y visualiza sus características.
   - **Clasificación:** Predice la próxima línea de producto que un cliente podría comprar.
4. Visualiza métricas, reportes y gráficos interactivos para cada modelo.

## Créditos y alineación conceptual

Este proyecto sigue la arquitectura y especificaciones documentadas en el archivo `modelos_conceptuales.md` ubicado en la carpeta `docs/` y en la ruta original proporcionada.

---

¿Dudas, sugerencias o mejoras? ¡Contribuciones y feedback son bienvenidos!
