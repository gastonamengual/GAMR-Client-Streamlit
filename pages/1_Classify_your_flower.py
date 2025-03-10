import csv
import io

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.api_client.api_client import API_Client
from app.api_client.model import BackendService, backend_service_urls
from app.flower_classification import IMAGE_FLOWER_MAPPING, Flower
from app.flower_classification.model import Dataset


def authenticate(api_client: API_Client):
    token = api_client.authenticate()
    st.session_state.token = token


def get_classifiers(api_client: API_Client):
    models = [""]
    models = models + api_client.get_classifier()
    return models


def get_classifier_versions(api_client: API_Client, classifier: str):
    classifier_versions = [""]
    classifier_versions = classifier_versions + api_client.get_classifier_versions(
        classifier=classifier
    )
    return classifier_versions


def read_csv_to_data(uploaded_file: UploadedFile) -> Dataset:
    file_content = uploaded_file.getvalue().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(file_content))

    headers = next(csv_reader)

    required_columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]

    if not all(col in headers for col in required_columns):
        st.error(
            f"❌ Invalid dataset! Ensure it contains these columns: {required_columns}"
        )
        st.stop()

    st.success("✅ Dataset loaded successfully!")

    col_idx = {col: headers.index(col) for col in required_columns}

    X, y = [], []

    for row in csv_reader:
        X.append(
            [
                float(row[col_idx["sepal_length"]]),
                float(row[col_idx["sepal_width"]]),
                float(row[col_idx["petal_length"]]),
                float(row[col_idx["petal_width"]]),
            ]
        )
        y.append(int(row[col_idx["species"]]))  # Assuming species is already numerical

    return Dataset(X=X, y=y)


def training_tab(api_client: API_Client):
    new_classifier = st.text_input("Enter a new classifier name to train:", "")

    classifiers = get_classifiers(api_client=api_client)
    disable_selectbox = bool(new_classifier)
    classifier = st.selectbox(
        "Or select an existing Flower Classifier",
        classifiers,
        disabled=disable_selectbox,
    )

    classifier_to_train = new_classifier if new_classifier else classifier

    st.markdown(f"### Training: {classifier_to_train}")

    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
    if uploaded_file:
        data = read_csv_to_data(uploaded_file)
        if st.button(f"Train {classifier}!"):
            flower_payload = api_client.train_classifier(
                classifier=classifier_to_train,
                data=data,
            )
            st.write(
                f"New version trained: {flower_payload.model_name} - v{flower_payload.model_version}"
            )


def prediction_tab(api_client: API_Client):
    classifiers = get_classifiers(api_client=api_client)
    classifier = st.selectbox("Select Flower Classifier", classifiers)

    if classifier:
        classifier_versions = get_classifier_versions(api_client, classifier=classifier)
        classifier_version = st.selectbox(
            "Select Classifier Version", classifier_versions
        )

        if classifier and classifier_version:
            st.write("Enter your flower features")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                sepal_length = st.slider(
                    "Sepal Length", min_value=4.0, max_value=8.0, value=5.0
                )
            with col2:
                sepal_width = st.slider(
                    "Sepal Width", min_value=2.0, max_value=5.0, value=3.0
                )
            with col3:
                petal_length = st.slider(
                    "Petal Length", min_value=1.0, max_value=7.0, value=4.0
                )
            with col4:
                petal_width = st.slider(
                    "Petal Width", min_value=0.1, max_value=2.5, value=1.5
                )

            flower = Flower(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
            )

            if st.button("Predict Flower!"):
                flower = api_client.classify_flower(
                    flower=flower,
                    classifier=classifier,
                    classifier_version=str(classifier_version),
                )
                image_path = IMAGE_FLOWER_MAPPING[flower.classification]  # type: ignore
                st.write(f"Your flower is an Iris {flower.classification}")
                st.image(image_path, width=400)

                st.text("Was the model good? Promote it!")


def main():
    st.title("Flower Recognition - MLFlow")
    st.header("By Gastón Amengual")

    backend_service = st.selectbox(
        "Choose a Service:",
        [option.value for option in BackendService],
        index=2,
    )
    backend_service_url = backend_service_urls[backend_service]

    api_client = API_Client(username="gaston", base_url=backend_service_url)
    authenticate(api_client)

    # Create tabs
    tab1, tab2 = st.tabs(["🔮 Prediction", "📚 Training"])
    with tab1:
        prediction_tab(api_client)
    with tab2:
        training_tab(api_client)


st.set_page_config(page_title="ML Model", page_icon="🤖", layout="wide")
main()
