import logging
from pathlib import Path
import joblib
from app.core.config import MODEL_PATH

logger = logging.getLogger(__name__)

# Aqui se guardara el modelo  una vez cargado
# mientras nadie lo cargue, vale None (es decir, "no hay modelo")
_model = None

def load_model(path:Path = MODEL_PATH)->None:
    """
     Carga el pipeline desde disco
     si falla (archivo ausente, vacio o corrupto), la app sigue 
     funcionando sin modelo y /health informara con "degraded"
    """
    global _model
    try:
        _model = joblib.load(path)
    except Exception:
        logger.exception("No se pudo cargar el modelo desde %s",path)
        _model = None

def is_model_loaded() -> bool:
    """
    Indica si el modelo de ML esta disponible para hacer 
    predicciones.

    Devuelve True si ya hay un modelo guardado en memoria
    Devuelve False si no hay modelo guardado en memoria 
    """
    return _model is not None
