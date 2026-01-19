from __future__ import annotations
import numpy as np
import pandas as pd
import streamlit as st

from trading_journal.core import summarize_kpis
from trading_journal.ui.components import kpi_card
from trading_journal.utils import fmt_usd

def render_kpis(df: pd.DataFrame):
    k = summarize_kpis(df)

    k1, k2, k3, k4, k5, k6 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2, 1.2], gap="large")

    with k1:
        kpi_card("Trades", f"{k['total_trades']}", sub="Operaciones filtradas")

    with k2:
        net_pnl = k["net_pnl"]
        kpi_card(
            "PnL neto (gross)",
            fmt_usd(net_pnl),
            badge_text=("Good" if net_pnl >= 0 else "Bad"),
            badge_type=("good" if net_pnl >= 0 else "bad"),
        )

    with k3:
        wr = k["win_rate"]
        kpi_card("Win rate", f"{wr:,.2f}%" if not np.isnan(wr) else "—", sub="Wins/Total")

    with k4:
        kpi_card("PnL promedio", fmt_usd(k["avg_trade"]), sub="Por trade")

    with k5:
        tot_c = k["total_commission"]
        avg_c = k["avg_commission"]
        kpi_card("Comisiones total", fmt_usd(tot_c) if not np.isnan(tot_c) else "—",
                 sub=f"Prom: {fmt_usd(avg_c) if not np.isnan(avg_c) else '—'}")

    with k6:
        dd = k["max_drawdown"]
        kpi_card("Max drawdown", fmt_usd(dd), sub="Sobre equity", badge_text="Risk", badge_type="warn")

    st.markdown("<br/>", unsafe_allow_html=True)
