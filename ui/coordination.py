"""Live inter-agent message stream."""

import streamlit as st


def render_tab_coordination() -> None:
    st.markdown("## Multi-Agent Coordination Stream")
    st.caption(
        "Timeline of message passing: Sentinel → Civic Nudge → Resolver."
    )

    logs = st.session_state["logs"]
    if not logs:
        st.info("No coordination events yet. Run a triage in the first tab to generate logs.")
        return

    tag_class = {
        "Sentinel Agent": "tag-sentinel",
        "Civic Nudge Agent": "tag-civic",
        "Resolver Agent": "tag-resolver",
    }
    for entry in logs:
        agent = entry["agent"]
        cls = tag_class.get(agent, "")
        level = entry["level"]
        level_color = {
            "INFO": "#38bdf8",
            "WARN": "#fbbf24",
            "ERROR": "#fb7185",
        }.get(level, "#94a3b8")
        st.markdown(
            f'<div class="log-entry">'
            f'<span style="color:{level_color}">[{entry["timestamp"]}]</span> '
            f'<span class="{cls}"><b>{agent}</b></span> → '
            f'{entry["message"]}'
            f"</div>",
            unsafe_allow_html=True,
        )
