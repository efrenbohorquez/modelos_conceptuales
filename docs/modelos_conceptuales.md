# Explicación de los Modelos y Conceptos de Redes Neuronales Aplicados

## Regresión (MLPRegressor)
Utiliza un perceptrón multicapa (red neuronal feedforward) para predecir la calificación del cliente. El modelo aprende relaciones no lineales entre variables transaccionales/demográficas y la calificación, usando capas ocultas y activación ReLU.

## Segmentación (PCA + KMeans)
Simula el uso de autoencoders (redes neuronales para reducción de dimensionalidad) mediante PCA para obtener una representación latente de los datos y luego agrupa clientes con KMeans. Los autoencoders permiten encontrar patrones complejos y PCA es una aproximación clásica.

## Clasificación (MLPClassifier)
Implementa una red neuronal multicapa para predecir la próxima línea de producto. Utiliza softmax en la salida para clasificación multiclase y aprende límites de decisión complejos mediante retropropagación.

## Detección de Anomalías (Isolation Forest)
     
### Descripción del modelo:
Isolation Forest es un algoritmo basado en árboles aleatorios que identifica observaciones atípicas (anómalas) en conjuntos de datos multivariados. Es eficiente para grandes volúmenes de datos y no requiere que las variables sigan una distribución específica.
- Aísla observaciones mediante divisiones aleatorias; las que requieren menos divisiones para ser aisladas son consideradas anomalías.
- Útil para detectar fraudes, errores de captura y comportamientos inusuales.
- El parámetro `contamination` controla la proporción esperada de anomalías.
