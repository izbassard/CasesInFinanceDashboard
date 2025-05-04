import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Plot trend lines
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['date'], df_filtered['copper_price'], label='Copper', color='orange', linewidth=2)
ax.plot(df_filtered['date'], df_filtered['zink_price'], label='Zinc', color='steelblue', linewidth=2)

ax.set_title("Monthly Copper & Zinc Prices (2015–2020)")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD per Metric Ton)")
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)
