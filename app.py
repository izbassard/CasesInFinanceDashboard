import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page title and layout
st.set_page_config(page_title="Commodity Prices Dashboard", layout="wide")
st.title("Commodity Prices (2015-2020)")

# Function to fetch and process data
def get_commodity_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Date range
start_date = '2015-01-01'
end_date = '2020-12-31'

# Fetch data
with st.spinner('Loading data...'):
    copper_data = get_commodity_data('HG=F', start_date, end_date)  # Copper futures ticker
    zinc_data = get_commodity_data('ZN=F', start_date, end_date)    # Zinc futures ticker

# Create two columns for the charts
col1, col2 = st.columns(2)

# Copper Price Chart
with col1:
    st.subheader("Copper Daily Prices (2015-2020)")
    fig_copper = px.line(copper_data, 
                         x='Date', 
                         y='Close', 
                         labels={'Close': 'Price (USD)'},
                         color_discrete_sequence=['#FF5733'])
    fig_copper.update_layout(showlegend=False)
    st.plotly_chart(fig_copper, use_container_width=True)

# Zinc Price Chart
with col2:
    st.subheader("Zinc Daily Prices (2015-2020)")
    fig_zinc = px.line(zinc_data, 
                       x='Date', 
                       y='Close', 
                       labels={'Close': 'Price (USD)'},
                       color_discrete_sequence=['#33A1FF'])
    fig_zinc.update_layout(showlegend=False)
    st.plotly_chart(fig_zinc, use_container_width=True)

# Add some metrics
st.subheader("Price Summary (2015-2020)")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Copper Highest", f"${copper_data['Close'].max():.2f}")

with metric_col2:
    st.metric("Copper Lowest", f"${copper_data['Close'].min():.2f}")

with metric_col3:
    st.metric("Zinc Highest", f"${zinc_data['Close'].max():.2f}")

with metric_col4:
    st.metric("Zinc Lowest", f"${zinc_data['Close'].min():.2f}")

# Add a note about the data source
st.caption("Data source: Yahoo Finance (yfinance) - Copper (HG=F) and Zinc (ZN=F) futures prices")