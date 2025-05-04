import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Copper and Zinc Prices", layout="wide")
st.title("Commodity Price Trends (2015 - 2020)")

# Function to fetch data with error handling
@st.cache_data
def get_price_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            return None
        return data["Adj Close"]
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Date range
start_date = "2015-01-01"
end_date = "2020-12-31"

# Get data
copper_data = get_price_data("HG=F", start_date, end_date)  # Copper Futures
zinc_data = get_price_data("ZNC=F", start_date, end_date)   # Zinc Futures

# Layout
col1, col2 = st.columns(2)

# Plot Copper
with col1:
    st.subheader("Copper Price Trend (USD)")
    if copper_data is not None:
        df_copper = pd.DataFrame({"Date": copper_data.index, "Price": copper_data.values})
        fig_copper = px.line(df_copper, x="Date", y="Price", title="Copper Daily Price (2015 - 2020)")
        st.plotly_chart(fig_copper, use_container_width=True)
    else:
        st.warning("Copper price data is unavailable or could not be loaded.")

# Plot Zinc
with col2:
    st.subheader("Zinc Price Trend (USD)")
    if zinc_data is not None:
        df_zinc = pd.DataFrame({"Date": zinc_data.index, "Price": zinc_data.values})
        fig_zinc = px.line(df_zinc, x="Date", y="Price", title="Zinc Daily Price (2015 - 2020)")
        st.plotly_chart(fig_zinc, use_container_width=True)
    else:
        st.warning("Zinc price data is unavailable or could not be loaded.")
