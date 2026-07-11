import json

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.document import Document


# ---------------------------------------
# Create Document
# ---------------------------------------

def create_document(
    db: Session,
    user_id: int,
    original_filename: str,
    saved_filename: str,
    file_hash: str,
    extracted_text: str,
    analysis: dict,
):

    document = Document(
        user_id=user_id,
        original_filename=original_filename,
        saved_filename=saved_filename,
        file_hash=file_hash,
        extracted_text=extracted_text,
        ai_analysis=json.dumps(analysis)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


# ---------------------------------------
# Duplicate Check
# ---------------------------------------

def get_document_by_hash(
    db: Session,
    user_id: int,
    file_hash: str
):

    return (
        db.query(Document)
        .filter(
            Document.user_id == user_id,
            Document.file_hash == file_hash
        )
        .first()
    )


# ---------------------------------------
# Document History
# ---------------------------------------

def get_user_documents(
    db: Session,
    user_id: int
):

    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )


# ---------------------------------------
# Get Single Document
# ---------------------------------------

def get_document_by_id(
    db: Session,
    document_id: int,
    user_id: int
):

    return (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user_id
        )
        .first()
    )


# ---------------------------------------
# Search Documents
# ---------------------------------------

def search_documents(
    db: Session,
    user_id: int,
    query: str
):

    return (
        db.query(Document)
        .filter(
            Document.user_id == user_id,
            or_(
                Document.original_filename.ilike(f"%{query}%"),
                Document.extracted_text.ilike(f"%{query}%")
            )
        )
        .order_by(Document.created_at.desc())
        .all()
    )


# ---------------------------------------
# Delete Document
# ---------------------------------------

def delete_document(
    db: Session,
    document: Document
):

    db.delete(document)
    db.commit()

    return True