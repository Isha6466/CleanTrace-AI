"""Coordinates the agent mesh for a single field report."""

import datetime
from typing import Any, Dict

from google import genai
from PIL import Image
import streamlit as st

from agents.civic_nudge import civic_nudge_agent
from agents.sentinel import sentinel_agent
from core.firestore import save_report
from core.state import add_log


def run_ingestion_triage(
    client: genai.Client,
    image: Image.Image,
    city: str,
    sector: str,
    micro_zone: str,
    location: str,
) -> Dict[str, Any]:
    """Sentinel inspects the photo; Civic Nudge logs the hotspot if waste is present."""
    st.session_state["agent_status"]["Sentinel Agent"] = True
    detection = sentinel_agent(client, image, location)

    result: Dict[str, Any] = {"detection": detection, "nudge": None, "incident": None}

    if not detection.get("waste_detected"):
        return result

    st.session_state["agent_status"]["Civic Nudge Agent"] = True
    nudge = civic_nudge_agent(
        {
            "micro_zone": micro_zone,
            "city": city,
            "sector": sector,
            "severity_score": detection["severity_score"],
            "summary": detection["summary"],
        }
    )
    result["nudge"] = nudge

    incident = {
        "id": len(st.session_state["reports"]) + 1,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "sector": sector,
        "micro_zone": micro_zone,
        "location": location,
        "severity_score": detection["severity_score"],
        "categories": detection["categories"],
        "summary": detection["summary"],
        "cleanliness_index": nudge["cleanliness_index"],
        "strikes": nudge["strikes"],
        "status": "PENDING",
        "image": image,
    }
    st.session_state["reports"].append(incident)
    save_report(incident)
    add_log(
        "Civic Nudge Agent",
        f"Incident #{incident['id']} logged — status PENDING",
        "INFO",
    )
    result["incident"] = incident
    return result
