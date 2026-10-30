from pathlib import Path

# parents[3] sube 3 niveles: core -> app -> backend -> raíz del repositorio.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODELS_DIR = PROJECT_ROOT / "models"

# Modelo final Si todavia no esta en el
# repositorio, se usa el modelo anterior para no dejar la API sin modelo.
_FINAL_MODEL = MODELS_DIR / "models" / "pipeline.joblib"
_LEGACY_MODEL = MODELS_DIR / "pipeline.joblib"

if _FINAL_MODEL.exists():
    MODEL_PATH, MODEL_VERSION = _FINAL_MODEL, "final"
else:
    MODEL_PATH, MODEL_VERSION = _LEGACY_MODEL, "legacy"