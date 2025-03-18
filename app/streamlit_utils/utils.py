import streamlit as st


def stop_execution(message: str):
    st.error(message)
    st.stop()
