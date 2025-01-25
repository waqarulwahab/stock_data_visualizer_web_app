import pandas as pd

def read_csv(file):
    """Read the uploaded CSV file."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        raise ValueError(f"Error reading the file: {e}")

def validate_columns(df, required_columns):
    """Validate if the required columns exist in the dataframe."""
    return all(col in df.columns for col in required_columns)
