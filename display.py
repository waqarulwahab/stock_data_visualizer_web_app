import streamlit as st

def display_dataframe(filtered_df):
    """Display the dataframe if the user toggles the display button."""
    if st.sidebar.toggle("Dataframe Display"):
        st.write("### Filtered Data:")
        st.write(filtered_df)
