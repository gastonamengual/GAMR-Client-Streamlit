from app.flower_classification import FlowerService


def get_classifier_versions(flower_service: FlowerService, classifier: str):
    classifier_versions = [""]
    classifier_versions = classifier_versions + flower_service.get_classifier_versions(
        classifier=classifier
    )
    return classifier_versions
