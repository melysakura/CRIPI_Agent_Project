"""Entry point for the multipage CRIPI Streamlit dashboard."""

import streamlit as st

st.set_page_config(
    page_title="CRIPI Climate Resilience Dashboard",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

page = st.navigation(
    [
        st.Page("pages/0_CRIPI_Explained.py", title="CRIPI Explained", icon="📘"),
        st.Page("pages/1_CRIPI_Dashboard.py", title="CRIPI Dashboard", icon="📊"),
        st.Page("pages/2_State_Clusters.py", title="State Clusters", icon="🧩"),
        st.Page("pages/3_CRIPI_Assistant.py", title="CRIPI Assistant", icon="💬"),
    ]
)
page.run()
