from typing import Literal
from pydantic import BaseModel

class PreprocessResponse(BaseModel):
    """
     como ve el pipeline de NLP el texto de una reseña, paso a paso
    """
    original_text: str
    normalized_text: str
    tokens: list[str]
     # Tokens sin stop words (las negaciones como "no" se conservan)
    filtered_tokens: list[str]
    # Metodo con el que fue entrenado el modelo
    morphological_method: Literal["stemming", "lemmatization", "none"]
    # Raices (stemming) o lemas (lemmatization) de filtered_tokens
    morphological_tokens: list[str]
    # Texto final que recibe el vectorizador TF-IDF del modelo
    processed_text: str