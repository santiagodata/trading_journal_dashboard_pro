from __future__ import annotations
import numpy as np

def fmt_usd(x: float | int | None) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    sign = "-" if x < 0 else ""
    v = abs(float(x))
    return f"{sign}${v:,.2f}"
