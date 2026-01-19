from __future__ import annotations
import streamlit as st

from trading_journal.config import SETTINGS
from trading_journal.data import load_nt_csv_cached
from trading_journal.ui import apply_global_styles, sidebar_uploader, sidebar_filters
from trading_journal.core import apply_filters
from trading_journal.utils import validate_minimum_schema
from trading_journal.ui.kpis import render_kpis
from trading_journal.features import render_overview, render_risk, render_costs, render_trades

st.set_page_config(
    page_title=SETTINGS.title,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

st.markdown(f"# {SETTINGS.title}")
st.markdown(f'<div class="small-note">{SETTINGS.subtitle}</div>', unsafe_allow_html=True)
st.markdown("<hr/>", unsafe_allow_html=True)

file_bytes = sidebar_uploader()
if not file_bytes:
    st.info("Sube tu CSV de NinjaTrader para ver el dashboard.")
    st.stop()

df = load_nt_csv_cached(file_bytes)

ok, msg = validate_minimum_schema(df)   # ✅ sin agg_mode
if not ok:
    st.error(msg)
    st.stop()

filters = sidebar_filters(df)           # ✅ aquí se define filters
fdf = apply_filters(df, filters)

if fdf.empty:
    st.warning("Con esos filtros no quedan trades. Ajusta los filtros.")
    st.stop()

render_kpis(fdf)  # ✅ sin agg_mode

tab_overview, tab_risk, tab_costs, tab_trades = st.tabs(
    ["📈 Overview", "🧠 Riesgo & Eficiencia", "💸 Costos (Fees + ETD)", "🧾 Trades"]
)

with tab_overview:
    render_overview(fdf, agg_mode=filters.agg_mode)

with tab_risk:
    render_risk(fdf)

with tab_costs:
    render_costs(fdf, agg_mode=filters.agg_mode)

with tab_trades:
    render_trades(fdf)  # ✅ tabla no necesita agg_mode

st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">Export recomendado: NinjaTrader → Performance → Trades → Grid → Save As (CSV).</div>',
    unsafe_allow_html=True,
)
