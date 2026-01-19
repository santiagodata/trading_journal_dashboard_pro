# Trading Journal Dashboard (PRO architecture)

Dashboard interactivo estilo *trading journal* para analizar performance, riesgo, eficiencia, **ETD** y **comisiones** usando un CSV exportado de NinjaTrader.

## ✅ Arquitectura
- `app/` → Streamlit entrypoints (main + pages)
- `src/trading_journal/` → paquete Python (modular y testeable)
  - `config/` → constantes, nombres de columnas, theme, settings
  - `data/` → loaders + parsers (CSV NinjaTrader)
  - `core/` → métricas (drawdown, ratios, agregaciones)
  - `features/` → módulos de UI/plots por feature (overview, risk, costs, trades)
  - `ui/` → estilos, componentes (KPI cards), sidebar, layout helpers
  - `utils/` → helpers (formatters, validation, caching wrappers)
- `tests/` → tests rápidos del parser de moneda

## ▶️ Ejecutar
```bash
pip install -r requirements.txt
pip install -e .
streamlit run app/main.py
```

## 📥 Export recomendado en NinjaTrader
Performance → Trades → Grid → Save As → CSV

## Notas
- Incluye parsing robusto de moneda tipo es-CO (`$ 1.234,56`, `- 2,90`, etc.)
- Incluye KPIs + tabs + tabla exportable
- Usa `st.cache_data` para acelerar carga en CSVs grandes
