from __future__ import annotations
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_risk(df: pd.DataFrame):
    r1, r2 = st.columns([1.1, 1.1], gap="large")

    if "MAE" in df.columns and "MFE" in df.columns:
        fig_sc = px.scatter(
            df,
            x="MAE",
            y="MFE",
            color=("Result" if "Result" in df.columns else None),
            size=(np.clip(df["Qty"], 1, 10) if "Qty" in df.columns else None),
            title="MAE vs MFE (USD)",
        )
        maxv = float(np.nanmax([df["MAE"].max(), df["MFE"].max()]))
        fig_sc.add_trace(go.Scatter(x=[0, maxv], y=[0, maxv], mode="lines", name="Diagonal (MFE=MAE)"))
        fig_sc.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=380)
        r1.plotly_chart(fig_sc, use_container_width=True)

    if "ETD" in df.columns:
        fig_etd = px.histogram(df, x="ETD", nbins=25, title="Distribución de ETD (USD)")
        fig_etd.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=380)
        r2.plotly_chart(fig_etd, use_container_width=True)

    if "DOW" in df.columns and "Hour" in df.columns and "Profit" in df.columns:
        piv = df.pivot_table(index="DOW", columns="Hour", values="Profit", aggfunc="sum").fillna(0)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        piv = piv.reindex([d for d in day_order if d in piv.index])
        fig_hm = px.imshow(piv, aspect="auto", title="Heatmap PnL: Día vs Hora (gross)")
        fig_hm.update_layout(margin=dict(l=10, r=10, t=45, b=10), height=420)
        st.plotly_chart(fig_hm, use_container_width=True)
