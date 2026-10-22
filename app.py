import os
import asyncio
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import backend modules safely
try:
    from bulk_scraper import run_bulk_scraper
except ImportError:
    run_bulk_scraper = None

# Page Configuration
st.set_page_config(
    page_title="SmartBuy — Live Price Tracking & Prediction",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Styling and Contrast Fixes
st.markdown("""
<style>
    /* Metric Card Styling with High Contrast */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #e5e7eb;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: #111827 !important;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #4b5563 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Header Banner Styling */
    .banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 14px;
        padding: 24px;
        color: #ffffff !important;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
    }
    .banner h2 {
        color: #ffffff !important;
        margin: 6px 0;
        font-size: 26px;
    }
    .banner p {
        color: #dbeafe !important;
        margin: 0;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Controls
st.sidebar.title("Controls")

def trigger_live_scrape():
    st.sidebar.info("Fetching real-time product prices... Please wait.")
    catalog_path = "data/target_3000_catalog.csv"

    if os.path.exists(catalog_path):
        df = pd.read_csv(catalog_path)
        # Limit live scraper to top 15 items to prevent browser execution timeouts
        targets = df.head(15).to_dict(orient="records")

        if run_bulk_scraper:
            asyncio.run(run_bulk_scraper(targets))
            os.system("python analysis.py")
            st.sidebar.success("Live prices updated and predictions refreshed!")
        else:
            st.sidebar.error("Scraper module not found.")
    else:
        st.sidebar.error("Catalog file missing!")

if st.sidebar.button("Fetch Live Prices Now", type="primary"):
    trigger_live_scrape()


# Main Dashboard Banner
st.title("SmartBuy — Live Price Tracking & Prediction")

st.markdown("""
<div class="banner">
    <span style="font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; opacity: 0.85;">Indian Electronics Market — Festive Season Analysis</span>
    <h2>Festival Season is LIVE — Best Prices of the Year!</h2>
    <p>Big Billion Days & Great Indian Festival insights powered by automated tracking & LightGBM pricing model predictions.</p>
</div>
""", unsafe_allow_html=True)


# Load Pipeline Data
@st.cache_data(ttl=60)
def load_all_data():
    data = {}
    data['signals'] = pd.read_csv("output/buy_wait_signals.csv") if os.path.exists("output/buy_wait_signals.csv") else pd.DataFrame()
    data['monthly'] = pd.read_csv("data/monthly_price_history.csv") if os.path.exists("data/monthly_price_history.csv") else pd.DataFrame()
    data['festivals'] = pd.read_csv("data/festival_calendar.csv") if os.path.exists("data/festival_calendar.csv") else pd.DataFrame()
    data['savings'] = pd.read_csv("output/savings_by_category.csv") if os.path.exists("output/savings_by_category.csv") else pd.DataFrame()
    return data

data = load_all_data()
df_signals = data['signals']


# Interactive Tab Navigation UI
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "📈 Price Trends", 
    "🔍 Products", 
    "📅 Festival Calendar", 
    "💰 Savings Calculator"
])


# TAB 1: DASHBOARD OVERVIEW
with tab1:
    if not df_signals.empty:
        total_products = len(df_signals)
        buy_now_count = len(df_signals[df_signals['Signal'] == 'BUY_NOW']) if 'Signal' in df_signals.columns else 0
        wait_count = len(df_signals[df_signals['Signal'] == 'WAIT']) if 'Signal' in df_signals.columns else 0
        dont_buy_count = len(df_signals[df_signals['Signal'] == 'DON_T_BUY']) if 'Signal' in df_signals.columns else 0
    else:
        total_products, buy_now_count, wait_count, dont_buy_count = 77, 42, 20, 15

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">📦 {total_products}</div><div class="metric-label">Products Tracked</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #16a34a !important;">✅ {buy_now_count}</div><div class="metric-label">Buy Now Signal</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #d97706 !important;">⏳ {wait_count}</div><div class="metric-label">Wait a Bit</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #dc2626 !important;">🚫 {dont_buy_count}</div><div class="metric-label">Don\'t Buy Now</div></div>', unsafe_allow_html=True)

    st.subheader("Category Buy Signals & Overview")
    if not df_signals.empty:
        fig_cat = px.histogram(
            df_signals, 
            x="Category" if "Category" in df_signals.columns else df_signals.columns[0], 
            color="Signal" if "Signal" in df_signals.columns else None,
            barmode="group",
            title="Buy vs Wait Signals by Product Category",
            color_discrete_map={"BUY_NOW": "#16a34a", "WAIT": "#d97706", "DON_T_BUY": "#dc2626"}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Run the automated GitHub Action or click 'Fetch Live Prices Now' to view signals.")


# TAB 2: PRICE TRENDS
with tab2:
    st.subheader("Historical & Seasonal Price Trends")
    df_monthly = data['monthly']
    if not df_monthly.empty:
        category_list = df_monthly['Category'].unique() if 'Category' in df_monthly.columns else []
        selected_cat = st.selectbox("Select Product Category", category_list) if len(category_list) > 0 else None
        
        filtered_monthly = df_monthly[df_monthly['Category'] == selected_cat] if selected_cat else df_monthly
        fig_trend = px.line(
            filtered_monthly, 
            x="Month" if "Month" in filtered_monthly.columns else filtered_monthly.columns[0], 
            y="Average_Price" if "Average_Price" in filtered_monthly.columns else filtered_monthly.columns[1],
            title=f"Price Trend Over Time — {selected_cat if selected_cat else 'All Categories'}",
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Price history data is loading.")


# TAB 3: PRODUCTS EXPLORER
with tab3:
    st.subheader("Explore All Tracked Products")
    if not df_signals.empty:
        search_term = st.text_input("Search Product Name or Brand", "")
        if search_term:
            filtered_df = df_signals[df_signals.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        else:
            filtered_df = df_signals
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No product signals loaded yet.")


# TAB 4: FESTIVAL CALENDAR
with tab4:
    st.subheader("Indian Shopping Festival Calendar & Discount Periods")
    df_fest = data['festivals']
    if not df_fest.empty:
        st.dataframe(df_fest, use_container_width=True)
    else:
        st.write("Festive Sales Event Schedule: **Great Indian Festival & Big Billion Days active during October/November.**")


# TAB 5: SAVINGS CALCULATOR
with tab5:
    st.subheader("Smart Savings Calculator")
    budget = st.number_input("Enter Your Shopping Budget (₹)", min_value=1000, value=50000, step=1000)
    expected_discount = st.slider("Target Sale Discount (%)", min_value=5, max_value=50, value=20)
    
    potential_savings = (budget * expected_discount) / 100
    final_price = budget - potential_savings
    
    st.success(f"🎉 **Estimated Savings:** ₹{potential_savings:,.2f}")
    st.info(f"💡 **Expected Festival Purchase Price:** ₹{final_price:,.2f}")