import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(page_title="Commodity Prices Dashboard", layout="wide")
st.title("Commodity Prices (2015-2020)")

# Function to get price data
@st.cache_data
def get_price_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data = data.reset_index()  # Make sure Date becomes a column
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure proper datetime format
    return data

# Date range
start_date = "2015-01-01"
end_date = "2020-12-31"

# Get data with error handling
try:
    with st.spinner('Fetching copper data...'):
        copper_data = get_price_data("HG=F", start_date, end_date)  # Copper futures
        
    with st.spinner('Fetching zinc data...'):
        zinc_data = get_price_data("ZN=F", start_date, end_date)    # Zinc futures
        
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Create two columns for layout
col1, col2 = st.columns(2)

# Copper Price Chart
with col1:
    st.subheader("Copper Daily Prices (2015-2020)")
    if not copper_data.empty:
        # Rename columns to simplify for Plotly
        plot_data = copper_data.rename(columns={'Date': 'Date', 'Close': 'Price'})
        fig_copper = px.line(plot_data, 
                            x='Date', 
                            y='Price',
                            labels={'Price': 'Price (USD)'},
                            color_discrete_sequence=['#FF5733'])
        fig_copper.update_layout(showlegend=False)
        st.plotly_chart(fig_copper, use_container_width=True)
    else:
        st.warning("No copper data available")

# Zinc Price Chart
with col2:
    st.subheader("Zinc Daily Prices (2015-2020)")
    if not zinc_data.empty:
        # Rename columns to simplify for Plotly
        plot_data = zinc_data.rename(columns={'Date': 'Date', 'Close': 'Price'})
        fig_zinc = px.line(plot_data, 
                          x='Date', 
                          y='Price',
                          labels={'Price': 'Price (USD)'},
                          color_discrete_sequence=['#33A1FF'])
        fig_zinc.update_layout(showlegend=False)
        st.plotly_chart(fig_zinc, use_container_width=True)
    else:
        st.warning("No zinc data available")

# Metrics section
st.subheader("Price Summary (2015-2020)")
m1, m2, m3, m4 = st.columns(4)

with m1:
    if not copper_data.empty:
        st.metric("Copper Highest", f"${copper_data['Close'].max():.2f}")

with m2:
    if not copper_data.empty:
        st.metric("Copper Lowest", f"${copper_data['Close'].min():.2f}")

with m3:
    if not zinc_data.empty:
        st.metric("Zinc Highest", f"${zinc_data['Close'].max():.2f}")

with m4:
    if not zinc_data.empty:
        st.metric("Zinc Lowest", f"${zinc_data['Close'].min():.2f}")

# Data source info
st.caption("Data source: Yahoo Finance (yfinance) - Copper (HG=F) and Zinc (ZN=F) futures prices")