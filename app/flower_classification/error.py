from app.api_client.error import BaseCustomException


class FlowerPredictionNotObtained(BaseCustomException):
    pass


class ModelsNotObtained(BaseCustomException):
    pass


class VersionsNotObtained(BaseCustomException):
    pass
