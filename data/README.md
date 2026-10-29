# Datos del proyecto

Dataset de **reseñas en español con puntaje de 1 a 5** para estimar la puntuación a partir del texto.

> Esta información alimenta el informe técnico: origen, licencia, fecha, tamaño y distribución del dataset.

## Origen del dataset

| Campo                               | Valor                                                                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nombre                              | The Multilingual Amazon Reviews Corpus (MARC), reseñas de productos de Amazon en español                                                                                                |
| Fuente / enlace                     | Copia en Hugging Face: https://huggingface.co/datasets/SetFit/amazon_reviews_multi_es (archivo `train.jsonl`). Corpus original: https://docs.opendata.aws/amazon-reviews-ml/readme.html |
| Fecha de descarga                   | 28/10/2026                                                                                                                                                                              |
| Idioma                              | Español                                                                                                                                                                                 |
| Número de registros (crudo)         | 200.000 (archivo `train.jsonl`). Se trabaja con una muestra de 20.000: 4.000 por puntaje, elegida al azar con semilla 42                                                                |
| Número de registros (tras limpieza) | [completar con la salida de `python data/dividir_dataset.py data/raw/reviews.csv`]                                                                                                      |

## Columnas

| Columna                                        | Obligatoria  | ¿La trae la copia SetFit?            | Descripción                                                  |
| ---------------------------------------------- | ------------ | ------------------------------------ | ------------------------------------------------------------ |
| `review_text`                                  | Sí           | Sí (`text`)                          | Texto completo de la reseña                                  |
| `rating`                                       | Sí           | Sí (`label`, de 0 a 4; se le suma 1) | Puntaje original, entero de 1 a 5 (variable objetivo)        |
| `review_id`                                    | No           | Sí (`id`)                            | Identificador de la reseña                                   |
| `product_category`                             | Recomendable | **No**                               | Categoría del producto, para analizar el error por categoría |
| `product_id`, `nombre_producto`, `review_date` | No           | **No**                               | Útiles para duplicados y análisis temporal; no se inventan   |

Las columnas que la fuente no trae **no se rellenan ni se inventan**: se dejan fuera y se documenta aquí. El modelo solo necesita `review_text` y `rating`.

## Distribución de puntajes

Resultado de `python data/revisar_dataset.py data/raw/reviews.csv` sobre la muestra de 20.000 reseñas:

| Puntaje | Reseñas | %    |
| ------- | ------- | ---- |
| 1       | 4.000   | 20,0 |
| 2       | 4.000   | 20,0 |
| 3       | 4.000   | 20,0 |
| 4       | 4.000   | 20,0 |
| 5       | 4.000   | 20,0 |

- Valores faltantes: 0. Textos vacíos: 0. Puntajes inválidos: 0.
- Reseñas duplicadas (mismo texto y puntaje): 37. El script de división las elimina.
- Longitud de los textos: promedio 27,8 palabras, mediana 22, mínimo 2, máximo 458.
- Textos de menos de 3 palabras: 16. **No se eliminan**: son lenguaje real.
- Las clases están balanceadas porque el corpus original está balanceado y la muestra es estratificada. En reseñas reales suele haber muchas más de 5 estrellas, y se debe tener en cuenta al interpretar los resultados.

## Estructura de carpetas

```
data/
├── raw/                 # dato crudo tal como se descargó (no se modifica)
├── processed/           # train.csv y test.csv generados por dividir_dataset.py
├── descargar_dataset.py # baja el dataset y lo guarda en raw/reviews.csv
├── revisar_dataset.py   # revisión de calidad
├── dividir_dataset.py   # partición estratificada, semilla 42
└── README.md
```

## Cómo usar los scripts

```bash
pip install pandas scikit-learn huggingface_hub openpyxl   # openpyxl solo hace falta para leer .xlsx

# 0. Descargar el dataset (crea data/raw/reviews.csv)
python data/descargar_dataset.py

# 1. Revisar calidad del dato crudo
python data/revisar_dataset.py data/raw/reviews.csv

# 2. Dividir en entrenamiento y prueba (una sola vez)
python data/dividir_dataset.py data/raw/reviews.csv
```

## Reglas del grupo para los datos

- No se eliminan reseñas negativas, cortas ni con errores ortográficos: son lenguaje real.
- El desbalance de puntajes se trata sobre el conjunto de entrenamiento
