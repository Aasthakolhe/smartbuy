import os
import streamlit as st
import streamlit.components.v1 as components

# Configure page layout to wide mode and full height
st.set_page_config(
    page_title="SmartBuy — Buy Smart. Buy Right.",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header padding and default margins
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Read and render index.html
html_file_path = "index.html"

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Render the exact index.html page full-screen inside Streamlit
    components.html(html_content, height=1200, scrolling=True)
else:
    st.error("index.html not found in project root directory.")