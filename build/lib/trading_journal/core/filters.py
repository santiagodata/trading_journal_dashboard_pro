from __future__ import annotations
import pandas as pd
from dataclasses import dataclass
from datetime import date

@dataclass
class Filters:
    accounts: list[str] | None = None
    instruments: list[str] | None = None
    positions: list[str] | None = None
    qty_range: tuple[int, int] | None = None
    date_from: date | None = None
    date_to: date | None = None
    agg_mode: str = "Diario"

def apply_filters(df: pd.DataFrame, f: Filters) -> pd.DataFrame:
    out = df.copy()

    if f.accounts and "Account" in out.columns:
        out = out[out["Account"].isin(f.accounts)]
    if f.instruments and "Instrument" in out.columns:
        out = out[out["Instrument"].isin(f.instruments)]
    if f.positions and "Market pos." in out.columns:
        out = out[out["Market pos."].isin(f.positions)]
    if f.qty_range and "Qty" in out.columns:
        qmin, qmax = f.qty_range
        out = out[(out["Qty"] >= qmin) & (out["Qty"] <= qmax)]
    if f.date_from and f.date_to and "Exit time" in out.columns:
        out = out[(out["Exit time"].dt.date >= f.date_from) & (out["Exit time"].dt.date <= f.date_to)]

    return out
