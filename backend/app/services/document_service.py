from pathlib import Path
import shutil
import json
import hashlib
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.models.user import User

from app.extraction.extractor import extract_text
from app.ai.analyzer import analyze_document

from app.crud.document_crud import (
    create_document,
    get_document_by_hash,
    get_user_documents,
    get_document_by_id,
    search_documents,
    delete_document
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}


# ============================================================
# Upload Document
# ============================================================

async def upload_document(
    file: UploadFile,
    db: Session,
    current_user: User
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are allowed."
        )

    filename = f"{uuid4()}.{extension}"

    destination = UPLOAD_DIR / filename

    try:

        # Read uploaded file once
        file_bytes = await file.read()

        # SHA256 Hash
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Duplicate Check
        duplicate = get_document_by_hash(
            db=db,
            user_id=current_user.id,
            file_hash=file_hash
        )

        if duplicate:

            return {

                "message": "Document already uploaded.",

                "document_id": duplicate.id,

                "original_filename": duplicate.original_filename

            }

        # Save File
        with destination.open("wb") as buffer:
            buffer.write(file_bytes)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to save uploaded file. {str(e)}"
        )

    # ========================================================
    # OCR
    # ========================================================

    try:

        extracted_text = extract_text(
            str(destination)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Text Extraction Failed. {str(e)}"
        )

    if not extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in uploaded document."
        )

    # ========================================================
    # AI Analysis
    # ========================================================

    try:

        analysis = analyze_document(
            extracted_text
        )

    except Exception as e:

        analysis = {
            "error": str(e)
        }

    # ========================================================
    # Save to Database
    # ========================================================

    document = create_document(

        db=db,

        user_id=current_user.id,

        original_filename=file.filename,

        saved_filename=filename,

        file_hash=file_hash,

        extracted_text=extracted_text,

        analysis=analysis

    )

    return {

        "message": "Document Uploaded Successfully",

        "document_id": document.id,

        "user_id": current_user.id,

        "original_filename": file.filename,

        "saved_filename": filename,

        "file_type": extension,

        "text_length": len(extracted_text),

        "preview": extracted_text[:1000],

        "analysis": analysis

    }

# ============================================================
# Document History
# ============================================================

def document_history(
    db: Session,
    current_user: User
):

    documents = get_user_documents(
        db=db,
        user_id=current_user.id
    )

    history = []

    for doc in documents:

        history.append({

            "id": doc.id,

            "original_filename": doc.original_filename,

            "saved_filename": doc.saved_filename,

            "created_at": doc.created_at

        })

    return history


# ============================================================
# Get Single Document
# ============================================================

def get_single_document(
    db: Session,
    current_user: User,
    document_id: int
):

    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:

        analysis = json.loads(document.ai_analysis)

    except Exception:

        analysis = document.ai_analysis

    return {

        "id": document.id,

        "user_id": document.user_id,

        "original_filename": document.original_filename,

        "saved_filename": document.saved_filename,

        "preview": document.extracted_text[:2000],

        "analysis": analysis,

        "created_at": document.created_at

    }


# ============================================================
# Search Documents
# ============================================================

def search_document(
    db: Session,
    current_user: User,
    query: str
):

    documents = search_documents(
        db=db,
        user_id=current_user.id,
        query=query
    )

    results = []

    for doc in documents:

        results.append({

            "id": doc.id,

            "original_filename": doc.original_filename,

            "saved_filename": doc.saved_filename,

            "created_at": doc.created_at

        })

    return results


# ============================================================
# Download Document
# ============================================================

def download_document(
    db: Session,
    current_user: User,
    document_id: int
):

    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    file_path = UPLOAD_DIR / document.saved_filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found on server."
        )

    return FileResponse(
        path=file_path,
        filename=document.original_filename,
        media_type="application/pdf"
    )


# ============================================================
# Delete Document
# ============================================================

def delete_document_service(
    db: Session,
    current_user: User,
    document_id: int
):

    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    file_path = UPLOAD_DIR / document.saved_filename

    if file_path.exists():

        file_path.unlink()

    delete_document(
        db=db,
        document=document
    )

    return {

        "message": "Document deleted successfully."

    }