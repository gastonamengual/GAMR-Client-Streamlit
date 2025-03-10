from dataclasses import asdict, dataclass

import requests  # type: ignore

from app.api_client.error import TokenNotObtainedError
from app.flower_classification import (
    FLOWER_CLASSIFICATION_MAPPING,
    Dataset,
    Flower,
    FlowerPayload,
    FlowerPredictionNotObtained,
    ModelsNotObtained,
    VersionsNotObtained,
)
from app.object_recognition import DetectionNotObtained, ImagePayload

from ..utils import get_token


@dataclass
class API_Client:
    username: str
    base_url: str

    @property
    def token(self) -> str:
        return get_token()

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def authenticate(self) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/token", json={"username": self.username}
            )

            if not response.ok:
                raise TokenNotObtainedError(
                    f"ERROR {response.status_code} - Token not obtained: {response.json()}"
                )
            token = response.json().get("token")

            return token

        except Exception as ex:
            raise TokenNotObtainedError(f"Token request failed: {ex}")

    def detect_objects(self, image_payload: ImagePayload) -> bytes:
        payload = asdict(image_payload)
        try:
            response = requests.post(
                f"{self.base_url}/detect_objects",
                headers=self.get_headers(),
                json=payload,
            )

            if not response.ok:
                raise DetectionNotObtained(
                    f"ERROR {response.status_code} - Image could not be processed: {response.json()}"
                )
            detected_image = response.content

            return detected_image

        except Exception as e:
            raise DetectionNotObtained(f"Detection request failed: {e}")

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
        try:
            response = requests.post(
                f"{self.base_url}/flower/specie/classify",
                headers=self.get_headers(),
                json=flower_payload.model_dump(),
            )
            if not response.ok:
                raise FlowerPredictionNotObtained(
                    f"ERROR {response.status_code} - Image could not be processed: {response.json()}"
                )
        except Exception as e:
            raise FlowerPredictionNotObtained(f"Detection request failed: {e}")

        predicted_flower_payload = FlowerPayload(**response.json())
        print(predicted_flower_payload)
        flower.classification = FLOWER_CLASSIFICATION_MAPPING[
            predicted_flower_payload.data.y[0]  # type: ignore
        ]
        return flower

    def train_classifier(self, classifier: str, data: Dataset) -> FlowerPayload:
        flower_payload = FlowerPayload(
            data=data,
            model_name=classifier,
        )
        try:
            response = requests.post(
                f"{self.base_url}/flower/specie/train",
                headers=self.get_headers(),
                json=flower_payload.model_dump(),
            )
            if not response.ok:
                raise FlowerPredictionNotObtained(
                    f"ERROR {response.status_code} - Image could not be processed: {response.json()}"
                )
            return FlowerPayload(**response.json())

        except Exception as e:
            raise FlowerPredictionNotObtained(f"Detection request failed: {e}")

    def get_classifier(self) -> list[str]:
        try:
            response = requests.get(
                f"{self.base_url}/flower/specie/classifiers", headers=self.get_headers()
            )
            if not response.ok:
                raise ModelsNotObtained(
                    f"ERROR {response.status_code} - Models not obtained: {response.json()}"
                )
            models = response.json()["models"]
            return models
        except Exception as e:
            raise ModelsNotObtained(f"Detection request failed: {e}")

    def get_classifier_versions(self, classifier: str) -> list[str]:
        try:
            response = requests.get(
                f"{self.base_url}/flower/specie/{classifier}/versions",
                headers=self.get_headers(),
            )
            if not response.ok:
                raise VersionsNotObtained(
                    f"ERROR {response.status_code} - Versions not obtained: {response.json()}"
                )
            models = response.json()["versions"]
            return models
        except Exception as e:
            raise VersionsNotObtained(f"Detection request failed: {e}")
