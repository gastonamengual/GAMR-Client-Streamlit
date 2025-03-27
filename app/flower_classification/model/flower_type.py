from enum import Enum
from pathlib import Path


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
    FlowerType.SETOSA: f"{Path.cwd()}/app/data/flower_images/setosa.jpg",
    FlowerType.VERSICOLOR: f"{Path.cwd()}/app/data/flower_images/versicolor.jpg",
    FlowerType.VIRGINICA: f"{Path.cwd()}/app/data/flower_images/virginica.jpg",
}
