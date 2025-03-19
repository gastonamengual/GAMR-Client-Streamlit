import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.api_client.api_client import API_Client
from app.api_client.model import BackendService, backend_service_urls
from app.object_recognition import ImagePayload, ObjectDetectionService
from app.streamlit_utils.object_detection import preprocess_image


def generate_ui() -> tuple[UploadedFile | None, str, str]:
    st.title("Image Recognition App")
    st.header("By Gastón Amengual")

    col1, col2 = st.columns(2)

    with col1:
        backend_service = st.selectbox(
            "Choose a Backend Service:",
            [option.value for option in BackendService],
        )
        backend_service_url = backend_service_urls[backend_service]
        if backend_service == "Render + Docker":
            st.warning(
                "Due to Render's free trial, this request can take up 50 seconds"
            )

    with col2:
        model_service = st.selectbox("Choose an AI Model Registry", ["HuggingFace"])

    uploaded_image = st.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False
    )

    return uploaded_image, backend_service_url, model_service


def get_prediction(
    filename: str, encoded_image: str, model_service: str, api_client: API_Client
) -> bytes:
    image_payload = ImagePayload(
        filename=filename,
        image_bytes=encoded_image,
        model_service=model_service,
    )
    service = ObjectDetectionService(api_client=api_client)
    return service.detect_objects(image_payload)


def main() -> None:
    uploaded_image, backend_service_url, model_service = generate_ui()

    if not uploaded_image:
        return

    placeholder = st.empty()
    placeholder.image(uploaded_image, use_container_width=True)

    if not st.button("Detect objects!"):
        return

    encoded_image = preprocess_image(uploaded_image)

    api_client = API_Client(base_url=backend_service_url)
    api_client.authenticate()

    detected_image = get_prediction(
        filename=uploaded_image.name,
        encoded_image=encoded_image,
        model_service=model_service,
        api_client=api_client,
    )

    st.header("Objects detected!")
    placeholder.empty()
    st.image(detected_image, use_container_width=True)


if __name__ == "__main__":
    main()
