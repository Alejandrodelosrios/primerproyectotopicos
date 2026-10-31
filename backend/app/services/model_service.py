import logging
import re
from pathlib import Path
import joblib
from app.core.config import MODEL_PATH, MODEL_VERSION,PROJECT_ROOT

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

#metodo morfologico que se muestra cuando no hay modelo cargado.
DEFAULT_NLP_METHOD = "stemming"

def get_nlp_method()-> str:
    """
     Devuelve el metodo morfologico ("stemming", "lemmatization" o "none")
    con el que fue entrenado el modelo cargado, para mostrar el mismo
    proceso que usa el modelo. Si no hay modelo, usa el valor por defecto
    """
    if _model is None:
        return DEFAULT_NLP_METHOD
    return _model.named_steps["nlp"].method

def _to_snake_case(name:str)->str:
    """
    LogisticRegression -> logistic_regression
    """
    return re.sub(r"(?<!^)(?=[A-Z])","_", name).lower()

def predict(text:str)-> dict:
    """
     Predice la puntuacion (1 a 5) de una reseña con el pipeline cargado
     el pipeline ya incluye el NLP, por eso recibe el texto crudo.
     usa predict() para la puntuacion y predict_proba() para las probabilidades 
    """
    if _model is None:
        raise RuntimeError("El modelo no esta cargado")
    
    classes = [int(c) for c in _model.classes_]
    stars = int(_model.predict([text])[0])
    probs = _model.predict_proba([text])[0]

    probabilities = {str(c): round(float(p),4) for c,p in zip(classes,probs)}
    return {
       "stars": stars,
        "confidence": probabilities[str(stars)],
        "probabilities": probabilities,
        "model_name": _to_snake_case(type(_model.named_steps["classifier"]).__name__),
        "method": _model.named_steps["nlp"].method, 
    }
def get_model_info() -> dict:
    """Describe el modelo cargado, leyendo su configuracion real del pipeline."""
    if _model is None:
        raise RuntimeError("El modelo no esta cargado")
    
    tfidf = _model.named_steps["tfidf"]
    return {
        "model_name": type(_model.named_steps["classifier"]).__name__,
        "model_version": MODEL_VERSION,
        "nlp_method": _model.named_steps["nlp"].method,
        "vectorizer": type(tfidf).__name__,
        "ngram_range": list(tfidf.ngram_range),
        "classes": [int(c) for c in _model.classes_],
        # Ruta relativa al repositorio: no expone carpetas de la maquina
        "artifact_path": MODEL_PATH.relative_to(PROJECT_ROOT).as_posix(),
    }