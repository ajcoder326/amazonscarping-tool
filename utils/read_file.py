import os
import pandas as pd

def read_file(file_path):
    """Read CSV/XLSX file and return (base_name, first_column_list)"""

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read the file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide CSV or Excel.")

    # Get filename without extension
    base_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(base_name)[0]

    # Get first column list
    first_column_list = df.iloc[:, 0].tolist()

    return name_without_ext, first_column_list
