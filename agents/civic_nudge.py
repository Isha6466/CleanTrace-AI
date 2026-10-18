"""Civic Nudge Agent — cleanliness index, strike ledger, bilingual RWA notice."""

from typing import Any, Dict

from core.config import SURCHARGE_AMOUNT, SURCHARGE_THRESHOLD
from core.firestore import increment_strike
from core.state import add_log
import streamlit as st


def civic_nudge_agent(incident: Dict[str, Any]) -> Dict[str, Any]:
    """Computes cleanliness index, tracks strikes, and drafts a bilingual notice."""
    add_log(
        "Civic Nudge Agent",
        f"Computing index for micro-zone {incident['micro_zone']}",
        "INFO",
    )

    severity = int(incident.get("severity_score", 0))
    cleanliness_index = max(0, 100 - severity * 10)

    micro_zone = incident["micro_zone"]
    strikes = increment_strike(micro_zone)
    if strikes == 0:
        # Firestore not configured — fall back to session-state ledger
        strikes = st.session_state["strikes"].get(micro_zone, 0) + 1
    st.session_state["strikes"][micro_zone] = strikes

    surcharge_triggered = strikes > SURCHARGE_THRESHOLD

    notice = (
        f"🚨 RWA / RESIDENTS NOTICE — {micro_zone}\n\n"
        f"English:\n"
        f"Dear residents, waste has been reported in your micro-zone ({micro_zone}). "
        f"Cleanliness Index: {cleanliness_index}/100. Strike count: {strikes}/{SURCHARGE_THRESHOLD}. "
        f"Please keep your streets clean and dispose of waste responsibly. "
        f"Repeated violations may trigger a mandatory civic waste cess.\n\n"
        f"हिंदी:\n"
        f"प्रिय निवासियों, आपके माइक्रो-ज़ोन ({micro_zone}) में कचरा रिपोर्ट किया गया है। "
        f"स्वच्छता सूचकांक: {cleanliness_index}/100। स्ट्राइक गिनती: {strikes}/{SURCHARGE_THRESHOLD}। "
        f"कृपया अपनी सड़कों को साफ रखें और कचरा जिम्मेदारी से निपटाएं। "
        f"बार-बार उल्लंघन पर अनिवार्य नागरिक अपशिष्ट उपकर लागू हो सकता है।\n\n"
        f"Jai Hind — CleanTrace AI Civic Sentinel"
    )

    result = {
        "cleanliness_index": cleanliness_index,
        "strikes": strikes,
        "surcharge_triggered": surcharge_triggered,
        "notice": notice,
    }

    if surcharge_triggered:
        alert = (
            "⚠️ MANDATORY SANITATION SURCHARGE TRIGGERED: "
            f"Chronic dumping violation threshold breached (>{SURCHARGE_THRESHOLD} strikes). "
            f"Mandatory {SURCHARGE_AMOUNT} civic waste cess levied on micro-zone maintenance."
        )
        result["alert"] = alert
        add_log(
            "Civic Nudge Agent",
            f"SURCHARGE TRIGGERED for {micro_zone} (strikes={strikes})",
            "WARN",
        )
    else:
        add_log(
            "Civic Nudge Agent",
            f"strikes={strikes}/{SURCHARGE_THRESHOLD} for {micro_zone}, index={cleanliness_index}",
            "INFO",
        )

    return result
