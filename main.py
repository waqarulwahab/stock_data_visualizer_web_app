import streamlit as st
from data_processing import read_csv, validate_columns
from filters import filter_by_date, filter_by_rows, filter_by_columns
from display import display_dataframe
from visualizations import *
from kpis import *
from user_inputs import get_date_range, get_row_range, get_required_columns

# Set Streamlit layout to full width
st.set_page_config(layout="wide")

# Title of the app (Centered)
# st.markdown(
#     """
#     <h1 style="text-align: center;">CSV Viewer App</h1>
#     """,
#     unsafe_allow_html=True,
# )


st.sidebar.image("LOGO.jpg", width=200)  # Replace with your logo file path or URL
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Read the uploaded CSV file
        df = read_csv(uploaded_file)

        # Required columns
        required_columns = ["date", "close", "volume", "open", "high", "low"]
        if validate_columns(df, required_columns):
            # Get date range from user
            start_date, end_date = get_date_range(df)

            # Filter dataframe by date
            filtered_df = filter_by_date(df, start_date, end_date)

            # Get row range from user
            start_row, end_row = get_row_range(filtered_df)

            # Filter dataframe by rows
            filtered_df = filter_by_rows(filtered_df, start_row, end_row)

            # Get required columns from user
            selected_columns = get_required_columns(filtered_df, required_columns)
            filtered_df = filter_by_columns(filtered_df, selected_columns)
            filtered_df['date'] = pd.to_datetime(filtered_df['date'])
            # Format 'date' column to show only the date (YYYY-MM-DD)
            filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d')

            calculate_and_display_kpis(filtered_df)

            if "date" not in selected_columns:
                st.error("The 'date' column must be selected for plotting.")

            # Visualization
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
            with col1:
                line_chart = st.toggle("Line Chart")
            with col2:
                candlestick_chart =  st.toggle("Candlestick Chart")
            with col3:
                volume_price_chart = st.toggle("Volume Price Chart")  
            with col4:
                high_low_range_area_chart = st.toggle("High-Low Range Area Chart")
            with col5:
                moving_avg_chart = st.toggle("Moving Average Chart")

            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
            with col1:
               bollinger_bands_cahrt = st.toggle("Bollinger Bands Chart")
            with col2:
                volume_bar_chart = st.toggle("Volume Bar Chart")     
            with col3:
                scatter_plot = st.toggle("Scatter Plot")
            with col4:
                volume_density = st.toggle("Volume Density Chart")
            with col5:
                coorelation_heatmap = st.toggle("Correlation Heatmap")

   
            col1, col2 = st.columns([1,1])
            with col1:
                ohlc_bar_chart = st.toggle("OHLC Bar Chart")    
            with col2:
                pass
            
            st.divider()

            # Display dataframe
            display_dataframe(filtered_df)



            if ohlc_bar_chart:
                plot_ohlc_bar_chart_with_labels(filtered_df)

            if volume_density:
                plot_volume_density_chart(filtered_df)
            if coorelation_heatmap:
                plot_correlation_heatmap(filtered_df)

            col1, col2 = st.columns([1,1])
            with col1:
                if volume_bar_chart:
                    plot_volume_bar_chart(filtered_df)
            with col2:
                if scatter_plot:
                    plot_scatter_plot(filtered_df, y_column="close")  

            col1, col2 = st.columns([1,1])
            with col1:
                if moving_avg_chart:
                    plot_moving_average_chart(filtered_df, window=14)
            with col2:
                if bollinger_bands_cahrt:
                    plot_bollinger_bands_chart(filtered_df, window=20, std_dev=2)

            if volume_price_chart:
                plot_volume_price_chart(filtered_df)                
            if high_low_range_area_chart:
                plot_high_low_range_area_chart(filtered_df)

            col1, col2 = st.columns([1,1])
            with col1:
                if line_chart:
                    plot_line_chart(filtered_df)
            with col2:
                if candlestick_chart:
                    plot_candlestick_chart(filtered_df)   









        else:
            st.error(f"The file must have the following columns: {', '.join(required_columns)}")
    except Exception as e:
        st.error(str(e))
else:
    st.info("Please upload a CSV file using the sidebar.")







