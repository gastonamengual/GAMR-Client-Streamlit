import streamlit as st

from app.api_client.api_client import API_Client
from app.api_client.model import BackendService, backend_service_urls
from app.flower_recognition import Dataset, FlowerPayload


def authenticate(api_client: API_Client):
    token = api_client.authenticate()
    st.session_state.token = token


def select_model(api_client: API_Client):
    models = [""]
    models = models + api_client.get_models()
    model_name = st.selectbox("Select Model", models)
    return model_name


def select_version(api_client: API_Client, model_name: str):
    api_client = API_Client(username="gaston", base_url="http://localhost:8080")
    token = api_client.authenticate()
    st.session_state.token = token
    model_versions = [""]
    model_versions = model_versions + api_client.get_model_versions(
        model_name=model_name
    )
    model_version = st.selectbox("Select Model Version", model_versions)
    return model_version


def main():
    st.title("Flower Recognition - MLFlow")
    st.header("By Gastón Amengual")

    backend_service = st.selectbox(
        "Choose a Backend Service:",
        [option.value for option in BackendService],
        index=2,
    )
    backend_service_url = backend_service_urls[backend_service]

    api_client = API_Client(username="gaston", base_url=backend_service_url)
    authenticate(api_client)

    model_name = select_model(api_client)
    if model_name:
        model_version = select_version(api_client, model_name)

    if model_name and model_version:
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

        dataset = Dataset(X=[[sepal_length, sepal_width, petal_length, petal_width]])
        flower_payload = FlowerPayload(
            data=dataset,
            model_name=model_name,
            model_version=model_version,
        )

        if st.button("Predict Flower!"):
            prediction = api_client.predict_flower_model(flower_payload)
            st.write(f"Prediction: {prediction}")

        # if st.button("Train new version with new data"):
        # # Make prediction with the selected model
        # model_version = 1
        # st.write(f"Trained new version: v{model_version}")

        # if st.button("Was the model good? Promote it!"):
        #     st.text_input("Model Alias")


main()
