"""Sentinel Agent — vision inspector for street-waste photographs."""

import json
from typing import Any, Dict

from google import genai
from PIL import Image

from core.config import MODEL_NAME, WASTE_CATEGORIES
from core.state import add_log


def sentinel_agent(client: genai.Client, image: Image.Image, location: str) -> Dict[str, Any]:
    """Detects waste in a street photo using strict JSON output."""
    add_log("Sentinel Agent", f"Received field report for {location}", "INFO")

    system_prompt = (
        "You are the Sentinel Agent, an autonomous civic vision inspector. "
        "Analyze the street-waste photograph and the reported location. "
        "Return ONLY a single valid JSON object (no markdown, no extra text) with exactly these keys:\n"
        "- waste_detected: boolean (true if any litter/dump/waste is visible)\n"
        f"- categories: list of strings from {WASTE_CATEGORIES}\n"
        "- severity_score: integer 1-10 (1 = minimal litter, 10 = severe illegal dumping)\n"
        "- summary: concise one-sentence summary of what is visible\n"
    )

    user_prompt = f"Location: {location}\nRespond with JSON only."

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[system_prompt, image, user_prompt],
        )
        text = response.text or "{}"
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        data.setdefault("waste_detected", False)
        data.setdefault("categories", [])
        data.setdefault("severity_score", 0)
        data.setdefault("summary", "No summary provided.")
        data["severity_score"] = max(0, min(10, int(data.get("severity_score", 0))))
        add_log(
            "Sentinel Agent",
            f"waste_detected={data['waste_detected']}, severity={data['severity_score']}, "
            f"categories={data['categories']}",
            "INFO",
        )
        return data
    except Exception as exc:
        add_log("Sentinel Agent", f"Analysis failed: {exc}", "ERROR")
        return {
            "waste_detected": False,
            "categories": [],
            "severity_score": 0,
            "summary": f"Sentinel analysis error: {exc}",
        }
