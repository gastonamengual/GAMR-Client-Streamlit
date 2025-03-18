from app.flower_classification import FlowerService


def get_classifiers(flower_service: FlowerService):
    models = [""]
    models = models + flower_service.get_classifier()
    return models
