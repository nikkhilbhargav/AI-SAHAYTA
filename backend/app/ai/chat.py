import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_document(
    document_text: str,
    question: str
):

    prompt = f"""
You are AI Sahayta, an AI assistant for Government Jobs, Exams, and Official Notifications.

Your job is to answer ONLY using the uploaded document.

Rules:

1. Use ONLY the information available in the document.

2. Never make up facts.

3. If the answer is not present in the document, reply exactly:

"I could not find this information in the uploaded document."

4. Answer in a clear and well-formatted manner.

5. If possible, use bullet points.

6. Keep answers concise unless the user asks for details.

--------------------------------------------------------

DOCUMENT

{document_text}

--------------------------------------------------------

QUESTION

{question}

--------------------------------------------------------

ANSWER

"""

    response = model.generate_content(prompt)

    return response.text.strip()