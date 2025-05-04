import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Copper & Zinc Prices (2015–2020)", layout="centered")

st.title("Copper and Zinc Prices (2015–2020)")
st.markdown("**Units:** U.S. Dollars per Metric Ton  \n**Frequency:** Monthly, Not Seasonally Adjusted")

# Load CSV file
df = pd.read_csv("copper_zinc_prices.csv")

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

# Filter data from Jan 2015 to Dec 2020
mask = (df['date'] >= '2015-01-01') & (df['date'] <= '2020-12-31')
df_filtered = df.loc[mask]

# Melt the dataframe to long format for Plotly Express
df_long = df_filtered.melt(id_vars='date', value_vars=['copper_price', 'zinc_price'],
                           var_name='Metal', value_name='Price')

# Rename for nicer labels
df_long['Metal'] = df_long['Metal'].str.replace('_price', '').str.title()

# Create interactive line plot
fig = px.line(df_long, x='date', y='Price', color='Metal',
              title='Monthly Copper & Zinc Prices (2015–2020)',
              labels={'date': 'Date', 'Price': 'Price (USD per Metric Ton)', 'Metal': 'Metal'},
              template='plotly_white')

fig.update_traces(mode='lines+markers')
fig.update_layout(hovermode="x unified")

# Show interactive plot in Streamlit
st.plotly_chart(fig, use_container_width=True)
