import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_document(document_text: str, question: str):

    prompt = f"""
You are an AI Government Assistant.

Use ONLY the document below.

If the answer is not present,
reply:

"I could not find this information in the uploaded document."

DOCUMENT

{document_text}

QUESTION

{question}
"""

    response = model.generate_content(prompt)

    return response.text