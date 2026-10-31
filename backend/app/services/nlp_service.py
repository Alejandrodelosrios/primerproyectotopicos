from src.nlp.preprocessing import (normalize_text,tokenize_text,
    lemmatize_tokens,remove_stopwords,stem_tokens)

from app.services.model_service import DEFAULT_NLP_METHOD

def preprocess_text(text: str, method:str = DEFAULT_NLP_METHOD) -> dict:
    """
     Aplica el preprocesamiento del equipo de NLP y devuelve cada 
     paso
     Usa las mismas funciones y el mismo orden que SpanishReviewTransformer
     el modelo: normalizar -> tokenizar -> quitar stop words -> raiz/lema.
     tokenize_text normaliza internamente, por eso se le pasa el texto original.
     method puede ser "stemming", "lemmatization" o none. 
    """
    tokens = tokenize_text(text)
    filtered_tokens = remove_stopwords(tokens)

    if method == "stemming":
        morphological_tokens = stem_tokens(filtered_tokens)
    elif method == "lemmatization":
        morphological_tokens = lemmatize_tokens(filtered_tokens)
    else:
        morphological_tokens = filtered_tokens

    return {
        "original_text": text,
        "normalized_text": normalize_text(text),
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "morphological_method": method,
        "morphological_tokens": morphological_tokens,
        "processed_text": " ".join(morphological_tokens)
    }