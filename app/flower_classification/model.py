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


FLOWER_CLASSIFICATION_MAPPING = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
IMAGE_FLOWER_MAPPING = {
    "Setosa": "./images/setosa.jpg",
    "Versicolor": "./images/versicolor.jpg",
    "Virginica": "./images/virginica.jpg",
}


class FlowerPayload(BaseModel):
    data: Dataset
    model_name: str
    model_version: str | None = ""
