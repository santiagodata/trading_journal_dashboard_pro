from __future__ import annotations
import streamlit as st

def apply_global_styles():
    css = """
    <style>
    :root {
      --card: rgba(255,255,255,0.06);
      --text: rgba(255,255,255,0.92);
      --muted: rgba(255,255,255,0.65);
      --good: #22c55e;
      --bad: #ef4444;
      --warn: #f59e0b;
    }
    .stApp {
      background: radial-gradient(1200px 900px at 25% 10%, rgba(110,231,255,0.18), transparent 60%),
                  radial-gradient(900px 700px at 85% 20%, rgba(34,197,94,0.10), transparent 55%),
                  radial-gradient(800px 800px at 55% 95%, rgba(239,68,68,0.10), transparent 55%),
                  linear-gradient(180deg, #070b14 0%, #0b1220 55%, #070b14 100%);
      color: var(--text);
    }
    section[data-testid="stSidebar"] {
      background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
      border-right: 1px solid rgba(255,255,255,0.08);
    }
    .kpi {
      background: var(--card);
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 18px;
      padding: 14px 14px 12px 14px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    .kpi .label { font-size: 12px; color: var(--muted); letter-spacing: 0.3px; }
    .kpi .value { font-size: 28px; font-weight: 800; margin-top: 6px; }
    .kpi .sub { font-size: 12px; color: var(--muted); margin-top: 6px; }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.06);
    }
    .badge.good { color: var(--good); }
    .badge.bad { color: var(--bad); }
    .badge.warn { color: var(--warn); }
    div[data-testid="stPlotlyChart"] > div {
      background: rgba(255,255,255,0.03) !important;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 18px;
      padding: 10px;
    }
    div[data-testid="stDataFrame"] {
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 18px;
      overflow: hidden;
    }
    .small-note { color: var(--muted); font-size: 12px; }
    hr { border: none; height: 1px; background: rgba(255,255,255,0.10); margin: 10px 0 18px 0; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
