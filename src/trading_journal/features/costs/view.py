from __future__ import annotations
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from trading_journal.utils import fmt_usd
from trading_journal.core import add_period_column

def render_costs(df: pd.DataFrame, agg_mode: str = "Diario"):
    s1, s2 = st.columns([1.15, 1.0], gap="large")

    if "Commission" in df.columns:
        if "Date" in df.columns:
            tmp = add_period_column(df, agg_mode)
            comm_by_period = tmp.groupby("Period", as_index=False)["Commission"].sum()
            fig_comm = px.line(comm_by_period, x="Period", y="Commission", title=f"Comisión ({agg_mode.lower()})")
        else:
            fig_comm = px.histogram(df, x="Commission", nbins=25, title="Distribución de comisiones")
        fig_comm.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=360)
        s1.plotly_chart(fig_comm, use_container_width=True)

    if "Total Fees" in df.columns and "Profit" in df.columns:
        tmp = df.sort_values("Exit time") if "Exit time" in df.columns else df.copy()
        tmp["Trade # (seq)"] = range(1, len(tmp) + 1)
        fig_fee = go.Figure()
        fig_fee.add_trace(go.Bar(x=tmp["Trade # (seq)"], y=tmp["Total Fees"], name="Total fees"))
        fig_fee.add_trace(go.Scatter(x=tmp["Trade # (seq)"], y=tmp["Profit"], mode="lines", name="PnL (gross)"))
        fig_fee.update_layout(title="Fees vs PnL por trade", xaxis_title="Trade #", yaxis_title="USD",
                              margin=dict(l=10, r=10, t=45, b=10), height=360)
        s2.plotly_chart(fig_fee, use_container_width=True)

    st.markdown("### Resumen de costos")
    c1, c2, c3, c4 = st.columns(4, gap="large")
    avg_etd = float(df["ETD"].mean()) if "ETD" in df.columns else np.nan
    med_etd = float(df["ETD"].median()) if "ETD" in df.columns else np.nan
    total_fees = float(df["Total Fees"].sum()) if "Total Fees" in df.columns else np.nan
    net_after = float(df["Net Profit (after fees)"].sum()) if "Net Profit (after fees)" in df.columns else np.nan

    with c1: st.metric("ETD promedio", fmt_usd(avg_etd) if not np.isnan(avg_etd) else "—")
    with c2: st.metric("ETD mediana", fmt_usd(med_etd) if not np.isnan(med_etd) else "—")
    with c3: st.metric("Total fees", fmt_usd(total_fees) if not np.isnan(total_fees) else "—")
    with c4: st.metric("PnL after fees", fmt_usd(net_after) if not np.isnan(net_after) else "—")
