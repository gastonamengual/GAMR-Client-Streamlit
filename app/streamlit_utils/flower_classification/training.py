import streamlit as st

from app.api_client.api_client import API_Client
from app.flower_classification import FlowerService

from .classifiers import get_classifiers
from .read_csv_data import read_csv_to_data


def training_tab(backend_service_url: str) -> None:
    api_client = API_Client(base_url=backend_service_url)
    api_client.authenticate()

    flower_service = FlowerService(api_client=api_client)

    new_classifier = st.text_input("Enter a new classifier name to train:", "")

    classifiers = get_classifiers(flower_service=flower_service)
    disable_selectbox = bool(new_classifier)
    classifier = st.selectbox(
        "Or select an existing Flower Classifier",
        classifiers,
        disabled=disable_selectbox,
    )

    classifier_to_train = new_classifier or classifier

    st.markdown(f"### Training: {classifier_to_train}")

    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
    if not uploaded_file:
        return

    data = read_csv_to_data(uploaded_file)

    if not st.button(f"Train {classifier}!"):
        return

    flower_payload = flower_service.train_classifier(
        classifier=classifier_to_train,
        data=data,
    )
    st.write(
        f"New version trained: {flower_payload.model_name} - v{flower_payload.model_version}"  # noqa: E501
    )
