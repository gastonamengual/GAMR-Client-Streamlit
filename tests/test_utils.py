from pathlib import Path

from app.streamlit_utils.object_detection import preprocess_image


def test_preprocess_image() -> None:
    sample_img_url = f"{Path.cwd()}/tests/examples/sample_images/desktop.jpg"

    image_base64 = preprocess_image(sample_img_url)
    assert image_base64 is not None
