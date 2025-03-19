import streamlit as st


def stop_execution(message: str) -> None:
    st.error(message)
    st.stop()
