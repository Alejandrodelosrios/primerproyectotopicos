from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints

MIN_TEXT_LENGTH = 3
MAX_TEXT_LENGTH = 5000

# strip_whitespace recorta los espacios "antes" de medir el largo
# asi  "  ab  " se rechaza (queda de 2 caracteres) y " " tambien
ReviewText = Annotated[str,
                       StringConstraints(
                           strip_whitespace=True,
                           min_length=MIN_TEXT_LENGTH,
                           max_length=MAX_TEXT_LENGTH
                        ),
                      ]

class ReviewRequest(BaseModel):
    """
     Entrada comun de los endpoints: el texto de una reseña
    """
    text: ReviewText

    model_config = ConfigDict(
        json_schema_extra={"example": {"text": "No me GUSTO la bateria"}}
        )