<!--
Este proyecto está alineado y documentado según la arquitectura conceptual ubicada en:
C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md
-->

# Modelos Conceptuales de Redes Neuronales para Supermercados

Este proyecto implementa y documenta tres modelos conceptuales de redes neuronales aplicados a datos de ventas de supermercados, permitiendo:

- Carga y visualización de datos.
- Análisis descriptivo interactivo.
- Entrenamiento y visualización de los modelos propuestos:
  - Regresión (predicción de calificación del cliente)
  - Segmentación de clientes (clustering sobre embeddings PCA)
  - Clasificación multiclase (predicción de próxima línea de producto)

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
