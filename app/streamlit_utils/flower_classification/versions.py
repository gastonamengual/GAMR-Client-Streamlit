from app.flower_classification import FlowerService


def get_classifier_versions(
    flower_service: FlowerService, classifier: str
) -> list[str]:
    classifier_versions = [""]
    return classifier_versions + flower_service.get_classifier_versions(
        classifier=classifier
    )
