from pydantic import BaseModel

from .dataset import Dataset


class FlowerPayload(BaseModel):
    data: Dataset | None
    model_name: str
    model_version: str | None = ""
