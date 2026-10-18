"""Resolver Agent — before/after cleanup verification officer."""

import json
from typing import Any, Dict

from google import genai
from PIL import Image

from core.config import MODEL_NAME
from core.state import add_log


def resolver_agent(
    client: genai.Client, before_img: Image.Image, after_img: Image.Image
) -> Dict[str, Any]:
    """Compares before/after cleanup photos and returns RESOLVED/REJECTED with confidence."""
    add_log("Resolver Agent", "Received before/after cleanup images for verification", "INFO")

    system_prompt = (
        "You are the Resolver Agent, an autonomous civic verification officer. "
        "You are given TWO photographs: a 'Before' image (waste present) and an 'After' image (post-cleanup). "
        "Determine whether the waste has been authentically cleared. "
        "Return ONLY a single valid JSON object (no markdown, no extra text) with exactly these keys:\n"
        "- status: string, either \"RESOLVED\" or \"REJECTED\"\n"
        "- confidence: integer 0-100 (verification confidence percentage)\n"
        "- reasoning: concise one-sentence explanation\n"
    )

    user_prompt = (
        "Compare the Before and After images. Has the waste been cleared? Respond with JSON only."
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[system_prompt, before_img, after_img, user_prompt],
        )
        text = response.text or "{}"
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        status = str(data.get("status", "REJECTED")).upper()
        if status not in ("RESOLVED", "REJECTED"):
            status = "REJECTED"
        data["status"] = status
        data["confidence"] = max(0, min(100, int(data.get("confidence", 0))))
        data.setdefault("reasoning", "No reasoning provided.")
        add_log("Resolver Agent", f"status={status}, confidence={data['confidence']}%", "INFO")
        return data
    except Exception as exc:
        add_log("Resolver Agent", f"Verification failed: {exc}", "ERROR")
        return {
            "status": "REJECTED",
            "confidence": 0,
            "reasoning": f"Resolver verification error: {exc}",
        }
