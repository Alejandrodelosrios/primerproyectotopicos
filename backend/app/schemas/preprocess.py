from pydantic import BaseModel

class PreprocessResponse(BaseModel):
    """
     como ve el pipeline de NLP el texto de una reseña
    """
    original_text: str
    normalized_text: str
    tokens: list[str]