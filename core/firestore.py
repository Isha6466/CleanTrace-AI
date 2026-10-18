"""Firestore persistence layer for CleanTrace AI.

Reads/writes reports and strike counts to Firestore so data survives
across sessions and Cloud Run instances. Falls back gracefully when
FIRESTORE_CREDENTIALS_PATH is not set.
"""

import os
from typing import Any, Dict, List, Optional

import streamlit as st

_db: Optional["firestore.Client"] = None


def _get_db():
    """Initialise and return a Firestore client, or None if not configured."""
    global _db
    if _db is not None:
        return _db
    cred_path = os.getenv("FIRESTORE_CREDENTIALS_PATH", "").strip()
    if not cred_path or not os.path.exists(cred_path):
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
        return _db
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Reports collection
# ---------------------------------------------------------------------------
def save_report(report: Dict[str, Any]) -> None:
    """Persist a single incident report to Firestore."""
    db = _get_db()
    if db is None:
        return
    try:
        # Store without the PIL image (not serialisable); keep a reference
        payload = {k: v for k, v in report.items() if k != "image"}
        db.collection("reports").document(str(report["id"])).set(payload)
    except Exception:
        return


def load_reports() -> List[Dict[str, Any]]:
    """Load all incident reports from Firestore."""
    db = _get_db()
    if db is None:
        return []
    try:
        docs = db.collection("reports").stream()
        reports = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = int(doc.id)
            reports.append(data)
        return sorted(reports, key=lambda r: r.get("id", 0))
    except Exception:
        return []


def update_report_status(report_id: int, status: str, strikes: int) -> None:
    """Update the status and strike count of an existing report."""
    db = _get_db()
    if db is None:
        return
    try:
        db.collection("reports").document(str(report_id)).update(
            {"status": status, "strikes": strikes}
        )
    except Exception:
        return


# ---------------------------------------------------------------------------
# Strikes collection (one doc per micro-zone)
# ---------------------------------------------------------------------------
def get_strike_count(micro_zone: str) -> int:
    """Read the current strike count for a micro-zone from Firestore."""
    db = _get_db()
    if db is None:
        return 0
    try:
        doc = db.collection("strikes").document(micro_zone).get()
        if doc.exists:
            return int(doc.to_dict().get("count", 0))
        return 0
    except Exception:
        return 0


def increment_strike(micro_zone: str) -> int:
    """Atomically increment and return the new strike count for a micro-zone."""
    db = _get_db()
    if db is None:
        return 0
    try:
        ref = db.collection("strikes").document(micro_zone)
        doc = ref.get()
        current = int(doc.to_dict().get("count", 0)) if doc.exists else 0
        new_count = current + 1
        ref.set({"count": new_count, "micro_zone": micro_zone})
        return new_count
    except Exception:
        return 0


def decrement_strike(micro_zone: str) -> int:
    """Decrement (floor at 0) and return the new strike count."""
    db = _get_db()
    if db is None:
        return 0
    try:
        ref = db.collection("strikes").document(micro_zone)
        doc = ref.get()
        current = int(doc.to_dict().get("count", 0)) if doc.exists else 0
        new_count = max(0, current - 1)
        ref.set({"count": new_count, "micro_zone": micro_zone})
        return new_count
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Counts for sidebar
# ---------------------------------------------------------------------------
def get_dashboard_counts() -> Dict[str, int]:
    """Return open incidents and zones-with-strikes counts from Firestore."""
    db = _get_db()
    if db is None:
        return {"open": 0, "zones": 0}
    try:
        reports = load_reports()
        open_count = sum(1 for r in reports if r.get("status") == "PENDING")
        zones = len({r.get("micro_zone", "") for r in reports if r.get("strikes", 0) > 0})
        return {"open": open_count, "zones": zones}
    except Exception:
        return {"open": 0, "zones": 0}