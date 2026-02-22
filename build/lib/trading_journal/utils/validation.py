from __future__ import annotations
import pandas as pd

REQUIRED_COLS_MIN = {"Profit", "Exit time"}

def validate_minimum_schema(df: pd.DataFrame) -> tuple[bool, str]:
    missing = [c for c in REQUIRED_COLS_MIN if c not in df.columns]
    if missing:
        return False, f"Faltan columnas mínimas requeridas: {missing}"
    if df.empty:
        return False, "El dataset está vacío."
    return True, "OK"
