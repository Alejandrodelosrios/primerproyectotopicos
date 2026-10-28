from src.nlp.preprocessing import normalize_text,tokenize_text

def preprocess_text(text: str) -> dict:
    """
     Aplica el preprocesamiento del equipo de NLP y devuelve cada 
     paso
     Usa las mismas funciones que el entrenamiento, asi lo que se 
     muestra es lo que recibe el modelo tokenize_text normaliza
     internamente, por eso se le pasa el texto original
    """
    return {
        "original_text": text,
        "normalized_text": normalize_text(text),
        "tokens": tokenize_text(text)
    }