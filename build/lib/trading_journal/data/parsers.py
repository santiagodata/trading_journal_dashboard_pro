from __future__ import annotations
import re
import numpy as np

def parse_money_es_co(x) -> float:
    """Parse currency strings like '$ 1.234,56', '- 2,90', '-$108,40' into float."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return np.nan
    s = s.replace("$", "").replace(" ", "")
    s = s.replace("−", "-")  # unicode minus
    # thousands '.' and decimal ','
    s = s.replace(".", "").replace(",", ".")
    s = re.sub(r"[^0-9\.\-]", "", s)
    try:
        return float(s)
    except Exception:
        return np.nan
