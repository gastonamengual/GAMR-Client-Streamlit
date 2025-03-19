import streamlit as st


def main() -> None:
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
    Welcome to my MLOps project!

    Explore the power of machine learning through our interactive demos and models.

    🌸 Iris Classifier:

    Upload your flower dataset and watch as the model classifies your flowers into one of three categories based on sepal and petal measurements.

    Streamlit UI + FastAPI backend service (hosted in Vercel) + FastAPI Model Registry (hosted in Vercel) + MLFLow Registry (hosted in render as a Docker Image)

    🖼️ Object Recognition:

    The object recognition model can detect objects in images, helping you explore how deep learning models work with visual data.

    Streamlit UI + FastAPI backend service (hosted in Vercel) + Model Registry (hosted in HuggingFace)


    """  # noqa: E501
    )
