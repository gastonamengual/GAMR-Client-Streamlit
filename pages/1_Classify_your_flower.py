import streamlit as st

from app.api_client.model import BackendService, backend_service_urls
from app.streamlit_utils.flower_classification import classification_tab, training_tab


def main() -> None:
    disabled = False
    st.title("Iris Classification Feature Currently Disabled")
    st.markdown("""

    ### Hosting Limitations
    - **Vercel** does not support deployments exceeding 250MB, and **MLflow** exceeds this limit, making it impossible to host the API there.
    - **Render's** free tier has a 512MB RAM limit, which is not enough for running **MLflow** reliably.

    ### Alternative Solutions
    To enable **MLflow** with a functional model registry, a paid hosting option is required. Possible alternatives include:
    - **Azure Functions** - Serverless compute service that can run ML models efficiently.
    - **AWS Lambda** - Scalable serverless option with flexible resource allocation.

    """)  # noqa: E501

    if disabled:
        return

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
