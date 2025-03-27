from pydantic import BaseModel

from app.flower_classification.model.flower_type import FlowerType


class Flower(BaseModel):
    sepal_length: float
    petal_length: float
    sepal_width: float
    petal_width: float
    classification: FlowerType | None = None
