import asyncio
import os
import pandas as pd
import streamlit as st
from bulk_scraper import run_bulk_scraper

# Page config
st.set_page_config(page_title="SmartBuy Platform", layout="wide")

st.title("SmartBuy — Live Price Tracking & Prediction")


# Function to handle live fetching
def trigger_live_scrape():
    st.info("Fetching real-time product prices... Please wait.")
    catalog_path = "data/target_3000_catalog.csv"

    if os.path.exists(catalog_path):
        targets = pd.read_csv(catalog_path).to_dict(orient="records")
        # Run async scraper on demand
        asyncio.run(run_bulk_scraper(targets))

        # Re-run ML analysis pipeline
        os.system("python analysis.py")
        st.success("Live prices updated and predictions refreshed!")
    else:
        st.error("Catalog file missing! Run build_3000_catalog.py first.")


# Sidebar trigger button
with st.sidebar:
    st.header("Controls")
    if st.button("Fetch Live Prices Now", type="primary"):
        trigger_live_scrape()

# Read and render index.html
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.html(html_content)
else:
    st.error("index.html not found.")