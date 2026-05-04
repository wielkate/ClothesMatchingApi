import base64
import logging

import requests

from commons.constants import GEMINI_URL, MODEL, HEADERS

PROMPT = """
You are a clothing categorization assistant.
Look at this clothing item image and classify it into one of these categories:

- top: worn on the upper body as a base layer. Examples: t-shirt, shirt, blouse, tank top, polo
- bottom: worn on the lower body. Examples: pants, jeans, trousers, shorts, skirt, leggings
- mid_layer: worn over a top for style or light warmth. Examples: jacket, blazer, hoodie, cardigan, sweater
- outer_layer: worn as the outermost layer for weather protection. Examples: coat, raincoat, parka, puffer jacket, trench coat
- unknown: the item doesn't fit any category above, or you cannot identify it

Respond with ONLY one of these exact words:
"Top" | "Bottom" | "Mid layer" | "Outerwear" | "Unknown"

No explanation. No punctuation. Just the single category word.
"""


def get_payload(file):
    image_data = base64.b64encode(file.read()).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_data
                        }
                    }
                ]
            }
        ]
    }

    return payload


# Using REST
def get_clothes_tag(file) -> str:
    payload = get_payload(file)

    response = requests.post(
        url=f"{GEMINI_URL}/{MODEL}:generateContent",
        headers=HEADERS,
        json=payload
    ).json()

    text = response["candidates"][0]["content"]["parts"][0]["text"].strip()
    logging.info(f"Raw response from Gemini: {text}")

    allowed = {"Top", "Bottom", "Mid layer", "Outerwear", "Unknown"}
    return text if text in allowed else "Unknown"
