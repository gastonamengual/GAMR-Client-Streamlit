import streamlit as st

from app.api_client.api_client import API_Client
from app.flower_classification import FlowerService
from app.streamlit_utils.utils import stop_execution

from .read_csv_data import REQUIRED_COLUMNS, read_csv_to_data


def training_tab(backend_service_url: str) -> None:
    api_client = API_Client(base_url=backend_service_url)

    flower_service = FlowerService(api_client=api_client)

    classifiers = flower_service.get_classifiers()
    if not classifiers:
        st.error("There are no trained classifiers")
    existing_classifier = None
    if classifiers:
        existing_classifier = st.selectbox(
            "Select an existing Flower Classifier",
            ["", *classifiers],
        )

    disable_selectbox = bool(existing_classifier)
    new_classifier = st.text_input(
        "Or enter a new classifier name to train:", "", disabled=disable_selectbox
    )
    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
    if not uploaded_file:
        return

    data = read_csv_to_data(uploaded_file)
    if data is None:
        stop_execution(
            f"Invalid dataset! Ensure it contains these columns: {REQUIRED_COLUMNS}"
        )
        return
    st.success("✅ Dataset loaded successfully!")

    classifier_to_train = new_classifier or existing_classifier

    if not classifier_to_train:
        return

    st.markdown(f"### Training: {classifier_to_train}")

    if not st.button(f"Train {classifier_to_train}!"):
        return

    flower_payload = flower_service.train_classifier(
        classifier=classifier_to_train,
        data=data,
    )
    st.write(
        f"New version trained: {flower_payload.model_name} - v{flower_payload.model_version}"  # noqa: E501
    )
