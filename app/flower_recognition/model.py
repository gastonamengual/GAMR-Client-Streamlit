from dataclasses import dataclass, field


from typing import Optional
from uuid import uuid4


@dataclass
class Dataset:
    X: list[list[float]]
    y: Optional[list[int]] = None


@dataclass
class FlowerPayload:
    data: Dataset
    model_name: str
    model_version: Optional[str] = ""
    experiment_name: Optional[str] = field(
        default_factory=lambda: f"experiment-{uuid4()}"
    )
