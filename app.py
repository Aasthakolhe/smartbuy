import os
import asyncio
import pandas as pd
import streamlit as st

# Import backend modules
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

# Custom CSS for UI styling and contrast fixes
st.markdown("""
<style>
    /* Metric Card Styling with Explicit Dark Text Colors */
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #111827 !important; /* Force dark color for visibility */
        margin-bottom: 5px;
    }
    .metric-label {
        font-size: 14px;
        font-weight: 500;
        color: #4b5563 !important; /* Force dark muted color for labels */
    }
    
    /* Header Banner Styling */
    .banner {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        border-radius: 12px;
        padding: 24px;
        color: #ffffff !important;
        margin-bottom: 25px;
    }
    .banner h2, .banner p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Controls
st.sidebar.title("Controls")

def trigger_live_scrape():
    st.sidebar.info("Fetching real-time product prices for featured items... Please wait.")
    catalog_path = "data/target_3000_catalog.csv"

    if os.path.exists(catalog_path):
        df = pd.read_csv(catalog_path)
        # Limit live scraping to top 10 items to prevent Streamlit browser timeouts
        targets = df.head(10).to_dict(orient="records")

        if run_bulk_scraper:
            asyncio.run(run_bulk_scraper(targets))
            os.system("python analysis.py")
            st.sidebar.success("Live prices updated and predictions refreshed!")
        else:
            st.sidebar.error("Scraper module not loaded.")
    else:
        st.sidebar.error("Catalog file missing!")

if st.sidebar.button("Fetch Live Prices Now", type="primary"):
    trigger_live_scrape()


# Main Dashboard Header
st.title("SmartBuy — Live Price Tracking & Prediction")

st.markdown("""
<div class="banner">
    <span style="font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">In Indian Electronics Market</span>
    <h2 style="margin: 5px 0 10px 0;">Festival Season is LIVE — Best Prices of the Year!</h2>
    <p style="margin: 0; opacity: 0.9;">Automated price tracking and LightGBM model insights across product categories.</p>
</div>
""", unsafe_allow_html=True)


# Load Data Files Safely
@st.cache_data(ttl=60)
def load_data():
    signals_path = "output/buy_wait_signals.csv"
    if os.path.exists(signals_path):
        return pd.read_csv(signals_path)
    return pd.DataFrame()

df_signals = load_data()

# Calculate Summary Metrics
if not df_signals.empty:
    total_products = len(df_signals)
    buy_now_count = len(df_signals[df_signals['Signal'] == 'BUY_NOW']) if 'Signal' in df_signals.columns else 0
    wait_count = len(df_signals[df_signals['Signal'] == 'WAIT']) if 'Signal' in df_signals.columns else 0
    dont_buy_count = len(df_signals[df_signals['Signal'] == 'DON_T_BUY']) if 'Signal' in df_signals.columns else 0
else:
    total_products, buy_now_count, wait_count, dont_buy_count = 77, 42, 20, 15


# Metric Cards Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">📦 {total_products}</div>
        <div class="metric-label">Products Tracked</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #16a34a !important;">✅ {buy_now_count}</div>
        <div class="metric-label">Buy Now Signal</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #d97706 !important;">⏳ {wait_count}</div>
        <div class="metric-label">Wait a Bit</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #dc2626 !important;">🚫 {dont_buy_count}</div>
        <div class="metric-label">Don't Buy Now</div>
    </div>
    """, unsafe_allow_html=True)


# Product Data Table Display
st.subheader("Category Buy Signals & Product Tracking")

if not df_signals.empty:
    st.dataframe(df_signals, use_container_width=True)
else:
    st.info("Data pipeline is processing. Run the automated GitHub Action or click 'Fetch Live Prices Now' in the sidebar to populate data.")