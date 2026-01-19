from __future__ import annotations

import io
import pandas as pd
import numpy as np

from trading_journal.config import MONEY_COLS, FEE_COLS, SETTINGS
from trading_journal.data.parsers import parse_money_es_co
from trading_journal.utils.cache import cache_data


@cache_data(ttl=SETTINGS.cache_ttl_seconds)
def load_nt_csv_cached(file_bytes: bytes) -> pd.DataFrame:
    return load_nt_csv(file_bytes)


def _normalize_datetime_series(s: pd.Series) -> pd.Series:
    """
    NinjaTrader en es-CO puede exportar AM/PM como 'a. m.' o 'a m' (y con NBSP).
    Esto normaliza a 'AM'/'PM' para que pandas lo parsee.
    """
    ss = s.astype(str)

    # NBSP -> space (muy común al copiar/guardar en Windows)
    ss = ss.str.replace("\u00a0", " ", regex=False)

    # Normalizar variantes comunes
    replacements = [
        ("a. m.", "AM"),
        ("p. m.", "PM"),
        ("a.m.", "AM"),
        ("p.m.", "PM"),
        (" a m", " AM"),
        (" p m", " PM"),
        (" am", " AM"),
        (" pm", " PM"),
    ]
    for old, new in replacements:
        ss = ss.str.replace(old, new, regex=False)

    return ss


def _parse_price_series(s: pd.Series) -> pd.Series:
    """
    Precios suelen venir como '25880,25' (coma decimal).
    Convertimos coma->punto y opcionalmente removemos miles con punto.
    """
    ss = s.astype(str).str.replace("\u00a0", " ", regex=False).str.strip()
    ss = ss.str.replace(" ", "", regex=False)

    # Si alguna vez vienen miles con punto, lo removemos.
    # (Si estás 100% seguro de que nunca hay miles, puedes quitar esta línea)
    ss = ss.str.replace(".", "", regex=False)

    # Decimal coma -> punto
    ss = ss.str.replace(",", ".", regex=False)

    return pd.to_numeric(ss, errors="coerce")


def load_nt_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Load NinjaTrader grid CSV (semicolon-separated) and return cleaned DataFrame.

    IMPORTANT:
    - En tu CSV, 'Profit' ya viene NETO (fees descontados por NinjaTrader).
    - 'Cum. net profit' es la curva acumulada neta real de NinjaTrader.
    """
    df = pd.read_csv(io.BytesIO(file_bytes), sep=";", engine="python")
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]

    # ---- Datetimes ----
    for col in ["Entry time", "Exit time"]:
        if col in df.columns:
            norm = _normalize_datetime_series(df[col])
            df[col] = pd.to_datetime(norm, dayfirst=True, errors="coerce")

    # ---- Prices ----
    for col in ["Entry price", "Exit price"]:
        if col in df.columns:
            df[col] = _parse_price_series(df[col])

    # ---- Money cols ----
    for col in MONEY_COLS:
        if col in df.columns:
            df[col] = df[col].apply(parse_money_es_co)

    # ---- Derived fields ----
    if "Profit" in df.columns:
        df["Result"] = np.where(df["Profit"] > 0, "Win", np.where(df["Profit"] < 0, "Loss", "BE"))

    if "Exit time" in df.columns:
        df["Date"] = df["Exit time"].dt.date
        df["DOW"] = df["Exit time"].dt.day_name()
        df["Hour"] = df["Exit time"].dt.hour

    # Total fees (si existen)
    fee_cols = [c for c in FEE_COLS if c in df.columns]
    df["Total Fees"] = df[fee_cols].sum(axis=1, min_count=1) if fee_cols else np.nan

    # Profit ya es NETO. NO recalcular "after fees".
    # Si queremos una referencia de "gross", lo estimamos así:
    if "Profit" in df.columns:
        df["Gross Profit (before fees)"] = df["Profit"] + df["Total Fees"].fillna(0)

    return df
