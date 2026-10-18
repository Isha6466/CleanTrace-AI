"""Session-scoped incident log, strikes, and agent coordination stream.

Reports and strikes are mirrored to Firestore when
FIRESTORE_CREDENTIALS_PATH is set so data persists across sessions.
"""

import datetime

import streamlit as st

from core.firestore import get_dashboard_counts, get_strike_count, load_reports


def init_session_state() -> None:
    if "reports" not in st.session_state:
        st.session_state["reports"] = load_reports() or []
    if "strikes" not in st.session_state:
        # Hydrate strike counts from Firestore for known micro-zones
        firestore_strikes = {}
        for r in st.session_state["reports"]:
            mz = r.get("micro_zone", "")
            if mz:
                firestore_strikes[mz] = get_strike_count(mz)
        st.session_state["strikes"] = firestore_strikes
    if "logs" not in st.session_state:
        st.session_state["logs"] = []
    if "agent_status" not in st.session_state:
        st.session_state["agent_status"] = {
            "Sentinel Agent": False,
            "Civic Nudge Agent": False,
            "Resolver Agent": False,
        }


def add_log(agent: str, message: str, level: str = "INFO") -> None:
    """Append a timestamped coordination-stream entry (newest first)."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state["logs"].insert(
        0,
        {
            "timestamp": timestamp,
            "agent": agent,
            "message": message,
            "level": level,
        },
    )
