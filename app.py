import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SmartBuy — Buy Smart. Buy Right.", page_icon="🛒", layout="wide")

# Safe Column Filtering Helper
def get_signal_count(df, target_signal):
    if df.empty:
        return 0
    # Search across potential signal column names
    signal_col = None
    for col in ['Signal', 'signal', 'Buy_Signal', 'buy_signal', 'Recommendation']:
        if col in df.columns:
            signal_col = col
            break
    
    if signal_col:
        return len(df[df[signal_col].astype(str).str.upper() == target_signal.upper()])
    return 0

# Load pipeline dataset
signals_path = "output/buy_wait_signals.csv"
if os.path.exists(signals_path):
    df_signals = pd.read_csv(signals_path)
    total_count = len(df_signals)
    buy_count = get_signal_count(df_signals, 'BUY_NOW')
    wait_count = get_signal_count(df_signals, 'WAIT')
    dont_buy_count = get_signal_count(df_signals, 'DON_T_BUY')
else:
    total_count, buy_count, wait_count, dont_buy_count = 77, 8, 67, 2

# Render index.html dynamically
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Safely replace baseline metrics if markers exist
    html_content = html_content.replace('id="tracked-count">77', f'id="tracked-count">{total_count}')
    html_content = html_content.replace('id="buy-count">8', f'id="buy-count">{buy_count}')
    
    components.html(html_content, height=1200, scrolling=True)
else:
    st.error("index.html not found in repository root.")