import pandas as pd
import streamlit as st

# Individual KPI functions

def get_latest_closing_price(filtered_df):
    """Calculate the most recent closing price."""
    return filtered_df["close"].iloc[-1]

def get_daily_price_change(filtered_df):
    """Calculate the daily price change (absolute and percentage)."""
    if len(filtered_df) > 1:
        latest_close = filtered_df["close"].iloc[-1]
        previous_close = filtered_df["close"].iloc[-2]
        daily_change_abs = latest_close - previous_close
        daily_change_pct = (daily_change_abs / previous_close) * 100
        return daily_change_abs, daily_change_pct
    return 0, 0

def get_52_week_high_low(filtered_df):
    """Calculate the 52-week high and low prices."""
    if "high" in filtered_df.columns and "low" in filtered_df.columns:
        return filtered_df["high"].max(), filtered_df["low"].min()
    return None, None

def get_average_volume(filtered_df, days=30):
    """Calculate the average trading volume over the last `days` days."""
    if "volume" in filtered_df.columns:
        if len(filtered_df) >= days:
            return filtered_df["volume"].iloc[-days:].mean()
        return filtered_df["volume"].mean()
    return None

def get_ytd_return(filtered_df):
    """Calculate the Year-to-Date (YTD) return as a percentage."""
    if "close" in filtered_df.columns:
        latest_close = filtered_df["close"].iloc[-1]
        year_start_close = filtered_df["close"].iloc[0]
        return ((latest_close - year_start_close) / year_start_close) * 100
    return None

def get_moving_average(filtered_df, window):
    """Calculate the moving average for the specified window size."""
    if len(filtered_df) >= window:
        return filtered_df["close"].rolling(window=window).mean().iloc[-1]
    return None





def calculate_and_display_kpis(filtered_df):
    """
    Calculate and display key performance indicators (KPIs) for the stock dataset.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing the stock data with 'date', 'close', 'high', 'low', and 'volume' columns.
    """
    if "close" not in filtered_df.columns or "date" not in filtered_df.columns:
        st.error("The dataframe must contain 'date' and 'close' columns to calculate KPIs.")
        return

    # Ensure the dataframe is sorted by date
    filtered_df = filtered_df.sort_values(by="date")

    # Calculate KPIs
    latest_close = get_latest_closing_price(filtered_df)
    daily_change_abs, daily_change_pct = get_daily_price_change(filtered_df)
    high_52_week, low_52_week = get_52_week_high_low(filtered_df)
    avg_volume_30_days = get_average_volume(filtered_df, days=30)
    ytd_return = get_ytd_return(filtered_df)
    moving_avg_50 = get_moving_average(filtered_df, window=50)
    moving_avg_200 = get_moving_average(filtered_df, window=200)

    # Display KPIs
    # st.markdown("<h2 style='text-align: center;'>📊 Key Performance Indicators (KPIs)</h2>", unsafe_allow_html=True)
    # st.title("📊 Key Performance Indicators (KPIs)")

    with st.container():
        col1, col2, col3 = st.columns(3)

        # Latest Closing Price
        with col1:
            st.markdown("### 💰 Latest Closing Price")
            st.write(f"<h3 style='color: #1f77b4;'>${latest_close:.2f}</h3>", unsafe_allow_html=True)

        # Daily Price Change
        with col2:
            st.markdown("### 📈 Daily Price Change")
            delta_color = "green" if daily_change_abs >= 0 else "red"
            st.write(
                f"<h3 style='color: {delta_color};'>${daily_change_abs:.2f} ({daily_change_pct:.2f}%)</h3>",
                unsafe_allow_html=True,
            )

        # 52-Week High and Low
        with col3:
            st.markdown("### 📅 52-Week High & Low")
            st.write(f"<b>High:</b> ${high_52_week:.2f}" if high_52_week else "N/A", unsafe_allow_html=True)
            st.write(f"<b>Low:</b> ${low_52_week:.2f}" if low_52_week else "N/A", unsafe_allow_html=True)

    with st.container():
        col4, col5, col6 = st.columns(3)

        # Average Volume
        with col4:
            st.markdown("### 📊 Average Volume (30 days)")
            st.write(f"<h3 style='color: #9467bd;'>{avg_volume_30_days:,.0f}</h3>" if avg_volume_30_days else "N/A",
                     unsafe_allow_html=True)

        # YTD Return
        with col5:
            st.markdown("### 🏆 Year-to-Date Return")
            ytd_color = "green" if ytd_return >= 0 else "red"
            st.write(f"<h3 style='color: {ytd_color};'>{ytd_return:.2f}%</h3>", unsafe_allow_html=True)

        # Moving Averages
        with col6:
            st.markdown("### 📊 Moving Averages")
            st.write(f"<b>50-Day:</b> ${moving_avg_50:.2f}" if moving_avg_50 else "N/A", unsafe_allow_html=True)
            st.write(f"<b>200-Day:</b> ${moving_avg_200:.2f}" if moving_avg_200 else "N/A", unsafe_allow_html=True)

    st.markdown("---")












