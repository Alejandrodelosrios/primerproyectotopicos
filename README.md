# Proyecto Integrador – Análisis de Reseñas de Productos

**Materia:** Tópicos y Programación Avanzada  
**Tipo:** Proyecto integrador – Primer Parcial  
**Presentación:** 3 de noviembre de 2026  
**Tecnologías:** Python, NLP, Machine Learning, FastAPI y React

## Descripción

Aplicación web que utiliza técnicas de Procesamiento de Lenguaje Natural (NLP) y Machine Learning para analizar reseñas de productos escritas en español y predecir una calificación entre 1 y 5 estrellas.

El sistema permitirá ingresar una reseña, procesar su contenido mediante un pipeline NLP y obtener una puntuación estimada utilizando un modelo de clasificación supervisada.

## Objetivo general

Desarrollar una aplicación web que integre procesamiento de texto, entrenamiento de modelos de Machine Learning, una API REST y una interfaz web para predecir la puntuación de reseñas de productos.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje principal | Python 3.11 |
| Procesamiento NLP | NLTK, spaCy |
| Machine Learning | scikit-learn |
| Vectorización | TF-IDF |
| Modelo principal | Regresión logística |
| Backend | FastAPI |
| Frontend | React + TypeScript |
| Formato de datos | CSV |
| Serialización | Joblib |
| Pruebas | Pytest |

## Arquitectura del proyecto

```text
proyecto-integrador/
├── data/
│   ├── reviews.csv
│   └── processed.csv
├── notebooks/
│   └── exploracion.ipynb
├── src/
│   ├── nlp/
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   └── models/
│       ├── __init__.py
│       ├── train.py
│       └── evaluate.py
├── api/
│   ├── main.py
│   └── schemas.py
├── frontend/
├── tests/
│   ├── test_nlp.py
│   └── test_api.py
├── models/
│   ├── pipeline.joblib
│   └── metrics.json
├── docs/
│   └── informe.md
├── requirements.txt
├── README.md
└── CONTRIBUCIONES.md
```

## Pipeline de NLP

El procesamiento de texto contempla las siguientes etapas:

1. **Normalización:** conversión a minúsculas y tratamiento de tildes, puntuación, números, URLs y emojis.
2. **Tokenización:** separación del texto en palabras o tokens.
3. **Stop words:** eliminación de palabras frecuentes conservando negaciones relevantes para el sentimiento.
4. **Stemming:** reducción de palabras a sus raíces.
5. **Lematización:** conversión de palabras a su forma base.
6. **N-gramas:** comparación de unigramas con unigramas y bigramas.
7. **TF-IDF:** representación numérica de las reseñas.

Se compararán stemming y lematización para seleccionar la estrategia que produzca mejores resultados.

## Modelo de Machine Learning

Se utilizará inicialmente **Logistic Regression** como clasificador multiclase para predecir puntuaciones de 1 a 5.

El rendimiento se comparará contra un modelo baseline, utilizando métricas como:

- Accuracy.
- Precision.
- Recall.
- Macro F1-score.
- Mean Absolute Error (MAE).
- Matriz de confusión.

Se empleará validación cruzada para el ajuste de hiperparámetros y un conjunto de prueba independiente para la evaluación final.

## Dataset

El conjunto de datos contendrá reseñas de productos en español y su calificación real.

Columnas mínimas:

| Columna | Descripción |
|---|---|
| `review_text` | Texto de la reseña |
| `rating` | Puntuación real del 1 al 5 |

Se buscará utilizar un conjunto inicial de aproximadamente 10.000 reseñas, procurando una representación adecuada de las cinco categorías.

La fuente definitiva, licencia, fecha de obtención y análisis exploratorio se documentarán antes del entrenamiento.

## Instalación

### Requisitos previos

- Python 3.11.
- Node.js y npm para el frontend.
- Git.

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto-integrador
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

Activación en Windows:

```bash
.venv\Scripts\activate
```

Activación en Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Descargar el modelo de spaCy para español

```bash
python -m spacy download es_core_news_sm
```

### 5. Entrenar el modelo

Cuando los scripts y el dataset estén implementados:

```bash
python -m src.models.train
```

Este proceso deberá generar los siguientes artefactos:

- `models/pipeline.joblib`
- `models/metrics.json`

### 6. Iniciar FastAPI

```bash
uvicorn api.main:app --reload
```

Documentación de la API:

`http://localhost:8000/docs`

### 7. Iniciar React

```bash
cd frontend
npm install
npm run dev
```

## Endpoints previstos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio y modelo |
| POST | `/predict` | Predicción de 1 a 5 estrellas |
| POST | `/preprocess` | Visualización del procesamiento NLP |
| GET | `/metrics` | Métricas del clasificador |

## Pruebas

```bash
python -m pytest tests/ api/tests/
```

Los archivos de pruebas se agregarán conforme avance la implementación. Los comandos de ejecución deberán verificarse antes de la entrega.

## Estado del proyecto

**Estado inicial: planificación y configuración.**

Pendientes:

- Selección y validación del dataset.
- Implementación del pipeline NLP.
- Entrenamiento y comparación de experimentos.
- Evaluación y serialización del modelo.
- Integración con FastAPI.
- Desarrollo del frontend React.
- Pruebas y documentación final.

## Equipo y contribuciones

Las responsabilidades individuales se documentarán en `CONTRIBUCIONES.md` y deberán coincidir con el historial real de commits.

## Integridad académica

El proyecto seguirá las normas de atribución de librerías, datasets y recursos externos. Se documentará el uso de asistentes de inteligencia artificial y cada integrante deberá comprender, explicar y modificar sus aportes.