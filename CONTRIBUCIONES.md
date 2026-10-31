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


## Brayan Gonzales

**Área:** Frontend.
**Tecnologías:** React, TypeScript, Bootstrap y Vite.

### Primer avance: formulario y vista de preprocesamiento

Implementé una interfaz que permite ingresar una reseña y consultar
su preprocesamiento mediante la API del backend.

### Contribuciones realizadas

- Integración de Bootstrap para los estilos de la interfaz.
- Formulario de ingreso de reseñas con contador de caracteres.
- Validación del texto entre 3 y 5000 caracteres, después de
  eliminar espacios al inicio y al final.
- Consumo del endpoint POST /api/v1/preprocess mediante fetch.
- Visualización del texto original, texto normalizado y tokens.
- Manejo del estado de carga y mensajes de error.
- Configuración del proxy de Vite para conectar con el backend
  durante el desarrollo.
- Incorporación de etiquetas y atributos de accesibilidad.

### Archivos principales

- frontend/src/App.tsx
- frontend/src/main.tsx
- frontend/src/index.css
- frontend/vite.config.ts
- frontend/package.json
- frontend/package-lock.json

### Evidencia en Git

| Commit | Descripción |
| --- | --- |
| 1eb3a58 | feat(frontend): agregar formulario y vista de preprocesamiento |

### Verificación

- Compilación con npm run build: correcta.
- Revisión con npm run lint: sin errores.

### Trabajo pendiente

- Integrar la predicción de estrellas cuando esté disponible.
- Mostrar las etapas adicionales de preprocesamiento cuando
  las exponga la API.
- Implementar el panel de métricas del modelo.


### Segundo avance: predicción y preprocesamiento completo

Amplié la interfaz para consultar la predicción de estrellas y
visualizar todas las etapas de preprocesamiento expuestas por la API.

#### Contribuciones realizadas

- Separación de las peticiones HTTP y los tipos de respuesta
  en frontend/src/services/reviews.ts.
- Integración con POST /api/v1/predict.
- Visualización de la puntuación estimada mediante estrellas.
- Presentación de la probabilidad de la puntuación predicha.
- Visualización de probabilidades para las cinco puntuaciones.
- Ampliación del preprocesamiento para mostrar stop words
  eliminadas, tokens conservados, raíces o lemas y texto final
  para el vectorizador TF-IDF.
- Ejecución paralela de las consultas mediante Promise.allSettled.
- Manejo independiente de errores de predicción y preprocesamiento.
- Creación de un componente reutilizable para visualizar tokens.

#### Archivos principales

- frontend/src/App.tsx
- frontend/src/services/reviews.ts

#### Evidencia en Git

- Rama: feature/frontend-prediction.
- Commit: completar con el identificador después de crearlo.

#### Trabajo pendiente

- Implementar el panel de métricas del modelo.