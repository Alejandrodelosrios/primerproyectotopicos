from fastapi import APIRouter
from app.schemas.preprocess import PreprocessResponse
from app.schemas.review import ReviewRequest
from app.services.nlp_service import preprocess_text

router = APIRouter(tags=["NLP"])

@router.post("/preprocess", response_model=PreprocessResponse,
             summary="Mostrar el preprocesamiento NLP de una reseña"
            )
def preprocess(request: ReviewRequest):
    """
     Devuelve el texto normalizado y sus tokens
     no usa el modelo de ML, asi que funciona aunque el modelo no
     este cargado
    """
    return PreprocessResponse(**preprocess_text(request.text))