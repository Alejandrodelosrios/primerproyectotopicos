from fastapi import FastAPI
from app.routers.health import router as health_router

API_V1_PREFIX = "/api/v1"

app = FastAPI(title="reseña de productos",
              description= """API que consume el modelo de NLP 
                        para estimar la puntuación de una reseña.""",
             )

app.include_router(health_router, prefix=API_V1_PREFIX)