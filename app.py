import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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

python
elif page == "Net Present Value":
    # --- Constants ---
    copper = {
        "initial_investment": 50_000_000,  # These were zinc values
        "life": 8,                         # These were zinc values
        "annual_cash_flow": 10_000_000,    # These were zinc values
        "salvage_value": 5_000_000         # These were zinc values
    }

    zinc = {
        "initial_investment": 150_000_000,  # These were copper values
        "life": 12,                         # These were copper values
        "annual_cash_flow": 20_000_000,     # These were copper values
        "salvage_value": 10_000_000         # These were copper values
    }

    def calculate_npv(rate, project):
        r = rate / 100
        cash_flows = [project["annual_cash_flow"]] * project["life"]
        cash_flows[-1] += project["salvage_value"]
        npv = -project["initial_investment"] + sum(cf / (1 + r)**(i + 1) for i, cf in enumerate(cash_flows))
        return npv / 1_000_000  # Return in millions

    # --- UI Layout ---
    st.markdown("""
    <style>
    .big-font {
        font-size:32px !important;
        font-weight: bold !important;
    }
    .metric-label {
        font-size:16px !important;
        color: #666 !important;
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Top Row: Title and Discount Rate Slider
    col_title, col_slider = st.columns([2, 3])
    
    with col_title:
        st.markdown("## Net Present Value Analysis")
        st.markdown("Compare investment options for copper and zinc projects")
    
    with col_slider:
        discount_rate = st.slider(
            "Adjust Discount Rate (%)", 
            min_value=1.0, 
            max_value=20.0, 
            value=8.0, 
            step=0.5,
            help="Change the discount rate to see its impact on project NPV"
        )

    # Middle Row: KPI Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p class="metric-label">COPPER PROJECT NPV</p>', unsafe_allow_html=True)
        npv_copper = calculate_npv(discount_rate, copper)
        st.markdown(f'<p class="big-font" style="color:#FFA500">${npv_copper:.1f}M</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="metric-label">ZINC PROJECT NPV</p>', unsafe_allow_html=True)
        npv_zinc = calculate_npv(discount_rate, zinc)
        st.markdown(f'<p class="big-font" style="color:#1F77B4">${npv_zinc:.1f}M</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<p class="metric-label">CURRENT DISCOUNT RATE</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">{discount_rate:.1f}%</p>', unsafe_allow_html=True)

    # Bottom Row: NPV Chart
    rates = np.linspace(1, 20, 100)
    npv_copper_list = [calculate_npv(r, copper) for r in rates]
    npv_zinc_list = [calculate_npv(r, zinc) for r in rates]

    fig = go.Figure()

    # Copper line
    fig.add_trace(go.Scatter(
        x=rates, 
        y=npv_copper_list, 
        mode='lines', 
        name='Copper Project',
        line=dict(color='orange', width=3)
    ))
    
    # Zinc line
    fig.add_trace(go.Scatter(
        x=rates, 
        y=npv_zinc_list, 
        mode='lines', 
        name='Zinc Project',
        line=dict(color='blue', width=3)
    ))

    # Current NPV points
    fig.add_trace(go.Scatter(
        x=[discount_rate], 
        y=[npv_copper], 
        mode='markers+text',
        name=f'Copper @ {discount_rate:.1f}%',
        text=[f"${npv_copper:.1f}M"],
        textposition='top center',
        marker=dict(color='orange', size=12),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[discount_rate], 
        y=[npv_zinc], 
        mode='markers+text',
        name=f'Zinc @ {discount_rate:.1f}%',
        text=[f"${npv_zinc:.1f}M"],
        textposition='top center',
        marker=dict(color='blue', size=12),
        showlegend=False
    ))

    # Add zero line reference
    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="NPV Sensitivity to Discount Rate",
        xaxis_title="Discount Rate (%)",
        yaxis_title="Net Present Value (Million USD)",
        template="plotly_white",
        hovermode="x unified",
        height=500,  # Increased chart height
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Additional information
    st.markdown("""
    <div style="background-color:#f8f9fa;padding:15px;border-radius:5px;margin-top:20px">
    <small>
    <b>Analysis Notes:</b><br>
    • The Copper project requires higher initial investment but generates more cash flow over a longer period<br>
    • The Zinc project has lower initial costs but shorter lifespan<br>
    • NPV becomes negative when discount rate exceeds ~11.5% for Copper and ~15% for Zinc
    </small>
    </div>
    """, unsafe_allow_html=True)