from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.extraction.extractor import extract_text
from app.ai.analyzer import analyze_document
from app.crud.document_crud import create_document


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}


async def upload_document(
    file: UploadFile,
    db: Session
):

    # -------------------------
    # Validate File
    # -------------------------

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

    # -------------------------
    # Generate Unique Filename
    # -------------------------

    filename = f"{uuid4()}.{extension}"

    destination = UPLOAD_DIR / filename

    # -------------------------
    # Save File
    # -------------------------

    try:

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to save uploaded file. {str(e)}"
        )

    # -------------------------
    # Extract Text
    # -------------------------

    try:

        extracted_text = extract_text(str(destination))

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

    # -------------------------
    # AI Analysis
    # -------------------------

    try:

        analysis = analyze_document(extracted_text)

    except Exception as e:

        analysis = {
            "error": str(e)
        }

    # -------------------------
    # Save in PostgreSQL
    # -------------------------

    try:

        document = create_document(
            db=db,
            user_id=1,   # Temporary (JWT login ke baad dynamic hoga)
            original_filename=file.filename,
            saved_filename=filename,
            extracted_text=extracted_text,
            analysis=analysis
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    # -------------------------
    # Response
    # -------------------------

    return {

        "message": "Document Uploaded Successfully",

        "document_id": document.id,

        "original_filename": file.filename,

        "saved_filename": filename,

        "file_type": extension,

        "text_length": len(extracted_text),

        "preview": extracted_text[:1000],

        "analysis": analysis
    }