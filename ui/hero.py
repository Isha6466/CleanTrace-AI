"""Top-of-page brand banner."""

import streamlit as st


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Civic governance · Multi-agent mesh</div>
          <div class="hero-title">🧹 CleanTrace <span>AI</span></div>
          <div class="hero-sub">
            Autonomous waste-hotspot intelligence for cities: ingest a street photo,
            triage the micro-zone, nudge residents, and verify cleanup.
          </div>
          <div class="pipeline">
            <span class="pipe">1 · Sentinel vision</span>
            <span class="pipe">2 · Civic Nudge</span>
            <span class="pipe">3 · Resolver verify</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
