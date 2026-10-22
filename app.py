import os
import asyncio
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Import backend scraper safely
try:
    from bulk_scraper import run_bulk_scraper
except ImportError:
    run_bulk_scraper = None

# Configure page layout and keep sidebar open by default
st.set_page_config(
    page_title="SmartBuy — Buy Smart. Buy Right.",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ SmartBuy Controls")
st.sidebar.write("Trigger manual price updates and LightGBM model analysis.")

def trigger_live_scrape():
    st.sidebar.info("Fetching real-time prices... Please wait.")
    catalog_path = "data/target_3000_catalog.csv"

    if os.path.exists(catalog_path):
        df = pd.read_csv(catalog_path)
        targets = df.head(15).to_dict(orient="records")

        if run_bulk_scraper:
            asyncio.run(run_bulk_scraper(targets))
            os.system("python analysis.py")
            st.sidebar.success("Prices updated successfully!")
            st.rerun()
        else:
            st.sidebar.error("Scraper module not loaded.")
    else:
        st.sidebar.error("Catalog file missing!")

if st.sidebar.button("🔄 Fetch Live Prices Now", type="primary", use_container_width=True):
    trigger_live_scrape()


# --- DATA & HTML RENDER ---
def get_signal_count(df, target_signal):
    if df.empty:
        return 0
    signal_col = None
    for col in ['Signal', 'signal', 'Buy_Signal', 'buy_signal', 'Recommendation']:
        if col in df.columns:
            signal_col = col
            break
    if signal_col:
        return len(df[df[signal_col].astype(str).str.upper() == target_signal.upper()])
    return 0

signals_path = "output/buy_wait_signals.csv"
if os.path.exists(signals_path):
    df_signals = pd.read_csv(signals_path)
    total_count = len(df_signals)
    buy_count = get_signal_count(df_signals, 'BUY_NOW')
    wait_count = get_signal_count(df_signals, 'WAIT')
    dont_buy_count = get_signal_count(df_signals, 'DON_T_BUY')
else:
    total_count, buy_count, wait_count, dont_buy_count = 77, 8, 67, 2

# Read index.html and inject live counts
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    html_content = html_content.replace('id="tracked-count">77', f'id="tracked-count">{total_count}')
    html_content = html_content.replace('id="buy-count">8', f'id="buy-count">{buy_count}')
    
    components.html(html_content, height=1200, scrolling=True)
else:
    st.error("index.html not found in repository root.")