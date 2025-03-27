from pydantic import BaseModel


class Dataset(BaseModel):
    X: list[list[float]]
    y: list[int] | None = None
