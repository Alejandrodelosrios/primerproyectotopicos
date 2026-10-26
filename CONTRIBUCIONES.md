# CONTRIBUCIONES.md

## Proyecto Integrador – Análisis de Reseñas con NLP y Machine Learning

**Materia:** Tópicos y Programación Avanzada  
**Avance:** 26/10/2026

## Integrantes
Diana Murillo
## 1. Avance "Skeleton"

**Área asignada:** Procesamiento de Lenguaje Natural y Machine Learning.

### Responsabilidades previstas

**A. Pipeline NLP**

Archivo principal: `src/nlp/preprocessing.py`

- Implementar normalización del texto en español.
- Desarrollar tokenización.
- Configurar stop words y conservar negaciones relevantes.
- Implementar stemming utilizando NLTK.
- Implementar lematización utilizando spaCy.
- Comparar unigramas y bigramas.
- Integrar la vectorización TF-IDF.
- Asegurar que el preprocesamiento sea reutilizable durante entrenamiento e inferencia.

**B. Entrenamiento del modelo**

Archivo principal: `src/models/train.py`

- Configurar un modelo de regresión logística multiclase.
- Preparar la división de datos de entrenamiento y prueba.
- Implementar una línea base de comparación.
- Ejecutar experimentos con distintas configuraciones del NLP.
- Ajustar hiperparámetros mediante validación cruzada.
- Entrenar y guardar el pipeline mediante Joblib.

**C. Evaluación**

Archivo principal: `src/models/evaluate.py`

- Calcular Accuracy, Precision, Recall y Macro F1-score.
- Calcular MAE para evaluar el error ordinal.
- Generar la matriz de confusión.
- Analizar predicciones incorrectas.
- Exportar las métricas para el backend.

**D. Integración con FastAPI**

Colaborar en la integración del modelo entrenado mediante:

- Carga de `pipeline.joblib`.
- Endpoint `/predict`.
- Endpoint `/preprocess`.
- Endpoint `/metrics`.
- Validación de la consistencia entre entrenamiento e inferencia.

### Entregables asignados

| Archivo | Entregable |
|---|---|
| `src/nlp/preprocessing.py` | Pipeline de procesamiento NLP |
| `src/models/train.py` | Entrenamiento reproducible |
| `src/models/evaluate.py` | Evaluación y comparación |
| `models/pipeline.joblib` | Modelo entrenado y serializado |
| `models/metrics.json` | Métricas de evaluación |
| `tests/test_nlp.py` | Pruebas automatizadas del NLP |

Los artefactos y pruebas se incorporarán conforme se completen las implementaciones.

### Registro de contribuciones realizadas

| Fecha | Commit | Descripción | Estado |
|---|---|---|---|
| Pendiente | Pendiente | Implementación de normalización y tokenización | Planificado |
| Pendiente | Pendiente | Stop words, stemming y lematización | Planificado |
| Pendiente | Pendiente | Vectorización TF-IDF y n-gramas | Planificado |
| Pendiente | Pendiente | Entrenamiento del clasificador | Planificado |
| Pendiente | Pendiente | Evaluación y serialización | Planificado |
| Pendiente | Pendiente | Integración y pruebas | Planificado |

**Nota:** los registros se actualizarán únicamente después de que existan los commits correspondientes.

## 2. Otros integrantes

Las contribuciones de los demás integrantes se incorporarán cuando se confirmen sus nombres y responsabilidades definitivas.

## 3. Reglas de colaboración

- Cada integrante trabajará con su propia cuenta de Git.
- Las funcionalidades se desarrollarán en ramas independientes.
- Los cambios se integrarán mediante pull requests revisados.
- Se utilizarán mensajes descriptivos siguiendo Conventional Commits.
- No se modificará la autoría del historial.
- Los trabajos colaborativos se identificarán mediante `Co-authored-by` cuando corresponda.
- Cada integrante deberá tener contribuciones significativas en NLP o Machine Learning.

## 4. Defensa individual

Cada integrante deberá demostrar conocimiento de sus contribuciones, explicar las decisiones técnicas y completar una modificación funcional durante la presentación.

El historial de Git será la evidencia principal para validar estas contribuciones.


## Desde aqui deben continuar los demas