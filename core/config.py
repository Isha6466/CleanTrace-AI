"""Runtime configuration for CleanTrace AI."""

import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
WASTE_CATEGORIES = ["plastic", "organic", "debris", "animal dung", "mixed"]
PAGE_TITLE = "CleanTrace AI"
PAGE_ICON = "🧹"
SURCHARGE_THRESHOLD = 3
SURCHARGE_AMOUNT = "₹5,000/month"


def gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "").strip()
