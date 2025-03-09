from dataclasses import asdict, dataclass

import requests  # type: ignore

from app.object_detection import DetectionNotObtained
from app.flower_recognition import (
    FlowerPredictionNotObtained,
    ModelsNotObtained,
    VersionsNotObtained,
)
from app.api_client.error import TokenNotObtainedError

from app.flower_recognition import FlowerPayload
from app.object_detection import ImagePayload

from ..utils import get_token


@dataclass
class API_Client:
    username: str
    base_url: str

    @property
    def token(self) -> str:
        return get_token()

    def get_headers(self):
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

    def predict_flower_model(self, flower_payload: FlowerPayload):
        payload = asdict(flower_payload)
        try:
            response = requests.post(
                f"{self.base_url}/predict_flower",
                headers=self.get_headers(),
                json=payload,
            )
            if not response.ok:
                raise FlowerPredictionNotObtained(
                    f"ERROR {response.status_code} - Image could not be processed: {response.json()}"
                )
            predicted_flower = response.json()["prediction"]
            return predicted_flower
        except Exception as e:
            raise FlowerPredictionNotObtained(f"Detection request failed: {e}")

    def get_models(self):
        try:
            response = requests.get(
                f"{self.base_url}/models", headers=self.get_headers()
            )
            if not response.ok:
                raise ModelsNotObtained(
                    f"ERROR {response.status_code} - Models not obtained: {response.json()}"
                )
            models = response.json()["models"]
            return models
        except Exception as e:
            raise ModelsNotObtained(f"Detection request failed: {e}")

    def get_model_versions(self, model_name: str):
        try:
            response = requests.get(
                f"{self.base_url}/{model_name}/model_versions",
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
