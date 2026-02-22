from __future__ import annotations
import pandas as pd

def add_period_column(df: pd.DataFrame, agg_mode: str) -> pd.DataFrame:
    """
    Crea una columna 'Period' para agrupar series temporales.
    - Diario: Date
    - Semanal: semana ISO (inicio lunes)
    - Mensual: YYYY-MM
    """
    out = df.copy()

    if "Exit time" not in out.columns or out["Exit time"].isna().all():
        out["Period"] = None
        return out

    dt = out["Exit time"]

    if agg_mode == "Mensual":
        out["Period"] = dt.dt.to_period("M").astype(str)  # "2026-01"
    elif agg_mode == "Semanal":
        # ISO week: "YYYY-Www"
        iso = dt.dt.isocalendar()
        out["Period"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
    else:
        # Diario
        out["Period"] = dt.dt.date

    return out
