# Backend: API de reseñas de productos

API en FastAPI que consume el pipeline de NLP/ML para estimar la puntuación (1 a 5 estrellas) de una reseña.

## Cómo correrla

Desde la **raíz del proyecto** (no desde `backend/`):

```bash
python -m uvicorn app.main:app --app-dir backend --reload
```

La documentación interactiva está en `http://127.0.0.1:8000/docs` (Swagger) y `/redoc`.

## Cómo probarla

```bash
cd backend
pytest -v
```

Deben pasar todas las pruebas. Es normal ver avisos amarillos `InconsistentVersionWarning`: el modelo se entrenó con scikit-learn 1.5.2 y se está usando una versión más nueva. Funciona igual y desaparece al reentrenar.

## Estado de los endpoints

| Método | Ruta | Para qué sirve | Estado |
|---|---|---|---|
| GET | `/api/v1/health` | Estado de la API y del modelo | Listo |
| POST | `/api/v1/preprocess` | Muestra el NLP paso a paso | Listo |
| POST | `/api/v1/predict` | Predice las estrellas de una reseña | Listo |
| GET | `/api/v1/models/info` | Modelo activo y su configuración | Listo |
| GET | `/api/v1/models/metrics` | Resultados del entrenamiento | Listo |
| GET | `/api/v1/models/experiments` | Comparación de configuraciones | Listo |

## Estructura del código

```
backend/app/
├── main.py       Crea la app, carga el modelo al iniciar y registra los routers
├── core/         Configuración: rutas del modelo y de los resultados
├── routers/      Define las URLs y qué hacer con cada petición
├── schemas/      Define la forma de los datos de entrada y de salida
└── services/     Lógica real: cargar el modelo, predecir, leer resultados
```

El modelo se carga **una sola vez** al iniciar la API y se guarda en memoria. El pipeline incluye el NLP, por eso recibe el texto sin procesar.

## Qué modelo se carga

`core/config.py` busca primero `models/final/pipeline.joblib`. Si no existe, usa `models/pipeline.joblib`. La versión que se muestra en `/health` y `/models/info` depende de cuál se cargó:

| Archivo cargado | `model_version` |
|---|---|
| `models/final/pipeline.joblib` | `"final"` |
| `models/pipeline.joblib` | `"legacy"` |

## Ejemplos

### `GET /api/v1/health`

Respuesta 200:

```json
{ "status": "healthy", "model_loaded": true, "model_version": "legacy" }
```

Respuesta 503, si el modelo no cargó:

```json
{ "status": "degraded", "model_loaded": false, "model_version": null }
```

### `POST /api/v1/preprocess`

Petición:

```json
{ "text": "NO me GUSTÓ la batería" }
```

Respuesta 200:

```json
{
  "original_text": "NO me GUSTÓ la batería",
  "normalized_text": "no me gustó la batería",
  "tokens": ["no", "me", "gustó", "la", "batería"],
  "filtered_tokens": ["no", "gustó", "batería"],
  "morphological_method": "stemming",
  "morphological_tokens": ["no", "gust", "bat"],
  "processed_text": "no gust bat"
}
```

Las etapas, en orden: normalizar, tokenizar, quitar stop words, reducir a raíz (o lema) y unir. Las negaciones como "no" se conservan porque cambian el sentido de la reseña. `morphological_method` sale del modelo cargado, y `processed_text` es lo mismo que recibe el modelo. Este endpoint no usa el modelo para predecir, así que funciona aunque el modelo no esté cargado (en ese caso usa stemming).

### `POST /api/v1/predict`

Petición:

```json
{ "text": "Excelente producto, llegó rápido y funciona perfectamente." }
```

Respuesta 200:

```json
{
  "prediction": {
    "stars": 5,
    "confidence": 0.8915,
    "probabilities": { "1": 0.0026, "2": 0.0028, "3": 0.0126, "4": 0.0904, "5": 0.8915 }
  },
  "model": { "name": "logistic_regression", "method": "stemming" }
}
```

`confidence` es la probabilidad de la puntuación elegida. Las probabilidades suman aproximadamente 1.

Respuesta 503, si el modelo no cargó:

```json
{ "detail": "El modelo no esta disponible" }
```

### `GET /api/v1/models/info`

```json
{
  "model_name": "LogisticRegression",
  "model_version": "legacy",
  "nlp_method": "stemming",
  "vectorizer": "TfidfVectorizer",
  "ngram_range": [1, 2],
  "classes": [1, 2, 3, 4, 5],
  "artifact_path": "models/pipeline.joblib"
}
```

Los datos se leen del modelo cargado. La ruta es relativa al repositorio.

### `GET /api/v1/models/metrics`

Lee `models/final/metrics.json` (respuesta abreviada):

```json
{
  "selection_rule": "max CV macro_f1 on train only",
  "best_params": { "method": "stemming", "ngram_range": [1, 2], "C": 1.0 },
  "best_cv_macro_f1": 0.4487,
  "cv_folds": 3,
  "train_size": 15938,
  "test_size": 3984,
  "labels": [1, 2, 3, 4, 5],
  "baseline":   { "accuracy": 0.2005, "macro_f1": 0.0668, "mae": 1.9955, "confusion_matrix": [[...]] },
  "final_test": { "accuracy": 0.4526, "macro_f1": 0.4480, "mae": 0.7600, "confusion_matrix": [[...]] }
}
```

En la matriz de confusión las filas son la estrella real y las columnas la predicha, en el orden de `labels`. El `baseline` es una predicción trivial, para comparar.

### `GET /api/v1/models/experiments`

Lee `models/final/experiments.csv` (una fila por configuración, abreviado):

```json
{
  "experiments": [
    {
      "method": "stemming", "ngrams": "1-2", "C": 1.0,
      "cv_macro_f1_mean": 0.4487, "cv_macro_f1_std": 0.0094,
      "cv_accuracy_mean": 0.4538, "cv_mae_mean": 0.7571
    }
  ]
}
```

### Error de validación (422)

Si el texto está vacío o es demasiado corto o largo:

```json
{ "detail": [ { "type": "string_too_short", "loc": ["body", "text"], "msg": "..." } ] }
```

## Validación de entradas

Aplica a `/preprocess` y `/predict`.

| Regla | Valor |
|---|---|
| Largo mínimo del texto | 3 caracteres (después de recortar espacios) |
| Largo máximo del texto | 5000 caracteres |
| Campo ausente o tipo incorrecto | 422 |

## Códigos de respuesta

| Código | Cuándo |
|---|---|
| 200 | Petición correcta |
| 404 | `/models/metrics` o `/models/experiments`: faltan los archivos de resultados |
| 405 | Método HTTP no permitido |
| 422 | Entrada inválida |
| 503 | `/health`, `/predict` y `/models/info`: el modelo no está cargado. `/preprocess`: el modelo usa lematización y falta el modelo de spaCy |

## ¿Por qué FastAPI?

- Valida las entradas con Pydantic, lo que cubre los textos vacíos o demasiado largos.
- Genera la documentación (Swagger y ReDoc) a partir del código.
- Está en Python, igual que el modelo de ML, sin capa intermedia.
- Permite probar con `TestClient` y sustituir dependencias en los tests.

## Solución de problemas

| Mensaje | Causa y solución |
|---|---|
| `No module named 'app'` | Falta un `__init__.py` o está mal escrito (lleva dos guiones bajos a cada lado). |
| `No module named 'src'` | La API se ejecuta desde la raíz del repo y los tests desde `backend/`. |
| `No module named 'nltk'` (o `spacy`, `sklearn`) | Faltan dependencias. Instálalas en el entorno virtual activo. |
| `/health` responde 503 | El modelo no cargó: el archivo falta, está corrupto o no se puede leer. El motivo aparece en la consola. |
| `/models/metrics` responde 404 | Faltan `models/final/metrics.json` o `experiments.csv`. Se generan con `python -m src.models.experiments`. |
| `/preprocess` responde 503 | El modelo usa lematización y falta el modelo de spaCy: `python -m spacy download es_core_news_sm`. |
| `InconsistentVersionWarning` | Aviso, no error. Ver "Cómo probarla". |
| Error 500 | Revisa la consola de uvicorn, que muestra el detalle. |

## Pendiente de acordar con el equipo

- **`models/final/pipeline.joblib`:** no está en el repositorio (el `.gitignore` bloquea los `.joblib`). Hasta que se suba, la API usa `models/pipeline.joblib`. Pedir confirmación a la responsable del modelo de que es el mismo.
- **Requirements:** el `requirements.txt` de la raíz tiene versiones que no existen o no se instalan en Python 3.13, y el de `backend/` no incluye todas las librerías que se usan. Hay que unificarlos.
- **Versión de Python:** el README principal indica 3.11. La API se probó con 3.12 y 3.13.
- **CORS:** no está configurado. En desarrollo el frontend usa el proxy de Vite hacia `/api`. Si se llama a la API directamente desde el navegador, hay que agregarlo en `main.py`.