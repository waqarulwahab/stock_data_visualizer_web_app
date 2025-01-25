import pandas as pd

def filter_by_date(df, start_date, end_date):
    """Filter the dataframe by a date range."""
    df['date'] = pd.to_datetime(df['date'])
    return df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

def filter_by_rows(df, start_row, end_row):
    """Filter the dataframe by row indices."""
    return df.iloc[start_row:end_row, :]

def filter_by_columns(df, selected_columns):
    """Filter the dataframe by selected columns."""
    return df[selected_columns]
