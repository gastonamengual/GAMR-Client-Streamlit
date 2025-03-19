from enum import Enum

from pydantic import BaseModel


class Dataset(BaseModel):
    X: list[list[float]]
    y: list[int] | None = None


class Flower(BaseModel):
    sepal_length: float
    petal_length: float
    sepal_width: float
    petal_width: float
    classification: str | None = None


class FlowerPayload(BaseModel):
    data: Dataset
    model_name: str
    model_version: str | None = ""


class FlowerType(Enum):
    SETOSA = "Setosa"
    VERSICOLOR = "Versicolor"
    VIRGINICA = "Virginica"


FLOWER_CLASSIFICATION_MAPPING = {
    0: FlowerType.SETOSA,
    1: FlowerType.VERSICOLOR,
    2: FlowerType.VIRGINICA,
}

IMAGE_FLOWER_MAPPING = {
    FlowerType.SETOSA: "./images/setosa.jpg",
    FlowerType.VERSICOLOR: "./images/versicolor.jpg",
    FlowerType.VIRGINICA: "./images/virginica.jpg",
}
