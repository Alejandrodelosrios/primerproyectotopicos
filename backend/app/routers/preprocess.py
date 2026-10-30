from fastapi import APIRouter, HTTPException, status
from app.schemas.preprocess import PreprocessResponse
from app.schemas.review import ReviewRequest
from app.services.model_service import get_nlp_method
from app.services.nlp_service import preprocess_text

router = APIRouter(tags=["NLP"])


@router.post("/preprocess", response_model=PreprocessResponse,
             summary="Mostrar el preprocesamiento NLP de una reseña",
             responses={503: {"description": "Falta el modelo de spaCy "
                                             "necesario para lematizar"}}
             )
def preprocess(request: ReviewRequest):
    """
     Devuelve cada etapa del NLP: texto normalizado, tokens, tokens sin
     stop words y raices o lemas, segun el metodo del modelo cargado.
     No usa el modelo para predecir, asi que funciona aunque el modelo
     no este cargado (en ese caso usa stemming por defecto)
    """
    try:
        return PreprocessResponse(
            **preprocess_text(request.text, method=get_nlp_method())
        )
    except RuntimeError as error:
        # Pasa si el modelo usa lematizacion y falta es_core_news_sm
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        )