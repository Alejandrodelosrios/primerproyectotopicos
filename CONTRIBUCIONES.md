# CONTRIBUCIONES.md

## Proyecto Integrador – Análisis de Reseñas con NLP y Machine Learning

## Repositorio: Alejandrodelosrios/primerproyectotopicos
## Registro de commits

## Contribuciones — MurilloDiana

## Contribuciones de MurilloDiana — NLP y Machine Learning
## Rama examinada: nlp/config


### Historial de commits

| Fecha (UTC) | Commit | Mensaje registrado | Aporte identificado |
|---|---|---|---|
| 26/10/2026 | [`456371b`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/456371bbc19a) | `arquitectura` | Estructura inicial y archivos base de NLP, entrenamiento, evaluación, artefactos y pruebas. |
| 26/10/2026 | [`46f3cc6`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/46f3cc60ba6a) | `documentacion` | Creación de `README.md`, `CONTRIBUCIONES.md` y `requirements.txt` para documentar el proyecto y sus dependencias. |
| 26/10/2026 | [`2fc9eb8`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/2fc9eb800303) | `feat(nlp): implement spanish text normalization and tokenization` | Implementación de normalización y tokenización de textos en español, con pruebas automatizadas en `tests/test_nlp.py`. |
| 28/10/2026 | [`67d922c`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/67d922c567e1) | `feat(ml): implement TF-IDF and logistic regression pipeline` | Modificaciones al preprocesamiento, pruebas de morfología, exportaciones NLP y configuración de Pytest. El contenido real del commit difiere parcialmente de su mensaje. |
| 29/10/2026 | [`5ab058e`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/5ab058e96cb0) | `Merge branch 'data' ... into nlp/config` | Integración de la rama `data` con `nlp/config`. No se atribuye como desarrollo propio el código procedente de la rama integrada. |
| 29/10/2026 | [`c310fef`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/c310fef5dac5) | `feat(ml): integrate NLP pipeline and validated training results` | Integración del transformador NLP, TF-IDF, regresión logística, entrenamiento con divisiones externas, evaluación, métricas y pruebas automatizadas. |
| 30/10/2026 | [`24e3520`](https://github.com/Alejandrodelosrios/primerproyectotopicos/commit/24e3520c2791) | `feat(ml): validate NLP models and document training results` | Implementación de experimentos NLP/ML, pruebas automatizadas y exportación de resultados en `models/final/` y `models/quick/`. |

### Resumen de contribuciones

Las contribuciones del usuario `MurilloDiana` abarcan:

- **Arquitectura:** estructura inicial de los módulos NLP y Machine Learning.
- **Documentación:** archivos de configuración, dependencias y contribuciones.
- **Procesamiento NLP:** normalización, tokenización y procesamiento morfológico de textos en español.
- **Machine Learning:** integración de TF-IDF y regresión logística para clasificar reseñas de 1 a 5 estrellas.
- **Entrenamiento:** utilización de conjuntos externos de entrenamiento y prueba.
- **Evaluación:** generación de métricas y comparación de configuraciones NLP/ML.
- **Calidad:** implementación de pruebas automatizadas.
- **Integración:** incorporación de la rama `data` al flujo de trabajo NLP/ML.

### Trazabilidad

Las contribuciones se encuentran respaldadas por los commits del usuario `MurilloDiana` en el repositorio.

La autoría de los cambios provenientes de otras ramas se mantiene diferenciada, respetando el historial de Git.

### Detalle funcional de los aportes
1. Base del proyecto y documentación
Se establecieron archivos para el procesamiento NLP (src/nlp/), entrenamiento y evaluación (src/models/), pruebas y documentación. El propósito fue habilitar una organización reproducible del proyecto y facilitar que otros integrantes integraran API y frontend.

Evidencia: commits 456371b y 46f3cc6.
2. Normalización y tokenización de reseñas
Se incorporó procesamiento de texto en español y pruebas unitarias para validar casos de entrada. La normalización y tokenización son las etapas de preparación del contenido textual antes de convertirlo a características numéricas para los modelos.

Evidencia: 2fc9eb8.
3. Procesamiento morfológico y pruebas
Se ampliaron las funciones NLP y las pruebas de morfología, dentro del flujo que permite trabajar con stop words, stemming y lematización. Estas alternativas permiten comparar distintas representaciones del texto en español.

Evidencia: 67d922c. Aunque el mensaje menciona TF-IDF y regresión logística, su listado de archivos modificados corresponde principalmente a NLP, pruebas y configuración.
4. Integración del modelo y entrenamiento
Se incorporaron src/nlp/transformer.py, src/models/pipeline.py, src/models/train.py y src/models/evaluate.py, junto con pruebas para el pipeline y los conjuntos externos de datos. El objetivo fue mantener un mismo flujo de preprocesamiento y clasificación, reutilizable desde el backend sin duplicar la lógica de NLP.

Evidencia: c310fef.
5. Evaluación experimental
Se agregó src/models/experiments.py y tests/test_experiments.py, así como archivos de salida de experimentos, métricas y ejemplos de errores. Esto permite documentar la selección de configuraciones y comparar el desempeño del modelo.

Evidencia: 24e3520.
Alcance de la autoría
- Este documento solo enumera commits identificados con el usuario GitHub MurilloDiana.
- El commit de merge de la rama data se identifica como actividad de integración, sin atribuir a MurilloDiana la creación original de los scripts de otro integrante.
- Los archivos de caché y artefactos generados presentes en algunos commits no se consideran, por sí solos, evidencia de desarrollo funcional.
- Los resultados de métricas deben interpretarse a partir de los archivos y las ejecuciones correspondientes; no se atribuyen mejoras de rendimiento que no estén verificadas.
Verificación
Historial consultado: commits de la rama nlp/config. Cada identificador en la tabla enlaza a su commit para revisar archivos y cambios.


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


### Ajuste de dependencias e integración del entorno Python
Identifiqué conflictos de versiones que impedían instalar las
dependencias necesarias para ejecutar el sistema.

#### Contribuciones realizadas
- Revisión de las dependencias de la raíz y del backend.
- Centralización de las dependencias Python en requirements.txt.
- Retiro de las restricciones incompatibles de Starlette y
  pydantic-core, permitiendo que FastAPI y Pydantic seleccionen
  sus versiones correspondientes.
  un poco la comprensión y el mantenimiento del entorno.

#### Archivos modificados
- requirements.txt
- backend/requirements.txt (eliminado)

#### Evidencia en Git
- Rama: feature/dependencies-alignment.
- Commit: completar después de crearlo.