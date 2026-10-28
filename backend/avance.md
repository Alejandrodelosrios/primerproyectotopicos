## Estado de los endpoints

| Método | Ruta | Estado |
|---|---|---|
| GET | `/api/v1/health` | Listo |
| POST | `/api/v1/preprocess` | Listo |
| POST | `/api/v1/predict` | Pendiente |
| GET | `/api/v1/metrics` | Pendiente |

La documentación interactiva está en `/docs` (Swagger) y `/redoc`.

## Ejemplo: `POST /api/v1/preprocess`

Petición:

```json
{ "text": "NO me GUSTÓ la batería" }
```

Respuesta 200:

```json
{
  "original_text": "NO me GUSTÓ la batería",
  "normalized_text": "no me gustó la batería",
  "tokens": ["no", "me", "gustó", "la", "batería"]
}
```

Respuesta 422 (abreviada), si el texto está vacío:

```json
{ "detail": [ { "type": "string_too_short", "loc": ["body", "text"], "msg": "..." } ] }
```

## Validación de entradas

| Regla | Valor |
|---|---|
| Largo mínimo del texto | 3 caracteres (después de recortar espacios) |
| Largo máximo del texto | 5000 caracteres |
| Campo ausente o tipo incorrecto | 422 |

## Códigos de respuesta

| Código | Cuándo |
|---|---|
| 200 | Petición correcta |
| 405 | Método HTTP no permitido |
| 422 | Entrada inválida |
| 503 | `/health`: el modelo no está cargado |

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
| `/health` responde 503 | El modelo no cargó. Es normal mientras `models/pipeline.joblib` esté vacío. El motivo aparece en la consola. |
| Error 500 | Revisa la consola de uvicorn, que muestra el detalle. |

## Pendiente de acordar con el equipo

- Versión de Python (el README principal indica 3.11).
- Si los endpoints llevan el prefijo `/api/v1`.