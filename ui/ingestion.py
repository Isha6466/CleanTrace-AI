"""Citizen & field reporting tab."""

from typing import Optional

import streamlit as st
from google import genai
from PIL import Image

from agents.orchestrator import run_ingestion_triage


def render_tab_ingestion(client: Optional[genai.Client]) -> None:
    st.markdown("## Citizen & Field Reporting")
    st.caption(
        "Submit a street-waste photo with hierarchical location details to trigger the multi-agent triage."
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        city = st.text_input("City", placeholder="e.g. Delhi, Mumbai, New York")
        sector = st.text_input(
            "Sector / Ward / Locality", placeholder="e.g. Rohini Sector 2, Andheri East"
        )
        micro_zone = st.text_input(
            "Micro-Zone / Pocket / Block / Street",
            placeholder="e.g. Pocket 5, Block B, 4th Crossroad",
        )
    with col2:
        image_file = st.file_uploader("Street waste photo", type=["png", "jpg", "jpeg"])
        camera_file = st.camera_input("Or snap a photo")
        image_source = image_file or camera_file

    location = " | ".join([p for p in [city, sector, micro_zone] if p])

    run_triage = st.button(
        "Run Multi-Agent Triage", type="primary", use_container_width=True
    )

    if not run_triage:
        return

    if not client:
        st.error("Gemini API client not initialised. Set GEMINI_API_KEY in .env.")
        return
    if not image_source:
        st.error("Please upload or capture a street-waste photo.")
        return
    if not micro_zone:
        st.error("Micro-Zone is required to log the incident.")
        return

    image = Image.open(image_source).convert("RGB")

    with st.spinner("Agent mesh running: Sentinel → Civic Nudge..."):
        result = run_ingestion_triage(client, image, city, sector, micro_zone, location)

    detection = result["detection"]
    st.divider()
    st.markdown("### Sentinel Agent — Detection Report")
    det_col1, det_col2, det_col3 = st.columns(3)
    with det_col1:
        st.metric("Waste Detected", "Yes" if detection["waste_detected"] else "No")
    with det_col2:
        st.metric("Severity Score", f"{detection['severity_score']} / 10")
    with det_col3:
        st.metric("Categories", ", ".join(detection["categories"]) or "—")
    st.markdown(f"**Summary:** {detection['summary']}")

    if not detection["waste_detected"]:
        st.info("No waste detected. Incident not logged.")
        return

    nudge = result["nudge"]
    st.divider()
    st.markdown("### Civic Nudge Agent — Zone Action")
    n_col1, n_col2 = st.columns(2)
    with n_col1:
        st.metric("Cleanliness Index", f"{nudge['cleanliness_index']} / 100")
    with n_col2:
        st.metric("Strike Count", f"{nudge['strikes']} / 3")

    if nudge["surcharge_triggered"]:
        st.markdown(
            f'<div class="alert"><b>{nudge["alert"]}</b></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### WhatsApp / RWA Notice Draft (Hindi + English)")
    st.markdown(f'<div class="notice">{nudge["notice"]}</div>', unsafe_allow_html=True)

    incident = result["incident"]
    st.success(f"Incident #{incident['id']} saved. Status: PENDING")
