"""
CleanTrace AI
Autonomous Multi-Agent Civic Governance & Waste Hotspot Mesh

Streamlit command desk. Agents live under /agents, shared runtime under /core.
"""

from core.client import get_client
from core.config import PAGE_ICON, PAGE_TITLE, gemini_api_key
from core.state import init_session_state
from ui.coordination import render_tab_coordination
from ui.hero import render_hero
from ui.ingestion import render_tab_ingestion
from ui.resolution import render_tab_resolution
from ui.sidebar import render_sidebar
from ui.styles import load_css

import streamlit as st


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
    )
    load_css()
    init_session_state()
    render_sidebar()
    render_hero()

    api_key = gemini_api_key()
    client = get_client(api_key) if api_key else None

    tab1, tab2, tab3 = st.tabs(
        [
            "Field Reporting",
            "Resolution Desk",
            "Coordination Stream",
        ]
    )

    with tab1:
        render_tab_ingestion(client)
    with tab2:
        render_tab_resolution(client)
    with tab3:
        render_tab_coordination()


if __name__ == "__main__":
    main()
