import streamlit as st

from app.api_client.api_client import API_Client
from app.flower_classification.model import IMAGE_FLOWER_MAPPING, Flower
from app.flower_classification.service import FlowerService


def get_features() -> tuple[float, float, float, float]:
    st.write("Enter your flower features")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        sepal_length = st.slider(
            "Sepal Length", min_value=4.0, max_value=8.0, value=5.0
        )
    with col2:
        sepal_width = st.slider("Sepal Width", min_value=2.0, max_value=5.0, value=3.0)
    with col3:
        petal_length = st.slider(
            "Petal Length", min_value=1.0, max_value=7.0, value=4.0
        )
    with col4:
        petal_width = st.slider("Petal Width", min_value=0.1, max_value=2.5, value=1.5)

    return sepal_length, sepal_width, petal_length, petal_width


def classification_tab(backend_service_url: str) -> None:
    api_client = API_Client(base_url=backend_service_url)

    flower_service = FlowerService(api_client=api_client)
    classifiers = flower_service.get_classifiers()
    if not classifiers:
        st.error("There are no trained classifiers")
        return

    classifier = st.selectbox("Select Flower Classifier", ["", *classifiers])

    if not classifier:
        return

    classifier_versions = flower_service.get_classifier_versions(classifier=classifier)
    classifier_version = st.selectbox(
        "Select Classifier Version", ["", *classifier_versions]
    )
    if not classifier_version:
        return

    sepal_length, sepal_width, petal_length, petal_width = get_features()

    flower = Flower(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )

    if not st.button("Predict Flower!"):
        return

    flower = flower_service.classify_flower(
        flower=flower,
        classifier=classifier,
        classifier_version=str(classifier_version),
    )
    image_path = IMAGE_FLOWER_MAPPING[flower.classification]  # type: ignore
    st.write(f"Your flower is an Iris {flower.classification.value}")  # type: ignore
    st.image(image_path, width=400)
