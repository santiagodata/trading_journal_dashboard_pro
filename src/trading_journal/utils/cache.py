from __future__ import annotations
import streamlit as st

def cache_data(ttl: int):
    """Wrapper to keep caching centralized."""
    return st.cache_data(ttl=ttl, show_spinner=False)
