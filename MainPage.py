import streamlit as st


def main() -> None:
    st.set_page_config(
        page_title="GAMR MLOps Project", page_icon="📱", layout="centered"
    )

    st.write("# Welcome to my MLOps project! 👋")

    st.markdown(
        """
        This platform is designed to showcase a flexible and scalable MLOps architecture. It simulates real-world industry scenarios where multiple clients and model registries seamlessly integrate, demonstrating how a well-structured, decoupled system can make AI deployments more efficient, adaptable, and easier to maintain.


        The client is part of a layered MLOps architecture:
        *	**Client**: Streamlit-based UI for user interaction.
        *	**Backend**: A FastAPI service that handles request validation and authentication, hosted both as a Docker image on Render and on Vercel.
        *	**Model Registry**:
            *	Hugging Face model for image classification.
            *	MLFlow model hosted on Render (Docker container) for iris classification.

        """  # noqa: E501
    )

    st.image("architecture.png")
