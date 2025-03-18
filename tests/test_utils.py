import os

from app.streamlit_utils.object_detection import preprocess_image


def test_preprocess_image():
    current_dir = os.getcwd()
    sample_img_url = f"{current_dir}/images/sample_images/desktop.jpg"

    image_base64 = preprocess_image(sample_img_url)
    assert image_base64 is not None
