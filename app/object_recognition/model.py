from dataclasses import dataclass


@dataclass
class ImagePayload:
    filename: str
    image_bytes: str
    model_service: str
