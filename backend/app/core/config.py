from pathlib import Path

# parents[3] sube 3 niveles: core -> app -> backend -> raíz del repositorio.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "models" / "pipeline.joblib"