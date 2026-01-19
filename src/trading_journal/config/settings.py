from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AppSettings:
    title: str = "Trading Journal Dashboard"
    subtitle: str = "Performance • Riesgo • Eficiencia • ETD • Comisiones"
    cache_ttl_seconds: int = 600  # 10 minutes

SETTINGS = AppSettings()
