"""Sidebar: brand, API status, live agent mesh."""

import streamlit as st

from core.config import MODEL_NAME, gemini_api_key
from core.firestore import get_dashboard_counts


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown('<div class="brand">CleanTrace AI</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subbrand">Autonomous Civic Sentinel Mesh</div>',
            unsafe_allow_html=True,
        )

        api_key = gemini_api_key()
        if api_key:
            st.success("API key loaded from environment")
        else:
            st.error("Set GEMINI_API_KEY in .env")

        st.markdown(f"**Vision model:** {MODEL_NAME}")

        st.divider()
        st.markdown("### Agent mesh")
        status = st.session_state["agent_status"]
        for agent, tag_class in [
            ("Sentinel Agent", "tag-sentinel"),
            ("Civic Nudge Agent", "tag-civic"),
            ("Resolver Agent", "tag-resolver"),
        ]:
            active = status.get(agent, False)
            dot = "dot-on" if active else "dot-off"
            badge = "badge-ok" if active else "badge-off"
            state_text = "ACTIVE" if active else "IDLE"
            st.markdown(
                f'<div class="status-row">'
                f'<span class="dot {dot}"></span>'
                f'<span class="badge {badge}">{state_text}</span>'
                f'<span class="{tag_class}">{agent}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        st.markdown("### About")
        st.caption(
            "Citizens upload a street photo. Sentinel classifies waste, "
            "Civic Nudge scores the micro-zone and drafts an RWA notice, "
            "Resolver verifies cleanup from before/after images."
        )
        counts = get_dashboard_counts()
        st.metric("Open incidents", counts["open"])
        st.metric("Zones with strikes", counts["zones"])
