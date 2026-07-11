from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.chat import ask_document


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    document_text: str
    question: str


@router.post("/")
def chat(request: ChatRequest):

    answer = ask_document(
        request.document_text,
        request.question
    )

    return {
        "answer": answer
    }