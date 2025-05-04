import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Page title
st.set_page_config(page_title="Commodity Price Trends", layout="wide")
st.title("Commodity Price Trends (2015 - 2020)")

# Download data
@st.cache_data
def get_price_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data['Adj Close']

# Date range
start_date = "2015-01-01"
end_date = "2020-12-31"

# Get copper and zinc prices
copper = get_price_data("HG=F", start_date, end_date)  # Copper Futures
zinc = get_price_data("ZNC=F", start_date, end_date)   # Zinc Futures

# Convert to DataFrame for Plotly
copper_df = pd.DataFrame({"Date": copper.index, "Copper Price (USD)": copper.values})
zinc_df = pd.DataFrame({"Date": zinc.index, "Zinc Price (USD)": zinc.values})

# Layout: two columns
col1, col2 = st.columns(2)

# Copper Plot
with col1:
    st.subheader("Copper Price Trend")
    fig1 = px.line(copper_df, x="Date", y="Copper Price (USD)", title="Copper Daily Price (2015 - 2020)")
    st.plotly_chart(fig1, use_container_width=True)

# Zinc Plot
with col2:
    st.subheader("Zinc Price Trend")
    fig2 = px.line(zinc_df, x="Date", y="Zinc Price (USD)", title="Zinc Daily Price (2015 - 2020)")
    st.plotly_chart(fig2, use_container_width=True)
