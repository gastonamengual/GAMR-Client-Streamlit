import csv
import io

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.flower_classification.model import Dataset


def read_csv_to_data(uploaded_file: UploadedFile) -> Dataset:
    file_content = uploaded_file.getvalue().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(file_content))

    headers = next(csv_reader)

    required_columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]

    if not all(col in headers for col in required_columns):
        st.error(
            f"❌ Invalid dataset! Ensure it contains these columns: {required_columns}"
        )
        st.stop()

    st.success("✅ Dataset loaded successfully!")

    col_idx = {col: headers.index(col) for col in required_columns}

    X, y = [], []

    for row in csv_reader:
        X.append(
            [
                float(row[col_idx["sepal_length"]]),
                float(row[col_idx["sepal_width"]]),
                float(row[col_idx["petal_length"]]),
                float(row[col_idx["petal_width"]]),
            ]
        )
        y.append(int(row[col_idx["species"]]))  # Assuming species is already numerical

    return Dataset(X=X, y=y)
