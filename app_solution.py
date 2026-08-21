"""Bootcamp entry point that loads the CRIPI Dashboard page."""

import importlib.util
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="CRIPI Dashboard",
    page_icon=":material/public:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page_path = Path(__file__).parent / "pages" / "1_CRIPI_Dashboard.py"
spec = importlib.util.spec_from_file_location("investment_priorities", page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
