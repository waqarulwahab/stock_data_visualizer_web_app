import streamlit as st
import pandas as pd

def get_date_range(df):
    """Allow the user to select a date range using date pickers."""
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=pd.to_datetime(df['date'].min()))
    with col2:
        end_date = st.date_input("End Date", value=pd.to_datetime(df['date'].max()))
    return start_date, end_date

def get_row_range(filtered_df):
    """Allow the user to select a row range."""
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_row = st.number_input("Start Row", min_value=0, max_value=len(filtered_df) - 1, value=0)
    with col2:
        end_row = st.number_input("End Row", min_value=0, max_value=len(filtered_df), value=len(filtered_df))
    return start_row, end_row

def get_required_columns(df, required_columns):
    """Validate required columns and allow the user to select additional columns."""
    return st.sidebar.multiselect(
        "Select Columns to Display",
        options=df.columns,
        default=required_columns
    )
