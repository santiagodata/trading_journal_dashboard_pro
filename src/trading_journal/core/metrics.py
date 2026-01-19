from __future__ import annotations

import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    if equity is None or equity.empty:
        return 0.0
    running_max = equity.cummax()
    dd = equity - running_max
    return float(dd.min())


def summarize_kpis(df: pd.DataFrame) -> dict:
    """
    KPIs coherentes con NinjaTrader:

    - Profit (CSV) ya es NETO (fees descontados). No volver a restar fees.
    - Cum. net profit (si existe) es la curva acumulada neta real (source of truth).
    """
    out: dict[str, float | int] = {}

    out["total_trades"] = int(len(df))

    # Profit neto (ya after fees)
    if "Profit" in df.columns:
        out["net_pnl"] = float(df["Profit"].sum())
        out["avg_trade"] = float(df["Profit"].mean())
        out["best_trade"] = float(df["Profit"].max())
        out["worst_trade"] = float(df["Profit"].min())
        out["win_rate"] = float((df["Profit"] > 0).mean() * 100)
    else:
        out["net_pnl"] = 0.0
        out["avg_trade"] = np.nan
        out["best_trade"] = np.nan
        out["worst_trade"] = np.nan
        out["win_rate"] = np.nan

    # Comisión (si existe)
    out["total_commission"] = float(df["Commission"].sum()) if "Commission" in df.columns else np.nan
    out["avg_commission"] = float(df["Commission"].mean()) if "Commission" in df.columns else np.nan

    # MAE/MFE/ETD
    out["avg_mae"] = float(df["MAE"].mean()) if "MAE" in df.columns else np.nan
    out["avg_mfe"] = float(df["MFE"].mean()) if "MFE" in df.columns else np.nan
    out["avg_etd"] = float(df["ETD"].mean()) if "ETD" in df.columns else np.nan
    out["median_etd"] = float(df["ETD"].median()) if "ETD" in df.columns else np.nan

    # Fees totales (si existe la columna derivada)
    out["total_fees"] = float(df["Total Fees"].sum()) if "Total Fees" in df.columns else np.nan

    # Net after fees = Profit (porque ya viene after fees)
    out["net_after_fees"] = out["net_pnl"]

    # Equity + Drawdown: preferir Cum. net profit si existe
    if "Cum. net profit" in df.columns and df["Cum. net profit"].notna().any():
        equity = df["Cum. net profit"]
    elif "Profit" in df.columns:
        equity = df["Profit"].cumsum()
    else:
        equity = pd.Series(dtype=float)

    out["max_drawdown"] = max_drawdown(equity)

    # Optional: gross total estimado (si existe en loader)
    out["gross_pnl_est"] = float(df["Gross Profit (before fees)"].sum()) if "Gross Profit (before fees)" in df.columns else np.nan

    return out
