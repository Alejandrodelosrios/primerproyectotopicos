# Aqui se guardara el modelo  una vez cargado
# mientras nadie lo cargue, vale None (es decir, "no hay modelo")
_model = None

def is_model_loaded() -> bool:
    """
    Indica si el modelo de ML esta disponible para hacer 
    predicciones.

    Devuelve True si ya hay un modelo guardado en memoria
    Devuelve False si no hay modelo guardado en memoria 
    """
    return _model is not None
