import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


def plot_line_chart(filtered_df):
    """
    Create and display a line chart using the filtered dataframe.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe with selected and filtered columns.
    """
    # Melt the dataframe for plotting
    plot_df = filtered_df.melt(id_vars="date", var_name="Metric", value_name="Value")
    
    # Create the line chart
    fig = px.line(
        plot_df,
        x="date",
        y="Value",
        color="Metric",
        labels={"date": "Date", "Value": "Value", "Metric": "Metric"},
        title="Interactive Line Chart"
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)






def plot_candlestick_chart(filtered_df):
    """
    Create and display a candlestick chart using the filtered dataframe.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date', 'open', 'high', 'low', and 'close' columns.
    """
    # Ensure the required columns are available
    required_columns = ["date", "open", "high", "low", "close"]
    if not all(col in filtered_df.columns for col in required_columns):
        st.error("The dataframe must contain 'date', 'open', 'high', 'low', and 'close' columns for a candlestick chart.")
        return

    # Create the candlestick chart
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=filtered_df["date"],
                open=filtered_df["open"],
                high=filtered_df["high"],
                low=filtered_df["low"],
                close=filtered_df["close"],
            )
        ]
    )
    
    # Customize layout
    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,  # Disable range slider for a cleaner view
        template="plotly_white",
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)





def plot_volume_density_chart(filtered_df):
    """
    Create and display a density chart for the 'volume' column.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe with the 'volume' column.
    """
    # Ensure the 'volume' column is available
    if "volume" not in filtered_df.columns:
        st.error("The 'volume' column is required for the density chart.")
        return

    # Create the density chart
    fig = px.density_contour(
        filtered_df,
        x="date",
        y="volume",
        title="Volume Density Chart",
        labels={"date": "Date", "volume": "Volume"},
    )

    # Customize layout
    fig.update_traces(contours_coloring="fill", contours_showlabels=True)
    fig.update_layout(template="plotly_white")

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



def plot_volume_bar_chart(filtered_df):
    """
    Create and display a bar chart for the trading volume.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date' and 'volume' columns.
    """
    # Ensure the required columns are available
    if "date" not in filtered_df.columns or "volume" not in filtered_df.columns:
        st.error("The dataframe must contain 'date' and 'volume' columns for the volume bar chart.")
        return

    # Create the bar chart
    fig = px.bar(
        filtered_df,
        x="date",
        y="volume",
        title="Volume Bar Chart",
        labels={"date": "Date", "volume": "Volume"},
    )

    # Customize layout
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Volume",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)




def plot_ohlc_bar_chart_with_labels(filtered_df):
    """
    Create and display an OHLC bar chart with labels for open, high, low, and close values.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date', 'open', 'high', 'low', and 'close' columns.
    """
    # Ensure the required columns are available
    required_columns = ["date", "open", "high", "low", "close"]
    if not all(col in filtered_df.columns for col in required_columns):
        st.error("The dataframe must contain 'date', 'open', 'high', 'low', and 'close' columns for the OHLC bar chart.")
        return

    # Create the OHLC bar chart
    fig = go.Figure(
        data=[
            go.Ohlc(
                x=filtered_df["date"],
                open=filtered_df["open"],
                high=filtered_df["high"],
                low=filtered_df["low"],
                close=filtered_df["close"],
                text=[
                    f"Open: {o}<br>High: {h}<br>Low: {l}<br>Close: {c}"
                    for o, h, l, c in zip(
                        filtered_df["open"], filtered_df["high"], filtered_df["low"], filtered_df["close"]
                    )
                ],
                hoverinfo="x+text",  # Display the labels on hover
            )
        ]
    )
    
    # Customize layout
    fig.update_layout(
        title="OHLC Bar Chart with Labels",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        xaxis_rangeslider_visible=False,  # Disable range slider for a cleaner view
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



def plot_moving_average_chart(filtered_df, window=7):
    """
    Create and display a moving average line chart for the 'close' price.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date' and 'close' columns.
        window (int): The window size for calculating the moving average (default: 7).
    """
    # Ensure the required columns are available
    if "date" not in filtered_df.columns or "close" not in filtered_df.columns:
        st.error("The dataframe must contain 'date' and 'close' columns for the moving average chart.")
        return

    # Calculate the moving average
    filtered_df["moving_average"] = filtered_df["close"].rolling(window=window).mean()

    # Create the line chart
    fig = px.line(
        filtered_df,
        x="date",
        y=["close", "moving_average"],
        title=f"Moving Average Line Chart (Window: {window})",
        labels={"date": "Date", "value": "Price", "variable": "Metric"},
    )

    # Customize layout
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Price",
        legend_title="Metrics",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



def plot_volume_price_chart(filtered_df):
    """
    Create and display a dual-axis chart showing close price and trading volume.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date', 'close', and 'volume' columns.
    """
    # Ensure the required columns are available
    required_columns = ["date", "close", "volume"]
    if not all(col in filtered_df.columns for col in required_columns):
        st.error("The dataframe must contain 'date', 'close', and 'volume' columns for this chart.")
        return

    # Create the figure
    fig = go.Figure()

    # Add Close Price line
    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["close"],
            name="Close Price",
            mode="lines",
            line=dict(color="blue"),
            yaxis="y1",  # Maps to the first y-axis
        )
    )

    # Add Volume bars
    fig.add_trace(
        go.Bar(
            x=filtered_df["date"],
            y=filtered_df["volume"],
            name="Volume",
            marker_color="orange",
            yaxis="y2",  # Maps to the second y-axis
        )
    )

    # Customize layout
    fig.update_layout(
        title="Volume Overlaid with Price Line Chart",
        xaxis=dict(title="Date"),
        yaxis=dict(
            title="Close Price",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue"),
            side="left",
        ),
        yaxis2=dict(
            title="Volume",
            titlefont=dict(color="orange"),
            tickfont=dict(color="orange"),
            overlaying="y",
            side="right",
        ),
        legend=dict(
            title="Legend",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2,
        ),
        template="plotly_white",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



def plot_bollinger_bands_chart(filtered_df, window=20, std_dev=2):
    """
    Create and display a Bollinger Bands chart with the close price and volatility bands.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date' and 'close' columns.
        window (int): The window size for calculating the moving average (default: 20).
        std_dev (int): The number of standard deviations for the upper and lower bands (default: 2).
    """
    # Ensure the required columns are available
    if "date" not in filtered_df.columns or "close" not in filtered_df.columns:
        st.error("The dataframe must contain 'date' and 'close' columns for the Bollinger Bands chart.")
        return

    # Calculate the moving average and Bollinger Bands
    filtered_df["moving_average"] = filtered_df["close"].rolling(window=window).mean()
    filtered_df["upper_band"] = filtered_df["moving_average"] + (filtered_df["close"].rolling(window=window).std() * std_dev)
    filtered_df["lower_band"] = filtered_df["moving_average"] - (filtered_df["close"].rolling(window=window).std() * std_dev)

    # Create the Bollinger Bands chart
    fig = px.line(
        filtered_df,
        x="date",
        y=["close", "moving_average", "upper_band", "lower_band"],
        title=f"Bollinger Bands (Window: {window}, Std Dev: {std_dev})",
        labels={"date": "Date", "value": "Price", "variable": "Metric"},
    )

    # Customize layout
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Price",
        legend_title="Metrics",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


def plot_high_low_range_area_chart(filtered_df):
    """
    Create and display a high-low range area chart.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'date', 'high', and 'low' columns.
    """
    # Ensure the required columns are available
    required_columns = ["date", "high", "low"]
    if not all(col in filtered_df.columns for col in required_columns):
        st.error("The dataframe must contain 'date', 'high', and 'low' columns for the high-low range area chart.")
        return

    # Create the area chart
    fig = go.Figure()

    # Add the high-low range area
    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["high"],
            name="High",
            mode="lines",
            line=dict(color="rgba(0, 100, 200, 0.7)"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["low"],
            name="Low",
            mode="lines",
            line=dict(color="rgba(200, 100, 0, 0.7)"),
            fill="tonexty",  # Fills the area between the high and low lines
            fillcolor="rgba(100, 150, 255, 0.3)",
        )
    )

    # Customize layout
    fig.update_layout(
        title="High-Low Range Area Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        legend_title="Metrics",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



def plot_scatter_plot(filtered_df, y_column="close"):
    """
    Create and display a scatter plot for volume vs. a selected price metric.

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing 'volume' and the selected y-axis column.
        y_column (str): The column to plot on the y-axis (default: 'close').
    """
    # Ensure the required columns are available
    if "volume" not in filtered_df.columns or y_column not in filtered_df.columns:
        st.error(f"The dataframe must contain 'volume' and '{y_column}' columns for the scatter plot.")
        return

    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x="volume",
        y=y_column,
        title=f"Scatter Plot: Volume vs. {y_column.capitalize()}",
        labels={"volume": "Volume", y_column: y_column.capitalize()},
        color=y_column,  # Color points based on the price metric
        size="volume",  # Scale point size by volume
    )

    # Customize layout
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Volume",
        yaxis_title=y_column.capitalize(),
        legend_title="Price",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)




def plot_correlation_heatmap(filtered_df):
    """
    Create and display an enhanced correlation heatmap for numerical columns (Low, High, Open, Close, Volume).

    Parameters:
        filtered_df (pd.DataFrame): The dataframe containing the numerical columns for correlation.
    """
    # Select numerical columns for correlation
    correlation_columns = ["low", "high", "open", "close", "volume"]
    available_columns = [col for col in correlation_columns if col in filtered_df.columns]

    # Ensure there are enough columns to compute correlations
    if len(available_columns) < 2:
        st.error("The dataframe must contain at least two numerical columns (low, high, open, close, volume) for the correlation heatmap.")
        return

    # Compute the correlation matrix
    correlation_matrix = filtered_df[available_columns].corr()

    # Create the heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=available_columns,
            y=available_columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
            text=correlation_matrix.round(2).values,  # Show rounded correlation values on hover
            hoverinfo="text+z",  # Show cell value and coordinates on hover
        )
    )

    # Customize layout
    fig.update_layout(
        title="Enhanced Correlation Heatmap",
        xaxis_title="Metrics",
        yaxis_title="Metrics",
        template="plotly_white",
        font=dict(size=14),  # General font size for the layout
    )

    # Annotate the heatmap with larger text labels
    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=available_columns[j],
                    y=available_columns[i],
                    text=f"{value:.2f}",  # Keep the value rounded to 2 decimal places
                    showarrow=False,
                    font=dict(size=16, color="black"),  # Increased font size for annotations
                )
            )
    fig.update_layout(annotations=annotations)

    # Display the heatmap in Streamlit
    st.plotly_chart(fig, use_container_width=True)


