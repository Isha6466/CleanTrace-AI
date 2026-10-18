"""Authority desk: review incidents and verify cleanup."""

from typing import Optional

import streamlit as st
from google import genai
from PIL import Image

from agents.resolver import resolver_agent
from core.firestore import decrement_strike, update_report_status
from core.state import add_log


def render_tab_resolution(client: Optional[genai.Client]) -> None:
    st.markdown("## Authority & Resolution Desk")
    st.caption(
        "Review logged incidents, verify cleanup with before/after images, and resolve."
    )

    pending = [r for r in st.session_state["reports"] if r["status"] == "PENDING"]

    st.markdown("### Logged incidents")
    if st.session_state["reports"]:
        rows = [
            {
                "ID": r["id"],
                "Time": r["timestamp"],
                "Micro-Zone": r["micro_zone"],
                "Severity": r["severity_score"],
                "Strikes": r["strikes"],
                "Status": r["status"],
            }
            for r in st.session_state["reports"]
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No incidents logged yet.")

    st.divider()
    st.markdown("### Resolution workflow")
    if not pending:
        st.info("No pending incidents to resolve.")
        return

    options = {
        f"#{r['id']} — {r['micro_zone']} (sev {r['severity_score']}/10)": r
        for r in pending
    }
    selected_label = st.selectbox("Select a pending incident", list(options.keys()))
    selected = options[selected_label]

    st.markdown(
        f'**Selected:** Incident #{selected["id"]} · {selected["micro_zone"]} · '
        f"Severity {selected['severity_score']}/10 · Strikes {selected['strikes']}/3"
    )

    after_file = st.file_uploader(
        "Upload 'After Cleanup' photo", type=["png", "jpg", "jpeg"], key="after_uploader"
    )
    verify = st.button(
        "Verify Cleanup (Resolver Agent)",
        type="primary",
        use_container_width=True,
    )

    if not verify:
        return
    if not client:
        st.error("Gemini API client not initialised.")
        return
    if not after_file:
        st.error("Please upload an 'After Cleanup' photo.")
        return

    before_img = selected["image"]
    after_img = Image.open(after_file).convert("RGB")

    st.session_state["agent_status"]["Resolver Agent"] = True
    with st.spinner("Resolver Agent comparing Before & After images..."):
        result = resolver_agent(client, before_img, after_img)

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Verification Status", result["status"])
    with res_col2:
        st.metric("Confidence", f"{result['confidence']}%")
    st.markdown(f"**Reasoning:** {result['reasoning']}")

    if result["status"] == "RESOLVED":
        selected["status"] = "RESOLVED"
        mz = selected["micro_zone"]
        if st.session_state["strikes"].get(mz, 0) > 0:
            st.session_state["strikes"][mz] -= 1
            selected["strikes"] = st.session_state["strikes"][mz]
        update_report_status(selected["id"], "RESOLVED", selected["strikes"])
        decrement_strike(mz)
        add_log(
            "Resolver Agent",
            f"Incident #{selected['id']} RESOLVED — strike reduced for {mz}",
            "INFO",
        )
        st.success("Incident marked RESOLVED. Strike count reduced.")
    else:
        add_log(
            "Resolver Agent",
            f"Incident #{selected['id']} REJECTED — cleanup not verified",
            "WARN",
        )
        st.warning("Cleanup not verified. Incident remains PENDING.")
