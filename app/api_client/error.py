from dataclasses import dataclass

from app.streamlit_utils import stop_execution


@dataclass
class BaseCustomException(Exception):
    message: str = ""

    def __post_init__(self) -> None:
        stop_execution(self.message)


class TokenNotObtainedError(BaseCustomException):
    pass


class PredictionNotObtained(BaseCustomException):
    pass
