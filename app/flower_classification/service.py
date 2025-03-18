from dataclasses import dataclass

from app.flower_classification import (
    FLOWER_CLASSIFICATION_MAPPING,
    Dataset,
    Flower,
    FlowerPayload,
    FlowerPredictionNotObtained,
    ModelsNotObtained,
    VersionsNotObtained,
)

from ..api_client.api_client import API_Client


@dataclass
class FlowerService:
    api_client: API_Client
    classify_path: str = "flower/specie/classify"
    train_path: str = "flower/specie/train"
    classifiers_path: str = "flower/specie/classifiers"

    def classify_flower(
        self, classifier: str, classifier_version: str, flower: Flower
    ) -> Flower:
        dataset = Dataset(
            X=[
                [
                    flower.sepal_length,
                    flower.sepal_width,
                    flower.petal_length,
                    flower.petal_width,
                ]
            ]
        )
        flower_payload = FlowerPayload(
            data=dataset,
            model_name=classifier,
            model_version=str(classifier_version),
        )
        response = self.api_client.perform_post_request(
            json_content=flower_payload.model_dump(), path=self.classify_path
        )
        if not response.ok:
            raise FlowerPredictionNotObtained(
                f"ERROR {response.status_code} - Prediction could not be processed: {response.json()}"
            )

        predicted_flower_payload = FlowerPayload(**response.json())
        flower.classification = FLOWER_CLASSIFICATION_MAPPING[
            predicted_flower_payload.data.y[0]  # type: ignore
        ]
        return flower

    def train_classifier(self, classifier: str, data: Dataset) -> FlowerPayload:
        flower_payload = FlowerPayload(
            data=data,
            model_name=classifier,
        )
        response = self.api_client.perform_post_request(
            json_content=flower_payload.model_dump(), path=self.train_path
        )
        if not response.ok:
            raise FlowerPredictionNotObtained(
                f"ERROR {response.status_code} - Training could not be processed: {response.json()}"
            )

        return FlowerPayload(**response.json())

    def get_classifier(self) -> list[str]:
        response = self.api_client.perform_get_request(path=self.classifiers_path)
        if not response.ok:
            raise ModelsNotObtained(
                f"ERROR {response.status_code} - Models not obtained: {response.json()}"
            )
        models = response.json()["models"]
        return models

    def get_classifier_versions(self, classifier: str) -> list[str]:
        response = self.api_client.perform_get_request(
            path=f"flower/specie/{classifier}/versions"
        )
        if not response.ok:
            raise VersionsNotObtained(
                f"ERROR {response.status_code} - Versions not obtained: {response.json()}"
            )
        versions = response.json()["versions"]
        return versions
