"""Gemini client factory."""

from typing import Optional

import streamlit as st
from google import genai


def get_client(api_key: Optional[str]) -> Optional[genai.Client]:
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as exc:
        st.error(f"Failed to initialise GenAI client: {exc}")
        return None
