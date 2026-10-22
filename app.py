import os
import asyncio
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Import backend modules safely
try:
    from bulk_scraper import run_bulk_scraper
except ImportError:
    run_bulk_scraper = None

# Configure page layout
st.set_page_config(
    page_title="SmartBuy — Buy Smart. Buy Right.",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling to clean up padding around iframe
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls for On-Demand Scraping
st.sidebar.title("SmartBuy Controls")

def trigger_live_scrape():
    st.sidebar.info("Fetching real-time product prices... Please wait.")
    catalog_path = "data/target_3000_catalog.csv"

    if os.path.exists(catalog_path):
        df = pd.read_csv(catalog_path)
        # Limit to top 15 items for quick cloud fetching
        targets = df.head(15).to_dict(orient="records")

        if run_bulk_scraper:
            asyncio.run(run_bulk_scraper(targets))
            os.system("python analysis.py")
            st.sidebar.success("Live prices updated! Refreshing view...")
            st.rerun()
        else:
            st.sidebar.error("Scraper module not found.")
    else:
        st.sidebar.error("Catalog file missing!")

if st.sidebar.button("🔄 Fetch Live Prices Now", type="primary"):
    trigger_live_scrape()

# Read and render index.html
html_file_path = "index.html"

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Render exact index.html template
    components.html(html_content, height=1200, scrolling=True)
else:
    st.error("index.html not found in project root directory.")