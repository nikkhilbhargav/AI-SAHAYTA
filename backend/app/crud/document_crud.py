import json

from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    user_id: int,
    original_filename: str,
    saved_filename: str,
    extracted_text: str,
    analysis: dict,
):

    document = Document(
        user_id=user_id,
        original_filename=original_filename,
        saved_filename=saved_filename,
        extracted_text=extracted_text,
        ai_analysis=json.dumps(analysis)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document