from __future__ import annotations
import streamlit as st
import pandas as pd
from trading_journal.core import Filters

def sidebar_uploader() -> bytes | None:
    st.sidebar.markdown("## 📥 Data")
    uploaded = st.sidebar.file_uploader("Cargar export de NinjaTrader (CSV Grid)", type=["csv"])
    st.sidebar.markdown("## 🎛️ Filtros")
    if not uploaded:
        return None
    return uploaded.getvalue()

def sidebar_filters(df: pd.DataFrame) -> Filters:
    with st.sidebar:
        accounts = sorted(df["Account"].dropna().unique().tolist()) if "Account" in df.columns else []
        instruments = sorted(df["Instrument"].dropna().unique().tolist()) if "Instrument" in df.columns else []
        positions = sorted(df["Market pos."].dropna().unique().tolist()) if "Market pos." in df.columns else []

        sel_accounts = st.multiselect("Cuenta", accounts, default=accounts) if accounts else None
        sel_instruments = st.multiselect("Instrumento", instruments, default=instruments) if instruments else None
        sel_positions = st.multiselect("Market position", positions, default=positions) if positions else None

        qty_range = None
        if "Qty" in df.columns and len(df) > 0:
            qty_min, qty_max = int(df["Qty"].min()), int(df["Qty"].max())
            qty_range = st.slider("Rango de Qty", min_value=qty_min, max_value=qty_max, value=(qty_min, qty_max))

        d1, d2 = None, None
        if "Exit time" in df.columns and df["Exit time"].notna().any():
            min_dt = df["Exit time"].min().date()
            max_dt = df["Exit time"].max().date()
            d1 = st.date_input("Desde", value=min_dt)
            d2 = st.date_input("Hasta", value=max_dt)

        agg_mode = st.selectbox(
            "Agrupar series por",
            options=["Diario", "Semanal", "Mensual"],
            index=0,
        )

    return Filters(
        accounts=sel_accounts,
        instruments=sel_instruments,
        positions=sel_positions,
        qty_range=qty_range,
        date_from=d1,
        date_to=d2,
        agg_mode=agg_mode,
    )
