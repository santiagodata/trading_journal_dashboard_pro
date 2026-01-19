from __future__ import annotations
import pandas as pd
import streamlit as st
from trading_journal.config import DEFAULT_TABLE_COLS

def render_trades(df: pd.DataFrame):
    st.markdown("### Trades (filtrados)")

    cols = [c for c in DEFAULT_TABLE_COLS if c in df.columns]
    table_df = df[cols].sort_values("Exit time") if "Exit time" in df.columns else df[cols]

    st.dataframe(table_df, use_container_width=True, height=520)

    csv_out = table_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar trades filtrados (CSV)", data=csv_out, file_name="trades_filtrados.csv", mime="text/csv")
