import os
import json
import re

import google.generativeai as genai
from dotenv import load_dotenv

from app.ai.prompts import SYSTEM_PROMPT

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_document(text: str):

    prompt = f"""
{SYSTEM_PROMPT}

Government Notification:

{text}
"""

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    # Remove ```json and ```
    response_text = re.sub(r"^```json", "", response_text)
    response_text = re.sub(r"^```", "", response_text)
    response_text = re.sub(r"```$", "", response_text)

    response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except Exception:

        return {
            "raw_response": response_text
        }