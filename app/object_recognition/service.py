from dataclasses import asdict, dataclass

from app.api_client.api_client import API_Client
from app.object_recognition import DetectionNotObtained, ImagePayload


@dataclass
class ObjectDetectionService:
    api_client: API_Client
    detect_path: str = "detect_objects"

    def detect_objects(self, image_payload: ImagePayload) -> bytes:
        response = self.api_client.perform_post_request(
            json_content=asdict(image_payload), path=self.detect_path
        )

        if not response.ok:
            raise DetectionNotObtained(
                f"ERROR {response.status_code} - Image could not be processed: {response.json()}"
            )
        detected_image = response.content

        return detected_image
