import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('copper_zink_prices.csv', delimiter='\t')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

# Sidebar configuration
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Market Analysis"])

# Main content
st.title("Copper and Zinc Prices Dashboard")
st.markdown("""
**Data Source:** Monthly prices from 2015-2020  
**Units:** U.S. Dollars per Metric Ton (Not Seasonally Adjusted)
""")

if page == "Market Analysis":
    st.header("Market Analysis: Copper vs Zinc Prices")
    
    # Filter data for 2015-2020
    filtered_data = data[(data['Date'].dt.year >= 2015) & (data['Date'].dt.year <= 2020)]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot copper prices
    ax.plot(filtered_data['Date'], filtered_data['copper_price'], 
            label='Copper Price', color='#b87333', linewidth=2)
    
    # Plot zinc prices
    ax.plot(filtered_data['Date'], filtered_data['zink_price'], 
            label='Zinc Price', color='#7d7d7d', linewidth=2)
    
    # Formatting
    ax.set_title('Monthly Copper and Zinc Prices (2015-2020)', fontsize=14)
    ax.set_ylabel('Price (USD per Metric Ton)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis to show years
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent cutoff
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    # Add some statistics
    st.subheader("Price Statistics (2015-2020)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Copper - Highest Price", f"${filtered_data['copper_price'].max():,.2f}")
        st.metric("Copper - Lowest Price", f"${filtered_data['copper_price'].min():,.2f}")
        st.metric("Copper - Average Price", f"${filtered_data['copper_price'].mean():,.2f}")
    
    with col2:
        st.metric("Zinc - Highest Price", f"${filtered_data['zink_price'].max():,.2f}")
        st.metric("Zinc - Lowest Price", f"${filtered_data['zink_price'].min():,.2f}")
        st.metric("Zinc - Average Price", f"${filtered_data['zink_price'].mean():,.2f}")