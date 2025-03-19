from app.flower_classification import FlowerService


def get_classifiers(flower_service: FlowerService) -> list[str]:
    models = [""]
    return models + flower_service.get_classifier()
