import streamlit as st

from app.api_client.model import BackendService, backend_service_urls
from app.streamlit_utils.flower_classification import classification_tab, training_tab


def main():
    st.title("Flower Recognition - MLFlow")
    st.header("By Gastón Amengual")

    backend_service = st.selectbox(
        "Choose a Service:",
        [option.value for option in BackendService],
        index=2,
    )
    backend_service_url = backend_service_urls[backend_service]

    tab1, tab2 = st.tabs(["🔮 Prediction", "📚 Training"])
    with tab1:
        classification_tab(backend_service_url)
    with tab2:
        training_tab(backend_service_url)


st.set_page_config(page_title="ML Model", page_icon="🤖", layout="wide")
main()
