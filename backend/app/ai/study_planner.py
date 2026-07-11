import os
import json
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_study_plan(document_text: str):

    prompt = f"""
You are an expert Government Exam Mentor.

Read the government recruitment notification.

Generate a personalized study plan.

Return ONLY valid JSON.

Schema:

{{
    "study_duration": "",
    "daily_hours": "",
    "subjects": [],
    "weekly_plan": [],
    "revision_strategy": "",
    "mock_test_strategy": "",
    "important_books": [],
    "tips": []
}}

Notification:

{document_text}
"""

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    # Remove Markdown code block if Gemini returns ```json ... ```
    response_text = re.sub(r"^```json\s*", "", response_text)
    response_text = re.sub(r"^```\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)

    response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except Exception:
        return {
            "raw_response": response_text
        }