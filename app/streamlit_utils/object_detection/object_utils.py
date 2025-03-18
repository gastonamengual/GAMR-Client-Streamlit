import base64
import io

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def preprocess_image(uploaded_image: UploadedFile) -> str:
    image = Image.open(uploaded_image)
    buffer = io.BytesIO()
    image.save(buffer, format="jpeg")
    image_bytes = buffer.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")
