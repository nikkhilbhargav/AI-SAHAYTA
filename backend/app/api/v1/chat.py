from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.auth.current_user import get_current_user
from app.models.user import User

from app.models.document import Document

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.ai.chat import ask_document


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


# -------------------------------------------------
# Chat With Uploaded Document
# -------------------------------------------------

@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = (
        db.query(Document)
        .filter(
            Document.id == request.document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    answer = ask_document(
        document_text=document.extracted_text,
        question=request.question
    )

    return ChatResponse(
        answer=answer
    )