from __future__ import annotations
import streamlit as st

def kpi_card(label: str, value: str, sub: str | None = None, badge_text: str | None = None, badge_type: str | None = None):
    badge_html = ""
    if badge_text:
        klass = "badge"
        if badge_type in ("good", "bad", "warn"):
            klass += f" {badge_type}"
        badge_html = f'<span class="{klass}">{badge_text}</span>'
    sub_html = f'<div class="sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="kpi">
          <div class="label">{label} {badge_html}</div>
          <div class="value">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
