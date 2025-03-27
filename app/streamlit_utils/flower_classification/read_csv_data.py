import csv
import io

from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.flower_classification.model.dataset import Dataset

REQUIRED_COLUMNS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species",
]


def read_csv_to_data(uploaded_file: UploadedFile) -> Dataset | None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(file_content))

    headers = next(csv_reader)

    if not all(col in headers for col in REQUIRED_COLUMNS):
        return None

    col_idx = {col: headers.index(col) for col in REQUIRED_COLUMNS}

    X, y = [], []

    for row in csv_reader:
        X.append([
            float(row[col_idx["sepal_length"]]),
            float(row[col_idx["sepal_width"]]),
            float(row[col_idx["petal_length"]]),
            float(row[col_idx["petal_width"]]),
        ])
        y.append(int(row[col_idx["species"]]))  # Assuming species is already numerical

    return Dataset(X=X, y=y)
