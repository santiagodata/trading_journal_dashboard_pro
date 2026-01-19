from __future__ import annotations
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from trading_journal.core import add_period_column

def render_overview(df: pd.DataFrame, agg_mode: str = "Diario"):
    c1, c2 = st.columns([1.6, 1.0], gap="large")

    if "Profit" in df.columns:
        eq = df[["Exit time", "Profit"]].copy()
        eq = eq.sort_values("Exit time") if "Exit time" in eq.columns else eq
        eq["Equity"] = eq["Profit"].cumsum()

        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(x=list(range(1, len(eq)+1)), y=eq["Equity"], mode="lines", name="Equity"))
        fig_eq.update_layout(title="Curva de Equity (gross)", xaxis_title="Trade #", yaxis_title="USD",
                             margin=dict(l=10, r=10, t=45, b=10), height=360)
        c1.plotly_chart(fig_eq, use_container_width=True)

        fig_hist = px.histogram(df, x="Profit", nbins=25, title="Distribución de PnL por trade (gross)")
        fig_hist.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=360)
        c2.plotly_chart(fig_hist, use_container_width=True)

    c3, c4 = st.columns([1.0, 1.0], gap="large")
    if "Profit" in df.columns:
        tmp = df.sort_values("Exit time") if "Exit time" in df.columns else df.copy()
        tmp["Trade # (seq)"] = range(1, len(tmp) + 1)
        fig_bar = px.bar(tmp, x="Trade # (seq)", y="Profit", title="PnL por trade (gross)")
        fig_bar.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=360)
        c3.plotly_chart(fig_bar, use_container_width=True)

    if "Date" in df.columns and "Profit" in df.columns:
        tmp = add_period_column(df, agg_mode)
        grp = tmp.groupby("Period", as_index=False)["Profit"].sum()
        title = f"PnL ({agg_mode.lower()})"
        fig_day = px.bar(grp, x="Period", y="Profit", title=title)
        fig_day.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=360)
        c4.plotly_chart(fig_day, use_container_width=True)
