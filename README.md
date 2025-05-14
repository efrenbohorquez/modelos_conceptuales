# Modelos Conceptuales de Redes Neuronales para Supermercados

Este proyecto implementa tres modelos de redes neuronales sobre datos de ventas de supermercados, permitiendo:
- Carga y visualización de datos.
- Análisis descriptivo interactivo.
- Entrenamiento y visualización de los modelos propuestos (regresión, clustering, clasificación).

## Objetivos del Proyecto

El objetivo principal es proporcionar una herramienta interactiva para el análisis y modelado de datos de supermercados, facilitando la toma de decisiones basada en datos. Los objetivos específicos son:

1. **Predicción de la Calificación del Cliente (Regresión):**
   - Desarrollar un modelo que prediga la satisfacción del cliente a partir de las características de la transacción y del cliente.
   - Identificar los factores que más influyen en la satisfacción.

2. **Segmentación de Clientes (Clustering con Autoencoders):**
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

## Instalación rápida

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Requisitos
- Python 3.8+
- Streamlit
- Pandas, Numpy, Scikit-learn, (Tensorflow/Keras solo si usas Python <=3.11), Matplotlib, Seaborn
