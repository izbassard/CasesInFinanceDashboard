import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(page_title="Kazakhmys Dashboard", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Kazakhmys Dashboard")
page = st.sidebar.radio("Select a page", ["Market Research", "Net Present Value"])

# --- Load Data ---
# Load copper & zinc prices
df_prices = pd.read_csv("copper_zinc_prices.csv")
df_prices['date'] = pd.to_datetime(df_prices['date'], format='%m/%d/%Y')
df_prices = df_prices[(df_prices['date'] >= '2015-01-01') & (df_prices['date'] <= '2020-12-31')]

# Transform to long format for plotting
df_long = df_prices.melt(id_vars='date', value_vars=['copper_price', 'zinc_price'],
                         var_name='Metal', value_name='Price')
df_long['Metal'] = df_long['Metal'].str.replace('_price', '').str.title()

# Load PPI data
df_ppi = pd.read_csv("PCU2122321223.csv")
df_ppi['date'] = pd.to_datetime(df_ppi['observation_date'], format='%m/%d/%Y')
df_ppi.rename(columns={'PCU2122321223': 'PPI'}, inplace=True)
df_ppi = df_ppi[df_ppi['date'] <= '2020-12-31']

# --- Market Research Page ---
if page == "Market Research":
    st.title("Market Research")
    st.markdown("**Units:** U.S. Dollars per Metric Ton and Index Value  \n**Frequency:** Monthly")

    col1, col2 = st.columns(2)

    with col1:
        fig_prices = px.line(df_long, x='date', y='Price', color='Metal',
                             title='Monthly Copper & Zinc Prices (2015–2020)',
                             labels={'date': 'Date', 'Price': 'Price (USD per Metric Ton)', 'Metal': 'Metal'},
                             template='plotly_white')
        fig_prices.update_traces(mode='lines+markers')
        fig_prices.update_layout(hovermode="x unified")
        st.plotly_chart(fig_prices, use_container_width=True)

    with col2:
        fig_ppi = go.Figure()

        fig_ppi.add_trace(go.Scatter(x=df_ppi['date'], y=df_ppi['PPI'],
                                     mode='lines+markers',
                                     name='PPI',
                                     line=dict(color='firebrick', width=2)))

        highlight_dates = ['2008-09-01', '2020-03-01']
        annotations = ['2008 Crash', 'COVID-19 Crash']

        for d, label in zip(highlight_dates, annotations):
            fig_ppi.add_vline(x=pd.to_datetime(d), line_dash="dash", line_color="gray")
            fig_ppi.add_annotation(x=pd.to_datetime(d), y=max(df_ppi['PPI']),
                                   text=label,
                                   showarrow=True,
                                   arrowhead=1,
                                   yshift=10)

        fig_ppi.update_layout(title="Producer Price Index: Copper, Nickel, Lead and Zinc Mining",
                              xaxis_title="Date",
                              yaxis_title="Index Value",
                              template='plotly_white',
                              hovermode="x unified")

        st.plotly_chart(fig_ppi, use_container_width=True)

# --- Net Present Value Page ---
elif page == "Net Present Value":
    st.title("Net Present Value")
    st.info("This section is under development.")
